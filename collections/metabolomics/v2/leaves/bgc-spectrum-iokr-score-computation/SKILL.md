---
name: bgc-spectrum-iokr-score-computation
description: Use when when you have a collection of microbial genomes with predicted
  BGCs (via antiSMASH), a set of MS/MS spectra (e.g. from GNPS), and you want to score
  potential BGC-spectrum associations based on the presence of conserved molecular
  substructures inferred from the BGC's closest MIBiG homolog.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - IOKR
  - NPLinker
  - BiG-SCAPE
  - antiSMASH
  - MIBiG
  - GNPS
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- In principle, IOKR works by first learning a mapping from the space of spectra to
  the space of molecular fingerprints
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining
  the hierarchical relationship between them
- Finally, we present NPLinker, a software framework to link genomic and metabolomic
  data
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE clusters the BGCs separately by product type
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker_cq
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

# BGC-spectrum IOKR score computation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute IOKR (Integrative Omic-based Knowledge Rank) scores for individual BGC-spectrum pairs by comparing molecular fingerprints derived from BGC homology to MIBiG with MS/MS spectral features. This score measures feature-based sequence-to-metabolite predictive linkage independent of compound class annotation.

## When to use

When you have a collection of microbial genomes with predicted BGCs (via antiSMASH), a set of MS/MS spectra (e.g. from GNPS), and you want to score potential BGC-spectrum associations based on the presence of conserved molecular substructures inferred from the BGC's closest MIBiG homolog. Use this when strain correlation alone cannot reliably distinguish links because multiple BGCs or spectra share the same strain distribution.

## When NOT to use

- Input BGCs lack MIBiG homology or show insufficient sequence similarity — IOKR relies on MIBiG homology to assign molecular structures and will fail or produce uninformative scores for novel, uncharacterized BGCs.
- Spectra contain fragment peaks not represented in the training dataset — filtering to training peaks may remove discriminative information, reducing score reliability.
- The analysis goal is to prioritize links for a single BGC-spectrum pair in isolation — IOKR scores are not directly comparable across different BGCs or spectra because the fingerprint features depend on MIBiG homology specificity.

## Inputs

- Set of predicted BGCs with MIBiG homology annotations (from antiSMASH + BiG-SCAPE)
- MS/MS spectra in GNPS or compatible format
- Pre-trained or reference IOKR kernel model trained on spectrum-fingerprint pairs
- Molecular fingerprints for MIBiG BGCs (substructure feature vectors)

## Outputs

- Table with columns: BGC_ID, spectrum_ID, IOKR_score (float, range ~0–0.04)
- Optionally: scored BGC-spectrum pair rankings for downstream link prioritization

## How to apply

Train or retrieve a pre-trained IOKR kernel model on spectrum-molecular fingerprint pairs from a reference library (e.g. GNPS MS2 spectra paired with MIBiG BGC fingerprints). For each input BGC, retrieve its closest MIBiG homolog and extract the corresponding molecular fingerprint (encoded as substructure features). Filter input spectra to include only peaks present in the training data using a Probability Product Kernel to avoid expensive fragmentation tree computation. For each (BGC, spectrum) pair, compute the IOKR score by evaluating the kernel function between the BGC's molecular fingerprint and the spectrum's fragment features. The resulting score reflects the likelihood that the spectrum originates from the BGC's predicted product. Score values range from 0 to ~0.04 empirically; validated links typically have higher mean scores (0.0364) than random pairs (0.0105).

## Related tools

- **antiSMASH** (Predicts BGCs from microbial genomes; required to produce input BGCs for IOKR scoring) — https://antismash.secondarymetabolites.org/
- **BiG-SCAPE** (Clusters BGCs into GCFs and maps them to MIBiG reference BGCs, enabling homology-based fingerprint retrieval for IOKR) — https://github.com/medema/BiG-SCAPE
- **MIBiG** (Reference database of characterized BGCs; IOKR uses MIBiG homologs to assign molecular fingerprints to input BGCs) — https://mibig.secondarymetabolites.org/
- **GNPS** (Public MS/MS spectrum library; source of training spectra for IOKR kernel model and input spectra for scoring) — https://gnps.ucsd.edu/
- **NPLinker** (Framework integrating IOKR scoring with strain correlation and other link-scoring functions for prioritizing BGC-spectrum associations) — https://github.com/sdrogers/nplinker

## Evaluation signals

- IOKR scores for validated BGC-spectrum links should be significantly higher (mean ~0.0364) than mean scores for random or negative control pairs (mean ~0.0105); statistical test (e.g., t-test or Mann–Whitney U) should yield p < 0.05.
- Top-n recall: validated links should appear in the top-ranked IOKR scores for their spectrum; empirically, top-1 accuracy ~12%, top-5 ~17%, top-20 ~21% on benchmark datasets suggests reasonable discriminative power.
- AUC ≥ 0.65 when ROC-analyzing IOKR scores to distinguish validated from random BGC-spectrum pairs (empirical AUC = 0.6534 reported).
- Distribution check: standardized IOKR scores (z-scored across all pairs) should show non-zero mean for validated links when combined with standardized strain correlation scores, indicating complementary information (empirical p = 2.633 × 10⁻⁴ for combined filtering at 90th percentile).
- No spurious score inflation: verify that spectra retained after Probability Product Kernel filtering (only peaks in training data) still cover functionally discriminative mass ranges; compare spectrum coverage before/after filtering.

## Limitations

- IOKR relies on MIBiG homology to assign molecular structures to BGCs; this restricts its use to BGCs showing considerable sequence similarity to characterized reference BGCs and fails for genuinely novel BGCs or those with only distant MIBiG matches.
- Kernel function and parameter selection (e.g., substructure feature type, kernel bandwidth) significantly affect IOKR performance, but parameter sensitivity and optimal choices are not fully characterized across diverse BGC/spectrum datasets.
- IOKR score comparison across different BGCs or spectra is unreliable because standardization is local to the specific GCF-MF context; raw scores cannot be reliably used to rank links across independent analyses.
- Score performance breakdown by product type is difficult to characterize due to insufficient test set size for rare compound classes, limiting generalization claims.
- Filtering spectra to include only peaks found in training data may discard discriminative fragment information from rare or underrepresented spectra, reducing sensitivity for novel metabolites.

## Evidence

- [other] The IOKR score is generalised from BGC-spectrum pairs to GCF-MF pairs by computing the maximum IOKR score over all (BGC in GCF, spectrum in MF) combinations: "The IOKR score is generalised from BGC-spectrum pairs to GCF-MF pairs by computing the maximum IOKR score over all (BGC in GCF, spectrum in MF) combinations: for a GCF G and MF M, σ_IOKR(M, G) ="
- [abstract] To avoid time-consuming computation of fragmentation trees for the spectra, we filter the input spectra to include only the peaks found in the training data, before filtering using the Probability: "to avoid time-consuming computation of fragmentation trees for the spectra, we filter the input spectra to include only the peaks found in the training data, before filtering using the Probability"
- [discussion] A drawback of the current IOKR scoring method is its reliance on MIBiG homology to assign molecular structures to BGCs, which is needed to compute the molecular fingerprint. This restricts its use to: "A drawback of the current IOKR scoring method is its reliance on MIBiG homology to assign molecular structures to BGCs, which is needed to compute the molecular fingerprint. This restricts its use to"
- [results] IOKR score mean for all links: 0.0105; for validated links: 0.0364 with p=1.7968 × 10−9: "IOKR 0.0105 ... 0.0364 [with p-value] 1.7968 × 10−9"
- [abstract] We use library MS2 spectra from the public, community-driven GNPS knowledge base as a training set for the IOKR model: "The IOKR model is trained on a set of spectrum-molecular fingerprint pairs. We use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model"
- [abstract] unlike most such methods, does not directly depend on the natural product compound class: "we introduce a new feature-based analysis method which, unlike most such methods, does not directly depend on the natural product compound class"
- [discussion] IOKR is also highly dependent on the choice of both kernel function and parameters, as the molecular fingerprints denote particular substructures: "IOKR is also highly dependent on the choice of both kernel function and parameters, as the molecular fingerprints denote particular substructures"
