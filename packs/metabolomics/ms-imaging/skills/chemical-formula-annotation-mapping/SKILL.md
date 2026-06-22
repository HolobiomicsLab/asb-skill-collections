---
name: chemical-formula-annotation-mapping
description: 'Use when you have processed MSI peak data (in rMSIproc format) and need to distinguish matrix-related ions from analyte signals. Specifically: (1) you have a peak matrix with m/z values and spatial intensity maps; (2) you have a reference matrix identity (e.g., ''Ag1'' for silver);'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - rMSIcleanup
  - R
  - rMSI
  - rMSIproc
  techniques:
  - MS-imaging
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

# chemical-formula-annotation-mapping

## Summary

Map detected m/z peaks to chemical formulas and classify them as matrix-related or non-matrix ions by integrating chemical identity with spatial distribution patterns across the MSI dataset. This skill enables transparent, justified annotation of matrix signals in mass spectrometry imaging.

## When to use

Apply this skill when you have processed MSI peak data (in rMSIproc format) and need to distinguish matrix-related ions from analyte signals. Specifically: (1) you have a peak matrix with m/z values and spatial intensity maps; (2) you have a reference matrix identity (e.g., 'Ag1' for silver); (3) you want to document classification rationale to prevent downstream misidentification of matrix artifacts as genuine analyte peaks.

## When NOT to use

- Input is raw imzML without prior processing via rMSIproc—use ProcessWizard() first.
- Matrix identity is unknown or not specified—the algorithm requires a reference matrix formula to classify peaks.
- Peak matrix already manually curated or pre-filtered for matrix removal—redundant re-annotation may introduce inconsistency.

## Inputs

- Peak matrix file (.zip format from rMSIproc)
- Processed MSI dataset (.tar format from rMSI)
- Matrix identity string (e.g., 'Ag1' for silver)
- m/z values and spatial intensity maps per peak

## Outputs

- Annotation results object containing classification (matrix vs. non-matrix) for each peak
- Per-annotation visual report (multi-panel PDF) with spatial map, chemical formula, overlap status, and justification
- Compiled transparent documentation artifact
- Clean peak matrix (.zip) with matrix annotations removed (optional downstream step)

## How to apply

Load the peak matrix (.zip) and processed MSI data (.tar) using rMSIproc and rMSI. For each detected peak, retrieve its m/z value, chemical formula, and spatial distribution pattern across tissue pixels. Invoke rMSIcleanup's annotate_matrix() function with the matrix identity (e.g., 'Ag1' for silver-assisted LADI) as the reference. The algorithm integrates chemical formula matching with spatial distribution analysis: peaks matching known matrix formula(e) that show uniform spatial coverage are classified as matrix-related; peaks with identical or near-identical m/z (isobaric or overlapping) are flagged by the overlapping peak detection feature to document misclassification risk. Generate a visual report via generate_pdf_report() showing per-annotation justification (ion spatial map, formula identifier, peak overlap status, classification decision).

## Related tools

- **rMSIcleanup** (Primary annotation engine; executes annotate_matrix() to classify ions as matrix-related based on chemical formula and spatial distribution, and generate_pdf_report() to produce transparent justification per annotation.) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Loads and manages processed MSI data (.tar); provides spatial intensity maps and peak intensity data for formula matching and distribution analysis.) — https://github.com/prafols/rMSI
- **rMSIproc** (Loads peak matrix (.zip) and manages data I/O; provides ProcessWizard() for converting raw imzML to rMSIproc format if needed.) — https://github.com/prafols/rMSIproc
- **R** (Runtime environment and scripting language for rMSIcleanup and dependency packages.)

## Examples

```
results<-rMSIcleanup::annotate_matrix(pks,"Ag1",full); rMSIcleanup::generate_pdf_report(results,pks,full,"test",folder="/home/gbaquer/")
```

## Evaluation signals

- All detected peaks are assigned a classification (matrix vs. non-matrix) with no missing annotations.
- Visual report contains a multi-panel figure for each annotated ion, including spatial map, chemical formula label, and classification rationale text.
- Peaks flagged by overlapping peak detection feature are documented in the report with isobaric/overlap conflict noted.
- Spatial distribution of classified matrix peaks should show uniform or matrix-like coverage (not isolated to single regions or analyte-rich areas).
- Removed matrix peak matrix (.zip output) has fewer peaks than input, and removed peaks correspond exactly to those marked matrix-related in the report.

## Limitations

- Algorithm accuracy depends on accurate chemical formula prediction; m/z alone is insufficient without formula assignment.
- Overlapping peak detection may not resolve ambiguous cases where analyte and matrix signals truly co-localize spatially.
- Requires a priori knowledge of the matrix compound identity; automatic matrix detection is not addressed in this workflow.
- Visual report transparency is limited by peak count; very large datasets may produce unwieldy multi-hundred-page PDFs.

## Evidence

- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
- [intro] The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [intro] The package generates a visual report to transparently justify each annotation: "the package generates a visual report to transparently justify each annotation"
- [other] For each annotated ion, retrieve its chemical formula, m/z value, and spatial distribution pattern across the MSI dataset: "For each annotated ion, retrieve its chemical formula, m/z value, and spatial distribution pattern across the MSI dataset"
- [other] Generate a multi-panel visual report for each annotation showing: ion spatial map, chemical formula identifier, peak overlap status, and classification justification (matrix vs. non-matrix): "Generate a multi-panel visual report for each annotation showing: ion spatial map, chemical formula identifier, peak overlap status, and classification justification (matrix vs. non-matrix)"
- [readme] rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data.: "rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data."
- [readme] results<-rMSIcleanup::annotate_matrix(pks,"Ag1",full); rMSIcleanup::generate_pdf_report(results,pks,full,"test",folder="/home/gbaquer/"): "results<-rMSIcleanup::annotate_matrix(pks,"Ag1",full); rMSIcleanup::generate_pdf_report(results,pks,full,"test",folder="/home/gbaquer/")"
