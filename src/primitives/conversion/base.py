from abc import abstractmethod
from typing import Collection

from src.primitives.typing import Parallelism


class BaseConverter:
    """
    .. py:class:: BaseConverter
    Base class for converting a `Parallelism` to another form for pertinent computation or examination.
    """
    @classmethod
    @abstractmethod
    def convert_parallelism(cls, parallelism: Parallelism, **kwargs) -> Collection:
        """
        Takes a parallelism and converts it to a form designated by a subclass.
        :param parallelism: a ``Parallelism`` in its standard form (as a set of branches).
        :param kwargs: a collection of keyword arguments meant to modify the conversion of parallelisms.
        :return: a ``Parallelism`` in its converted form (as some ``Collection`` of parallelism information).
        """
        raise NotImplementedError
