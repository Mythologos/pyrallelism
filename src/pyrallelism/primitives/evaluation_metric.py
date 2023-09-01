from enum import StrEnum
from typing import NamedTuple, Sequence, Type

from .score.base import ScoringFunction
from .score.instantiations import ExactScorer, MaximumParallelBranchScorer, \
    MaximumBranchAwareWordOverlapScorer, MaximumWordOverlapScorer
from .size.base import SizeFunction
from .size.instantiations import ParallelismSizer, BranchSizer, WordSizer


class EvaluationMetric(NamedTuple):
    """
    .. py:class:: EvaluationMetric
    Data-centric class for formally combining a `ScoringFunction` and `SizeFunction` into a metric,
    fitting into the family of bipartite parallelism metrics.
    """
    score: Type[ScoringFunction]
    size: Type[SizeFunction]


class DefinedMetric(StrEnum):
    """
    .. py:class:: DefinedMetric
    Enumeration class for the names and abbreviations of a set of predefined bipartite parallelism metrics.
    """
    EXACT_PARALLELISM_MATCH = "epm"
    MAXIMUM_PARALLELISM_BRANCH_MATCH = "mpbm"
    MAXIMUM_BRANCH_AWARE_WORD_OVERLAP = "mbawo"
    MAXIMUM_WORD_OVERLAP = "mwo"


DEFINED_METRICS: Sequence[str] = tuple([metric for metric in DefinedMetric])

EPM_METRIC: EvaluationMetric = EvaluationMetric(ExactScorer, ParallelismSizer)
MPBM_METRIC: EvaluationMetric = EvaluationMetric(MaximumParallelBranchScorer, BranchSizer)
MBAWO_METRIC: EvaluationMetric = EvaluationMetric(MaximumBranchAwareWordOverlapScorer, WordSizer)
MWO_METRIC: EvaluationMetric = EvaluationMetric(MaximumWordOverlapScorer, WordSizer)

METRIC_TABLE: dict[str, EvaluationMetric] = {
    DefinedMetric.EXACT_PARALLELISM_MATCH: EPM_METRIC,
    DefinedMetric.MAXIMUM_PARALLELISM_BRANCH_MATCH: MPBM_METRIC,
    DefinedMetric.MAXIMUM_BRANCH_AWARE_WORD_OVERLAP: MBAWO_METRIC,
    DefinedMetric.MAXIMUM_WORD_OVERLAP: MWO_METRIC
}


def get_metric(metric_name: str) -> EvaluationMetric:
    try:
        metric: EvaluationMetric = METRIC_TABLE[metric_name]
    except KeyError:
        raise ValueError(f"The metric <{metric_name}> is not recognized.")
    return metric
