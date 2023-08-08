from abc import abstractmethod

from pyrallelism.primitives.typing import Branch, ParallelismDirectory, TokenIdentifiers


class BaseParallelismLoader:
    """
    .. py:class:: BaseParallelismLoader
    Base class for loading a `ParallelismDirectory` from a given file format.
    """
    @classmethod
    def load_parallelism_directory(cls, filepath: str, **kwargs) -> ParallelismDirectory:
        """
        Loads a file into a `ParallelismDirectory` by whatever means is appropriate;
        the nature of the loading procedure is specified by the focus of a given subclass.
        :param filepath: the path to a file from which a ParallelismDirectory will be generated.
        The type of the file should correspond to the loader subclass used.
        :param kwargs: a collection of keyword arguments meant to modify the creation of a `ParallelismDirectory`.
        One such example is a pre-specified *stratum_count*, or number of strata to consider during evaluation.
        :return: a `ParallelismDirectory` derived from the provided file.
        """
        parallelism_directory: ParallelismDirectory = {}
        stratum_rows: list[list[tuple[int, int]]] = cls._read_file(filepath, **kwargs)
        for stratum_row in stratum_rows:
            cls._handle_stratum(parallelism_directory, stratum_row)

        return parallelism_directory

    @staticmethod
    @abstractmethod
    def _read_file(filepath: str, **kwargs) -> list[TokenIdentifiers]:
        raise NotImplementedError

    @staticmethod
    def _handle_stratum(directory: ParallelismDirectory, stratum_row: list[tuple[int, int]]):
        """
        Iterates over an individual stratum to derive branches from a given TSV file.
        Adds branches from an individual stratum to the `ParallelismDirectory` being developed.
        :param directory: the `ParallelismDirectory` to be filled with branches from the given stratum.
        :param stratum_row: a `list` containing nonnegative `parallelism_id` and `branch_id` values.
        """
        token_index: int = 0
        while token_index < len(stratum_row):
            parallelism_id, branch_id = stratum_row[token_index]
            if parallelism_id != -1:
                branch_start: int = token_index
                for subsequent_token_index in range(token_index + 1, len(stratum_row)):
                    subsequent_parallelism_id, subsequent_branch_id = stratum_row[subsequent_token_index]
                    if subsequent_parallelism_id != parallelism_id or subsequent_branch_id != branch_id:
                        branch_end: int = subsequent_token_index
                        break
                else:
                    branch_end = len(stratum_row)

                new_branch: Branch = (branch_start, branch_end)
                if parallelism_id not in directory:
                    directory[parallelism_id] = set()
                directory[parallelism_id].add(new_branch)

                token_index = branch_end
            else:
                token_index += 1
