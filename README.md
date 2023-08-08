# Pyrallelism

**Authors**: Stephen Bothwell and David Chiang (University of Notre Dame)

**Maintainer**: Stephen Bothwell

This library is purposed toward the task of **rhetorical parallelism detection** (RPD). 
It consists of a variety of extensible scoring utilities for the task.
The sections below describe in more detail the objective of this repository;
they also describe the contents of the codebase and provide avenues for extensions and contributions.

We release this codebase under a [**TODO**: license].

## Overview

...

We also have a set of unit tests. For these unit tests, 
we source data from the Wikipedia article on rhetorical parallelism.

## Codebase

### Interface

We provide an interface in `scorer.py` to interact with this library on a high level. 
Assuming that data has been massaged into the desired formats and a user wishes to employ preexisting metrics,
this interface presents a standard way to compute bipartite parallelism metrics between hypotheses and references.

The general interface is as follows:

```
>>> python scorer.py --help
usage: scorer.py [-h] [--beta BETA] [--loaders LOADERS [LOADERS ...]] [--metric METRIC] [--output-filepath OUTPUT_FILEPATH]
                 [--output-filetype OUTPUT_FILETYPE [OUTPUT_FILETYPE ...]] [--stratum-count STRATUM_COUNT]                 
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
  --output-filetype OUTPUT_FILETYPE [OUTPUT_FILETYPE ...]
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

### Primitives

...

## Contributing

...

## Citations

To cite this library, please refer to the following paper:

```
...
```

Our sample data for unit testing comes from the following resource:

```
@misc{wikipediacontributorsParallelismRhetoricWikipedia2023,
  title = {Parallelism (Rhetoric) \textemdash{} {{Wikipedia}}, the Free Encyclopedia},
  author = {{Wikipedia contributors}},
  year = {2023}
}
```
