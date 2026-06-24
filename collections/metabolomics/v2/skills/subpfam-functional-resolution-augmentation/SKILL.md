---
name: subpfam-functional-resolution-augmentation
description: Use when you have annotated genes with Pfam domains but require higher
  functional specificity to detect natural product sub-clusters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2431
  edam_topics:
  - http://edamontology.org/topic_0102
  - http://edamontology.org/topic_0621
  tools:
  - iPRESTO
  - Pfam domain scanner
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1010462
  title: iPRESTO
evidence_spans:
- iPRESTO (integrated Prediction and Rigorous Exploration of biosynthetic Sub-clusters
  Tool) is a command line tool for the detection of gene sub-clusters
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# subpfam-functional-resolution-augmentation

## Summary

This skill augments Pfam domain annotations with subPfam assignments to increase functional resolution when tokenizing individual genes in Biosynthetic Gene Clusters. It enables finer-grained domain-level representation suitable for detecting functionally coherent sub-clusters within larger BGCs.

## When to use

Apply this skill when you have annotated genes with Pfam domains but require higher functional specificity to detect natural product sub-clusters. Use it specifically when Pfam-level annotation alone produces over-broad domain tokens that obscure functionally distinct sub-domains, or when linking detected sub-clusters to specific natural product substructures requires domain-level granularity beyond standard Pfam assignments.

## When NOT to use

- Input genes have not yet been scanned for Pfam domains; perform standard Pfam annotation first.
- Downstream analysis does not require sub-cluster detection or natural product substructure linking; standard Pfam tokens may be sufficient for coarser-grained clustering tasks.
- Genes belong to non-biosynthetic pathways where Pfam/subPfam domain architecture is not the primary discriminator.

## Inputs

- GenBank-format BGC sequence files
- Gene sequences annotated with Pfam domain assignments
- Pfam domain identifiers and boundaries per gene

## Outputs

- Tokenized BGC representation (one token string per gene, combining Pfam domains and subPfams)
- Gene-level annotation objects enriched with subPfam metadata

## How to apply

After initial Pfam domain scanning of BGC genes, systematically augment each Pfam annotation with its corresponding subPfam assignment to increase resolution. Represent each gene as a token string combining both Pfam domains and their subPfam refinements. This dual-level representation preserves broad functional categories (via Pfams) while capturing fine-grained functional distinctions (via subPfams) needed for subsequent sub-cluster detection methods like PRESTO-STAT or PRESTO-TOP. The rationale is that subPfams partition Pfam domains into functionally distinct subtypes, allowing the similarity network filtering and sub-cluster detection steps to discriminate between genes with related but non-identical biosynthetic roles.

## Related tools

- **iPRESTO** (Command-line tool that executes BGC tokenization using Pfam and subPfam domains as part of its integrated sub-cluster detection pipeline)
- **Pfam domain scanner** (Upstream tool for initial Pfam domain assignment; provides the base annotations that are subsequently augmented with subPfams)

## Evaluation signals

- Each gene in the tokenized output contains both Pfam and subPfam identifiers in its token string; verify no gene is represented by Pfam domains alone.
- Token strings show increased specificity compared to Pfam-only representation; subPfam tokens refine broad Pfam categories into distinct functional subtypes.
- Downstream similarity network filtering produces non-trivial redundancy reduction, indicating that subPfam augmentation enabled meaningful discrimination among BGCs.
- Sub-clusters detected after augmentation show tighter functional coherence and stronger linkage to specific natural product substructures than pre-augmentation results.
- Audit log or token comparison confirms subPfam assignments are non-empty and systematic across all genes; no missing or spurious subPfam entries.

## Limitations

- Augmentation depends on the completeness and accuracy of the underlying Pfam domain database; genes lacking Pfam annotation cannot be augmented.
- SubPfam assignments may not exist for all Pfam domains; augmentation coverage may be partial, requiring fallback to Pfam-only representation for unaugmented domains.
- Increased dimensionality from dual-level annotation may inflate computational cost in large-scale BGC screening; trade-off between resolution and scalability should be considered.
- The quality of sub-cluster detection and natural product linkage depends critically on downstream filtering and statistical methods (PRESTO-STAT, PRESTO-TOP); augmentation alone does not guarantee valid or interpretable results.

## Evidence

- [other] Each gene in a BGC is tokenised by representing it as a combination of its Pfam domains, with subPfams employed to increase resolution of the domain annotation.: "Each gene in a BGC is tokenised by representing it as a combination of its Pfam domains, with subPfams employed to increase resolution of the domain annotation."
- [intro] BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [other] Represent each gene as a token string combining its Pfam domains and subPfams.: "Represent each gene as a token string combining its Pfam domains and subPfams."
- [intro] The sub-clusters found with iPRESTO can then be linked to Natural Product substructures: "The sub-clusters found with iPRESTO can then be linked to Natural Product substructures"
- [intro] Tokenise BGCs using Pfam domains and subPfams: "iPRESTO detects gene sub-clusters in Biosynthetic Gene Clusters by tokenizing BGCs using Pfam domains and subPfams"
