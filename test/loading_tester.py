from typing import Sequence, Type
from unittest import TestCase

from pyrallelism.primitives.loading.base import BaseParallelismLoader
from pyrallelism.primitives.loading.instantiations import TSVLoader, XMLLoader
from pyrallelism.primitives.typing import ParallelismDirectory, Parallelism


class LoadingTester(TestCase):
    """
    .. py:class:: LoadingTester
    Class to test the pre-made data-loading functions of this module.
    Checks to see whether both are able to load the gold parallelism directory exactly.
    """
    def setUp(self):
        self.filepath_base: str = "data"
        self.loaders: list[tuple[Type[BaseParallelismLoader], str]] = [
            (TSVLoader, f"{self.filepath_base}/wikipedia_perfect_hyp.tsv"),
            (XMLLoader, f"{self.filepath_base}/wikipedia_gt.xml")
        ]

        self.stratum_count: int = 2
        self.loading_kwargs: dict[str, int] = {"stratum_count": self.stratum_count}

        self.parallelism_count = 4
        self.gold_parallelisms: Sequence[Parallelism] = (
            {(51, 55), (56, 60), (62, 66)},
            {(104, 107), (108, 115), (116, 121)},
            {(152, 161), (162, 168), (169, 176), (176, 184)},
            {(230, 243), (245, 257)}
        )

    def test_loaders(self):
        for loader_class, loader_filepath in self.loaders:
            loaded_directory: ParallelismDirectory = \
                loader_class.load_parallelism_directory(loader_filepath, **self.loading_kwargs)

            self.assertEqual(len(loaded_directory), len(self.gold_parallelisms))
            for parallelism_id, parallelism in loaded_directory.items():
                self.assertSetEqual(self.gold_parallelisms[int(parallelism_id) - 1], parallelism)
