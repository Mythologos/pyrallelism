from src.primitives.typing import BranchedWordSet, Parallelism
from src.primitives.conversion.base import BaseConverter


class BranchedWordConverter(BaseConverter):
    """
    .. py:class:: BranchedWordConverter
    Subclass of `BaseConverter` which converts a `Parallelism` to a `BranchedWordSet`.
    """
    @classmethod
    def convert_parallelism(cls, parallelism: Parallelism, **kwargs) -> BranchedWordSet:
        converted_parallelism: list[set[int]] = []
        for branch in parallelism:
            branch_start, branch_end = branch
            branched_word_representation: set[int] = set(range(branch_start, branch_end))
            converted_parallelism.append(branched_word_representation)

        return converted_parallelism
