# This file contains help messages for this package's CLI.

HYPOTHESIS_HELP: str = "A valid file or directory path to hypothesis data in a designated loading format."
REFERENCE_HELP: str = "A valid file or directory path to reference data in a designated loading format."
BETA_HELP: str = "The \u03B2 value used to weight precision and recall in the computed F1 score."
LOADERS_HELP: str = "A collection of one or two loaders used to load relevant data. " \
                    "If one is given, it is used for both the hypothesis and reference; " \
                    "if two are given, they are used for the hypothesis and reference in that order."
METRICS_HELP: str = "A predefined metric to compute over the given hypothesis and reference data."
OUTPUT_PATH_HELP: str = "A path to an output file used to store results of the metric's computations."
OUTPUT_TYPE_HELP: str = "The type (and format) of output file that will be used to store metric results."
STRATUM_COUNT_HELP: str = "The number of strata to which the given bipartite parallelism metrics should attend. " \
                        "If no value is supplied, the stratum count is inferred from the data."
