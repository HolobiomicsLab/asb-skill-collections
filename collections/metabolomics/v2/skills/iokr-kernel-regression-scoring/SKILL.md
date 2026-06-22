---
name: iokr-kernel-regression-scoring
description: Use when when you have paired genomics (antiSMASH-detected BGCs with MIBiG homology assignments) and metabolomics data (MS2 spectra from GNPS), and you need to score BGC-spectrum links using molecular structure similarity rather than strain co-occurrence patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
  - NPLinker
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- After downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE clusters the BGCs separately by product type
- antiSMASH to score the correspondence between the MIBiG entries and the detected BGCs
- the MIBiG database [32] has emerged as a central repository of characterised microbial BGCs
- this way, we built a set of known BGC-spectrum pairs. To avoid etabolites based on properties absent from an MS2 spectrum,
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
---

# IOKR Kernel Regression Scoring

## Summary

Score GCF-MF links by training an in silico kernel regression model on spectrum-molecular fingerprint pairs from GNPS, then predicting the match probability between query spectra and BGC-derived fingerprints. This provides a complementary scoring dimension to strain correlation, especially for BGCs showing homology to characterized MIBiG references.

## When to use

When you have paired genomics (antiSMASH-detected BGCs with MIBiG homology assignments) and metabolomics data (MS2 spectra from GNPS), and you need to score BGC-spectrum links using molecular structure similarity rather than strain co-occurrence patterns. Particularly useful to break ties or enrich link rankings when strain correlation alone cannot distinguish between links with identical strain patterns.

## When NOT to use

- BGCs lack MIBiG homology or characterized structural reference: IOKR relies on molecular structure assignment via homology, so it cannot score links to completely novel BGCs.
- Input spectra are not MS2 fragmentation spectra or lack sufficient peak information: the method requires spectral fragmentation patterns comparable to GNPS library training data.
- You need fast, rough prioritization: IOKR involves fragmentation tree computation or kernel matrix assembly and can be computationally expensive at large scale.

## Inputs

- MS2 spectra from GNPS (library and query spectra in standard format)
- BGC assemblies with antiSMASH-detected clusters and MIBiG homology assignments
- Molecular fingerprint training pairs (spectrum–fingerprint pairs from GNPS library)
- GCF-MF candidate link pairs (all potential associations between clustered BGCs and metabolite features)

## Outputs

- Raw IOKR scores for each GCF-MF link (predicted fingerprint similarity values)
- Standardized IOKR scores s*_IOKR with zero mean and unit variance across all links
- Per-link p-values indicating statistical enrichment of validated links

## How to apply

Train a kernel regression (KR) model on library MS2 spectra from GNPS paired with their known molecular fingerprints, using a molecular fingerprint representation (e.g., ECFP4 or similar). For each BGC with MIBiG homology, extract or predict its molecular fingerprint from the characterized reference. Filter input spectra to include only peaks found in the training data using a Probability Product Kernel to reduce computation. Score each potential GCF-MF link by applying the trained KR model: the output is a predicted fingerprint from the BGC's reference structure, compared against the query spectrum's observed fragmentation pattern. Standardize the resulting IOKR scores across all links as s*_IOKR = (σ_IOKR − E[σ_IOKR]) / √Var[σ_IOKR] to enable fair comparison with standardized strain correlation scores. The IOKR score's strength lies in its independence from product class annotation, allowing it to score links even when natural product category is unknown.

## Related tools

- **GNPS** (Source of MS2 library spectra and community-curated spectrum-compound pairs for training the kernel regression model) — https://gnps.ucsd.edu
- **MIBiG** (Reference database for characterized BGCs; provides homology matches to antiSMASH predictions, enabling molecular structure assignment for kernel regression) — https://mibig.secondarymetabolites.org
- **antiSMASH** (Detects BGCs in microbial genomes; output clusters are assigned MIBiG homology to enable IOKR molecular fingerprint lookup) — https://antismash.secondarymetabolites.org
- **BiG-SCAPE** (Clusters antiSMASH-detected BGCs into Gene Cluster Families (GCFs); IOKR scores are computed for all potential GCF-spectrum pairings) — https://github.com/medema/BiG-SCAPE
- **NPLinker** (Integrates IOKR and strain correlation scores; provides standardization, combination, and ranking of GCF-MF links) — https://github.com/sdrogers/nplinker

## Evaluation signals

- IOKR score mean across all links should be close to zero after standardization (e.g., -0.0060 ± small variance); validated links should have significantly higher standardized scores (e.g., mean ≥ 3.6 or higher with p < 0.001).
- Top-n accuracy (e.g., true BGC ranked in top-5, top-10, top-20 candidate matches) should exceed random baseline (e.g., >0.12 for top-1 vs. 0.0 random; >0.19 for top-10 vs. 0.0044 random).
- ROC-AUC should substantially exceed 0.5 (random classifier). Reported AUC in the paper is 0.6534 vs. 0.5209 random baseline.
- Standardized IOKR scores should be statistically independent from standardized strain correlation scores (allow complementary ranking without redundancy).
- Peak filtering step should reduce false positives by excluding spectra peaks not observed in GNPS training library, reducing spurious high-scoring links.

## Limitations

- IOKR's reliance on MIBiG homology restricts scoring to BGCs showing considerable homology to characterized references; completely novel BGCs cannot be scored unless de novo structure prediction is integrated.
- Kernel function and parameter selection (e.g., kernel type, fingerprint representation, regularization strength) significantly affect performance but choices are not fully characterized in the paper; practitioners must optimize for their dataset.
- IOKR top-n accuracy remains modest even with optimization (e.g., 0.1870 for top-10), limiting its utility as a standalone filter; combination with strain correlation is recommended.
- Performance breakdown by natural product class is theoretically possible but difficult in practice due to insufficient test set size for rare product types.
- The method does not distinguish between structurally similar metabolites; scoring is based on molecular fingerprint similarity, which can conflate isomers or closely related compounds.

## Evidence

- [abstract] IOKR model training and filtering: "we introduce a new feature-based analysis method which, unlike most such methods, does not directly depend on the natural product compound class. The IOKR model is trained on a set of"
- [results] Standardization formula for IOKR: "To make the IOKR score comparable to the standardised correlation score, we can standardise it in a similar manner"
- [results] IOKR mean and performance baseline: "IOKR 0.0105 ... 0.0364. Table 3 shows the top-n performance of IOKR, i.e. how often the 'true' BGC match for a given spectrum is among the top n matches"
- [results] Complementary scoring with IOKR and strain correlation: "the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores (p-value of 2.633 × 10−4 and 0.0208"
- [discussion] MIBiG homology dependency limitation: "A drawback of the current IOKR scoring method is its reliance on MIBiG homology to assign molecular structures to BGCs, which is needed to compute the molecular fingerprint. This restricts its use to"
- [abstract] Peak filtering and kernel parameter sensitivity: "to avoid time-consuming computation of fragmentation trees for the spectra, we filter the input spectra to include only the peaks found in the training data, before filtering using the Probability"
- [discussion] Kernel parameter tuning difficulty: "IOKR is also highly dependent on the choice of both kernel function and parameters, as the molecular fingerprints denote particular substructures"
- [abstract] NPLinker integration of IOKR: "we introduce a method for combining their scores into a single scoring function for genomic and metabolomic links, which shows improved performance over either of the individual approaches"
