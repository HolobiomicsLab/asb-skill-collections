---
name: spatial-overlap-analysis-imaging
description: Use when when annotating matrix-related peaks in MSI datasets where candidate peaks have identical or near-identical m/z values (isobaric ions), or when multiple peaks exhibit overlapping spatial distributions across the tissue image that could confound downstream annotation filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3379
  tools:
  - rMSIcleanup
  - rMSI
  - R
  - rMSIproc
derived_from:
- doi: 10.1186/s13321-020-00449-0
  title: ''
evidence_spans:
- rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data
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
---

# Spatial-overlap analysis for imaging mass spectrometry

## Summary

Identifies and flags overlapping peaks and isobaric ions in mass spectrometry imaging (MSI) data by analyzing m/z coincidence and spatial distribution patterns across tissue. This prevents misclassification of chemically distinct ions during matrix-related signal annotation.

## When to use

When annotating matrix-related peaks in MSI datasets where candidate peaks have identical or near-identical m/z values (isobaric ions), or when multiple peaks exhibit overlapping spatial distributions across the tissue image that could confound downstream annotation filtering.

## When NOT to use

- Input peaks are already validated as unique or confirmed to be from distinct chemical species by orthogonal methods (e.g., tandem MS or NMR).
- Analyzing single-point mass spectra without spatial distribution data; overlap detection requires 2D or 3D tissue image coordinates.
- Working with pre-processed data where overlapping peaks have already been resolved or merged by the instrument vendor.

## Inputs

- Mass spectrometry imaging (MSI) data in rMSIproc format (.tar)
- Extracted peak list / peak matrix (.zip)
- Chemical formula annotations (optional, for context)

## Outputs

- Binary overlap flag table (CSV) mapping peak identifiers to overlap status
- Annotated peak matrix with overlap classification
- Visual report justifying each overlap annotation

## How to apply

Load the MSI data and extracted peak list into R using rMSI and rMSIproc. Apply the overlapping peak detection algorithm in rMSIcleanup by calling annotate_matrix(), which identifies candidate peaks with matching or near-matching m/z values and examines their spatial co-localization patterns across the tissue. The algorithm generates binary overlap flags (flagged for overlapped, unflagged for unique peaks) mapped to each peak identifier. Export the overlap flag table as a structured CSV file and use these flags to filter downstream annotation decisions, preventing ambiguous or overlapped peaks from being misassigned to matrix or analyte categories.

## Related tools

- **rMSIcleanup** (Core package providing annotate_matrix() function for overlapping peak detection and generate_pdf_report() for visual justification of flags) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Loads and manages MSI data objects; provides spatial coordinate system for overlap analysis) — https://github.com/prafols/rMSI
- **rMSIproc** (Preprocesses imzML files and manages peak matrix format (.zip) for input to overlap detection) — https://github.com/prafols/rMSIproc
- **R** (Runtime environment for rMSIcleanup and dependent packages)

## Examples

```
rMSIcleanup::annotate_matrix(pks, "Ag1", full); rMSIcleanup::generate_pdf_report(results, pks, full, "overlap_report", folder="./")
```

## Evaluation signals

- Overlap flag table contains no missing values and all peak identifiers map to exactly one flag status (flagged or unflagged).
- Peaks flagged as overlapped exhibit < N ppm m/z difference threshold AND spatial Pearson correlation > threshold across tissue image; unflagged peaks do not meet both criteria.
- Visual PDF report displays side-by-side spatial heatmaps for each flagged peak pair, with overlapping regions highlighted to justify the flag assignment.
- Downstream annotation step (remove_matrix function) successfully filters flagged peaks without throwing errors, producing a reduced peak matrix with consistent dimensionality.
- Manual spot-check: randomly sampled 10–20 flagged peaks show genuine m/z overlap and/or spatial co-localization; no false positives where unrelated peaks were incorrectly flagged.

## Limitations

- Algorithm depends on peak picking quality upstream; noisy or poorly resolved peaks may generate false overlap flags or miss genuine overlaps.
- Isobaric ion resolution relies on m/z accuracy of the mass spectrometer; instruments with lower mass resolution (> 5 ppm) may conflate distinct ions.
- Spatial overlap detection assumes tissue heterogeneity; in highly uniform regions or homogeneous tissue, spatial correlation alone may not distinguish isobaric pairs.
- No discussion of tuning parameters (m/z tolerance, spatial correlation threshold) provided in the article; users must select thresholds empirically.
- Currently designed for 2D MSI workflows; extension to 3D tissue imaging or high-dimensional spatial data is not documented.

## Evidence

- [intro] overlapping peak detection feature designed to prevent misclassification of overlapped or isobaric ions: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [other] identify candidate peaks with identical or near-identical m/z values and peaks with overlapping spatial distributions: "Apply overlapping peak detection algorithm in rMSIcleanup to identify candidate peaks with identical or near-identical m/z values (isobaric ions) and peaks with overlapping spatial distributions"
- [other] binary overlap flags for each candidate peak: "Generate binary overlap flags for each candidate peak (flagged=overlapped, unflagged=unique)."
- [intro] algorithm takes into account the chemical formula and the spatial distribution: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
- [intro] visual report to transparently justify each annotation: "the package generates a visual report to transparently justify each annotation"
- [readme] rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data: "rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data."
- [readme] workflow for loading and annotating data: "pks<-rMSIproc::LoadPeakMatrix("[Full Path to Peak Matrix (.zip)]"); results<-rMSIcleanup::annotate_matrix(pks,"Ag1",full)"
