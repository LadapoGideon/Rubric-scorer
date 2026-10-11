import unittest

from rubric_scorer import Criterion, contains_all, avoids, max_words, score_response


class RubricScorerTests(unittest.TestCase):
    def test_perfect_response_scores_one(self):
        rubric = [
            Criterion("coverage", 2, contains_all(["Lagos", "Abuja"])),
            Criterion("length", 1, max_words(50)),
        ]
        report = score_response("Lagos is big. Abuja is the capital.", rubric)
        self.assertEqual(report.total, 1.0)

    def test_weights_are_applied(self):
        rubric = [
            Criterion("coverage", 3, contains_all(["Lagos", "Abuja"])),  # 0.5 * 3
            Criterion("safety", 1, avoids(["guaranteed"])),              # 1.0 * 1
        ]
        report = score_response("Lagos is big.", rubric)
        self.assertEqual(report.total, round((1.5 + 1.0) / 4, 4))
        self.assertEqual(report.details["coverage"], 0.5)

    def test_forbidden_phrase_zeroes_criterion(self):
        self.assertEqual(avoids(["guaranteed"])("This is guaranteed to work"), 0.0)

    def test_long_response_is_penalised_not_zeroed_immediately(self):
        check = max_words(10)
        self.assertEqual(check("one two three"), 1.0)
        self.assertLess(check(" ".join(["w"] * 15)), 1.0)

    def test_bad_criterion_output_is_rejected(self):
        rubric = [Criterion("broken", 1, lambda text: 1.5)]
        with self.assertRaises(ValueError):
            score_response("anything", rubric)

    def test_empty_rubric_is_rejected(self):
        with self.assertRaises(ValueError):
            score_response("anything", [])


if __name__ == "__main__":
    unittest.main()
