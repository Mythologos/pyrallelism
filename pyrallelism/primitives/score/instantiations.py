from numpy import int64, zeros
from numpy.typing import NDArray

from pyrallelism.primitives.assignment.lsa import LinearSumAssigner
from pyrallelism.primitives.typing import BranchedWordSet, Parallelism
from pyrallelism.primitives.score.base import ScoringFunction
from pyrallelism.primitives.conversion.instantiations import BranchedWordConverter


class ExactScorer(ScoringFunction):
    """
    .. py:class:: ExactScorer
    Subclass of `ScoringFunction` which gives a score of `1` if two `Parallelism` objects are equal;
    otherwise, it gives a score of `0`.
    """
    @classmethod
    def score_pair(cls, hypothesis: Parallelism, reference: Parallelism, **kwargs) -> int:
        score: int = 1 if hypothesis == reference else 0
        return score


class MaximumParallelBranchScorer(ScoringFunction):
    """
    .. py:class:: MaximumParallelBranchScorer
    Subclass of `ScoringFunction` which scores two `Parallelism` objects on their branch overlap.
    Branches must match exactly to count. A score is nonzero if and only if more than one pair of branches match;
    the maximal score for this function is `min(len(hypothesis), len(reference))`,
    where the `hypothesis` and `reference` are `Parallelism` objects.
    """
    @classmethod
    def score_pair(cls, hypothesis: Parallelism, reference: Parallelism, **kwargs) -> int:
        branch_intersection: set[tuple[int, int]] = hypothesis.intersection(reference)
        score: int = len(branch_intersection) if len(branch_intersection) > 1 else 0
        return score


class MaximumBranchAwareWordOverlapScorer(ScoringFunction, LinearSumAssigner):
    """
    .. py:class:: MaximumBranchAwareWordOverlapScorer
    Subclass of `ScoringFunction` which scores two `Parallelism` objects on their branched word-level overlap.
    The class performs an internal maximum bipartite matching with respect to word-level overlap.
    It does so to examine whether at least two pairs of branches match and
    what the maximal matching between branches is.
    The score produced by this class is `0` if either:

    - there is no overlap, or
    - there is some overlap but only between one pair of branches.

    Otherwise, the maximum score produced is the minimum number of words present in the parallelisms examined.
    Assuming that the parallelisms supplied are nonempty, this score must be at least `2`,
    as a match with a score of `1` is only possible if one (and only one) pair of branches match;
    this would be zeroed out in accordance with the aforementioned second condition.
    """
    @classmethod
    def score_pair(cls, hypothesis: Parallelism, reference: Parallelism, **kwargs) -> int:
        converted_hypothesis: BranchedWordSet = BranchedWordConverter.convert_parallelism(hypothesis)
        converted_reference: BranchedWordSet = BranchedWordConverter.convert_parallelism(reference)
        score: int = cls._get_branched_word_score(converted_hypothesis, converted_reference)
        return score

    @classmethod
    def _get_branched_word_score(cls, hypothesis: BranchedWordSet, reference: BranchedWordSet) -> int:
        """
        :param hypothesis: a parallelism in the form of a `BranchedWordSet` from the collection of hypotheses.
        :param reference: a `parallelism in the form of a `BranchedWordSet` from the collection of references.
        :return: a nonnegative `int` score representing how well *hypothesis* and *reference* match.
        """
        matrix_dimension: int = max(len(hypothesis), len(reference))
        branched_score_matrix: NDArray[int] = zeros((matrix_dimension, matrix_dimension), dtype=int64)
        for hypothesis_index, hypothesis_branch in enumerate(hypothesis, 0):
            for reference_index, reference_branch in enumerate(reference, 0):
                word_intersection: set[int] = hypothesis_branch.intersection(reference_branch)
                branched_score_matrix[hypothesis_index][reference_index] = len(word_intersection)

        lsa_entries: list[tuple[int, int]] = cls.get_lsa_entries(branched_score_matrix)
        branched_word_terms: list[int] = cls.get_lsa_terms(branched_score_matrix, lsa_entries)
        nonzero_branched_word_terms: list[int] = [term for term in branched_word_terms if term > 0]
        branched_word_score = 0 if len(nonzero_branched_word_terms) <= 1 else sum(branched_word_terms)

        return branched_word_score


class MaximumWordOverlapScorer(ScoringFunction):
    """
    .. py:class:: MaximumBranchAwareWordOverlapScorer
    Subclass of `ScoringFunction` which scores two `Parallelism` objects on their word-level overlap.
    The maximum possible score is the minimum number of words present out of
    the `hypothesis` and `reference` parallelisms.
    """
    @classmethod
    def score_pair(cls, hypothesis: Parallelism, reference: Parallelism, **kwargs) -> int:
        converted_hypothesis: BranchedWordSet = BranchedWordConverter.convert_parallelism(hypothesis)
        converted_reference: BranchedWordSet = BranchedWordConverter.convert_parallelism(reference)
        hypothesis_set: set[int] = set(token for branch in converted_hypothesis for token in branch)
        reference_set: set[int] = set(token for branch in converted_reference for token in branch)
        word_overlap_set: set[int] = hypothesis_set.intersection(reference_set)
        score: int = len(word_overlap_set)
        return score
