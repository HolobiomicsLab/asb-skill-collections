---
name: iokr-fingerprint-space-ranking
description: Use when when you have paired MS2 spectra and BGCs with structural candidates (e.g., from MIBiG homology), and you want to rank which BGC likely produces which spectrum using a compound-class-agnostic method.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
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

# IOKR fingerprint-space ranking

## Summary

A kernel regression method that ranks candidate BGC-spectrum links by projecting MS2 spectra into molecular fingerprint space and assigning IOKR scores without direct dependence on natural product compound class. This provides a complementary scoring signal to strain correlation for prioritizing validated genomic–metabolomic associations.

## When to use

When you have paired MS2 spectra and BGCs with structural candidates (e.g., from MIBiG homology), and you want to rank which BGC likely produces which spectrum using a compound-class-agnostic method. Use this skill when strain correlation alone cannot distinguish true links because many BGCs co-occur in the same strains, or when you need to combine multiple orthogonal scoring functions to improve enrichment of validated links above the 90th percentile threshold.

## When NOT to use

- Input spectra contain many peaks absent from the training data; PPK filtering would remove too much signal and bias the ranking.
- BGCs show little or no homology to MIBiG entries; IOKR relies on structure assignment via MIBiG similarity and cannot predict fingerprints directly from genomic sequences.
- Your goal is to identify novel compound classes; IOKR performance is limited by insufficient test set size for breaking down accuracy by product type, and dependence on kernel function and fingerprint choice may bias results toward training data chemistry.

## Inputs

- MS2 spectra (in GNPS-compatible format)
- BGC annotations with structural candidates derived from MIBiG homology matching
- Fragmentation trees or molecular fingerprints for candidate structures
- Training dataset of MS2 spectra paired with known molecular structures

## Outputs

- IOKR scores (σ_IOKR) for each BGC-spectrum pair
- Standardised IOKR scores (σ*_IOKR) using expected value and variance normalisation
- Ranked list of candidate BGC-spectrum links by IOKR score
- Combined ranking scores integrating IOKR and orthogonal scoring functions

## How to apply

First, filter input MS2 spectra to include only peaks found in the training data using Probability Product Kernel (PPK) as a denoising step to avoid expensive fragmentation tree computation. Next, rank candidate structures for each spectrum by projecting them into molecular fingerprint space using a trained Input-Output Kernel Regression (IOKR) model, assigning each spectrum a maximum IOKR score (σ_IOKR) corresponding to its best-matching candidate BGC. Standardise the IOKR score using the expected value and variance over all potential links to make it comparable to other scoring functions (σ*_IOKR). Finally, combine the standardised IOKR score with other scoring functions (e.g., standardised strain correlation) using an ℓp-norm with sign function adjustment to jointly rank links. Links scoring above the 90th percentile for the combined score will show significantly higher enrichment for validated links compared to either individual score alone.

## Related tools

- **NPLinker** (Framework integrating genomic and metabolomic data; implements IOKR scoring and link ranking for paired natural product discovery) — https://github.com/sdrogers/nplinker
- **GNPS** (Provides public metabolomic spectra library; supplies MS2 spectral data for IOKR candidate ranking) — https://gnps.ucsd.edu/
- **MIBiG** (Database of experimentally validated BGCs with structural annotations; used to assign candidate structures to BGCs and train IOKR model) — https://mibig.secondarymetabolites.org/
- **antiSMASH** (BGC detection and annotation in microbial genomes; output is used as input to IOKR for link ranking)
- **BiG-SCAPE** (Clusters BGCs into gene cluster families (GCFs); GCF-spectrum pairs are scored by IOKR)

## Evaluation signals

- IOKR top-n accuracy on a held-out test set (e.g., top-1: >0.12, top-10: >0.18) substantially exceeds random baseline (top-1: 0, top-10: 0.0044) and shows AUC ≥ 0.65
- Mean IOKR score for validated links is significantly higher than for all hypothetical links (p < 0.05 by Mann–Whitney U or t-test)
- Fisher exact test p-value for enrichment at the 90th percentile threshold is <0.05 (observed: p=0.0208 to p=2.633×10−4 in published datasets)
- Standardised IOKR score (σ*_IOKR) has comparable scale and distribution to standardised strain correlation score, enabling meaningful ℓp-norm combination
- Manual inspection of high-scoring (top percentile) BGC-spectrum pairs shows chemical consistency between MS2 peaks and candidate structures

## Limitations

- Restricted to BGCs showing considerable homology with MIBiG entries; cannot be applied to novel or divergent BGCs without structure assignment.
- IOKR performance is highly dependent on the choice of kernel function and molecular fingerprints; kernels used on MS2 spectra require further optimisation and may not generalise across different MS platforms or ionisation modes.
- Due to insufficient test set size, breaking down performance by natural product compound class to verify claimed class-agnosticism is currently difficult and cannot be fully validated.
- Training set includes metabolites from sources other than microbial organisms, which may introduce bias when ranking links in strictly microbial datasets.
- IOKR top-1 accuracy is modest (0.1208); true BGC matches rank in top-1 only ~12% of the time, necessitating use of combined scoring functions or manual curation for high-confidence predictions.

## Evidence

- [abstract] Potential links between spectra and BGCs belonging to this subset can then be ranked using IOKR: "Potential links between spectra and BGCs belonging to this subset can then be ranked using IOKR"
- [abstract] we filter the input spectra to include only the peaks found in the training data, before using the Probability Product Kernel (PPK): "we filter the input spectra to include only the peaks found in the training data, before using the Probability Product Kernel (PPK)"
- [abstract] We then introduce a new feature-based analysis method which, unlike most such methods, does not directly depend on the natural product compound class: "We then introduce a new feature-based analysis method which, unlike most such methods, does not directly depend on the natural product compound class"
- [results] To make the IOKR score comparable to the standardised correlation score, we can standardise it in a similar manner to the strain correlation score.: "To make the IOKR score comparable to the standardised correlation score, we can standardise it in a similar manner to the strain correlation score."
- [discussion] restricts its use to those BGCs which show considerable homology with MIBiG entries. While still useful in this form, predicting molecular fingerprints directly from BGCs would broaden the: "restricts its use to those BGCs which show considerable homology with MIBiG entries. While still useful in this form, predicting molecular fingerprints directly from BGCs would broaden the"
- [discussion] IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints: "IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints"
- [other] Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links: "Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links"
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
