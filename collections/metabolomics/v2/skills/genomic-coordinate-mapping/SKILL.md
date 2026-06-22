---
name: genomic-coordinate-mapping
description: Use when after sub-clusters have been detected by PRESTO-STAT or PRESTO-TOP statistical methods on tokenised and redundancy-filtered BGCs, and you need to report their precise genomic positions, gene locus tags, and orientations for integration with natural product substructure predictions or for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3106
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0749
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
---

# Genomic Coordinate Mapping

## Summary

Map detected biosynthetic sub-clusters back to their genomic positions within original BGC sequences, preserving locus tag, contig, and strand information to enable linking of structural predictions to physical genome locations. This skill is essential for grounding computational sub-cluster discoveries in genomic reality and facilitating downstream validation or visualization.

## When to use

After sub-clusters have been detected by PRESTO-STAT or PRESTO-TOP statistical methods on tokenised and redundancy-filtered BGCs, and you need to report their precise genomic positions, gene locus tags, and orientations for integration with natural product substructure predictions or for wet-lab validation and genome browser visualization.

## When NOT to use

- Tokenised BGCs have lost or do not carry genomic coordinate metadata during preprocessing — coordinate mapping cannot be performed without the original positional annotations.
- The analysis goal is purely comparative (e.g., identifying universal domain patterns across BGCs) and does not require grounding results in physical genome positions.
- Input sub-clusters are from computationally inferred or synthetic gene clusters without canonical genomic coordinates.

## Inputs

- Redundancy-filtered tokenised BGCs with retained genomic coordinate metadata (contig, strand, locus tag per gene)
- Detected sub-cluster membership (gene indices, domain compositions from PRESTO-STAT or PRESTO-TOP output)
- Original BGC GenBank or GFF3 annotations linking tokens to genomic features

## Outputs

- Sub-cluster genomic feature table (GFF3 or GenBank format) with locus tags, contig IDs, strand, start/end positions
- Structured sub-cluster records with genomic coordinates and constituent gene annotations
- Genome browser–compatible output (BED, GFF3, or custom JSON) for visualization

## How to apply

Retain genomic coordinate metadata (contig identifier, start/end positions, strand orientation, locus tags) throughout the tokenisation and redundancy-filtering pipeline. When sub-clusters are extracted after statistical detection, cross-reference the detected domain token patterns back to the original gene records using their position indices within the tokenised sequence. Reconstruct the genomic intervals by mapping each detected gene (identified by its token position and domain composition) to its corresponding genomic feature annotation, preserving strand and contig information. Export the detected sub-clusters with their constituent genes' genomic positions, locus tags, and orientations in structured format (e.g., GFF3 or GenBank feature table) to enable downstream linkage to natural product substructure annotations and integration with genome browsers.

## Related tools

- **iPRESTO** (Performs tokenisation, redundancy filtering, and sub-cluster detection; outputs must retain or annotate genomic coordinates for downstream mapping)

## Evaluation signals

- Every detected sub-cluster gene is successfully mapped to a unique locus tag, contig, strand, and genomic interval with no unmapped or ambiguous assignments.
- Genomic intervals are consistent with the original GenBank/GFF3 annotations: no coordinate mismatches, strand flips, or out-of-bounds positions.
- Output schema validates against GFF3 or GenBank feature table specification; all required fields (seqname, source, feature, start, end, score, strand, frame, attributes) are populated correctly.
- Locus tags in mapped output are traceable back to the original input BGC records and match the corresponding tokenised gene positions exactly.
- Genome browser (e.g., IGV, JBrowse) can successfully parse and display the exported coordinates without coordinate conversion errors.

## Limitations

- Genomic coordinate mapping fails or produces ambiguous results if tokenisation process discards or anonymises locus tag or positional metadata; metadata preservation must be enforced upstream.
- Redundancy filtering using similarity networks may merge or deduplicate similar BGCs, potentially creating ambiguity in coordinate assignment if not carefully tracked.
- Sub-clusters that span disjoint genomic regions or multiple contigs require special handling to preserve non-contiguous interval information in output format.
- Natural Product substructure linkage predictions are independent of genomic coordinate mapping; correct coordinates alone do not validate the correctness of structure–cluster associations.

## Evidence

- [other] Extract and record detected sub-clusters with their constituent genes, domain compositions, and genomic positions.: "Extract and record detected sub-clusters with their constituent genes, domain compositions, and genomic positions."
- [intro] BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution: "BGCs are tokenised by representing each gene as a combination of its Pfam domains, where subPfams are used to increase resolution"
- [intro] The sub-clusters found with iPRESTO can then be linked to Natural Product substructures: "The sub-clusters found with iPRESTO can then be linked to Natural Product substructures"
- [intro] a set of Biosynthetic Gene Clusters (BGCs) in GenBank format: "a set of Biosynthetic Gene Clusters (BGCs) in GenBank format"
