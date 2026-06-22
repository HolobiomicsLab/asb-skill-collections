---
name: feature-redundancy-reduction-with-ion-identity
description: Use when when processing MZmine2/MZmine3 peak tables from LC–MS metabolomics data where you observe inflated feature counts due to multiple ionization states, isotopic satellites, and neutral losses of the same parent compound, particularly before computing extract-level metrics (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - Ion Identity
  - inventa
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time' columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/), is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico annotations and taxonomically informed reponderation.'
- 'tima_results_filename: timaR reponderated output format'
- Inventa is capable to performe the calcultions based on the results from Ion Identity, reducing the total number of features.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_inventa_cq
    doi: 10.3389/fmolb.2022.1028334
    title: Inventa
  dedup_kept_from: coll_inventa_cq
schema_version: 0.2.0
---

# feature-redundancy-reduction-with-ion-identity

## Summary

Ion Identity grouping reduces redundant features in untargeted metabolomics by collapsing multiple peaks arising from the same molecule (adducts, isotopes, in-source fragments) into single representative features. This decreases feature table complexity and improves quantitative metric reproducibility such as Feature Component (FC) scoring in natural extract novelty assessment.

## When to use

When processing MZmine2/MZmine3 peak tables from LC–MS metabolomics data where you observe inflated feature counts due to multiple ionization states, isotopic satellites, and neutral losses of the same parent compound, particularly before computing extract-level metrics (e.g., FC) or before annotation filtering to avoid double-counting structurally identical entities.

## When NOT to use

- Input is already a deduplicated feature table or has undergone prior adduct/isotope filtering.
- Analysis goal requires preservation of individual adduct or isotope annotations (e.g., isotopic ratio studies).
- Ion Identity parameters are not available or not validated for your LC–MS platform and ionization mode.

## Inputs

- MZmine2 or MZmine3 peak quantification table (peak area, row m/z, row retention time columns)
- Ion Identity grouping results or configuration from MZmine interface

## Outputs

- Deduplicated quantitative feature table with Ion Identity groups collapsed
- Feature group mapping (original features to representative feature ID)
- Reduced feature count per sample

## How to apply

After generating a quantitative feature table (peak area, m/z, retention time columns) from MZmine2 or MZmine3, apply Ion Identity grouping to collapse co-eluting features with correlated intensity patterns and predictable mass differences (e.g., [M+H]+, [M+Na]+, [M+K]+ adducts; 13C isotopes; common neutral losses) into single consensus features. The reduced feature set is then used as input to downstream annotation filtering (ppm_error, shared_peaks, cosine score thresholds) and component scoring. Ion Identity output retains the total number of reduced features per sample while preserving quantitative intensity relationships; the grouping step should be documented in the workflow metadata to ensure reproducibility of FC and other metrics computed from the deduplicated table.

## Related tools

- **MZmine2** (Peak detection and quantification; source of raw feature table before Ion Identity grouping)
- **MZmine3** (Peak detection and quantification; modern alternative to MZmine2 with integrated Ion Identity module)
- **Ion Identity** (Groups redundant features (adducts, isotopes, in-source fragments) into single representative features, reducing table complexity)
- **inventa** (Accepts deduplicated feature tables as input and computes Feature Component (FC) and other novelty metrics on Ion Identity-reduced feature sets) — https://github.com/luigiquiros/inventa

## Evaluation signals

- Total feature count after Ion Identity grouping is substantially lower than input table (typical reduction 15–50% depending on ionization complexity).
- Each Ion Identity group contains features with mass differences consistent with known adduct or isotope patterns (e.g., 1.003 Da for 13C, 22 Da for [M+Na]+ − [M+H]+).
- Feature Component (FC) computed on deduplicated table is reproducible and does not artificially inflate non-annotated feature counts due to adduct redundancy.
- Peak area intensity sums or intensity correlations are preserved across grouped features (co-elution and ratio consistency).
- Downstream annotation filtering (ISDB, SIRIUS) produces expected number of unique molecular structures without duplication from redundant features.

## Limitations

- Ion Identity grouping relies on accurate m/z measurement and retention time alignment; errors in these measurements can lead to incorrect feature associations or missed groups.
- Efficacy depends on ionization mode, chromatography method, and sample complexity; chemodiverse extracts with wide m/z and RT ranges may yield incomplete or ambiguous groupings.
- Loss of isotopic abundance information when collapsing isotope clusters may limit downstream isotopic labeling or isotope-ratio studies.
- No changelog found for Ion Identity versioning or parameter updates; parameter consistency across MZmine versions not formally documented.

## Evidence

- [other] Inventa is capable to performe the calcultions based on the results from Ion Identity, reducing the total number of features.: "Inventa is capable to performe the calcultions based on the results from Ion Identity, reducing the total number of features."
- [other] MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time' columns. -Inventa takes input directly from MZmine2 or MZmine 3: "MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time' columns. -Inventa takes input directly from MZmine2 or MZmine 3"
- [methods] The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract.: "The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract."
- [readme] if you did export any other column, like identities, etc, please remove manually or add the corresponding lines in the funcion quand_table().: "if you did export any other column, like identities, etc, please remove manually or add the corresponding lines in the funcion quand_table()."
