---
name: gene-cluster-family-formation-and-similarity-clustering
description: Use when you have antiSMASH v5.0.0 BGC predictions from a set of microbial genomes and you need to integrate those predictions with GNPS metabolomic data (MS2 spectra and molecular families).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0084
  - http://edamontology.org/topic_0204
  tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
  techniques:
  - tandem-MS
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

# gene-cluster-family-formation-and-similarity-clustering

## Summary

Cluster antiSMASH-predicted biosynthetic gene clusters (BGCs) into Gene Cluster Families (GCFs) using BiG-SCAPE by grouping BGCs with similar product classes and sequence similarity, creating a hierarchical scaffold for linking genomic data to metabolomic families. This reduces the dimensionality of hypothetical BGC–metabolite links and enables strain-level and fingerprint-based scoring.

## When to use

Apply this skill when you have antiSMASH v5.0.0 BGC predictions from a set of microbial genomes and you need to integrate those predictions with GNPS metabolomic data (MS2 spectra and molecular families). BGC clustering is a prerequisite step for NPLinker: it groups individual BGCs into families so that scoring functions can be applied at the GCF level, reducing spurious single-BGC matches and improving the signal-to-noise ratio when ranking hypothetical GCF–MF links.

## When NOT to use

- BGCs are already manually curated into families or clusters from another source (e.g., hand-selected sets); re-clustering may introduce inconsistency.
- Input is a single genome with very few BGCs (< 5); clustering provides limited benefit and may obscure rare or unique BGC families.
- You lack strain metadata or microbial isolate information; GCF-level strain correlation scoring will be unreliable without this annotation.

## Inputs

- antiSMASH v5.0.0 BGC predictions (GenBank files or JSON records) from microbial genome assemblies
- Strain metadata associating each BGC to a microbial source

## Outputs

- Gene Cluster Families (GCFs) with BGC membership and product class assignments
- GCF-to-BGC mapping table
- BiG-SCAPE pairwise distance matrix (optional, for QC)

## How to apply

Run BiG-SCAPE v1.0.0 on the complete set of antiSMASH-predicted BGCs from all input microbial genomes. BiG-SCAPE clusters BGCs into GCFs by computing pairwise sequence similarity and grouping clusters that share the same product class (e.g., PKS, NRPS, PKS-NRP Hybrid) and fall within a distance threshold. The output GCF assignments are then used in NPLinker to construct Spectrum, MF, BGC, and GCF entity objects that maintain hierarchical relationships (GCF → BGCs → Spectra/MFs via strain association). This clustering step is essential before computing standardised strain correlation scores and IOKR scores, which operate on GCF–MF pairs rather than individual BGC–spectrum pairs. Validation involves confirming that GCF assignments preserve expected product class groupings and that homologous BGCs (e.g., those matching the same MIBiG entry) are clustered together.

## Related tools

- **antiSMASH** (Predicts biosynthetic gene clusters (BGCs) from microbial genome assemblies; required input for GCF clustering)
- **BiG-SCAPE** (Clusters antiSMASH-predicted BGCs into Gene Cluster Families by product class and sequence similarity distance)
- **NPLinker** (Ingests BiG-SCAPE GCF assignments and creates in-memory entity objects (GCF, BGC, Spectrum, MF) with hierarchical relationships for downstream scoring and filtering) — https://github.com/NPLinker/nplinker

## Evaluation signals

- All BGCs from antiSMASH input are assigned to exactly one GCF (no orphans or duplicates).
- GCFs with the same product class (e.g., all PKS-NRP Hybrid) cluster together; no cross-product-class GCFs unless due to divergent annotation in MIBiG.
- BGCs with documented homology to the same MIBiG reference entry are assigned to the same GCF or to neighboring GCFs with high sequence similarity.
- Downstream strain correlation and IOKR scores show significantly higher enrichment (p < 0.05) for GCF–MF links in validated datasets compared to random link pairs.
- GCF membership is reproducible across re-runs of BiG-SCAPE with the same parameters and input BGC set.

## Limitations

- BiG-SCAPE clustering is sensitive to distance threshold parameters; default parameters may not be optimal for all microbial clades or BGC types.
- Product class annotations from antiSMASH can be ambiguous or incorrect, leading to spurious cross-class GCF assignments.
- BGCs with very low sequence similarity or novel product classes may form singleton GCFs, reducing the benefit of strain-level aggregation in downstream scoring.
- Requires complete, high-quality antiSMASH predictions; fragmented or incomplete BGC predictions can inflate GCF counts and reduce link specificity.
- GCF assignments do not capture functional or evolutionary information beyond product class and sequence homology; metabolomic phenotype can diverge within a GCF.

## Evidence

- [other] Load antiSMASH v5.0.0 BGC predictions and run BiG-SCAPE v1.0.0 to cluster BGCs into Gene Cluster Families (GCFs), grouping BGCs by product class and similarity distance.: "Load antiSMASH v5.0.0 BGC predictions from input microbial genomes and run BiG-SCAPE v1.0.0 to cluster BGCs into Gene Cluster Families (GCFs), grouping BGCs by product class and similarity distance."
- [other] NPLinker creates objects for spectra, MFs, BGCs and GCFs from input data while maintaining hierarchical relationships and strain associations.: "NPLinker creates objects for spectra, MFs, BGCs and GCFs from input data while maintaining hierarchical relationships and strain associations"
- [abstract] The current state-of-the-art tools for microbial BGC clustering are BiG-SCAPE and BiG-SLICE.: "The current state-of-the-art tools for microbial BGC clustering are BiG-SCAPE [13] and BiG-SLICE [21]"
- [results] Because both of these show significant homology to the MIBiG BGC. Because both of them belong to the product class 'PKS-NRP Hybrid', BiG-SCAPE considers them as belonging to the same cluster.: "Because both of them belong to the product class 'PKS-NRP Hybrid', BiG-SCAPE considers them as belonging to the same cluster"
- [other] Potential links are aggregated from the BGC level to the GCF level, reducing spurious individual matches and improving signal for strain-based scoring.: "aggregate BGC–spectrum IOKR scores to GCF–MF level by taking the maximum"
