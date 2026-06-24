---
name: organism-taxonomy-identifier-mapping
description: Use when integrating organism records from 31 or more initial open databases
  with inconsistent taxonomy nomenclature, or when you need to count unique organisms
  in a validated structure-organism pair collection and verify the count against a
  known aggregate (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  tools:
  - R
  - Python 3
  - Kotlin
  license_tier: restricted
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- db/../standardizing.R, common.R
- 1_integrating.R
- Python scripts for data parsing and transformation
- 221[[smiles.py]]
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

# organism-taxonomy-identifier-mapping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Map and deduplicate organism taxonomy identifiers from heterogeneous natural products databases to produce a unified, validated organism reference set. This skill consolidates taxonomy data across multiple source formats and standardizations to enable accurate structure-organism pairing.

## When to use

Apply this skill when integrating organism records from 31 or more initial open databases with inconsistent taxonomy nomenclature, or when you need to count unique organisms in a validated structure-organism pair collection and verify the count against a known aggregate (e.g., 42166 unique organisms in LOTUS platinum).

## When NOT to use

- Input organisms are already deduplicated and validated against a single authoritative taxonomy source.
- You only need to retain raw organism records without deduplication or standardization.
- The analysis goal is structure validation only, not organism-structure pair validation.

## Inputs

- Raw organism records from multiple heterogeneous databases (as TSV/CSV or database tables)
- Organism taxonomy identifiers (species names, NCBI taxonomy IDs, or other nomenclatural forms)
- Reference taxonomy ontologies (Open Tree of Life, NCBI Taxonomy, or similar)

## Outputs

- Deduplicated organism taxonomy identifier set
- Count of unique organisms
- Validated organism reference table with standardized identifiers

## How to apply

Load the raw organism records from integrated database tables. Extract and normalize organism taxonomy identifiers using species binomial names, NCBI taxonomy IDs, or other canonical identifiers. Apply a cleaning pipeline (standardizing, translating, and validating taxonomy against reference ontologies such as OTL — Open Tree of Life) to remove duplicates and resolve synonyms. Deduplicate the normalized identifiers to obtain the final count of unique organisms. Compare the deduplicated count against the reported aggregate to validate correctness. The workflow typically proceeds through steps: 2_translating_organism (Kotlin), 3_cleaningTranslated.R (R), 4_cleaningTaxonomy.R (R), and 5_addingOTL.R (R), in the LOTUS processor pipeline.

## Related tools

- **R** (Execute organism taxonomy cleaning, translation, and validation scripts (3_cleaningTranslated.R, 4_cleaningTaxonomy.R, 5_addingOTL.R)) — https://github.com/lotusnprod/lotus-processor
- **Kotlin** (Translate and standardize organism taxonomy identifiers across database formats (2_translating_organism/main.kt)) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Parse and preprocess raw organism records before standardization) — https://github.com/lotusnprod/lotus-processor

## Examples

```
Rscript 4_cleaningTaxonomy.R --input organism_records.tsv --reference open-tree-of-life --output deduplicated_organisms.tsv
```

## Evaluation signals

- Deduplicated organism count matches the reported aggregate (42166 unique organisms in LOTUS platinum dataset).
- All organism records are linked to a valid taxonomy identifier (NCBI ID, OTL ID, or standardized binomial name).
- No duplicate organism identifiers remain in the output set after deduplication.
- Organism records passing validation match expected format: structured table with consistent columns for organism name, taxonomy ID, and source database.
- Comparison of input raw organism count vs. output deduplicated count shows expected reduction due to synonym/duplicate resolution.

## Limitations

- Taxonomy mapping accuracy depends on the quality and completeness of reference ontologies (OTL, NCBI); synonyms or obsolete names in source databases may not always resolve.
- Organisms with ambiguous or missing taxonomy identifiers in source records may be lost or require manual curation.
- Merging organisms across databases may conflate subspecific or strain-level distinctions if the reference taxonomy is coarser.
- The LOTUS processor workflow relies on R, Python 3, Java >= 17, and Make; results may vary across versions or operating systems (Windows requires dedicated setup).

## Evidence

- [methods] 42166 unique organisms count validation: "42166 unique organisms, with 588694 unique referenced structure-organism pairs"
- [methods] Multi-database integration and taxonomy standardization process: "originating from 31 initial open databases"
- [methods] Organism taxonomy cleaning workflow steps: "2_translating_organism, 3_cleaningTranslated.R, 4_cleaningTaxonomy.R, 5_addingOTL.R"
- [methods] Integrated organism subgraph in curation phase: "2_curating: 1_integrating.R, organism subgraph, structure subgraph, reference subgraph"
- [readme] LOTUS as comprehensive structure-organism pair resource: "LOTUS is a comprehensive collection of documented structure-organism pairs"
