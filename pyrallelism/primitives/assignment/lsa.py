from numpy.typing import NDArray
from scipy.optimize import linear_sum_assignment


class LinearSumAssigner:
    """
    .. py:class:: LinearSumAssigner
    Maintains all functions related to computing the maximal bipartite matching from a two-dimensional `NDArray`.
    """
    @staticmethod
    def get_lsa_entries(scoring_matrix: NDArray[int]) -> list[tuple[int, int]]:
        """
        Computes the linear sum assignment of a two-dimensional ``NDArray`` and collects the resulting entries
        in a single ``list`` of coordinates.
        :param scoring_matrix: a two-dimensional ``NDArray`` containing nonnegative ``int`` score values.
        :return: a ``list`` of indices to the input matrix indicating values that are part of the maximal score.
        """
        rows, columns = linear_sum_assignment(scoring_matrix, maximize=True)   # type: ignore
        entries: list[tuple[int, int]] = zip(rows, columns)
        return entries

    @classmethod
    def get_lsa_score(cls, scoring_matrix: NDArray[int], entries: list[tuple[int, int]]) -> int:
        """
        Computes the score of a linear sum assignment with a two-dimensional ``NDArray``
        and a set of indices to that ``NDArray``.
        :param scoring_matrix: a two-dimensional NDArray containing nonnegative ``int`` score values.
        :param entries: a ``list`` of indices to the input matrix indicating values that are part of the maximal score.
        :return: a nonnegative ``int`` representing the maximal linear sum assignment score.
        """
        lsa_score: int = sum(cls.get_lsa_terms(scoring_matrix, entries))
        return lsa_score

    @staticmethod
    def get_lsa_terms(scoring_matrix: NDArray[int], entries: list[tuple[int, int]]) -> list[int]:
        """
        Collects the scores involved in the maximal matching determined by linear sum assignment.
        :param scoring_matrix: a two-dimensional ``NDArray`` containing nonnegative ``int`` score values.
        :param entries: a ``list`` of indices to the input matrix indicating values that are part of the maximal score.
        :return: a ``list`` of ``int`` values representing individual bipartite matching scores within
        a maximal matching.
        """
        lsa_terms: list[int] = [scoring_matrix[row_index][column_index] for (row_index, column_index) in entries]
        return lsa_terms
