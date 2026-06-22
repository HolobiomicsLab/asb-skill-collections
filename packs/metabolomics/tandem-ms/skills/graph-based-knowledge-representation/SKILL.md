---
name: graph-based-knowledge-representation
description: Use when annotating metabolites in untargeted metabolomics experiments where both established biochemical pathways and experimental MS2 similarity patterns must be simultaneously leveraged.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
  tools:
  - MrnAnnoAlgo3 (MetDNA3)
  - MetDNA3 webserver
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-025-63536-6
  title: MetDNA3
evidence_spans:
- '`MrnAnnoAlgo3` is the core algorithm module of **MetDNA3**, designed to annotate metabolites'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metdna3_cq
    doi: 10.1038/s41467-025-63536-6
    title: MetDNA3
  dedup_kept_from: coll_metdna3_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-63536-6
  all_source_dois:
  - 10.1038/s41467-025-63536-6
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-based-knowledge-representation

## Summary

Construct and integrate knowledge-driven and data-driven graph layers to represent metabolite relationships and enable recursive annotation propagation. This skill bridges biochemical ontologies and experimental similarity patterns into a unified interactive networking topology for metabolite annotation.

## When to use

Use this skill when annotating metabolites in untargeted metabolomics experiments where both established biochemical pathways and experimental MS2 similarity patterns must be simultaneously leveraged. Apply it specifically when a single annotation layer (pathway alone or spectral similarity alone) produces incomplete or low-confidence results, and you need to propagate identities across interconnected metabolite networks.

## When NOT to use

- Input metabolites lack reference biochemical pathway data or established relationships in public databases; the knowledge layer will be sparse and contribute minimal signal.
- Experimental MS2 data are missing or too noisy to compute reliable similarity scores; the data-driven layer cannot be meaningfully constructed.
- Metabolites are from a single, linear biosynthetic pathway with no branching or cross-talk; simpler sequential annotation methods are more appropriate and faster.

## Inputs

- Metabolite feature table with retention time and m/z values
- MS2 spectral similarity matrix or scored pairwise comparisons
- Biochemical pathway database (structured as nodes and edges)
- Reference metabolite annotations or known identity seeds
- Mass spectrometry dataset (experimental spectra)

## Outputs

- Annotated metabolite list with confidence scores per layer
- Two-layer interactive network graph (knowledge + data-driven)
- Annotation propagation trace (which metabolites informed which identities)
- Refined metabolite identities with updated confidence metrics

## How to apply

First, instantiate the knowledge-driven layer by encoding established metabolite relationships and biochemical ontologies as static graph structures with nodes representing metabolites and edges representing known biochemical transformations or pathway relationships. Second, construct the data-driven layer by computing feature similarity and co-occurrence patterns from mass spectrometry data, creating edges between metabolites with high MS2 spectral similarity or co-abundance patterns above a defined confidence threshold. Third, implement the interactive networking topology that enables simultaneous querying of both layers—metabolite nodes are enriched by traversing paths through both the knowledge graph and the data-driven similarity network. Finally, apply the recursive annotation propagation algorithm, which iteratively refines metabolite identities by updating confidence scores based on relationships and annotations propagated from both layers, repeating until convergence or a fixed iteration limit is reached.

## Related tools

- **MrnAnnoAlgo3 (MetDNA3)** (Core algorithm module that implements the two-layer interactive networking topology and recursive annotation propagation for metabolite annotation) — https://github.com/ZhuMetLab/MrnAnnoAlgo3
- **MetDNA3 webserver** (Web interface providing complete MetDNA3 functionality including the MrnAnnoAlgo3 algorithm with demo data and interactive tutorials) — http://metdna.zhulab.cn

## Examples

```
devtools::install_github("ZhuMetLab/MrnAnnoAlgo3"); library(MrnAnnoAlgo3); result <- MrnAnnoAlgo3::annotate_metabolites(feature_table, ms2_similarity_matrix, pathway_db, seed_annotations)
```

## Evaluation signals

- Consistency check: annotations from the combined two-layer model match reference annotations in a held-out test set with metabolites of known identity; compare against single-layer (knowledge-only or data-only) baseline.
- Coverage metric: percentage of input metabolites receiving confident annotations increases after recursive propagation, compared to initial seed annotations.
- Confidence score monotonicity: annotation confidence scores are non-decreasing across propagation iterations; scores should stabilize rather than oscillate.
- Graph topology invariant: the number of nodes and edges in both layers remains stable after layer construction; no spurious nodes or edges are created during propagation.
- Layer agreement: metabolites ranked high by the knowledge layer and data-driven layer exhibit correlated confidence; strong disagreement suggests data quality issues or misaligned thresholds.

## Limitations

- Recursive propagation relies on seed annotations of sufficient quality; poor initial annotations propagate errors through both layers and reduce final accuracy.
- Knowledge-driven layer effectiveness depends on completeness and currency of the underlying biochemical pathway database; gaps or outdated pathways limit annotation coverage.
- Data-driven layer threshold selection (e.g., MS2 similarity cutoff, co-abundance threshold) is not fully automated; suboptimal choices can fragment or over-connect the network, degrading propagation.
- Computational cost scales with network size; processing large datasets requires optimization; README reports processing a typical untargeted metabolomics dataset in one hour.

## Evidence

- [readme] Two-layer interactive networking topology combines knowledge-driven and data-driven layers for metabolite annotation: "designed to annotate metabolites through a two-layer interactive networking topology (knowledge-driven and data-driven) and recursive annotation propagation algorithms"
- [other] Knowledge-driven layer encodes biochemical pathways and ontologies: "Define the knowledge-driven layer components, incorporating established metabolite relationships and biochemical ontologies as static graph structures"
- [other] Data-driven layer derives from MS data similarity and co-occurrence: "Define the data-driven layer components, incorporating feature similarity and co-occurrence patterns derived from experimental mass spectrometry data"
- [other] Recursive propagation refines identities using confidence scores from both layers: "Implement the recursive annotation propagation algorithm that iteratively refines metabolite identities by leveraging confidence scores and relationships from both layers"
- [readme] Performance advantage over prior versions: "Processes a typical untargeted metabolomics dataset in just one hour—over 10-fold faster than previous versions"
