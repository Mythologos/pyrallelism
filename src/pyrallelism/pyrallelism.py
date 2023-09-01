from argparse import ArgumentParser, Namespace
from os import path
from sys import argv
from typing import Any, Sequence

from .evaluator import evaluate_bipartite_parallelism_metric
from .primitives.evaluation_metric import DefinedMetric, get_metric
from .primitives.loading import TSVLoader, XMLLoader
from .primitives.loading.interface import get_loader
from .primitives.typing import ParallelismDirectory
from .structures.confusion_matrix import ReducedConfusionMatrix
from .utils.command_line_helpers import collect_directories
from .utils.output_format import get_output_type, CSV_FORMAT
from .utils.help_messages import *


def _use_pyrallelism_cli():
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("hypothesis_path", type=str, help=HYPOTHESIS_HELP)
    parser.add_argument("reference_path", type=str, help=REFERENCE_HELP)
    parser.add_argument("--beta", type=float, default=1.0, help=BETA_HELP)
    parser.add_argument("--loaders", type=get_loader, nargs="+", default=(TSVLoader, XMLLoader), help=LOADERS_HELP)
    parser.add_argument("--metric", type=get_metric, default=DefinedMetric.EXACT_PARALLELISM_MATCH, help=METRICS_HELP)
    parser.add_argument("--output-filepath", type=str, default="results", help=OUTPUT_PATH_HELP)
    parser.add_argument("--output-type", type=get_output_type, nargs="+", default=(CSV_FORMAT,), help=OUTPUT_TYPE_HELP)
    parser.add_argument("--stratum-count", type=int, default=None, help=STRATUM_COUNT_HELP)
    args: Namespace = parser.parse_args(argv[1:])

    if path.exists(args.hypothesis_path) is False:
        raise ValueError(f"The filepath <{args.hypothesis_path}> is not a valid filepath.")
    elif path.exists(args.reference_path) is False:
        raise ValueError(f"The filepath <{args.reference_path}> is not a valid filepath.")

    if len(args.loaders) > 2:
        raise ValueError("Too many loaders selected. Must be either one or two loaders.")
    else:
        if len(args.loaders) == 1:
            args.loaders.append(args.loaders[-1])
        hypothesis_loader, reference_loader = args.loaders

    loader_kwargs: dict[str, Any] = {"stratum_count": args.stratum_count}

    if path.isfile(args.hypothesis_path) and path.isfile(args.reference_path):
        hypothesis_dirs: Sequence[ParallelismDirectory] = \
            (hypothesis_loader.load_parallelism_directory(args.hypothesis_path, **loader_kwargs),)
        reference_dirs: Sequence[ParallelismDirectory] = \
            (reference_loader.load_parallelism_directory(args.reference_path, **loader_kwargs),)
        hypothesis_filename: str = args.hypothesis_path.split("/")[-1]
        reference_filename: str = args.reference_path.split("/")[-1]
        paired_filenames: Sequence[dict[str, str]] = (
            {"hypothesis_filename": hypothesis_filename, "reference_filename": reference_filename},
        )
    elif path.isdir(args.hypothesis_path) and path.isdir(args.reference_path):
        hypothesis_filenames, hypothesis_dirs = \
            collect_directories(args.hypothesis_path, hypothesis_loader, **loader_kwargs)
        reference_filenames, reference_dirs = \
            collect_directories(args.reference_path, reference_loader, **loader_kwargs)
        paired_filenames: Sequence[dict[str, str]] = tuple([
            {"hypothesis_filename": hypothesis_filenames[i], "reference_filename": reference_filenames[i]}
            for i in range(0, min(len(hypothesis_filenames), len(reference_filenames)))
        ])
    else:
        raise NotImplementedError("Behavior for a mixture of filepaths and directories is currently undefined.")

    confusion_matrices: list[ReducedConfusionMatrix] = []
    if len(hypothesis_dirs) != len(reference_dirs):
        raise NotImplementedError("An unequal number of hypotheses and references were collected. "
                                  "File matching behavior is currently not implemented under such conditions.")
    else:
        directory_pairs: list[tuple[ParallelismDirectory, ParallelismDirectory]] = zip(hypothesis_dirs, reference_dirs)
        for (hypotheses, references) in directory_pairs:
            confusion_matrix, _ = evaluate_bipartite_parallelism_metric(hypotheses, references, args.metric)
            confusion_matrices.append(confusion_matrix)

    for filetype in args.output_type:
        with open(f"{args.output_filepath}.{filetype.filetype}", encoding="utf-8", mode="w+") as output_file:
            output_file.write(filetype.title)
            for pair_index, matrix in enumerate(confusion_matrices):
                output_file.write(filetype.header.format(**paired_filenames[pair_index]))
                base_line_string: str = matrix.get_printable_statistics(filetype.line, beta=args.beta)
                output_file.write(base_line_string)
