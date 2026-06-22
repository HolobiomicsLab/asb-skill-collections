---
name: statistical-sub-cluster-detection
description: Use when you have a collection of Biosynthetic Gene Clusters that have been tokenised into Pfam domain and subPfam sequences and filtered for redundancy, and you seek to identify statistically significant groupings of genes that co-occur across multiple BGCs—particularly when downstream linking to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3928
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0204
  - http://edamontology.org/topic_3050
  tools:
  - iPRESTO
derived_from:
- doi: 10.1371/journal.pcbi.1010462
  title: iPRESTO
evidence_spans:
- iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters Tool) is a command line tool for the detection of gene sub-clusters
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ipresto_cq
    doi: 10.1371/journal.pcbi.1010462
    title: iPRESTO
  dedup_kept_from: coll_ipresto_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1010462
  all_source_dois:
  - 10.1371/journal.pcbi.1010462
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Statistical Sub-cluster Detection in Biosynthetic Gene Clusters

## Summary

Identifies statistically significant co-occurring domain patterns within tokenised and redundancy-filtered Biosynthetic Gene Clusters using the PRESTO-STAT algorithm. This skill discovers functionally coherent gene sub-clusters that may encode specific natural product substructures.

## When to use

Apply this skill when you have a collection of Biosynthetic Gene Clusters that have been tokenised into Pfam domain and subPfam sequences and filtered for redundancy, and you seek to identify statistically significant groupings of genes that co-occur across multiple BGCs—particularly when downstream linking to natural product substructures is planned.

## When NOT to use

- Input BGCs have not yet been tokenised into Pfam/subPfam domain representations
- Tokenised BGCs have not been filtered for redundancy; applying PRESTO-STAT to raw, unfiltered tokenised data will conflate signals across highly similar clusters
- The research goal is exploratory phenotyping or phylogenetic profiling rather than identifying functionally coherent sub-clusters linked to discrete biosynthetic outcomes

## Inputs

- Tokenised BGCs (Pfam domain + subPfam tokens per gene)
- Redundancy-filtered BGC collection (pre-filtered by Adjacency Index similarity network)

## Outputs

- Detected sub-clusters with constituent genes
- Domain compositions for each sub-cluster
- Genomic positions of sub-cluster members
- Statistical significance scores or p-values
- Structured sub-cluster records (JSON/tabular format)

## How to apply

Load redundancy-filtered tokenised BGCs (represented as Pfam domain and subPfam tokens per gene). Apply the PRESTO-STAT statistical algorithm, which is based on the methodology from Del Carratore et al. (2019), to detect statistically significant co-occurring domain patterns across the tokenised sequences. The algorithm identifies domain composition signatures that appear together more frequently than expected by chance. Extract detected sub-clusters recording their constituent genes, domain compositions, and genomic positions. Export results to a structured format (e.g., JSON or tabular) that preserves sub-cluster identity, member genes, domain tokens, and statistical significance scores.

## Related tools

- **iPRESTO** (Command-line tool that orchestrates tokenisation, redundancy filtering, and PRESTO-STAT sub-cluster detection on BGC collections) — https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1010462&type=printable

## Evaluation signals

- Detected sub-clusters are non-empty and contain at least 2 member genes with shared or complementary domain patterns
- Each sub-cluster record includes all required fields: constituent gene IDs, Pfam/subPfam domain tokens, genomic coordinates, and statistical significance (p-value or confidence score)
- Sub-clusters show higher within-cluster domain co-occurrence than expected in a permuted or random background distribution (as quantified by the PRESTO-STAT algorithm)
- Sub-cluster domain compositions are consistent with known biosynthetic modules or enzyme classes (e.g., adenylation + condensation + oxidoreductase combinations)
- No sub-cluster spans a genomic distance exceeding biologically plausible operonic or chromosomal linkage scales for the target organism

## Limitations

- PRESTO-STAT relies on statistical significance of domain co-occurrence; rare or novel domain combinations may be missed if sample size is small
- The method assumes Pfam and subPfam annotations are available and accurate; gaps or errors in reference databases propagate to sub-cluster detection
- Sub-clusters detected are correlative (co-occurring patterns) rather than directly evidence for functional co-regulation or co-expression
- Performance and sensitivity depend on upstream redundancy filtering parameters (Adjacency Index threshold); poorly tuned filtering may either over-collapse diverse sub-clusters or retain redundant copies that confound statistical signals

## Evidence

- [other] PRESTO-STAT is a sub-cluster detection method based on the statistical algorithm from Del Carratore et al. (2019), designed to identify gene sub-clusters within tokenised BGCs that have been filtered for redundancy.: "PRESTO-STAT is a sub-cluster detection method based on the statistical algorithm from Del Carratore et al. (2019), designed to identify gene sub-clusters within tokenised BGCs that have been filtered"
- [intro] BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [intro] Tokenised BGCs are filtered for redundancy using similarity network with an Adjacency Index of domains as a distance metric: "Tokenised BGCs are filtered for redundancy using similarity network with an Adjacency Index of domains as a distance metric"
- [intro] For the detection of sub-clusters two methods are used: PRESTO-STAT, which is based on the statistical algorithm from Del Carratore et al. (2019): "For the detection of sub-clusters two methods are used: PRESTO-STAT, which is based on the statistical algorithm from Del Carratore et al. (2019)"
- [intro] The sub-clusters found with iPRESTO can then be linked to Natural Product substructures: "The sub-clusters found with iPRESTO can then be linked to Natural Product substructures"
