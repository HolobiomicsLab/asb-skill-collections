# SciTask Card: Analyze scalability of asari by running it on increasing sample counts up to >100 mzML files and recording runtime and memory

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:33:42.864961+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_asari/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `benchmark-evaluation`
- DOI: `10.1038/s41467-023-39889-1`
- GitHub: `shuzhao-li-lab/asari_pcpfm_tutorials`

## Classification

- Task kind: `analysis`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `lc-ms`, `feature-detection`, `chromatogram-alignment`, `quality-control`, `database-annotation`
- Keywords: `high-resolution metabolomics` · `lc-ms` · `gc-ms` · `peak detection` · `mass alignment` · `extracted ion chromatogram` · `untargeted metabolomics` · `composite map processing` · `peak quality tracking`

## Research Question
How does asari's computational performance (wall-clock time and peak memory usage) scale with increasing numbers of LC-MS samples?

## Connected Finding
Asari is designed as a scalable program with performance-conscious implementation prioritizing disciplined use of memory and CPU resources.

## Task Description
Benchmark asari's computational performance and memory footprint on public metabolomics datasets across sample-set sizes (10, 50, 100+ samples) to validate the scalability claim of >1000 samples on a laptop computer.

## Inputs
- Public mzML files (minimum 100+ files) from MetaboLights or MassIVE repositories in centroided format
- asari software installed from PyPI or cloned from source (v1.10+)
- System profiling tools capable of capturing wall-clock runtime and peak memory usage

## Expected Outputs
- Scalability benchmark table (CSV or TSV) with columns: sample_count, wall_clock_time_seconds, peak_memory_mb, run_number, mean_time, std_dev_time, mean_memory, std_dev_memory
- Wall-clock time vs. sample count plot (PNG or PDF) showing linear or near-linear scaling up to 100+ samples
- Peak memory usage vs. sample count plot (PNG or PDF) demonstrating memory efficiency across cohort sizes
- Summary report (text or markdown) stating mean throughput (samples/hour) per cohort and extrapolated time estimate for 1000-sample project

## Expected Output File

- `scalability_benchmark_results.csv`

## Landmark Outputs

- `asari_process_run_10_samples.log`
- `asari_process_run_50_samples.log`
- `asari_process_run_100_samples.log`
- `benchmark_raw_metrics.csv`
- `time_vs_sample_count.png`
- `memory_vs_sample_count.png`

## Tools
- asari
- Python
- pymzml

## Skills
- lc-ms-dataset-acquisition-and-curation
- computational-resource-profiling-and-benchmarking
- software-performance-characterization-and-scaling-analysis
- time-and-memory-complexity-visualization
- scalability-extrapolation-and-throughput-estimation

## Workflow Description
1. Retrieve public mzML datasets from MetaboLights or MassIVE repositories; select or subsample test data to create cohorts of 10, 50, and 100+ samples. 2. Install asari from pip (v1.10+) with default parameters (5 ppm m/z tolerance, positive ionization mode). 3. For each cohort, execute asari process command and record wall-clock runtime and peak resident memory usage using system profiling tools (e.g., time command, psutil, or top). 4. Repeat runs 2–3 times per cohort to establish mean and standard deviation of timing and memory metrics. 5. Tabulate results by sample count and plot wall-clock time and memory versus sample number to verify linear or near-linear scaling. 6. Compare observed throughput (samples/hour) and memory per sample to the claimed benchmark threshold for laptop-class hardware (≤16 GB RAM, single CPU core).

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/conda_asari_screenshot.png` | figure | False |
| `figures/viz_screen_shot20220518.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog documenting version history, performance improvements, or scalability-related fixes

## Domain Knowledge
- asari processes mzML files by extracting mass tracks per sample, building a composite mass grid, and detecting elution peaks; memory efficiency derives from not retaining full intensity arrays in memory during intermediate steps.
- Laptop-class hardware is defined as single-core CPU and ≤16 GB RAM; the scalability claim of >1000 samples must be testable on such machines without parallel computing.
- Wall-clock time includes all stages: mzML parsing, mass track extraction (parallelized over samples), m/z alignment, RT calibration, and peak detection on composite mass tracks; profiling must capture the entire asari process subcommand execution.
- Peak memory usage fluctuates during execution (e.g., spike during composite mass track construction and peak detection); reported peak should be the maximum resident memory (RSS or VMS) observed during a single run.
- Scaling behavior may differ between small studies (≤10 samples, pairwise m/z alignment) and large studies (>10 samples, clustering-based m/z alignment); benchmark design should test both regimes.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: pymzml, Scalability benchmark table (CSV or TSV) with columns: sample_count, wall_clock_time_seconds, peak_memory_mb, run_number, mean_time, std_dev_time, mean_memory, std_dev_memory, Summary report (text or markdown) stating mean throughput (samples/hour) per cohort and extrapolated time estimate for 1000-sample project.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does asari's computational performance (wall-clock time and peak memory usage) scale with increasing numbers of LC-MS samples?: 'Scalable, performance conscious, disciplined use of memory and CPU'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Asari is designed as a scalable program with performance-conscious implementation prioritizing disciplined use of memory and CPU resources.: 'Scalable, performance conscious, disciplined use of memory and CPU'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Public mzML files (minimum 100+ files) from MetaboLights or MassIVE repositories in centroided format: 'Input data are centroied mzML files from LC-MS metabolomics.'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] asari software installed from PyPI or cloned from source (v1.10+): 'From PyPi repository: `pip3 install asari-metabolomics`. Add `--upgrade` to update to new versions.'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] System profiling tools capable of capturing wall-clock runtime and peak memory usage: 'Asari is designed to run > 1000 samples on a laptop computer.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Scalability benchmark table (CSV or TSV) with columns: sample_count, wall_clock_time_seconds, peak_memory_mb, run_number, mean_time, std_dev_time, mean_memory, std_dev_memory: 'Asari is designed to run > 1000 samples on a laptop computer. The performance is achieved via ... Main intensity values of each sample are not kept in memory.'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Wall-clock time vs. sample count plot (PNG or PDF) showing linear or near-linear scaling up to 100+ samples: 'Asari is designed to run > 1000 samples on a laptop computer.'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Peak memory usage vs. sample count plot (PNG or PDF) demonstrating memory efficiency across cohort sizes: 'Main intensity values of each sample are not kept in memory.'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Summary report (text or markdown) stating mean throughput (samples/hour) per cohort and extrapolated time estimate for 1000-sample project: 'Asari is designed to run > 1000 samples on a laptop computer.'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] asari: 'Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] Python: 'Requires Python 3.8+.'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] pymzml: 'The default method uses `pymzml` to parse mzML files.'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting version history, performance improvements, or scalability-related fixes: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that asari can be installed from github:shuzhao-li-lab/asari and runs without errors on Python 3.8+
- verify that mzML test files are available from github:shuzhao-li/data/tree/main/data or a public metabolomics repository (MetaboLights/MassIVE)
- file_exists: performance_log.csv or equivalent structured output containing wall-clock execution time and peak memory usage
- value_in_range: wall-clock time increases monotonically or sub-linearly as sample count increases from 10 to 50 to 100+ samples (no canonical answer for exact scaling exponent; parameter-sensitive to hardware and file sizes)
- value_in_range: peak memory usage remains below laptop physical RAM limit (typically 8–16 GB) at 100+ sample threshold, robust to typical consumer hardware configurations
- output_matches_reference: reported scalability metric (samples processed per unit time, or memory per sample) is consistent with claim '>1000 samples on a laptop' stated in article abstract or results section

### Expert Review
- assess whether wall-clock time and memory measurements were collected under controlled, reproducible conditions (fixed hardware specs, single-threaded vs. multi-threaded configuration, consistent input file sizes)
- evaluate whether the tested mzML files are representative of real metabolomics datasets in terms of complexity, spectral density, and retention-time resolution
- determine whether measured scalability trajectory (time/memory vs. sample count) is extrapolatable to the claimed >1000-sample threshold or whether the tested range (10–100) is insufficient to validate the claim
- assess sensitivity of performance measurements to parameter choices (e.g., mass tolerance ppm, peak prominence thresholds, smoothing window size) that may affect per-sample processing cost

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Retrieve or construct public mzML test datasets at three scale points: 10, 50, and 100+ samples.
2. Install asari from PyPI (pip install asari-metabolomics) using default configuration (5 ppm tolerance, positive mode).
3. Execute asari process on each cohort using a system profiler (time, psutil, or Linux /usr/bin/time -v) to capture wall-clock duration and peak memory.
4. Repeat each run 2–3 times and calculate mean, standard deviation, and throughput (samples/hour) per cohort.
5. Plot wall-clock time and peak memory as functions of sample count; visually assess linearity and extrapolate to 1000-sample scenario.
6. Validation: confirm that observed scaling behaviour supports or refutes the >1000-samples-on-laptop claim by verifying that extrapolated runtime for 1000 samples remains <24 hours on a single CPU core with ≤16 GB peak memory.
7. References: source article (DOI: 10.1038/s41467-023-39889-1)

## Workflow Ports

**Inputs:**

- `mzml_dataset` — Public mzML dataset (100+ centroided files)
- `asari_software` — asari software (pip install or source clone)

**Outputs:**

- `benchmark_table` — Scalability benchmark table (CSV/TSV)
- `time_plot` — Wall-clock time vs. sample count plot (PNG/PDF)
- `memory_plot` — Peak memory vs. sample count plot (PNG/PDF)
- `summary_report` — Scalability summary report (TXT/MD)

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:shuzhao-li-lab__asari`
- **Synthesized at:** 2026-06-16T05:44:32+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
