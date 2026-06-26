---
name: overlapping-peak-detection-interpretation
description: Use when annotating matrix-related signals in MSI datasets where chemical
  formulas or spatial distributions alone are ambiguous, or when multiple ions share
  nominal m/z values (isobaric peaks).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - rMSIcleanup
  - R
  - rMSI
  - rMSIproc
  techniques:
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-020-00449-0
  title: ''
evidence_spans:
- rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI
  data
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00449-0
  all_source_dois:
  - 10.1186/s13321-020-00449-0
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# overlapping-peak-detection-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Detect and document overlapping or isobaric peaks in mass spectrometry imaging data to prevent misclassification of matrix-related ions and transparently justify annotation decisions. This skill interprets overlap status as part of the classification rationale for each m/z feature.

## When to use

Apply this skill when annotating matrix-related signals in MSI datasets where chemical formulas or spatial distributions alone are ambiguous, or when multiple ions share nominal m/z values (isobaric peaks). Use it to flag potential misclassification risks before generating the final transparent annotation report, especially in silver-assisted or other matrix-assisted ionization workflows where matrix and analyte ions may overlap in mass space or spatial footprint.

## When NOT to use

- Input peak matrix is already deconvolved or has been pre-filtered to remove overlaps—overlapping peak detection would be redundant.
- MSI data has insufficient mass resolution (e.g., low-resolution TOF) such that all nominal m/z bins are effectively resolved and isobaric confusion is minimal.
- The analysis goal is exploratory visualization only and does not require formal justification of annotation confidence or misclassification risk.

## Inputs

- Annotation matrix with classified ion labels (matrix vs. non-matrix) from rMSIcleanup::annotate_matrix()
- Peak matrix in rMSIproc format (.zip file containing m/z, intensity, and spatial pixel coordinates)
- Processed MSI dataset (.tar file with full spatial distribution and chemical formula information)
- Chemical formula and m/z metadata for each annotated ion

## Outputs

- Per-annotation overlap status record (presence/absence of isobaric or co-localized peaks)
- Classification justification documentation including peak overlap rationale for each ion
- Multi-panel visual report with ion spatial map, peak overlap status, and misclassification risk flag
- Transparent annotation artifact (PDF or structured report) compiled from all per-annotation overlap assessments

## How to apply

For each annotated ion in the rMSIcleanup workflow, retrieve its chemical formula, m/z value, and spatial distribution pattern across the MSI dataset. Use rMSIcleanup's overlapping peak detection feature to identify isobaric or co-localized peaks that could confound classification. Document the peak overlap status (present/absent) for each annotation, capturing both nominal m/z collisions and spatial co-occurrence patterns. Include this overlap status explicitly in the per-annotation justification record. Rank or flag annotations with detected overlaps as higher-risk classifications that require manual review or additional evidence (e.g., high-resolution m/z, orthogonal spatial signatures) before finalizing matrix removal. The rationale is that transparent documentation of overlap prevents silent misclassification and allows downstream users to weight annotations by confidence.

## Related tools

- **rMSIcleanup** (Primary tool; provides the overlapping peak detection feature and integration into annotation workflow) — https://github.com/gbaquer/rMSIcleanup
- **rMSIproc** (Data preprocessing and format management; loads/stores peak matrix in required format) — https://github.com/prafols/rMSIproc
- **rMSI** (MSI data loading and spatial distribution querying for overlap detection) — https://github.com/prafols/rMSI
- **R** (Execution environment for rMSIcleanup and dependent packages)

## Examples

```
rMSIcleanup::annotate_matrix(pks, "Ag1", full); rMSIcleanup::generate_pdf_report(results, pks, full, "test_with_overlaps", folder="/home/user/")
```

## Evaluation signals

- Overlap status (present/absent) is recorded and exported for every annotated ion in the justification artifact.
- Overlapping peaks are visibly flagged or highlighted in the multi-panel visual report, distinguishing high-overlap from non-overlapping annotations.
- Classification rationale text explicitly mentions peak overlap status as part of the justification for matrix vs. non-matrix decision.
- Ions with detected overlaps are tagged with a misclassification risk level (low/medium/high) and listed separately for manual review.
- The generated PDF report includes a summary table or histogram of overlap prevalence across the dataset, enabling meta-assessment of annotation confidence.

## Limitations

- Overlapping peak detection effectiveness depends on mass resolution and accuracy of the input m/z calibration; low-resolution data may not resolve true isobaric peaks.
- Spatial overlap detection relies on pixel-level co-localization; at coarse spatial sampling or high feature abundance, false-positive overlap signals may inflate risk flags.
- The README and article do not specify the exact overlap detection algorithm (e.g., m/z tolerance window, spatial overlap threshold), limiting reproducibility and tuning options for specialized applications.
- Overlapping peak detection output is presented as binary (overlap present/absent) rather than a continuous confidence metric, which may obscure borderline or ambiguous cases.

## Evidence

- [intro] The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [other] For each annotated ion, retrieve its chemical formula, m/z value, and spatial distribution pattern across the MSI dataset. Identify overlapping or isobaric peaks using the overlapping peak detection feature to document potential misclassification risks.: "For each annotated ion, retrieve its chemical formula, m/z value, and spatial distribution pattern across the MSI dataset. Identify overlapping or isobaric peaks using the overlapping peak detection"
- [intro] the package generates a visual report to transparently justify each annotation: "the package generates a visual report to transparently justify each annotation"
- [other] Generate a multi-panel visual report for each annotation showing: ion spatial map, chemical formula identifier, peak overlap status, and classification justification (matrix vs. non-matrix).: "Generate a multi-panel visual report for each annotation showing: ion spatial map, chemical formula identifier, peak overlap status, and classification justification"
- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
