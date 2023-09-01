from typing import TypeAlias, Union

from numpy.typing import NDArray


Branch: TypeAlias = tuple[int, int]
Parallelism: TypeAlias = set[Branch]
ParallelismDirectory: TypeAlias = dict[int, Parallelism]

LSAComponents: TypeAlias = dict[str, Union[NDArray[int], list[tuple[int, int]]]]

BranchedWordSet: TypeAlias = list[set[int]]

TokenIdentifiers: TypeAlias = list[tuple[int, int]]
