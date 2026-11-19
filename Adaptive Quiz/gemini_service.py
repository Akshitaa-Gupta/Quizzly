import os
import json
import re
from difflib import SequenceMatcher
from dotenv import load_dotenv
import pymupdf as fitz
from questions import ConceptQuestionGenerator

# Load .env file
load_dotenv()

def get_api_key():
    """Retrieves GEMINI_API_KEY securely from environment without printing or exposing."""
    return os.getenv("GEMINI_API_KEY", "").strip()

def get_model_name():
    """Returns a verified, free-tier, multimodal (vision-capable) Gemini model name for PDF/vision input.

    Uses the GEMINI_MODEL env var when it is set, and validates it against a known-good
    allow-list. The default is gemini-3.8-flash, which Google's API recommends as the
    replacement for the now-unavailable gemini-2.5-flash.

    Any model name that is not in the allow-list (including stale/invalid values such as
    gemini-2.5-flash) is rejected and falls back to gemini-3.8-flash so the API never
    receives a model that it will reject with a 404.
    """
    allowed = {
        "gemini-3.8-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
        "gemma-4-31b-it",
        "gemma-4-26b-a4b-it",
    }
    raw = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    if raw and raw in allowed:
        return raw
    return "gemini-3.8-flash"




def is_gemini_configured():
    """Checks whether a non-placeholder GEMINI_API_KEY is present."""
    key = get_api_key()
    return bool(key and key != "your_gemini_api_key_here")

def validate_question(q):
    """
    Strict validation gate for MCQs:
    - Must be a dictionary with required keys
    - Question must end with ? and have reasonable length (> 15 chars)
    - Must NOT be a broken fragment (e.g. 'What is It?')
    - Exactly 4 distinct options
    - Correct answer must be one of 'A', 'B', 'C', 'D'
    - Options must not be overly similar or identical
    """
    if not isinstance(q, dict):
        return False

    req_keys = ("question", "options", "correct_answer", "explanation", "difficulty")
    if not all(k in q for k in req_keys):
        return False

    question = str(q["question"]).strip()
    if len(question) < 18 or not question.endswith("?"):
        return False

    # Block undesirable generated fragments
    low_q = question.lower()
    banned_phrases = (
        "what is it?", "what is this?", "what is that?",
        "what is but", "what is however", "what is and",
        "according to the pdf, what is", "what is the 7 cs of communication?"
    )
    if any(b in low_q for b in banned_phrases):
        return False

    # Options validation: exactly 4 distinct options
    options = q.get("options")
    if not isinstance(options, dict) or set(options.keys()) != {"A", "B", "C", "D"}:
        return False

    opt_values = [str(options[k]).strip() for k in ("A", "B", "C", "D")]
    # Check for empty options
    if any(len(v) < 1 for v in opt_values):
        return False

    # Check that all four options are distinct
    if len(set(v.lower() for v in opt_values)) < 4:
        return False

    # Check for literally identical options (ratio > 0.98 on long strings)
    for i in range(4):
        for j in range(i + 1, 4):
            if len(opt_values[i]) > 30 and len(opt_values[j]) > 30:
                if SequenceMatcher(None, opt_values[i].lower(), opt_values[j].lower()).ratio() > 0.98:
                    return False

    if q.get("correct_answer") not in ("A", "B", "C", "D"):
        return False

    if not str(q.get("explanation", "")).strip():
        return False

    if q.get("difficulty") not in ("Easy", "Medium", "Hard"):
        q["difficulty"] = "Medium"

    return True

def extract_pdf_info(filepath):
    """
    Analyzes PDF content:
    - Extracts embedded text
    - Determines page count
    - Classifies if scanned / handwritten (minimal or no extractable text)
    """
    doc = fitz.open(filepath)
    total_pages = len(doc)
    extracted_text = ""
    pages_with_images = 0

    for page_idx, page in enumerate(doc):
        t = page.get_text("text").strip()
        if t:
            extracted_text += t + "\n"
        images = page.get_images()
        if images:
            pages_with_images += 1

    doc.close()

    total_words = len(extracted_text.split())
    # If very few words per page, it is likely scanned, image-only, or handwritten.
    # Many real textbook pages have 40+ words but handwritten notes have far fewer.
    # Use a more robust combined signal: low text ratio OR high-image ratio OR text-only short.
    image_page_ratio = pages_with_images / max(total_pages, 1)
    is_scanned_or_handwritten = (
        total_words < 40 * total_pages
        or len(extracted_text.strip()) < 100
        or image_page_ratio >= 0.5
    )

    return {
        "text": extracted_text,
        "page_count": total_pages,
        "is_scanned_or_handwritten": is_scanned_or_handwritten,
        "word_count": total_words
    }

def generate_questions_with_gemini(filepath, is_handwritten=False, target_count=10):
    """
    Generates high-quality academic MCQs via the Google Gemini API using google-genai SDK.
    Supports multimodal input (images of pages for handwritten/scanned PDFs)
    and text input for text-based PDFs.
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured in .env.")

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    model_name = get_model_name()

    prompt = f"""
You are an expert Computer Science university professor creating an exam for second-year B.Tech students.
Your task is to generate high-quality, professional, concept-based multiple choice questions (MCQs) directly from the provided study material.

CRITICAL QUALITY REQUIREMENTS:
1. Every question must be clear, natural, grammatically sound, and test a meaningful technical or theoretical concept.
2. Under NO circumstances generate questions like "What is It?", "What is this?", "What is But noise...", or questions containing broken grammar or vague pronouns.
3. Each question must have EXACTLY 4 distinct, plausible options labeled A, B, C, and D.
4. Exactly one option must be the correct answer.
5. Provide a concise, clear one-line explanation for why the correct option is right.
6. Assign a difficulty level: "Easy", "Medium", or "Hard".
7. Include the core concept tested (e.g. "Pipelining Hazards", "Process Synchronization", "Formal Communication").
8. Do NOT use generic prefixes like "According to the PDF" or "Based on the text". Frame questions naturally. NEVER begin a question with "According to the study material", "According to the PDF", "Based on the study material", "According to the passage", "Based on the passage", "In the text", "As stated in the document", "In the document", "Per the material", or any similar source-referencing phrase. Write questions as direct questions a professor would ask a student.


9. Handwritten notes or diagrams are present, carefully transcribe the technical terms, equations, and concepts and base the questions strictly on what is written. Do not hallucinate concepts not present in the material. Help the model by including, together with the page images, a concise transcription of any legible handwritten text so it can extract precise facts, numbers, definitions, and relationships for MCQ generation.

10. Each question must be independently answerable without referring back to the source document.

Target: Generate between {min(target_count, 15)} and {min(target_count + 5, 20)} distinct questions.

Respond ONLY with valid JSON matching this schema:
[
  {{
    "question": "Clear and complete question text ending with a question mark?",
    "options": {{
      "A": "First plausible option",
      "B": "Second plausible option",
      "C": "Third plausible option",
      "D": "Fourth plausible option"
    }},
    "correct_answer": "A",
    "explanation": "Clear one-line explanation.",
    "difficulty": "Easy",
    "concept": "Core Concept Name",
    "source_page": 1
  }}
]
"""

    contents = []

    if is_handwritten:
        # Multimodal path: render PDF pages as high-res images for Gemini vision,
        # and also provide a text transcription of any legible text found on the page.
        doc = fitz.open(filepath)
        max_pages = min(len(doc), 8)  # Read up to 8 pages to remain within free-tier quota
        for i in range(max_pages):
            page = doc[i]
            pix = page.get_pixmap(dpi=140)
            img_bytes = pix.tobytes("jpeg")
            part = types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg")
            contents.append(part)

            # Transcribe any legible text on the page so the model has explicit
            # textual signal for extracting precise facts/definitions.
            page_text = page.get_text("text").strip()
            if page_text:
                contents.append(
                    types.Part.from_text(
                        text=f"[Transcription of page {i + 1} handwritten notes]:\n{page_text}\n"
                    )
                )
        doc.close()
        contents.append(prompt)
    else:
        # Text-based PDF path: extract text and send as prompt
        doc = fitz.open(filepath)
        full_text = "\n".join(page.get_text("text") for page in doc)
        doc.close()
        # Truncate text if excessively long to respect free-tier token windows
        trimmed_text = full_text[:25000]
        contents.append(f"STUDY MATERIAL CONTENT:\n{trimmed_text}\n\n{prompt}")

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
    except Exception as e:
        err_msg = str(e).lower()
        if "429" in err_msg or "resource_exhausted" in err_msg or "quota" in err_msg:
            raise RuntimeError("Gemini API free-tier quota exceeded or rate-limited. Please wait a moment or try again.")
        elif "api_key" in err_msg or "400" in err_msg or "unauthorized" in err_msg:
            raise RuntimeError("Gemini API key is invalid or unauthorized. Please verify your GEMINI_API_KEY in .env.")
        else:
            raise RuntimeError(f"Gemini API request failed: {str(e)}")

    if not response or not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    raw_json = response.text.strip()
    # Strip markdown code blocks if wrapped
    if raw_json.startswith("```"):
        raw_json = re.sub(r"^```(?:json)?\s*", "", raw_json)
        raw_json = re.sub(r"\s*```$", "", raw_json)

    try:
        parsed = json.loads(raw_json)
    except Exception as e:
        raise ValueError(f"Failed to parse Gemini output as structured JSON: {str(e)}")

    if not isinstance(parsed, list):
        if isinstance(parsed, dict) and "questions" in parsed:
            parsed = parsed["questions"]
        else:
            raise ValueError("Gemini output format was not a list of questions.")

    validated = []
    seen_stems = set()
    for item in parsed:
        if validate_question(item):
            norm_stem = re.sub(r"\s+", " ", item["question"].strip().lower())
            if norm_stem not in seen_stems:
                seen_stems.add(norm_stem)
                validated.append(item)

    return validated

def process_pdf_material(filepath, target_count=10):
    """
    Main entry point for processing uploaded PDF study material.
    Returns:
        dict with keys:
            - questions: list of validated question dicts
            - method: 'gemini_multimodal', 'gemini_text', or 'offline_rule_based'
            - is_scanned_or_handwritten: bool
            - page_count: int
            - error: optional error string
    """
    pdf_info = extract_pdf_info(filepath)
    is_handwritten = pdf_info["is_scanned_or_handwritten"]
    page_count = pdf_info["page_count"]
    text = pdf_info["text"]

    # Determine if the document's text is too sparse to be useful for the text path.
    # If so, use the multimodal (vision) path for scanned/handwritten content.
    can_use_text_path = len(text.strip()) >= 100

    # Compute page-image ratio from pdf_info's word_count context is insufficient;
    # recompute the image page count here to decide routing reliably.
    page_doc = fitz.open(filepath)
    pages_with_images = sum(1 for p in page_doc if p.get_images())
    page_doc.close()
    image_page_ratio = pages_with_images / max(page_count, 1)

    if is_gemini_configured():
        try:
            questions = generate_questions_with_gemini(
                filepath,
                is_handwritten=is_handwritten or (not can_use_text_path and image_page_ratio >= 0.5),
                target_count=target_count
            )
            if questions:
                method = "gemini_multimodal" if is_handwritten else "gemini_text"
                return {
                    "questions": questions,
                    "method": method,
                    "is_scanned_or_handwritten": is_handwritten,
                    "page_count": page_count,
                    "error": None
                }
        except Exception as e:
            # If handwritten, cannot extract text via PyMuPDF rules
            if is_handwritten:
                return {
                    "questions": [],
                    "method": "gemini_multimodal",
                    "is_scanned_or_handwritten": True,
                    "page_count": page_count,
                    "error": str(e)
                }
            # For text-based, fallback to offline rule-based generator
            pass

    # 2. If handwritten and Gemini not available / failed
    if is_handwritten:
        return {
            "questions": [],
            "method": "unsupported",
            "is_scanned_or_handwritten": True,
            "page_count": page_count,
            "error": "This document appears to contain scanned or handwritten content without embedded text. To extract questions, please ensure a valid GEMINI_API_KEY is configured in your .env file."
        }

    # 3. Offline rule-based extraction for embedded text
    offline_gen = ConceptQuestionGenerator()
    offline_questions = offline_gen.generate_questions(pdf_info["text"], target_count=target_count * 2)

    valid_offline = []
    seen = set()
    for q in offline_questions:
        if validate_question(q):
            norm = q["question"].strip().lower()
            if norm not in seen:
                seen.add(norm)
                valid_offline.append(q)

    if not valid_offline:
        return {
            "questions": [],
            "method": "offline_rule_based",
            "is_scanned_or_handwritten": False,
            "page_count": page_count,
            "error": "Could not extract sufficient concept definitions from this PDF. Please ensure the document has clear textbook explanations and headings."
        }

    return {
        "questions": valid_offline,
        "method": "offline_rule_based",
        "is_scanned_or_handwritten": False,
        "page_count": page_count,
        "error": None
    }
