---
name: peak-removal-robustness-testing
description: Use when when validating a metabolomics pathway analysis method (particularly decomposition-based approaches like PLAGE) against data quality degradation, or when comparing robustness across methods (PLAGE vs. ORA vs. GSEA).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PLAGE (Pathway Level Analysis of Gene Expression)
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pals
    doi: 10.3390/metabo11020103
    title: pals
  dedup_kept_from: coll_pals
schema_version: 0.2.0
---

# peak-removal-robustness-testing

## Summary

Assess the stability of pathway activity rankings under random peak dropout to validate that pathway scoring methods can tolerate missing metabolite identifications—a common problem in metabolomics datasets. This skill measures whether top-ranking pathways remain stable as peaks are progressively removed from the dataset.

## When to use

When validating a metabolomics pathway analysis method (particularly decomposition-based approaches like PLAGE) against data quality degradation, or when comparing robustness across methods (PLAGE vs. ORA vs. GSEA). Apply this skill to datasets where peak identification is uncertain or peak dropout due to instrument noise, dynamic range limits, or post-processing filtering is expected to occur.

## When NOT to use

- Input dataset is already heavily pre-filtered or normalized by vendor software; peak removal may no longer reflect realistic noise scenarios.
- Pathway database is incomplete or pathway annotations are sparse (< 50% of peaks matched to entities); results will not generalize.
- Analysis goal is peak identification or spectrum-to-structure matching; this skill validates pathway ranking stability, not annotation quality.

## Inputs

- Peak intensity matrix (CSV format: rows=peak features with peak ID in column 1, columns=individual samples)
- Pathway annotation matrix (CSV format: peak ID, pathway/metabolite entity ID)
- Experimental design specification (comparisons as case/control pairs)

## Outputs

- Rank-order correlation values (Spearman's rho or Kendall's tau) vs. peak removal rate
- Pathway retention percentage (proportion of top-K pathways remaining in top-K set) vs. removal rate
- Stability plot (correlation or retention % on y-axis vs. removal rate on x-axis)
- Tabulated results showing correlation and retention metrics for each noise/removal condition

## How to apply

Starting from a clean reference metabolomics dataset (peak intensity matrix with pathway annotations), run the pathway analysis method (e.g., PLAGE via PALS) on unperturbed data and record ranked pathway activity scores as a baseline. Then systematically create perturbed copies by removing random peaks at increasing rates (e.g., 0%, 5%, 10%, 15%, 20% random peak removal) and re-run the same method on each perturbed dataset using identical pathway decomposition settings. Compute rank-order correlation (Spearman's rho or Kendall's tau) between perturbed rankings and the clean baseline for each removal rate. Additionally, tabulate the percentage of top-K pathways (K=5, 10, 20) that persist in the top-K set as removal intensity increases. A robust method should maintain high rank-order correlation and pathway retention across all removal conditions.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Primary method to execute pathway decomposition (PLAGE, ORA, GSEA) on perturbed datasets and compute ranked pathway activity scores) — https://github.com/glasgowcompbio/PALS
- **PLAGE (Pathway Level Analysis of Gene Expression)** (Decomposition algorithm used within PALS to compute pathway activity scores that are then ranked for stability comparison) — https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-6-225
- **ORA (Over-Representation Analysis)** (Alternative pathway ranking method included in PALS for benchmarking robustness comparison against PLAGE) — https://github.com/glasgowcompbio/PALS
- **GSEA (Gene Set Enrichment Analysis)** (Alternative pathway ranking method included in PALS for benchmarking robustness comparison against PLAGE) — https://github.com/glasgowcompbio/PALS

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control
```

## Evaluation signals

- Spearman's rho or Kendall's tau correlation between perturbed and baseline rankings remains > 0.8 across all tested removal rates (0–20%)
- Top-K pathway retention does not drop below 80% until 15%+ peak removal; steeper retention curves indicate lower robustness
- Rank-order correlation decays smoothly as removal rate increases (no sudden jumps or reversals), indicating consistent behavior
- Pathway retention and correlation profiles are consistent within replicate runs on independently perturbed datasets (stochastic stability)
- PLAGE-based stability outperforms ORA and GSEA on the same removal conditions (comparative benchmark validation)

## Limitations

- Peak removal is uniformly random; realistic peak dropout may correlate with peak intensity or spectral region, which could yield different stability profiles.
- Findings are specific to metabolomics; applicability to proteomics or transcriptomics depends on whether pathway coverage and annotation density are comparable.
- Stability is computed on a single baseline dataset; generalization to other metabolomics cohorts (e.g., different organisms, tissue types, instruments) is not tested here.
- The skill does not address systematic peak misidentification (false positives in annotation); it only measures robustness to missing (unidentified) peaks.

## Evidence

- [other] How does the rank-order stability of top-scoring pathways in PALS degrade as Gaussian noise and random peak removal increase in severity across a metabolomics dataset?: "How does the rank-order stability of top-scoring pathways in PALS degrade as Gaussian noise and random peak removal increase in severity across a metabolomics dataset?"
- [other] PALS demonstrates robustness to noise and missing peaks in metabolomics data, outperforming ORA and GSEA alternatives on these dimensions.: "PALS demonstrates robustness to noise and missing peaks in metabolomics data, outperforming ORA and GSEA alternatives on these dimensions."
- [other] For each noise level (0%, 5%, 10%, 15%, 20%, 25% Gaussian noise intensity and 0%, 5%, 10%, 15%, 20% random peak removal rate), create a perturbed copy of the dataset.: "For each noise level (0%, 5%, 10%, 15%, 20%, 25% Gaussian noise intensity and 0%, 5%, 10%, 15%, 20% random peak removal rate), create a perturbed copy of the dataset."
- [other] Compute rank-order correlation (Spearman's rho or Kendall's tau) between perturbed pathway rankings and clean baseline ranking for each noise condition.: "Compute rank-order correlation (Spearman's rho or Kendall's tau) between perturbed pathway rankings and clean baseline ranking for each noise condition."
- [other] Compute the percentage of top-K pathways (K=5, 10, 20) that remain in the top-K set across noise conditions.: "Compute the percentage of top-K pathways (K=5, 10, 20) that remain in the top-K set across noise conditions."
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] decomposes activity levels in pathways via the PLAGE method: "decomposes activity levels in pathways via the PLAGE method"
