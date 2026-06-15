---
name: validated-link-enrichment-analysis
description: Use when when you have a ranked list of GCF-MF (genomic cluster family–molecular feature) link predictions from one or more scoring functions, a curated set of known validated links for the same strain(s), and need to assess whether combining or filtering by percentile thresholds improves.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
derived_from:
- doi: 10.1371/journal.pcbi.1008920
  title: NPLinker
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- NPLinker, a software framework to link genomic and metabolomic data
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker
    doi: 10.1371/journal.pcbi.1008920
    title: NPLinker
  dedup_kept_from: coll_nplinker
schema_version: 0.2.0
---

# validated-link-enrichment-analysis

## Summary

Quantifies whether genomic-metabolomic links scoring in the top percentile (e.g., 90th) of one or more scoring functions are enriched for experimentally validated pairs, using Fisher exact test to compare enrichment across individual and combined scoring strategies. This skill detects whether high-scoring predictions align significantly better with known true links than chance.

## When to use

When you have a ranked list of GCF-MF (genomic cluster family–molecular feature) link predictions from one or more scoring functions, a curated set of known validated links for the same strain(s), and need to assess whether combining or filtering by percentile thresholds improves prioritization of true links over false positives.

## When NOT to use

- Input lacks curated validated links or ground truth pairs—enrichment analysis cannot be computed without a reference set of known true links.
- Scoring functions have not been standardised or are on incomparable scales—raw unnormalised scores (e.g., raw strain correlation biased by link size) will distort percentile-based filtering and mask genuine enrichment patterns.
- Sample size is too small (< 50 validated links total across all datasets pooled)—statistical power becomes insufficient to detect significant enrichment or distinguish between strategies.

## Inputs

- GCF-MF link predictions with raw and standardised strain correlation scores (σ_corr, σ*_corr)
- GCF-MF link predictions with IOKR scores (σ_IOKR, σ*_IOKR)
- Combined scored GCF-MF links (e.g., s'1/2 = sgn(s'_corr)|s'_corr|^1/2 + sgn(s'_IOKR)|s'_IOKR|^1/2)
- Curated validated GCF-MF pairs from Paired Omics Data Platform or MIBiG-GNPS with antiSMASH BLAST matching

## Outputs

- Proportion of validated links for all links, top raw correlation, top standardised correlation, top IOKR, and top combined scores
- Fisher exact test p-values comparing joint vs. single-function enrichment
- Contingency tables (validated/non-validated × above/below percentile threshold) per scoring function and per dataset

## How to apply

Load the predicted GCF-MF links with their scores (raw and/or standardised strain correlation σ*_corr, IOKR σ*_IOKR, or combined scores) and identify the subset of links that are experimentally validated from curated repositories (e.g., MIBiG-GNPS pairs with antiSMASH BLAST matching cumulative score ≥10000). Apply percentile thresholds (e.g., 90th percentile) independently for each scoring function and for joint criteria (both functions above threshold). Calculate the proportion of validated links within each filtered subset. Use Fisher exact test to compute two-tailed p-values comparing the enrichment of validated links in the joint top-percentile group against enrichment in either individual score's top-percentile group. A p-value <0.05 indicates that combining scoring functions significantly improves link prioritization.

## Related tools

- **antiSMASH** (Detects biosynthetic gene clusters (BGCs) in microbial genomes; provides BLAST matching (cumulative score) for validated link identification)
- **BiG-SCAPE** (Clusters BGCs into genomic cluster families (GCFs); output GCFs are the genomic side of GCF-MF pairs being scored and validated)
- **NPLinker** (Computes strain correlation and IOKR scores for GCF-MF pairs; produces scored predictions that are input to enrichment analysis) — https://github.com/sdrogers/nplinker
- **GNPS** (Public metabolomics database; spectra and spectral data define the molecular feature (MF) side of GCF-MF pairs)
- **MIBiG** (Curated BGC and metabolite database; paired with GNPS to define validated GCF-MF links via Paired Omics Data Platform)

## Examples

```
# Compute enrichment: load GCF-MF predictions with σ*_corr and σ*_IOKR, filter to 90th percentile for each score and both combined, count validated links (cumulative BLAST score ≥10000) in each subset, and pool across three datasets to compute Fisher exact p-values comparing joint vs. individual enrichment.
```

## Evaluation signals

- Contingency tables are balanced (no zero or extreme cell counts <5) after percentile filtering; Fisher exact test is applicable.
- Top percentile groups (especially joint criterion) show ≥2-fold higher proportion of validated links than all-links baseline or single-function groups.
- Fisher exact test p-values are reported for both individual scores and combined score comparisons; p < 0.05 indicates significant enrichment, supporting complementarity claim.
- Validated link enrichment is consistent across all three independent datasets (Crüsemann, Gross, Leão) with same percentile threshold and scoring function(s).
- Raw vs. standardised score distributions confirm standardisation (σ*_corr, σ*_IOKR) achieves mean ≈ 0 for all links and mean > 2 for validated links before percentile filtering (t-test p < 0.001).

## Limitations

- Method is restricted to GCF-MF pairs present in curated repositories (MIBiG-GNPS); cannot evaluate enrichment on novel or unvalidated links outside these databases.
- Percentile threshold (e.g., 90th) is arbitrary; optimal threshold may vary by dataset or scoring function combination, requiring sensitivity analysis.
- IOKR performance depends on training set composition and is limited to BGCs with considerable homology to MIBiG entries; links to novel or remote BGCs may have inflated IOKR scores.
- Fisher exact test assumes independence of GCF-MF pairs; strain-level correlation or shared BGC ancestry can inflate type I error if not accounted for.
- Small test set size limits breakdown of performance by product type or other subclasses, reducing interpretability of which link types benefit most from combined scoring.

## Evidence

- [other] Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links (p=2.633×10−4 from IOKR and p=0.0208 from standardised correlation) compared to either individual score alone.: "Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links"
- [other] Identify validated links for each dataset from the Paired Omics Data Platform based on curated BGC-spectrum correspondence with antiSMASH BLAST matching (cumulative score ≥10000).: "validated links for each dataset from the Paired Omics Data Platform based on curated BGC-spectrum correspondence with antiSMASH BLAST matching (cumulative score ≥10000)"
- [other] Filter links at the 90th percentile threshold for each scoring function independently and for the joint (both functions) criterion.: "Filter links at the 90th percentile threshold for each scoring function independently and for the joint (both functions) criterion"
- [other] Calculate the proportion of validated links within each percentile group (total links, top raw correlation, top standardised correlation, top IOKR, top combined) for all three datasets.: "Calculate the proportion of validated links within each percentile group (total links, top raw correlation, top standardised correlation, top IOKR, top combined)"
- [other] Pool validated link counts across datasets and compute Fisher exact test p-values comparing enrichment of the joint top percentile group versus either single-function top percentile group.: "Pool validated link counts across datasets and compute Fisher exact test p-values comparing enrichment of the joint top percentile group versus either single-function top percentile group"
- [abstract] Using multiple link-scoring functions together makes it easier to prioritise true links relative to others: "Using multiple link-scoring functions together makes it easier to prioritise true links relative to others"
- [results] Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links, and for the links scoring above the 90th percentile: "proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links, and for the links scoring above the 90th percentile"
