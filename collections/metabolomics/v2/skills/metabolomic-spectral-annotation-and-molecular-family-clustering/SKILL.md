---
name: metabolomic-spectral-annotation-and-molecular-family-clustering
description: Use when when you have raw or GNPS-processed MS2 spectral data from microbial strains and need to organize spectra into molecular families (grouped by spectral similarity) while preserving strain provenance, as a prerequisite for linking metabolomic families to gene cluster families (GCFs) via.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
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
---

# metabolomic-spectral-annotation-and-molecular-family-clustering

## Summary

Import and organize tandem MS (MS2) spectra from GNPS into NPLinker Spectrum objects, cluster spectra into molecular families (MFs) via spectral similarity, and maintain strain-level associations to enable downstream correlation scoring with genomic clusters. This prepares metabolomic data for integration with BGC/GCF predictions.

## When to use

When you have raw or GNPS-processed MS2 spectral data from microbial strains and need to organize spectra into molecular families (grouped by spectral similarity) while preserving strain provenance, as a prerequisite for linking metabolomic families to gene cluster families (GCFs) via strain correlation or other scoring methods.

## When NOT to use

- Input spectra are already de-replicated or have been merged at the MF level and strain-level granularity has been lost — you need raw or minimally processed spectra with intact strain metadata.
- MS2 spectra lack strain annotation or strain information cannot be reliably traced to the MF level — strain correlation scoring requires complete strain provenance.
- Your goal is to perform novel spectral clustering or similarity assessment — NPLinker assumes GNPS-derived MF assignments; it does not recompute spectral clustering.

## Inputs

- GNPS MS2 spectra with metadata (strain ID, MF cluster assignment)
- GNPS molecular family (MF) cluster assignments and spectral similarity groupings
- Strain annotations linked to each spectrum

## Outputs

- NPLinker Spectrum objects (in-memory, with strain ID and parent MF reference)
- NPLinker MF objects (in-memory, with hierarchical Spectrum children and strain associations)
- Organized metabolomic data structure ready for scoring and linking to GCFs

## How to apply

Load MS2 spectra and molecular family assignments from GNPS output into NPLinker's Spectrum and MF in-memory objects, maintaining hierarchical relationships between spectra, MFs, and strain IDs. Group spectra into MFs based on GNPS spectral clustering (which clusters spectra by cosine similarity). Retain strain annotation metadata for each spectrum and MF to enable downstream strain correlation scoring. The MF-level organization allows aggregation of per-spectrum scores (e.g., IOKR) to the family level by taking the maximum score, reducing noise and computational burden when ranking hypothetical links.

## Related tools

- **GNPS** (Source for MS2 spectra, spectral clustering into molecular families, and strain-linked metabolomic metadata)
- **NPLinker** (In-memory object framework (Spectrum, MF classes) for organizing metabolomic data and maintaining hierarchical strain relationships) — https://github.com/NPLinker/nplinker

## Evaluation signals

- All Spectrum objects are successfully instantiated and linked to a parent MF object with correct strain ID.
- Each MF object contains ≥1 child Spectrum; strain ID is consistent across spectra within an MF (or flagged if heterogeneous).
- Hierarchical relationships (Spectrum → MF → strain) can be traversed without missing or null references; no orphaned spectra.
- Strain metadata is retained and accessible for downstream correlation scoring; spot-check that strain IDs match the original GNPS metadata.
- The total count of Spectrum objects and MF objects matches expected counts from GNPS output (e.g., 6246 spectra and corresponding MF assignments as in the article example).

## Limitations

- Relies on GNPS spectral clustering quality; spectra grouped into MFs by cosine similarity may not reflect true chemical relatedness if spectral noise or fragmentation variation is high.
- Strain annotation must be complete and non-ambiguous; if a spectrum is assigned to multiple strains or strain provenance is uncertain, correlation scoring will be unreliable.
- MF-level aggregation (e.g., taking the maximum IOKR score) can mask heterogeneity within a family — high-scoring outlier spectra may dominate if the family contains spectra of differing structural classes.
- No de novo structure annotation or molecular formula assignment at this stage; MFs are spectral clusters only, not validated chemical entities.

## Evidence

- [other] Import GNPS metabolomic data: MS2 spectra, molecular families (MFs) from spectral clustering, and strain annotations for each spectrum and MF.: "Import GNPS metabolomic data: MS2 spectra, molecular families (MFs) from spectral clustering, and strain annotations for each spectrum and MF."
- [other] Create NPLinker in-memory objects (Spectrum, MF, BGC, GCF entities) maintaining hierarchical relationships and strain IDs: "Create NPLinker in-memory objects (Spectrum, MF, BGC, GCF entities) maintaining hierarchical relationships and strain IDs"
- [results] The MIBiG/GNPS data set consists of sets of associated BGC, metabolite and spectrum: "The MIBiG/GNPS data set consists of sets of associated BGC, metabolite and spectrum"
- [abstract] metabolomic output from the public, community-driven Global Natural Products Social (GNPS) knowledge base: "metabolomic output from the public, community-driven Global Natural Products Social (GNPS) knowledge base"
- [other] aggregate BGC–spectrum IOKR scores to GCF–MF level by taking the maximum: "aggregate BGC–spectrum IOKR scores to GCF–MF level by taking the maximum"
