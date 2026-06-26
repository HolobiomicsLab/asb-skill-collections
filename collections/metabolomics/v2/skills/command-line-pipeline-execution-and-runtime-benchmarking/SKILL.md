---
name: command-line-pipeline-execution-and-runtime-benchmarking
description: Use when when you have peak-abundance .csv files and assigned molecular
  formula data from FT-ICR MS preprocessing, and you need to verify that a published
  pipeline's runtime claims (e.g., '<1 min for 40 samples', '~2 min for 120 samples')
  hold true on your own datasets or reference datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetaboDirect
  - Python 3.8
  - R 4.0.2
  - NumPy
  - pandas
  - seaborn
  - matplotlib
  - vegan
  - SYNCSA
  - NumPy, pandas
  - vegan, SYNCSA
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis
  (e.g., chemodiversity analysis, multivariate statistics)
- The MetaboDirect pipeline was developed in Python 3.8
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2
- It requires the Python dependencies NumPy
- It requires the Python dependencies NumPy [40], pandas
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# command-line-pipeline-execution-and-runtime-benchmarking

## Summary

Execute a fully automated command-line pipeline on FT-ICR MS data and measure wall-clock runtime across sample-size conditions to validate that observed performance matches published benchmarks. This skill verifies reproducibility of computational efficiency claims by comparing empirical runtimes against reference thresholds.

## When to use

When you have peak-abundance .csv files and assigned molecular formula data from FT-ICR MS preprocessing, and you need to verify that a published pipeline's runtime claims (e.g., '<1 min for 40 samples', '~2 min for 120 samples') hold true on your own datasets or reference datasets. Use this skill when computational efficiency is a selection criterion or a reproducibility target.

## When NOT to use

- If raw FT-ICR MS spectra preprocessing is required; MetaboDirect does not provide raw spectra data preprocessing.
- If your datasets lack pre-assigned molecular formulas; the pipeline accepts only peak abundance and assigned molecular formula data.
- If you need to benchmark individual filter steps or sub-tasks in isolation; this skill measures end-to-end main pipeline runtime only.

## Inputs

- Peak-abundance .csv files (average ~1025 peaks per sample)
- Assigned molecular formula data (.csv format with elemental composition)
- MetaboDirect v0.3.4 or later (cloned from GitHub)
- Python 3.8+ and R 4.0+ environments

## Outputs

- Wall-clock runtime in seconds for pipeline execution
- Output .csv files (data matrices, transformed features, analysis results)
- Visualization files (Van Krevelen diagrams, elemental/molecular class composition plots)
- Runtime comparison report against reference benchmarks

## How to apply

Clone the pipeline repository and install Python dependencies (NumPy, pandas, seaborn, py4cytoscape, matplotlib) and R libraries (vegan, SYNCSA, tidyverse, RColorBrewer, etc.). Obtain or download peak-abundance .csv files with assigned molecular formulas from public repositories (e.g., OSF). Execute the main pipeline via command-line interface with default parameters, excluding optional steps (e.g., KEGG database queries or transformation network calculation) unless benchmarking the full pipeline. Record wall-clock runtime in seconds using system timing utilities (e.g., Unix `time` command). Verify that all expected output .csv files and visualization files are generated without errors. Compare observed runtime against reference benchmarks; for the bacterium-phage dataset (36 samples, ~495 assigned molecular formulas per sample), expect ~36 seconds for main pipeline steps.

## Related tools

- **MetaboDirect** (Command-line pipeline for automated analysis and visualization of FT-ICR MS data; executed to measure runtime performance) — https://github.com/Coayala/MetaboDirect
- **Python 3.8** (Runtime environment and dependency management for MetaboDirect execution)
- **R 4.0.2** (Statistical and visualization environment required by MetaboDirect R modules (vegan, SYNCSA, tidyverse))
- **NumPy, pandas** (Python dependencies for data manipulation and matrix operations in MetaboDirect pipeline)
- **vegan, SYNCSA** (R packages for chemodiversity analysis and multivariate statistics within MetaboDirect)

## Examples

```
time metabodirect -i peak_abundance.csv -f molecular_formulas.csv -o output_dir
```

## Evaluation signals

- Wall-clock runtime for bacterium-phage dataset (36 samples, ~495 assigned formulas per sample) is approximately 36 seconds (or <1 min as published).
- All expected output .csv files are generated without errors during pipeline execution.
- All visualization files (Van Krevelen diagrams, elemental composition plots) are successfully created.
- Observed runtime falls within or below published reference benchmarks for the same sample size and peak/formula count.
- No runtime warnings, missing file errors, or incomplete data matrix outputs are reported in standard output or logs.

## Limitations

- MetaboDirect does not provide raw spectra data preprocessing; input data must already be peak-detected and molecular formulas must be pre-assigned (typically via separate MS processing software).
- Benchmark times may vary depending on hardware specifications (CPU, RAM), which should be documented alongside runtime measurements.
- KEGG database queries and transformation network calculation are optional steps that significantly increase runtime; published benchmarks exclude these, so runtime cannot be fairly compared if they are included.
- Pipeline runtime is sensitive to the number of detected peaks and formula assignments per sample; datasets with very high peak counts may not match published benchmarks for smaller datasets.

## Evidence

- [other] Execute the main MetaboDirect pipeline using the command-line interface with default parameters for data pre-processing, data diagnostics, data exploration, and chemodiversity analysis, excluding KEGG database queries and transformation network calculation.: "Execute the main MetaboDirect pipeline using the command-line interface with default parameters for data pre-processing, data diagnostics, data exploration, and chemodiversity analysis, excluding"
- [other] Record wall-clock runtime (seconds) for the phage dataset execution and the S. fallax leachate dataset execution using system timing utilities.: "Record wall-clock runtime (seconds) for the phage dataset execution and the S. fallax leachate dataset execution using system timing utilities."
- [other] For the bacterium-phage dataset (36 samples with average 495 assigned molecular formulas per sample), the main MetaboDirect pipeline steps without KEGG mapping or transformation network calculation completed in less than 1 min (~36 s).: "For the bacterium-phage dataset (36 samples with average 495 assigned molecular formulas per sample), the main MetaboDirect pipeline steps without KEGG mapping or transformation network calculation"
- [results] 40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min to generate all the figures, plots, and outputs.: "40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min to generate all the figures, plots, and outputs"
- [methods] MetaboDirect does not provide raw spectra data preprocessing.: "MetaboDirect does not provide raw spectra data preprocessing"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules.: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules"
