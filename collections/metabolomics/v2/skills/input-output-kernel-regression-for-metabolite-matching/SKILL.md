---
name: input-output-kernel-regression-for-metabolite-matching
description: Use when apply IOKR when you have BGCs with structural predictions based on MIBiG homology (cumulative BLAST score ≥10,000) and you wish to rank hypothetical BGC–spectrum links using metabolite structure information rather than genomic or strain-based features alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3658
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0621
  tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
  - CDK (Chemistry Development Kit)
  - PubChem
  - Klekota-Roth fingerprints
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

# Input-Output Kernel Regression for Metabolite Matching

## Summary

IOKR is a feature-based scoring method that ranks BGC–spectrum links by learning a regression model from molecular fingerprints of MIBiG-homologous metabolites to MS2 spectral features, enabling BGC–metabolite link prioritization independent of compound class. The method improves link ranking when combined with strain correlation scores.

## When to use

Apply IOKR when you have BGCs with structural predictions based on MIBiG homology (cumulative BLAST score ≥10,000) and you wish to rank hypothetical BGC–spectrum links using metabolite structure information rather than genomic or strain-based features alone. Use IOKR especially when compound-class-independent scoring is needed or when genomic similarity alone is insufficient to discriminate true links.

## When NOT to use

- When BGCs lack structural annotations or MIBiG homology; IOKR requires predicted metabolite structures derived from homologous database entries with cumulative BLAST score ≥10,000.
- When the goal is purely genomic or strain-based link ranking; IOKR adds computational cost and requires spectral data, so use strain correlation alone if metabolomic context is unavailable.
- When high-resolution MS2 spectra or complete spectral training data are unavailable; IOKR performance depends on the quality and breadth of the underlying kernel functions and spectral feature representation.

## Inputs

- BGCs with MIBiG structural homology assignment (cumulative BLAST score ≥10,000)
- MS2 spectra with m/z and intensity peaks
- Predicted metabolite structures from MIBiG homology matches
- Gene Cluster Families (GCFs) from BiG-SCAPE clustering
- Molecular Families (MFs) from GNPS spectral clustering

## Outputs

- Standardized IOKR scores for each BGC–spectrum pair
- Aggregated GCF–MF link scores (maximum IOKR per GCF–MF combination)
- Ranked list of hypothetical GCF–MF links sortable by IOKR score
- Combined scoring table merging standardized IOKR and strain correlation scores

## How to apply

First, identify BGCs with considerable homology to MIBiG entries (cumulative BLAST score ≥10,000) and extract predicted metabolite structures from matching MIBiG records. Generate molecular fingerprints using CDK substructure, PubChem, and Klekota-Roth representations. Train an Input-Output Kernel Regression model using the fingerprints as input features and MS2 spectral features as output. Before scoring, filter input spectra using a Probability Product Kernel to retain only peaks found in the IOKR training data, reducing computational cost and noise. For each BGC–spectrum candidate pair, compute the IOKR score reflecting the regression model's confidence that the spectrum matches the predicted metabolite. Standardize IOKR scores using expected value and variance computed over all potential links in the data set: s*_IOKR = (s_IOKR − E[s_IOKR]) / √Var[s_IOKR]. Aggregate BGC–spectrum IOKR scores to the GCF–MF level by taking the maximum score, reflecting that any BGC in a GCF may produce the observed metabolite. Rank links by standardized IOKR score or combine it with standardized strain correlation scores using the ℓ₁/₂-norm: s_combined = sgn(s*_corr)|s*_corr|^(1/2) + sgn(s*_IOKR)|s*_IOKR|^(1/2).

## Related tools

- **NPLinker** (Framework implementing IOKR scoring within the orchestrated pipeline for loading BGCs, GCFs, spectra, and MFs; provides standardization and aggregation infrastructure) — https://github.com/sdrogers/nplinker
- **MIBiG** (Database of characterized BGCs with structural annotations; source of training metabolites and homology targets for IOKR fingerprint generation)
- **GNPS** (Provides MS2 spectra and molecular families as IOKR input; defines the metabolomic space against which BGC structures are ranked)
- **antiSMASH** (Predicts BGCs from genomic input; IOKR operates on BGCs identified by antiSMASH v5.0.0)
- **BiG-SCAPE** (Clusters BGCs into GCFs; IOKR aggregates BGC–spectrum scores to GCF–MF level for ranking)
- **CDK (Chemistry Development Kit)** (Generates molecular fingerprints (CDK substructure) used as input features for IOKR regression)
- **PubChem** (Source of molecular fingerprints (PubChem representation) for IOKR feature extraction)
- **Klekota-Roth fingerprints** (Molecular fingerprint library (Klekota-Roth representation) used alongside CDK and PubChem for multi-view IOKR feature set)

## Evaluation signals

- IOKR scores for validated links (true BGC–spectrum pairs) are significantly higher (p < 0.05) than scores for all hypothetical links, demonstrated by mean standardized IOKR of 0.0364 (validated) vs. 0.0105 (all), p = 1.7968 × 10⁻⁹.
- Top-n accuracy metrics show IOKR outperforms random baseline: top-1 accuracy 0.1208 (vs. 0.0 random), top-5 0.1708 (vs. 0.0014 random), AUC 0.6534 (vs. 0.5209 random).
- Links scoring jointly in the 90th percentile for both standardized strain correlation and IOKR show significantly higher enrichment of validated links (p < 0.05) compared to either score alone, confirming complementarity.
- Standardized IOKR scores display mean ≈ 0 and unit variance across all links, confirming proper z-normalization: s*_IOKR = (s_IOKR − E[s_IOKR]) / √Var[s_IOKR].
- Manual spectral interpretation (matching MS2 peaks to predicted metabolite structures) confirms that high-scoring IOKR-ranked links correspond to plausible chemical fragmentation patterns.

## Limitations

- IOKR is restricted to BGCs showing considerable homology with MIBiG entries (cumulative BLAST score ≥10,000); novel or divergent BGCs without structural homology cannot be scored, limiting applicability to orphan natural products.
- Performance is highly dependent on the choice of molecular fingerprint representations (CDK, PubChem, Klekota-Roth) and kernel function; suboptimal fingerprint selection or kernel miscalibration reduces discrimination.
- Due to insufficient test set size, performance breakdown by natural product compound class cannot be verified, even though IOKR is theoretically class-independent.
- Kernels used for MS2 spectral feature extraction require further optimization; current spectral kernel design may not capture all relevant fragmentation patterns.
- Training set includes metabolites from non-microbial sources; this domain mismatch may reduce accuracy when applied to strictly microbial natural products.

## Evidence

- [other] For BGCs with MIBiG structural homology (cumulative BLAST score ≥10,000), extract molecular fingerprints from predicted metabolite structures and score BGC–spectrum links using Input-Output Kernel Regression (IOKR) with CDK substructure, PubChem, and Klekota-Roth fingerprints: "For BGCs with MIBiG structural homology (cumulative BLAST score ≥10,000), extract molecular fingerprints from predicted metabolite structures and score BGC–spectrum links using Input-Output Kernel"
- [other] Standardise IOKR scores using expected value and variance over the set of all potential links: s*_IOKR = (s_IOKR − E[s_IOKR]) / √Var[s_IOKR]; aggregate BGC–spectrum IOKR scores to GCF–MF level by taking the maximum.: "Standardise IOKR scores using expected value and variance over the set of all potential links: s*_IOKR = (s_IOKR − E[s_IOKR]) / √Var[s_IOKR]; aggregate BGC–spectrum IOKR scores to GCF–MF level by"
- [abstract] We then introduce a new feature-based analysis method which, unlike most such methods, does not directly depend on the natural product compound class: "We then introduce a new feature-based analysis method which, unlike most such methods, does not directly depend on the natural product compound class"
- [abstract] we filter the input spectra to include only the peaks found in the training data, before using the Probability Product Kernel (PPK): "we filter the input spectra to include only the peaks found in the training data, before using the Probability Product Kernel (PPK)"
- [discussion] IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints: "IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints"
- [discussion] restricts its use to those BGCs which show considerable homology with MIBiG entries. While still useful in this form, predicting molecular fingerprints directly from BGCs would broaden the: "restricts its use to those BGCs which show considerable homology with MIBiG entries. While still useful in this form, predicting molecular fingerprints directly from BGCs would broaden the"
- [results] top-1: 0.1208, top-5: 0.1708, top-10: 0.1870, top-20: 0.2121, top-200: 0.2946; AUC: 0.6534: "top-1: 0.1208, top-5: 0.1708, top-10: 0.1870, top-20: 0.2121, top-200: 0.2946; AUC: 0.6534"
- [abstract] they are in fact complementary, and show a way to combine them to improve their performance: "they are in fact complementary, and show a way to combine them to improve their performance"
