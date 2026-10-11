"""Score an AI response against a weighted rubric."""
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Criterion:
    name: str
    weight: float
    check: Callable[[str], float]  # must return a score from 0.0 to 1.0


@dataclass
class ScoreReport:
    total: float
    details: dict = field(default_factory=dict)


def score_response(response: str, rubric: list[Criterion]) -> ScoreReport:
    if not rubric:
        raise ValueError("rubric must contain at least one criterion")
    total_weight = sum(c.weight for c in rubric)
    if total_weight <= 0:
        raise ValueError("total weight must be positive")

    details = {}
    weighted_sum = 0.0
    for criterion in rubric:
        score = criterion.check(response)
        if not 0.0 <= score <= 1.0:
            raise ValueError(f"criterion {criterion.name!r} returned {score}, expected 0 to 1")
        details[criterion.name] = score
        weighted_sum += score * criterion.weight
    return ScoreReport(total=round(weighted_sum / total_weight, 4), details=details)


def contains_all(terms):
    """Fraction of required terms that appear in the response."""
    if not terms:
        raise ValueError("terms must not be empty")

    def check(text):
        lowered = text.lower()
        return sum(1 for t in terms if t.lower() in lowered) / len(terms)

    return check


def max_words(limit):
    """Full score up to the limit, then the score drops as the response runs longer."""
    if limit <= 0:
        raise ValueError("limit must be positive")

    def check(text):
        n = len(text.split())
        if n <= limit:
            return 1.0
        return max(0.0, 1 - (n - limit) / limit)

    return check


def avoids(phrases):
    """Score 0 if any forbidden phrase appears, otherwise 1."""
    def check(text):
        lowered = text.lower()
        return 0.0 if any(p.lower() in lowered for p in phrases) else 1.0

    return check
