import os
import uuid
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import pymupdf as fitz
from questions import (
    STANDARD_QUESTIONS,
    get_standard_questions,
    build_mixed_quiz,
    ConceptQuestionGenerator
)

app = Flask(__name__)
app.secret_key = "adaptive_quiz_secret_key_btech_cse"
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
generator = ConceptQuestionGenerator()

ALLOWED_EXTENSIONS = {"pdf"}

# Fast in-memory lookup for standard questions
STANDARD_BY_ID = {q["id"]: q for q in STANDARD_QUESTIONS}

# Server-side storage for PDF questions to avoid overflowing the 4KB client cookie limit
PDF_STORE = {}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_pdf_text(filepath):
    """Extracts raw text from PDF using PyMuPDF."""
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    doc.close()
    return text


def get_pool(source, pdf_id=None):
    """Returns the available list of questions for standard or PDF sources."""
    if source == "pdf" and pdf_id:
        return PDF_STORE.get(pdf_id, [])
    return get_standard_questions()


def get_question_by_id(source, pdf_id, q_id):
    """Retrieves a single question dictionary by its unique identifier."""
    if source == "pdf" and pdf_id:
        pdf_list = PDF_STORE.get(pdf_id, [])
        for q in pdf_list:
            if str(q["id"]) == str(q_id):
                return q
        return None
    return STANDARD_BY_ID.get(q_id)


def pick_adaptive_question(pool, target_diff, used_ids):
    """
    Selects an unused question matching target difficulty.
    Falls back gracefully to neighboring difficulty if the target pool is exhausted.
    """
    used_set = set(used_ids)
    fallback_order = {
        "Easy": ["Easy", "Medium", "Hard"],
        "Medium": ["Medium", "Easy", "Hard"],
        "Hard": ["Hard", "Medium", "Easy"]
    }.get(target_diff, ["Easy", "Medium", "Hard"])

    for diff in fallback_order:
        candidates = [q for q in pool if q.get("difficulty") == diff and q["id"] not in used_set]
        if candidates:
            return random.choice(candidates)

    remaining = [q for q in pool if q["id"] not in used_set]
    return random.choice(remaining) if remaining else None


@app.route("/")
def index():
    return render_template(
        "index.html",
        total_standard_questions=len(STANDARD_QUESTIONS)
    )


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "pdf_file" not in request.files:
            flash("No file part provided in the upload request.")
            return redirect(request.url)

        file = request.files["pdf_file"]
        if file.filename == "":
            flash("No file selected. Please choose a PDF file.")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            try:
                raw_text = extract_pdf_text(filepath)
            except Exception as e:
                flash(f"Error reading PDF file: {str(e)}")
                return redirect(request.url)

            # Generate all valid unique MCQs from the PDF without artificial caps
            questions = generator.generate_questions(raw_text)

            if not questions:
                flash("Could not extract reliable concept questions from this PDF. Please ensure the document has clear definitional sentences or upload a different study guide.")
                return redirect(request.url)

            # Store generated questions in server-side PDF_STORE, storing only pdf_id in session
            pdf_id = str(uuid.uuid4())
            PDF_STORE[pdf_id] = questions
            session["pdf_id"] = pdf_id
            session["pdf_filename"] = filename

            return redirect(url_for("configure", source="pdf"))
        else:
            flash("Invalid file format. Please upload a PDF document (.pdf).")
            return redirect(request.url)

    return render_template("upload.html")


@app.route("/configure", methods=["GET", "POST"])
def configure():
    source = request.args.get("source", "standard")
    if request.method == "POST":
        source = request.form.get("source", "standard")

    # Determine question source pool and limits
    if source == "pdf":
        pdf_id = session.get("pdf_id")
        available_questions = get_pool("pdf", pdf_id)
        if not available_questions:
            flash("No uploaded PDF questions found. Please upload a PDF document first.")
            return redirect(url_for("upload"))
        max_available = len(available_questions)
        source_title = session.get("pdf_filename", "Uploaded PDF Document")
        is_pdf = True
    else:
        source = "standard"
        pdf_id = None
        available_questions = get_pool("standard")
        max_available = len(available_questions)
        source_title = "Standard B.Tech CSE Question Bank"
        is_pdf = False

    if request.method == "POST":
        mode = request.form.get("mode", "adaptive")
        if mode not in ("adaptive", "mixed"):
            mode = "adaptive"

        # Validate question count
        raw_count = request.form.get("question_count", "10")
        try:
            target_count = int(raw_count)
        except ValueError:
            flash("Please enter a valid numeric question count.")
            return redirect(url_for("configure", source=source))

        if target_count < 1:
            flash("Quiz length must be at least 1 question.")
            return redirect(url_for("configure", source=source))

        if target_count > max_available:
            flash(
                f"Requested length ({target_count}) exceeds the {max_available} available unique questions for this source. "
                f"Unrelated questions will not be inserted, and questions are not duplicated. "
                f"Please choose a number between 1 and {max_available}."
            )
            return redirect(url_for("configure", source=source))

        # Setup new quiz session state with lightweight IDs
        session["quiz_source"] = source
        session["quiz_mode"] = mode
        session["total_questions"] = target_count
        session["current_index"] = 0
        session["score"] = 0
        session["answers"] = []
        session["review_queue_ids"] = []
        session["feedback"] = None
        session["review_index"] = 0

        if mode == "mixed":
            # Select balanced combination across Easy, Medium, Hard
            selected_qs = build_mixed_quiz(available_questions, target_count)
            session["quiz_question_ids"] = [q["id"] for q in selected_qs]
            session["current_difficulty"] = selected_qs[0].get("difficulty", "Medium")
        else:
            # Adaptive Mode: start at Easy
            session["used_question_ids"] = []
            session["current_difficulty"] = "Easy"
            first_q = pick_adaptive_question(available_questions, "Easy", used_ids=[])
            if not first_q:
                first_q = available_questions[0]
            session["current_q_id"] = first_q["id"]
            session["used_question_ids"] = [first_q["id"]]

        return redirect(url_for("quiz"))

    # Preset lengths filtered by availability
    all_presets = [5, 10, 15, 20]
    default_count = min(10, max_available) if max_available >= 5 else max_available

    return render_template(
        "configure.html",
        source=source,
        source_title=source_title,
        max_available=max_available,
        all_presets=all_presets,
        default_count=default_count,
        is_pdf=is_pdf
    )


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    total_questions = session.get("total_questions")
    current_index = session.get("current_index", 0)
    mode = session.get("quiz_mode", "adaptive")
    source = session.get("quiz_source", "standard")
    pdf_id = session.get("pdf_id")

    if not total_questions:
        flash("No active quiz session found. Please configure your quiz first.")
        return redirect(url_for("index"))

    # Completion check: navigate to results once all configured questions are completed
    if current_index >= total_questions:
        return redirect(url_for("result"))

    # Retrieve current question according to mode
    if mode == "mixed":
        q_ids = session.get("quiz_question_ids", [])
        if not q_ids or current_index >= len(q_ids):
            return redirect(url_for("result"))
        current_q = get_question_by_id(source, pdf_id, q_ids[current_index])
    else:
        current_q_id = session.get("current_q_id")
        current_q = get_question_by_id(source, pdf_id, current_q_id)

    if not current_q:
        return redirect(url_for("result"))

    difficulty = current_q.get("difficulty", "Medium")

    if request.method == "POST":
        # Handle 'Next Question' or 'View Results' transition
        if "next" in request.form:
            session["feedback"] = None
            session["current_index"] += 1
            new_index = session["current_index"]

            if new_index >= total_questions:
                # Finished all configured questions -> navigate to results
                return redirect(url_for("result"))

            if mode == "adaptive":
                # Select the next question adaptively
                target_diff = session.get("next_difficulty", "Easy")
                pool = get_pool(source, pdf_id)
                used_ids = session.get("used_question_ids", [])
                next_q = pick_adaptive_question(pool, target_diff, used_ids)
                if not next_q:
                    # Pool exhausted
                    return redirect(url_for("result"))
                session["current_q_id"] = next_q["id"]
                session["current_difficulty"] = next_q.get("difficulty", target_diff)
                used_ids.append(next_q["id"])
                session["used_question_ids"] = used_ids

            return redirect(url_for("quiz"))

        # Process user option submission
        selected_option = request.form.get("option")
        if not selected_option:
            flash("Please choose an answer option before checking.")
            return redirect(url_for("quiz"))

        is_correct = (selected_option == current_q["correct_answer"])

        if is_correct:
            session["score"] += 1
            if mode == "adaptive":
                if difficulty == "Easy":
                    next_diff = "Medium"
                elif difficulty == "Medium":
                    next_diff = "Hard"
                else:
                    next_diff = "Hard"
                session["next_difficulty"] = next_diff
        else:
            review_queue_ids = session.get("review_queue_ids", [])
            if current_q["id"] not in review_queue_ids:
                review_queue_ids.append(current_q["id"])
                session["review_queue_ids"] = review_queue_ids

            if mode == "adaptive":
                if difficulty == "Hard":
                    next_diff = "Medium"
                elif difficulty == "Medium":
                    next_diff = "Easy"
                else:
                    next_diff = "Easy"
                session["next_difficulty"] = next_diff

        correct_key = current_q["correct_answer"]
        correct_text = current_q["options"].get(correct_key, "")
        selected_text = current_q["options"].get(selected_option, "")
        explanation = current_q.get("explanation", "")
        is_last = (current_index + 1 >= total_questions)

        session["feedback"] = {
            "is_correct": is_correct,
            "selected_key": selected_option,
            "selected_text": selected_text,
            "correct_key": correct_key,
            "correct_text": correct_text,
            "concept": current_q.get("concept", "Concept"),
            "explanation": explanation,
            "is_last": is_last
        }

        answers = session.get("answers", [])
        answers.append({
            "id": current_q["id"],
            "selected": selected_option,
            "is_correct": is_correct
        })
        session["answers"] = answers

        return redirect(url_for("quiz"))

    return render_template(
        "quiz.html",
        question=current_q,
        index=current_index + 1,
        total=total_questions,
        remaining=total_questions - (current_index + 1),
        progress_percent=round(((current_index + 1) / total_questions) * 100, 1),
        difficulty=difficulty,
        mode=mode,
        feedback=session.get("feedback"),
        is_review=False
    )


@app.route("/review_round", methods=["GET", "POST"])
def review_round():
    review_queue_ids = session.get("review_queue_ids", [])
    review_index = session.get("review_index", 0)
    source = session.get("quiz_source", "standard")
    pdf_id = session.get("pdf_id")

    if not review_queue_ids or review_index >= len(review_queue_ids):
        flash("You have completed reviewing all incorrect answers! 🎉")
        return redirect(url_for("result"))

    current_q_id = review_queue_ids[review_index]
    current_q = get_question_by_id(source, pdf_id, current_q_id)
    if not current_q:
        return redirect(url_for("result"))

    total_reviews = len(review_queue_ids)

    if request.method == "POST":
        if "next" in request.form:
            session["feedback"] = None
            session["review_index"] += 1
            if session["review_index"] >= total_reviews:
                flash("Great job! All missed questions have been reviewed and reinforced. 🌟")
                return redirect(url_for("result"))
            return redirect(url_for("review_round"))

        selected_option = request.form.get("option")
        if not selected_option:
            flash("Please choose an answer option.")
            return redirect(url_for("review_round"))

        is_correct = (selected_option == current_q["correct_answer"])
        correct_key = current_q["correct_answer"]
        correct_text = current_q["options"].get(correct_key, "")
        selected_text = current_q["options"].get(selected_option, "")
        explanation = current_q.get("explanation", "")
        is_last = (review_index + 1 >= total_reviews)

        session["feedback"] = {
            "is_correct": is_correct,
            "selected_key": selected_option,
            "selected_text": selected_text,
            "correct_key": correct_key,
            "correct_text": correct_text,
            "concept": current_q.get("concept", "Concept"),
            "explanation": explanation,
            "is_last": is_last
        }

        return redirect(url_for("review_round"))

    return render_template(
        "quiz.html",
        question=current_q,
        index=review_index + 1,
        total=total_reviews,
        remaining=total_reviews - (review_index + 1),
        progress_percent=round(((review_index + 1) / total_reviews) * 100, 1),
        difficulty="Mistake Review",
        mode="Review",
        feedback=session.get("feedback"),
        is_review=True
    )


@app.route("/start_review")
def start_review():
    """Resets review round pointer and launches interactive mistake review."""
    session["review_index"] = 0
    session["feedback"] = None
    return redirect(url_for("review_round"))


@app.route("/result")
def result():
    stored_answers = session.get("answers", [])
    score = session.get("score", 0)
    total = session.get("total_questions", len(stored_answers))
    percentage = round((score / total) * 100, 1) if total > 0 else 0
    review_queue_ids = session.get("review_queue_ids", [])
    mode = session.get("quiz_mode", "adaptive")
    source = session.get("quiz_source", "standard")
    pdf_id = session.get("pdf_id")

    # Reconstruct rich answer details from stored IDs
    detailed_answers = []
    breakdown = {
        "Easy": {"total": 0, "correct": 0},
        "Medium": {"total": 0, "correct": 0},
        "Hard": {"total": 0, "correct": 0}
    }

    for item in stored_answers:
        q = get_question_by_id(source, pdf_id, item["id"])
        if q:
            diff = q.get("difficulty", "Medium")
            is_c = item.get("is_correct", False)
            if diff in breakdown:
                breakdown[diff]["total"] += 1
                if is_c:
                    breakdown[diff]["correct"] += 1

            correct_k = q["correct_answer"]
            selected_k = item.get("selected", "")
            detailed_answers.append({
                "id": q["id"],
                "question": q["question"],
                "selected": selected_k,
                "selected_text": q["options"].get(selected_k, ""),
                "correct": correct_k,
                "correct_text": q["options"].get(correct_k, ""),
                "is_correct": is_c,
                "difficulty": diff,
                "concept": q.get("concept", ""),
                "explanation": q.get("explanation", "")
            })

    return render_template(
        "result.html",
        score=score,
        total=total,
        percentage=percentage,
        answers=detailed_answers,
        review_count=len(review_queue_ids),
        mode=mode,
        source=source,
        breakdown=breakdown
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
