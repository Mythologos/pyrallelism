from src.primitives.typing import BranchedWordSet, Parallelism
from src.primitives.conversion.base import BaseConverter


class BranchedWordConverter(BaseConverter):
    """
    .. py:class:: BranchedWordConverter
    Subclass of `BaseConverter` which converts a `Parallelism` to a `BranchedWordSet`.
    """
    @classmethod
    def convert_parallelism(cls, parallelism: Parallelism, **kwargs) -> BranchedWordSet:
        converted_parallelism: list[set[int]] = \
            [set(range(start, end)) for branch in parallelism for (start, end) in branch]
        return converted_parallelism
