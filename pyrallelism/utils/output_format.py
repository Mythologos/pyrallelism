from enum import StrEnum
from typing import NamedTuple


class OutputFormat(NamedTuple):
    """
    .. py:class:: OutputFormat
    Data-centric class for holding three general categories for filling out information pertaining to
    scoring with a bipartite parallelism metric.
    """
    filetype: str
    title: str
    header: str
    line: str


class DefinedFormat(StrEnum):
    """
    .. py:class:: DefinedFormat
    Enumeration class for the names and abbreviations of text formats predefined by the provided interface.
    """
    TEXT: str = "txt"
    CSV: str = "csv"


CSV_FORMAT: OutputFormat = OutputFormat(
    filetype=DefinedFormat.CSV,
    title="hypothesis_filename,reference_filename,score,hypothesis_count,reference_count,precision,recall,f_score\n",
    header="{hypothesis_filename},{reference_filename},",
    line="{score},{hypothesis_count},{reference_count},{precision},{recall},{f_score}\n"
)

TEXT_FORMAT: OutputFormat = OutputFormat(
    filetype=DefinedFormat.TEXT,
    title="Directory Results:\n",
    header="File <{hypothesis_filename}> (Hypothesis) vs. <{reference_filename}> (Reference):\n",
    line="\t* Precision: {precision} ({score} / {hypothesis_count})"
         "\n\t* Recall: {recall} ({score} / {reference_count})"
         "\n\t* F-{beta}: {f_score}"
         "\n\n"
)

FORMAT_TABLE: dict[str, OutputFormat] = {DefinedFormat.CSV: CSV_FORMAT, DefinedFormat.TEXT: TEXT_FORMAT}


def get_output_filetype(format_name: str) -> OutputFormat:
    try:
        selected_format: OutputFormat = FORMAT_TABLE[format_name]
    except KeyError:
        raise ValueError(f"The format <{format_name}> is not recognized.")
    return selected_format
