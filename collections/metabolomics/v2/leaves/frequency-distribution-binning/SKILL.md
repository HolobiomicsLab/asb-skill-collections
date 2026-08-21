---
name: frequency-distribution-binning
description: Use when you have loaded a table of entity–attribute pairs (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  tools:
  - R
  - Python 3
  - lotus-processor
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- standardizing.R, 1_integrating.R, 1_cleaningOriginal.R, 4_cleaningTaxonomy.R, 5_addingOTL.R
- 1_integrating.R
- 221[[smiles.py]], 260[[3_cleaningAndEnriching/sanitizing.py]], 280[[3_cleaningAndEnriching/stereocounting.py]]
- R - Python 3 - Java >= 17
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus
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

# frequency-distribution-binning

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Partitions a collection of unique entities (e.g., 2D chemical structures) into discrete frequency bins based on a count attribute (e.g., organism prevalence), then tallies membership in each bin and compares results against a gold-standard reference. This skill enables validation of large structure–organism pair databases and reveals the diversity distribution of chemical scaffolds across biological systems.

## When to use

Apply this skill when you have loaded a table of entity–attribute pairs (e.g., structure–organism associations in LOTUS), need to understand the prevalence distribution of unique entities across a categorical or ordinal dimension, must validate whether your counts match published or expected totals, and want to stratify downstream analyses or discovery by prevalence strata.

## When NOT to use

- Input is already a pre-aggregated frequency distribution (i.e., counts per bin are already computed); skip directly to validation and reporting.
- No ground truth or expected distribution is available and the analysis goal is not comparative; in this case, descriptive binning may proceed without validation logic.
- Entity counts in the source table are already normalized or transformed (e.g., log-scaled or percentile-ranked); re-binning on transformed counts will conflate the transformation with the binning strategy.

## Inputs

- Structure–organism pairs table (TSV or flat file with entity ID and count or organism list)
- Definition of frequency bins (thresholds and labels)
- Gold-standard reference counts (if available for validation)

## Outputs

- Bin membership counts (number of entities per bin)
- Summary report documenting bin distribution and discrepancies
- Optionally: stratified entity lists grouped by prevalence bin

## How to apply

Load the structure–organism pairs table (or analogous entity–attribute table) into a tabular format (TSV, CSV, or R/Python dataframe). Group all unique entities (structures) by their associated count in the target dimension (organism count). Define frequency bins that align with biological or analytical hypotheses—for LOTUS, the bins are singleton structures (1 organism), low-diversity (2–10 organisms), medium-diversity (11–100 organisms), and high-diversity (>100 organisms). Count the number of entities in each bin, generate a summary report, and compare bin membership counts against the published gold-standard totals. Discrepancies indicate potential data cleaning issues, missing records, or schema mismatches that should be investigated before downstream use.

## Related tools

- **R** (Grouping, binning, and summarization of structure–organism counts; report generation and comparison against gold-standard totals) — https://www.r-project.org
- **Python 3** (Alternative implementation for loading, grouping, binning, and validating entity–count distributions in tabular form) — https://www.python.org
- **lotus-processor** (Repository providing the complete LOTUS workflow, including data curation, structure–organism pair assembly, and validation pipelines) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# Load LOTUS structure–organism pairs; group by organism count; bin into frequency classes
lotus_table <- read.table('lotus_structure_organism_pairs.tsv', sep='\t', header=TRUE)
organism_counts <- table(lotus_table$structure_id)
bins <- data.frame(structure_id=names(organism_counts), count=as.numeric(organism_counts))
bins$bin <- ifelse(bins$count==1, 'singleton', ifelse(bins$count<=10, 'low_diversity', ifelse(bins$count<=100, 'medium_diversity', 'high_diversity')))
summary_report <- table(bins$bin)
print(summary_report)
```

## Evaluation signals

- Bin membership counts match the published gold-standard totals (or documented discrepancies are fully explained and tracked)
- All unique entities appear in exactly one bin; no entity is miscounted or assigned to multiple bins
- The sum of counts across all bins equals the total number of unique entities in the input table
- Bin boundaries are consistent with the defined thresholds (e.g., no structure with 1 organism is classified as low-diversity)
- A summary report is produced documenting bin labels, membership counts, and any reconciliation notes against reference data

## Limitations

- Binning thresholds are arbitrary and domain-specific; the LOTUS thresholds (1, 2–10, 11–100, >100) may not generalize to other entity–count distributions or research questions.
- This skill assumes the input entity–attribute pairs are already deduplicated and correctly curated; upstream errors in data cleaning or integration will propagate into incorrect bin assignments.
- If the gold-standard reference totals are themselves incorrect or outdated, discrepancies will not reveal the true source of mismatch.
- Large datasets (e.g., >500k entities) may require memory-efficient implementations or streaming approaches not detailed in the LOTUS workflow.

## Evidence

- [other] Group all unique 2D structures by their associated organism count.: "Group all unique 2D structures by their associated organism count."
- [other] Bin structures into four frequency bins: singleton structures (1 organism), low-diversity structures (2–10 organisms), medium-diversity structures (11–100 organisms), and high-diversity structures (>100 organisms).: "Bin structures into four frequency bins: singleton structures (1 organism), low-diversity structures (2–10 organisms), medium-diversity structures (11–100 organisms), and high-diversity structures"
- [other] Count the number of structures in each bin and compare against the reported gold-standard counts.: "Count the number of structures in each bin and compare against the reported gold-standard counts."
- [other] Generate a summary report documenting bin membership counts and any discrepancies.: "Generate a summary report documenting bin membership counts and any discrepancies."
- [readme] LOTUS is a comprehensive collection of documented structure-organism pairs designed to enable computational understanding of organisms and their chemistry.: "LOTUS is a comprehensive collection of documented structure-organism pairs designed to enable computational understanding of organisms and their chemistry."
- [methods] 588694 | 484174 (3D|2D) unique referenced structure-organism pairs: "588694 | 484174 (3D|2D) unique referenced structure-organism pairs"
