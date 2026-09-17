---
name: metabolite-identifier-mapping
description: Use when after peak detection and MS1 feature picking from merged FIA-MS
  spectra (typically 0–30 s acquisition window), when you have a list of accurate
  monoisotopic masses and need to assign HMDB compound identifiers, molecular formulas,
  and structural annotations to support mzTab output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - OpenMS
  - SmartPeak
  - SmartPeakCLI
  - pyOpenMS
  techniques:
  - direct-infusion-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c03421
  title: SmartPeak
evidence_spans:
- The software is based on the OpenMS toolkit
- The software is based on the OpenMS toolkit.
- SmartPeak automates targeted and quantitative metabolomics data processing
- SmartPeak CLI provides an equivalent of SmartPeak GUI application, however with
  a possibility to run in headless mode
- SmartPeak CLI provides an equivalent of SmartPeak GUI application
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omu_metabolomics_count_data_tool_cq
    doi: 10.1128/mra.00129-19
    title: omu metabolomics count data tool
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Metabolite Identifier Mapping

## Summary

Maps detected molecular features to metabolite identifiers and structural metadata by executing accurate mass searches against a reference database (e.g., HMDB) using configured mass error tolerances and adduct ion specifications. This skill bridges peak detection and metabolite annotation in untargeted FIA-MS workflows.

## When to use

After peak detection and MS1 feature picking from merged FIA-MS spectra (typically 0–30 s acquisition window), when you have a list of accurate monoisotopic masses and need to assign HMDB compound identifiers, molecular formulas, and structural annotations to support mzTab output generation or untargeted metabolomics interpretation.

## When NOT to use

- Input is already a fully annotated feature table with verified metabolite identifiers; re-mapping risks introducing conflicting or redundant annotations.
- Mass calibration error exceeds the configured tolerance window; feature masses are unreliable and will produce false or spurious matches.
- Reference database mapping files are missing, outdated, or incompatible with the ion adduct specifications; the search will fail or return incomplete annotations.

## Inputs

- Merged MS1 spectra (mzML or OpenMS native format) with detected molecular features and accurate m/z values
- Feature list with monoisotopic masses and integration metadata from peak picking
- HMDB reference database mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv)
- Ion adduct specification files (positive_adducts.tsv, negative_adducts.tsv)
- Mass error tolerance threshold (ppm)

## Outputs

- Annotated feature list with HMDB compound identifiers and molecular formula assignments
- mzTab format file summarizing accurate mass search annotations and feature lists
- Metabolite-to-feature mapping table (typically embedded in mzTab PSM and MTD sections)

## How to apply

Execute accurate mass search against the reference database (HMDB) using the detected feature masses and the configured mass error tolerance (typically in ppm range specified in SmartPeak parameters). Supply positive and negative adduct mapping files (e.g., positive_adducts.tsv, negative_adducts.tsv) and HMDB structure mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv) to enable ionization-aware and structure-aware annotation. The search returns one or more candidate matches per feature; annotate each detected peak with the matched HMDB compound identifier, molecular formula, and associated structural metadata. Assemble the annotated features into mzTab format, preserving the mass-to-metabolite linkage for downstream reporting and validation.

## Related tools

- **SmartPeak** (Orchestrates the complete workflow including peak detection, accurate mass search against HMDB, and annotation assembly into mzTab format) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (Command-line interface for executing accurate mass search and annotation steps without GUI interaction) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (Underlying toolkit providing accurate mass search algorithms and mzTab export functionality)
- **pyOpenMS** (Python bindings for parsing and programmatically processing mzTab and annotation output files)

## Examples

```
docker run --rm -ti -v C:/data:/sample-data autoflowresearch/smartpeak-cli:latest bash -c "SmartPeakCLI --input_raw /sample-data/FIAMS_data.mzML --accuracy_mass_search --hmdb_mapping /sample-data/HMDBMappingFile.tsv --output_mtab /sample-data/output.mzTab"
```

## Evaluation signals

- All detected features have assigned HMDB compound identifiers and molecular formulas; no features remain unannotated unless outside database coverage.
- Mass error between detected m/z and reference m/z is within the configured tolerance for all matched features (verify in mzTab accuracy metric columns).
- Ion adduct assignments are consistent with the specified positive/negative adduct lists; check PSM columns in mzTab for adduct type annotations.
- mzTab output file validates against the mzTab schema (v1.0 or later); verify MTD (metadata), PSM (peptide spectrum match analog), and feature sections are present and non-empty.
- Mapping reproducibility: re-running the workflow with identical parameters and input files produces identical HMDB assignments and mzTab output.

## Limitations

- Reference database coverage is incomplete; many detected features may fall outside HMDB scope and remain unmapped.
- Isotopic variants and in-source fragments can produce ambiguous mass matches; the skill does not resolve multiplicity without additional MS/MS confirmation.
- Mass calibration drift across the acquisition window (0–30 s) can degrade accuracy; pre-calibration using SmartPeak's calibration curve optimization is required.
- Adduct specification files must be manually curated and kept synchronized with the ionization mode and instrument configuration; mismatches produce incorrect annotations.

## Evidence

- [methods] Execute accurate mass search against the HMDB database using the mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv) and specified ion adducts (positive_adducts.tsv, negative_adducts.tsv) with the configured mass error tolerance.: "Execute accurate mass search against the HMDB database using the mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv) and specified ion adducts (positive_adducts.tsv, negative_adducts.tsv)"
- [methods] Annotate detected peaks with HMDB compound identifiers, molecular formulas, and structural metadata.: "Annotate detected peaks with HMDB compound identifiers, molecular formulas, and structural metadata."
- [methods] Assemble results into mzTab format containing the feature list and mass search annotations, then store the mzTab output file.: "Assemble results into mzTab format containing the feature list and mass search annotations, then store the mzTab output file."
- [other] SmartPeak automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting, which collectively support the generation of comprehensive data summaries including feature annotations and quality metrics.: "SmartPeak automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting, which collectively support the generation of comprehensive data"
