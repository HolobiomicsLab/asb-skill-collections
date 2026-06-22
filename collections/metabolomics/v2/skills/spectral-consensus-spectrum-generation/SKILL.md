---
name: spectral-consensus-spectrum-generation
description: Use when after extracting and filtering top-TIC spectra for a given feature (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - dures
  - S4Vectors
  - dplyr
  - call_aggregate
  - extract_raw_spectra
  - Spectra
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-consensus-spectrum-generation

## Summary

Generate a consensus MS/MS spectrum by aggregating fragment m/z values and intensities across replicate spectra within a specified mass tolerance, producing a merged spectrum with fragment recurrence frequencies. This step is essential for denoising and downstream metabolite annotation in untargeted metabolomics.

## When to use

After extracting and filtering top-TIC spectra for a given feature (e.g., using 80% TIC cutoff), when you need to identify stable, recurring fragments across multiple replicate MS/MS measurements and establish a baseline fragment frequency distribution for labeling and denoising individual spectra.

## When NOT to use

- Input spectra have not been pre-filtered by top-TIC cutoff; consensus will reflect noise and low-quality spectra equally.
- Mass tolerance is not calibrated for your instrument type; grouping will either miss true co-eluting fragments or merge distinct ones incorrectly.
- Single replicate spectrum available for a feature; consensus spectrum requires multiple spectra to compute meaningful recurrence frequencies.

## Inputs

- Top-TIC-filtered MS/MS spectra collection (Spectra object or equivalent) for a single feature
- Mass tolerance threshold (Da; typically 0.05)
- Folder path containing input and output data

## Outputs

- Consensus spectrum dataframe with columns: mean m/z, mean intensity, fragment recurrence frequency
- Fragment count (total number of unique fragments after merging)
- Recurrence frequency vector for downstream labeling and filtering

## How to apply

Input the top-TIC-filtered spectra collection for a single feature (e.g., 66 spectra after 80% TIC filtering from 83 original spectra). Apply the call_aggregate function with a mass tolerance parameter (default 0.05 Da) to group and merge fragment m/z values across all spectra, summing intensities for each grouped fragment and recording recurrence frequency (count of spectra in which each fragment appears). The output is a consensus spectrum dataframe containing mean m/z, mean intensity, and fragment recurrence count for each merged fragment. This frequency information becomes the reference standard for subsequent labeling of individual spectra and frequency-based denoising steps.

## Related tools

- **call_aggregate** (Core function that merges fragments across top-TIC spectra within mass tolerance and computes recurrence frequencies) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **extract_raw_spectra** (Prerequisite function that filters to top-TIC spectra and performs intra-spectrum grouping before consensus generation) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **Spectra** (Bioconductor package providing MS/MS spectrum object representation and aggregation infrastructure)
- **S4Vectors** (Bioconductor package providing S4 class system used by Spectra and consensus spectrum data structures)
- **dplyr** (Data manipulation and aggregation within consensus spectrum dataframe construction)

## Examples

```
l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path)
```

## Evaluation signals

- Fragment count matches expected consensus spectrum size (e.g., 498 fragments for feature 1982 as reported in task_002).
- All fragments in the consensus spectrum have recurrence frequency ≥ 1 (each fragment appears in at least one replicate spectrum).
- Mean m/z and mean intensity values are within expected ranges for the instrument and ionization mode (e.g., positive mode).
- Recurrence frequency distribution is reasonable for the number of input spectra (e.g., max frequency ≤ number of top-TIC spectra used, typically 66 for 80% TIC cutoff on ~83 input spectra).
- Consensus spectrum has fewer or equal fragments than the largest individual input spectrum (merging should not create new fragments, only combine them).

## Limitations

- Mass tolerance (0.05 Da) is empirically chosen and may not be optimal for all instruments; calibration via parameter tuning (Pareto front analysis) is recommended.
- Consensus generation assumes replicate spectra are comparable in quality and ionization efficiency; highly variable or outlier spectra can inflate fragment frequencies.
- Fragment recurrence frequency alone does not indicate biological significance; frequency-based denoising thresholds must be tuned relative to noise background.
- Consensus spectrum aggregates intensities across spectra, masking intensity variation that may correlate with sample composition or instrument drift.

## Evidence

- [other] Generate consensus spectrum by applying call_aggregate to group fragments across all 66 top-TIC spectra with mass tolerance 0.05 Da to merge nearby m/z values and sum intensities.: "Generate consensus spectrum by applying call_aggregate to group fragments across all 66 top-TIC spectra with mass tolerance 0.05 Da to merge nearby m/z values and sum intensities."
- [other] Extract consensus spectrum dataframe containing mean m/z, mean intensity, and fragment recurrence frequencies for each of the 498 fragments.: "Extract consensus spectrum dataframe containing mean m/z, mean intensity, and fragment recurrence frequencies for each of the 498 fragments."
- [methods] In the **third step**, a **consensus spectrum** is generated using the **top 80% TIC spectra**, and the corresponding **fragment frequencies** are calculated: "In the third step, a consensus spectrum is generated using the top 80% TIC spectra, and the corresponding fragment frequencies are calculated"
- [readme] l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path): "l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path)"
- [methods] fragments in the reference spectra that fall within the specified *m/z* tolerance (`tol`) are grouped together: "fragments in the reference spectra that fall within the specified m/z tolerance are grouped together"
