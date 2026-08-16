---
name: m-z-value-clustering-mass-spectrometry
description: Use when processing extracted peak lists from MSI data and you need to
  annotate matrix-related signals but suspect that multiple ions with the same or
  very similar m/z values (isobaric ions) are present.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
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

# m/z-value clustering in mass spectrometry

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and flag mass-to-charge ratio (m/z) peaks with identical or near-identical values (isobaric ions) to prevent their misclassification during matrix-related signal annotation in mass spectrometry imaging (MSI) data. This skill uses spatial distribution and chemical formula context to distinguish overlapping or isobaric peaks that would otherwise confound downstream annotation.

## When to use

Apply this skill when processing extracted peak lists from MSI data and you need to annotate matrix-related signals but suspect that multiple ions with the same or very similar m/z values (isobaric ions) are present. Trigger conditions include: (1) peak list contains candidate peaks with m/z differences smaller than your mass spectrometer's resolution; (2) spatial distribution patterns suggest multiple ions at the same nominal m/z; (3) downstream annotation tasks require confidence that each peak ID uniquely represents a single chemical species, not a mixture of isobaric ions.

## When NOT to use

- Input peak list has already been de-isotoped and clustered by a prior tool; applying a second clustering pass may introduce redundant or conflicting flags.
- Mass spectrometer has very poor m/z resolution (>>1 Da); m/z-based clustering alone cannot discriminate isobaric ions and spatial patterns become unreliable.
- Tissue region of interest shows uniform spatial distribution across all peaks; overlapping peaks cannot be distinguished by spatial co-localization patterns, making binary flags ambiguous.

## Inputs

- Extracted peak matrix in rMSIproc format (.zip file containing peak intensity matrix)
- Processed MSI data file (.tar archive in rMSI format)
- Chemical formula database or mass library (implicit; used for plausibility checks)

## Outputs

- Binary overlap flag table (CSV) mapping peak identifiers to overlap status (overlapped vs. unique)
- Annotated peak matrix with isobaric/overlapped peaks flagged for downstream filtering
- Peak clustering assignments (peaks grouped by identical or near-identical m/z values)

## How to apply

Load the extracted peak matrix (in rMSIproc format, typically a .zip file) and the processed MSI data into R using rMSI and rMSIproc. Apply the overlapping peak detection algorithm embedded in rMSIcleanup's annotation workflow, which scans the peak list for candidate peaks with identical or near-identical m/z values and cross-validates their spatial distributions across the tissue image. The algorithm assigns a binary overlap flag to each peak (flagged=overlapped/isobaric, unflagged=unique). The decision to flag a peak as overlapped considers both chemical formula plausibility and whether peaks exhibit spatially coincident intensity patterns. Export the overlap flag table as a structured CSV mapping peak identifiers to overlap status; use these flags to exclude or quarantine overlapped peaks from downstream matrix annotation filtering, preventing misidentification of isobaric ions as distinct chemical entities.

## Related tools

- **rMSIcleanup** (Primary tool embedding the overlapping peak detection algorithm; called via annotate_matrix() function to identify and flag isobaric peaks) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Loads processed MSI data (.tar) into R and provides spatial distribution context for overlap detection) — https://github.com/prafols/rMSI
- **rMSIproc** (Loads and stores peak matrices in .zip format; handles file I/O for peak list input) — https://github.com/prafols/rMSIproc
- **R** (Execution environment for rMSIcleanup and dependency packages)

## Examples

```
pks <- rMSIproc::LoadPeakMatrix("Ag_Pancreas_TOF_2015_Dataset2.zip"); full <- rMSI::LoadMsiData("Ag_Pancreas_TOF_2015_Dataset2_proc.tar"); results <- rMSIcleanup::annotate_matrix(pks, "Ag1", full); overlap_flags <- results$overlapping_peaks
```

## Evaluation signals

- Overlap flag table contains one row per peak in the input matrix; all peak IDs are present and accounted for (no missing or duplicate entries).
- Peaks flagged as 'overlapped' have m/z values within the mass spectrometer's stated resolution (e.g., <5 ppm for TOF-MS); peaks flagged as 'unique' should have no neighbors within that tolerance.
- Overlapped peaks exhibit spatially coincident intensity patterns (Pearson r > threshold) across the tissue image; non-overlapped peaks show spatial distributions that differ significantly or are spatially isolated.
- Visual report generated by rMSIcleanup::generate_pdf_report() displays spatial heatmaps and m/z histograms confirming that flagged overlaps correspond to actual co-localized ion signals, not spurious clustering.
- Downstream matrix annotation results change when overlapped peaks are excluded: matrix-ion candidates that were ambiguous before filtering become unambiguous post-filtering, indicating the flags prevented misclassification.

## Limitations

- Overlapping peak detection relies on spatial distribution information; if all peaks are uniformly distributed (e.g., whole-tissue matrix signal), spatial patterns alone cannot discriminate isobaric ions.
- Algorithm uses chemical formula and spatial distribution as joint criteria; if the correct chemical formula is not in the reference database or if spatial distribution is weak, false negatives (missed overlaps) may occur.
- Binary overlap flags do not quantify the degree of overlap or provide a confidence score; practitioners cannot easily distinguish between high-confidence and borderline overlaps.
- Performance and sensitivity depend on the mass spectrometer's m/z resolution and the tissue's spatial heterogeneity; results may not generalize across different instruments or sample types.

## Evidence

- [intro] The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [other] Apply overlapping peak detection algorithm in rMSIcleanup to identify candidate peaks with identical or near-identical m/z values (isobaric ions) and peaks with overlapping spatial distributions across the tissue image: "Apply overlapping peak detection algorithm in rMSIcleanup to identify candidate peaks with identical or near-identical m/z values (isobaric ions) and peaks with overlapping spatial distributions"
- [other] Generate binary overlap flags for each candidate peak (flagged=overlapped, unflagged=unique). Export overlap flag table as a structured CSV file mapping peak identifiers to overlap status for downstream annotation filtering: "Generate binary overlap flags for each candidate peak (flagged=overlapped, unflagged=unique). Export overlap flag table as a structured CSV file mapping peak identifiers to overlap status"
- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
- [readme] rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data. The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related. The algorithm incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions.: "rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data. The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are"
