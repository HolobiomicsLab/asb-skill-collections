---
name: tabular-results-aggregation-and-comparison
description: Use when when you have chemical annotations (GNPS matches) distributed across multiple sample groups (e.g., by sample type, extraction method, ionization source) with unequal numbers of files per group, and you need to compare enrichment fairly without group-size bias.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MassIVE
  - ReDU
  - GNPS
  - Emperor
derived_from:
- doi: 10.1038/s41592-020-0916-7
  title: ReDU
- doi: 10.1186/2047-217x-2-16
  title: ''
evidence_spans:
- ReDU only interacts with MassIVE
- data uploaded to MassIVE as a public dataset
- Validation of the ReDU sample information template using the drag-and-drop validator
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_redu_cq
    doi: 10.1038/s41592-020-0916-7
    title: ReDU
  dedup_kept_from: coll_redu_cq
schema_version: 0.2.0
---

# tabular-results-aggregation-and-comparison

## Summary

Normalize chemical annotation counts across sample groups of unequal size by computing enrichment percentages, enabling fair cross-group comparison in metabolomics and mass spectrometry data. This skill transforms raw frequency counts into percentage-normalized tables suitable for visualization and statistical comparison.

## When to use

When you have chemical annotations (GNPS matches) distributed across multiple sample groups (e.g., by sample type, extraction method, ionization source) with unequal numbers of files per group, and you need to compare enrichment fairly without group-size bias. Use this skill before generating PCA score plots or other comparative visualizations in tools like Emperor.

## When NOT to use

- Input chemical annotations are already normalized or aggregated by an upstream workflow—do not re-normalize.
- Sample groups have equal or near-equal file counts and raw frequency comparison is scientifically justified.
- The analysis goal is to report absolute counts of chemical occurrences, not enrichment or proportional representation.

## Inputs

- ReDU sample-information template (TSV format with sample metadata)
- GNPS chemical annotation data (spectral library matches for all samples)
- Sample grouping category (e.g., 'sample type', 'extraction method', 'ionization source')

## Outputs

- Normalized enrichment table (rows: chemicals; columns: sample groups; values: enrichment percentages 0–100)
- Validated frequency counts matching source annotations
- Tabular data suitable for PCA visualization and Emperor plotting

## How to apply

Load the ReDU sample-information template (TSV format) and associated GNPS chemical annotations for all samples, then group by the selected sample-information category. For each group, enumerate unique chemicals and count how many samples within that group contain each chemical. Compute enrichment as (count of samples in group with chemical) / (total samples in group) × 100 to normalize for unequal group sizes. Tabulate results with chemicals as rows and groups as columns, displaying the enrichment percentage in each cell. Finally, validate that row sums and group totals match the source annotation data and that all percentages fall within [0, 100].

## Related tools

- **ReDU** (Community platform to aggregate public tandem MS data and sample metadata; provides the sample-information template and GNPS annotation integration) — https://github.com/mwang87/ReDU-MS2-GNPS
- **GNPS** (Performs spectral library matching to assign chemical annotations (MS2 spectra comparison); outputs annotation identifiers used as input to enrichment calculation) — https://github.com/CCMS-UCSD/GNPSDocumentation
- **Emperor** (Visualization tool that accepts enrichment tables to generate interactive PCA score plots for comparative exploration of sample groups) — https://github.com/biocore/emperor
- **MassIVE** (Public mass spectrometry data repository where annotated datasets are stored and retrieved; provides the raw MS2 spectra and file metadata)

## Evaluation signals

- Row sums and group totals in the enrichment table match the source GNPS annotation data exactly (no loss or duplication of counts).
- All enrichment percentages fall within the valid range [0, 100].
- Group totals equal (count of samples in group containing any chemical) and reflect correct file enumeration per group.
- When visualized in Emperor (PCA score plot), sample groups show distinct clustering patterns consistent with the enrichment differences.
- Spot-check: manually verify a single chemical's enrichment percentage for one group by hand-counting samples and confirming the calculation.

## Limitations

- The same chemical may have multiple GNPS annotations due to slight MS2 spectral variation (m/z or abundance differences), leading to apparent duplicates that should be deduplicated or merged before aggregation.
- Enrichment percentages do not convey absolute abundance or intensity; they only indicate presence/absence proportion, potentially masking differences in chemical quantity.
- Sample-information categories must be manually completed in the ReDU template; incomplete or inconsistent metadata will result in incorrect grouping and enrichment calculations.
- The method assumes that samples are the unit of enumeration; results are sensitive to file-level duplicates or batch effects within groups.

## Evidence

- [other] For each group, enumerate the unique chemicals (GNPS annotations) present across all samples in that group and count the number of samples within the group containing each chemical.: "For each group, enumerate the unique chemicals (GNPS annotations) present across all samples in that group and count the number of samples within the group containing each chemical."
- [other] Compute enrichment as (count of samples in group containing chemical) / (total samples in group) × 100 to yield percentage, normalizing for group-size imbalance.: "Compute enrichment as (count of samples in group containing chemical) / (total samples in group) × 100 to yield percentage, normalizing for group-size imbalance."
- [other] Tabulate results with rows as chemicals and columns as groups, displaying enrichment percentage in each cell.: "Tabulate results with rows as chemicals and columns as groups, displaying enrichment percentage in each cell."
- [other] Validate that row sums and group totals match the source annotation data and that all percentages fall within [0, 100].: "Validate that row sums and group totals match the source annotation data and that all percentages fall within [0, 100]."
- [abstract] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra cause the pattern to match different reference MS2 spectra"
- [other] Load the ReDU sample-information template (TSV format) and associated GNPS chemical annotations for all samples, grouping by the sample-information category selected: "Load the ReDU sample-information template (TSV format) and associated GNPS chemical annotations for all samples, grouping by the sample-information category selected"
- [abstract] ReDU is the bridge between the [(GNPS2)](https://gnps2.org/) and [MassIVE](https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp), a public data repository for mass spectrometry data: "ReDU is the bridge between GNPS and MassIVE, a public data repository for mass spectrometry data"
- [abstract] The results are plotted using Emperor which provides interactive plotting capabilities to explore the data via a PCA score plot: "The results are plotted using Emperor which provides interactive plotting capabilities to explore the data via a PCA score plot"
