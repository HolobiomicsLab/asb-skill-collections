# SciTask Card: Reconstruct the PCPFM fixed processing pipeline from raw mzML input to annotated feature table output

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T12:44:57.617706+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_pcpfm/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `data-analysis`
- DOI: `10.1371/journal.pcbi.1011912`
- GitHub: `shuzhao-li-lab/PythonCentricPipelineForMetabolomics`

## Classification

- Task kind: `component_reconstruction`
- Article type: `research-article`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `lc-ms`, `tandem-ms`, `feature-detection`, `database-annotation`, `spectral-library-matching`, `metabolite-identification`

## Research Question
What are the sequential data processing steps that the PCPFM pipeline executes to transform raw LC-MS metabolomics data into normalized feature tables ready for statistical analysis?

## Connected Finding
PCPFM implements a fixed orchestrator pipeline that sequences: (1) experiment assembly from metadata; (2) raw file conversion to mzML; (3) Asari feature extraction producing full and preferred feature tables; (4) blank masking by comparing sample to blank intensities with configurable intensity ratios; (5) sample dropping by metadata field or QAQC results; (6) TIC normalization using common features above a percentile threshold; (7) missing value imputation as multiples of minimum feature values; (8) optional batch correction using pycombat; and (9) empirical compound construction via khipu with configurable mz/rt tolerances and adduct/isotope definitions.

## Task Description
Implement the fixed PCPFM orchestration control loop that coordinates sequential metabolomics data processing: experiment assembly, LC-MS feature extraction via Asari, blank masking, sample dropping, normalization, missing-value imputation, and empirical compound construction. The system must maintain experiment state across all stages and output a feature table and empirical compound list ready for downstream annotation and statistical analysis.

## Inputs
- CSV metadata file with sample names, file paths, sample type classification, and batch identifiers
- Raw LC-MS data files in Thermo .raw or mzML format

## Expected Outputs
- Processed feature table (TSV/CSV) with normalized, imputed, and filtered metabolomic features ready for statistical analysis
- Empirical compound JSON file representing putative metabolites grouped by isotopes and adducts with pre-annotation
- Experiment state JSON file (experiment.json) tracking all processing steps, intermediate tables, and metadata

## Expected Output File

- `preferred_feature_table.tsv`

## Landmark Outputs

- `converted_acquisitions/*.mzML`
- `asari_results/preferred_Feature_table.tsv`
- `feature_tables/*_blank_masked.tsv`
- `feature_tables/*_normalized.tsv`
- `feature_tables/*_imputed.tsv`
- `annotations/empCpd.json`

## Tools
- Python
- ThermoRawFileParser
- Asari
- khipu

## Skills
- lc-ms-feature-extraction-and-alignment
- metabolite-quality-control-filtering
- feature-intensity-normalization-and-batch-correction
- missing-value-imputation-in-metabolomics
- empirical-compound-grouping-by-adducts-and-isotopes
- experiment-metadata-organization-and-tracking

## Workflow Description
1. Assemble experiment using pcpfm assemble with CSV metadata file (sample names, file paths, sample types, batch identifiers) to create an experiment directory and JSON state object. 2. Convert Thermo .raw files to centroid mzML format using ThermoRawFileParser via pcpfm convert command with $RAW_PATH and $OUT_PATH substitution. 3. Run Asari feature extraction on mzML files using pcpfm asari, inferring ionization mode and generating 'full' and 'preferred' feature table monikers with default 5 ppm m/z tolerance and 2 sec retention-time tolerance. 4. Perform blank masking using pcpfm blank_masking with intensity-ratio threshold (default 3×) to remove features where blank intensity exceeds sample intensity; repeat for each blank type if needed. 5. Drop unwanted samples (QC, blanks) via pcpfm drop_samples by metadata field match, sample name, or QAQC filter criteria. 6. Normalize feature intensities using pcpfm normalize with TIC based on common features at specified percentile cutoff (default 90%); optionally apply batch-aware two-step normalization (within-batch then between-batch). 7. Remove infrequent features via pcpfm drop_missing_features using feature-retention percentile threshold (default 50%) to discard rare features. 8. Impute missing values using pcpfm impute with interpolation ratio (default 0.5×) applied to minimum per-feature value. 9. Build empirical compounds from final feature table using pcpfm build_empCpds with khipu, specifying adducts (charge up to z=3), isotope patterns (13C3), m/z tolerance (default 5 ppm), and retention-time tolerance (default 2 sec); save moniker for downstream annotation.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history is documented
- The provided section text contains no description of the ARCH-PIPELINE fixed architecture, its stages, control flow, or orchestrator implementation

## Domain Knowledge
- Asari infers ionization mode from mzML files and applies it consistently throughout feature extraction and empirical compound construction; ionization mode must match across all samples in an experiment.
- Blank masking compares feature intensities between blanks and study samples by intensity ratio (default 3×); this assumes blanks and study samples are reasonably temporally aligned and may fail if acquisition order violates this assumption.
- Feature imputation uses a multiplicative floor (default 0.5× minimum feature intensity) rather than a fixed threshold, because mass-spectrometry intensity error is multiplicative and must scale with feature abundance.
- Empirical compound construction in khipu groups features by m/z tolerance (default 5 ppm for Orbitrap), retention-time tolerance (default 2 sec), and chemical logic (adducts up to charge z=3, 13C3 isotopologues); singleton features (no associated adducts or isotopes) cannot be assigned formulas for Level 4 annotation.
- Normalization using common features (e.g., 90th percentile) prevents bias introduced by samples with disproportionately high or low feature counts; batch-aware normalization requires both a batch metadata field and a second normalization pass to correct inter-batch systematic shifts.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] What are the sequential data processing steps that the PCPFM pipeline executes to transform raw LC-MS metabolomics data into normalized feature tables ready for statistical analysis?: 'The pipeline can convert Thermo .raw to mzML, process mzML data to feature tables (Asari), perform quality control, data normalization and batch correction, pre-annotation to group features to'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] PCPFM implements a fixed orchestrator pipeline that sequences: (1) experiment assembly from metadata; (2) raw file conversion to mzML; (3) Asari feature extraction producing full and preferred feature tables; (4) blank masking by comparing sample to blank intensities with configurable intensity ratios; (5) sample dropping by metadata field or QAQC results; (6) TIC normalization using common features above a percentile threshold; (7) missing value imputation as multiples of minimum feature values; (8) optional batch correction using pycombat; and (9) empirical compound construction via khipu with configurable mz/rt tolerances and adduct/isotope definitions.: 'pcpfm assemble, pcpfm convert, pcpfm asari, pcpfm blank_masking --blank_intensity_ratio, pcpfm drop_samples, pcpfm normalize --TIC_normalization_percentile, pcpfm impute --interpolation_ratio, pcpfm'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] CSV metadata file with sample names, file paths, sample type classification, and batch identifiers: 'CSV file for metadata (minimal sample names and file path)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Raw LC-MS data files in Thermo .raw or mzML format: 'Inputs should include a set of raw files (.raw or .mzML)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Processed feature table (TSV/CSV) with normalized, imputed, and filtered metabolomic features ready for statistical analysis: 'Outputs are intended to be immediately usable for downstream analysis'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Empirical compound JSON file representing putative metabolites grouped by isotopes and adducts with pre-annotation: 'empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Experiment state JSON file (experiment.json) tracking all processing steps, intermediate tables, and metadata: 'The experiment object will be used throught the processing and store intermediates'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Python: 'Python-Centric Pipeline for Metabolomics'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] ThermoRawFileParser: 'convert Thermo .raw to mzML (ThermoRawFileParser)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] Asari: 'process mzML data to feature tables (Asari)'
- `ev_011` from `agent2_synthesis` (agent2_traced): [intro] khipu: 'pre-annotation to group featues to empirical compounds (khipu)'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history is documented: '_No changelog found._'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] The provided section text contains no description of the ARCH-PIPELINE fixed architecture, its stages, control flow, or orchestrator implementation: '[UNTRUSTED_DOCUMENT] _No changelog found._ ## References ... [/UNTRUSTED_DOCUMENT]'

## Evaluation Strategy
### Direct Checks
- verify that github:shuzhao-li-lab/PythonCentricPipelineForMetabolomics repository is accessible and contains a README
- file_exists: README.md or equivalent documentation in the repository root
- contains_substring: README describes a fixed architecture pipeline with steps for (1) experiment assembly, (2) Asari feature extraction, (3) blank masking, (4) sample dropping, (5) normalization, (6) imputation, (7) empCpd construction
- file_exists: a Python orchestrator script or module that implements the fixed control loop (e.g., main.py, pipeline.py, or equivalent in the repo)
- script_runs: the orchestrator script executes without errors on a minimal valid mzML input and produces intermediate outputs at each of the seven pipeline stages
- output_matches_reference: intermediate outputs from a reference execution (if provided in asari_pcpfm_tutorials or deployment guide) match in structure (column names, data types, row counts for identical inputs) — robust to parameter choices
- file_format_is: final output of pipeline is one of (.txt, JSON) as stated in EnrichedIndex
- verify that the orchestrator implements a bounded, deterministic, sequentially-ordered control loop with no branching or conditional re-entry — no 'and then', 'if', or loops over variable sub-task counts

### Expert Review
- Evaluate whether the documented pipeline architecture faithfully represents the method as described in the published article (DOI: 10.1371/journal.pcbi.1011912), particularly the role and configuration of blank masking, sample dropping, normalization, and imputation steps
- Assess whether the fixed control loop design is scientifically sound for typical LC-MS metabolomics workflows and whether any documented deviations or optional branches undermine the 'fixed' characterization
- Review documentation clarity: does the README or equivalent explicitly describe the purpose, input contracts, and output semantics of each of the seven stages?

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Parse and validate CSV metadata; create experiment directory structure and initialize experiment.json state object with sample metadata, file paths, and sample-type annotations.
2. Convert Thermo .raw files to centroid mzML using ThermoRawFileParser; store converted files in experiment/converted_acquisitions subdirectory.
3. Run Asari feature extraction on mzML files with inferred ionization mode, m/z tolerance (5 ppm), and retention-time tolerance (2 sec); generate 'full' and 'preferred' feature table monikers.
4. Apply blank masking by comparing feature intensity ratios (study samples vs. blanks, default 3×) to remove likely contaminants and background ions; retain filtered feature table moniker.
5. Drop unwanted samples (blanks, QC, outliers) via metadata field or QAQC filter criteria; generate trimmed feature table moniker.
6. Normalize feature intensities using TIC of common features (default 90th percentile) with within-batch and between-batch correction if multiple batches present; apply normalization factors to all samples.
7. Impute missing values using multiplicative floor (default 0.5× per-feature minimum) to handle zero or missing entries while respecting multiplicative error structure.
8. Remove infrequent features below retention percentile (default 50%) to discard rare and potentially spurious features; generate filtered feature table moniker.
9. Build empirical compounds from final feature table using khipu with adducts (z ≤ 3), isotope patterns (13C3), m/z tolerance (5 ppm), and retention-time tolerance (2 sec); assign pre-annotations (adduct class, isotope status) and generate empCpd.json.
10. Validation: Verify feature table row count > 0, empCpd.json contains ≥1 compound objects with required keys (adducts, rt, mz, features), and experiment.json tracks all moniker transformations with no gaps in processing history.
11. References: source article (DOI: 10.1371/journal.pcbi.1011912)

## Workflow Ports

**Inputs:**

- `metadata_csv` — Sample metadata with names, file paths, types, and batch identifiers
- `raw_data_files` — Raw LC-MS acquisitions in .raw or .mzML format

**Outputs:**

- `processed_feature_table` — Normalized, imputed, blank-masked, sample-filtered feature table (TSV)
- `empirical_compounds` — Empirical compound JSON with pre-annotation (isotopes, adducts)
- `experiment_state` — Experiment state JSON tracking all processing steps and intermediates

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:shuzhao-li-lab__PythonCentricPipelineForMetabolomics`
- **Synthesized at:** 2026-06-15T12:53:24+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
