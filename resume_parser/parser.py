import re
import importlib

# Try to import PyMuPDF (fitz). If unavailable, keep a None placeholder
try:
    fitz = importlib.import_module("fitz")  # PyMuPDF
except Exception:
    fitz = None

# Try to import spaCy. We will lazy-load the language model (so missing model
# doesn't crash at import time). If spaCy itself isn't installed, set to None.
try:
    spacy = importlib.import_module("spacy")
except Exception:
    spacy = None

SKILL_KEYWORDS = [
    "Python", "Java", "C++", "Machine Learning", "Deep Learning", "Data Science",
    "Django", "Flask", "React", "SQL", "MongoDB", "Git", "HTML", "CSS", "JavaScript"
]


def get_spacy_nlp():
    """Return a loaded spaCy nlp object or None if unavailable.

    We avoid loading the model at import time so that missing models don't
    raise exceptions during module import. If spaCy is installed but the
    English model isn't, we return None (caller should fallback).
    """
    if spacy is None:
        return None
    try:
        return spacy.load("en_core_web_sm")
    except Exception:
        # Could be ModelNotFoundError or other OSError; return None to indicate
        # fallback should be used.
        return None

def extract_text_from_pdf(filepath):
    if fitz is None:
        raise RuntimeError(
            "PyMuPDF (fitz) is not installed. Install it with: \n"
            "    pip install pymupdf\n"
            "or add it to your project's requirements."
        )

    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        # use get_text() which works across many PyMuPDF versions
        text += page.get_text()
    return text

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r"(\+91[\-\s]?)?[789]\d{9}", text)
    return match.group(0) if match else None

def extract_linkedin(text):
    match = re.search(r"https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?", text)
    return match.group(0) if match else None

def extract_skills(text):
    """Extract skills from text.

    Prefer spaCy model-based tokenization when available. If spaCy or the
    model isn't available, fall back to a simple case-insensitive keyword
    search using word-boundary matching.
    """
    # Try spaCy first
    nlp = get_spacy_nlp()
    found = set()
    if nlp is not None:
        doc = nlp(text)
        # match tokens exactly against the SKILL_KEYWORDS (case-sensitive as
        # keywords include C++ and mixed-case items). We'll also do a
        # case-insensitive match for tokens that differ only by case.
        keywords_set = set(SKILL_KEYWORDS)
        keywords_lower = {k.lower(): k for k in SKILL_KEYWORDS}
        for token in doc:
            t = token.text
            if t in keywords_set:
                found.add(t)
            else:
                key = t.lower()
                if key in keywords_lower:
                    found.add(keywords_lower[key])
        return list(found)

    # Fallback: regex word-boundary search (case-insensitive)
    text_lower = text.lower()
    for kw in SKILL_KEYWORDS:
        # use word boundaries to avoid partial matches
        pattern = r"\b" + re.escape(kw.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.add(kw)
    return list(found)

def extract_education(text):
    pattern = r"(B\.?Tech|M\.?Tech|B\.?Sc|M\.?Sc|Bachelor|Master|Ph\.?D).*?(?=\n|,|\.)"
    return list(set(re.findall(pattern, text, flags=re.IGNORECASE)))

def extract_experience(text):
    pattern = r"(\d+)\+?\s*(years|yrs|year)\s*(of)?\s*(experience)?"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return [f"{m[0]} years" for m in matches]

def calculate_resume_score(skills, education, experience, email, phone, linkedin):
    score = 0
    if skills: score += min(len(skills), 10) * 2  # Max 20
    if education: score += 20
    if experience: score += 20
    if email: score += 10
    if phone: score += 10
    if linkedin: score += 20
    return min(score, 100)

def parse_resume(filepath):
    text = extract_text_from_pdf(filepath)

    email = extract_email(text)
    phone = extract_phone(text)
    linkedin = extract_linkedin(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    score = calculate_resume_score(skills, education, experience, email, phone, linkedin)

    return {
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "skills": skills,
        "education": education,
        "experience": experience,
        "score": score
    }
