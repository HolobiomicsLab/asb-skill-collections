---
name: annotation-confidence-assessment
description: Use when after MS-FINDER in silico annotation has been executed on exported LC-MS features and multiple database matches (with HRR scores) have been returned.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MS-CleanR
  - MS-FINDER
  - MS-DIAL
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_cleanr_cq
    doi: 10.1021/acs.analchem.0c01594
    title: MS-CleanR
  dedup_kept_from: coll_ms_cleanr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01594
  all_source_dois:
  - 10.1021/acs.analchem.0c01594
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# annotation-confidence-assessment

## Summary

Evaluate and rank in silico metabolite annotations from MS-FINDER by consolidating hydrogen rearrangement rules (HRR) scores across multiple database matches and prioritizing results according to user-defined criteria. This skill ensures only high-confidence compound identifications are retained in the final LC-MS feature annotation table.

## When to use

Apply this skill after MS-FINDER in silico annotation has been executed on exported LC-MS features and multiple database matches (with HRR scores) have been returned. Use it when you need to consolidate per-feature annotations into a unified, prioritized annotation table and merge results back into the filtered peak list while reducing false-positive identifications.

## When NOT to use

- Input data lack MS/MS spectra — MS-CleanR discards all features without MS/MS during the first filtering step, and MS-FINDER requires MS/MS for annotation.
- Features have not been exported to MS-FINDER yet — this skill operates on MS-FINDER results, not raw peak lists or pre-annotation filtered features.
- No multiple databases are available for cross-validation — the skill's value is in comparing HRR scores across database matches; single-database annotations cannot be ranked by prioritization rules.

## Inputs

- MS-FINDER output files (compound ID, HRR score, database match, structural predictions per feature)
- MS-CleanR filtered and clustered feature table (m/z, retention time, MS/MS spectra, feature clusters)

## Outputs

- Unified annotation table (feature ID, m/z, retention time, best-match compound ID, HRR score, database source, prioritization rank)
- Annotated peak list merged with original MS-CleanR filtered feature metadata

## How to apply

Parse MS-FINDER results to extract per-feature annotations including compound ID, HRR score, database source, and structural predictions. Compare scores across multiple database matches for each feature and apply user-defined prioritization rules (e.g., highest HRR score, database hierarchy, structural likelihood). Consolidate duplicate or conflicting annotations by selecting the highest-confidence match according to your priority schema. Merge the prioritized annotations into the MS-CleanR filtered peak list, preserving m/z, retention time, and clustering metadata. The rationale is that HRR scoring reflects the probability of hydrogen rearrangement pathways in fragmentation, so higher scores indicate more chemically plausible annotations; database priority reflects domain-specific trust (e.g., prioritizing plant metabolite databases for botanical samples).

## Related tools

- **MS-FINDER** (Executes in silico annotation and generates HRR scores and database matches that are parsed and prioritized by this skill) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Produces filtered and clustered feature table and exports features to MS-FINDER; receives prioritized annotations merged back into peak list) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-DIAL** (Upstream tool; generates peak list and peak character estimation used by MS-CleanR before annotation export) — http://prime.psc.riken.jp/compms/index.html

## Examples

```
# After MS-FINDER annotation, merge results with MS-CleanR filtered features:
# library(mscleanr); annotated_features <- merge_annotations(msfinder_results, cleanr_features, priority_db=c('NIST','PubChem'), score_threshold=0.5)
```

## Evaluation signals

- HRR scores for retained annotations are above a user-defined threshold (e.g., score > 0.5); lower-scoring matches are filtered or marked as low-confidence.
- No feature in the output annotation table lacks a prioritized compound ID and HRR score; all exported features are accounted for.
- Annotations from multiple databases for the same feature are consolidated to a single row per feature, with priority ranking recorded (e.g., database 1 vs. database 2 match for the same m/z).
- The final merged peak list retains all original MS-CleanR metadata columns (m/z, retention time, cluster ID, RSD/RMD filter flags) alongside new annotation columns (compound ID, HRR score, database source).
- Visual or statistical inspection shows no annotation conflicts (e.g., two different compound IDs for the same feature with identical high HRR scores) — conflicts either resolved by database priority or flagged as ambiguous.

## Limitations

- At least 3 blank and 3 QC samples must be correctly identified in the MS-DIAL sample list for upstream filtering; missing or mislabeled QC samples degrade feature quality before annotation.
- All features without MS/MS spectra are discarded during the first MS-CleanR step, so MS1-only data will cause the workflow to crash before annotation can occur.
- HRR scoring prioritizes fragmentation chemistry plausibility but does not replace orthogonal validation (e.g., retention time standards, MS/MS library matching, or NMR confirmation); high HRR scores alone do not guarantee biological relevance.
- Known R version incompatibility: 'Error: the condition has length > 1' during database annotation merging if using R > 4.2; user must downgrade R or await patched version.
- The tool is no longer actively maintained; active development shifted to MS-DIAL 5.x, which integrates parts of MS-CleanR functionality.

## Evidence

- [readme] all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system. At this step, multiple databases can be queried: "all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system. At this step, multiple databases can be queried"
- [other] Parse MS-FINDER results and consolidate per-feature annotations (compound ID, score, database match, structural predictions) into a unified annotation table.: "Parse MS-FINDER results and consolidate per-feature annotations (compound ID, score, database match, structural predictions) into a unified annotation table."
- [readme] The final step will merge annotation results to the filtered peak list by prioritizing database annotation depending on user choice.: "The final step will merge annotation results to the filtered peak list by prioritizing database annotation depending on user choice."
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
- [readme] At least 3 blanks and 3 QCs samples are needed for Blank ratio analysis. These samples must be identified as such in the MS-Dial sample list.: "At least 3 blanks and 3 QCs samples are needed for Blank ratio analysis. These samples must be identified as such in the MS-Dial sample list."
