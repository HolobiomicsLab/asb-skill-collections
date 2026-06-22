---
name: mass-spectrometry-feature-grouping
description: Use when after raw data processing and feature extraction (e.g., via XCMS, OpenMS, or enviPick) when you have detected features across multiple LC-MS or GC-MS analyses and need to identify which features represent the same chemical across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3172
  tools:
  - patRoon
  - XCMS
  - OpenMS
  - enviPick
  - KPIC2
  - Python
  - PFΔScreen
  - pyOpenMS
  - pandas
  - MsFeatures
  - xcms
  - faahKO
  techniques:
  - LC-MS
  - GC-MS
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-020-00477-w
  title: patRoon
- doi: 10.1007/s00216-023-05070-2
  title: ''
- doi: 10.1021/ac051437y
  title: ''
evidence_spans:
- The `generateTPs` function is used to obtain TPs for a particular set of parents.
- componTP <- generateComponents(algorithm = "tp",
- PFΔScreen is an open-source Python based non-target screening software tool
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package with additional functionality being implemented
- VignetteDepends{xcms,BiocStyle,faahKO,pheatmap,MsFeatures}
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_patroon_cq
    doi: 10.1186/s13321-020-00477-w
    title: patRoon
  - build: coll_pfdeltascreen_cq
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  - build: coll_xcms_cq
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_patroon_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00477-w
  all_source_dois:
  - 10.1186/s13321-020-00477-w
  - 10.1007/s00216-023-05070-2
  - 10.1021/ac051437y
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-feature-grouping

## Summary

Feature grouping aggregates detected mass spectrometry features across multiple analyses by retention time, mass-to-charge ratio, and chromatographic alignment to create a unified feature table. This is a foundational step in non-target analysis that enables downstream annotation, suspect screening, and transformation product detection.

## When to use

Apply this skill after raw data processing and feature extraction (e.g., via XCMS, OpenMS, or enviPick) when you have detected features across multiple LC-MS or GC-MS analyses and need to identify which features represent the same chemical across samples. This is essential before suspect screening, formula annotation, or componentization.

## When NOT to use

- Input is already a pre-grouped feature table from an external tool not integrated with patRoon; skip to suspect screening or annotation.
- Only single-analysis data available; feature grouping is not meaningful without cross-sample alignment.
- Raw mass spectrometry data has not yet been processed through peak detection and feature extraction.

## Inputs

- Raw extracted features from single analyses (featureLists with m/z, retention time, intensity)
- Analysis metadata including file names and optional sample annotations (treatment group, class, replicate)
- Feature extraction algorithm output (XCMS, OpenMS, enviPick, KPIC2, or similar)

## Outputs

- Feature group object (fGroups) with aligned m/z and retention time across analyses
- Consensus feature table mapping feature IDs to chemical properties (m/z, retention time, intensity)
- Sample-by-feature intensity matrix ready for downstream annotation and screening

## How to apply

Load extracted features from all analyses into patRoon using the appropriate feature extraction algorithm. Perform retention time alignment across analyses using the algorithm's built-in grouping function (e.g., XCMS's density-based or mzMatch-style grouping), which uses mass tolerance (typically 2–8 ppm for high-resolution instruments) and retention time window parameters. The grouping function creates a feature group object (fGroups) mapping each detected feature to a consensus m/z and retention time. Optionally filter grouped features by sample metadata (e.g., treatment group) using sample annotations. Validate output by inspecting the fGroups object structure, confirming feature counts per analysis match expected values, and verifying retention time consistency within each group. Post-process with filters for intensity thresholds, blank removal, or replication criteria to prioritize high-confidence features.

## Related tools

- **XCMS** (Peak detection and feature grouping across analyses using density-based or mzMatch algorithms) — https://github.com/sneumann/xcms
- **OpenMS** (Alternative feature extraction and grouping via high-resolution mass spectrometry algorithms) — http://openms.de/
- **enviPick** (Environmental mass spectrometry feature detection and grouping)
- **KPIC2** (Alternative feature extraction method compatible with patRoon grouping workflows)
- **patRoon** (Core framework providing consistent interface to feature grouping and cross-sample alignment) — https://github.com/rickhelmus/patRoon

## Examples

```
fGroups <- groupFeatures(featureLists, method = "xcms", mzTol = 5, rtTol = 30); fGroupsF <- filter(fGroups, blankRatio = 0.5, intensity = 1000)
```

## Evaluation signals

- Feature group object (fGroups) is created successfully with no missing or null entries for consensus m/z, retention time, or intensity.
- Retention time consistency within each group meets the algorithm's tolerance window (e.g., <30 seconds for LC-MS); outliers indicate misalignment.
- Feature count per analysis matches expected values from raw feature extraction; unexpected drops suggest aggressive filtering or alignment failures.
- Intensity values are present and non-zero for all features across replicates; missing data indicates incomplete grouping.
- Downstream suspect screening or annotation shows expected hit rates for known standards or control compounds, confirming feature quality.

## Limitations

- Feature grouping accuracy depends on retention time reproducibility across analyses; poorly aligned chromatography (e.g., from instrumental drift) degrades grouping.
- Mass accuracy and resolution requirements scale with mass range; high-mass features (>500 Da) may require stricter ppm tolerances.
- Isomeric compounds with identical m/z and similar retention time cannot be distinguished by grouping alone; downstream MS/MS or other modality is required.
- Samples with large retention time shifts (e.g., from different batches or environmental conditions) may require algorithm-specific parameter tuning or separate grouping.
- Feature grouping does not inherently handle adducts, isotopes, or in-source fragments; componentization is a separate step for resolving these relationships.

## Evidence

- [other] Finding from article methods section: "Finding of features across analyses and grouping them across analyses"
- [other] Workflow step definition: "Feature extraction: Finding features and grouping them across analyses."
- [readme] Algorithm specificity in README: "Feature extraction | Finding features and grouping them across analyses. | Native (`piek`, `greedy`), [XCMS], [OpenMS], [enviPick], [DataAnalysis], [KPIC2], [SIRIUS], [SAFD]"
- [other] Retention time and mass tolerance context: "pSet <- list(method = "centWave", ppm = c(2, 8))"
- [other] Post-processing and filtering: "Data clean-up & prioritization | Filters for blanks, replicates, intensity thresholds, neutral losses, annotation scores, identification levels and many more."
