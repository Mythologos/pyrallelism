from typing import Sequence, TypeAlias
from unittest import TestCase

from src.pyrallelism.evaluator import evaluate_bipartite_parallelism_metric
from src.pyrallelism.primitives.evaluation_metric import DefinedMetric, DEFINED_METRICS, EvaluationMetric, get_metric
from src.pyrallelism.primitives.loading import XMLLoader, TSVLoader
from src.pyrallelism.primitives.typing import ParallelismDirectory

AnswerDict: TypeAlias = dict[str, tuple[int, int, int]]


class EvaluationTester(TestCase):
    """
    .. py:class:: EvaluationTester
    Class to test the main function of this module: *evaluate_bipartite_parallelism_metric*,
    as it brings much of the underlying code together.
    """
    def setUp(self):
        # Should define the files to be used, the desired results corresponding to each metric.
        self.base_directory = "data"
        self.ground_truth_xml = "wikipedia_gt.xml"

        self.stratum_count: int = 2
        self.loading_kwargs: dict[str, int] = {"stratum_count": self.stratum_count}

        ground_truth_filepath: str = f"{self.base_directory}/{self.ground_truth_xml}"
        self.reference_directory: ParallelismDirectory = \
            XMLLoader.load_parallelism_directory(ground_truth_filepath, **self.loading_kwargs)

        perfect_answers: AnswerDict = {
            DefinedMetric.EXACT_PARALLELISM_MATCH: (4, 4, 4),
            DefinedMetric.MAXIMUM_PARALLELISM_BRANCH_MATCH: (12, 12, 12),
            DefinedMetric.MAXIMUM_BRANCH_AWARE_WORD_OVERLAP: (82, 82, 82),
            DefinedMetric.MAXIMUM_WORD_OVERLAP: (82, 82, 82)
        }
        flawed_answers: AnswerDict = {
            DefinedMetric.EXACT_PARALLELISM_MATCH: (1, 4, 4),
            DefinedMetric.MAXIMUM_PARALLELISM_BRANCH_MATCH: (5, 10, 12),
            DefinedMetric.MAXIMUM_BRANCH_AWARE_WORD_OVERLAP: (29, 44, 82),
            DefinedMetric.MAXIMUM_WORD_OVERLAP: (41, 44, 82)
        }

        self.evaluation_answers: Sequence[tuple[str, AnswerDict]] = (
            (f"{self.base_directory}/wikipedia_perfect_hyp.tsv", perfect_answers),
            (f"{self.base_directory}/wikipedia_flawed_hyp.tsv", flawed_answers)
        )

    def test_evaluations(self):
        for filepath, answers in self.evaluation_answers:
            self._test_evaluation(filepath, answers)

    def _test_evaluation(self, hypothesis_filepath: str, evaluation_answers: dict[str, tuple[int, int, int]]):
        hypothesis_directory: ParallelismDirectory = \
            TSVLoader.load_parallelism_directory(hypothesis_filepath, **self.loading_kwargs)

        for defined_metric in DEFINED_METRICS:
            metric: EvaluationMetric = get_metric(defined_metric)
            confusion_matrix, _ = \
                evaluate_bipartite_parallelism_metric(hypothesis_directory, self.reference_directory, metric)
            expected_score, expected_hypotheses, expected_references = evaluation_answers[defined_metric]
            self.assertEqual(expected_score, confusion_matrix.score)
            self.assertEqual(expected_hypotheses, confusion_matrix.hypothesis_count)
            self.assertEqual(expected_references, confusion_matrix.reference_count)
