---
name: kernel-regression-learning-from-spectral-fingerprint-pairs
description: Use when when you have a training set of MS2 spectra with known chemical structures (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - GNPS
  - MIBiG
  - Chemistry Development Kit (CDK)
  - Probability Product Kernel (PPK)
  - antiSMASH
  - NPLinker
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- we use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model
- To assign one or more molecular structures to BGCs, according to how many high-scoring matches are found in MIBiG
- Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit
- Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit [29]
- we filter the input spectra to include only the peaks found in the training data, before using the Probability Product Kernel (PPK)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# kernel-regression-learning-from-spectral-fingerprint-pairs

## Summary

Train an Input-Output Kernel Regression (IOKR) model to learn a mapping from MS2 spectrum space (via spectrum kernels) to molecular fingerprint space (via structured fingerprints like CDK Substructure or PubChem Substructure) using paired spectrum–metabolite training data from spectral libraries. This enables prediction of molecular fingerprints for novel spectra and ranking of genomic BGCs by their predicted fingerprint similarity.

## When to use

When you have a training set of MS2 spectra with known chemical structures (e.g., from GNPS library with structural annotations), and you want to predict molecular properties or chemical structures for novel spectra without relying on compound class information, or to enable BGC-spectrum matching in natural products discovery pipelines. Apply this skill when you need a model that is agnostic to natural product type and can generalize across diverse chemical classes.

## When NOT to use

- When your training set lacks known molecular structures or SMILES annotations for spectra; IOKR requires paired spectrum–structure training data.
- When you have a small training set (<100 spectrum–structure pairs); kernel methods often require sufficient training data to learn meaningful fingerprint projections.
- When your test spectra and training spectra come from substantially different ionization modes, mass analyzers, or spectral preprocessing; kernel methods are sensitive to feature space alignment.

## Inputs

- MS2 spectra with known chemical structures (GNPS library or similar, with SMILES annotations)
- Molecular fingerprint extractors (CDK, PubChem, Klekota-Roth)
- Spectrum kernel function (e.g., cosine kernel, PPK)
- Candidate set of molecules or BGCs (e.g., MIBiG entries with homology-based structure assignment)
- Test set of MS2 spectra to be scored against candidates

## Outputs

- Trained IOKR model mapping spectrum kernel space to fingerprint space
- Predicted molecular fingerprints for novel spectra
- Ranked lists of candidate BGCs or molecules for each spectrum (by inner product score)
- IOKR scores (mean, distribution) for all hypothetical spectrum–candidate pairs
- Ranking metrics: top-n accuracy, AUC, p-values comparing validated vs. random links

## How to apply

First, extract molecular fingerprints (e.g., CDK Substructure, PubChem Substructure, Klekota-Roth) from SMILES strings of metabolites in the training set (e.g., 4138 annotated spectra from GNPS). Construct spectrum kernels (e.g., cosine similarity, PPK-filtered) for the training spectra and their associated fingerprints, then use operator-valued kernel regression to learn the mapping from spectrum kernel space X (with kernel K_x) to fingerprint space F. For inference on novel spectra, apply the Probability Product Kernel (PPK) as a denoising step to retain only peaks present in the training data, compute the learned mapping to predict fingerprints, and rank candidate BGCs (or other molecular candidates) by inner product ⟨ĥ(spectrum), φ(candidate)⟩ in fingerprint space. Evaluate using top-n accuracy (n=1,5,10,20,200) and AUC against randomized baselines to assess ranking performance.

## Related tools

- **GNPS** (Source of training set: 4138 spectra with structural annotations used to extract molecular fingerprints and train the IOKR model.) — https://gnps.ucsd.edu
- **MIBiG** (Source of candidate BGC structures and validation ground truth; paired with GNPS via InChIKey matching to construct evaluation dataset.) — https://mibig.secondarymetabolites.org
- **Chemistry Development Kit (CDK)** (Molecular fingerprint extraction from SMILES strings (CDK Substructure fingerprints).)
- **Probability Product Kernel (PPK)** (Denoising filter applied to input spectra to retain only peaks present in training data before IOKR prediction.)
- **antiSMASH** (BGC prediction and annotation in genomes; produces candidate set filtered by MIBiG homology for ranking by IOKR.) — https://antismash.secondarymetabolites.org
- **NPLinker** (Framework integrating IOKR scoring with strain correlation and other methods to link genomic and metabolomic data.) — https://github.com/sdrogers/nplinker

## Evaluation signals

- Mean IOKR score for validated spectrum–BGC pairs should be significantly higher than for all hypothetical pairs (validated link mean ≥ 0.036 vs. all-pairs mean ≈ 0.01, p < 0.05).
- Top-n accuracy metrics should substantially exceed random baseline (e.g., top-1 accuracy ≥ 0.10 vs. baseline ~0.0 for large candidate sets; AUC ≥ 0.65 vs. random AUC = 0.52).
- Distribution histogram of IOKR scores should show clear separation between validated and random link populations when overlaid.
- Ranked predictions for test spectra should reproduce published benchmarks (e.g., Table 3 results from the original paper) when evaluated on the same MIBiG/GNPS dataset.
- High-scoring links should pass manual validation by matching MS2 peaks to predicted molecular structures (spot-check against known fragmentation patterns).

## Limitations

- IOKR performance is highly dependent on the choice of kernel function and molecular fingerprint representation; kernels on MS2 spectra may require optimization for new datasets.
- Model applicability is restricted to BGCs with considerable sequence homology to MIBiG entries (only 2242 of 3316 BGCs in the study could be assigned structures); de novo prediction of fingerprints directly from BGCs sequences is not addressed.
- Insufficient test set size in the reported evaluation makes it difficult to validate that the model is truly independent of natural product compound class, despite this being a design goal.
- Training data mixing (IOKR training set includes non-microbial metabolites from GNPS) may introduce bias toward structures over-represented in public spectral libraries.
- PPK denoising step removes potentially informative peaks not present in the training data, which could sacrifice sensitivity for novel chemical environments.

## Evidence

- [other] construct the IOKR model by learning a mapping from the spectrum kernel space (X, with kernel K_x) to the molecular fingerprint space (F) using the training pairs, implementing operator-valued kernel regression with the paired spectrum-fingerprint training sets: "construct the IOKR model by learning a mapping from the spectrum kernel space (X, with kernel K_x) to the molecular fingerprint space (F) using the training pairs, implementing operator-valued kernel"
- [other] extract molecular fingerprints (CDK Substructure, PubChem Substructure, Klekota-Roth) from SMILES strings for each annotated metabolite: "extract molecular fingerprints (CDK Substructure, PubChem Substructure, Klekota-Roth) from SMILES strings for each annotated metabolite"
- [other] Filter input MS2 spectra using the Probability Product Kernel (PPK) to retain only peaks present in the training data as a denoising step.: "Filter input MS2 spectra using the Probability Product Kernel (PPK) to retain only peaks present in the training data as a denoising step"
- [other] apply the trained IOKR model to predict molecular fingerprints and rank candidate BGCs (restricted to 2242 BGCs with MIBiG homology assignments) by computing the inner product ⟨ĥ(spectrum), φ(BGC_candidate)⟩ in fingerprint space: "apply the trained IOKR model to predict molecular fingerprints and rank candidate BGCs by computing the inner product ⟨ĥ(spectrum), φ(BGC_candidate)⟩ in fingerprint space"
- [other] IOKR achieves a mean score of 0.0105 for all 2966 BGC-spectrum links and 0.0364 for validated links (p=1.7968 × 10−9), with top-1 accuracy of 0.1208, top-5 accuracy of 0.1708, and AUC of 0.6534 compared to a random baseline AUC of 0.5209: "IOKR achieves a mean score of 0.0105 for all 2966 BGC-spectrum links and 0.0364 for validated links (p=1.7968 × 10−9), with top-1 accuracy of 0.1208, top-5 accuracy of 0.1708, and AUC of 0.6534"
- [abstract] Input-Output Kernel Regression (IOKR) approach does not directly depend on natural product compound class: "Input-Output Kernel Regression (IOKR) approach does not directly depend on natural product compound class"
- [discussion] IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints: "IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints"
- [discussion] restricts its use to those BGCs which show considerable homology with MIBiG entries. While still useful in this form, predicting molecular fingerprints directly from BGCs would broaden the applicability: "restricts its use to those BGCs which show considerable homology with MIBiG entries"
