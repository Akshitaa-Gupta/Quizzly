import os
import io
import unittest
import sqlite3
import json
from unittest.mock import patch, MagicMock

import db
from app import app
import gemini_service

class QuizzlyComprehensiveTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configure app for testing with an in-memory or test database
        cls.test_db_path = os.path.join(os.path.dirname(__file__), "instance", "test_quizzly.db")
        db.DEFAULT_DB_PATH = cls.test_db_path
        db.init_db(cls.test_db_path)

    @classmethod
    def tearDownClass(cls):
        # Clean up test database
        if os.path.exists(cls.test_db_path):
            try:
                os.remove(cls.test_db_path)
            except Exception:
                pass

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "quizzly_test_secret_key"
        self.client = app.test_client()

    # 1. Dashboard & Navigation
    def test_01_dashboard_and_navigation(self):
        """Verify dashboard loads real metrics, branding, and navigation."""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Quizzly", resp.data)
        self.assertIn(b"Learn. Practice. Improve.", resp.data)
        self.assertIn(b"Total Quizzes", resp.data)
        self.assertIn(b"Python Programming", resp.data)
        self.assertIn(b"Data Structures", resp.data)

    def test_02_subject_catalog(self):
        """Verify /subjects catalog loads with all 5 core subjects."""
        resp = self.client.get("/subjects")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Python Programming", resp.data)
        self.assertIn(b"Data Structures", resp.data)
        self.assertIn(b"Computer Org.", resp.data)
        self.assertIn(b"Discrete Structures", resp.data)
        self.assertIn(b"Engineering Mathematics", resp.data)

    # 2. Subject Quizzes & Question Banks
    def test_03_subject_question_counts_and_validation(self):
        """Verify all 5 subjects have verified questions with exactly 4 options and 1 answer."""
        for subj in ["python", "data_structures", "coa", "dstl", "mathematics"]:
            qs = db.get_questions_by_subject(subj, db_path=self.test_db_path)
            self.assertGreaterEqual(len(qs), 20, f"Subject {subj} has fewer than 20 questions")
            for q in qs:
                self.assertTrue(gemini_service.validate_question(q), f"Malformed question in {subj}: {q}")

    # 3. Quiz Configuration
    def test_04_configure_page(self):
        """Verify configuration page displays question counts and mode selections."""
        resp = self.client.get("/configure?subject=python")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"20 Unique Questions Available", resp.data)
        self.assertIn(b"Adaptive Mode", resp.data)
        self.assertIn(b"Mixed Mode", resp.data)
        self.assertIn(b"Timer Mode", resp.data)

    def test_05_configure_validation_excess_count(self):
        """Verify validation rejects counts exceeding available unique questions."""
        resp = self.client.post("/configure", data={
            "subject": "python",
            "question_count": "50",
            "mode": "adaptive"
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"exceeds available 20 unique questions", resp.data)

    # 4. Adaptive Mode Quiz Flow (All Correct)
    def test_06_adaptive_quiz_all_correct(self):
        """Test complete 5-question Adaptive quiz with all correct answers."""
        # 1. Start quiz
        resp = self.client.post("/configure", data={
            "subject": "python",
            "question_count": "5",
            "mode": "adaptive",
            "timer_mode": "untimed"
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Question 1 / 5", resp.data)

        # Answer 5 questions correctly
        diffs = []
        for i in range(1, 6):
            sess_id = self.client.get("/quiz").data
            with self.client.session_transaction() as sess:
                current_sess = db.get_session(sess["active_session_id"], db_path=self.test_db_path)
                q_id = current_sess["question_ids"][current_sess["current_index"]]
                q = db.get_question(q_id, db_path=self.test_db_path)
                correct_ans = q["correct_answer"]
                diffs.append(q["difficulty"])

            # Submit answer
            sub = self.client.post("/quiz", data={"action": "check", "option": correct_ans}, follow_redirects=True)
            self.assertIn(b"Correct! Excellent job!", sub.data)

            # Advance
            adv = self.client.post("/quiz", data={"action": "next"}, follow_redirects=True)

        # Finished all 5 correctly: Flawless score skips review and goes straight to result!
        self.assertIn(b"Assessment Performance", adv.data)
        self.assertIn(b"5 / 5", adv.data)
        self.assertIn(b"100.0%", adv.data)
        self.assertIn(b"Flawless Mastery!", adv.data)

        # Verify difficulty escalated: starts Easy, moves up
        self.assertEqual(diffs[0], "Easy")
        self.assertEqual(diffs[1], "Medium")

    # 5. Adaptive Mode Quiz Flow (All Incorrect) + Automatic Wrong-Answer Review
    def test_07_adaptive_quiz_all_incorrect_and_automatic_review(self):
        """Test complete 5-question Adaptive quiz with mistakes, triggering automatic review."""
        self.client.post("/configure", data={
            "subject": "data_structures",
            "question_count": "5",
            "mode": "adaptive",
            "timer_mode": "untimed"
        }, follow_redirects=True)

        for i in range(1, 6):
            with self.client.session_transaction() as sess:
                current_sess = db.get_session(sess["active_session_id"], db_path=self.test_db_path)
                q_id = current_sess["question_ids"][current_sess["current_index"]]
                q = db.get_question(q_id, db_path=self.test_db_path)
                wrong_ans = "B" if q["correct_answer"] == "A" else "A"

            self.client.post("/quiz", data={"action": "check", "option": wrong_ans}, follow_redirects=True)
            adv = self.client.post("/quiz", data={"action": "next"}, follow_redirects=True)

        # Automatic redirection to Automatic Misconception Review!
        self.assertIn(b"Automatic Misconception Review", adv.data)
        self.assertIn(b"Mistake 1 of 5", adv.data)

        # Answer review round questions
        for r in range(1, 6):
            with self.client.session_transaction() as sess:
                answers = db.get_session_answers(sess["active_session_id"], is_review=0, db_path=self.test_db_path)
                wrong_q = db.get_question(answers[r - 1]["question_id"], db_path=self.test_db_path)
                corr = wrong_q["correct_answer"]

            sub_rev = self.client.post("/review_round", data={"action": "check", "option": corr}, follow_redirects=True)
            self.assertIn(b"Well done! You mastered this misconception!", sub_rev.data)
            nxt_rev = self.client.post("/review_round", data={"action": "next"}, follow_redirects=True)

        # Once review completes, result page is shown
        self.assertIn(b"Assessment Performance", nxt_rev.data)
        # Main score remains isolated and unchanged: 0 / 5
        self.assertIn(b"0 / 5", nxt_rev.data)
        self.assertIn(b"0.0%", nxt_rev.data)
        # Review score tracked separately: 5/5
        self.assertIn(b"5/5 Mastered", nxt_rev.data)

    # 6. Mixed Mode Quiz Flow
    def test_08_mixed_mode_quiz_flow(self):
        """Test complete 10-question Mixed mode quiz with fixed balanced difficulties."""
        resp = self.client.post("/configure", data={
            "subject": "coa",
            "question_count": "10",
            "mode": "mixed",
            "timer_mode": "untimed"
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Question 1 / 10", resp.data)

        # Verify no duplicate IDs in session
        with self.client.session_transaction() as sess:
            current_sess = db.get_session(sess["active_session_id"], db_path=self.test_db_path)
            q_ids = current_sess["question_ids"]
            self.assertEqual(len(q_ids), 10)
            self.assertEqual(len(q_ids), len(set(q_ids)))

    # 7. Timer, Pause, and Resume
    def test_09_timer_pause_and_resume(self):
        """Verify timed quiz pause, SQLite persistence, and resuming from dashboard."""
        self.client.post("/configure", data={
            "subject": "dstl",
            "question_count": "5",
            "mode": "adaptive",
            "timer_mode": "timed",
            "time_limit_minutes": "10"
        }, follow_redirects=True)

        # Answer question 1
        with self.client.session_transaction() as sess:
            sess_id = sess["active_session_id"]
            current_sess = db.get_session(sess_id, db_path=self.test_db_path)
            q = db.get_question(current_sess["question_ids"][0], db_path=self.test_db_path)
            ans = q["correct_answer"]

        self.client.post("/quiz", data={"action": "check", "option": ans, "time_remaining": "580"}, follow_redirects=True)
        self.client.post("/quiz", data={"action": "next", "time_remaining": "575"}, follow_redirects=True)

        # Explicitly Pause Quiz
        pause_resp = self.client.post("/quiz/pause", data={"time_remaining": "570"}, follow_redirects=True)
        self.assertIn(b"Quiz successfully paused", pause_resp.data)

        # Dashboard now displays the Resume Quiz card with preserved state
        dash_resp = self.client.get("/")
        self.assertIn(b"Unfinished Session Detected", dash_resp.data)
        self.assertIn(b"Resume Quiz", dash_resp.data)
        self.assertIn(b"Question 2 of 5", dash_resp.data)

        # Click Resume
        resumed = self.client.get("/quiz")
        self.assertEqual(resumed.status_code, 200)
        self.assertIn(b"Question 2 / 5", resumed.data)

    # 8. Timer Expiration Handling
    def test_10_timer_expiration(self):
        """Verify that timer expiration completes the quiz cleanly."""
        self.client.post("/configure", data={
            "subject": "mathematics",
            "question_count": "5",
            "mode": "adaptive",
            "timer_mode": "timed",
            "time_limit_minutes": "1"
        }, follow_redirects=True)

        expire_resp = self.client.get("/quiz/expire", follow_redirects=True)
        self.assertEqual(expire_resp.status_code, 200)
        self.assertIn(b"Time has expired!", expire_resp.data)

    # 9. PDF Processing & Validation
    def test_11_pdf_text_extraction_and_mcq_generation(self):
        """Verify text-based PDF extraction and question generation."""
        sample_pdf = os.path.join(os.path.dirname(__file__), "uploads", "Technical_Communication_unit_-1_1.pdf")
        if not os.path.exists(sample_pdf):
            self.skipTest("Sample PDF not found")

        with open(sample_pdf, "rb") as f:
            pdf_bytes = f.read()

        upload_resp = self.client.post("/upload", data={
            "pdf_file": (io.BytesIO(pdf_bytes), "Technical_Communication_unit_-1_1.pdf")
        }, content_type="multipart/form-data", follow_redirects=True)

        self.assertEqual(upload_resp.status_code, 200)
        self.assertIn(b"Quiz Configuration", upload_resp.data)
        self.assertIn(b"Uploaded Study Notes", upload_resp.data)

    # 10. Gemini Mock Multimodal Generation Test
    @patch("google.genai.Client")
    def test_12_gemini_multimodal_handwritten_notes(self, mock_client_cls):
        """Verify Gemini multimodal processing for handwritten notes with structured JSON validation."""
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client

        mock_response = MagicMock()
        mock_response.text = json.dumps([
            {
                "question": "What is the primary characteristic of an Equivalence Relation?",
                "options": {
                    "A": "It is reflexive, symmetric, and transitive",
                    "B": "It is irreflexive and asymmetric",
                    "C": "It is strictly anti-symmetric and complete",
                    "D": "It operates exclusively on prime numbers"
                },
                "correct_answer": "A",
                "explanation": "An equivalence relation must be reflexive, symmetric, and transitive.",
                "difficulty": "Easy",
                "concept": "Equivalence Relations",
                "source_page": 1
            }
        ])
        mock_client.models.generate_content.return_value = mock_response

        # Call generate_questions_with_gemini
        sample_pdf = os.path.join(os.path.dirname(__file__), "uploads", "Technical_Communication_unit_-1_1.pdf")
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key", "GEMINI_MODEL": "gemini-2.5-flash"}):
            qs = gemini_service.generate_questions_with_gemini(sample_pdf, is_handwritten=True, target_count=5)
            self.assertEqual(len(qs), 1)
            self.assertEqual(qs[0]["correct_answer"], "A")
            self.assertTrue(gemini_service.validate_question(qs[0]))

    # 11. SQLite History and Analytics
    def test_13_quiz_history_and_analytics(self):
        """Verify that completed quizzes are recorded in SQLite analytics and history."""
        hist_resp = self.client.get("/history")
        self.assertEqual(hist_resp.status_code, 200)
        self.assertIn(b"Assessment History", hist_resp.data)
        self.assertIn(b"Total Completed", hist_resp.data)

if __name__ == "__main__":
    unittest.main()

