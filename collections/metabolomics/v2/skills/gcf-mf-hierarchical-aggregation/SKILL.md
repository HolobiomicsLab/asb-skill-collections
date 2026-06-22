---
name: gcf-mf-hierarchical-aggregation
description: Use when when you have predicted BGC-spectrum IOKR scores or other pairwise linking scores, and need to rank genomic clusters (GCFs from BiG-SCAPE) against metabolomic clusters (MFs from MS/MS spectra grouping), particularly in NPLinker workflows where one GCF may contain multiple BGCs and one MF.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0821
  tools:
  - NPLinker
  - BiG-SCAPE
  - IOKR
  techniques:
  - LC-MS
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

# GCF-MF hierarchical aggregation

## Summary

Generalizes pairwise BGC-spectrum link scores to Gene Cluster Family (GCF) to Molecular Family (MF) level by computing the maximum score over all constituent BGC-spectrum pairs. This hierarchical aggregation enables scoring of multi-BGC/multi-spectrum links in natural product discovery workflows.

## When to use

When you have predicted BGC-spectrum IOKR scores or other pairwise linking scores, and need to rank genomic clusters (GCFs from BiG-SCAPE) against metabolomic clusters (MFs from MS/MS spectra grouping), particularly in NPLinker workflows where one GCF may contain multiple BGCs and one MF may contain multiple spectra.

## When NOT to use

- When input scores are already aggregated at the GCF-MF level; hierarchical aggregation is a one-way transformation.
- When GCF or MF membership is undefined or empty (no BGCs in a GCF or no spectra in an MF).
- When you need to preserve information about which specific BGC-spectrum pair drove the max score but do not also record the pair ID; track the winning pair separately if forensic detail is required.

## Inputs

- BGC-spectrum IOKR score table (columns: BGC_ID, spectrum_ID, σ_IOKR)
- GCF membership table (columns: GCF_ID, BGC_ID)
- MF membership table (columns: MF_ID, spectrum_ID)

## Outputs

- GCF-MF link score table (columns: GCF_ID, MF_ID, max_IOKR_score, num_pairs_evaluated)
- Ranked GCF-MF pairs sorted by max_IOKR_score descending

## How to apply

Load the table of BGC-spectrum IOKR scores σ_IOKR(m, g) for all predicted pairs. For each candidate GCF-MF pair, retrieve all BGCs assigned to the GCF and all spectra assigned to the MF. Filter the BGC-spectrum score table to only pairs where both the BGC and spectrum are present in the input data. Compute the maximum IOKR score over all qualifying (BGC, spectrum) combinations: σ_IOKR(G, M) = max{σ_IOKR(m, g) : m ∈ M, g ∈ G}. Output a ranked table with columns GCF_ID, MF_ID, max_IOKR_score, and num_pairs_evaluated. The max aggregation rationale is that if even one BGC-spectrum pair shows strong evidence of linkage, the GCF-MF pair warrants investigation; this avoids diluting weak average signals from heterogeneous clusters.

## Related tools

- **IOKR** (Generates BGC-spectrum pairwise link scores (σ_IOKR) that are aggregated by this skill)
- **NPLinker** (Framework orchestrating genomic-metabolomic linking; implements hierarchical aggregation workflow) — https://github.com/sdrogers/nplinker
- **BiG-SCAPE** (Produces Gene Cluster Family (GCF) assignments from antiSMASH BGCs; output GCF_ID is input to aggregation)

## Evaluation signals

- Output table has exactly as many rows as there are unique (GCF_ID, MF_ID) pairs tested; no duplicates.
- Each max_IOKR_score value lies within the range [min, max] of the input BGC-spectrum scores; no score should exceed the global maximum or fall below the global minimum.
- For each row, num_pairs_evaluated ≥ 1 and ≤ (|BGCs in GCF| × |spectra in MF|); verify no false negatives from filtering logic.
- Spot-check 5–10 rows: manually retrieve the constituent BGC-spectrum pairs and confirm the reported max_IOKR_score equals the observed maximum.
- Validated links (from PoDP or other ground truth) should rank significantly higher (p < 0.05 by Mann–Whitney U test) than random GCF-MF pairs, mirroring the p-value of 2.633 × 10⁻⁴ reported for combined IOKR + standardised correlation linkage.

## Limitations

- Max aggregation discards information about the full distribution of BGC-spectrum scores within a GCF-MF pair; a GCF-MF pair with one strong match and many weak matches looks identical to one with all strong matches.
- IOKR scoring itself relies on MIBiG homology to assign molecular structures to BGCs, restricting use to BGCs showing considerable homology; BGCs without characterized homologs will have no IOKR scores and will be omitted from aggregation.
- If a GCF contains BGCs not in the input IOKR score table (e.g. novel, unannotated BGCs), those BGCs are silently filtered out, potentially underestimating the true number of candidate pairs and biasing the aggregation toward characterized BGCs.
- Kernel function and parameter selection for IOKR significantly affects performance but choices are not fully characterized; aggregation quality is downstream of IOKR calibration choices.

## Evidence

- [other] The IOKR score is generalised from BGC-spectrum pairs to GCF-MF pairs by computing the maximum IOKR score over all (BGC in GCF, spectrum in MF) combinations: for a GCF G and MF M, σ_IOKR(M, G) = max{σ_IOKR(m, g) : m ∈ M, g ∈ G}: "The IOKR score is generalised from BGC-spectrum pairs to GCF-MF pairs by computing the maximum IOKR score over all (BGC in GCF, spectrum in MF) combinations: for a GCF G and MF M, σ_IOKR(M, G) ="
- [other] Workflow: (1) Load the set of predicted BGC-spectrum IOKR scores (σ_IOKR values for individual pairs). (2) For each GCF-MF pair, retrieve all associated BGCs in the GCF and all spectra in the MF. (3) Filter to (BGC, spectrum) pairs where both elements are present in the input IOKR score table.: "1. Load the set of predicted BGC-spectrum IOKR scores (σ_IOKR values for individual pairs). 2. For each GCF-MF pair, retrieve all associated BGCs in the GCF and all spectra in the MF. 3. Filter to"
- [other] For each GCF-MF pair, compute the maximum IOKR score over all matching (BGC, spectrum) pairs: σ_IOKR(G,M) = max σ_IOKR(m, g) for m ∈ M, g ∈ G. Output a table with columns: GCF_ID, MF_ID, max_IOKR_score, num_pairs_evaluated.: "For each GCF-MF pair, compute the maximum IOKR score over all matching (BGC, spectrum) pairs: σ_IOKR(G,M) = max σ_IOKR(m, g) for m ∈ M, g ∈ G. 5. Output a table with columns: GCF_ID, MF_ID,"
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
- [discussion] A drawback of the current IOKR scoring method is its reliance on MIBiG homology to assign molecular structures to BGCs, which is needed to compute the molecular fingerprint. This restricts its use to: "A drawback of the current IOKR scoring method is its reliance on MIBiG homology to assign molecular structures to BGCs, which is needed to compute the molecular fingerprint. This restricts its use to"
