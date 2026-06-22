---
name: mztab-format-generation
description: Use when after completing peak detection, MS1 feature picking, and accurate mass database search (e.g., against HMDB) on FIA-MS or LC-MS(/MS) data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - OpenMS
  - SmartPeak
  - SmartPeakCLI
  - pyOpenMS
  - BFAIR
  techniques:
  - LC-MS
  - direct-infusion-MS
derived_from:
- doi: 10.1021/acs.analchem.0c03421
  title: SmartPeak
evidence_spans:
- The software is based on the OpenMS toolkit
- The software is based on the OpenMS toolkit.
- SmartPeak automates targeted and quantitative metabolomics data processing
- SmartPeak CLI provides an equivalent of SmartPeak GUI application, however with a possibility to run in headless mode
- SmartPeak CLI provides an equivalent of SmartPeak GUI application
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

# mztab-format-generation

## Summary

Generate standardized mzTab output files that summarize MS1 feature annotations, accurate mass search results, and quality metrics from untargeted metabolomics workflows. This skill bridges raw peak detection and comprehensive data archival, enabling reproducible sharing and downstream analysis of metabolite identifications.

## When to use

Apply this skill after completing peak detection, MS1 feature picking, and accurate mass database search (e.g., against HMDB) on FIA-MS or LC-MS(/MS) data. Use it when you need to serialize feature lists, compound annotations (molecular formulas, HMDB IDs, structural metadata), and mass error tolerances into a portable, standards-compliant format for reporting, archival, or integration with other metabolomics pipelines.

## When NOT to use

- Input peaks have not been searched against a reference database or lack compound annotation; mzTab requires populated SMA (small molecule) features with accession identifiers.
- Data originates from targeted or SRM/MRM workflows where you already have pre-defined transition lists; mzTab is optimized for discovery and untargeted annotation, not scheduled transitions.
- Mass search results are ambiguous or unresolved (e.g., multiple equally ranked HMDB matches without tie-breaking); mzTab does not resolve rank ambiguity; filter or annotate first.

## Inputs

- Detected MS1 peaks (m/z, retention time, intensity values)
- Accurate mass search results (matched HMDB compound IDs, molecular formulas, mass error per match)
- Ion adduct assignment (positive_adducts.tsv, negative_adducts.tsv)
- HMDB mapping metadata (HMDBMappingFile.tsv, HMDB2StructMapping.tsv)
- Workflow parameters (mass tolerance in ppm, resolution, time range)

## Outputs

- mzTab file (.mzTab) containing feature list and mass search annotations
- Structured metadata section (MTD) with acquisition and software details
- Small molecule feature table (SMA) with compound identifiers and quality metrics

## How to apply

After executing SEARCH_ACCURATE_MASS against HMDB mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv) with configured mass error tolerance and ion adducts (positive_adducts.tsv, negative_adducts.tsv), collect the annotated peak list (feature m/z, retention time, intensity, assigned compound identifiers) and mass search metadata (mass error per feature, adduct assignment confidence). Assemble these into mzTab format by populating the MTD (metadata) section with acquisition parameters, software version, and search settings; the PSM or PEP section with individual peak annotations; and the SMA (small molecule feature) section with feature-level summaries. Validate the mzTab schema compliance and write to a .mzTab file for storage and downstream consumption.

## Related tools

- **SmartPeak** (Orchestrates peak detection, accurate mass search, and mzTab assembly workflow end-to-end) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (Command-line interface to execute mzTab generation workflow without GUI) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (Underlying toolkit providing mzTab writers and metabolite search algorithms)
- **pyOpenMS** (Python API for parsing and post-processing mzTab output files)
- **BFAIR** (Provides downstream untargeted FIA-MS analysis and integration of mzTab results into metabolic models) — https://github.com/AutoFlowResearch/BFAIR

## Examples

```
docker run --rm -ti -v C:/data:/sample-data autoflowresearch/smartpeak-cli:latest bash -c "SmartPeakCLI --input /sample-data/FIAMS_config.xml --output /sample-data/results.mzTab"
```

## Evaluation signals

- mzTab file validates against mzTab schema (MTD, SMA, PSM sections present and well-formed)
- All detected peaks from MS1 feature picking appear in the SMA section with m/z, retention time, and intensity values preserved
- Accurate mass search annotations are populated: each matched feature includes HMDB accession ID, molecular formula, mass error in ppm, and adduct assignment
- Mass error per annotated feature falls within the configured tolerance window (e.g., ±5 ppm for 12,000 resolution)
- Metadata section (MTD) includes software name/version (SmartPeak), acquisition parameters (max_mz=1500, resolution=12000, time range 0–30 s), and database reference (HMDB version)

## Limitations

- mzTab generation depends on prior successful accurate mass search; if no peaks match HMDB with confidence above threshold, the SMA section will be sparse or empty.
- Mass error tolerance and ion adduct configuration must be set before search; post-hoc relaxation of tolerance or addition of new adducts requires re-running the SEARCH_ACCURATE_MASS step.
- Ambiguous or low-confidence matches (multiple HMDB compounds with overlapping m/z windows) are not automatically ranked or filtered; filtering or manual curation may be needed for interpretation.
- mzTab output does not include chromatographic peak shape or integration quality metrics beyond intensity; refer to SmartPeak's native reporting (e.g., QC plots) for peak quality assessment.

## Evidence

- [other] Execute accurate mass search against the HMDB database using the mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv) and specified ion adducts (positive_adducts.tsv, negative_adducts.tsv) with the configured mass error tolerance.: "Execute accurate mass search against the HMDB database using the mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv) and specified ion adducts (positive_adducts.tsv, negative_adducts.tsv)"
- [other] Annotate detected peaks with HMDB compound identifiers, molecular formulas, and structural metadata. Assemble results into mzTab format containing the feature list and mass search annotations, then store the mzTab output file.: "Annotate detected peaks with HMDB compound identifiers, molecular formulas, and structural metadata. Assemble results into mzTab format containing the feature list and mass search annotations, then"
- [other] SmartPeak automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting, which collectively support the generation of comprehensive data summaries including feature annotations and quality metrics.: "SmartPeak automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting, which collectively support the generation of comprehensive data"
- [readme] The software is based on the OpenMS toolkit.: "The software is based on the OpenMS toolkit."
- [readme] These files can be parsed and processed by the pyOpenMS Python package: "These files can be parsed and processed by the pyOpenMS Python package"
