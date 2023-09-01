from enum import StrEnum
from typing import Type

from .base import BaseParallelismLoader
from .instantiations import TSVLoader, XMLLoader


class DefinedLoader(StrEnum):
    """
    .. py:class:: DefinedLoader
    Enumeration class for the names and abbreviations of predefined file loaders.
    """
    TSV: str = "tsv"
    XML: str = "xml"


LOADER_TABLE: dict[str, Type[BaseParallelismLoader]] = {
    DefinedLoader.TSV: TSVLoader,
    DefinedLoader.XML: XMLLoader
}


def get_loader(loader_name: str) -> Type[BaseParallelismLoader]:
    try:
        loader: Type[BaseParallelismLoader] = LOADER_TABLE[loader_name]
    except KeyError:
        raise ValueError(f"The loader <{loader_name}> is not recognized.")
    return loader
