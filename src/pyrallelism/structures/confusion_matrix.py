from __future__ import annotations

from typing import Optional, Sequence


class ReducedConfusionMatrix:
    """
    .. py:class:: ReducedConfusionMatrix
    Data structure class to accumulate classification results. It represents a "reduced" version of a confusion matrix,
    where we cannot feasibly tabulate all the true negative values.
    This class is intended to compute and display precision, recall, and the F-\u03B2 scores.
    Moreover, it can aggregate such metrics across multiple individual matrices.
    """
    def __init__(self):
        super().__init__()
        self.score: int = 0
        self.hypothesis_count: int = 0
        self.reference_count: int = 0

    def __add__(self, other: ReducedConfusionMatrix) -> ReducedConfusionMatrix:
        """
        Adds two `ReducedConfusionMatrix` instances together to create a new `ReducedConfusionMatrix`.
        Addition occurs via summing each attribute--`score`, `hypothesis_count`, and `reference_count`.
        :param other: the second operand of the `ReducedConfusionMatrix` addition.
        :return: a new `ReducedConfusionMatrix` with summed attributes.
        """
        new_matrix: ReducedConfusionMatrix = ReducedConfusionMatrix()
        if isinstance(other, ReducedConfusionMatrix):
            new_matrix.score = self.score + other.score
            new_matrix.hypothesis_count = self.hypothesis_count + other.hypothesis_count
            new_matrix.reference_count = self.reference_count + other.reference_count
        else:
            raise TypeError(f"The value <{other}> is not a MatchingConfusionMatrix. Please try again.")
        return new_matrix

    def __iadd__(self, other):
        """
        Adds two `ReducedConfusionMatrix` instances together in-place.
        Addition occurs via summing each attribute--`score`, `hypothesis_count`, and `reference_count`.
        :param other: the second operand of the `ReducedConfusionMatrix` addition.
        :return: the current `ReducedConfusionMatrix` object.
        """
        if isinstance(other, ReducedConfusionMatrix):
            self.score += other.score
            self.hypothesis_count += other.hypothesis_count
            self.reference_count += other.reference_count
        else:
            raise TypeError(f"The value <{other}> is not a MatchBox. Please try again.")
        return self

    def calculate_precision(self) -> float:
        """
        Calculates the precision of the current `ReducedConfusionMatrix`.
        It accommodates for various cases as follows:
            - If `hypothesis_count` is less than zero, a `ValueError` is raised.
            - If `hypothesis_count` is zero, `0.0` is returned.
            - If `score` is less than zero, a `ValueError` is raised.
            - If none of the above are true, then the precision is calculated as `score / hypothesis_count`.
        :return: a `float` indicating the precision metric of the current `ReducedConfusionMatrix` object.
        """
        if self.hypothesis_count < 0:
            raise ValueError("The sum of all hypotheses is negative, which should not be possible.")
        elif self.hypothesis_count == 0:
            precision = 0.0
        else:
            if self.score < 0:
                raise ValueError("The score is negative, which should not be possible.")
            else:
                precision: float = self.score / self.hypothesis_count

        return precision

    def calculate_recall(self) -> Optional[float]:
        """
        Calculates the recall of the current `ReducedConfusionMatrix`.
        It accommodates for various cases as follows:
            - If `reference_count` is less than zero, a `ValueError` is raised.
            - If `reference_count` is zero, `0.0` is returned.
            - If `score` is less than zero, a `ValueError` is raised.
            - If none of the above are true, then the precision is calculated as `score / reference_count`.
        :return: a `float` indicating the recall metric of the current `ReducedConfusionMatrix` object.
        """
        if self.reference_count < 0:
            raise ValueError("The sum of all references is negative, which should not be possible.")
        elif self.reference_count == 0:
            recall: float = 0.0
        else:
            if self.score < 0:
                raise ValueError("The score is negative, which should not be possible.")
            else:
                recall: float = self.score / self.reference_count

        return recall

    def calculate_f_score(self, beta: float = 1) -> Optional[float]:
        """
        Calculates the F-score of the current `ReducedConfusionMatrix`.
        It accommodates for various cases as follows:
            - If either of `precision` or `recall` returns `None`, then this function also returns `None`.
            - If either of `precision` or `recall` is `0.0`, then this function also returns `0.0`.
            - If none of the above are true, then the precision is calculated as::

                f_score = ((1 + beta**2) * precision * recall) / ((beta**2 * precision) * recall)
        :param beta: an optional positive `float` weight given to precision and recall.
        The default value is `1`, which weights precision and recall equally.
        Values higher than `1` favor recall, whereas values lower than `1` favor precision.
        :return: a `float` indicating the F-score metric of the current `ReducedConfusionMatrix` object.
        """
        if beta <= 0:
            raise ValueError(f"The given value of beta, <{beta}> is not positive.")
        else:
            precision: Optional[float] = self.calculate_precision()
            recall: Optional[float] = self.calculate_recall()

            if precision is None or recall is None:
                f_score: Optional[float] = None
            elif precision == 0.0 and recall == 0.0:
                f_score: float = 0.0
            else:
                f_score_numerator: float = precision * recall
                f_score_denominator: float = (beta**2 * precision) + recall
                f_score: float = (1 + beta**2) * (f_score_numerator / f_score_denominator)

        return f_score

    def get_statistics(self, beta: float = 1) -> Sequence[Optional[float]]:
        """
        Collects and returns the `precision`, `recall`, and `f_score` for the current `ReducedConfusionMatrix` instance.
        :param beta: an optional positive `float` weight given to precision and recall.
        The default value is `1`, which weights precision and recall equally.
        Values higher than `1` favor recall, whereas values lower than `1` favor precision.
        :return: a `float` indicating the F-score metric of the current `ReducedConfusionMatrix` object.
        """
        precision: Optional[float] = self.calculate_precision()
        recall: Optional[float] = self.calculate_recall()
        f_score: Optional[float] = self.calculate_f_score(beta)
        return precision, recall, f_score

    def get_printable_statistics(self, output_format: str, beta: float = 1) -> str:
        """
        Collects and returns a string containing all available statistics from the `ReducedConfusionMatrix`,
        outputting them in a provided form.
        :param output_format: a `str` which corresponds to a desired format for the data.
        All values are given by their names as indicated throughout the class,
        so any custom format strings should use those names to insert those values into them.
        :param beta: an optional positive `float` weight given to precision and recall.
        The default value is `1`, which weights precision and recall equally.
        Values higher than `1` favor recall, whereas values lower than `1` favor precision.
        :return: a `float` indicating the F-score metric of the current `ReducedConfusionMatrix` object.
        """
        precision: Optional[float] = self.calculate_precision()
        recall: Optional[float] = self.calculate_recall()
        f_score: Optional[float] = self.calculate_f_score(beta)

        stats_display_kwargs: dict[str, Optional[float]] = {
            "score": self.score,
            "hypothesis_count": self.hypothesis_count,
            "reference_count": self.reference_count,
            "precision": precision,
            "recall": recall,
            "f_score": f_score,
            "beta": beta
        }

        stat_results: str = output_format.format(**stats_display_kwargs)
        return stat_results
