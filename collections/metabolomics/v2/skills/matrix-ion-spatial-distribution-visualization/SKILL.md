---
name: matrix-ion-spatial-distribution-visualization
description: Use when after rMSIcleanup has classified ions as matrix-related or non-matrix, and you need to audit, validate, or communicate the annotation decisions. Use it when overlapping or isobaric peaks are present in the dataset and you must document misclassification risks per annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3365
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

# matrix-ion-spatial-distribution-visualization

## Summary

Generate multi-panel visual reports that display ion spatial maps alongside chemical formula identifiers, peak overlap status, and classification justification to transparently document matrix-related annotations in MSI datasets. This skill enables practitioners to inspect and validate the rationale behind each matrix vs. non-matrix ion classification decision.

## When to use

Apply this skill after rMSIcleanup has classified ions as matrix-related or non-matrix, and you need to audit, validate, or communicate the annotation decisions. Use it when overlapping or isobaric peaks are present in the dataset and you must document misclassification risks per annotation. Also use it when preparing publishable or review-ready documentation that requires transparent justification of ion filtering choices.

## When NOT to use

- Input MSI data has not yet been processed into rMSIproc format or loaded into rMSI objects; preprocessing must complete first.
- No matrix-related annotations have been computed; rMSIcleanup::annotate_matrix() has not been run or produced no classifications.
- The goal is exploratory peak discovery rather than validation and documentation of pre-existing classifications.

## Inputs

- rMSIcleanup annotation results object (from annotate_matrix output)
- Peak matrix in rMSIproc format (.zip file)
- Processed MSI dataset (rMSI .tar file containing m/z values, spatial coordinates, and pixel intensities)
- Overlapping peak detection results (peak conflict list)

## Outputs

- Multi-panel visual report PDF with per-ion annotation justifications
- Compiled transparency documentation artifact (one report per classified ion)
- Ion spatial maps with classification labels and overlap flags

## How to apply

Load the annotation matrix and classified ion data output from rMSIcleanup::annotate_matrix(). For each annotated ion, retrieve its chemical formula, m/z value, and spatial distribution pattern across the MSI dataset. Use the overlapping peak detection feature to identify and flag isobaric or overlapping peaks that pose misclassification risks for that specific ion. Then construct a multi-panel figure for each annotation showing: (1) the ion's spatial map across the tissue section, (2) its chemical formula and m/z identifier, (3) peak overlap status and any conflicting assignments, and (4) the classification justification (matrix vs. non-matrix reasoning). Compile all per-annotation reports into a single PDF or document artifact. The spatial distribution pattern—whether the ion co-localizes uniformly with matrix signal or shows tissue-specific localization—is a primary decision input for classification justification.

## Related tools

- **rMSIcleanup** (Executes matrix-related ion annotation and generates the visual report component that justifies each classification via generate_pdf_report()) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Loads and manages processed MSI data (.tar files) and provides spatial distribution data for each ion used in report visualization) — https://github.com/prafols/rMSI
- **rMSIproc** (Loads and stores peak matrices (.zip files) containing ion m/z, intensities, and chemical formula annotations) — https://github.com/prafols/rMSIproc
- **R** (Runtime environment for executing rMSIcleanup visualization and report generation functions)

## Examples

```
rMSIcleanup::generate_pdf_report(results, pks, full, "matrix_annotations", folder="./reports/")
```

## Evaluation signals

- Each ion in the report has a corresponding spatial map showing pixel-level intensity distribution across tissue coordinates.
- Chemical formula, m/z value, and peak overlap status are accurately displayed for every annotated ion without omissions.
- Classification justification (matrix vs. non-matrix) is explicitly stated and grounded in the spatial distribution pattern and overlap detection results for each ion.
- Isobaric or overlapping peaks are flagged and their misclassification risk is documented in the report.
- The compiled PDF or transparency artifact contains one multi-panel visualization per classified ion and is machine-readable or audit-traceable.

## Limitations

- Report generation relies on correct execution of rMSIcleanup::annotate_matrix(); misclassifications upstream will be visualized but not corrected by the report.
- Overlapping peak detection accuracy depends on mass resolution and spectral quality of the input MSI data; poor resolution may lead to undetected isobaric conflicts.
- Visual report generation assumes chemical formula annotations are already present in the peak matrix; missing or incorrect formula data will result in incomplete justifications.
- The skill documents classification decisions but does not programmatically re-classify or filter ions; it is a transparency and audit tool, not a correction mechanism.

## Evidence

- [intro] the package generates a visual report to transparently justify each annotation: "the package generates a visual report to transparently justify each annotation"
- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
- [intro] The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [other] Generate a multi-panel visual report for each annotation showing: ion spatial map, chemical formula identifier, peak overlap status, and classification justification (matrix vs. non-matrix).: "Generate a multi-panel visual report for each annotation showing: ion spatial map, chemical formula identifier, peak overlap status, and classification justification (matrix vs. non-matrix)."
- [readme] rMSIcleanup::generate_pdf_report(results,pks,full,"test",folder="/home/gbaquer/"): "rMSIcleanup::generate_pdf_report(results,pks,full,"test",folder="/home/gbaquer/")"
