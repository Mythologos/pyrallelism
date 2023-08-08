from abc import abstractmethod

from pyrallelism.primitives.typing import Parallelism, ParallelismDirectory


class SizeFunction:
    """
    .. py:class:: SizeFunction
    Base class for determining the size of `Parallelism` (or converted parallelism) objects.
    """
    @classmethod
    def compute_directory_size(cls, directory: ParallelismDirectory, **kwargs) -> int:
        """
        Collects the size of all individual parallelisms in a `ParallelismDirectory` and sums them.
        :param directory: a collection of parallelisms (`ParallelismDirectory`) whose sizes are to be determined.
        :param kwargs: a collection of keyword arguments meant to modify the size calculations for parallelisms.
        :return: a nonnegative `int` representing the overall size of all objects in *directory*.
        """
        parallelism_sizes: list[int] = \
            [cls.size_parallelism(parallelism, **kwargs) for parallelism in directory.values()]
        directory_size: int = sum(parallelism_sizes)
        return directory_size

    @classmethod
    @abstractmethod
    def size_parallelism(cls, parallelism: Parallelism, **kwargs) -> int:
        """
        Determines the size of a single parallelism by some method.
        :param parallelism: an individual `Parallelism` object whose size is to be calculated.
        :param kwargs: a collection of keyword arguments meant to modify the size calculations for
        an individual parallelism.
        :return: a nonnegative `int` representing the size of *parallelism* in terms of some predetermined criteria.
        """
        raise NotImplementedError
