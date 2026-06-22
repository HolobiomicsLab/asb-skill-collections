---
name: spectral-clustering-membership-resolution
description: Use when you have predicted BGC-spectrum link scores (e.g., IOKR or correlation values) for individual pairs and need to rank GCF-MF associations where each GCF contains multiple BGCs and each MF contains multiple spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0080
  tools:
  - NPLinker
  - BiG-SCAPE
  - IOKR
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them
- Finally, we present NPLinker, a software framework to link genomic and metabolomic data
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

# Spectral Clustering Membership Resolution

## Summary

Aggregate BGC-spectrum link scores from individual pairs to Gene Cluster Family (GCF) and Molecular Family (MF) level using maximum operator, enabling ranking and filtering of higher-order genomic–metabolomic associations. This skill resolves many-to-many relationships inherent in clustered data by computing a single representative score per GCF–MF pair.

## When to use

You have predicted BGC-spectrum link scores (e.g., IOKR or correlation values) for individual pairs and need to rank GCF-MF associations where each GCF contains multiple BGCs and each MF contains multiple spectra. Use this skill when clustering has created these groupings and you need a principled way to rank or filter cross-cluster links for downstream validation or prioritization.

## When NOT to use

- Input scores are already aggregated at the GCF or MF level (no further resolution needed).
- You need to preserve or report scores for all (BGC, spectrum) pairs rather than a single representative per GCF–MF pair.
- The research question requires mean, median, or weighted aggregation instead of maximum (e.g., to account for weak links within a family).

## Inputs

- BGC-spectrum link score table (IOKR scores or standardized correlation scores with columns: BGC_ID, spectrum_ID, score)
- GCF membership table (GCF_ID, BGC_ID associations)
- MF membership table (MF_ID, spectrum_ID associations)

## Outputs

- GCF-MF link score table (GCF_ID, MF_ID, max_score, num_pairs_evaluated)

## How to apply

For each GCF–MF pair, retrieve all constituent BGCs in the GCF and all spectra in the MF. Filter to (BGC, spectrum) combinations where both elements have a score in the input IOKR or correlation score table. Compute the maximum score over all matching pairs: σ(G,M) = max{σ(m,g) : m ∈ M, g ∈ G}. The maximum aggregation is justified because it identifies the strongest individual link evidence within each GCF–MF pair, providing a single comparable metric across all cluster pairs. Output a table with GCF_ID, MF_ID, max_score, and num_pairs_evaluated for filtering and ranking.

## Related tools

- **NPLinker** (Framework that orchestrates BGC clustering, spectrum grouping, and score aggregation for genomic–metabolomic link ranking) — https://github.com/sdrogers/nplinker
- **BiG-SCAPE** (Generates GCF membership by clustering predicted BGCs; output GCF assignments feed into this skill)
- **IOKR** (Produces BGC-spectrum link scores that are aggregated by this skill to GCF-MF level)

## Examples

```
# Pseudocode: for each (GCF_ID, MF_ID) pair, retrieve BGC-spectrum scores and compute max
for gcf_id, mf_id in gcf_mf_pairs:
    bgcs_in_gcf = membership_gcf[membership_gcf['GCF_ID'] == gcf_id]['BGC_ID']
    spectra_in_mf = membership_mf[membership_mf['MF_ID'] == mf_id]['spectrum_ID']
    matching_scores = scores[(scores['BGC_ID'].isin(bgcs_in_gcf)) & (scores['spectrum_ID'].isin(spectra_in_mf))]
    if len(matching_scores) > 0:
        max_score = matching_scores['IOKR_score'].max()
        output_row = (gcf_id, mf_id, max_score, len(matching_scores))
```

## Evaluation signals

- Output table has no NULL or missing scores for GCF-MF pairs where at least one (BGC, spectrum) combination exists in the input score table.
- num_pairs_evaluated > 0 for all rows; a count of 0 indicates no matching input pairs and should be filtered or flagged.
- max_score values are identical to at least one BGC-spectrum score in the input table for each output row (max operator is correctly applied).
- Distribution of max_score should show higher mean and lower p-value for validated GCF-MF links compared to all links, mirroring the enrichment observed in the article (standardized scores show enrichment at p ≈ 2.48 × 10⁻¹¹).
- Rank ordering of GCF-MF pairs by max_score should place known true links in top-k positions more often than random baseline.

## Limitations

- Maximum aggregation favors GCF–MF pairs with at least one strong individual link but may mask weaker consensus signals across many pairs; if all member pairs are weak, a weak maximum is still reported.
- Missing or sparse input score coverage (e.g., IOKR requiring MIBiG homology) means some (BGC, spectrum) combinations will have no score; pairs filtered out may represent true but unmeasured links.
- The choice of maximum over other aggregators (mean, median, weighted sum) is not empirically optimized in the article; alternative aggregation may yield different ranking and enrichment.
- Score comparability across different scoring functions (IOKR vs. standardized correlation) must be addressed separately (e.g., by standardization or combined scoring) before or after aggregation to ensure fair GCF–MF ranking.

## Evidence

- [other] σ_IOKR(M, G) = max{σ_IOKR(m, g) : m ∈ M, g ∈ G}, where σ_IOKR scores individual BGC-spectrum links: "the IOKR score is generalised from BGC-spectrum pairs to GCF-MF pairs by computing the maximum IOKR score over all (BGC in GCF, spectrum in MF) combinations: for a GCF G and MF M, σ_IOKR(M, G) ="
- [other] For each GCF-MF pair, compute the maximum IOKR score over all matching (BGC, spectrum) pairs: "For each GCF-MF pair, compute the maximum IOKR score over all matching (BGC, spectrum) pairs: σ_IOKR(G,M) = max σ_IOKR(m, g) for m ∈ M, g ∈ G"
- [other] Output a table with columns: GCF_ID, MF_ID, max_IOKR_score, num_pairs_evaluated: "Output a table with columns: GCF_ID, MF_ID, max_IOKR_score, num_pairs_evaluated"
- [other] How should IOKR BGC-spectrum link scores be generalised to score GCF-MF links when a GCF contains multiple BGCs and a MF contains multiple spectra?: "How should IOKR BGC-spectrum link scores be generalised to score GCF-MF links when a GCF contains multiple BGCs and a MF contains multiple spectra?"
- [other] Filter to (BGC, spectrum) pairs where both elements are present in the input IOKR score table: "Filter to (BGC, spectrum) pairs where both elements are present in the input IOKR score table"
