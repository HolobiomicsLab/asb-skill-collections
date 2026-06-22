---
name: adduct-based-feature-consolidation
description: Use when after accurate mass searching has assigned multiple detected m/z features to the same metabolite via positive and negative adduct libraries, and before sample-level feature merging.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - SmartPeak
  - SmartPeakGUI
  - SmartPeakCLI
  - OpenMS
  - pyOpenMS
  - BFAIR
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

# adduct-based-feature-consolidation

## Summary

Merge and consolidate multiply-charged and adducted molecular ions detected from the same compound into a single unified feature record. This skill is essential in untargeted metabolomics workflows to reduce redundancy and improve downstream quantification and annotation accuracy.

## When to use

Apply this skill after accurate mass searching has assigned multiple detected m/z features to the same metabolite via positive and negative adduct libraries, and before sample-level feature merging. Typical triggers: (1) a single compound appears as multiple m/z values differing by known adduct mass deltas (e.g., [M+H]+ and [M+Na]+, [M-H]− adducts); (2) quality-filtered features remain in a multi-injection dataset; (3) background-corrected feature lists are ready for consolidation.

## When NOT to use

- Input is a targeted assay with predetermined transitions—adduct merging is unnecessary when monitoring specific m/z windows.
- Feature table is already deduplicated or comes from a tool that has already resolved adducts.
- Accurate mass search has not yet been performed or adduct library assignments are unavailable or unreliable.

## Inputs

- Accurate-mass-searched feature list (mzTab or internal feature table format) with HMDB annotations and adduct assignments
- HMDB mapping file with positive and negative adduct library definitions
- Background-corrected feature list (post-FILTER_FEATURES_BACKGROUND_INTERFERENCES)

## Outputs

- Consolidated feature list with one entry per unique compound per sample (adducts merged)
- Merged feature metavalues (e.g., representative m/z, aggregated intensity, charge state)

## How to apply

After SEARCH_ACCURATE_MASS has mapped detected m/z features to compounds using HMDB and adduct libraries (positive and negative), invoke MERGE_FEATURES to group all m/z entries belonging to the same compound and charge state into a single consolidated feature entry. The merge operation collapses redundant adducted signals by selecting a representative m/z (typically the most intense or most reliable detection) and aggregating or averaging intensity, quality metrics, and metavalues across the adduct cluster. This step is critical because multiple adducts of the same compound—especially common in FIAMS FullScan workflows—would otherwise inflate feature counts and complicate quantification. Apply MERGE_FEATURES before MERGE_INJECTIONS to ensure each compound is represented once per injection, not once per adduct. Verify consolidation by checking that the output feature table has fewer entries than the input and that no compound appears with multiple m/z assignments in the same sample.

## Related tools

- **SmartPeak** (Orchestrates MERGE_FEATURES as a configurable workflow step within FIAMS FullScan Unknowns and other semi-targeted analyses) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (Underlying toolkit providing feature merging and adduct-aware algorithms) — https://github.com/OpenMS/OpenMS
- **pyOpenMS** (Python interface for parsing and programmatically manipulating merged feature files)
- **BFAIR** (Post-processing and analysis of merged untargeted FIA-MS metabolomics results) — https://github.com/AutoFlowResearch/BFAIR

## Evaluation signals

- Output feature count is lower than input count (adducts successfully consolidated).
- Each unique compound (by HMDB ID or inChIKey) appears exactly once per sample in the merged table.
- No feature in the output carries conflicting adduct annotations or multiple m/z values for the same charge state.
- Aggregated intensity and signal-to-noise ratio of merged features are consistent with the original strongest adduct signal.
- Downstream MERGE_INJECTIONS step completes without duplicate-compound errors.

## Limitations

- Adduct consolidation depends critically on accurate mass search quality; unreliable or incomplete HMDB annotations will produce incomplete or incorrect merges.
- Compounds that form multiple stable adducts with similar intensity may lose information if only one representative m/z is retained; consider retaining intensity-weighted consensus m/z or storing all adduct m/z values as metadata.
- SmartPeak's MERGE_FEATURES workflow step does not currently expose user-tunable parameters for adduct mass tolerance or selection criteria, limiting customization for non-standard adducts or unusual ionization regimes.

## Evidence

- [methods] Perform accurate mass search against HMDB mapping files using SEARCH_ACCURATE_MASS with positive and negative adduct libraries.: "Perform accurate mass search against HMDB mapping files using SEARCH_ACCURATE_MASS with positive and negative adduct libraries."
- [methods] Merge adducts of the same compound using MERGE_FEATURES.: "Merge adducts of the same compound using MERGE_FEATURES."
- [intro] The workflow automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting.: "The workflow automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting."
- [readme] SmartPeak is an application that encapsulates advanced algorithms to enable fast, accurate, and automated processing of CE-, GC- and LC-MS(/MS) data, and HPLC data for targeted and semi-targeted metabolomics, lipidomics, and fluxomics experiments.: "SmartPeak is an application that encapsulates advanced algorithms to enable fast, accurate, and automated processing of CE-, GC- and LC-MS(/MS) data, and HPLC data for targeted and semi-targeted"
- [readme] Tools for analyzing untargeted FIA-MS metabolomics data: "Tools for analyzing untargeted FIA-MS metabolomics data"
