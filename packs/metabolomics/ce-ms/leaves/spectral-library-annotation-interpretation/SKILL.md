---
name: spectral-library-annotation-interpretation
description: Use when you have received chemical annotations from GNPS spectral library
  matching and need to (1) assess annotation confidence and validity for downstream
  analysis, (2) understand why the same chemical may appear under multiple GNPS annotation
  IDs, or (3) decide whether to collapse or deduplicate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
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
  provenance_tier: literature
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

# spectral-library-annotation-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpret and contextualizechemical annotations derived from tandem MS spectral library matching, accounting for annotation confidence levels and spectral variation artifacts that produce multiple annotations for the same compound. This skill is essential when working with GNPS spectral library identifications to understand their limitations and ensure valid downstream statistical or visualization comparisons.

## When to use

You have received chemical annotations from GNPS spectral library matching and need to (1) assess annotation confidence and validity for downstream analysis, (2) understand why the same chemical may appear under multiple GNPS annotation IDs, or (3) decide whether to collapse or deduplicate annotations before tabulating enrichment across sample groups for visualization or statistical testing.

## When NOT to use

- Input annotations are already at the canonical compound level (i.e., deduplicated and merged by chemical identity) — skip the deduplication step and interpret annotations as final.
- Your analysis goal does not require cross-group comparison or does not depend on normalized sample counts — percentage enrichment normalization may be unnecessary.
- Annotation confidence is not a concern for your downstream use case (e.g., exploratory visualization only) — you may choose to skip confidence classification, but document this decision.

## Inputs

- GNPS chemical annotation table (tab-separated or CSV) with columns: annotation ID, compound name, MS2 similarity score, sample ID
- ReDU sample-information template (TSV format) with rows as samples and columns as metadata categories
- Sample grouping variable (e.g., sample type, extraction method, ionization source)

## Outputs

- Enrichment tabulation matrix with rows as GNPS annotations (or canonical compounds) and columns as sample groups, each cell containing percentage enrichment (0–100)
- Annotation confidence classification report (level 2 vs. level 3 per annotation)
- Deduplication mapping (if applied) linking multiple GNPS annotation IDs to canonical compound names
- Validation summary confirming row/group totals match source data and all percentages are within valid range

## How to apply

First, classify all GNPS annotations according to the 2007 Metabolomics Standards Initiative framework: level 2 annotations are putative identifications based on spectral library similarity (MS2 pattern matching), while level 3 are putatively characterized compound classes. Recognize that slight variations in MS2 spectra (m/z or abundance differences) will cause the same chemical to match different reference spectra and receive multiple distinct GNPS annotation IDs. When tabulating chemical enrichment across sample groups (for example, grouping by sample type, extraction method, or ionization source), decide whether to treat multiple annotations of the same chemical as separate entities or merge them into a single canonical compound entry. Document this decision and apply it consistently. Compute enrichment as (count of samples in group containing annotation) / (total samples in group) × 100 to normalize for group-size imbalance. Validate that row sums and group totals match the source annotation data and that all percentages fall within [0, 100]. When visualizing results in Emperor via PCA score plots, ensure that the enrichment tabulation accurately reflects the annotation-to-sample mapping from your source data.

## Related tools

- **GNPS** (Provides spectral library matching and chemical annotation IDs; spectral matching engine assigns MS2 spectra to reference library compounds) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ReDU** (Bridges GNPS annotations and sample metadata; provides interface to group annotations by sample information categories and filter by metadata attributes) — https://github.com/mwang87/ReDU-MS2-GNPS
- **Emperor** (Interactive visualization tool for displaying enrichment tabulation results as PCA score plots and interactive plots; enables exploration of annotation patterns across sample groups) — https://github.com/biocore/emperor
- **MassIVE** (Public repository hosting raw tandem MS data files; source of data linked to sample information and GNPS annotations) — https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp

## Evaluation signals

- Enrichment percentages for all annotations fall within [0, 100] with no negative or >100 values.
- Sum of enrichment values across all groups for each annotation matches the expected frequency based on source annotation data.
- Group totals (sum of all annotations in a group) are consistent with the number of unique samples and annotated compounds in that group.
- Multiple GNPS annotation IDs for the same chemical are either merged into a single row or clearly flagged as duplicates in the output, with deduplication logic documented.
- Annotation confidence classification (level 2 vs. level 3) is recorded and reported; any filtering or weighting by confidence level is justified and reproducible.

## Limitations

- The same chemical can have multiple GNPS annotations due to slight variation in MS2 spectra (m/z or abundance), leading to annotation ambiguity and potential inflated enrichment counts if deduplication is not applied.
- GNPS annotations via spectral library matching are level 2 or level 3 confidence (not confirmed structure); they should not be treated as definitively identified compounds without orthogonal validation.
- Enrichment percentages depend critically on the sample grouping variable chosen; different grouping schemes (e.g., sample type vs. extraction method) may yield different enrichment patterns and require separate interpretation.
- Group-size imbalance is only corrected via percentage normalization; statistical significance testing (e.g., chi-square or Fisher's exact test) is not performed and would require additional analysis.

## Evidence

- [abstract] Chemical annotations originating from spectral library matching are considered level 2 or level 3 by the 2007 metabolomics standard initiative: "GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on"
- [abstract] Same chemical multiple GNPS annotations due to spectral variation: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical"
- [other] Percentages normalize enrichment for group-size imbalance: "Percentages should be used to tabulate sample information enrichment for each chemical annotated across groups, enabling fair comparison when groups contain different file counts."
- [other] Enrichment computation formula with percentage normalization: "Compute enrichment as (count of samples in group containing chemical) / (total samples in group) × 100 to yield percentage, normalizing for group-size imbalance."
- [other] Validation of tabulation with row/group total consistency: "Validate that row sums and group totals match the source annotation data and that all percentages fall within [0, 100]."
- [other] ReDU grouping by sample information categories: "grouping by the sample-information category selected (e.g., sample type, extraction method, ionization source)"
