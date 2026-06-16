# SciTask Card: Reproduce the screening-mode Diagnostic EIC Plots for 10 selected targets across one batch

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:24:56.964844+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_tardis/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `visualization`
- DOI: `10.1021/acs.analchem.5c00567`
- GitHub: `pablovgd/TARDIS`
- Input from: `task_000`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `lipidomics`, `untargeted-metabolomics`, `computational-metabolomics`
- Techniques: `lc-ms`, `feature-detection`, `chromatogram-alignment`, `quality-control`, `spectral-library-matching`

## Research Question
Does tardisPeaks() in screening mode successfully generate and save extracted ion chromatogram (EIC) plots for all 10 target compounds (5 internal standards + 5 endogenous metabolites) to the diagnostic QC output folder?

## Connected Finding
tardisPeaks() in screening mode generates EIC plots for all 10 targets that are saved to the output folder and can be inspected, with resulting diagnostic plots for QC runs showing peak detection and integration for each component.

## Task Description
Execute tardisPeaks() with screening_mode=TRUE on a 14-run LC-MS vignette dataset (10 targets: 5 internal standards + 5 endogenous compounds) to perform target visibility screening and generate 10 diagnostic extracted ion chromatogram (EIC) PNG plots saved to output/screening/Diagnostic_QCs_Batch_1/.

## Inputs
- 14 centroided .mzML LC-MS data files (vignette dataset)
- Target list data.frame with compound ID, name, m/z, retention time, and polarity

## Expected Outputs
- 10 extracted ion chromatogram (EIC) PNG plots (one per target compound) with peak annotations

## Landmark Outputs

- `screening_results.csv`
- `target_visibility_summary.txt`
- `Diagnostic_QCs_Batch_1/*.png`

## Tools
- TARDIS
- Spectra
- xcms
- R
- MsExperiment
- knitr

## Skills
- lcms-target-visibility-screening
- extracted-ion-chromatogram-inspection
- targeted-metabolite-detection-parameter-optimization
- mass-spectrometry-polarity-filtering
- chromatographic-peak-annotation-visualization

## Workflow Description
1. Load 14 centroided .mzML LC-MS runs and a target list data.frame containing compound ID, name, theoretical m/z, expected retention time, and ionization polarity into the TARDIS package environment. 2. Execute tardisPeaks() function with screening_mode=TRUE to detect peaks and screen for target compound visibility within defined m/z and retention time windows across all runs, automatically applying polarity filtering. 3. Generate extracted ion chromatogram (EIC) plots for each of the 10 targets with peak annotation and save as individual PNG files to the output/screening/Diagnostic_QCs_Batch_1/ folder for visual inspection of target detection.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/Component_131.png` | figure | False |
| `figures/Component_14.png` | figure | False |
| `figures/Component_15.png` | figure | False |
| `figures/Component_1576.png` | figure | False |
| `figures/Component_1577.png` | figure | False |
| `figures/Component_1578.png` | figure | False |
| `figures/Component_1583.png` | figure | False |
| `figures/Component_17.png` | figure | False |
| `figures/Component_179.png` | figure | False |
| `figures/Component_183.png` | figure | False |
| `figures/Component_21.png` | figure | False |
| `figures/Component_22.png` | figure | False |
| `figures/Component_23.png` | figure | False |
| `figures/Component_24.png` | figure | False |
| `figures/Component_25.png` | figure | False |
| `figures/Component_331.png` | figure | False |
| `figures/Component_7.png` | figure | False |
| `figures/Component_9.png` | figure | False |
| `figures/tardis.png` | figure | False |
| `figures/tardis_new.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found

## Domain Knowledge
- Screening mode in TARDIS checks whether target compounds are detectable within predefined m/z and retention time windows before full peak detection, serving as a QC step to validate method parameters.
- EIC plots display intensity versus retention time for a single extracted m/z value, essential for visual confirmation that detected peaks correspond to intended targets and not isobaric interferences.
- Internal standards (typically stable isotope-labeled analogs) and endogenous compounds require separate polarity filtering within TARDIS because they may ionize in positive or negative mode; the tool automates this filtering to avoid manual subsetting.
- Centroiding converts profile-mode (high-resolution continuous) LC-MS data to centroid mode (peak apex m/z and intensity pairs), reducing file size and simplifying peak detection algorithms.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Does tardisPeaks() in screening mode successfully generate and save extracted ion chromatogram (EIC) plots for all 10 target compounds (5 internal standards + 5 endogenous metabolites) to the diagnostic QC output folder?: 'We can run screening mode using the argument `screening_mode = TRUE` in the tardis_peaks function.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] tardisPeaks() in screening mode generates EIC plots for all 10 targets that are saved to the output folder and can be inspected, with resulting diagnostic plots for QC runs showing peak detection and integration for each component.: 'The resulting EICs are saved in the output folder and can be inspected'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] 14 centroided .mzML LC-MS data files (vignette dataset): 'Input files need to be converted to the .mzML format and have to be centroided'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Target list data.frame with compound ID, name, m/z, retention time, and polarity: 'compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity'
- `ev_005` from `agent2_synthesis` (agent2_traced): [results] 10 extracted ion chromatogram (EIC) PNG plots (one per target compound) with peak annotations: 'The resulting EICs are again saved in the output folder and can be inspected'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] TARDIS: 'R package for *TArgeted Raw Data Integration In Spectrometry*'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Spectra: 'loads MS data as `Spectra` objects so it's easily integrated with other tools'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] xcms: 'It makes use of an established retention time correction algorithm from the `xcms` package'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] R: 'R package for *TArgeted Raw Data Integration In Spectrometry*'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] MsExperiment: 'Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object'
- `ev_011` from `agent2_synthesis` (agent2_traced): [results] knitr: 'knitr::include_graphics'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file exists at output/screening/Diagnostic_QCs_Batch_1/ directory
- file_format_is PNG for all 10 EIC plot files in output/screening/Diagnostic_QCs_Batch_1/
- row_count_equals 10 PNG files present in output/screening/Diagnostic_QCs_Batch_1/ (one per component)
- script_runs: tardisPeaks() executes without error when called with screening_mode=TRUE on vignette LC-MS dataset
- file_exists for each expected EIC plot file matching pattern corresponding to the 10 targets (5 internal standards + 5 endogenous)

### Expert Review
- visual inspection of EIC plots for correct peak identification and appropriate m/z and retention time windows for each of the 10 targets
- verification that screening mode output correctly flags target visibility within specified m/z and RT windows for all 14 runs
- assessment that EIC plot quality is sufficient for diagnostic inspection (clarity, axis labels, peak prominence relative to noise)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load 14 centroided .mzML LC-MS runs and target compound metadata (m/z, retention time, polarity) into TARDIS environment.
2. Execute tardisPeaks() with screening_mode=TRUE to screen target visibility within m/z and retention time windows, applying automatic polarity filtering.
3. Generate and save 10 extracted ion chromatogram (EIC) PNG plots with peak annotations to output/screening/Diagnostic_QCs_Batch_1/ folder.
4. Validation: verify that exactly 10 PNG files are generated (one per target), each file exists in the specified output directory, and files are readable PNG images with visible chromatographic traces and peak annotations.
5. References: source article (DOI: 10.1021/acs.analchem.5c00567)

## Workflow Ports

**Inputs:**

- `mzml_runs` — 14 centroided LC-MS .mzML files
- `target_list` — Target list data.frame with compound metadata

**Outputs:**

- `eic_plots` — 10 diagnostic EIC PNG plots

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:UGent-LIMET__TARDIS`
- **Synthesized at:** 2026-06-16T07:31:03+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
