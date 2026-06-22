---
name: top-n-accuracy-and-auc-metric-calculation
description: Use when you have a ranked candidate list (e.g., BGCs sorted by IOKR or strain-correlation score) for each test spectrum, a known ground-truth BGC for each spectrum, and you want to measure retrieval performance across multiple recall depths (top-1 through top-200) and overall discrimination.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3391
  tools:
  - GNPS
  - MIBiG
  - Chemistry Development Kit (CDK)
  - antiSMASH
  - NPLinker
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
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
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
---

# top-n-accuracy-and-auc-metric-calculation

## Summary

Compute ranking-based accuracy metrics (top-1, top-5, top-10, etc.) and area-under-curve (AUC) to evaluate how often a correct BGC-spectrum match ranks within the top n candidates, and assess discriminative power against a randomized baseline. This skill is essential for ranking-based retrieval tasks where a single ground-truth target must be re-identified within a sorted candidate list.

## When to use

You have a ranked candidate list (e.g., BGCs sorted by IOKR or strain-correlation score) for each test spectrum, a known ground-truth BGC for each spectrum, and you want to measure retrieval performance across multiple recall depths (top-1 through top-200) and overall discrimination ability (AUC). This is appropriate when you cannot threshold on a single decision boundary and instead need to understand how ranking quality scales with acceptance of more candidates.

## When NOT to use

- Input is a probabilistic classifier with soft confidence scores rather than deterministic ranks—use calibration and threshold-tuning instead.
- The ranking pool is smaller than ~50 candidates or contains many ties at the same score—top-n accuracy becomes unstable and AUC may not be interpretable.
- Ground truth is ambiguous (multiple equally valid BGCs per spectrum)—AUC computation requires binary labels and will produce spurious results.

## Inputs

- ranked BGC candidate list per spectrum (spectrum ID, candidate BGC ID, score)
- ground-truth BGC-spectrum pairs (2966 validated links)
- candidate BGC pool (2242 BGCs with MIBiG homology structure assignments)

## Outputs

- top-n accuracy table (n ∈ {1, 5, 10, 20, 200})
- AUC score and 95% confidence interval
- rank distribution histogram (with validated link positions overlay)
- p-value comparing validated vs. all-link score distributions

## How to apply

For each of the 2966 BGC-spectrum pairs, rank all candidate BGCs (2242 with MIBiG structure assignments) by descending score. Record the rank position of the correct BGC. For each threshold n ∈ {1, 5, 10, 20, 200}, compute top-n accuracy as the proportion of spectra for which the correct BGC appears in positions 1 to n. For AUC, use the rank positions to construct a binary classification problem: for each spectrum, assign a positive label to the correct BGC and negative labels to all other ranked candidates, then compute area-under-the-receiver-operating-characteristic curve. Generate a randomized baseline by permuting BGC ranks for each spectrum independently and repeating the same calculations; valid IOKR performance must substantially exceed baseline AUC (0.5209 baseline vs. 0.6534 observed). Report mean ± variance of scores, p-values comparing validated vs. all-link distributions, and visual histograms overlaying validated-link positions on the full score distribution.

## Related tools

- **GNPS** (source of MS2 spectra (6246 test spectra) matched to MIBiG BGCs via InChIKey for ground-truth pair construction)
- **MIBiG** (source of BGC candidate pool (2242 with structure assignments) and ground-truth validated BGC-spectrum pairs)
- **NPLinker** (framework orchestrating rank computation and metric calculation over BGC-spectrum pairs) — https://github.com/sdrogers/nplinker

## Evaluation signals

- Top-n accuracy must be monotonically non-decreasing with increasing n (e.g., top-1 ≤ top-5 ≤ top-10); any decrease indicates a computational error.
- AUC must fall in [0.5, 1.0]; AUC > 0.5 indicates the scoring function ranks correct BGCs higher than random; AUC = 0.5 exactly suggests no discriminative power.
- Validated-link score distribution must have significantly higher mean than all-link distribution (p < 0.05), with visual separation in histograms.
- Randomized baseline AUC must be approximately 0.5 (±0.01); deviations suggest incorrect rank permutation or label assignment.
- Reported results must match published Table 3 and Figure S2 (IOKR top-1: 0.1208, top-5: 0.1708, AUC: 0.6534; baseline top-1: 0.0, top-5: 0.0014, AUC: 0.5209).

## Limitations

- Performance breakdown by natural product compound class is difficult due to insufficient test set size for statistical stratification.
- IOKR applicability is restricted to BGCs with considerable homology to MIBiG entries; low-homology BGCs are not included in the candidate pool and cannot be ranked.
- Top-n accuracy is sensitive to candidate pool size and composition; results are not directly comparable across datasets with different numbers of structure-annotated BGCs.
- AUC computation assumes all negative candidates are equally undesirable; it does not account for semantic similarity among non-matching BGCs (e.g., same biosynthetic family).

## Evidence

- [results] IOKR top-1 accuracy: 0.1208; top-5: 0.1708; top-10: 0.1870; top-20: 0.2121; top-200: 0.2946; AUC: 0.6534: "Table 3 shows the top-n performance of IOKR, i.e. how often the 'true' BGC match for a given spectrum is among the top n matches returned by IOKR: top-1: 0.1208, top-5: 0.1708, top-10: 0.1870"
- [results] random baseline top-1 accuracy: 0.0; top-5: 0.0014; top-10: 0.0044; top-20: 0.0103; top-200: 0.1486; AUC: 0.5209: "baseline score was estimated by randomising the rank of the structures for each spectrum, and the same process was repeated: top-1: 0.0, top-5: 0.0014, top-10: 0.0044, top-20: 0.0103, top-200:"
- [other] Calculate top-n accuracy (n=1,5,10,20,200) and area-under-curve (AUC) by comparing the rank of the correct BGC relative to all ranked candidates for each spectrum: "Calculate top-n accuracy (n=1,5,10,20,200) and area-under-curve (AUC) by comparing the rank of the correct BGC relative to all ranked candidates for each spectrum, and compare against a randomized"
- [other] IOKR mean score of 0.0105 for all 2966 BGC-spectrum links and 0.0364 for validated links (p=1.7968 × 10−9): "IOKR achieves a mean score of 0.0105 for all 2966 BGC-spectrum links and 0.0364 for validated links (p=1.7968 × 10−9)"
- [other] Construct 2966 BGC-spectrum pairs by matching MIBiG entries to GNPS spectra using the first part of the InChIKey: "Construct 2966 BGC-spectrum pairs by matching MIBiG entries to GNPS spectra using the first part of the InChIKey to avoid confounding by stereoisomerism."
