---
name: spectral-peak-grouping-mass-tolerance
description: Use when after extracting raw MS/MS spectra from mzML files when you observe high fragment counts per spectrum (e.g., 98 fragments) and want to reduce noise from instrument measurement uncertainty.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - dures
  - dplyr
  - Spectra
  - data.table
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- devtools::install_github("BiosystemEngineeringLab-IITB/dures", auth_token = NULL)
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra", "BiocManager", "knitr", "markdown"),
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dures_cq
    doi: 10.1021/acs.analchem.5c01726
    title: DuReS
  dedup_kept_from: coll_dures_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01726
  all_source_dois:
  - 10.1021/acs.analchem.5c01726
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-grouping-mass-tolerance

## Summary

Merge MS/MS spectral peaks (m/z and intensity) within a specified mass tolerance to reduce fragment redundancy and noise in tandem mass spectrometry data. This intra-spectrum grouping step consolidates nearby m/z values by averaging their positions and summing their intensities, typically reducing fragment counts by 10–20% before downstream denoising.

## When to use

Apply this skill after extracting raw MS/MS spectra from mzML files when you observe high fragment counts per spectrum (e.g., 98 fragments) and want to reduce noise from instrument measurement uncertainty. Use it as a preprocessing step before consensus spectrum generation or frequency-based denoising, especially when replicate spectra from the same feature show multiple near-duplicate peaks that differ only within your instrument's mass accuracy (typically 0.05 Da for orbitrap or 5 ppm for time-of-flight).

## When NOT to use

- Input spectra are already denoised or have been processed by another grouping algorithm; re-grouping may double-merge peaks.
- Your instrument mass accuracy is unknown or poorly characterized; choosing tolerance without validation can lose signal or retain noise.
- Inter-spectrum (cross-replicate) grouping is required instead; this skill only groups peaks within single spectra, not across replicates.

## Inputs

- mzML files (raw MS/MS spectra)
- preprocessed spectra object from preprocess()
- feature metadata (m/z, retention time, feature ID)
- mass tolerance parameter (Da or ppm)

## Outputs

- grouped spectra object with merged m/z and summed intensities
- fragment count per spectrum (post-grouping)
- peak data matrix (m/z × intensity) for grouped spectra

## How to apply

Load preprocessed MS/MS spectra using the preprocess() function with specified m/z and RT tolerances (e.g., 5 ppm m/z, 0.1 min RT). Apply extract_raw_spectra() with a mass tolerance parameter (default 0.05 Da) to group fragments within each individual spectrum by merging m/z values (arithmetic mean) and summing their intensities. Verify the grouping by extracting peak data using Spectra::peaksData() before and after grouping, comparing fragment counts to confirm reduction (e.g., 98 → 81 fragments). The tolerance should match your instrument's mass accuracy; tighter tolerances (0.05 Da) preserve more peaks, while looser tolerances (0.1+ Da) achieve greater consolidation at the risk of merging genuine distinct ions.

## Related tools

- **dures** (R package providing extract_raw_spectra() function to perform intra-spectrum fragment grouping within specified mass tolerance) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **Spectra** (Bioconductor R package providing peaksData() to extract and inspect peak m/z and intensity matrices before and after grouping)
- **data.table** (R package for efficient manipulation of grouped peak data and fragment count aggregation)
- **dplyr** (R package for filtering and transforming spectral data before and after grouping)

## Examples

```
l2 = extract_raw_spectra(folder_path = folder_path, l1, 0.05, 0.8)
```

## Evaluation signals

- Fragment count reduction is monotonic and consistent with mass tolerance choice (e.g., tighter tolerance → smaller reduction; looser tolerance → larger reduction).
- Sum of pre-grouping and post-grouping intensities are equal or nearly equal for each spectrum (intensity is conserved during merging).
- Mean m/z of grouped peaks falls within the specified mass tolerance of the original constituent peaks (validate averaging arithmetic).
- Reported fragment counts match independently verified counts from external spectral files (e.g., MS2_scans_before_denoising .txt files) or manual spot-checks.
- No peaks disappear; final fragment count is strictly less than or equal to the input count (monotonic decrease or identity).

## Limitations

- Mass tolerance is global and uniform; instrument calibration drift or m/z-dependent accuracy variations are not modeled per-spectrum.
- Merging by arithmetic mean of m/z assumes equal reliability of all constituent peaks; weighted averaging by intensity may be more appropriate.
- Intra-spectrum grouping does not address cross-replicate redundancy; use inter-spectrum grouping or consensus spectrum generation for that.
- Very tight tolerances (e.g., 0.01 Da) may fail to merge true duplicates if instrumental noise exceeds the tolerance; very loose tolerances (e.g., 0.5 Da) risk merging distinct ions.
- No automatic validation that chosen tolerance matches instrument specs; user must supply or calibrate independently.

## Evidence

- [methods] After grouping, the number of fragments reduced to `81`: "After grouping, the number of fragments reduced to `81`"
- [methods] Apply extract_raw_spectra() with mass tolerance to group fragments by merging m/z values (mean) and summing intensities: "Apply extract_raw_spectra() with mass tolerance 0.05 Da to group fragments within each spectrum by merging m/z values (mean) and summing intensities."
- [methods] Fragments within default tolerance of 0.05 Da were merged: "fragments within a default tolerance of **0.05 Da** of one another were merged"
- [methods] Extract peak data using Spectra::peaksData() before intra-spectrum grouping for verification: "Extract peak data using Spectra::peaksData() before intra-spectrum grouping for features 1982 (spectrum scan_1587, expected 23 fragments)"
- [readme] DuReS extracts top x% TIC spectra and groups fragments within a specified mass tolerance: "Extract the top x% TIC spectra, and **Group fragments** within a specified **mass tolerance**"
- [methods] Fragment reduction from 98 to 81 fragments after intra-spectrum grouping: "Fragment reduction from 98 to 81 fragments after intra-spectrum grouping and labeling"
