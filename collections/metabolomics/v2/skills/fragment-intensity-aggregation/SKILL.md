---
name: fragment-intensity-aggregation
description: Use when after extracting raw MS/MS spectra from mzML files but before consensus spectrum generation, when you observe high-resolution fragment lists where nearby peaks (within a specified mass tolerance, typically 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - dures
  - dplyr
  - Spectra
  - data.table
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

# fragment-intensity-aggregation

## Summary

Merges m/z-proximal MS/MS fragments within individual spectra by averaging their mass-to-charge ratios and summing their intensities, reducing fragment redundancy while preserving signal strength. This intra-spectrum grouping is a foundational denoising step that reduces fragment count while maintaining spectral information fidelity.

## When to use

Apply this skill after extracting raw MS/MS spectra from mzML files but before consensus spectrum generation, when you observe high-resolution fragment lists where nearby peaks (within a specified mass tolerance, typically 0.05 Da) represent the same ion due to instrumental precision or isotopic fine structure, and you want to compress fragmentation patterns while summing their detection intensities.

## When NOT to use

- Input spectra are already processed or smoothed by the instrument or vendor software, making redundant grouping unnecessary.
- Analysis requires preservation of fine isotopic structure or high-mass-resolution features for 13C or 2H discrimination.
- Mass tolerance parameter is poorly calibrated or not experimentally validated for the instrument; incorrect tolerance leads to spurious merging or missed grouping.

## Inputs

- Raw MS/MS spectra in mzML format (multiple scans per feature)
- Preprocessed spectrum object list (output from dures preprocess())
- Feature metadata (precursor m/z, RT, feature ID)
- Mass tolerance parameter (Da; typically 0.05)

## Outputs

- Grouped fragment list per spectrum (merged m/z values and summed intensities)
- Reduced fragment count per spectrum (e.g., 98→81 fragments)
- Peak data matrix with aggregated m/z and intensity columns

## How to apply

Load preprocessed MS/MS spectra using the dures package preprocess() function with specified m/z tolerance (e.g., 5 ppm) and RT tolerance (e.g., 0.1 min). Apply extract_raw_spectra() with a mass tolerance parameter (default 0.05 Da) to identify and group fragments: for each spectrum, collect all m/z values that fall within the tolerance window, compute their mean m/z as the merged peak position, and sum the corresponding intensity values. Extract peak data using Spectra::peaksData() before and after grouping to verify fragment count reduction. The rationale is that instrumental artifacts, isotopic patterns, and calibration drift create multiple detections of the same chemical fragment; merging them reduces false diversity while preserving cumulative signal (intensity sum), improving downstream consensus spectrum quality and denoising efficacy.

## Related tools

- **dures** (Provides extract_raw_spectra() function to perform intra-spectrum fragment grouping and merging with configurable mass tolerance) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **Spectra** (Supplies peaksData() method to extract and validate fragment m/z and intensity matrices before and after grouping)
- **data.table** (Enables efficient grouping, aggregation, and validation of fragment lists at scale)

## Examples

```
l2 = extract_raw_spectra(folder_path = folder_path, l1, 0.05, 0.8)
```

## Evaluation signals

- Fragment count reduction matches reported values: e.g., feature 1982 from 23→22, feature 872 from 98→81 fragments.
- Merged m/z values fall within ±mass_tolerance of at least two pre-grouping m/z peaks; no spurious merging across distant peaks.
- Summed intensities of merged fragments equal or exceed the maximum intensity of component peaks (no signal loss).
- peaksData() output before and after grouping shows consistent total ion current (TIC) or only minor reduction due to grouping logic.
- Grouped spectra retain sufficient fragment diversity to distinguish metabolite classes in downstream consensus and annotation steps.

## Limitations

- Intra-spectrum grouping is sensitive to mass tolerance calibration; too loose a tolerance merges distinct ions; too tight a tolerance misses true duplicates, reducing the benefit of the step.
- Grouping assumes that all m/z-proximal peaks within a single spectrum represent the same fragment; in high-complexity spectra or at low resolution, this can conflate unrelated minor fragments.
- The step does not account for RT or chromatographic variation within a single spectrum; it only aggregates within-spectrum intensity, not across spectra (inter-spectrum grouping is a separate step in the DuReS workflow).
- Fragment intensities are simple sums; no weighting or outlier handling is applied, so a single very-high-intensity artifact can dominate the merged peak if it falls within tolerance.

## Evidence

- [methods] Apply extract_raw_spectra() with mass tolerance 0.05 Da to group fragments within each spectrum by merging m/z values (mean) and summing intensities.: "Apply extract_raw_spectra() with mass tolerance 0.05 Da to group fragments within each spectrum by merging m/z values (mean) and summing intensities."
- [methods] After grouping, the number of fragments reduced to `81`: "After grouping, the number of fragments reduced to `81`"
- [methods] fragments within a default tolerance of **0.05 Da** of one another were merged: "fragments within a default tolerance of **0.05 Da** of one another were merged"
- [methods] Extract the top x% TIC spectra, and Group fragments within a specified mass tolerance: "Extract the top x% TIC spectra, and Group fragments within a specified mass tolerance"
- [readme] extract top x% (where x = 0.8) TIC spectra, groups fragments within a given tolerance (0.05 Da): "extract top x% (where x = 0.8) TIC spectra, groups fragments within a given tolerance (0.05 Da)"
