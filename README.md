# Pyrallelism

**Authors**: Stephen Bothwell and David Chiang (University of Notre Dame)

**Maintainer**: Stephen Bothwell

This library is purposed toward the task of **rhetorical parallelism detection** (RPD). 
It consists of a variety of extensible scoring utilities for the task.
The sections below describe in more detail the contents of the codebase and provide avenues for extensions and contributions.
For details about bipartite parallelism metrics in general, please see our paper (cited below).

We release this codebase under an MIT license.

## Overview

This library consists of two major components.

First, it has an interface. If an end user wishes to use the library for evaluating results on rhetorical parallelism detection data
(or another task which can apply the same metrics), 
this library provides a standardized, easy-to-use, and customizable way to do just that.
It allows for data to be loaded from two predefined formats and four predefined metrics to be applied. Moreover,
it provides two output formats to store the computational results.

Second, it has an underlying extensible API. Mainly, this consists of a set of primitives 
for loading, converting, scoring, and sizing up data; for each of these actions, 
a base class exists which can be subclassed to fit nicely in pre-existing code. 
Enumerations and getters provide further ways to link new code easily to the aforementioned interface, 
allowing new metrics that follow the same principles to be integrated with relative ease.

This library also contains a small set of unit tests. For these unit tests, 
we source data from the Wikipedia article on rhetorical parallelism. 
We provide a citation for this data below.

## Codebase

### Interface

We provide an interface in `scorer.py` to interact with this library on a high level. 
Assuming that data has been massaged into the desired formats and a user wishes to employ preexisting metrics,
this interface presents a standard way to compute bipartite parallelism metrics between hypotheses and references.

The general interface is as follows (sans help messages):

```
>>> pyrallelism -h
usage: pyrallelism [-h] [--beta BETA] [--loaders LOADERS [LOADERS ...]] [--metric METRIC] [--output-filepath OUTPUT_FILEPATH] [--output-type OUTPUT_TYPE [OUTPUT_TYPE ...]]
                   [--stratum-count STRATUM_COUNT]
                   hypothesis_path reference_path

positional arguments:
  hypothesis_path
  reference_path

options:
  -h, --help            show this help message and exit
  --beta BETA
  --loaders LOADERS [LOADERS ...]
  --metric METRIC
  --output-filepath OUTPUT_FILEPATH
  --output-type OUTPUT_TYPE [OUTPUT_TYPE ...]
  --stratum-count STRATUM_COUNT
```

The interface requires a `hypothesis_path` and `reference_path` as inputs. 
These should either both be paths to individual files *or* paths to directories. 
If they are paths to directories, these directories should contain files of the same name which pair together.
Currently, there is no well-defined behavior for providing a mixture of a file and directory.

This interface also requests the following optional arguments:
- `--beta`: a positive `float` which defines the impact of precision and recall on the computed F1 scores.
- `--loaders`: a collection of either one or two strings referring to a manner of 
loading the `hypothesis_path` and `reference_path` data. If one string is given, it is used for both; 
if two strings are given, they should correspond to the hypothesis and then to the reference.
Possibilities available in the system currently are `tsv` and `xml`.
- `--metric`: the bipartite parallelism metric which the presented data will be evaluated on. Predefined options include:
  - `epm`: "exact parallelism match"
  - `mpbm`: "maximum parallel branch match"
  - `mbawo`: "maximum branch-aware word overlap"
  - `mwo`: "maximum word overlap"
  
  Each of these are described in more detail in our paper (see below for a citation).
- `--output-filepath`: a filepath (with no file extension) to a location which will be used to store the results of the performed evaluation. 
- `--output-filetype`: the type of file (and thus format) to be used to store the . Options include:
  - `csv`: a more data-oriented format allowing for easy loading and filtering of results.
  - `txt`: a more relaxed format allowing for easier viewing of results by humans.
- `--stratum-count`: a positive `int` referring to the number layers of parallelism to be considered. 
A value of 1 corresponds to a flat view of parallel structure, whereas a value greater than 1 incorporates nests.

### API

The API for this library consists of a few packages and subpackages. These include:
- `pyrallelism`
- `pyrallelism.primitives`
- `pyrallelism.primitives.assignment`
- `pyrallelism.primitives.conversion`
- `pyrallelism.primitives.loading`
- `pyrallelism.primitives.score`
- `pyrallelism.primitives.size`
- `pyrallelism.structures`
- `pyrallelism.utils`

Each of these will be described in turn below with regard to their contents. 
For more detailed documentation, see the class- and function-level documentation within the code.

#### Pyrallelism

The highest-level module of this library provides users access with its CLI (via the function `use_parallelism_cli`) 
and its standard bipartite parallelism metric calculation function (via the function `evaluate_bipartite_parallelism_metric`).

#### Primitives

Within the `primitives` subpackage, we define the `EvaluationMetric` class. This class composes two primitives--a scoring function 
and a size function--into one object. The `DefinedMetric` class then assigns a name for a metric, and the two are coordinated to select metrics for use. 
The `get_metric` getter function allows for the convenient access of predefined metrics by name.

The `typing` module defines a variety of types which are used throughout the code.
Namely, it provides an innate definition for a `Branch`, `Parallelism`, and `ParallelismDirectory`, 
all of which are used quite a few times.

Within this subpackage, a set of five further subpackages are defined. 
These packages provide functional and extensible base classes toward each subpackage's intention (if applicable),
and they include a set of predefined instantiations.

_Assignment_:

The `assignment` subpackage provides the `LinearSumAssigner` class. 
This class uses `scipy`'s implementation of the linear sum assignment algorithm 
to compute the maximal score (and entry locations for that score) for a given score matrix.

_Conversion_:

The `conversion` subpackage facilitates the alteration of a `Parallelism` to another form which may be more convenient 
for a certain scoring or size function (or both). 
Currently, the `BaseConverter` class has one instantiation in the `BranchedWordConverter`.
The `BranchedWordConverter` is used for the MBAWO and MWO metrics.

_Loading_:

The `loading` subpackage furnishes different procedures to load data for use with bipartite parallelism metrics. 
Currently, its base class, `BaseParallelismLoader`, has two instantiations.
The `TSVLoader` can load a TSV file into the desired format,
whereas the `XMLLoader` can load an XML file.
For examples of what these TSV and XML files should look like for use with this library,
see the Wikipedia-based examples in `test/data`.

_Score_:

The `score` subpackage supplies the first of the two critical elements of the `EvaluationMetric` class: 
the `ScoringFunction`. This class must be able to compare two parallelisms in some manner in order to determine how alike they are.
Current instantiations include one scoring function per metric: 
- The `ExactScorer` corresponds to the EPM metric.
- The `MaximumParallelBranchScorer` corresponds to the MPBM metric.
- The `MaximumBranchAwareWordOverlapScorer` corresponds to the MBAWO metric.
- The `MaximumWordOverlapScorer` corresponds to the MWO metric.

_Size_:

The `size` subpackage supplies the second of the two critical elements of the `EvaluationMetric` class: the `SizeFunction`.
This class must accept one parallelism and determine what its maximal score would be. 
Current instantations are threefold:
- The `ParallelismSizer` corresponds to the EPM metric.
- The `BranchSizer` corresponds to the MPBM metric.
- The `WordSizer` corresponds to the MBAWO and MWO metrics.

#### Structures

Within the `structures` subpackage, we give an implementation of a confusion matrix.
Strictly speaking, this `ReducedConfusionMatrix` class only fills three of the four slots 
traditionally considered for binary classification. 
Because the number of possible true negatives for rhetorical parallelism detection vastly exceeds 
the number of true positives, especially as the size of a document grows, bipartite parallelism metrics 
only compute precision, recall, and F-scores.

#### Utils

Within the `utils` subpackage, we lay out a template for output formats--in other words, 
a class which issues a few standard building blocks for displaying bipartite parallelism metric results. 
The `OutputFormat` class is purposed toward this end. 
Moreover, as with the `EvaluationMetric` class, 
we also use a `DefinedFormat` class to name and to allow for the easy access of each output format.
A getter function, `get_output_filetype`, coordinates these two classes with pre-existing interfaces.

## Contributing

This library is intended to provide a standard manner for using bipartite parallelism metrics; 
in some ways, it is intended to follow after libraries like [sacreBLEU](https://github.com/mjpost/sacrebleu) (Post 2018)
which had the same goal for the BLEU metric (Papineni *et al.* 2002) in machine translation tasks.
Thus, we hope to keep this library relatively static and stable to support future work and keep results consistent.

However, it is certainly possible that there are bugs, enhancements, or expansions on this work that merit addition. 
If you have a suggestion or code contribution that you would like to make, 
please open an issue or pull request to that end to start a discussion.

## Citations

To cite this library, please refer to the following paper:

```
@inproceedings{bothwellIntroducingRPD2023,
    author = {Bothwell, Stephen and DeBenedetto, Justin and Crnkovich, Theresa and M{\"u}ller, Hildegund and Chiang, David},
    title = "Introducing Rhetorical Parallelism Detection: {A} New Task with Datasets, Metrics, and Baselines",
    booktitle = "Proc. EMNLP",
    year = "2023",
    note = "To appear"
}
```

Our sample data for unit testing comes from the following resource:

```
@misc{wikipediacontributorsParallelismRhetoricWikipedia2023,
  title = {Parallelism (Rhetoric) \textemdash{} {{Wikipedia}}, the Free Encyclopedia},
  author = {{Wikipedia contributors}},
  year = {2023}
}
```

For other works referenced or cited here, see the following:
```
@inproceedings{postCallClarityReporting2018,
  title = {A Call for Clarity in Reporting {{BLEU}} Scores},
  booktitle = {Proceedings of the Third Conference on Machine Translation: {{Research}} Papers},
  author = {Post, Matt},
  year = {2018},
  month = oct,
  pages = {186--191},
  publisher = {{Association for Computational Linguistics}},
  address = {{Brussels, Belgium}},
  doi = {10.18653/v1/W18-6319},
  abstract = {The field of machine translation faces an under-recognized problem because of inconsistency in the reporting of scores from its dominant metric. Although people refer to ``the'' BLEU score, BLEU is in fact a parameterized metric whose values can vary wildly with changes to these parameters. These parameters are often not reported or are hard to find, and consequently, BLEU scores between papers cannot be directly compared. I quantify this variation, finding differences as high as 1.8 between commonly used configurations. The main culprit is different tokenization and normalization schemes applied to the reference. Pointing to the success of the parsing community, I suggest machine translation researchers settle upon the BLEU scheme used by the annual Conference on Machine Translation (WMT), which does not allow for user-supplied reference processing, and provide a new tool, SACREBLEU, to facilitate this.}
}

@inproceedings{papineniBleuMethodAutomatic2002,
  title = {Bleu: A Method for Automatic Evaluation of Machine Translation},
  booktitle = {Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics},
  author = {Papineni, Kishore and Roukos, Salim and Ward, Todd and Zhu, Wei-Jing},
  year = {2002},
  month = jul,
  pages = {311--318},
  publisher = {{Association for Computational Linguistics}},
  address = {{Philadelphia, Pennsylvania, USA}},
  doi = {10.3115/1073083.1073135}
}
```
