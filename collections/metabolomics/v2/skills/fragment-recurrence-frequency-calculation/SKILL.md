---
name: fragment-recurrence-frequency-calculation
description: Use when after extracting and grouping fragments from top x% TIC-filtered
  replicate spectra for a given feature, to quantify which fragments consistently
  appear across replicates. Use this when you have multiple MS/MS spectra for the
  same precursor (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - dures
  - S4Vectors
  - dplyr
  - Spectra
  - extract_raw_spectra
  - call_aggregate
  - label_individual_spectrum
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- devtools::install_github("BiosystemEngineeringLab-IITB/dures", auth_token = NULL)
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils",
  "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils",
  "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra", "BiocManager",
  "knitr", "markdown"),
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

# fragment-recurrence-frequency-calculation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calculate the recurrence frequency of each fragment across replicate MS/MS spectra by aggregating top-TIC consensus spectra and counting how often each m/z value appears. This frequency metric is used downstream for denoising and selecting high-confidence signal fragments.

## When to use

After extracting and grouping fragments from top x% TIC-filtered replicate spectra for a given feature, to quantify which fragments consistently appear across replicates. Use this when you have multiple MS/MS spectra for the same precursor (e.g., 66 spectra for feature 1982 after 80% TIC filtering) and need to identify robust, recurring signals before applying frequency thresholds for noise reduction.

## When NOT to use

- When working with single-shot MS/MS spectra (no replicates); frequency calculation requires multiple replicate acquisitions
- When input spectra have not yet been filtered to top x% TIC or intra-spectrum grouped; frequency is meaningless on ungrouped/unfiltered raw spectra
- When the goal is real-time single-spectrum annotation rather than multi-replicate consensus building

## Inputs

- Top x% TIC-filtered replicate MS/MS spectra (Spectra object) grouped by feature and ionization mode
- Preprocessed MS/MS data with intra-spectrum fragment grouping already applied
- Mass tolerance value (in Da, typically 0.05 Da)

## Outputs

- Consensus spectrum dataframe with mean m/z, mean intensity, and recurrence frequency for each fragment
- Fragment frequency distribution (count of spectra each m/z appears in)
- Frequency-labeled individual spectra with fragment recurrence metadata

## How to apply

Load the top x% TIC-filtered spectra (e.g., 66 spectra after 80% TIC filtering from an original set of 83) using extract_raw_spectra with mass tolerance (default 0.05 Da). Apply call_aggregate to generate a consensus spectrum by grouping fragments with the same mass tolerance and summing intensities across all replicate spectra. For each unique m/z in the consensus spectrum, count how many of the original replicate spectra contributed a fragment at that m/z (within tolerance), recording this count as the recurrence frequency. The resulting frequency distribution reveals which fragments are noise (low frequency, appearing in few spectra) versus signal (high frequency, appearing consistently). This frequency table becomes the basis for threshold-based denoising in downstream steps.

## Related tools

- **Spectra** (Container and manipulation of MS/MS spectrum objects; stores m/z, intensity, and metadata for replicate spectra) — https://bioconductor.org/packages/Spectra/
- **extract_raw_spectra** (Extracts top x% TIC spectra and performs intra-spectrum fragment grouping prior to frequency calculation) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **call_aggregate** (Generates consensus spectrum from top TIC spectra by grouping fragments within mass tolerance and aggregating intensities across replicates) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **label_individual_spectrum** (Applies recurrence frequency metadata to each individual spectrum for downstream frequency-based denoising) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **S4Vectors** (Provides vector and list infrastructure for storing and aggregating frequency counts) — https://bioconductor.org/packages/S4Vectors/
- **dplyr** (Data manipulation and grouping operations for organizing and summarizing fragment frequency tables) — https://cran.r-project.org/package=dplyr

## Examples

```
l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path)
```

## Evaluation signals

- Consensus spectrum fragment count matches expected output (e.g., 498 fragments for feature 1982)
- Recurrence frequency values are integers ≥ 1 and ≤ the total number of input spectra (e.g., ≤ 66 for feature 1982)
- All consensus fragments have corresponding frequency labels in the output dataframe with no missing values
- Frequency distribution shows expected pattern: high-frequency fragments (signal) have higher mean intensity than low-frequency fragments (noise)
- Individual spectrum labeling preserves fragment identity (m/z values) and correctly maps to consensus frequencies within mass tolerance

## Limitations

- Frequency calculation is sensitive to mass tolerance choice (default 0.05 Da); larger tolerances merge more fragments and inflate frequencies; smaller tolerances may fragment genuine peaks
- Low replicate counts reduce discriminative power of frequency thresholds (e.g., 3 replicates with frequency threshold 0.1 may retain too much noise)
- Frequency thresholds (e.g., 0.1) are dataset-dependent and require tuning via Pareto front analysis or statistical testing to avoid over- or under-denoising
- Does not account for intensity-weighted recurrence; a fragment appearing in all replicates at low intensity may be noise but carries same frequency as high-intensity recurring signal

## Evidence

- [methods] Generate consensus spectrum by applying call_aggregate to group fragments across all 66 top-TIC spectra with mass tolerance 0.05 Da to merge nearby m/z values and sum intensities.: "Generate consensus spectrum by applying call_aggregate to group fragments across all 66 top-TIC spectra with mass tolerance 0.05 Da to merge nearby m/z values and sum intensities."
- [methods] Extract consensus spectrum dataframe containing mean m/z, mean intensity, and fragment recurrence frequencies for each of the 498 fragments.: "Extract consensus spectrum dataframe containing mean m/z, mean intensity, and fragment recurrence frequencies for each of the 498 fragments."
- [methods] In the **third step**, a **consensus spectrum** is generated using the **top 80% TIC spectra**, and the corresponding **fragment frequencies** are calculated: "In the **third step**, a **consensus spectrum** is generated using the **top 80% TIC spectra**, and the corresponding **fragment frequencies** are calculated"
- [readme] This step aggregates the top 80% TIC spectra from step2 and calculates the fragment frequencies l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path): "This step aggregates the top 80% TIC spectra from step2 and calculates the fragment frequencies l3 = call_aggregate(l2$sps_top_tic_2, 0.05, folder_path)"
- [methods] Applies a user-defined frequency threshold (default = `0.1`) to retain **signal fragments**: "Applies a user-defined frequency threshold (default = `0.1`) to retain **signal fragments**"
