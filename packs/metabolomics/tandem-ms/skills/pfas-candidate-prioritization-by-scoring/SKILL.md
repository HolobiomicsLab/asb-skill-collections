---
name: pfas-candidate-prioritization-by-scoring
description: Use when you have a feature list (containing m/z, retention time, and molecular formula or neutral mass per feature) extracted from LC- or GC-HRMS data in mzML format with data-dependent acquisition, and you need to rank or flag features as likely PFAS compounds to reduce manual review burden in.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PFΔScreen
  - pyOpenMS
  - MSConvert
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen_cq
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-05070-2
  all_source_dois:
  - 10.1007/s00216-023-05070-2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# PFAS candidate prioritization by scoring

## Summary

Prioritize potential per- and polyfluoroalkyl substance (PFAS) features detected in non-target high-resolution mass spectrometry data by computing and thresholding normalized mass defect and mass-per-carbon metrics. This skill identifies high-priority PFAS candidates from feature lists using the MD/C–m/C approach and optional Kendrick mass defect analysis.

## When to use

Apply this skill when you have a feature list (containing m/z, retention time, and molecular formula or neutral mass per feature) extracted from LC- or GC-HRMS data in mzML format with data-dependent acquisition, and you need to rank or flag features as likely PFAS compounds to reduce manual review burden in non-target screening workflows.

## When NOT to use

- Input is already a manually curated suspect list or confirmed PFAS identifications—use this skill for discovery and prioritization of unknowns, not validation.
- Feature list lacks molecular formula information and no reliable heuristic for carbon count assignment is available—MD/C calculation requires accurate carbon numbers.
- Raw data is not in mzML format or lacks centroided, data-dependent (ddMS2) acquisition—feature detection and MS2 alignment depend on these specifications.

## Inputs

- Feature list (CSV or XLSX) with columns: m/z, retention time, molecular formula or neutral mass
- mzML files (LC- or GC-HRMS, data-dependent acquisition, centroided spectra)
- Optional blank control mzML file for blank subtraction

## Outputs

- Annotated feature list (Excel format) with MD, MD/C, m/C, and PFAS priority flag columns
- Interactive HTML plots: MD/C–m/C scatter plot, m/z vs. retention time plot, Kendrick mass defect vs. m/z plot, m/C histogram

## How to apply

For each feature in the input list, compute the mass defect (MD) as exact mass minus the nearest integer mass. Extract the number of carbons from the molecular formula if available, or apply a default heuristic. Calculate MD/C (mass defect divided by carbon count) and m/C (exact mass divided by carbon count). Apply user-defined MD/C and m/C threshold parameters to flag features exceeding both thresholds as high-priority PFAS candidates. The rationale is that PFAS compounds exhibit characteristic patterns in these normalized metrics due to their heavy fluorine content and repeating CF₂ units; features crossing both thresholds are more likely to be genuine PFAS than those passing only one criterion. Output annotated feature lists with calculated metrics and priority flags for downstream manual verification or MS2 fragment analysis.

## Related tools

- **PFΔScreen** (Integrates MD/C–m/C prioritization alongside Kendrick mass defect analysis and MS2 fragment matching; provides GUI for parameter tuning, feature detection, and result visualization) — https://github.com/JonZwe/PFAScreen
- **pyOpenMS** (Performs upstream feature detection in mzML raw data prior to MD/C–m/C scoring)
- **MSConvert** (Converts vendor-specific raw mass spectrometry files to vendor-independent mzML format as input to the workflow)

## Evaluation signals

- Output feature table contains MD, MD/C, m/C columns with numeric values in expected ranges (MD typically 0–1 Da; m/C and MD/C values vary by compound class).
- Priority flag (PFAS candidate = yes/no) is correctly assigned: features with MD/C AND m/C both exceeding user-defined thresholds are flagged 'yes'; all others 'no'.
- Blank-corrected sample features show higher PFAS candidate flags than corresponding blank features, confirming that prioritization is enriching genuine sample signals.
- Interactive MD/C–m/C plot shows clear visual separation of flagged vs. non-flagged features in the threshold-defined region.
- Manual inspection of high-priority features reveals characteristic PFAS markers (e.g., CF₂ repeating units, diagnostic MS2 fragments) in MS1 and MS2 spectra linked in RawDataVisualization tool.

## Limitations

- MD/C–m/C approach is empirical and tuned for known PFAS; novel or structurally atypical PFAS compounds may not exceed thresholds and will be missed.
- Accurate carbon count is essential; if molecular formula is unavailable or misassigned, MD/C calculation will be incorrect.
- Threshold parameters (MD/C and m/C cutoffs) are user-defined and require expert knowledge or literature calibration; suboptimal thresholds increase false positives or false negatives.
- Kendrick mass defect analysis and MS2 fragment prioritization are complementary but separate; MD/C–m/C alone does not confirm PFAS identity without downstream MS2 data review.

## Evidence

- [other] MD/C-m/C approach computes normalized mass metrics to identify PFAS: "For each feature, compute the mass defect (MD) as the difference between the exact mass and the nearest integer mass. Extract or infer the number of carbons from the molecular formula (if available)"
- [intro] PFΔScreen integrates MD/C-m/C with Kendrick and MS2 analysis for PFAS prioritization: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [readme] Input is feature list with m/z, RT, and molecular formula per feature: "To load a MS raw datafile, click the "Browse Sample.mzML" button and choose the mzML file of a sample and an optional mzML file of a blank control (Browse Blank.mzML). Sample and blank for raw data"
- [readme] Output includes annotated feature list and interactive plots for PFAS visualization: "The PFΔScreen results table (Excel format) and several interactive HTML plots are saved in a folder named after the sample that can be easily inspected, including a MD/C-m/C plot, a m/z vs. RT plot"
- [methods] MD/C-m/C approach exploits characteristic PFAS mass properties: "PFΔScreen prioritizes potential PFAS features in raw data from LC- or GC-HRMS measurements using MD/C-m/C approach, Kendrick mass defect analysis, and fragment mass differences with diagnostic"
