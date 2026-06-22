---
name: metadata-confidence-filtering
description: Use when you have curated structure-organism pairs from multiple sources and need to distinguish high-confidence, well-documented assertions from incomplete or conflicting records.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0091
  tools:
  - R
  - lotus-processor
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- db/../standardizing.R, common.R
- 1_integrating.R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus_cq
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.7554/eLife.70780
  all_source_dois:
  - 10.7554/eLife.70780
  - 10.1007/s00044-016-1764-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metadata-confidence-filtering

## Summary

Filter structure-organism pairs to retain only those meeting platinum-tier confidence standards by validating reference metadata, cross-checking against organism and structure dictionaries, and applying quality thresholds for high-confidence mappings. This skill ensures that curated natural products data meets reproducibility and completeness criteria before downstream analysis.

## When to use

Apply this skill when you have curated structure-organism pairs from multiple sources and need to distinguish high-confidence, well-documented assertions from incomplete or conflicting records. Specifically, use it after integration and organism/structure/reference cleaning when producing a publication-grade or downstream-analysis-ready collection that must support literature traceability and cross-database validation.

## When NOT to use

- Input is already a fully validated, externally peer-reviewed dataset with no missing or conflicting metadata — skip to downstream analysis.
- Reference dictionaries or metadata files are incomplete, outdated, or not yet synchronized with the curated table — defer filtering until dictionaries are refreshed.
- The analysis goal requires all curated pairs regardless of metadata completeness (e.g., exploratory curation audits, sensitivity analyses) — use the full curated table instead.

## Inputs

- interim/tables/3_curated/table.tsv.gz (curated structure-organism pair table)
- interim/dictionary/organism/dictionary.tsv.gz (organism reference dictionary)
- interim/dictionary/structure/dictionary.tsv.gz (structure reference dictionary)
- interim/dictionary/reference/dictionaryOrganism.tsv.gz (reference–organism linkage)
- interim/dictionary/reference/metadata.tsv.gz (reference metadata with authors, year, source)

## Outputs

- platinum.tsv.gz (validated platinum-tier structure-organism pair collection with validation flags and complete metadata)

## How to apply

Load the curated pair table (interim/tables/3_curated/table.tsv.gz) and three reference dictionaries (organism, structure, reference) along with their associated metadata files into R. Cross-reference each structure-organism pair against the organism dictionary (interim/dictionary/organism/dictionary.tsv.gz) and structure dictionary (interim/dictionary/structure/dictionary.tsv.gz) to confirm presence and consistency. Validate that each pair's literature citations have corresponding entries in reference metadata (interim/dictionary/reference/dictionaryOrganism.tsv.gz and metadata.tsv.gz), checking for completeness of author, year, and source fields. Retain only pairs that meet platinum-tier criteria: high-confidence mappings (e.g., no conflicting assertions across sources), complete metadata (no null critical fields), and validated reference links. Write passing pairs to platinum.tsv.gz with all validation flags and metadata columns preserved to enable traceability.

## Related tools

- **R** (Primary language for loading dictionaries, validating cross-references, and filtering pair tables in 2_validating.R) — https://www.r-project.org/
- **lotus-processor** (Parent workflow orchestrating 3_analyzing stage (which includes 2_validating.R) and producing platinum.tsv.gz as the validated collection) — https://github.com/lotusnprod/lotus-processor

## Evaluation signals

- Platinum collection size and composition: verify that platinum.tsv.gz contains fewer or equal pairs than the input curated table; document filtering rate (e.g., X% of curated pairs retained).
- Dictionary cross-reference completeness: spot-check 50–100 random pairs in platinum.tsv.gz to confirm each organism ID and structure ID appear in their respective dictionaries with matching metadata.
- Reference metadata validation: verify that all literature citations in platinum.tsv.gz have non-null author, year, and source fields; flag any rows with missing or contradictory reference IDs.
- No conflicting assertions: confirm that no structure-organism pair appears with contradictory organism or structure assignments (i.e., one CAS number mapped to two different organisms) in the platinum output.
- Schema and data type consistency: validate that platinum.tsv.gz matches the schema of the curated input table plus validation flag columns; confirm all numeric and categorical fields conform to expected types and ranges.

## Limitations

- Dictionary quality and timeliness: filtering relies on the completeness and correctness of organism, structure, and reference dictionaries; outdated or incomplete dictionaries will introduce false rejections or false acceptances.
- Conflicting-assertion detection: the method identifies direct contradictions but may miss subtle semantic inconsistencies (e.g., organism synonyms not reconciled in the dictionary, or structure stereoisomers incorrectly treated as identical).
- No changelog found — version history and updates not documented, making it difficult to track changes to validation criteria, dictionary content, or filtering thresholds across releases.
- Metadata completeness bias: filtering by reference metadata availability may systematically exclude older or less-cited natural products with sparse literature trails, even if scientifically valid.
- Dependency on external reference sources: if the underlying organism, structure, or reference dictionaries originate from 31 disparate external databases, their inherent inconsistencies or licensing restrictions may limit the platinum collection's scope.

## Evidence

- [other] The 2_validating.R step operates within the 3_analyzing stage as a validation filter that processes curated pairs and produces platinum.tsv.gz as its output.: "The 2_validating.R step operates within the 3_analyzing stage as a validation filter that processes curated pairs and produces platinum.tsv.gz as its output."
- [other] Load curated pairs and dictionaries, cross-reference against organism/structure/reference dictionaries, validate reference metadata, apply quality filters for platinum-tier standards, and write passing pairs to platinum.tsv.gz.: "Load the curated table (interim/tables/3_curated/table.tsv.gz) and reference dictionaries (organism, structure, reference) along with their metadata files using R. 2. Cross-reference each"
- [other] 588694 unique referenced structure-organism pairs from 42166 unique organisms, with 231330 unique curated structures in 3D format.: "588694 unique referenced structure-organism pairs (484174 in 3D|2D format) ... 231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms"
- [readme] LOTUS is a comprehensive collection of documented structure-organism pairs that should allow more complete understanding of organisms within computational approaches in Natural Products research.: "*LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented"
- [other] 3_analyzing: 1_sampling.R, 2_validating.R producing platinum.tsv.gz as part of the workflow pipeline.: "3_analyzing: 1_sampling.R, 2_validating.R producing platinum.tsv.gz"
