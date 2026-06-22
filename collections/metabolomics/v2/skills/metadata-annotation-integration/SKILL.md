---
name: metadata-annotation-integration
description: Use when you have chemical annotations (GNPS spectral library matches) assigned to MS/MS samples and a validated ReDU sample-information template (TSV) with categorical metadata (e.g., sample type, extraction method, ionization source).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
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

# metadata-annotation-integration

## Summary

Integrate sample metadata with tandem MS chemical annotations to enable stratified comparison of chemical enrichment across sample groups. This skill normalizes chemical occurrence counts to percentages within each metadata-defined group, accommodating imbalanced group sizes.

## When to use

You have chemical annotations (GNPS spectral library matches) assigned to MS/MS samples and a validated ReDU sample-information template (TSV) with categorical metadata (e.g., sample type, extraction method, ionization source). You need to compare which chemicals are enriched in each group despite unequal numbers of files per group, typically to produce a PCA score plot or enrichment dashboard stratified by sample information category.

## When NOT to use

- Samples lack validated sample-information metadata or the metadata category has zero variance (all samples in one group).
- Chemical annotations are already pre-aggregated at the group level or have been manually curated outside of GNPS spectral library matching.
- The goal is to compare absolute chemical abundance or spectral intensity, not presence/absence enrichment across groups.

## Inputs

- ReDU sample-information template (TSV format with categorical metadata columns)
- GNPS chemical annotations (MS/MS spectral library matches) indexed by sample
- Sample grouping category (e.g., 'sample type', 'extraction method', 'ionization source')

## Outputs

- Enrichment matrix (chemicals × groups, values = percentage of samples in group containing each chemical)
- Validated tabular data suitable for PCA visualization or enrichment dashboard
- Metadata-stratified chemical occurrence summary

## How to apply

Load the ReDU sample-information template (TSV format) and group samples by your chosen metadata category (e.g., sample type). For each group, enumerate all unique GNPS chemical annotations present across samples in that group and count how many samples within the group contain each chemical. Normalize these counts to percentages: (count of samples in group containing chemical) / (total samples in group) × 100. This percentage-based normalization corrects for groups with different numbers of files, ensuring fair comparison. Tabulate results as a matrix with chemicals as rows and groups as columns, with enrichment percentages in cells. Validate by confirming row sums match source annotation totals and all percentages fall in [0, 100].

## Related tools

- **ReDU** (User interface for grouping, filtering, and querying GNPS chemical annotations by sample information category; directly provides sample-information templates and annotation index) — https://github.com/mwang87/ReDU-MS2-GNPS
- **GNPS** (Generates chemical annotations via spectral library matching (MS/MS); provides putative annotations at metabolomics standard initiative levels 2–3) — https://github.com/CCMS-UCSD/GNPSDocumentation
- **MassIVE** (Public repository storing raw tandem MS data linked to ReDU and GNPS; provides data retrieval and curation infrastructure)
- **Emperor** (Visualizes enrichment matrices as interactive PCA score plots stratified by sample metadata; provides dynamic exploration of chemical-group associations) — https://github.com/biocore/emperor

## Evaluation signals

- Verify that row sums (aggregated enrichment across all groups for each chemical) match the total number of samples containing that chemical in the source annotation data.
- Confirm that all enrichment percentages lie in the range [0, 100]; no negative or supercumulative values.
- Check that group column totals (averaged enrichment across all chemicals for each group) reflect the relative size differences between groups; smaller groups may show higher average percentages due to potential chemical diversity bias.
- Validate that chemicals absent from a group have 0% enrichment; chemicals present in all samples of a group have 100%.
- Cross-reference the tabulated group sizes with the ReDU sample-information template record count to ensure no samples were dropped during integration.

## Limitations

- The same chemical can have multiple GNPS annotations due to slight variation in MS/MS spectra (m/z or abundance), leading to fragmented enrichment counts if not deduplicated beforehand.
- GNPS spectral library annotations are typically level 2 or 3 (putative based on library similarity or characterized compound class), not definitive identifications; chemical enrichment inference is probabilistic.
- Presence/absence enrichment (binary counting) masks abundance and intensity information; low-intensity or noise-like signals are treated equally to high-confidence signals if they pass annotation thresholds.
- Groups with very small sample counts (e.g., 1–2 samples) will show 0%, 50%, or 100% enrichment with high variance; statistical power is limited.
- Manual completion of the ReDU sample-information template introduces operator error; validation via the ReDU drag-and-drop validator is necessary before integration.

## Evidence

- [other] For each group, enumerate the unique chemicals (GNPS annotations) present across all samples in that group and count the number of samples within the group containing each chemical.: "For each group, enumerate the unique chemicals (GNPS annotations) present across all samples in that group and count the number of samples within the group containing each chemical."
- [other] Compute enrichment as (count of samples in group containing chemical) / (total samples in group) × 100 to yield percentage, normalizing for group-size imbalance.: "Compute enrichment as (count of samples in group containing chemical) / (total samples in group) × 100 to yield percentage, normalizing for group-size imbalance."
- [other] Tabulate results with rows as chemicals and columns as groups, displaying enrichment percentage in each cell.: "Tabulate results with rows as chemicals and columns as groups, displaying enrichment percentage in each cell."
- [other] Percentages should be used to tabulate sample information enrichment for each chemical annotated across groups, enabling fair comparison when groups contain different file counts.: "Percentages should be used to tabulate sample information enrichment for each chemical annotated across groups, enabling fair comparison when groups contain different file counts."
- [other] Load the ReDU sample-information template (TSV format) and associated GNPS chemical annotations for all samples, grouping by the sample-information category selected: "Load the ReDU sample-information template (TSV format) and associated GNPS chemical annotations for all samples, grouping by the sample-information category selected"
- [other] Validate that row sums and group totals match the source annotation data and that all percentages fall within [0, 100].: "Validate that row sums and group totals match the source annotation data and that all percentages fall within [0, 100]."
- [abstract] GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on: "GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3"
- [abstract] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra cause the pattern to match different reference MS2 spectra"
