---
name: biosynthetic-gene-cluster-detection-and-annotation
description: Use when you have assembled microbial genomes (nucleotide FASTA files) and want to identify biosynthetic potential and group related BGCs for downstream linking with metabolomic data;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0436
  edam_topics:
  - http://edamontology.org/topic_0204
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0621
  tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- NPLinker, a software framework to link genomic and metabolomic data
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  - 10.1371/journal.pcbi.1008920
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biosynthetic-gene-cluster-detection-and-annotation

## Summary

Detect BGCs in microbial genomes using antiSMASH and annotate them by clustering into Gene Cluster Families (GCFs) using BiG-SCAPE based on product class and structural similarity. This enables systematic integration of genomic predictions with metabolomic data for natural product discovery.

## When to use

You have assembled microbial genomes (nucleotide FASTA files) and want to identify biosynthetic potential and group related BGCs for downstream linking with metabolomic data; particularly when you plan to correlate genomic BGC clusters with metabolomic spectra or molecular families to discover BGC–metabolite relationships.

## When NOT to use

- Input genomes are unassembled or consist of raw sequencing reads rather than contigs/scaffolds.
- You already have manually curated or experimentally validated BGC annotations and do not need de novo prediction.
- The research goal focuses only on genomic variation without requiring integration with metabolomic data or natural product structure prediction.

## Inputs

- Microbial genome assemblies (FASTA format)
- antiSMASH v5.0.0 configuration parameters (e.g., hmm detection method, minimal cluster size)

## Outputs

- BGC predictions with genomic coordinates, gene annotations, and predicted product classes
- Gene Cluster Families (GCFs) with member BGCs grouped by structural similarity and product class
- BGC–strain associations and hierarchical BGC→GCF object relationships for in-memory representation

## How to apply

Run antiSMASH v5.0.0 on input microbial genome assemblies to predict BGCs, extracting genomic coordinates, predicted product classes, and gene annotations. Then apply BiG-SCAPE v1.0.0 to cluster the detected BGCs into GCFs by computing pairwise structural similarity distances and grouping BGCs with the same product class and similarity distance below a specified threshold. This hierarchical organization (BGC → GCF) preserves strain–BGC associations and enables efficient scoring and filtering when creating hypothetical links to metabolomic data. The resulting GCF assignments and BGC metadata (product type, MIBiG homology scores if available) become the genomic input to downstream scoring functions.

## Related tools

- **antiSMASH** (Detects and annotates biosynthetic gene clusters in genome assemblies, identifying product classes and gene boundaries)
- **BiG-SCAPE** (Clusters detected BGCs into Gene Cluster Families based on structural similarity distance and product class, grouping related BGCs for comparative analysis)
- **NPLinker** (Constructs in-memory representations of BGCs and GCFs, maintains strain–BGC associations, and integrates with metabolomic data for hypothesis generation) — https://github.com/sdrogers/nplinker
- **MIBiG** (Reference database of experimentally validated BGC structures; used to assign structural homology to predicted BGCs via cumulative BLAST score (threshold ≥10,000))

## Examples

```
# Run antiSMASH on genome assembly, then cluster BGCs into GCFs
antismash --genefinding-tool prodigal --html --output antismash_out genome.fasta
big-scape --inputfile antismash_out/genbank_output/ --output_dir big_scape_out --cutoff 0.3
```

## Evaluation signals

- BGC predictions are present for all input genomes and include product class annotations; antiSMASH output contains genomic coordinates and gene feature tables.
- All detected BGCs are successfully assigned to a GCF; no BGCs remain orphaned or unclassified after BiG-SCAPE clustering.
- GCF membership is consistent with product class: BGCs within the same GCF belong to the same predicted product type (e.g., all PKS or all NRP-PKS hybrid).
- Strain–BGC associations are preserved: each BGC is linked to the source genome, enabling strain correlation scoring in subsequent linking steps.
- MIBiG homology scores (if computed) follow the thresholds documented in the article: only BGCs with cumulative BLAST score ≥10,000 are retained for IOKR scoring.

## Limitations

- antiSMASH predictions depend on the quality and completeness of the input genome assembly; fragmented or low-coverage genomes may yield incomplete or absent BGC calls.
- BiG-SCAPE clustering is sensitive to the choice of similarity distance threshold and product class definitions; different thresholds yield different GCF compositions.
- The method does not directly predict metabolite structures from BGC sequences; structural annotation relies on MIBiG homology matching, which limits applicability to BGCs with considerable sequence identity to experimentally characterized clusters.
- Predictions are biased toward well-characterized bacterial and fungal natural product pathways; rare or novel BGC types may be missed or misclassified.

## Evidence

- [abstract] The most popular tool for BGC prediction in microbial genomes is antiSMASH: "The most popular tool for BGC prediction in microbial genomes is antiSMASH"
- [abstract] The current state-of-the-art tools for microbial BGC clustering are BiG-SCAPE and BiG-SLICE: "The current state-of-the-art tools for microbial BGC clustering are BiG-SCAPE [13] and BiG-SLICE [21]"
- [abstract] Genomes were run through antiSMASH v5.0.0 for BGC detection and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs: "after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs"
- [results] Both BGCs belonging to the product class PKS-NRP Hybrid, BiG-SCAPE considers them as belonging to the same cluster: "Because both of them belong to the product class "PKS-NRP Hybrid", BiG-SCAPE considers them as belonging to the same cluster"
- [other] NPLinker creates objects for spectra, MFs, BGCs and GCFs from input data while maintaining hierarchical relationships and strain associations: "Create NPLinker in-memory objects (Spectrum, MF, BGC, GCF entities) maintaining hierarchical relationships and strain IDs"
- [other] Only BGCs with cumulative BLAST score ≥10,000 are retained for IOKR scoring using MIBiG homology: "For BGCs with MIBiG structural homology (cumulative BLAST score ≥10,000), extract molecular fingerprints"
