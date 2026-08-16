---
name: bgc-spectrum-ranking-by-kernel-similarity
description: 'Use when you have: (1) a trained IOKR model mapping from spectrum kernels
  to molecular fingerprints, (2) MS2 spectra from your sample, (3) a set of candidate
  BGCs with known or predicted structures (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - GNPS
  - MIBiG
  - Chemistry Development Kit (CDK)
  - Probability Product Kernel (PPK)
  - antiSMASH
  - NPLinker
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
  and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- we use library MS2 spectra from the public, community-driven GNPS knowledge base
  [33] as a training set for the IOKR model
- To assign one or more molecular structures to BGCs, according to how many high-scoring
  matches are found in MIBiG
- Molecular fingerprints are extracted from SMILES strings using the Chemistry Development
  Kit
- Molecular fingerprints are extracted from SMILES strings using the Chemistry Development
  Kit [29]
- we filter the input spectra to include only the peaks found in the training data,
  before using the Probability Product Kernel (PPK)
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

# BGC-spectrum ranking by kernel similarity

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Rank candidate biosynthetic gene clusters (BGCs) against observed mass spectrometry data by learning a mapping from spectrum kernel space to molecular fingerprint space using Input-Output Kernel Regression (IOKR), then scoring BGC-spectrum pairs via inner product in fingerprint space. This approach ranks true metabolite-BGC links significantly above random baseline, achieving top-5 accuracy of 0.1708 and AUC of 0.6534 on the MIBiG-GNPS paired dataset.

## When to use

Apply this skill when you have: (1) a trained IOKR model mapping from spectrum kernels to molecular fingerprints, (2) MS2 spectra from your sample, (3) a set of candidate BGCs with known or predicted structures (e.g., via antiSMASH and MIBiG homology assignment), and (4) the goal of ranking which BGCs are most likely to produce the observed spectra without relying on natural product compound class annotations.

## When NOT to use

- BGCs lack structural assignments or show minimal homology to reference databases (MIBiG); IOKR relies on known or predicted compound structures to compute fingerprints.
- MS2 spectra are from a compound class significantly underrepresented in the IOKR training set; the method does not directly account for natural product class and may generalise poorly.
- You require real-time ranking with no pre-trained model; IOKR model training requires paired spectrum-fingerprint data and is computationally expensive.

## Inputs

- Pre-trained IOKR model (mapping spectrum kernel space to molecular fingerprint space)
- MS2 spectra (raw peak lists or probability distributions)
- Candidate BGC set with associated molecular structures or fingerprints
- Molecular fingerprints for BGC structures (CDK Substructure, PubChem Substructure, or Klekota-Roth)
- Spectrum kernel function (e.g., cosine similarity, Jaccard kernel)

## Outputs

- Ranked list of BGCs per spectrum (sorted by IOKR score descending)
- IOKR score per BGC-spectrum pair
- Top-n accuracy metrics (top-1, top-5, top-10, top-20, top-200)
- Area-under-curve (AUC) statistic vs. random baseline
- Standardised IOKR score (optional, for integration with other scoring functions)

## How to apply

First, filter input MS2 spectra using the Probability Product Kernel (PPK) as a denoising step to retain only peaks present in the training data. Apply the pre-trained IOKR model to each filtered spectrum to predict molecular fingerprints in the learned feature space. For each spectrum, compute the inner product between the predicted fingerprint and the fingerprints of all candidate BGC structures (restricted to those with structural assignments via MIBiG homology or other trusted source) to produce a ranked list of BGC candidates. Calculate top-n accuracy (n=1, 5, 10, 20, 200) and area-under-curve (AUC) metrics by comparing the rank of the true BGC relative to all candidates. Optionally, standardise IOKR scores using expected value and variance across all potential links to enable combination with complementary scoring functions (e.g., strain correlation) via an ℓp-norm combination with sign adjustment.

## Related tools

- **NPLinker** (Framework implementing IOKR scoring and BGC-spectrum link ranking within an integrated genomics-metabolomics pipeline) — https://github.com/sdrogers/nplinker
- **GNPS** (Source of MS2 spectra and spectral kernels for training and evaluation; community library provides reference spectra with structural annotations)
- **MIBiG** (Database of experimentally validated BGC-metabolite pairs; provides structural annotations and homology reference for candidate BGC filtering)
- **antiSMASH** (Tool for automated BGC detection and prediction in microbial genomes; produces candidate BGC set for ranking)
- **Chemistry Development Kit (CDK)** (Extracts molecular fingerprints (CDK Substructure, PubChem Substructure, Klekota-Roth) from SMILES strings for fingerprint space mapping)
- **Probability Product Kernel (PPK)** (Denoises MS2 spectra by filtering to retain only peaks present in training data before IOKR prediction)

## Evaluation signals

- Top-n accuracy for validated BGC-spectrum pairs must be significantly above random baseline (e.g., top-5: 0.1708 vs. random 0.0014; top-1: 0.1208 vs. random 0.0)
- Mean IOKR score for validated links must be significantly higher than for all hypothetical links (e.g., 0.0364 vs. 0.0105, p < 0.05)
- AUC metric must exceed 0.5 (random baseline ~0.52); the study reports AUC of 0.6534, representing ~25% improvement over baseline
- Distribution histograms of IOKR scores should show validated links enriched in the right tail; visual inspection should confirm separation from mean of all links
- When combined with complementary scores (e.g., strain correlation), integrated ranking should yield better precision at the 90th percentile than either score alone

## Limitations

- IOKR restricts use to BGCs with considerable homology to MIBiG entries; novel or structurally divergent BGCs cannot be ranked if their fingerprints are not in the training set or a related reference database.
- Performance is highly dependent on the choice of both spectrum kernel function and molecular fingerprint scheme; kernels used on MS2 spectra require further optimisation and may not generalise across instrument types or fragmentation methods.
- Insufficient test set size limits ability to break down performance by natural product compound class; while IOKR does not theoretically depend on class, validation across diverse chemistry is incomplete.
- Method assumes training data (GNPS library with structural annotations) is representative of the unknown spectra; severe domain shift (e.g., novel microbial taxa, uncommon biosynthetic pathways) is not handled explicitly.

## Evidence

- [methods] For each spectrum, apply the trained IOKR model to predict molecular fingerprints and rank candidate BGCs by computing the inner product in fingerprint space: "For the 6246 MS2 spectra in the MIBiG/GNPS evaluation set, apply the trained IOKR model to predict molecular fingerprints and rank candidate BGCs (restricted to 2242 BGCs with MIBiG homology"
- [methods] Filter input MS2 spectra using PPK to retain only peaks present in training data as denoising before IOKR: "Filter input MS2 spectra using the Probability Product Kernel (PPK) to retain only peaks present in the training data as a denoising step."
- [results] IOKR achieves mean score 0.0364 for validated links vs. 0.0105 for all links (p=1.7968 × 10−9), with top-5 accuracy 0.1708 and AUC 0.6534: "IOKR achieves a mean score of 0.0105 for all 2966 BGC-spectrum links and 0.0364 for validated links (p=1.7968 × 10−9), with top-1 accuracy of 0.1208, top-5 accuracy of 0.1708, and AUC of 0.6534"
- [discussion] IOKR is highly dependent on kernel function and fingerprint choice; kernels used on MS2 spectra need further optimization: "IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints... the kernels used on the MS2 spectra can almost surely be further optimised"
- [discussion] IOKR reliance on MIBiG homology restricts use to BGCs with considerable similarity: "restricts its use to those BGCs which show considerable homology with MIBiG entries. While still useful in this form, predicting molecular fingerprints directly from BGCs would broaden the"
- [methods] Create IOKR model by learning mapping from spectrum kernel space to fingerprint space using training pairs: "Construct the IOKR model by learning a mapping from the spectrum kernel space (X, with kernel K_x) to the molecular fingerprint space (F) using the training pairs, implementing operator-valued kernel"
