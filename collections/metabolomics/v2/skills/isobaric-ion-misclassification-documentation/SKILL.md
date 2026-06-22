---
name: isobaric-ion-misclassification-documentation
description: Use when after matrix annotation has been performed on mass spectrometry imaging (MSI) data when you need to identify and document ions whose m/z values overlap with or are isobaric to other peaks, creating risk of false positive or false negative matrix assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - rMSIcleanup
  - R
  - rMSI
  - rMSIproc
derived_from:
- doi: 10.1186/s13321-020-00449-0
  title: ''
evidence_spans:
- rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data
- rMSIcleanup is an open-source R package
- devtools::install_github("prafols/rMSI", ref = "0.8")
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rmsicleanup_ms_imaging_matrix_peak_annot_cq
    doi: 10.1186/s13321-020-00449-0
    title: ''
  dedup_kept_from: coll_rmsicleanup_ms_imaging_matrix_peak_annot_cq
schema_version: 0.2.0
---

# isobaric-ion-misclassification-documentation

## Summary

Document and visualize potential misclassification risks arising from overlapping or isobaric peaks in matrix-related ion annotation workflows. This skill generates transparent, per-annotation reports that justify classification decisions by flagging peak overlap status and spatial distribution patterns.

## When to use

Apply this skill after matrix annotation has been performed on mass spectrometry imaging (MSI) data when you need to identify and document ions whose m/z values overlap with or are isobaric to other peaks, creating risk of false positive or false negative matrix assignments. Specifically use it when the annotation output requires transparent justification for stakeholders, or when downstream data cleaning decisions depend on understanding which annotations carry isobaric ambiguity.

## When NOT to use

- Input annotation has already been manually curated and validated by domain experts; use this skill during initial annotation QC, not post-curation review.
- MSI data lacks sufficient spatial resolution or pixel count to meaningfully assess spatial distribution patterns as a discriminator for matrix assignment.
- Peak mass accuracy or mass resolution is too poor to resolve isobaric ions reliably; document this limitation instead of generating false-confidence reports.

## Inputs

- rMSIcleanup annotation output (matrix classification results)
- Peak matrix in rMSIproc format (.zip)
- Processed MSI dataset (.tar)
- Chemical formula database or annotation lookup

## Outputs

- Multi-panel visual report PDF with per-annotation documentation
- Per-ion classification justification records (spatial map, formula, overlap status, rationale)
- Compiled isobaric risk inventory artifact

## How to apply

Load the annotation matrix and classified ion data from rMSIcleanup output along with the full MSI dataset. For each annotated ion, retrieve its chemical formula, m/z value, and spatial distribution pattern. Use the overlapping peak detection feature to systematically identify isobaric peaks and document their co-occurrence within the spectral window. For each flagged annotation, generate a multi-panel visual report showing: the ion's spatial map across the tissue section, its chemical formula identifier, peak overlap status (overlapped vs. isolated), and explicit classification justification (matrix vs. non-matrix). Compile all per-annotation reports into a single transparent artifact that allows downstream users to assess confidence in each annotation decision based on isobaric risk.

## Related tools

- **rMSIcleanup** (Performs matrix annotation and provides overlapping peak detection feature; generates the annotation output that is documented by this skill) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Loads and provides access to processed MSI datasets required to retrieve spatial distribution patterns and peak data) — https://github.com/prafols/rMSI
- **rMSIproc** (Loads and stores peak matrix in rMSIproc format; provides data serialization for annotation workflow input/output) — https://github.com/prafols/rMSIproc
- **R** (Execution environment for rMSIcleanup functions and report generation)

## Examples

```
rMSIcleanup::generate_pdf_report(results, pks, full, "test", folder="/home/user/")
```

## Evaluation signals

- Each annotated ion in the report is flagged with explicit overlap status (overlapped vs. isolated) based on detected isobaric peaks within the spectral window.
- Spatial distribution maps for each ion are present and visually distinct from matrix-only ions (matrix annotations should show uniform tissue coverage; analyte annotations should show localized regions).
- Classification justification text for each annotation explicitly references the rationale (e.g., 'classified as matrix due to ubiquitous spatial distribution despite m/z overlap with candidate analyte X').
- No ion lacking isobaric detection has been marked as 'no overlap detected' without evidence from the overlapping peak detection feature.
- All ions present in the input annotation matrix are represented in the output report; no annotations are silently omitted.

## Limitations

- Overlapping peak detection relies on mass accuracy and resolving power of the instrument; data acquired at low mass resolution may fail to distinguish true isobaric ions from noise or artifacts.
- Spatial distribution discrimination assumes biological/chemical prior knowledge (e.g., that matrix ions distribute uniformly and analyte ions cluster regionally); this assumption may not hold for all sample types or matrix compositions.
- Visual report generation depends on data availability; missing or corrupted spatial maps for specific m/z values will result in incomplete per-annotation documentation.
- The skill documents but does not automatically resolve isobaric ambiguity; final annotation correctness depends on domain expert review of the justifications.

## Evidence

- [intro] The algorithm incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions.: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [intro] The package generates a visual report to transparently justify each annotation.: "the package generates a visual report to transparently justify each annotation"
- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related.: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
- [other] For each annotated ion, retrieve its chemical formula, m/z value, and spatial distribution pattern across the MSI dataset. Identify overlapping or isobaric peaks using the overlapping peak detection feature to document potential misclassification risks.: "For each annotated ion, retrieve its chemical formula, m/z value, and spatial distribution pattern across the MSI dataset. Identify overlapping or isobaric peaks using the overlapping peak detection"
- [other] Generate a multi-panel visual report for each annotation showing: ion spatial map, chemical formula identifier, peak overlap status, and classification justification (matrix vs. non-matrix).: "Generate a multi-panel visual report for each annotation showing: ion spatial map, chemical formula identifier, peak overlap status, and classification justification (matrix vs. non-matrix)."
