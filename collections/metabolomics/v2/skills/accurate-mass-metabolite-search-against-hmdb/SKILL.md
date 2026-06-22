---
name: accurate-mass-metabolite-search-against-hmdb
description: Use when after MS1 feature detection and spectra merging in an untargeted or semi-targeted metabolomics workflow, when you have a list of observed accurate m/z values from high-resolution mass spectrometry (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - SmartPeak
  - SmartPeakGUI
  - SmartPeakCLI
  - OpenMS
  - pyOpenMS
  - BFAIR
  techniques:
  - direct-infusion-MS
  - NMR
derived_from:
- doi: 10.1021/acs.analchem.0c03421
  title: SmartPeak
evidence_spans:
- SmartPeak automates targeted and quantitative metabolomics data processing
- SmartPeak GUI provides functionality to facilitate users to get up and running as quickly as possible
- SmartPeak CLI provides an equivalent of SmartPeak GUI application, however with a possibility to run in headless mode
- SmartPeak CLI provides an equivalent of SmartPeak GUI application
- The software is based on the OpenMS toolkit
- The software is based on the OpenMS toolkit.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smartpeak_cq
    doi: 10.1021/acs.analchem.0c03421
    title: SmartPeak
  dedup_kept_from: coll_smartpeak_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03421
  all_source_dois:
  - 10.1021/acs.analchem.0c03421
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# accurate-mass-metabolite-search-against-hmdb

## Summary

Search detected MS1 features against the Human Metabolome Database (HMDB) using accurate mass values and positive/negative adduct libraries to annotate unknowns in untargeted FIA-MS and full-scan metabolomics workflows. This skill bridges peak detection and compound identification by matching observed m/z values to putative metabolite structures.

## When to use

After MS1 feature detection and spectra merging in an untargeted or semi-targeted metabolomics workflow, when you have a list of observed accurate m/z values from high-resolution mass spectrometry (e.g., FIAMS FullScan data at 12000 ppm resolution) and need to assign metabolite identities prior to background filtering and adduct deconvolution.

## When NOT to use

- Input features have been pre-annotated via targeted methods (e.g., MRM transitions with known retention times); use this skill only for unknowns.
- Mass spectrometry data is low-resolution (e.g., quadrupole, nominal m/z); accurate mass search requires ≥5 ppm accuracy to distinguish isobars.
- No HMDB or curated mass library is available or accessible; the skill requires validated reference compound databases.

## Inputs

- merged MS1 feature list (mzML format or OpenMS featureXML)
- HMDB mapping files with theoretical m/z values and adduct definitions
- positive adduct library (e.g., [M+H]+, [M+Na]+, [M+K]+)
- negative adduct library (e.g., [M-H]-, [M+Cl]-)
- accurate mass tolerance threshold (ppm)

## Outputs

- annotated feature list with putative metabolite identities
- mzTab output with compound annotations and metavalues
- feature table with HMDB mapping scores and confidence ranks

## How to apply

Load the merged MS1 features and invoke SEARCH_ACCURATE_MASS against HMDB mapping files, specifying both positive and negative adduct libraries to account for ionization diversity in FIA-MS. The search compares observed m/z values to theoretical m/z values of known metabolites in HMDB, typically using mass tolerance windows appropriate to instrument resolution (e.g., ±5–10 ppm for Orbitrap-level accuracy). Annotations are stored in mzTab format alongside feature metadata (e.g., retention time, intensity) to enable downstream filtering by signal intensity thresholds and blank-to-sample ratios. The rationale is that accurate mass alone provides provisional identifications; subsequent background estimation and feature filtering steps remove false positives driven by contamination or chemical noise.

## Related tools

- **SmartPeak** (Orchestrates SEARCH_ACCURATE_MASS workflow step and manages feature annotation pipeline) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (Underlying toolkit providing MS data I/O, accurate mass matching algorithms, and mzTab export)
- **pyOpenMS** (Python bindings for parsing and post-processing annotated feature files and mass mapping results)
- **BFAIR** (Companion library offering post-hoc FIA-MS annotation analysis and metabolite network visualization) — https://github.com/AutoFlowResearch/BFAIR
- **SmartPeakGUI** (Interactive visualization and validation of HMDB search results before and after background filtering) — https://github.com/AutoFlowResearch/SmartPeak

## Examples

```
# In SmartPeak workflow configuration (workflow_FIAMS_Unknowns.csv):
# Step 5: SEARCH_ACCURATE_MASS -in features.featureXML -db HMDB_mapping.tsv -mass_tolerance 5 -adducts pos_neg -out annotated_features.mzTab
```

## Evaluation signals

- Annotated feature list contains ≥1 HMDB compound per input m/z within specified tolerance; verify m/z match errors are ≤ tolerance threshold (typically ≤5 ppm).
- mzTab output includes populated compound reference columns (database ID, chemical formula, exact mass, adduct type) for ≥80% of detected features (or lower if expected in biological sample).
- Positive and negative adduct annotations are both present and distinguish chemically plausible ionization products (e.g., [M+H]+ vs. [M-H]- are not assigned to the same feature).
- Background estimation step (ESTIMATE_FEATURE_BACKGROUND_INTERFERENCES) succeeds and reduces feature count by removing low-intensity matches present in blank samples, confirming provisional identities are real signals.
- Downstream adduct merging (MERGE_FEATURES) clusters multiple adduct annotations of the same compound, indicating mass search correctly resolved structural isomers or different ionization states.

## Limitations

- Accurate mass search is ambiguous for isomeric metabolites with identical m/z; chemical identity requires orthogonal evidence (e.g., retention time, MS/MS fragmentation, or NMR).
- HMDB coverage is incomplete for lipids, unusual phytochemicals, and microbial metabolites; annotations for out-of-database compounds will be false negatives.
- Adduct ionization efficiency varies by matrix and instrument; the positive/negative libraries may not cover all observable adducts in a given sample, leading to missed identifications or misassignments.
- No changelog or version history provided for HMDB mapping files; reproducibility may be compromised if library versions are not explicitly tracked.
- Mass tolerance must be tuned to instrument calibration; poorly calibrated instruments or drifting m/z offsets can cause systematic search failures or false positives.

## Evidence

- [methods] Perform accurate mass search against HMDB mapping files using SEARCH_ACCURATE_MASS with positive and negative adduct libraries.: "Perform accurate mass search against HMDB mapping files using SEARCH_ACCURATE_MASS with positive and negative adduct libraries."
- [other] SmartPeak automates workflow steps from peak detection and integration over calibration curve optimization, to quality control reporting, which form the basis for configuring analysis types such as FIAMS FullScan Unknowns.: "SmartPeak automates workflow steps from peak detection and integration over calibration curve optimization, to quality control reporting, which form the basis for configuring analysis types such as"
- [other] Extract spectra windows over the acquisition time range (0–30 min) using EXTRACT_SPECTRA_WINDOWS with FIAMS resolution set to 12000 and max_mz to 1500.: "Extract spectra windows over the acquisition time range (0–30 min) using EXTRACT_SPECTRA_WINDOWS with FIAMS resolution set to 12000 and max_mz to 1500."
- [other] Store mzTab annotations with STORE_ANNOTATIONS and feature lists with STORE_FEATURES.: "Store mzTab annotations with STORE_ANNOTATIONS and feature lists with STORE_FEATURES."
- [readme] The software is based on the OpenMS toolkit.: "The software is based on the OpenMS toolkit."
