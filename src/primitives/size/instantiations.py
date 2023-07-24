from src.primitives.typing import BranchedWordSet, Parallelism
from src.primitives.size.base import SizeFunction
from src.primitives.conversion.instantiations import BranchedWordConverter


class ParallelismSizer(SizeFunction):
    """
    .. py:class:: ParallelismSizer
    A subclass of `SizeFunction` which considers each parallelism as having a size of `1` so long as it exists.
    Otherwise, its size is `0`.
    """
    @classmethod
    def size_parallelism(cls, parallelism: Parallelism, **kwargs) -> int:
        parallelism_size: int = 1 if parallelism is not None else 0
        return parallelism_size


class BranchSizer(SizeFunction):
    """
    .. py:class:: BranchSizer
    A subclass of `SizeFunction` which considers each parallelism as being as large as its number of branches.
    """
    @classmethod
    def size_parallelism(cls, parallelism: Parallelism, **kwargs) -> int:
        parallelism_size: int = len(parallelism)
        return parallelism_size


class WordSizer(SizeFunction):
    """
    .. py:class:: WordSizer
    A subclass of `SizeFunction` which considers each parallelism as being as large as its number of words;
    it assumes that the words can be represented as a set--that is, following the definition of a parallelism,
    no one word is counted twice.
    """
    @classmethod
    def size_parallelism(cls, parallelism: Parallelism, **kwargs) -> int:
        converted_parallelism: BranchedWordSet = BranchedWordConverter.convert_parallelism(parallelism)
        token_set: set[int] = set(token for branch in converted_parallelism for token in branch)
        parallelism_size: int = len(token_set)
        return parallelism_size
