# SciTask Card: Reproduce the runtime benchmark metrics for the MetaboDirect main pipeline across sample-size conditions

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:03:26.683093+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_metabodirect`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `benchmark-evaluation`, `data-processing`, `statistical-analysis`
- GitHub: `Coayala/MetaboDirect`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, placeholder, 4 grounding failures

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `microbiome-metabolomics`, `environmental-metabolomics`, `untargeted-metabolomics`
- Techniques: `direct-infusion-ms`, `high-resolution-ms`, `feature-detection`, `metabolite-identification`, `multivariate-statistics`, `molecular-networking`

## Research Question
Do the wall-clock runtimes of MetaboDirect's main pipeline on real FT-ICR MS datasets match the reported performance benchmarks of <1 min for 40 samples and ~2 min for 120 samples?

## Connected Finding
For the bacterium-phage dataset (36 samples with average 495 assigned molecular formulas per sample), the main MetaboDirect pipeline steps without KEGG mapping or transformation network calculation completed in less than 1 min (~36 s), and for the S. fallax dataset (4 samples with average 1793 assigned molecular formulas), the main pipeline completed in around 30 s.

## Task Description
Execute the MetaboDirect v0.3.4 pipeline (main steps only, excluding KEGG and transformation networks) on two FT-ICR MS datasets (phage-infected bacterium and S. fallax leachate) from the deposited OSF repository and measure wall-clock runtime for each dataset, then compare observed times against the reported benchmarks.

## Inputs
- Peak-abundance and molecular formula .csv files for bacterium-phage model system (36 samples) and S. fallax leachate incubation (4 samples) from OSF repository
- MetaboDirect v0.3.4 source code from GitHub repository and Zenodo deposit

## Expected Outputs
- Wall-clock runtime (in seconds) for phage dataset main pipeline execution
- Wall-clock runtime (in seconds) for S. fallax leachate dataset main pipeline execution
- CSV files containing filtered peaks, thermodynamic indices, normalized intensities, diagnostic tables, and diversity metrics for each dataset
- Comparison table or report documenting observed runtimes vs. reported benchmarks with percent deviation

## Expected Output File

- `runtime_benchmark_report.csv`

## Landmark Outputs

- `phage_filtered_peaks.csv`
- `phage_thermodynamic_indices.csv`
- `phage_normalized_intensities.csv`
- `phage_diversity_metrics.csv`
- `sfallax_filtered_peaks.csv`
- `sfallax_thermodynamic_indices.csv`

## Tools
- MetaboDirect
- Python 3.8
- R 4.0.2
- NumPy
- pandas
- seaborn
- matplotlib
- vegan
- SYNCSA

## Skills
- ft-icr-ms-data-preprocessing-and-quality-control
- peak-intensity-normalization-method-selection
- thermodynamic-molecular-index-calculation-from-elemental-composition
- metabolite-chemodiversity-index-calculation-and-interpretation
- multivariate-ordination-analysis-nmds-pca
- command-line-pipeline-execution-and-runtime-benchmarking

## Workflow Description
1. Clone MetaboDirect v0.3.4 from the GitHub repository (https://github.com/Coayala/MetaboDirect, Zenodo DOI 10.5281/zenodo.7278253) and install Python dependencies (NumPy, pandas, seaborn, py4cytoscape, matplotlib). 2. Download peak-abundance .csv files for the phage dataset (36 samples, ~1025 peaks average, ~495 assigned molecular formulas) and S. fallax leachate dataset (4 samples) from OSF (https://doi.org/10.17605/OSF.IO/XFHZ9). 3. Execute the main MetaboDirect pipeline using the command-line interface with default parameters for data pre-processing, data diagnostics, data exploration, and chemodiversity analysis, excluding KEGG database queries and transformation network calculation. 4. Record wall-clock runtime (seconds) for the phage dataset execution and the S. fallax leachate dataset execution using system timing utilities. 5. Compare observed runtimes against reference benchmarks: phage dataset expected <36 seconds, S. fallax expected as reported in paper; verify all output .csv and visualization files are generated without errors.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `metabodirect.pdf` | main_article | True |

## Missing Information
- Specific wall-clock runtime for S. fallax dataset (4 samples) main pipeline execution is not reported; only benchmarks for 40 and 120 samples are stated
- Exact number of peaks detected and peaks with assigned molecular formula for S. fallax dataset is not provided in the results section
- No documentation provided regarding system hardware specifications (CPU, RAM, OS) used for the reported runtime benchmarks, limiting reproducibility of timing comparisons across different computational environments
- Specific MetaboDirect command-line invocation parameters and configuration options used for the runtime benchmarks are not detailed in the methods or results

## Domain Knowledge
- FT-ICR MS generates monoisotopic peaks with high mass accuracy (±0.5 ppm error tolerance typical for formula assignment validation) suitable for direct injection analysis of complex organic matter without chromatographic separation.
- Peak intensity normalization method selection affects downstream statistical comparisons; SPANS scoring evaluates bias introduced by normalization choices and must be evaluated per-dataset based on grouping variables and data distribution characteristics.
- Chemodiversity metrics adapted from ecological indices (Shannon, Gini-Simpson, Chao1, Rao's quadratic entropy) require intensity sum-normalization of raw peak abundances prior to calculation to account for differences in total ion current across samples.
- MetaboDirect accepts only post-processed peak tables (molecular formula already assigned) and does not perform raw spectra deconvolution; raw FT-ICR MS .xml data must first be processed by tools such as Formularity, DataAnalysis, or Xcalibur.
- Wall-clock runtime benchmarking should measure end-to-end pipeline execution excluding external database queries (KEGG) and optional transformation network generation, as these are optional and computationally expensive steps.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Do the wall-clock runtimes of MetaboDirect's main pipeline on real FT-ICR MS datasets match the reported performance benchmarks of <1 min for 40 samples and ~2 min for 120 samples?: '40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min to generate all the figures, plots, and outputs'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] For the bacterium-phage dataset (36 samples with average 495 assigned molecular formulas per sample), the main MetaboDirect pipeline steps without KEGG mapping or transformation network calculation completed in less than 1 min (~36 s), and for the S. fallax dataset (4 samples with average 1793 assigned molecular formulas), the main pipeline completed in around 30 s.: 'The main steps of the MetaboDirect pipeline (without KEGG database mapping or calculating transformation networks) took less than 1 min (~36 s) for this data set. For this data set, the main steps of'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Peak-abundance and molecular formula .csv files for bacterium-phage model system (36 samples) and S. fallax leachate incubation (4 samples) from OSF repository: 'The first came from the exometabolome of a marine phage-host model system that uses a known, ecologically relevant marine bacterium (Pseudoalateromonas) and two contrastingly different infecting'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] MetaboDirect v0.3.4 source code from GitHub repository and Zenodo deposit: 'The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and is available to install through the Python Package Index'
- `ev_005` from `agent2_synthesis` (agent2_traced): [results] Wall-clock runtime (in seconds) for phage dataset main pipeline execution: '40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min'
- `ev_006` from `agent2_synthesis` (agent2_traced): [results] Wall-clock runtime (in seconds) for S. fallax leachate dataset main pipeline execution: 'The main steps of the MetaboDirect pipeline (without KEGG database mapping or calculating transformation networks) took less than 1 min (~36 s)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] CSV files containing filtered peaks, thermodynamic indices, normalized intensities, diagnostic tables, and diversity metrics for each dataset: 'This pre-processing step generates several .csv files containing the list of filtered peaks with their respective thermodynamic and molecular indices and the normalized and unnormalized intensities'
- `ev_008` from `agent2_synthesis` (agent2_traced): [results] Comparison table or report documenting observed runtimes vs. reported benchmarks with percent deviation: 'The main steps of the MetaboDirect pipeline (without KEGG database mapping or calculating transformation networks) took less than 1 min (~36 s)'
- `ev_009` from `agent2_synthesis` (agent2_traced): [abstract] MetaboDirect: 'develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Python 3.8: 'The MetaboDirect pipeline was developed in Python 3.8'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] R 4.0.2: 'The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] NumPy: 'It requires the Python dependencies NumPy'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] pandas: 'It requires the Python dependencies NumPy [40], pandas'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] seaborn: 'It requires the Python dependencies NumPy [40], pandas [41, 42], seaborn'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] matplotlib: 'It requires the Python dependencies NumPy [40], pandas [41, 42], seaborn [43], py4cytoscape, and matplotlib'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] vegan: 'diversity metrics using functions from the R packages vegan'
- `ev_017` from `agent2_synthesis` (agent2_traced): [methods] SYNCSA: 'diversity metrics using functions from the R packages vegan [63] and SYNCSA'
- `ev_018` from `agent2_synthesis` (agent2_traced): [results] Specific wall-clock runtime for S. fallax dataset (4 samples) main pipeline execution is not reported; only benchmarks for 40 and 120 samples are stated: '40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min'
- `ev_019` from `agent2_synthesis` (agent2_traced): [results] Exact number of peaks detected and peaks with assigned molecular formula for S. fallax dataset is not provided in the results section: 'The data set had an average of 1025 peaks detected across the whole data set (n = 36 samples) and an average of 495 peaks that got assigned a molecular formula'
- `ev_020` from `agent2_synthesis` (agent2_traced): [methods] No documentation provided regarding system hardware specifications (CPU, RAM, OS) used for the reported runtime benchmarks, limiting reproducibility of timing comparisons across different computational environments: '40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min to generate all the figures, plots, and outputs'
- `ev_021` from `agent2_synthesis` (agent2_traced): [results] Specific MetaboDirect command-line invocation parameters and configuration options used for the runtime benchmarks are not detailed in the methods or results: 'The main steps of the MetaboDirect pipeline (without KEGG database mapping or calculating transformation networks) took less than 1 min (~36 s)'

## Evaluation Strategy
### Direct Checks
- file_exists: verify that peak-abundance list files exist at OSF deposit https://doi.org/10.17605/OSF.IO/XFHZ9 for both bacterium-phage dataset and S. fallax dataset
- file_format_is: verify that retrieved peak-abundance files are in MetaboDirect-compatible format (CSV or TSV with columns for m/z, molecular formula, and sample abundances)
- script_runs: verify that MetaboDirect v0.3.4 (installed from https://github.com/Coayla/MetaboDirect or Zenodo DOI 10.5281/zenodo.7278253) executes the main pipeline (excluding KEGG and transformation networks) without error on bacterium-phage dataset
- script_runs: verify that MetaboDirect v0.3.4 executes the main pipeline (excluding KEGG and transformation networks) without error on S. fallax dataset
- value_in_range: wall-clock runtime for bacterium-phage dataset main pipeline (36 samples, ~495 peaks with formula) should be <1 min (reported as ~36 s in results), parameter-sensitive to system hardware and background processes
- value_in_range: wall-clock runtime for S. fallax dataset main pipeline (4 samples) should complete in measurable time; exact baseline from text reports 40 samples in <1 min and 120 samples in ~2 min, robust to interpolation
- output_matches_reference: verify that primary output artifacts (Van Krevelen diagrams, molecular class composition plots, NMDS/PCA ordinations, diversity metrics tables) are generated for both datasets as documented in article figures and supplementary figures
- contains_substring: verify that MetaboDirect execution log or output summary reports completion of steps: data pre-processing, data diagnostics, data exploration, chemodiversity analysis (no KEGG mapping, no transformation networks)
- file_exists: verify that output directory contains at least one quantitative diversity metric file (Chao1, Gini-Simpson, Shannon, or Rao's quadratic entropy values), matching structure shown in supplementary Fig. S6

### Expert Review
- Confirm that reported runtimes (~36 s for 36-sample bacterium-phage dataset, interpolated expectation for 4-sample S. fallax) are consistent with the stated pipeline efficiency claim ('40 samples in <1 min, 120 samples in ~2 min'); assess whether observed times align with documented computational complexity
- Verify that main pipeline output metrics (molecular diversity indices, ordination coordinates, compound class distributions) reproduce the trends reported in article results section (e.g., no significant phage or time effect in PERMANOVA; clustering by phosphorus content in NMDS)
- Assess whether peak-detection and molecular-formula-assignment statistics for the rerun datasets match or reasonably approximate the reported values (bacterium-phage: ~1025 peaks detected, ~495 with formula; S. fallax: specific counts per sample)
- Evaluate whether the absence of KEGG mapping and transformation networks in the executed pipeline is a valid and representative test of core MetaboDirect functionality, or whether exclusion of these modules substantially alters runtime claims

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Install MetaboDirect v0.3.4 with Python (NumPy, pandas, seaborn, matplotlib) and R (vegan, SYNCSA) dependencies from GitHub and Zenodo sources.
2. Retrieve phage-infected bacterium (36 samples, ~1025 peaks, ~495 assigned formulas) and S. fallax leachate (4 samples) peak-abundance CSV files from OSF deposit.
3. Execute MetaboDirect main pipeline (data pre-processing, diagnostics, exploration, chemodiversity analysis) excluding KEGG mapping and transformation networks via command-line interface.
4. Measure and record wall-clock runtime for phage dataset and S. fallax dataset using system timing tools; generate all intermediate CSV outputs (filtered peaks, thermodynamic indices, normalized intensities, diversity metrics).
5. Validation: Compare observed runtimes (phage expected <36 seconds; S. fallax per reported value) against benchmarks; verify all expected CSV and visualization output files exist and contain non-empty tables with correct column headers matching pipeline documentation.

## Workflow Ports

**Inputs:**

- `phage_peak_data` — Phage dataset peak-abundance and molecular formula CSV files (36 samples) ← `task_001/feature_comparison_table`
- `sfallax_peak_data` — S. fallax leachate peak-abundance and molecular formula CSV files (4 samples)
- `metabodirect_source` — MetaboDirect v0.3.4 source code repository

**Outputs:**

- `phage_runtime` — Phage dataset main pipeline wall-clock runtime (seconds)
- `sfallax_runtime` — S. fallax leachate dataset main pipeline wall-clock runtime (seconds)
- `phage_outputs` — Phage dataset processed CSV files (filtered peaks, thermodynamic indices, diversity metrics)
- `sfallax_outputs` — S. fallax dataset processed CSV files (filtered peaks, thermodynamic indices, diversity metrics)
- `runtime_comparison` — Benchmark comparison report with observed vs. reference runtimes and deviations

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (4):
  - missing_information[2]: evidence_span not found in section 'methods' (value='No documentation provided regarding system hardware specific', span='40 samples were processed in less than 1 min whereas 120 sam')
  - research_question vs. finding semantic mismatch: RQ asks about 40-sample and 120-sample benchmarks; finding reports 36-sample (~36s) and 4-sample (~30s) data, which do not directly validate the stated benchmarks
  - expected_outputs[1]: evidence_span for 'S. fallax leachate dataset main pipeline execution' uses phage-dataset text (~36s for 36 samples), not S. fallax-specific runtime
  - expected_outputs[3]: evidence_span for 'Comparison table or report' cites only phage runtime text, not a comparison document
- Notes: This card exhibits significant coherence problems. The research_question asks whether observed runtimes match '40-sample <1 min' and '120-sample ~2 min' benchmarks, but the finding reports runtimes for 36-sample (36s) and 4-sample (30s) datasets—which are different datasets and sample counts than the benchmark reference. The research question is not directly answered by the finding; instead, the finding reports actual measurements on different-sized datasets. The expected_outputs section contains evidence_span mismatches (e.g., expected_outputs[1] and [3] both cite the phage/40-120 text rather than S. fallax-specific evidence). Additionally, the S. fallax finding (~30s) is stated but not grounded in any quoted evidence_span from the source text. The task would benefit from: (1) clarifying whether the RQ targets the stated benchmarks (40/120 samples) or the actual datasets (36/4 samples), (2) providing explicit side-by-side comparison statements in the finding, (3) grounding each finding claim with its specific evidence_span, and (4) documenting hardware/OS specifications as a task input to support reproducibility. Currently scored 2/5 due to RQ-finding mismatch and placeholder/generic language in expected outputs.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
