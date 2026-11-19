import os
import sqlite3
import json
import uuid
from datetime import datetime

DATABASE_DIR = os.path.join(os.path.dirname(__file__), "instance")
DEFAULT_DB_PATH = os.path.join(DATABASE_DIR, "quizzly.db")

SUBJECTS = {
    "python": "Python Programming",
    "data_structures": "Data Structures",
    "coa": "Computer Organization and Architecture",
    "dstl": "Discrete Structures and Theory of Logic",
    "mathematics": "Mathematics"
}

def get_db(db_path=None):
    """Establishes SQLite connection with WAL mode and row factory."""
    path = db_path or DEFAULT_DB_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_db(db_path=None):
    """Initializes tables and seeds initial subject question banks."""
    conn = get_db(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        explanation TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        concept TEXT,
        source_ref TEXT DEFAULT 'Standard Bank',
        is_built_in INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS pdf_documents (
        id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        stored_path TEXT NOT NULL,
        page_count INTEGER DEFAULT 1,
        is_scanned_or_handwritten INTEGER DEFAULT 0,
        extraction_method TEXT DEFAULT 'pymupdf_text',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS quiz_sessions (
        session_id TEXT PRIMARY KEY,
        subject TEXT NOT NULL,
        pdf_doc_id TEXT,
        mode TEXT NOT NULL,
        is_timed INTEGER DEFAULT 0,
        time_limit_seconds INTEGER DEFAULT 0,
        time_remaining_seconds INTEGER DEFAULT 0,
        total_questions INTEGER NOT NULL,
        current_index INTEGER DEFAULT 0,
        score INTEGER DEFAULT 0,
        status TEXT DEFAULT 'in_progress',
        question_ids_json TEXT NOT NULL,
        current_difficulty TEXT DEFAULT 'Easy',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pdf_doc_id) REFERENCES pdf_documents(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS quiz_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        question_id INTEGER NOT NULL,
        question_order INTEGER NOT NULL,
        selected_option TEXT,
        is_correct INTEGER DEFAULT 0,
        time_spent_seconds INTEGER DEFAULT 0,
        is_review_round INTEGER DEFAULT 0,
        answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES quiz_sessions(session_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT UNIQUE NOT NULL,
        subject TEXT NOT NULL,
        mode TEXT NOT NULL,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        percentage REAL NOT NULL,
        correct_count INTEGER NOT NULL,
        incorrect_count INTEGER NOT NULL,
        unanswered_count INTEGER DEFAULT 0,
        easy_accuracy REAL DEFAULT 0.0,
        medium_accuracy REAL DEFAULT 0.0,
        hard_accuracy REAL DEFAULT 0.0,
        review_total INTEGER DEFAULT 0,
        review_score INTEGER DEFAULT 0,
        time_taken_seconds INTEGER DEFAULT 0,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES quiz_sessions(session_id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_questions_subject ON questions(subject);
    CREATE INDEX IF NOT EXISTS idx_questions_diff ON questions(difficulty);
    CREATE INDEX IF NOT EXISTS idx_sessions_status ON quiz_sessions(status);
    CREATE INDEX IF NOT EXISTS idx_answers_session ON quiz_answers(session_id);
    """)

    # Seed subject questions if empty
    cursor.execute("SELECT COUNT(*) AS count FROM questions WHERE is_built_in = 1")
    count = cursor.fetchone()["count"]
    if count == 0:
        seed_subject_questions(conn)

    conn.commit()
    conn.close()

def seed_subject_questions(conn):
    """Seeds verified academic B.Tech CSE questions across all 5 subjects."""
    from subject_bank import ALL_SUBJECT_QUESTIONS
    cursor = conn.cursor()
    for q in ALL_SUBJECT_QUESTIONS:
        cursor.execute("""
            INSERT INTO questions (
                subject, question, option_a, option_b, option_c, option_d,
                correct_answer, explanation, difficulty, concept, source_ref, is_built_in
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            q["subject"], q["question"], q["options"]["A"], q["options"]["B"],
            q["options"]["C"], q["options"]["D"], q["correct_answer"],
            q["explanation"], q["difficulty"], q.get("concept", ""), q.get("source_ref", "Standard Bank")
        ))
    conn.commit()

# ==================== QUESTION ACCESS HELPERS ====================

def get_questions_by_subject(subject, difficulty=None, db_path=None):
    """Retrieves all questions for a subject, optionally filtered by difficulty."""
    conn = get_db(db_path)
    cursor = conn.cursor()
    if difficulty:
        cursor.execute("SELECT * FROM questions WHERE subject = ? AND difficulty = ?", (subject, difficulty))
    else:
        cursor.execute("SELECT * FROM questions WHERE subject = ?", (subject,))
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_question_dict(r) for r in rows]

def get_question(q_id, db_path=None):
    """Retrieves a single question dictionary by ID."""
    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = ?", (q_id,))
    row = cursor.fetchone()
    conn.close()
    return _row_to_question_dict(row) if row else None

def _row_to_question_dict(row):
    """Converts SQLite Row to standard question dictionary."""
    return {
        "id": row["id"],
        "subject": row["subject"],
        "question": row["question"],
        "options": {
            "A": row["option_a"],
            "B": row["option_b"],
            "C": row["option_c"],
            "D": row["option_d"]
        },
        "correct_answer": row["correct_answer"],
        "explanation": row["explanation"],
        "difficulty": row["difficulty"],
        "concept": row["concept"] or "",
        "source_ref": row["source_ref"] or "Standard Bank"
    }

# ==================== SESSION & QUIZ FLOW HELPERS ====================

def create_quiz_session(subject, mode, total_questions, question_ids, is_timed=False, time_limit_seconds=0, pdf_doc_id=None, db_path=None):
    """Creates a new quiz session row in SQLite with a secure UUID."""
    session_id = str(uuid.uuid4())
    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_sessions (
            session_id, subject, pdf_doc_id, mode, is_timed, time_limit_seconds,
            time_remaining_seconds, total_questions, current_index, score, status,
            question_ids_json, current_difficulty, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 'in_progress', ?, 'Easy', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (
        session_id, subject, pdf_doc_id, mode, 1 if is_timed else 0,
        time_limit_seconds, time_limit_seconds, total_questions,
        json.dumps(question_ids)
    ))
    conn.commit()
    conn.close()
    return session_id

def get_session(session_id, db_path=None):
    """Retrieves a session dict with parsed question_ids."""
    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz_sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    data["question_ids"] = json.loads(data["question_ids_json"])
    return data

def get_active_session(db_path=None):
    """Returns the most recent in-progress or paused quiz session for resuming."""
    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM quiz_sessions 
        WHERE status IN ('in_progress', 'paused')
        ORDER BY updated_at DESC LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    data["question_ids"] = json.loads(data["question_ids_json"])
    return data

def update_session(session_id, updates, db_path=None):
    """Updates fields in quiz_sessions table."""
    conn = get_db(db_path)
    cursor = conn.cursor()
    fields = []
    values = []
    for k, v in updates.items():
        if k == "question_ids":
            fields.append("question_ids_json = ?")
            values.append(json.dumps(v))
        else:
            fields.append(f"{k} = ?")
            values.append(v)
    fields.append("updated_at = CURRENT_TIMESTAMP")
    values.append(session_id)
    sql = f"UPDATE quiz_sessions SET {', '.join(fields)} WHERE session_id = ?"
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def record_answer(session_id, question_id, question_order, selected_option, is_correct, time_spent_seconds=0, is_review=0, db_path=None):
    """Records a student's answer in quiz_answers table."""
    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_answers (
            session_id, question_id, question_order, selected_option,
            is_correct, time_spent_seconds, is_review_round, answered_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (session_id, question_id, question_order, selected_option, 1 if is_correct else 0, time_spent_seconds, 1 if is_review else 0))
    conn.commit()
    conn.close()

def get_session_answers(session_id, is_review=0, db_path=None):
    """Fetches all recorded answers for a session."""
    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM quiz_answers 
        WHERE session_id = ? AND is_review_round = ?
        ORDER BY question_order ASC
    """, (session_id, is_review))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_quiz_result(session_id, db_path=None):
    """Computes final results from quiz_answers and saves into quiz_results table."""
    sess = get_session(session_id, db_path)
    if not sess:
        return None
    
    answers = get_session_answers(session_id, is_review=0, db_path=db_path)
    review_answers = get_session_answers(session_id, is_review=1, db_path=db_path)
    
    total = sess["total_questions"]
    answered_count = len(answers)
    correct_count = sum(1 for a in answers if a["is_correct"])
    incorrect_count = answered_count - correct_count
    unanswered_count = max(0, total - answered_count)
    percentage = round((correct_count / total) * 100, 1) if total > 0 else 0.0

    # Difficulty accuracy
    diff_stats = {"Easy": [0, 0], "Medium": [0, 0], "Hard": [0, 0]}
    for a in answers:
        q = get_question(a["question_id"], db_path)
        if q:
            d = q.get("difficulty", "Medium")
            if d in diff_stats:
                diff_stats[d][1] += 1
                if a["is_correct"]:
                    diff_stats[d][0] += 1

    easy_acc = round((diff_stats["Easy"][0] / diff_stats["Easy"][1]) * 100, 1) if diff_stats["Easy"][1] > 0 else 0.0
    med_acc = round((diff_stats["Medium"][0] / diff_stats["Medium"][1]) * 100, 1) if diff_stats["Medium"][1] > 0 else 0.0
    hard_acc = round((diff_stats["Hard"][0] / diff_stats["Hard"][1]) * 100, 1) if diff_stats["Hard"][1] > 0 else 0.0

    review_total = len(review_answers)
    review_score = sum(1 for a in review_answers if a["is_correct"])
    time_taken = max(0, sess["time_limit_seconds"] - sess["time_remaining_seconds"]) if sess["is_timed"] else 0

    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO quiz_results (
            session_id, subject, mode, score, total_questions, percentage,
            correct_count, incorrect_count, unanswered_count,
            easy_accuracy, medium_accuracy, hard_accuracy,
            review_total, review_score, time_taken_seconds, completed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (
        session_id, sess["subject"], sess["mode"], correct_count, total, percentage,
        correct_count, incorrect_count, unanswered_count,
        easy_acc, med_acc, hard_acc,
        review_total, review_score, time_taken
    ))
    cursor.execute("UPDATE quiz_sessions SET status = 'completed', score = ? WHERE session_id = ?", (correct_count, session_id))
    conn.commit()
    conn.close()

    return {
        "session_id": session_id,
        "subject": sess["subject"],
        "mode": sess["mode"],
        "score": correct_count,
        "total_questions": total,
        "percentage": percentage,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "unanswered_count": unanswered_count,
        "easy_accuracy": easy_acc,
        "medium_accuracy": med_acc,
        "hard_accuracy": hard_acc,
        "review_total": review_total,
        "review_score": review_score,
        "time_taken_seconds": time_taken,
        "diff_stats": diff_stats
    }

def get_quiz_result(session_id, db_path=None):
    """Retrieves saved quiz result row."""
    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz_results WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# ==================== ANALYTICS & HISTORY HELPERS ====================

def get_analytics(db_path=None):
    """Calculates real dashboard statistics strictly from SQLite data."""
    conn = get_db(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total_quizzes FROM quiz_results")
    total_quizzes = cursor.fetchone()["total_quizzes"]

    if total_quizzes == 0:
        conn.close()
        return {
            "total_quizzes": 0,
            "avg_score": 0.0,
            "total_questions_answered": 0,
            "highest_score": 0.0,
            "subject_breakdown": {},
            "recent_results": []
        }

    cursor.execute("SELECT ROUND(AVG(percentage), 1) AS avg_score, MAX(percentage) AS highest_score FROM quiz_results")
    agg = cursor.fetchone()
    avg_score = agg["avg_score"] or 0.0
    highest_score = agg["highest_score"] or 0.0

    cursor.execute("SELECT SUM(total_questions) AS total_answered FROM quiz_results")
    total_answered = cursor.fetchone()["total_answered"] or 0

    cursor.execute("""
        SELECT subject, COUNT(*) AS count, ROUND(AVG(percentage), 1) AS avg_pct
        FROM quiz_results GROUP BY subject
    """)
    subject_rows = cursor.fetchall()
    subject_breakdown = {r["subject"]: {"count": r["count"], "avg_pct": r["avg_pct"]} for r in subject_rows}

    cursor.execute("""
        SELECT * FROM quiz_results 
        ORDER BY completed_at DESC LIMIT 5
    """)
    recent = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return {
        "total_quizzes": total_quizzes,
        "avg_score": avg_score,
        "total_questions_answered": total_answered,
        "highest_score": highest_score,
        "subject_breakdown": subject_breakdown,
        "recent_results": recent
    }

def get_quiz_history(limit=50, db_path=None):
    """Fetches full quiz history list."""
    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM quiz_results 
        ORDER BY completed_at DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ==================== PDF DOCUMENT HELPERS ====================

def save_pdf_document(filename, stored_path, page_count=1, is_scanned_or_handwritten=0, extraction_method='pymupdf_text', db_path=None):
    """Registers an uploaded PDF document."""
    doc_id = str(uuid.uuid4())
    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pdf_documents (id, filename, stored_path, page_count, is_scanned_or_handwritten, extraction_method)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (doc_id, filename, stored_path, page_count, is_scanned_or_handwritten, extraction_method))
    conn.commit()
    conn.close()
    return doc_id

def save_pdf_questions(pdf_doc_id, questions, db_path=None):
    """Saves AI or rule-generated questions linked to a PDF document into the questions table."""
    conn = get_db(db_path)
    cursor = conn.cursor()
    inserted_ids = []
    for q in questions:
        cursor.execute("""
            INSERT INTO questions (
                subject, question, option_a, option_b, option_c, option_d,
                correct_answer, explanation, difficulty, concept, source_ref, is_built_in
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            f"pdf:{pdf_doc_id}", q["question"], q["options"]["A"], q["options"]["B"],
            q["options"]["C"], q["options"]["D"], q["correct_answer"],
            q["explanation"], q["difficulty"], q.get("concept", "PDF Concept"),
            q.get("source_ref", f"PDF Page {q.get('source_page', 1)}")
        ))
        inserted_ids.append(cursor.lastrowid)
    conn.commit()
    conn.close()
    return inserted_ids

def get_pdf_questions(pdf_doc_id, db_path=None):
    """Retrieves all generated questions for a specific PDF document."""
    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE subject = ?", (f"pdf:{pdf_doc_id}",))
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_question_dict(r) for r in rows]

