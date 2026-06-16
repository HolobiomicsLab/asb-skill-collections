# SciTask Card: Reproduce spectrum processing pipeline using MsmsSpectrum (set_mz_range, remove_precursor_peak, filter)

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:16:56.758905+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_spectrumutils/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `benchmark-evaluation`
- DOI: `10.1021/acs.analchem.9b04884`
- GitHub: `bittremieuxlab/spectrum_utils`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Techniques: `feature-detection`, `spectral-library-matching`, `quality-control`, `tandem-ms`

## Research Question
What is the sequence and behavior of spectrum preprocessing operations in spectrum_utils when applied to an MsmsSpectrum object?

## Connected Finding
spectrum_utils provides common spectrum processing operations including precursor & noise peak removal, intensity filtering, and intensity scaling optimized for computational efficiency.

## Task Description
Reconstruct and validate the spectrum_utils preprocessing pipeline by loading an MsmsSpectrum object via USI, applying set_mz_range (100–1400 m/z), remove_precursor_peak, filter_intensity (min_intensity=0.05, max_num_peaks=50), and scale_intensity operations in sequence, then verify that the resulting m/z and intensity arrays match the documented behavior.

## Inputs
- Public proteomics USI identifier (e.g., mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840)

## Expected Outputs
- Filtered MsmsSpectrum object with validated m/z array (100–1400 range), intensity array (scaled by square root, ≤50 peaks), and precursor peak removed
- Verification report (JSON or text) confirming m/z range boundaries, peak count ≤50, absence of precursor peak, and intensity scaling applied

## Expected Output File

- `validation_report.json`

## Landmark Outputs

- `raw_spectrum.mzML or raw_spectrum_metadata.json`
- `spectrum_after_mz_filter.json`
- `spectrum_after_precursor_removal.json`
- `spectrum_after_intensity_filter.json`
- `spectrum_after_scaling.json`

## Tools
- spectrum_utils
- Python

## Skills
- spectral-mz-range-filtering
- precursor-peak-removal-mass-tolerance
- intensity-threshold-noise-filtering
- peak-count-capping
- intensity-normalization-and-scaling
- spectrum-array-validation

## Workflow Description
1. Load an MsmsSpectrum object from a public proteomics dataset using the Universal Spectrum Identifier (USI) mechanism via spectrum_utils.spectrum.MsmsSpectrum.from_usi(). 2. Apply set_mz_range with min_mz=100 and max_mz=1400 to restrict the m/z window. 3. Apply remove_precursor_peak using the specified fragment tolerance (e.g., 10 ppm or 0.05 Da) to remove the parent ion. 4. Apply filter_intensity with min_intensity=0.05 (as a fraction of base peak) and max_num_peaks=50 to remove low-intensity noise and cap the peak count. 5. Apply scale_intensity with mode='root' to scale intensities by their square root. 6. Verify that the resulting spectrum object's m/z and intensity arrays contain only peaks within the expected range and that intensity values are properly scaled.

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
- No changelog found
- Documentation or reference spectrum data for verifying expected output of the preprocessing pipeline

## Domain Knowledge
- The m/z range 100–1400 is standard for peptide fragment analysis and filters out low-mass noise and high-mass artifacts outside the typical fragmentation window.
- Precursor peak removal requires a mass tolerance (ppm or Da) to account for instrument calibration error; spectrum_utils accepts both ppm and Da modes.
- Base peak intensity is the most intense peak in the spectrum; min_intensity=0.05 means retaining only peaks ≥5% of base peak intensity, a common threshold for noise reduction.
- Square-root scaling (scale_intensity='root') is applied after intensity filtering to de-emphasize overly intense peaks and improve visual and statistical balance.
- The max_num_peaks parameter caps the total number of peaks retained; max_num_peaks=50 ensures a manageable, interpretable peak list for fragment annotation.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What is the sequence and behavior of spectrum preprocessing operations in spectrum_utils when applied to an MsmsSpectrum object?: 'Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] spectrum_utils provides common spectrum processing operations including precursor & noise peak removal, intensity filtering, and intensity scaling optimized for computational efficiency.: 'Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Public proteomics USI identifier (e.g., mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840): 'usi = "mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840"
spectrum = sus.MsmsSpectrum.from_usi(usi)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Filtered MsmsSpectrum object with validated m/z array (100–1400 range), intensity array (scaled by square root, ≤50 peaks), and precursor peak removed: 'spectrum = (
    spectrum.set_mz_range(min_mz=100, max_mz=1400)
    .remove_precursor_peak(fragment_tol_mass, fragment_tol_mode)
    .filter_intensity(min_intensity=0.05, max_num_peaks=50)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Verification report (JSON or text) confirming m/z range boundaries, peak count ≤50, absence of precursor peak, and intensity scaling applied: 'Process the spectrum.
fragment_tol_mass, fragment_tol_mode = 10, "ppm"
spectrum = (
    spectrum.set_mz_range(min_mz=100, max_mz=1400)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] spectrum_utils: 'spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Python: 'spectrum_utils is a Python package'
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: 'No changelog found.'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] Documentation or reference spectrum data for verifying expected output of the preprocessing pipeline: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists in spectrum_utils repository: a Python module or example script that demonstrates loading an MsmsSpectrum object
- verify file exists in spectrum_utils repository: documentation or source code defining the set_mz_range method signature and behavior
- verify file exists in spectrum_utils repository: documentation or source code defining the remove_precursor_peak method signature and behavior
- verify file exists in spectrum_utils repository: documentation or source code defining the filter_intensity method signature and behavior
- script_runs: execute a reproducible Python script that instantiates an MsmsSpectrum object, applies set_mz_range(min_mz=100, max_mz=1400), remove_precursor_peak, and filter_intensity in sequence using the spectrum_utils package from github:bittremieux/spectrum_utils
- output_matches_reference: peak array structure (m/z values, intensities, length) after executing the preprocessing pipeline matches the documented behavior in the spectrum_utils README or API documentation

### Expert Review
- assess whether the resulting filtered peak arrays exhibit expected mass spectrometry properties: peaks fall within the specified m/z range (100–1400), precursor peak is absent, low-intensity noise is removed according to the min_intensity threshold, and peak ordering is preserved
- assess whether the sequential application of filters produces chemically plausible output for the test spectrum (no artifacts, no unexpected peak loss, no data corruption)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Load an MsmsSpectrum object from a public USI using spectrum_utils.MsmsSpectrum.from_usi().
2. Restrict m/z range to 100–1400 using set_mz_range() to remove out-of-range peaks.
3. Remove precursor (parent) ion peaks using remove_precursor_peak() with specified mass tolerance.
4. Filter low-intensity noise peaks using filter_intensity() with min_intensity=0.05 (5% base peak) and cap peak count at max_num_peaks=50.
5. Scale peak intensities by square root using scale_intensity('root') to normalize intensity distribution.
6. Validation: verify resulting spectrum m/z array is within [100, 1400], peak count is ≤50, precursor peak is absent, and intensity values reflect square-root transformation.
7. References: source article (DOI: 10.1021/acs.analchem.9b04884); MSV000082283 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082283); MSV000079960 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000079960); MSV000080679 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080679); PXD000561 (https://www.ebi.ac.uk/pride/archive/projects/PXD000561); PXD014834 (https://www.ebi.ac.uk/pride/archive/projects/PXD014834); PXD022531 (https://www.ebi.ac.uk/pride/archive/projects/PXD022531); PXD004732 (https://www.ebi.ac.uk/pride/archive/projects/PXD004732)

## Workflow Ports

**Inputs:**

- `usi_identifier` — Public proteomics USI identifier

**Outputs:**

- `filtered_spectrum` — Filtered and scaled MsmsSpectrum object
- `validation_report` — Verification report confirming preprocessing compliance

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:bittremieux-lab__spectrum_utils`
- **Synthesized at:** 2026-06-16T07:23:50+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
