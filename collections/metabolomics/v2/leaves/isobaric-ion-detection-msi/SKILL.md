---
name: isobaric-ion-detection-msi
description: Use when you have loaded MSI data with an extracted peak list and need
  to annotate matrix-related signals, particularly when the dataset may contain isobaric
  ions or peaks with overlapping spatial distributions that could be misclassified
  during downstream annotation filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3371
  tools:
  - rMSIcleanup
  - rMSI
  - R
  - rMSIproc
  techniques:
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-020-00449-0
  title: ''
evidence_spans:
- rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI
  data
- devtools::install_github("prafols/rMSI", ref = "0.8")
- rMSIcleanup is an open-source R package
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

# Isobaric Ion Detection in Mass Spectrometry Imaging

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identifies and flags ions with identical or near-identical m/z values (isobaric ions) and overlapping spatial distributions in MSI data to prevent their misclassification during matrix annotation. This skill is essential when processing MSI datasets where isobaric peaks can be erroneously assigned to matrix or analyte classes.

## When to use

Apply this skill when you have loaded MSI data with an extracted peak list and need to annotate matrix-related signals, particularly when the dataset may contain isobaric ions or peaks with overlapping spatial distributions that could be misclassified during downstream annotation filtering. Use it before generating a final annotation report to ensure confidence in peak identity assignments.

## When NOT to use

- Input peak list already contains pre-validated isobaric annotations from an orthogonal method (e.g., high-resolution tandem MS or exact mass database matching).
- Working with data from instruments with inherently high mass resolution (>100,000) where isobaric overlap is negligible; consider whether the overhead of detection justifies the use case.
- Data has not been processed into rMSIproc format; the skill requires standardized input file types (.tar and .zip) and spatial distribution matrices.

## Inputs

- MSI data in rMSI format (.tar processed data)
- Peak list in rMSIproc format (.zip peak matrix)
- Peak identifiers (m/z values and spatial coordinates)

## Outputs

- Binary overlap flag table (CSV: peak identifiers mapped to overlap status)
- Filtered peak list with isobaric annotations
- Visual annotation report justifying overlap classifications

## How to apply

Load the MSI data and peak list into R using rMSI and rMSIproc, then apply the overlapping peak detection algorithm in rMSIcleanup to identify candidate peaks with identical or near-identical m/z values and peaks with overlapping spatial distributions across the tissue image. The algorithm considers both chemical formula and spatial distribution patterns to distinguish genuine isobaric ions from unique peaks. Generate binary overlap flags for each candidate peak (flagged=overlapped, unflagged=unique) and export the overlap flag table as a structured CSV file mapping peak identifiers to overlap status. Use these flags to filter annotation results downstream and prevent misassignment of overlapped ions to matrix or analyte categories.

## Related tools

- **rMSIcleanup** (Executes the overlapping peak detection algorithm and generates overlap flags and visual reports) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Loads and manages MSI data objects and spatial image matrices required for overlap detection) — https://github.com/prafols/rMSI
- **rMSIproc** (Loads and stores peak matrix files in standardized format and processes raw imzML into rMSI-compatible format) — https://github.com/prafols/rMSIproc
- **R** (Runtime environment for executing rMSIcleanup functions and manipulating overlap flag tables)

## Examples

```
results <- rMSIcleanup::annotate_matrix(pks, "Ag1", full); overlap_flags <- results$overlap_table; write.csv(overlap_flags, "overlap_flags.csv", row.names=FALSE)
```

## Evaluation signals

- Overlap flag table contains binary entries (0/1 or FALSE/TRUE) for every peak in the input list with no missing values.
- Flagged peaks exhibit either identical m/z values (within instrument mass accuracy tolerance) or correlated spatial intensity patterns across the tissue image; unflagged peaks show distinct m/z or orthogonal spatial distributions.
- Generated PDF report visually displays overlap flags superimposed on tissue heatmaps and includes chemical formula and spatial distribution justifications for each classification decision.
- Downstream annotation results show reduced or eliminated misclassification of overlapped ions into matrix or analyte categories compared to runs without overlap filtering.
- CSV export format matches expected schema: peak_id | m/z | overlap_flag | spatial_correlation_score (where applicable).

## Limitations

- The algorithm's overlap detection accuracy depends on peak picking quality upstream; poorly resolved or noisy peaks may generate false positive or false negative overlap flags.
- Spatial distribution analysis assumes uniform tissue sectioning and imaging resolution; regions with variable pixel density or sampling artifacts may produce unreliable overlap correlations.
- The skill requires conversion of raw imzML data to rMSIproc format, adding preprocessing overhead; compatibility is limited to this specific ecosystem and does not natively support other MSI formats (e.g., Bruker .d, Waters .raw).
- No quantitative threshold or p-value is provided in the article for determining the overlap correlation coefficient cutoff; users must rely on visual inspection of the generated report to validate flag assignments.

## Evidence

- [intro] The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [other] Apply overlapping peak detection algorithm in rMSIcleanup to identify candidate peaks with identical or near-identical m/z values (isobaric ions) and peaks with overlapping spatial distributions across the tissue image.: "Apply overlapping peak detection algorithm in rMSIcleanup to identify candidate peaks with identical or near-identical m/z values (isobaric ions) and peaks with overlapping spatial distributions"
- [other] Generate binary overlap flags for each candidate peak (flagged=overlapped, unflagged=unique) and export overlap flag table as a structured CSV file mapping peak identifiers to overlap status: "Generate binary overlap flags for each candidate peak (flagged=overlapped, unflagged=unique). 4. Export overlap flag table as a structured CSV file mapping peak identifiers to overlap status"
- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
- [readme] rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data. The algorithm incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions.: "rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data. The algorithm incorporates an overlapping peak detection feature to prevent misclassification of overlapped or"
