import unittest
import io
import os
from app import app, STANDARD_BY_ID, get_question_by_id, PDF_STORE

class AdaptiveQuizTestSuite(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test_secret_key"
        self.client = app.test_client()

    def test_01_landing_page(self):
        """Verify landing page renders successfully with both options."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Adaptive Quiz Platform", response.data)
        self.assertIn(b"Standard CSE Bank", response.data)
        self.assertIn(b"PDF Concept Quiz", response.data)

    def test_02_configuration_page_standard(self):
        """Verify configuration page displays standard question bank options."""
        response = self.client.get("/configure?source=standard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"75 Unique Questions Available", response.data)
        self.assertIn(b"Adaptive Mode", response.data)
        self.assertIn(b"Mixed Mode", response.data)

    def test_03_configuration_validation_exceeding_count(self):
        """Verify rejecting counts that exceed available questions."""
        response = self.client.post("/configure", data={
            "source": "standard",
            "question_count": "100",
            "mode": "adaptive"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"exceeds the 75 available unique questions", response.data)

    def test_04_quiz_flow_all_correct_adaptive_5_questions(self):
        """Test complete 5-question Adaptive quiz where user answers everything correctly."""
        resp = self.client.post("/configure", data={
            "source": "standard",
            "question_count": "5",
            "mode": "adaptive"
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Question 1 / 5", resp.data)
        self.assertIn(b"Difficulty: Easy", resp.data)

        diffs = []
        for i in range(1, 6):
            with self.client.session_transaction() as sess:
                current_q_id = sess["current_q_id"]
                current_q = STANDARD_BY_ID[current_q_id]
                correct_ans = current_q["correct_answer"]
                diffs.append(sess["current_difficulty"])

            submit_resp = self.client.post("/quiz", data={"option": correct_ans}, follow_redirects=True)
            self.assertEqual(submit_resp.status_code, 200)
            self.assertIn(b"Correct! Well done!", submit_resp.data)

            if i < 5:
                self.assertIn(b"Next Question", submit_resp.data)
                next_resp = self.client.post("/quiz", data={"next": "1"}, follow_redirects=True)
                self.assertEqual(next_resp.status_code, 200)
                self.assertIn(f"Question {i + 1} / 5".encode(), next_resp.data)
            else:
                self.assertIn(b"View Final Results", submit_resp.data)
                final_resp = self.client.post("/quiz", data={"next": "1"}, follow_redirects=True)
                self.assertEqual(final_resp.status_code, 200)
                self.assertIn(b"Performance Summary", final_resp.data)
                self.assertIn(b"5 / 5", final_resp.data)
                self.assertIn(b"100.0%", final_resp.data)
                self.assertIn(b"Flawless Score!", final_resp.data)

        # Verify difficulty transition
        self.assertEqual(diffs[0], "Easy")
        self.assertEqual(diffs[1], "Medium")
        self.assertEqual(diffs[2], "Hard")

    def test_05_quiz_flow_all_incorrect_adaptive_5_questions_and_review(self):
        """Test complete 5-question Adaptive quiz with all wrong answers, then wrong-answer review."""
        self.client.post("/configure", data={
            "source": "standard",
            "question_count": "5",
            "mode": "adaptive"
        }, follow_redirects=True)

        for i in range(1, 6):
            with self.client.session_transaction() as sess:
                current_q = STANDARD_BY_ID[sess["current_q_id"]]
                correct_ans = current_q["correct_answer"]
                wrong_ans = "B" if correct_ans == "A" else "A"

            submit_resp = self.client.post("/quiz", data={"option": wrong_ans}, follow_redirects=True)
            self.assertIn(b"Not quite!", submit_resp.data)
            advance_resp = self.client.post("/quiz", data={"next": "1"}, follow_redirects=True)

        # Result page assertions
        self.assertIn(b"0 / 5", advance_resp.data)
        self.assertIn(b"0.0%", advance_resp.data)
        self.assertIn(b"Misconception Review Queue", advance_resp.data)
        self.assertIn(b"Launch Wrong-Answer Review (5)", advance_resp.data)

        # Launch Wrong-Answer Review
        rev_start = self.client.get("/start_review", follow_redirects=True)
        self.assertEqual(rev_start.status_code, 200)
        self.assertIn(b"Mistake Review 1 / 5", rev_start.data)

        # Answer mistakes in review round
        for r in range(1, 6):
            with self.client.session_transaction() as sess:
                q_id = sess["review_queue_ids"][sess["review_index"]]
                rev_q = STANDARD_BY_ID[q_id]
                correct_ans = rev_q["correct_answer"]

            sub = self.client.post("/review_round", data={"option": correct_ans}, follow_redirects=True)
            self.assertIn(b"Correct! Well done!", sub.data)
            nxt = self.client.post("/review_round", data={"next": "1"}, follow_redirects=True)

        # Review finished
        self.assertIn(b"Great job! All missed questions have been reviewed", nxt.data)
        # Main score remains isolated
        self.assertIn(b"0 / 5", nxt.data)

    def test_06_quiz_flow_mixed_mode_10_questions(self):
        """Test complete 10-question Mixed mode quiz with mixed performance."""
        resp = self.client.post("/configure", data={
            "source": "standard",
            "question_count": "10",
            "mode": "mixed"
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Question 1 / 10", resp.data)
        self.assertIn(b"Mixed", resp.data)

        with self.client.session_transaction() as sess:
            q_ids = sess["quiz_question_ids"]
            self.assertEqual(len(q_ids), 10)
            self.assertEqual(len(q_ids), len(set(q_ids)))

        for i in range(10):
            with self.client.session_transaction() as sess:
                current_q = STANDARD_BY_ID[sess["quiz_question_ids"][i]]
                correct_ans = current_q["correct_answer"]
                chosen = correct_ans if (i % 2 == 0) else ("B" if correct_ans == "A" else "A")

            self.client.post("/quiz", data={"option": chosen}, follow_redirects=True)
            self.client.post("/quiz", data={"next": "1"}, follow_redirects=True)

        result_page = self.client.get("/result")
        self.assertIn(b"5 / 10", result_page.data)
        self.assertIn(b"50.0%", result_page.data)
        self.assertIn(b"Mixed Mode", result_page.data)

    def test_07_quiz_flow_15_and_20_questions(self):
        """Test complete 15-question and 20-question configurations without repetition."""
        for count in [15, 20]:
            resp = self.client.post("/configure", data={
                "source": "standard",
                "question_count": str(count),
                "mode": "adaptive"
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"Question 1 / {count}".encode(), resp.data)

            for i in range(count):
                with self.client.session_transaction() as sess:
                    current_q = STANDARD_BY_ID[sess["current_q_id"]]
                    ans = current_q["correct_answer"]
                self.client.post("/quiz", data={"option": ans}, follow_redirects=True)
                adv = self.client.post("/quiz", data={"next": "1"}, follow_redirects=True)

            self.assertIn(f"{count} / {count}".encode(), adv.data)
            self.assertIn(b"100.0%", adv.data)

    def test_08_starting_new_quiz_resets_length_and_state(self):
        """Verify starting a new quiz resets length and session state cleanly."""
        self.client.post("/configure", data={
            "source": "standard",
            "question_count": "15",
            "mode": "mixed"
        }, follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.assertEqual(sess["total_questions"], 15)

        self.client.post("/configure", data={
            "source": "standard",
            "question_count": "5",
            "mode": "adaptive"
        }, follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.assertEqual(sess["total_questions"], 5)
            self.assertEqual(sess["current_index"], 0)
            self.assertEqual(sess["score"], 0)
            self.assertEqual(len(sess["answers"]), 0)

    def test_09_pdf_upload_and_configuration_limit(self):
        """Verify PDF upload generates questions and enforces length limits without duplication."""
        pdf_path = os.path.join(os.path.dirname(__file__), "uploads", "Technical_Communication_unit_-1_1.pdf")
        if not os.path.exists(pdf_path):
            self.skipTest("Sample PDF not found in uploads directory")

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        upload_resp = self.client.post("/upload", data={
            "pdf_file": (io.BytesIO(pdf_bytes), "Technical_Communication_unit_-1_1.pdf")
        }, content_type="multipart/form-data", follow_redirects=True)

        self.assertEqual(upload_resp.status_code, 200)
        self.assertIn(b"Quiz Configuration", upload_resp.data)
        self.assertIn(b"Extracted from Uploaded PDF", upload_resp.data)

        with self.client.session_transaction() as sess:
            pdf_id = sess["pdf_id"]
            pdf_qs = PDF_STORE[pdf_id]
            available = len(pdf_qs)
            self.assertTrue(available > 0)

        # Excess length rejected
        excess_count = available + 10
        exceed_resp = self.client.post("/configure", data={
            "source": "pdf",
            "question_count": str(excess_count),
            "mode": "adaptive"
        }, follow_redirects=True)
        self.assertIn(b"exceeds the", exceed_resp.data)
        self.assertIn(b"Unrelated questions will not be inserted", exceed_resp.data)

        # Valid length (5 questions) accepted
        valid_resp = self.client.post("/configure", data={
            "source": "pdf",
            "question_count": "5",
            "mode": "adaptive"
        }, follow_redirects=True)
        self.assertEqual(valid_resp.status_code, 200)
        self.assertIn(b"Question 1 / 5", valid_resp.data)

        # Answer all 5 questions
        for i in range(5):
            with self.client.session_transaction() as sess:
                current_q = get_question_by_id("pdf", sess["pdf_id"], sess["current_q_id"])
                ans = current_q["correct_answer"]
                self.assertTrue(str(current_q["id"]).startswith("PDF-"))
            self.client.post("/quiz", data={"option": ans}, follow_redirects=True)
            self.client.post("/quiz", data={"next": "1"}, follow_redirects=True)

        res = self.client.get("/result")
        self.assertIn(b"5 / 5", res.data)
        self.assertIn(b"100.0%", res.data)

if __name__ == "__main__":
    unittest.main()
