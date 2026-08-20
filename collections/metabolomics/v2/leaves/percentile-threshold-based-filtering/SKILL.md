---
name: percentile-threshold-based-filtering
description: Use when you have paired genomic-metabolomic link scores (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3172
  tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
  - Paired Omics Data Platform
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were
  run through antiSMASH v5.0.0 for BGC detection
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# percentile-threshold-based-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply percentile-based cutoffs to link-scoring functions to rank and prioritize validated genomic-metabolomic associations. This skill filters links scoring above a fixed percentile threshold (e.g., 90th) for one or multiple scoring functions, then evaluates enrichment of validated links within the filtered set to assess whether the threshold reliably separates true from spurious links.

## When to use

You have paired genomic-metabolomic link scores (e.g., strain correlation, IOKR, or combined scores) computed across all possible BGC-spectrum pairs, a curated set of validated links from the Paired Omics Data Platform or similar gold standard, and you need to determine whether a fixed percentile threshold can improve signal-to-noise by enriching true links relative to the baseline. Use this skill when filtering by a single percentile level on one or both dimensions, then comparing enrichment statistics.

## When NOT to use

- Input scores are already on a fixed scale (e.g., 0–100) and you need to preserve absolute thresholds across independent studies—percentile filtering will be study-specific and non-comparable.
- Validated link set is very small (n < 20) or severely imbalanced; Fisher exact test and enrichment fractions may lack power or be unstable.
- You lack a curated gold standard; filtering without validation targets is circular and will not yield meaningful enrichment p-values.

## Inputs

- Link score matrix or table with columns: BGC/GCF_ID, MF/spectrum_ID, score_function_name, score_value for all candidate pairs
- Validated link set: curated BGC-spectrum pairs from Paired Omics Data Platform or equivalent gold standard with validation provenance

## Outputs

- Filtered link table: subset of input links passing the percentile threshold for one or both scoring functions
- Enrichment statistics table: rows for 'all links', 'top percentile (function A)', 'top percentile (function B)', 'top percentile (both)'; columns for total links, validated count, enrichment fraction, Fisher p-value

## How to apply

First, compute or import link scores for all candidate BGC-MF (or GCF-MF) pairs across your dataset(s). Filter links independently at the 90th percentile (or other decision threshold) for each scoring function—e.g., retain only pairs where standardised strain correlation σ*_corr ≥ 90th percentile value, or where standardised IOKR σ*_IOKR ≥ 90th percentile value. For joint filtering, retain links meeting BOTH criteria simultaneously. Next, identify validated links from a curated source (e.g., Paired Omics Data Platform with antiSMASH BLAST cumulative score ≥10000). Calculate the proportion of validated links (enrichment fraction) within each filtered group and compare against baseline (all links). Use Fisher exact test or equivalent on contingency tables pooled across datasets to compute p-values; threshold typically p < 0.05. The rationale is that percentile filtering is threshold-agnostic and comparable across scoring functions with different scales; joint filtering captures complementarity by requiring both scoring functions to agree on high-confidence links.

## Related tools

- **antiSMASH** (Detects BGCs in microbial genomes and provides BLAST-based matching (cumulative score ≥10000) for validation of genome-metabolite links) — https://antismash.secondarymetabolites.org
- **BiG-SCAPE** (Clusters BGCs into GCFs, which are then scored and filtered by percentile thresholds in link ranking)
- **NPLinker** (Framework that implements strain correlation and IOKR scoring functions, and orchestrates percentile-based filtering of GCF-MF links) — https://github.com/sdrogers/nplinker
- **Paired Omics Data Platform** (Provides curated validated genomic-metabolomic link pairs, used as gold standard for enrichment testing)

## Evaluation signals

- Validated links are enriched (higher proportion) in the top percentile group compared to all links; Fisher exact test p-value ≤ 0.05 indicates significant enrichment.
- Joint percentile filtering (both scoring functions) shows equal or better enrichment than either function alone, confirming complementarity (evidence: 90th percentile combined p=2.633×10−4 from IOKR vs. p=0.0208 from correlation alone).
- Percentile thresholds are consistent and reproducible across independent datasets (Crüsemann, Gross, Leão); enrichment trends align.
- Number of links retained after filtering scales predictably with percentile level (e.g., 90th percentile typically retains ~10% of all links); verify no degenerate filtering (0 or 100% retention).
- Validated link counts across pooled datasets are sufficient for Fisher exact test (expected cell counts ≥5) and p-values are two-tailed.

## Limitations

- Percentile filtering is dataset-dependent; the 90th percentile cutoff will differ across studies with different score distributions, limiting cross-study comparability of absolute thresholds.
- Joint filtering at high percentiles (e.g., both functions ≥ 90th) may yield very few links, reducing statistical power; trade-off between precision (fewer false positives) and recall (more true positives discovered).
- Enrichment analysis relies on the quality and completeness of the curated validated link set; missing or mislabeled gold standard links will bias p-values and enrichment fractions.
- IOKR performance is restricted to BGCs with considerable MIBiG homology; percentile filtering on IOKR scores will not improve ranking of novel or divergent BGCs lacking training data homology.

## Evidence

- [methods] Filter links at the 90th percentile threshold for each scoring function independently and for the joint (both functions) criterion. Calculate the proportion of validated links within each percentile group.: "Filter links at the 90th percentile threshold for each scoring function independently and for the joint (both functions) criterion. 7. Calculate the proportion of validated links within each"
- [results] Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links (p=2.633×10−4 from IOKR and p=0.0208 from standardised correlation) compared to either individual score alone.: "Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links (p=2.633×10−4 from IOKR and p=0.0208 from"
- [results] Both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links at the 90th percentile threshold.: "both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links"
- [methods] Validated links for each dataset were identified from the Paired Omics Data Platform based on curated BGC-spectrum correspondence with antiSMASH BLAST matching (cumulative score ≥10000).: "Identify validated links for each dataset from the Paired Omics Data Platform based on curated BGC-spectrum correspondence with antiSMASH BLAST matching (cumulative score ≥10000)"
- [methods] Pool validated link counts across datasets and compute Fisher exact test p-values comparing enrichment of the joint top percentile group versus either single-function top percentile group.: "Pool validated link counts across datasets and compute Fisher exact test p-values comparing enrichment of the joint top percentile group versus either single-function top percentile group"
