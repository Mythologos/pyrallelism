from os import listdir
from typing import Sequence, Type

from natsort import natsorted

from ..primitives.loading import BaseParallelismLoader
from ..primitives.typing import ParallelismDirectory


def collect_directories(directory_filepath: str, loader: Type[BaseParallelismLoader], **kwargs) -> \
        tuple[list[str], Sequence[ParallelismDirectory]]:
    sorted_filenames: list[str] = natsorted(listdir(directory_filepath))
    parallelism_directories: list[ParallelismDirectory] = []
    for filename in sorted_filenames:
        current_filepath: str = f"{directory_filepath}/{filename}"
        new_directory: ParallelismDirectory = loader.load_parallelism_directory(current_filepath, **kwargs)
        parallelism_directories.append(new_directory)
    parallelism_directories: Sequence[ParallelismDirectory] = tuple(parallelism_directories)
    return sorted_filenames, parallelism_directories

