# Rubric Scorer

Scores an AI response against a weighted checklist. Each criterion returns a score from 0 to 1, and the total is a weighted average.

**Skills shown:** writing evaluation rubrics, turning quality criteria into code, testing edge cases.

## Run the tests

```
python3 -m unittest -v
```

## Example

```python
from rubric_scorer import Criterion, contains_all, avoids, max_words, score_response

rubric = [
    Criterion("coverage", 2, contains_all(["Lagos", "Abuja"])),
    Criterion("length", 1, max_words(60)),
    Criterion("safety", 1, avoids(["guaranteed returns"])),
]
print(score_response(response_text, rubric))
```
