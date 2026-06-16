# SciTask Card: Reproduce the speed benchmark showing spectrum_utils v0.4.0 is faster than pymzML v2.5.2 and pyOpenMS v2.7.0

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:16:56.758905+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_spectrumutils/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `benchmark-evaluation`, `data-processing`
- DOI: `10.1021/acs.analchem.9b04884`
- GitHub: `bittremieuxlab/spectrum_utils`
- Input from: `task_002`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Techniques: `feature-detection`, `spectral-library-matching`, `quality-control`, `tandem-ms`

## Research Question
Does spectrum_utils achieve higher throughput (spectra per second) compared to pymzML and pyOpenMS when processing the same benchmark dataset?

## Connected Finding
The provided document text does not contain reported throughput comparison results or benchmarking data comparing spectrum_utils, pymzML, and pyOpenMS performance metrics.

## Task Description
Re-run the throughput comparison benchmark across spectrum_utils, pymzML, and pyOpenMS on the iPRG2012.mgf dataset, measuring spectra-per-second processing rate for each library and verify that spectrum_utils achieves higher throughput than both alternatives as reported in the paper.

## Inputs
- iPRG2012.mgf mass spectrometry benchmark dataset

## Expected Outputs
- Benchmarking results table containing median processing time (seconds) and spectra-per-second throughput for spectrum_utils, pymzML, and pyOpenMS
- Box plot visualization comparing processing time distributions across the three libraries

## Expected Output File

- `throughput_benchmark_results.csv`

## Landmark Outputs

- `spectrum_utils_runtimes.npy`
- `pymzml_runtimes.npy`
- `pyopenms_runtimes.npy`
- `runtime_boxplot.png`

## Tools
- spectrum_utils
- pymzML
- pyOpenMS
- Python
- pyteomics
- matplotlib
- seaborn
- NumPy

## Skills
- mass-spectrometry-benchmark-design
- spectrum-processing-pipeline-construction
- computational-throughput-measurement
- multi-library-comparative-analysis
- spectrum-filtering-and-normalization
- runtime-performance-profiling

## Workflow Description
1. Load iPRG2012.mgf dataset and parse spectra using pyteomics.mgf.read, filtering to spectra with ≥10 peaks and valid charge states. 2. For each library (spectrum_utils, pymzML, pyOpenMS), apply identical processing: set m/z range to 100–1400 Da, remove precursor peak, filter intensity (min_intensity=0.05, max_num_peaks=150), and scale intensities by square root. 3. Measure wall-clock time per spectrum for each library using Python time.time() before and after processing steps. 4. Compute processing rate (spectra per second) as the inverse of median runtime per spectrum for each library. 5. Tabulate median runtimes and throughput rates; verify spectrum_utils median is lower than both pymzML and pyOpenMS.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/annot_fmt.png` | figure | False |
| `figures/facet.png` | figure | False |
| `figures/ion_types.png` | figure | False |
| `figures/mass_errors.png` | figure | False |
| `figures/mirror.png` | figure | False |
| `figures/neutral_losses_1.png` | figure | False |
| `figures/neutral_losses_2.png` | figure | False |
| `figures/proforma_ast.png` | figure | False |
| `figures/proforma_ex1.png` | figure | False |
| `figures/proforma_ex2.png` | figure | False |
| `figures/proforma_ex3.png` | figure | False |
| `figures/quickstart.png` | figure | False |
| `figures/runtime.png` | figure | False |
| `figures/spectrum_utils.png` | figure | False |
| `paper.md` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| massive | `MSV000082283` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283 | # Retrieve the spectrum by its USI.     usi = "mzspec:MSV000082283:f07074:scan:5475"     spectrum = sus.MsmsSpectrum.from_usi( |
| massive | `MSV000079960` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960 | as sus   peptide = "DLTDYLM[Oxidation]K" usi_top = "mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372" spectrum_top = sus.MsmsSpectrum. |
| massive | `MSV000080679` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679 | a(peptide, 0.5, "Da", ion_types="aby") usi_bottom = "mzspec:MSV000080679:j11962_C1orf144:scan:10671" spectrum_bottom = sus.MsmsSpect |
| pride | `PXD000561` | https://www.ebi.ac.uk/pride/archive/projects/PXD000561 | s sup import spectrum_utils.spectrum as sus   usi = "mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555" peptide = |
| pride | `PXD014834` | https://www.ebi.ac.uk/pride/archive/projects/PXD014834 | s sup import spectrum_utils.spectrum as sus   usi = "mzspec:PXD014834:TCGA-AA-3518-01A-11_W_VU_20120915_A0218_3F_R_FR01:scan:8370 |
| pride | `PXD022531` | https://www.ebi.ac.uk/pride/archive/projects/PXD022531 | as sup import spectrum_utils.spectrum as sus  usi = "mzspec:PXD022531:j12541_C5orf38:scan:12368" peptide = "VAATLEILTLK/2" spectr |
| pride | `PXD004732` | https://www.ebi.ac.uk/pride/archive/projects/PXD004732 | s sup import spectrum_utils.spectrum as sus   usi = "mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840" |

## Missing Information
- No changelog found.
- No explicit description provided of the benchmark dataset, its size, format, number of spectra, or location for reproducibility of the throughput comparison.
- No specification provided of the exact throughput values (spectra-per-second rates) reported for spectrum_utils, pymzML, and pyOpenMS in the original paper.
- No description provided of the computational environment, hardware specifications, Python version, or library version requirements for reproducing the reported throughput comparison.

## Domain Knowledge
- Spectrum processing pipelines are non-idempotent and must be applied in fixed order: m/z range filtering, precursor removal, intensity filtering, then intensity scaling.
- The iPRG2012 benchmark dataset is a standard mass spectrometry proteomics dataset used for reproducible performance comparisons across spectrum analysis tools.
- Spectra with fewer than 10 peaks or missing charge state information must be excluded to ensure fair comparison across libraries with differing handling of invalid inputs.
- Processing time measurements must use wall-clock time (time.time()) before and after all processing steps to capture the full computational cost including overhead; Numba JIT compilation causes significant outliers on first invocation.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does spectrum_utils achieve higher throughput (spectra per second) compared to pymzML and pyOpenMS when processing the same benchmark dataset?: 'spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] The provided document text does not contain reported throughput comparison results or benchmarking data comparing spectrum_utils, pymzML, and pyOpenMS performance metrics.: 'spectrum_utils contains the following features: - Spectrum loading from online proteomics and metabolomics data resources'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] iPRG2012.mgf mass spectrometry benchmark dataset: 'mgf_filename = "iPRG2012.mgf"'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Benchmarking results table containing median processing time (seconds) and spectra-per-second throughput for spectrum_utils, pymzML, and pyOpenMS: 'spectrum_utils (version 0.4.0) is faster than alternative libraries, such as [pymzML](https://github.com/pymzml/pymzML/) (version 2.5.2) and [pyOpenMS](https://pyopenms.readthedocs.io/) (version'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Box plot visualization comparing processing time distributions across the three libraries: 'fig, ax = plt.subplots()
sns.boxplot(
    data=[runtimes_spectrum_utils, runtimes_pymzml, runtimes_pyopenms],
    flierprops={"markersize": 2},
    ax=ax,
)
ax.set_yscale("log")'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] spectrum_utils: 'spectrum_utils (version 0.4.0) is faster than alternative libraries'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] pymzML: 'pymzML](https://github.com/pymzml/pymzML/) (version 2.5.2)'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] pyOpenMS: 'pyOpenMS](https://pyopenms.readthedocs.io/) (version 2.7.0)'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Python: 'import time
import matplotlib.pyplot as plt'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] pyteomics: 'import pyteomics.mgf'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] matplotlib: 'import matplotlib.pyplot as plt'
- `ev_012` from `agent2_synthesis` (agent2_traced): [other] seaborn: 'import seaborn as sns'
- `ev_013` from `agent2_synthesis` (agent2_traced): [other] NumPy: 'import numpy as np'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found.: 'No changelog found.'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] No explicit description provided of the benchmark dataset, its size, format, number of spectra, or location for reproducibility of the throughput comparison.: '[The provided section contains only metadata and references; no benchmark dataset details are present in the text.]'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] No specification provided of the exact throughput values (spectra-per-second rates) reported for spectrum_utils, pymzML, and pyOpenMS in the original paper.: '[The provided section contains only metadata and references; no throughput numeric results are present in the text.]'
- `ev_017` from `agent2_synthesis` (agent2_traced): [discussion] No description provided of the computational environment, hardware specifications, Python version, or library version requirements for reproducing the reported throughput comparison.: '[The provided section contains only metadata and references; no environmental specifications are present in the text.]'

## Evaluation Strategy
### Direct Checks
- verify that benchmark dataset is accessible and loadable (file_exists for dataset artifact or public accession resolvable)
- verify that spectrum_utils, pymzML, and pyOpenMS can all be installed and imported in a common Python environment (script_runs for installation and import statements)
- verify that throughput benchmark script executes without errors on the benchmark dataset (script_runs for benchmark execution code)
- verify that output throughput table contains numeric spectra-per-second rates for all three tools with same dataset and same computational environment (format_is for table structure and field_present for rate columns)
- verify that spectrum_utils spectra-per-second rate value is numerically greater than both pymzML and pyOpenMS rates in the output (value_in_range or comparison check robust to parameter choices in dataset size and hardware)
- verify that reported throughput rates match the values cited in the paper's results section (output_matches_reference to paper citation of specific spectra-per-second numbers)

### Expert Review
- assess whether benchmark conditions (hardware, Python version, library versions, dataset size, processing pipeline) match those described in the paper's methods section
- assess whether observed throughput ratios are consistent with expected performance characteristics and algorithmic complexity of the three implementations
- assess whether any confounding factors (caching, JIT compilation, memory pressure, GC behavior) could invalidate fair comparison across the three tools

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Load iPRG2012.mgf and iterate over spectra, filtering to valid entries (≥10 peaks, charge present).
2. Apply identical five-step processing pipeline to each spectrum: m/z range (100–1400), precursor removal, intensity filtering (≥5% base peak, max 150 peaks), square-root scaling, and measure elapsed time.
3. Repeat for spectrum_utils, pymzML, and pyOpenMS independently; collect per-spectrum runtimes.
4. Compute summary statistics: median, percentiles, and spectra-per-second throughput (1/median_time).
5. Validation: spectrum_utils median processing time must be strictly lower than both pymzML and pyOpenMS medians, and reported throughput (spectra/second) must reflect the inverse relationship shown in the paper's box plot.
6. References: source article (DOI: 10.1021/acs.analchem.9b04884); MSV000082283 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283); MSV000079960 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960); MSV000080679 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679); PXD000561 (https://www.ebi.ac.uk/pride/archive/projects/PXD000561); PXD014834 (https://www.ebi.ac.uk/pride/archive/projects/PXD014834); PXD022531 (https://www.ebi.ac.uk/pride/archive/projects/PXD022531); PXD004732 (https://www.ebi.ac.uk/pride/archive/projects/PXD004732)

## Workflow Ports

**Inputs:**

- `mgf_benchmark_file` — iPRG2012.mgf mass spectrometry benchmark dataset ← `task_002/annotation_report`

**Outputs:**

- `throughput_table` — Benchmarking results with processing times and throughput rates
- `runtime_boxplot` — Box plot visualization of processing time distributions

**Used:** `urn:asb:port:task_002/annotation_report`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:bittremieux-lab__spectrum_utils`
- **Synthesized at:** 2026-06-16T07:23:50+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
