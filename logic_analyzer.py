"""
Logic Analyzer  --  the core idea of this project.

While a student solves a coding question, they also write the LOGIC (their thinking) in a text box.
This module uses NLP (TF-IDF + cosine similarity) + concept coverage + reasoning-structure features
to estimate how well the student actually understands the problem.

Final logic score (0-100) = weighted mix of:
    35%  semantic similarity with the reference explanation   (TF-IDF cosine, word 1-2 grams)
    35%  concept coverage (key ideas the answer should mention)
    15%  reasoning structure (steps, conditions, loops, reasons, complexity)
    15%  explanation depth (length adequacy)
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STRUCTURE_PATTERNS = {
    "sequence":  r"\b(first|second|then|next|after that|finally|step|1\.|2\.|3\.)\b",
    "condition": r"\b(if|else|otherwise|when|case|edge)\b",
    "iteration": r"\b(loop|for each|iterate|traverse|while|pointer|repeat)\b",
    "reasoning": r"\b(because|so that|therefore|since|hence|in order to)\b",
    "complexity": r"(o\(n\)|o\(1\)|o\(log n\)|o\(n log n\)|time complexity|space complexity)",
}


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _similarity(student: str, reference: str) -> float:
    if not student:
        return 0.0
    try:
        vec = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        m = vec.fit_transform([reference, student])
        return float(cosine_similarity(m[0], m[1])[0][0])
    except ValueError:  # empty vocabulary
        return 0.0


def _concept_coverage(student: str, concepts):
    hit, missed = [], []
    for group in concepts:
        if any(alt in student for alt in group):
            hit.append(group[0])
        else:
            missed.append(group[0])
    return (len(hit) / len(concepts) if concepts else 0.0), hit, missed


def _structure(student: str):
    found = [k for k, p in STRUCTURE_PATTERNS.items() if re.search(p, student)]
    return len(found) / len(STRUCTURE_PATTERNS), found


def analyze_logic(student_text: str, problem: dict, code: str = "") -> dict:
    """Return a dict with score (0-100), level, feedback and diagnostics."""
    s = _clean(student_text)
    words = len(s.split()) if s else 0

    sim = min(1.0, _similarity(s, _clean(problem["reference"])) * 1.6)   # scale: short answers rarely reach 1.0
    cov, hit, missed = _concept_coverage(s, problem["concepts"])
    struct, found = _structure(s)
    depth = min(1.0, words / 45)

    score = 100 * (0.35 * sim + 0.35 * cov + 0.15 * struct + 0.15 * depth)
    if words < 5:
        score = min(score, 10)           # practically no explanation

    if score >= 75:
        level = "Strong understanding"
    elif score >= 50:
        level = "Moderate understanding"
    elif score >= 25:
        level = "Basic understanding"
    else:
        level = "Weak / no explanation"

    feedback = []
    if words < 20:
        feedback.append("Explanation is too short - describe your approach step by step.")
    if missed:
        feedback.append("Try to mention: " + ", ".join(missed[:4]) + ".")
    if "complexity" not in found:
        feedback.append("Add the time complexity of your approach (e.g. O(n)).")
    if "condition" not in found:
        feedback.append("Mention edge cases / conditions you handle.")
    if not feedback:
        feedback.append("Great, clear and complete explanation!")

    return {
        "score": round(score, 1),
        "level": level,
        "similarity": round(sim * 100, 1),
        "coverage": round(cov * 100, 1),
        "structure": round(struct * 100, 1),
        "words": words,
        "concepts_hit": hit,
        "concepts_missed": missed,
        "feedback": feedback,
    }


def consistency_flag(code_pct: float, logic_pct: float) -> str:
    """Compare code correctness with the quality of written logic."""
    if code_pct >= 80 and logic_pct < 30:
        return "Code is correct but logic explanation is weak - possible copied/memorised solution."
    if code_pct < 40 and logic_pct >= 60:
        return "Good conceptual understanding but weak implementation - needs coding practice."
    if code_pct >= 70 and logic_pct >= 60:
        return "Strong: correct code and clear reasoning."
    return "Needs improvement in both implementation and explanation."
