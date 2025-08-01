from typing import Callable, List, Optional, Type

from rapidfuzz import fuzz
from sqlalchemy.orm import Session

DEFAULT_FUZZY_MATCH_THRESHOLD = 85


def fuzzy_match_single(
    db: Session,
    model: Type,
    input_str: str,
    field: Callable,
    threshold: int = DEFAULT_FUZZY_MATCH_THRESHOLD
) -> Optional[object]:
    candidates: List[object] = db.query(model).all()
    best_match = None
    best_score = 0

    for candidate in candidates:
        candidate_value = field(candidate)
        score = fuzz.ratio(input_str.lower(), candidate_value.lower())
        if score > best_score:
            best_score = score
            best_match = candidate

    if best_score >= threshold:
        return best_match
    return None


def fuzzy_match_composite(
    db: Session,
    model: Type,
    input_fields: dict,  # {"name": "ABCD", "slug": "abcd"}
    # {"name": lambda x: x.name, "slug": lambda x: x.slug}
    field_extractors: dict,
    weights: dict = None,
    threshold: int = DEFAULT_FUZZY_MATCH_THRESHOLD
) -> Optional[object]:
    if weights is None:
        weights = {k: 1.0 for k in input_fields}

    candidates = db.query(model).all()
    best_score = 0
    best_match = None

    for candidate in candidates:
        score = 0
        for key, input_val in input_fields.items():
            val = field_extractors[key](candidate)
            score += fuzz.ratio(
                input_val.lower(), val.lower()
            ) * weights.get(key, 1.0)
        if score > best_score:
            best_score = score
            best_match = candidate

    if best_score >= threshold:
        return best_match
    return None
