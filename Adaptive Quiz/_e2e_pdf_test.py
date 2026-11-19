import os
import sys

# Ensure the project root is importable
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Load .env exactly as the app does
from dotenv import load_dotenv
load_dotenv(override=True)

import gemini_service

# 1. Verify model resolution
resolved = gemini_service.get_model_name()
print("RESOLVED_MODEL=" + resolved)

# 2. Build a small text-based sample PDF
import pymupdf as fitz

SAMPLE_PDF = os.path.abspath("uploads/TestSample_pdf.pdf")
os.makedirs("uploads", exist_ok=True)

if not os.path.exists(SAMPLE_PDF):
    doc = fitz.open()
    doc.insert_text((72, 72), "Sample Study Material for Adaptive Quiz Testing.")
    doc.insert_text((72, 120), "Distributed systems require concurrency control and process synchronization.")
    doc.insert_text((72, 160), "Deadlocks occur when four necessary conditions hold simultaneously.")
    doc.insert_text((72, 200), "Pipelining improves throughput by overlapping instruction execution stages.")
    doc.insert_text((72, 240), "Memory hierarchy design balances latency and capacity.")
    doc.insert_text((72, 280), "Virtual memory allows processes to use more memory than physically available.")
    doc.save(SAMPLE_PDF)
    doc.close()

# 3. Run the full pipeline (no real API call; Gemini is not configured in this env)
env_before = dict(os.environ)
try:
    # Remove the key so is_gemini_configured() returns False -> path goes to offline rule-based
    os.environ.pop("GEMINI_API_KEY", None)
    result = gemini_service.process_pdf_material(SAMPLE_PDF, target_count=6)
finally:
    os.environ.update(env_before)

print("METHOD=" + str(result.get("method")))
print("QUESTION_COUNT=" + str(len(result.get("questions", []))))
print("ERROR=" + str(result.get("error")))

# 4. Validate each returned question
validated = [q for q in result.get("questions", []) if gemini_service.validate_question(q)]
print("VALIDATED_COUNT=" + str(len(validated)))
for q in validated:
    print("Q_PROTOTYPE: [" + q.get("difficulty", "?") + "] " + q.get("question", ""))
    print("  OPTIONS=" + str(q.get("options")))
    print("  CORRECT=" + str(q.get("correct_answer")))
    print("  EXPLANATION=" + str(q.get("explanation")))

# Report
if result.get("error"):
    print("FAILURE_ERROR=" + str(result["error"]))
elif len(validated) >= 1:
    print("END_TO_END_OK=YES")
else:
    print("END_TO_END_OK=NO")
