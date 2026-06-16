# Workflow Challenge: `coll_spectrumutils_workflow`


> spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization, providing optimized spectrum processing operations, fragment annotation using the ProForma 2.0 specification, and publication-quality spectrum plotting.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

spectrum_utils provides common spectrum processing operations including precursor and noise peak removal, intensity filtering, and intensity scaling optimized for computational efficiency. The package enables annotation of observed spectrum fragments using the ProForma 2.0 specification for modified peptidoforms, supporting multiple ion types and optional neutral loss annotation. spectrum_utils includes functionality for loading spectra from online proteomics and metabolomics data resources via the Universal Spectrum Identifier (USI) mechanism, as well as publication-quality and interactive spectrum visualization capabilities including standard plots, mirror plots for comparing spectra, and mass error plots.

## Research questions

- What is the sequence and behavior of spectrum preprocessing operations in spectrum_utils when applied to an MsmsSpectrum object?
- Does spectrum_utils.fragment_annotation correctly annotate b and y ions for a given ProForma 2.0 peptidoform string when applied to a publicly deposited spectrum?
- Does spectrum_utils achieve higher throughput (spectra per second) compared to pymzML and pyOpenMS when processing the same benchmark dataset?
- How does enabling neutral loss annotation in spectrum_utils.fragment_annotation affect the fraction of observed peaks that receive an interpretation?
- Can spectrum_utils load a publicly deposited mass spectrometry spectrum via Universal Spectrum Identifier (USI) and annotate it with fragment ion types for visualization?

## Methods overview

Load an MsmsSpectrum object from a public USI using spectrum_utils.MsmsSpectrum.from_usi(). Restrict m/z range to 100–1400 using set_mz_range() to remove out-of-range peaks. Remove precursor (parent) ion peaks using remove_precursor_peak() with specified mass tolerance. Filter low-intensity noise peaks using filter_intensity() with min_intensity=0.05 (5% base peak) and cap peak count at max_num_peaks=50. Scale peak intensities by square root using scale_intensity('root') to normalize intensity distribution. Validation: verify resulting spectrum m/z array is within [100, 1400], peak count is ≤50, precursor peak is absent, and intensity values reflect square-root transformation. References: source article (DOI: 10.1021/acs.analchem.9b04884); MSV000082283 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283); MSV000079960 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960); MSV000080679 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679); PXD000561 (https://www.ebi.ac.uk/pride/archive/projects/PXD000561); PXD014834 (https://www.ebi.ac.uk/pride/archive/projects/PXD014834); PXD022531 (https://www.ebi.ac.uk/pride/archive/projects/PXD022531); PXD004732 (https://www.ebi.ac.uk/pride/archive/projects/PXD004732) Load the target spectrum from a public USI-indexed repository using MsmsSpectrum.from_usi(). Parse the ProForma 2.0 string to extract sequence, modification sites, and modification types using the internal formal grammar and abstract syntax tree. Compute theoretical m/z values for all b and y ions from the annotated peptide. Match observed spectrum peaks to theoretical fragments within the specified mass tolerance (default: 10 ppm or 0.5 Da). Assign ion type ('b' or 'y'), charge state, and mass error to each matched peak. Validation: confirm that all returned annotations have m/z values within the input tolerance and ion types are correctly labeled as 'b' or 'y'. References: source article (DOI: 10.1021/acs.analchem.9b04884); MSV000082283 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283); MSV000079960 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960); MSV000080679 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679); PXD000561 (https://www.ebi.ac.uk/pride/archive/projects/PXD000561); PXD014834 (https://www.ebi.ac.uk/pride/archive/projects/PXD014834); PXD022531 (https://www.ebi.ac.uk/pride/archive/projects/PXD022531); PXD004732 (https://www.ebi.ac.uk/pride/archive/projects/PXD004732) Load iPRG2012.mgf and iterate over spectra, filtering to valid entries (≥10 peaks, charge present). Apply identical five-step processing pipeline to each spectrum: m/z range (100–1400), precursor removal, intensity filtering (≥5% base peak, max 150 peaks), square-root scaling, and measure elapsed time. Repeat for spectrum_utils, pymzML, and pyOpenMS independently; collect per-spectrum runtimes. Compute summary statistics: median, percentiles, and spectra-per-second throughput (1/median_time). Validation: spectrum_utils median processing time must be strictly lower than both pymzML and pyOpenMS medians, and reported throughput (spectra/second) must reflect the inverse relationship shown in the paper's box plot. References: source article (DOI: 10.1021/acs.analchem.9b04884); MSV000082283 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283); MSV000079960 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960); MSV000080679 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679); PXD000561 (https://www.ebi.ac.uk/pride/archive/projects/PXD000561); PXD014834 (https://www.ebi.ac.uk/pride/archive/projects/PXD014834); PXD022531 (https://www.ebi.ac.uk/pride/archive/projects/PXD022531); PXD004732 (https://www.ebi.ac.uk/pride/archive/projects/PXD004732) Retrieve public MS/MS spectrum via USI and load into spectrum_utils MsmsSpectrum object. Apply standard spectrum preprocessing: m/z range filtering (100–1400), precursor peak removal (10 ppm tolerance), noise filtering (0.05 min intensity, max 50 peaks), and square-root intensity scaling. Annotate fragment ions using ProForma peptide string with default ion types (a, b, y) and neutral losses disabled; count peaks receiving interpretation. Re-annotate the same spectrum with common neutral losses (NH₃, H₂O) enabled; count peaks receiving interpretation. Calculate peak annotation fractions for both conditions and compute the relative increase. Validation: verify that peak interpretation fraction increase when neutral losses are enabled matches the order-of-magnitude improvement shown in the reported neutral loss example spectra. References: source article (DOI: 10.1021/acs.analchem.9b04884); MSV000082283 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283); MSV000079960 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960); MSV000080679 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679); PXD000561 (https://www.ebi.ac.uk/pride/archive/projects/PXD000561); PXD014834 (https://www.ebi.ac.uk/pride/archive/projects/PXD014834); PXD022531 (https://www.ebi.ac.uk/pride/archive/projects/PXD022531); PXD004732 (https://www.ebi.ac.uk/pride/archive/projects/PXD004732) Retrieve the spectrum from a public proteomics data repository using the USI accession. Parse the ProForma peptide string and match fragment ion masses against observed m/z peaks within the specified tolerance. Generate and label annotated peaks for b and y ion types. Render a publication-quality spectrum plot with annotated fragments, appropriate axis labels, and styling (grid, spines). Validation: Output PNG file exists, contains rendered spectrum with visible annotated peaks, and pixel dimensions are consistent with specified figure size. References: source article (DOI: 10.1021/acs.analchem.9b04884); MSV000082283 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283); MSV000079960 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960); MSV000080679 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679); PXD000561 (https://www.ebi.ac.uk/pride/archive/projects/PXD000561); PXD014834 (https://www.ebi.ac.uk/pride/archive/projects/PXD014834); PXD022531 (https://www.ebi.ac.uk/pride/archive/projects/PXD022531); PXD004732 (https://www.ebi.ac.uk/pride/archive/projects/PXD004732)

**Domain:** bioinformatics

**Techniques:** feature-detection, spectral-library-matching, quality-control, tandem-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils enables spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils provides common spectrum processing operations including precursor and noise peak removal, intensity filtering, and intensity scaling optimized for computational efficiency. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils enables annotating observed spectrum fragments using the ProForma 2.0 specification for modified peptidoforms. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils supports publication-quality, fully customizable spectrum plotting and interactive spectrum plotting. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils uses sphinx to generate its documentation. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils project follows PEP 8 guidelines for Python code style. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils uses black to format and lint Python code. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils uniquely supports the full ProForma 2.0 specification. _[grounded: system_spectrum_utils]_
- **(finding)** Internally, spectrum_utils represents the ProForma 2.0 specification as a formal grammar which is used to create an abstract syntax tree when parsing a ProForma string. _[grounded: system_spectrum_utils]_
- **(finding)** By default, spectrum_utils annotates peptide b and y ions during fragment ion annotation. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils supports internal fragment ions which result from two amide bond cleavages and do not contain either terminus. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils supports immonium ions which are internal fragments for individual amino acids formed by a b/y cleavage on the N-terminal side and an a/x cleavage on the C-terminal side. _[grounded: system_spectrum_utils]_
- **(finding)** By default, no neutral losses are considered in spectrum_utils. _[grounded: system_spectrum_utils]_
- **(finding)** By default in spectrum_utils, singly-charged b and y peptide fragment ions are annotated with a label in spectrum plots. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils requires Python version 3.8 and above. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils supports Python version 3.8 and above. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils has fastobo as a third-party dependency. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils has Lark as a third-party dependency. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils has Matplotlib as a third-party dependency. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils has Numba as a third-party dependency. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils has NumPy as a third-party dependency. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils has Pandas as a third-party dependency. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils has platformdirs as a third-party dependency. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils has Pyteomics as a third-party dependency. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils has Vega-Altair as a third-party dependency. _[grounded: system_spectrum_utils]_
- **(finding)** Wout Bittremieux authored a paper titled 'spectrum_utils: A Python package for mass spectrometry data processing and visualization' published in Analytical Chemistry in 2020. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils processing has been optimized for computational efficiency using NumPy and Numba to process thousands of spectra per second. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils version 0.4.0 is faster than pymzML version 2.5.2 when performing typical spectrum processing tasks. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils version 0.4.0 is faster than pyOpenMS version 2.7.0 when performing typical spectrum processing tasks. _[grounded: system_spectrum_utils]_
- **(finding)** Numba's JIT compilation causes a significant outlier in the initial spectrum_utils method call before subsequent calls can be made very efficiently. _[grounded: system_spectrum_utils]_
- **(finding)** ProForma Base Level Support includes support for amino acid sequences.
- **(finding)** ProForma Base Level Support includes support for protein modifications using Unimod and PSI-MOD. _[grounded: tool_unimod]_
- **(finding)** ProForma Base Level Support includes support for N-terminal, C-terminal, and labile modifications.
- **(finding)** ProForma specification supports unusual amino acids O and U.
- **(finding)** ProForma specification supports ambiguous amino acids including X, B, and Z.
- **(finding)** ProForma Top Down Extensions include support for RESID CV/ontology for protein modifications. _[grounded: tool_resid]_
- **(finding)** ProForma Cross-Linking Extensions include support for cross-linked peptides using the XL-MOD CV/ontology. _[grounded: tool_xlmod]_
- **(finding)** ProForma Glycan Extensions include support for GNO CV/ontology for protein modifications.
- **(finding)** spectrum_utils supports primary peptide fragment ions of types a, b, c, x, y, and z. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils supports intact precursor ions marked as type p. _[grounded: system_spectrum_utils]_
- **(finding)** spectrum_utils supports reporter ions from isobaric labeling marked as type r. _[grounded: system_spectrum_utils]_
- **(finding)** The neutral loss of ammonia (NH3) has a mass difference of 17.026549.
- **(finding)** The neutral loss of water (H2O) has a mass difference of 18.010565.
- **(finding)** The neutral loss of carbon monoxide (CO) has a mass difference of 27.994915.
- **(finding)** The neutral loss of carbon dioxide (CO2) has a mass difference of 43.989829.
- **(finding)** The neutral loss of phosphoric acid (H3PO4) has a mass difference of 97.976896.
- **(finding)** spectrum_utils is freely available as open source under the Apache 2.0 license. _[grounded: system_spectrum_utils]_
- **(finding)** The quickstart instructs users to restrict the mass range to 100–1400 m/z.
- **(finding)** The quickstart instructs users to scale peak intensities by their square root to de-emphasize overly intense peaks.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Pyteomics or pymzML for reading MS data files

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Offline tools cannot be used when spectrum requires retrieval from USI

## Steps

### Step `task_001`
- Title: Reproduce spectrum processing pipeline using MsmsSpectrum (set_mz_range, remove_precursor_peak, filter)
- Task kind: `reproduction`
- Task: Reconstruct and validate the spectrum_utils preprocessing pipeline by loading an MsmsSpectrum object via USI, applying set_mz_range (100–1400 m/z), remove_precursor_peak, filter_intensity (min_intensity=0.05, max_num_peaks=50), and scale_intensity operations in sequence, then verify that the resulting m/z and intensity arrays match the documented behavior.
- Inputs:
  - Public proteomics USI identifier (e.g., mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840)
- Expected outputs:
  - Filtered MsmsSpectrum object with validated m/z array (100–1400 range), intensity array (scaled by square root, ≤50 peaks), and precursor peak removed
  - Verification report (JSON or text) confirming m/z range boundaries, peak count ≤50, absence of precursor peak, and intensity scaling applied
- Tools: spectrum_utils, Python
- Landmark output files: raw_spectrum.mzML or raw_spectrum_metadata.json, spectrum_after_mz_filter.json, spectrum_after_precursor_removal.json, spectrum_after_intensity_filter.json, spectrum_after_scaling.json
- Primary expected artifact: `validation_report.json`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce fragment annotation of a spectrum using ProForma 2.0 peptidoform notation
- Task kind: `reproduction`
- Task: Annotate b and y fragment ions in a publicly deposited tandem mass spectrum using spectrum_utils' ProForma 2.0 parser, then verify that annotated peak m/z values and ion types match expected fragment assignments.
- Inputs:
  - A ProForma 2.0 peptidoform string specifying sequence and modifications (e.g., 'DLTDYLM[Oxidation]K' or 'EM[Oxidation]EVEES[Phospho]PEK')
  - A tandem mass spectrum as a public USI accession or mzspec resource (e.g., mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372)
  - Fragment ion mass tolerance and tolerance mode (e.g., 10 ppm or 0.5 Da)
- Expected outputs:
  - A structured annotation report listing all matched b and y ion peaks with their assigned ion type, charge state, theoretical m/z, observed m/z, and mass error
  - A validation table or JSON structure confirming that each annotated peak's m/z and ion type match expected values within the tolerance window
- Tools: spectrum_utils, Python, ProForma 2.0, Unimod
- Landmark output files: spectrum_metadata.json, theoretical_fragments.csv, annotated_peaks.json
- Primary expected artifact: `fragment_annotation_report.json`

### Step `task_003`
- Depends on: `task_002`
- Title: Reproduce the speed benchmark showing spectrum_utils v0.4.0 is faster than pymzML v2.5.2 and pyOpenMS v2.7.0
- Task kind: `reproduction`
- Task: Re-run the throughput comparison benchmark across spectrum_utils, pymzML, and pyOpenMS on the iPRG2012.mgf dataset, measuring spectra-per-second processing rate for each library and verify that spectrum_utils achieves higher throughput than both alternatives as reported in the paper.
- Inputs:
  - iPRG2012.mgf mass spectrometry benchmark dataset
- Expected outputs:
  - Benchmarking results table containing median processing time (seconds) and spectra-per-second throughput for spectrum_utils, pymzML, and pyOpenMS
  - Box plot visualization comparing processing time distributions across the three libraries
- Tools: spectrum_utils, pymzML, pyOpenMS, Python, pyteomics, matplotlib, seaborn, NumPy
- Landmark output files: spectrum_utils_runtimes.npy, pymzml_runtimes.npy, pyopenms_runtimes.npy, runtime_boxplot.png
- Primary expected artifact: `throughput_benchmark_results.csv`

### Step `task_004`
- Depends on: `task_002`
- Title: Reconstruct neutral-loss annotation to verify that neutral losses increase the fraction of interpreted peaks
- Task kind: `component_reconstruction`
- Task: Load a publicly deposited MS/MS spectrum via USI, annotate fragment ions using spectrum_utils with neutral loss disabled and enabled, compute the fraction of observed peaks receiving interpretation in each condition, and verify the increase matches reported results.
- Inputs:
  - Public MS/MS spectrum deposited in PRIDE/MassIVE repository (e.g., mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840)
  - ProForma 2.0 peptide sequence string (e.g., 'WNQLQAFWGTGK' or with modifications)
- Expected outputs:
  - Fraction of observed peaks annotated without neutral loss (numeric value between 0 and 1)
  - Fraction of observed peaks annotated with neutral loss enabled (numeric value between 0 and 1)
  - Comparison report showing increase in peak interpretation fraction when neutral losses are enabled
- Tools: spectrum_utils, Python
- Landmark output files: spectrum_processed.pkl, annotations_without_nl.json, annotations_with_nl.json, peak_counts.csv
- Primary expected artifact: `peak_annotation_comparison.csv`

### Step `task_005`
- Depends on: `task_002`
- Title: Reproduce publication-quality spectrum plot using spectrum_utils.plot and Matplotlib
- Task kind: `reproduction`
- Task: Load a publicly deposited tandem mass spectrum via Universal Spectrum Identifier (USI), annotate fragment ions using ProForma 2.0 specification for b and y peptide ions, and render a publication-quality spectrum visualization as a PNG file.
- Inputs:
  - Universal Spectrum Identifier (USI) string for a public tandem MS spectrum (e.g., mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555)
  - ProForma 2.0 peptide sequence string with optional modifications (e.g., VLHPLEGAVVIIFK or EM[Oxidation]EVEES[Phospho]PEK)
  - Fragment ion mass tolerance value and mode (e.g., 10 ppm or 0.05 Da)
- Expected outputs:
  - PNG image file containing the annotated mass spectrum with b and y ions highlighted and labeled
- Tools: spectrum_utils, Python, matplotlib, ProForma 2.0
- Landmark output files: spectrum_object.pkl, annotated_spectrum.png
- Primary expected artifact: `annotated_spectrum.png`

## Final expected outputs

- `Benchmarking results table containing median processing time (seconds) and spectra-per-second throughput for spectrum_utils, pymzML, and pyOpenMS` (type: file, tolerance: hash)
- `Box plot visualization comparing processing time distributions across the three libraries` (type: file, tolerance: hash)
- `Fraction of observed peaks annotated without neutral loss (numeric value between 0 and 1)` (type: file, tolerance: hash)
- `Fraction of observed peaks annotated with neutral loss enabled (numeric value between 0 and 1)` (type: file, tolerance: hash)
- `Comparison report showing increase in peak interpretation fraction when neutral losses are enabled` (type: file, tolerance: hash)
- `PNG image file containing the annotated mass spectrum with b and y ions highlighted and labeled` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: open — validity-first.** The deterministic match-rubrics above are demoted to *informational*. The binding evaluator is **SCIENTIFIC_VALIDITY** (below). Any scientifically sound method that addresses the research question is valid, and novel findings or unexplored aspects can score positively — **different is not wrong**.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** intermediate

- **Orchestration planning:** static

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_spectrumutils_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Benchmarking results table containing median processing time (seconds) and spectra-per-second throughput for spectrum_utils, pymzML, and pyOpenMS": "<locator>",
    "Box plot visualization comparing processing time distributions across the three libraries": "<locator>",
    "Fraction of observed peaks annotated without neutral loss (numeric value between 0 and 1)": "<locator>",
    "Fraction of observed peaks annotated with neutral loss enabled (numeric value between 0 and 1)": "<locator>",
    "Comparison report showing increase in peak interpretation fraction when neutral losses are enabled": "<locator>",
    "PNG image file containing the annotated mass spectrum with b and y ions highlighted and labeled": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
