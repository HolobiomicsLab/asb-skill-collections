---
name: pathway-rank-stability-assessment
description: Use when when you have completed a PALS pathway analysis on a clean metabolomics peak intensity matrix and pathway annotation set, and you need to verify that the ranked pathway discoveries are not artifacts of favorable data quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS
  - PALS Viewer
  - ORA
  - GSEA
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways, decomposes activity levels in pathways
- we introduce PALS (Pathway Activity Level Scoring), a complete tool that performs database queries of pathways, decomposes activity levels in pathways
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

# pathway-rank-stability-assessment

## Summary

Quantify the robustness of pathway activity rankings under realistic perturbations (Gaussian noise and random peak dropout) to validate that top-scoring pathways remain stable across degraded metabolomics data. This skill is essential for assessing whether PALS pathway decomposition produces reliable discoveries despite the noise and missing peaks prevalent in mass spectrometry workflows.

## When to use

When you have completed a PALS pathway analysis on a clean metabolomics peak intensity matrix and pathway annotation set, and you need to verify that the ranked pathway discoveries are not artifacts of favorable data quality. Apply this skill if your use case requires high confidence in pathway activity scores (e.g., for experimental validation, clinical decision support, or publication) or if you want to compare the robustness of PALS against alternative methods (ORA, GSEA) under realistic data degradation.

## When NOT to use

- Your intensity data already passes rigorous quality control and you have independent biological replication with low technical noise; stability testing adds computational cost without new insight.
- You are performing exploratory hypothesis generation where ranked pathways are used only as a starting point for functional validation and do not require pre-validated robustness.
- Your dataset is small (few samples per group) such that adding noise/dropout scenarios further depletes statistical power; focus first on increasing sample size.

## Inputs

- Peak intensity matrix (CSV: rows=peak features with ID column, columns=samples with group labels)
- Pathway annotation matrix (CSV: peak ID → KEGG or ChEBI compound ID, many-to-many mapping allowed)
- Experimental design specification (comparison pairs: case vs. control group names)
- PALS method choice (PLAGE recommended for decomposition robustness)
- Pathway database selection (PiMP_KEGG, COMPOUND, or ChEBI)

## Outputs

- Rank-order stability plot (x=noise/dropout level, y=Spearman's rho or Kendall's tau)
- Top-K pathway retention table (% of top-K pathways stable across each noise condition)
- Pathway rankings for each noise/dropout condition (CSV or dataframe)
- Summary statistics (mean correlation, retention rates, confidence intervals)

## How to apply

Load your reference metabolomics intensity matrix (peak features × samples) and pathway annotations (peak ID → KEGG/ChEBI compound ID), then run PALS using the PLAGE decomposition method on the unperturbed baseline to establish ground-truth ranked pathway activity scores. Systematically create perturbed copies of the intensity matrix by injecting Gaussian noise (0%, 5%, 10%, 15%, 20%, 25% intensity levels) and independent random peak removal (0%, 5%, 10%, 15%, 20% dropout rates). Re-run PALS on each perturbed dataset using identical pathway decomposition parameters. After each run, compute rank-order correlation (Spearman's rho or Kendall's tau) between the perturbed and clean baseline pathway rankings, and calculate the percentage of top-K pathways (K=5, 10, 20) that remain in the top-K set. Plot stability curves (correlation or retention % vs. noise/dropout severity) and tabulate results; PALS is robust if correlation remains >0.7–0.8 and top-K retention >80% under moderate perturbations.

## Related tools

- **PALS** (Pathway Activity Level Scoring tool that decomposes activity levels in pathways via PLAGE method; used to rank pathways on clean and perturbed datasets and generate stability comparisons) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive web interface (Streamlit-based) for running PALS, inspecting pathway ranking results, and visualizing stability across conditions) — https://pals.glasgowcompbio.org/app/
- **ORA** (Over-representation analysis method included in PALS for benchmarking robustness comparison against PLAGE) — https://github.com/glasgowcompbio/PALS
- **GSEA** (Gene Set Enrichment Analysis method included in PALS for benchmarking robustness comparison against PLAGE) — https://github.com/glasgowcompbio/PALS

## Examples

```
python pals/run_pals.py PLAGE perturbed_int_df.csv annotation_df.csv pathway_ranks_noise_10pct.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- Spearman's rho or Kendall's tau rank correlation between baseline and perturbed pathway rankings remains ≥0.7–0.8 under moderate noise (10–15% Gaussian) and moderate peak dropout (10% removal), indicating rank stability.
- Top-K pathway retention (K=5, 10, 20) remains ≥80% across intermediate noise/dropout conditions; steeper drop-off at extreme conditions (≥20% noise + ≥20% dropout) is acceptable if core pathways persist.
- PALS stability curves show shallower degradation slopes than ORA and GSEA under identical perturbations, confirming the claimed robustness advantage of the PLAGE decomposition approach.
- No pathway flips from significant (p<0.05 or activity score above threshold) to non-significant until noise exceeds ≥20% intensity level, indicating signal-to-noise margin is sufficient.
- Results are reproducible: re-running the same noise/dropout seed produces identical or near-identical rank orderings (Pearson correlation >0.99).

## Limitations

- Stability assessment is specific to the noise model chosen (Gaussian noise and uniform random peak dropout); real metabolomics noise may exhibit non-Gaussian tails or correlated dropout patterns (e.g., systematic ionization bias). Results may not generalize to other perturbation regimes.
- Computational cost scales with the number of noise/dropout levels tested (5–6 noise levels × 5 dropout rates = 25–30 PALS runs); large pathway databases or many samples can be slow.
- Stability depends on baseline dataset quality and pathway annotation coverage; sparse or low-quality annotations will reduce stability independent of the method's inherent robustness.
- Top-K retention metric is sensitive to the choice of K; selecting K=5 may show high stability while K=50 shows degradation. Report results for multiple K values to avoid misleading conclusions.
- The comparison against ORA and GSEA assumes equal implementation quality and parameter tuning; differences in stability may reflect tuning choices rather than fundamental method differences.

## Evidence

- [other] How does the rank-order stability of top-scoring pathways in PALS degrade as Gaussian noise and random peak removal increase in severity across a metabolomics dataset?: "How does the rank-order stability of top-scoring pathways in PALS degrade as Gaussian noise and random peak removal increase in severity"
- [other] PALS demonstrates robustness to noise and missing peaks in metabolomics data, outperforming ORA and GSEA alternatives on these dimensions.: "PALS demonstrates robustness to noise and missing peaks in metabolomics data, outperforming ORA and GSEA alternatives"
- [other] Compute rank-order correlation (Spearman's rho or Kendall's tau) between perturbed pathway rankings and clean baseline ranking for each noise condition.: "Compute rank-order correlation (Spearman's rho or Kendall's tau) between perturbed pathway rankings and clean baseline ranking"
- [other] Compute the percentage of top-K pathways (K=5, 10, 20) that remain in the top-K set across noise conditions.: "Compute the percentage of top-K pathways (K=5, 10, 20) that remain in the top-K set across noise conditions"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data"
- [other] For each noise level (0%, 5%, 10%, 15%, 20%, 25% Gaussian noise intensity and 0%, 5%, 10%, 15%, 20% random peak removal rate), create a perturbed copy of the dataset.: "For each noise level (0%, 5%, 10%, 15%, 20%, 25% Gaussian noise intensity and 0%, 5%, 10%, 15%, 20% random peak removal rate)"
