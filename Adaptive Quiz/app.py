import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

import db
from db import SUBJECTS, get_questions_by_subject, get_question
from gemini_service import process_pdf_material, is_gemini_configured

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "quizzly_edtech_secret_key_2026")
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize SQLite database and question bank on startup
db.init_db()

ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def select_adaptive_question(pool, target_diff, used_ids):
    """
    Selects an unused question matching target difficulty.
    Falls back gracefully to neighboring difficulties if the target difficulty is exhausted.
    """
    used_set = set(used_ids)
    fallback_map = {
        "Easy": ["Easy", "Medium", "Hard"],
        "Medium": ["Medium", "Easy", "Hard"],
        "Hard": ["Hard", "Medium", "Easy"]
    }
    order = fallback_map.get(target_diff, ["Easy", "Medium", "Hard"])

    for diff in order:
        candidates = [q for q in pool if q.get("difficulty") == diff and q["id"] not in used_set]
        if candidates:
            return random.choice(candidates)

    remaining = [q for q in pool if q["id"] not in used_set]
    return random.choice(remaining) if remaining else None

def build_mixed_quiz(pool, target_count):
    """
    Selects a balanced combination of Easy, Medium, and Hard questions
    without repeating any question IDs.
    """
    easy_pool = [q for q in pool if q.get("difficulty") == "Easy"]
    med_pool = [q for q in pool if q.get("difficulty") == "Medium"]
    hard_pool = [q for q in pool if q.get("difficulty") == "Hard"]

    easy_target = target_count // 3
    med_target = target_count // 3
    hard_target = target_count - (easy_target + med_target)

    selected = []
    e_take = min(easy_target, len(easy_pool))
    m_take = min(med_target, len(med_pool))
    h_take = min(hard_target, len(hard_pool))

    if e_take > 0: selected.extend(random.sample(easy_pool, e_take))
    if m_take > 0: selected.extend(random.sample(med_pool, m_take))
    if h_take > 0: selected.extend(random.sample(hard_pool, h_take))

    if len(selected) < target_count:
        used_ids = {q["id"] for q in selected}
        rem = [q for q in pool if q["id"] not in used_ids]
        needed = target_count - len(selected)
        if rem and needed > 0:
            selected.extend(random.sample(rem, min(needed, len(rem))))

    random.shuffle(selected)
    return selected

# ==================== MAIN APPLICATION ROUTES ====================

@app.route("/")
def index():
    """Main dashboard displaying real SQLite stats, resume card, and subjects."""
    analytics = db.get_analytics()
    active_sess = db.get_active_session()
    return render_template(
        "dashboard.html",
        analytics=analytics,
        active_session=active_sess,
        subject_names=SUBJECTS
    )

@app.route("/subjects")
def subjects_list():
    """Displays subject catalog with question difficulty counts."""
    data = {}
    for code, name in SUBJECTS.items():
        qs = get_questions_by_subject(code)
        counts = {"Easy": 0, "Medium": 0, "Hard": 0}
        for q in qs:
            d = q.get("difficulty", "Medium")
            if d in counts: counts[d] += 1
        icon_map = {
            "python": "🐍",
            "data_structures": "🌲",
            "coa": "⚡",
            "dstl": "📐",
            "mathematics": "🔢"
        }
        desc_map = {
            "python": "Core syntax, data types, OOP, decorators, generators, and asyncio event loops.",
            "data_structures": "Arrays, stacks, queues, BSTs, AVL balancing, Heaps, and Graph algorithms.",
            "coa": "Instruction cycles, addressing modes, pipelining hazards, cache, and virtual memory.",
            "dstl": "Propositional logic, sets, relations, equivalence, Posets, lattices, and recurrence.",
            "mathematics": "Linear algebra, matrix rank, calculus limits, Bayes' theorem, and distributions."
        }
        data[code] = {
            "name": name,
            "icon": icon_map.get(code, "📚"),
            "desc": desc_map.get(code, ""),
            "counts": counts,
            "total": len(qs)
        }
    return render_template("subjects_list.html", subjects_data=data)

@app.route("/configure", methods=["GET", "POST"])
def configure():
    """Quiz setup: question count, mode (Adaptive/Mixed), and timer options."""
    subject = request.args.get("subject") or request.form.get("subject", "python")
    doc_id = request.args.get("doc_id") or request.form.get("doc_id")

    # Fetch available question pool
    if subject == "pdf" and doc_id:
        pool = db.get_pdf_questions(doc_id)
        source_title = "Uploaded Study Notes (PDF)"
    else:
        subject = subject if subject in SUBJECTS else "python"
        pool = get_questions_by_subject(subject)
        source_title = SUBJECTS.get(subject, "Subject Quiz")

    max_available = len(pool)
    if max_available == 0:
        flash("No questions found for this source. Please try another subject or upload your notes.", "warning")
        return redirect(url_for("index"))

    if request.method == "POST":
        mode = request.form.get("mode", "adaptive")
        if mode not in ("adaptive", "mixed"):
            mode = "adaptive"

        # Validate count
        raw_count = request.form.get("question_count", "10")
        try:
            target_count = int(raw_count)
        except ValueError:
            flash("Please enter a valid numeric question count.", "error")
            return redirect(url_for("configure", subject=subject, doc_id=doc_id))

        if target_count < 1:
            flash("Question count must be at least 1.", "error")
            return redirect(url_for("configure", subject=subject, doc_id=doc_id))

        if target_count > max_available:
            flash(f"Requested count ({target_count}) exceeds available {max_available} unique questions.", "error")
            return redirect(url_for("configure", subject=subject, doc_id=doc_id))

        # Timer setup
        timer_mode = request.form.get("timer_mode", "untimed")
        is_timed = (timer_mode == "timed")
        time_limit_seconds = 0
        if is_timed:
            try:
                mins = int(request.form.get("time_limit_minutes", "10"))
                time_limit_seconds = max(60, min(mins * 60, 3600))
            except ValueError:
                time_limit_seconds = 600

        # Build initial question list
        if mode == "mixed":
            chosen = build_mixed_quiz(pool, target_count)
            question_ids = [q["id"] for q in chosen]
        else:
            first_q = select_adaptive_question(pool, "Easy", used_ids=[])
            if not first_q: first_q = pool[0]
            question_ids = [first_q["id"]]

        # Persist session into SQLite
        session_id = db.create_quiz_session(
            subject=subject,
            mode=mode,
            total_questions=target_count,
            question_ids=question_ids,
            is_timed=is_timed,
            time_limit_seconds=time_limit_seconds,
            pdf_doc_id=doc_id if subject == "pdf" else None
        )

        session["active_session_id"] = session_id
        session["feedback"] = None
        return redirect(url_for("quiz"))

    default_count = min(10, max_available) if max_available >= 5 else max_available
    return render_template(
        "configure.html",
        subject=subject,
        doc_id=doc_id,
        source_title=source_title,
        max_available=max_available,
        default_count=default_count
    )

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Upload PDF study material (standard text, scanned, or handwritten)."""
    if request.method == "POST":
        if "pdf_file" not in request.files:
            flash("No file part provided.", "error")
            return redirect(request.url)

        file = request.files["pdf_file"]
        if file.filename == "":
            flash("No file selected. Please choose a PDF.", "error")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Process document via PyMuPDF + Gemini Multimodal Vision
            result = process_pdf_material(filepath, target_count=12)

            if result["error"] or not result["questions"]:
                flash(result["error"] or "Could not extract valid questions from this document.", "error")
                return redirect(request.url)

            # Register PDF document and save generated questions into SQLite
            doc_id = db.save_pdf_document(
                filename=filename,
                stored_path=filepath,
                page_count=result["page_count"],
                is_scanned_or_handwritten=1 if result["is_scanned_or_handwritten"] else 0,
                extraction_method=result["method"]
            )
            db.save_pdf_questions(doc_id, result["questions"])

            method_label = "Gemini Multimodal AI" if "gemini" in result["method"] else "Quizzly Engine"
            flash(f"Successfully generated {len(result['questions'])} validated concept questions via {method_label}!", "success")
            return redirect(url_for("configure", subject="pdf", doc_id=doc_id))
        else:
            flash("Invalid format. Please upload a PDF file (.pdf).", "error")
            return redirect(request.url)

    return render_template("upload.html")

# ==================== QUIZ EXECUTION & ADAPTIVE LOGIC ====================

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Interactive quiz screen with real-time feedback and dynamic difficulty adaptation."""
    session_id = session.get("active_session_id")
    if not session_id:
        active = db.get_active_session()
        if active:
            session_id = active["session_id"]
            session["active_session_id"] = session_id
        else:
            flash("No active quiz session found. Please start a quiz.", "warning")
            return redirect(url_for("index"))

    quiz_sess = db.get_session(session_id)
    if not quiz_sess or quiz_sess["status"] == "completed":
        flash("This quiz has been completed.", "info")
        return redirect(url_for("result"))

    # If paused, mark in_progress upon student visit
    if quiz_sess["status"] == "paused":
        db.update_session(session_id, {"status": "in_progress"})
        quiz_sess["status"] = "in_progress"

    total = quiz_sess["total_questions"]
    current_index = quiz_sess["current_index"]
    mode = quiz_sess["mode"]

    # Check if all questions are finished
    if current_index >= total:
        return redirect(url_for("finish_main_quiz"))

    # Fetch current question
    q_ids = quiz_sess["question_ids"]
    current_q_id = q_ids[current_index]
    current_q = get_question(current_q_id)
    if not current_q:
        return redirect(url_for("finish_main_quiz"))

    if request.method == "POST":
        action = request.form.get("action")

        # 1. Next Question transition
        if action == "next":
            session["feedback"] = None
            new_index = current_index + 1
            updates = {"current_index": new_index}

            # Update remaining time if timed
            if quiz_sess["is_timed"]:
                try:
                    time_rem = int(request.form.get("time_remaining", quiz_sess["time_remaining_seconds"]))
                    updates["time_remaining_seconds"] = max(0, time_rem)
                except ValueError:
                    pass

            if new_index >= total:
                db.update_session(session_id, updates)
                return redirect(url_for("finish_main_quiz"))

            # In Adaptive mode: pick the next question dynamically
            if mode == "adaptive":
                target_diff = session.get("next_difficulty", "Easy")
                if quiz_sess["subject"] == "pdf":
                    pool = db.get_pdf_questions(quiz_sess["pdf_doc_id"])
                else:
                    pool = get_questions_by_subject(quiz_sess["subject"])

                next_q = select_adaptive_question(pool, target_diff, q_ids)
                if next_q:
                    q_ids.append(next_q["id"])
                    updates["question_ids"] = q_ids
                    updates["current_difficulty"] = next_q["difficulty"]

            db.update_session(session_id, updates)
            return redirect(url_for("quiz"))

        # 2. Check Answer submission
        selected_option = request.form.get("option")
        if not selected_option:
            flash("Please select an answer choice.", "warning")
            return redirect(url_for("quiz"))

        is_correct = (selected_option == current_q["correct_answer"])

        # Update remaining time from form
        if quiz_sess["is_timed"]:
            try:
                time_rem = int(request.form.get("time_remaining", quiz_sess["time_remaining_seconds"]))
                db.update_session(session_id, {"time_remaining_seconds": max(0, time_rem)})
            except ValueError:
                pass

        # Record answer in SQLite (prevents double scoring)
        db.record_answer(
            session_id=session_id,
            question_id=current_q["id"],
            question_order=current_index + 1,
            selected_option=selected_option,
            is_correct=is_correct,
            is_review=0
        )

        # Update score and adaptive difficulty
        new_score = quiz_sess["score"] + (1 if is_correct else 0)
        updates = {"score": new_score}

        current_diff = current_q.get("difficulty", "Medium")
        if is_correct:
            next_diff = "Medium" if current_diff == "Easy" else "Hard"
        else:
            next_diff = "Medium" if current_diff == "Hard" else "Easy"

        session["next_difficulty"] = next_diff
        updates["current_difficulty"] = next_diff
        db.update_session(session_id, updates)

        session["feedback"] = {
            "is_correct": is_correct,
            "selected_key": selected_option,
            "correct_key": current_q["correct_answer"],
            "correct_text": current_q["options"].get(current_q["correct_answer"], ""),
            "explanation": current_q.get("explanation", "")
        }

        return redirect(url_for("quiz"))

    # Render quiz question view
    return render_template(
        "quiz.html",
        quiz_session=quiz_sess,
        question=current_q,
        index=current_index + 1,
        total=total,
        remaining=total - (current_index + 1),
        progress_percent=round(((current_index + 1) / total) * 100, 1),
        difficulty=current_q.get("difficulty", "Medium"),
        mode=mode,
        feedback=session.get("feedback"),
        is_last=(current_index + 1 >= total)
    )

@app.route("/quiz/pause", methods=["POST"])
def pause_quiz():
    """Pauses active session, saving time and state to SQLite."""
    session_id = session.get("active_session_id")
    if session_id:
        updates = {"status": "paused"}
        try:
            time_rem = int(request.form.get("time_remaining", "0"))
            updates["time_remaining_seconds"] = max(0, time_rem)
        except ValueError:
            pass
        db.update_session(session_id, updates)
        flash("Quiz successfully paused. You can resume at any time from your Dashboard.", "info")
    return redirect(url_for("index"))

@app.route("/quiz/sync_timer", methods=["POST"])
def sync_timer():
    """Background AJAX endpoint to persist timer countdown in SQLite."""
    session_id = session.get("active_session_id")
    if session_id:
        try:
            time_rem = int(request.form.get("time_remaining", "0"))
            db.update_session(session_id, {"time_remaining_seconds": max(0, time_rem)})
            return jsonify({"status": "ok"})
        except Exception:
            pass
    return jsonify({"status": "error"}), 400

@app.route("/quiz/expire")
def expire_quiz():
    """Handles timer expiration by completing quiz."""
    session_id = session.get("active_session_id")
    if session_id:
        db.update_session(session_id, {"time_remaining_seconds": 0, "status": "completed"})
        flash("Time has expired! Generating your performance summary.", "warning")
        return redirect(url_for("finish_main_quiz"))
    return redirect(url_for("index"))

@app.route("/quiz/discard")
def discard_session():
    """Discards active unfinished session so user can start fresh."""
    session_id = session.get("active_session_id")
    if session_id:
        db.update_session(session_id, {"status": "discarded"})
        session.pop("active_session_id", None)
        flash("Previous quiz session discarded.", "info")
    return redirect(url_for("index"))

@app.route("/finish_main_quiz")
def finish_main_quiz():
    """
    Evaluates main quiz answers:
    - If 1 or more questions were answered incorrectly: launches automatic review round!
    - If 0 questions were answered incorrectly: navigates directly to results!
    """
    session_id = session.get("active_session_id")
    if not session_id:
        return redirect(url_for("index"))

    answers = db.get_session_answers(session_id, is_review=0)
    wrong_answers = [a for a in answers if not a["is_correct"]]

    if wrong_answers:
        # Launch automatic review round
        session["review_index"] = 0
        session["review_feedback"] = None
        db.update_session(session_id, {"status": "review_pending"})
        flash("Main quiz complete! Automatically launching the Misconception Review Round.", "info")
        return redirect(url_for("review_round"))
    else:
        # Flawless score! Go straight to results
        db.save_quiz_result(session_id)
        return redirect(url_for("result"))

# ==================== AUTOMATIC WRONG-ANSWER REVIEW ====================

@app.route("/review_round", methods=["GET", "POST"])
def review_round():
    """
    Automatic wrong-answer review round:
    - Presents missed questions again one by one
    - Allows 1 additional attempt with instant explanation
    - Does NOT alter original main quiz score
    """
    session_id = session.get("active_session_id")
    if not session_id:
        return redirect(url_for("index"))

    quiz_sess = db.get_session(session_id)
    answers = db.get_session_answers(session_id, is_review=0)
    wrong_answers = [a for a in answers if not a["is_correct"]]

    if not wrong_answers:
        db.save_quiz_result(session_id)
        return redirect(url_for("result"))

    review_index = session.get("review_index", 0)
    total_reviews = len(wrong_answers)

    if review_index >= total_reviews:
        # Finished reviewing all mistakes
        db.save_quiz_result(session_id)
        flash("🎉 Misconception review completed! You have reinforced your understanding.", "success")
        return redirect(url_for("result"))

    current_wrong = wrong_answers[review_index]
    current_q = get_question(current_wrong["question_id"])

    if request.method == "POST":
        action = request.form.get("action")

        if action == "next":
            session["review_feedback"] = None
            session["review_index"] = review_index + 1
            if session["review_index"] >= total_reviews:
                db.save_quiz_result(session_id)
                return redirect(url_for("result"))
            return redirect(url_for("review_round"))

        selected = request.form.get("option")
        if not selected:
            flash("Please choose an option.", "warning")
            return redirect(url_for("review_round"))

        is_correct = (selected == current_q["correct_answer"])

        # Record review answer
        db.record_answer(
            session_id=session_id,
            question_id=current_q["id"],
            question_order=review_index + 1,
            selected_option=selected,
            is_correct=is_correct,
            is_review=1
        )

        session["review_feedback"] = {
            "is_correct": is_correct,
            "selected_key": selected,
            "correct_key": current_q["correct_answer"],
            "correct_text": current_q["options"].get(current_q["correct_answer"], ""),
            "explanation": current_q.get("explanation", "")
        }
        return redirect(url_for("review_round"))

    return render_template(
        "review.html",
        quiz_session=quiz_sess,
        question=current_q,
        index=review_index + 1,
        total=total_reviews,
        progress_percent=round(((review_index + 1) / total_reviews) * 100, 1),
        feedback=session.get("review_feedback"),
        is_last=(review_index + 1 >= total_reviews)
    )

# ==================== RESULTS & HISTORY ====================

@app.route("/result")
def result():
    """Displays the comprehensive results dashboard for the completed quiz."""
    session_id = session.get("active_session_id")
    if not session_id:
        return redirect(url_for("index"))

    return show_result_page(session_id)

@app.route("/result/<session_id>")
def view_result(session_id):
    """Allows viewing previous quiz result from history."""
    return show_result_page(session_id)

def show_result_page(session_id):
    """Shared helper to render the results page."""
    res = db.get_quiz_result(session_id)
    if not res:
        res = db.save_quiz_result(session_id)
        if not res:
            flash("Result not found.", "error")
            return redirect(url_for("index"))

    # Reconstruct question-by-question breakdown
    answers = db.get_session_answers(session_id, is_review=0)
    detailed = []
    for a in answers:
        q = get_question(a["question_id"])
        if q:
            detailed.append({
                "order": a["question_order"],
                "question": q["question"],
                "options": q["options"],
                "selected": a["selected_option"],
                "correct": q["correct_answer"],
                "is_correct": bool(a["is_correct"]),
                "difficulty": q.get("difficulty", "Medium"),
                "concept": q.get("concept", ""),
                "explanation": q.get("explanation", "")
            })

    return render_template(
        "result.html",
        result=res,
        detailed_answers=detailed,
        subject_names=SUBJECTS
    )

@app.route("/history")
def history():
    """Displays chronological history of all quiz attempts from SQLite."""
    attempts = db.get_quiz_history(limit=50)
    analytics = db.get_analytics()
    return render_template(
        "history.html",
        history=attempts,
        analytics=analytics,
        subject_names=SUBJECTS
    )

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1")
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=debug_mode, port=port)
