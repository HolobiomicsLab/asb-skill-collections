---
name: group-wise-chemical-enrichment-calculation
description: Use when when comparing GNPS chemical annotations across two or more groups of samples (defined by ReDU sample-information categories such as sample type, extraction method, or ionization source) where the groups contain different numbers of files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-020-0916-7
  all_source_dois:
  - 10.1038/s41592-020-0916-7
  - 10.1186/2047-217x-2-16
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# group-wise-chemical-enrichment-calculation

## Summary

Normalize chemical annotation prevalence across sample groups with unequal file counts by computing per-group enrichment percentages, enabling fair comparative analysis of metabolite distribution in public mass spectrometry repositories.

## When to use

When comparing GNPS chemical annotations across two or more groups of samples (defined by ReDU sample-information categories such as sample type, extraction method, or ionization source) where the groups contain different numbers of files. Enrichment percentages are required to make valid statistical comparisons when group sizes are imbalanced.

## When NOT to use

- Input groups have already been normalized or enrichment percentages have already been computed from the same chemical annotation set.
- Sample-information categories are unknown or missing; the ReDU template has not been completed and validated.
- GNPS annotations have not been performed or chemical identifications are absent from the dataset.

## Inputs

- ReDU sample-information template (TSV format)
- GNPS chemical annotations for all samples
- Sample grouping category (string: sample type, extraction method, ionization source, etc.)

## Outputs

- Chemical enrichment table (rows=chemicals, columns=groups, values=enrichment percentages)
- Validated enrichment percentages within [0, 100] range
- Group size metadata for normalization verification

## How to apply

Load the ReDU sample-information template (TSV format) and the corresponding GNPS chemical annotations for all samples. Group samples by the selected sample-information category. For each group and each unique chemical (GNPS annotation), count how many samples in that group contain the chemical, then compute enrichment as (count of samples in group containing chemical) / (total samples in group) × 100. Tabulate results with rows as chemical compounds and columns as groups, with enrichment percentage in each cell. Validation is essential: row sums and group totals must match the source annotation data, and all percentages must fall within [0, 100]. This normalization method accounts for group-size imbalance and enables reliable downstream visualization (e.g., PCA score plots in Emperor) and statistical comparisons.

## Related tools

- **GNPS** (Performs spectral library matching to assign chemical annotations (level 2 or 3 by MSI standards) to MS/MS spectra; provides the annotation set used for enrichment calculation) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ReDU** (Hosts sample-information templates and organizes public MS/MS data by sample metadata; provides the grouping categories and sample-file associations used to stratify enrichment calculations) — https://github.com/mwang87/ReDU-MS2-GNPS
- **MassIVE** (Public mass spectrometry data repository that ReDU bridges to; source of the raw MS/MS data files and sample metadata) — https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp
- **Emperor** (Visualization tool that consumes the enrichment table to generate interactive PCA score plots for comparative exploration of chemical distributions across groups) — https://github.com/biocore/emperor

## Evaluation signals

- All enrichment percentages lie strictly within [0, 100]
- For each group, the sum of samples counted across all chemicals matches (total samples in group) × (number of unique chemicals), accounting for chemicals absent in some samples
- Row sums (total group membership across chemicals) and column sums (total chemical prevalence across groups) match source annotation counts
- Groups with different numbers of files now produce comparable enrichment values (e.g., a chemical present in 50% of samples in group A and 50% of samples in group B both yield 50%, regardless of group size)
- Downstream visualization (e.g., Emperor PCA) shows unbiased clustering patterns not driven by group-size artifacts

## Limitations

- The same chemical can have multiple GNPS annotations due to slight variation in MS2 spectra (m/z or abundance); manual or computational deduplication may be needed before enrichment calculation to avoid inflated chemical counts.
- Enrichment percentages do not account for spectral quality, annotation confidence scores, or the distinction between level 2 (putative annotation based on spectral library similarity) and level 3 (putatively characterized compound class) annotations; filtering by confidence threshold should be performed upstream.
- Sample-information template completion is manual and prone to missing or inconsistent entries; validation using the ReDU drag-and-drop validator is essential before enrichment calculation.

## Evidence

- [other] Percentages should be used to tabulate sample information enrichment for each chemical annotated across groups, enabling fair comparison when groups contain different file counts.: "Percentages should be used to tabulate sample information enrichment for each chemical annotated across groups, enabling fair comparison when groups contain different file counts."
- [other] For each group, enumerate the unique chemicals (GNPS annotations) present across all samples in that group and count the number of samples within the group containing each chemical. Compute enrichment as (count of samples in group containing chemical) / (total samples in group) × 100 to yield percentage, normalizing for group-size imbalance.: "For each group, enumerate the unique chemicals (GNPS annotations) present across all samples in that group and count the number of samples within the group containing each chemical. Compute"
- [other] Tabulate results with rows as chemicals and columns as groups, displaying enrichment percentage in each cell. Validate that row sums and group totals match the source annotation data and that all percentages fall within [0, 100].: "Tabulate results with rows as chemicals and columns as groups, displaying enrichment percentage in each cell. Validate that row sums and group totals match the source annotation data and that all"
- [other] Load the ReDU sample-information template (TSV format) and associated GNPS chemical annotations for all samples, grouping by the sample-information category selected (e.g., sample type, extraction method, ionization source).: "Load the ReDU sample-information template (TSV format) and associated GNPS chemical annotations for all samples, grouping by the sample-information category selected"
- [abstract] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra"
- [abstract] Chemical annotations originating from spectral library matching are considered level 2 or level 3 by the 2007 metabolomics standard initiative: "GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3"
