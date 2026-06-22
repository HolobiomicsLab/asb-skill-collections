---
name: computational-performance-benchmarking-and-timing-measurement
description: Use when when you need to validate that a newly published bioinformatics pipeline meets stated performance claims, or when you must characterize how execution time scales with dataset size (sample count, peak count, or formula complexity) and optional analysis features (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetaboDirect
  - Python
  - R
  - NumPy
  - pandas
  - seaborn
  - matplotlib
  - Formularity
  - KEGGREST
  - vegan
  - SYNCSA
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- Molecular transformation networks for each sample (mass difference network-based approach) are generated in this step
- The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1)
- The MetaboDirect pipeline was developed in Python 3.8 [38]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- requires the Python dependencies NumPy [40], pandas [41, 42]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and is available to install through the Python Package Index... It requires the Python dependencies NumPy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# computational-performance-benchmarking-and-timing-measurement

## Summary

Systematically measure and document wall-clock execution times for a bioinformatics pipeline across datasets of varying sizes and analysis configurations to establish performance baselines and characterize scalability. This skill is essential for validating computational efficiency claims and enabling users to estimate runtime requirements for their own datasets.

## When to use

When you need to validate that a newly published bioinformatics pipeline meets stated performance claims, or when you must characterize how execution time scales with dataset size (sample count, peak count, or formula complexity) and optional analysis features (e.g., KEGG annotation, transformation network generation). Apply this skill when benchmark results are published in a paper but reproducibility is uncertain, or when you must predict runtime for datasets of intermediate sizes not reported in the original article.

## When NOT to use

- Input data is already in a non-standard or proprietary format incompatible with the declared input specification (Formularity .csv); preprocessing is required first.
- The compute environment (OS, library versions, CPU architecture) differs substantially from the paper's specification, or you cannot enforce a controlled environment; timings may not be reproducible.
- Your goal is to optimize the pipeline's internal algorithm rather than validate its published performance; profiling and code-level analysis are required instead.

## Inputs

- Formularity .csv file with assigned molecular formulas, peak intensities, and m/z values (40, 120, or arbitrary sample counts)
- Real FT-ICR MS datasets in Formularity .csv format (bacterium-phage: 36 samples × 495 avg peaks; S. fallax: 4 samples × 1793 avg formulas)
- MetaboDirect software v0.3.4 and all declared dependencies (Python ≥3.5, R ≥4, Cytoscape ≥3.8, NumPy, pandas, seaborn, py4cytoscape, KEGGREST)
- System environment specification (OS, CPU, RAM)

## Outputs

- Wall-clock elapsed time in minutes for each dataset–pipeline-configuration pair
- Summary benchmark table with columns: dataset name, sample count, pipeline configuration (main only / with KEGG / full with transformation networks), elapsed time (minutes)
- Scalability characterization showing how execution time varies with sample count and configuration complexity

## How to apply

Install the target software (here: MetaboDirect v0.3.4 via pip with all declared dependencies) on a consistent compute environment, ensuring OS and library versions match the paper's specification. Obtain or generate test datasets with systematically varied parameters: for this skill, mock datasets were created by random subsampling to target sample counts (40 and 120), and real datasets from published experiments (bacterium-phage: 36 samples with 495 avg peaks; S. fallax: 4 samples with 1793 avg formulas) were obtained in the declared input format (Formularity .csv with assigned molecular formulas, peak intensities, m/z values). Execute the pipeline in isolation for each dataset–configuration pair (e.g., main pipeline only vs. with KEGG querying via KEGGREST vs. full analysis including transformation networks), recording elapsed wall-clock time using system timing tools (e.g., Unix `time` command or Python timeit). Compile results into a summary table with columns for dataset name, sample count, configuration scope, and elapsed time in minutes. Verify that reported times are consistent with the published benchmark table and that timing patterns (e.g., sub-linear scaling with sample count, exponential growth with optional features) align with the paper's claims about efficiency.

## Related tools

- **MetaboDirect** (The target pipeline whose computational performance is being benchmarked across dataset sizes and analysis configurations.) — https://github.com/Coayala/MetaboDirect
- **KEGGREST** (Optional R library used by MetaboDirect for KEGG database querying; execution time with this feature enabled is measured separately.)
- **vegan** (R package used by MetaboDirect for calculating diversity metrics during chemodiversity analysis step.)
- **SYNCSA** (R package used by MetaboDirect for diversity metric calculations.)

## Examples

```
metabodirect --input bacterium_phage_dataset.csv --config full_analysis --output benchmark_results.txt 2>&1 | grep -E '(Elapsed|Total time)'
```

## Evaluation signals

- Reported wall-clock times for the 40-sample and 120-sample mock datasets fall within the paper's stated ranges (<1 minute and ~2 minutes for main pipeline), confirming reproducibility of the base case.
- Timing for the bacterium-phage dataset (36 samples, 495 avg peaks) matches published benchmarks: ~36 seconds (main), ~10 minutes (with KEGG), ~21 minutes (full analysis) — confirming correct configuration and environment.
- Timing for the S. fallax leachate dataset (4 samples, 1793 avg formulas) matches published benchmarks: ~30 seconds (main) and ~32 minutes (full analysis), accounting for peak complexity differences.
- Execution time scaling follows expected patterns: main pipeline time grows approximately linearly with sample count; time with KEGG and transformation networks exhibits larger, non-linear increases due to database queries and network construction.
- Summary benchmark table structure and column labels match those in the paper's results section, and all timing measurements are positive, finite, and consistent across multiple runs (if re-executed).

## Limitations

- Benchmark times are system-dependent: absolute values will vary with CPU speed, RAM availability, I/O subsystem, and background process load; relative scaling patterns are more reproducible than absolute times.
- The paper provides only two publicly available datasets (bacterium-phage and S. fallax); mock datasets created by random subsampling may not capture performance variation from peak complexity, formula diversity, or data sparsity patterns in other real datasets.
- Optional KEGG querying adds network latency and database response time, which is not captured in offline profiling; published times assume active internet connectivity and KEGG server availability.
- Transformation network analysis time grows combinatorially with the number of detected masses; scaling behavior may differ substantially for datasets with very high or very low peak counts relative to those benchmarked in the paper.

## Evidence

- [other] MetaboDirect processed 40 samples in <1 minute and 120 samples in 2 minutes for main pipeline steps: "MetaboDirect processed 40 samples in <1 minute and 120 samples in 2 minutes for main pipeline steps"
- [other] bacterium-phage dataset (36 samples, 495 avg peaks) completed in ~36 seconds (main), 10 minutes (with KEGG), and 21 minutes (full analysis): "bacterium-phage dataset (36 samples, 495 avg peaks) completed in ~36 seconds (main), 10 minutes (with KEGG), and 21 minutes (full analysis)"
- [other] Run the main MetaboDirect pipeline on each of the 40-sample and 120-sample mock datasets using a single command, recording elapsed wall-clock time.: "Run the main MetaboDirect pipeline on each of the 40-sample and 120-sample mock datasets using a single command, recording elapsed wall-clock time."
- [other] Obtain or generate mock datasets with 40 and 120 samples by random subsampling from unpublished data, and obtain real FT-ICR MS datasets from the bacterium-phage system (Pseudoalateromonas with phages HP1 and HS2) and S. fallax leachate experiment, each in Formularity .csv format (assigned molecular formulas, peak intensities, m/z values).: "Obtain or generate mock datasets with 40 and 120 samples by random subsampling from unpublished data, and obtain real FT-ICR MS datasets from the bacterium-phage system (Pseudoalateromonas with"
- [other] Install MetaboDirect (v0.3.4) via Python Package Index with dependencies NumPy, pandas, seaborn, py4cytoscape, and matplotlib, ensuring compatibility on the target OS (Windows, Linux, or MacOS).: "Install MetaboDirect (v0.3.4) via Python Package Index with dependencies NumPy, pandas, seaborn, py4cytoscape, and matplotlib, ensuring compatibility on the target OS (Windows, Linux, or MacOS)."
- [readme] MetaboDirect can be installed directly from PyPi using: pip install metabodirect: "MetaboDirect can be installed directly from PyPi using: pip install metabodirect"
- [other] Compile all recorded compute times into a summary table with columns for dataset name, sample count / configuration, pipeline step scope, and elapsed time in minutes, and verify that reported times are consistent with the paper's benchmark table.: "Compile all recorded compute times into a summary table with columns for dataset name, sample count / configuration, pipeline step scope, and elapsed time in minutes, and verify that reported times"
