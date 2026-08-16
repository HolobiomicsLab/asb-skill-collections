---
name: normalization-for-unequal-group-sizes
description: Use when when tabulating chemical annotation enrichment (e.g., GNPS spectral
  library matches) across sample groups stratified by metadata category (e.g., sample
  type, extraction method, ionization source), and the groups contain different numbers
  of files or samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MassIVE
  - ReDU
  - GNPS
  - Emperor
  techniques:
  - CE-MS
  license_tier: restricted
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-020-0916-7
  all_source_dois:
  - 10.1038/s41592-020-0916-7
  - 10.1186/2047-217x-2-16
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# normalization-for-unequal-group-sizes

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Normalize chemical annotation enrichment across sample groups with unequal file counts by converting raw sample counts to percentages, enabling fair cross-group comparison in metabolomics cohort studies. This skill addresses the bias introduced when groups contain different numbers of reanalyzed mass spectrometry files.

## When to use

When tabulating chemical annotation enrichment (e.g., GNPS spectral library matches) across sample groups stratified by metadata category (e.g., sample type, extraction method, ionization source), and the groups contain different numbers of files or samples. Raw counts would bias comparison toward larger groups; percentage normalization is required to detect whether a chemical is truly enriched in a group rather than simply more frequent due to group size.

## When NOT to use

- Input is already a pre-aggregated feature table with normalized counts or relative abundances; apply this skill only to raw file-level annotations.
- All groups contain identical numbers of files; percentage normalization offers no advantage over raw counts when group sizes are equal, though it does no harm.
- Chemical abundance or intensity data are available and the goal is to compare absolute signal rather than presence/absence enrichment; use abundance-based normalization (e.g., total ion intensity) instead.

## Inputs

- ReDU sample-information template (TSV format) with sample metadata and file-to-sample mapping
- GNPS chemical annotation results for all reanalyzed files (compound identifiers and file associations)
- Selected sample information category (e.g., 'sample type', 'extraction method')

## Outputs

- Enrichment percentage matrix (chemicals × groups) suitable for PCA visualization or statistical comparison
- Tabulated result with row sums and group totals validated against source annotation data

## How to apply

For each sample information category (e.g., sample type), group all reanalyzed files by the chosen category value. For each unique chemical annotation (GNPS compound identifier or spectral match), count how many files within each group contain that chemical. Divide each count by the total number of files in that group and multiply by 100 to yield enrichment percentage: (count of files in group containing chemical) / (total files in group) × 100. Tabulate the result as a matrix with chemicals as rows and groups as columns, each cell containing the enrichment percentage [0, 100]. This normalization ensures groups of different sizes contribute equally to interpretation—a chemical present in 10 of 20 files (50%) in one group is directly comparable to one present in 5 of 10 files (50%) in another.

## Related tools

- **ReDU** (Loads sample-information templates and manages GNPS chemical annotation results; provides the file-level annotation data to be normalized) — https://github.com/mwang87/ReDU-MS2-GNPS
- **GNPS** (Provides chemical annotation (spectral library matches) for each file; annotations are grouped and counted per file within each group) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **Emperor** (Visualizes the normalized enrichment matrix as a PCA score plot for interactive exploration of chemical annotation patterns across groups) — https://github.com/biocore/emperor
- **MassIVE** (Public repository hosting the reanalyzed mass spectrometry files whose metadata and annotations feed into the normalization workflow) — https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp

## Evaluation signals

- All percentages in the enrichment matrix fall within [0, 100]; values outside this range indicate arithmetic or grouping errors.
- Row sums (sum of percentages for a single chemical across all groups) and column totals (sum of percentages for a group across all chemicals) match expected counts derived from the source GNPS annotation data and group membership.
- A chemical present in all files of a small group (e.g., 100% enrichment) and a subset of files in a large group (e.g., 50% enrichment) produces clearly different percentage values, enabling fair visual or statistical comparison in downstream PCA plots.
- Sample information metadata validation passes the ReDU template drag-and-drop validator before normalization, ensuring file-to-group assignments are correct.
- Cross-tabulation of grouped counts confirms that the sum of (enrichment percentage × group size) for each chemical equals the original count of files containing that chemical across all groups.

## Limitations

- Normalization by percentage obscures the absolute number of files and samples; a chemical present in 1 of 1 file (100%) in a singleton group may be flagged as equally enriched as one in 50 of 50 files (100%), leading to spurious biological conclusions. Practitioners should report both raw counts and percentages.
- The same chemical can have multiple GNPS annotations due to slight variation in MS2 spectra; preprocessing may be needed to cluster or collapse redundant annotations before enrichment tabulation, or annotation redundancy will artificially inflate the number of unique rows in the matrix.
- Percentage enrichment is sensitive to rare annotations in small groups; a single file in a 2-file group containing a unique chemical yields 50% enrichment despite low absolute prevalence. Consider filtering out chemicals observed in fewer than a minimum threshold (e.g., 2–3 files) before normalization.
- Metadata category selection is manual; choosing a category with many sparse subcategories (e.g., 'organism ID' with hundreds of unique values) can produce groups so small that percentages become uninformative or dominated by noise.

## Evidence

- [other] How should chemical annotations from re-analyzed public data grouped by sample information category be tabulated to enable valid comparison between groups with different numbers of files?: "How should chemical annotations from re-analyzed public data grouped by sample information category be tabulated to enable valid comparison between groups with different numbers of files?"
- [other] Percentages should be used to tabulate sample information enrichment for each chemical annotated across groups, enabling fair comparison when groups contain different file counts.: "Percentages should be used to tabulate sample information enrichment for each chemical annotated across groups, enabling fair comparison when groups contain different file counts."
- [other] Compute enrichment as (count of samples in group containing chemical) / (total samples in group) × 100 to yield percentage, normalizing for group-size imbalance.: "Compute enrichment as (count of samples in group containing chemical) / (total samples in group) × 100 to yield percentage, normalizing for group-size imbalance."
- [other] Tabulate results with rows as chemicals and columns as groups, displaying enrichment percentage in each cell.: "Tabulate results with rows as chemicals and columns as groups, displaying enrichment percentage in each cell."
- [other] Validate that row sums and group totals match the source annotation data and that all percentages fall within [0, 100].: "Validate that row sums and group totals match the source annotation data and that all percentages fall within [0, 100]."
- [abstract] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra cause the pattern to match different reference MS2 spectra"
- [methods] Manual completion of the ReDU sample information template: "Manual completion of the ReDU sample information template"
