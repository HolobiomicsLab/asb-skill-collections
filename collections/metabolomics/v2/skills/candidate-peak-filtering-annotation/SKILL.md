---
name: candidate-peak-filtering-annotation
description: Use when you have a peak list extracted from MSI data that includes candidate
  peaks with potential m/z overlap or spatial co-localization patterns across tissue
  images.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - rMSIcleanup
  - rMSI
  - R
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

# Overlapping Peak Detection and Isobaric Ion Flagging

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identifies and flags overlapped or isobaric ions (peaks with identical or near-identical m/z values and overlapping spatial distributions) to prevent their misclassification during matrix-related signal annotation in mass spectrometry imaging. This filtering step is essential for accurate peak annotation workflows where isobaric ambiguity could otherwise lead to false assignments.

## When to use

Apply this skill when you have a peak list extracted from MSI data that includes candidate peaks with potential m/z overlap or spatial co-localization patterns across tissue images. Use it before downstream matrix-related annotation filtering to ensure that overlapped or isobaric ions are explicitly flagged and excluded from or handled separately in annotation logic, particularly in silver-assisted laser desorption/ionization (AgLDI) or other matrix-intensive imaging modes.

## When NOT to use

- Input peak list is already manually curated or pre-filtered for isobaric overlap; redundant application.
- MSI data lacks spatial distribution information or was not processed through rMSI/rMSIproc; algorithm requires co-localization context.
- Peak matrix is not in rMSIproc format; conversion or re-processing is required first.

## Inputs

- Extracted peak list (peak matrix in rMSIproc .zip format)
- Processed MSI data (.tar file from rMSI containing spatial distribution)
- Candidate peak identifiers and m/z values

## Outputs

- Binary overlap flag table (CSV: peak identifier → overlap status)
- Flagged peak set (overlapped/isobaric ions)
- Unflagged peak set (unique peaks)

## How to apply

Load the extracted peak matrix and processed MSI data into R using rMSI and rMSIproc. Apply the overlapping peak detection algorithm in rMSIcleanup, which examines candidate peaks for identical or near-identical m/z values and cross-references their spatial distributions across the tissue image to identify co-localized signals. The algorithm generates binary overlap flags for each peak (flagged=overlapped, unflagged=unique) based on these criteria. Export the overlap flag table as a structured CSV mapping peak identifiers to overlap status. This output is then used in downstream annotation filtering to exclude or re-evaluate flagged peaks, preventing them from being incorrectly assigned as matrix-related or analyte signals solely on the basis of their m/z or spatial pattern.

## Related tools

- **rMSIcleanup** (Core package implementing overlapping peak detection algorithm and flagging logic) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Loads processed MSI data and peak lists to provide spatial distribution context for overlap detection) — https://github.com/prafols/rMSI
- **rMSIproc** (Processes raw imzML into peak matrix and processed data files required as input) — https://github.com/prafols/rMSIproc
- **R** (Execution environment for rMSIcleanup and all dependent packages)

## Examples

```
results <- rMSIcleanup::annotate_matrix(pks, "Ag1", full); overlap_flags <- results$overlap_flag_table; write.csv(overlap_flags, "overlap_flags.csv")
```

## Evaluation signals

- All candidate peaks in the input list have been assigned a binary overlap flag (no missing values in the output flag table).
- Flagged peaks exhibit either identical or near-identical m/z values AND overlapping spatial distributions across tissue image pixels; unflagged peaks are unique.
- Output CSV is structured and machine-readable with consistent peak identifiers and flag values; can be parsed and filtered by downstream annotation tools.
- Downstream annotation results show no false positive matrix-related assignments for flagged isobaric ions when excluded or re-weighted in the annotation logic.
- Visual inspection of flagged peaks in spatial distribution plots confirms co-localization patterns consistent with isobaric overlap rather than independent signals.

## Limitations

- Algorithm performance depends on mass accuracy of the peak detection method; insufficient mass resolution or calibration may cause false negatives (missed isobars).
- Spatial resolution and pixel size of the MSI acquisition affect ability to detect overlapping spatial distributions; low-resolution imaging may obscure true isobars.
- Algorithm assumes peak lists are already extracted and quantified; does not recover information from undetected or below-threshold ions.
- No quantitative threshold or confidence score provided for the overlap flags; flagging is binary and does not indicate degree or certainty of overlap.
- Performance not evaluated on datasets beyond silver-assisted MALDI imaging; transferability to other matrix types or ionization modes not explicitly demonstrated.

## Evidence

- [intro] The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [other] Apply overlapping peak detection algorithm in rMSIcleanup to identify candidate peaks with identical or near-identical m/z values (isobaric ions) and peaks with overlapping spatial distributions across the tissue image: "Apply overlapping peak detection algorithm in rMSIcleanup to identify candidate peaks with identical or near-identical m/z values (isobaric ions) and peaks with overlapping spatial distributions"
- [other] Generate binary overlap flags for each candidate peak (flagged=overlapped, unflagged=unique): "Generate binary overlap flags for each candidate peak (flagged=overlapped, unflagged=unique)"
- [other] Export overlap flag table as a structured CSV file mapping peak identifiers to overlap status for downstream annotation filtering: "Export overlap flag table as a structured CSV file mapping peak identifiers to overlap status for downstream annotation filtering"
- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
