from abc import abstractmethod

from numpy import int64, zeros
from numpy.typing import NDArray

from ..typing import Parallelism, ParallelismDirectory


class ScoringFunction:
    """
    .. py:class:: ScoringFunction
    Base class for scoring the similarity between two `Parallelism` (or converted parallelism) objects.
    """
    @classmethod
    def create_score_matrix(cls, hypotheses: ParallelismDirectory, references: ParallelismDirectory, **kwargs) -> \
            NDArray[int]:
        """
        Computes a two-dimensional `NDArray` containing the scores for all pairs of
        hypothesis and reference parallelisms.
        :param hypotheses: a collection of `Parallelism` objects; represents a set of guesses from a model.
        :param references: a collection of `Parallelism` objects; represents a set of ground truth values.
        :param kwargs: a collection of keyword arguments meant to modify the scoring of parallelism pairs.
        :return: a two-dimensional, square `NDArray` containing `int` scores for all pairs of
        hypothesis and reference parallelisms.
        """
        matrix_size: int = max(len(hypotheses), len(references))
        score_matrix: NDArray[int] = zeros((matrix_size, matrix_size), dtype=int64)
        for hypothesis_index, (hypothesis) in enumerate(hypotheses.values()):
            for reference_index, (reference) in enumerate(references.values()):
                score_matrix[hypothesis_index, reference_index] = cls.score_pair(hypothesis, reference, **kwargs)

        return score_matrix

    @classmethod
    @abstractmethod
    def score_pair(cls, hypothesis: Parallelism, reference: Parallelism, **kwargs) -> int:
        """
        Computes the matching score for a given hypothesis `Parallelism` and reference `Parallelism`.
        :param hypothesis: a `Parallelism` from the collection of hypotheses.
        :param reference: a `Parallelism` from the collection of references.
        :param kwargs: a collection of keyword arguments meant to modify the scoring of parallelism pairs.
        :return: a nonnegative `int` score representing how well *hypothesis* and *reference* match.
        """
        raise NotImplementedError
