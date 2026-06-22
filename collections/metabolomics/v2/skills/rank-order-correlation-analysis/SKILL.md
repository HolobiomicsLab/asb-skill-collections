---
name: rank-order-correlation-analysis
description: Use when when you have run a pathway ranking method (such as PALS/PLAGE) on clean metabolomics data and wish to assess how sensitive the resulting pathway activity rankings are to realistic data quality issues—specifically Gaussian noise and random peak dropout—which are prevalent in untargeted.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2939
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - ORA and GSEA (included in PALS)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11020103
  all_source_dois:
  - 10.3390/metabo11020103
  - 10.1186/1471-2105-6-225
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# rank-order-correlation-analysis

## Summary

Quantify the stability of pathway activity rankings under perturbation (noise and missing peaks) by computing rank-order correlations (Spearman's rho or Kendall's tau) between baseline and perturbed pathway scores. This skill validates the robustness of pathway ranking methods in metabolomics by measuring how ranking order degrades as data quality decreases.

## When to use

When you have run a pathway ranking method (such as PALS/PLAGE) on clean metabolomics data and wish to assess how sensitive the resulting pathway activity rankings are to realistic data quality issues—specifically Gaussian noise and random peak dropout—which are prevalent in untargeted metabolomics peak detection. This is particularly relevant if comparing pathway ranking methods (ORA, GSEA, PLAGE) or validating a method's suitability for noisy datasets.

## When NOT to use

- Input data is already cleaned and missing-peak-corrected; this skill is designed to stress-test robustness, not to repair data.
- Your goal is to identify differentially active pathways in a single clean dataset; use this skill only to validate the ranking method's reliability before deployment.
- Pathway database or decomposition method has already been validated in prior publications; repeating this stability analysis may add limited new insight unless comparing methods or data modalities.

## Inputs

- Peak intensity matrix (CSV: rows=peak features with peak ID in column 1, columns=sample intensities)
- Peak-to-pathway annotation matrix (CSV: two columns—peak ID and KEGG or ChEBI compound ID)
- Clean baseline pathway activity scores (output from initial PALS/PLAGE run)
- Noise levels and peak removal rates (e.g., Gaussian noise 0–25% in 5% increments, peak dropout 0–20% in 5% increments)

## Outputs

- Rank-order correlation values (Spearman's rho or Kendall's tau) for each noise/dropout condition
- Percentage of top-K pathways retained in top-K set for K=5, 10, 20 across noise conditions
- Stability plot (correlation or retention percentage vs. noise level and/or peak removal rate)
- Tabulated results (noise condition × method × correlation/retention metric)

## How to apply

First, run your pathway ranking method (e.g., PALS using PLAGE decomposition) on the unperturbed intensity matrix and peak-to-pathway annotations, recording the ranked pathway activity scores as the clean baseline. Then, systematically generate perturbed copies of the dataset by adding Gaussian noise (typically 5%, 10%, 15%, 20%, 25% intensity noise) and removing random peaks (0%, 5%, 10%, 15%, 20% dropout rate) in a factorial design. Re-run the ranking method on each perturbed dataset using identical pathway decomposition parameters. For each perturbation condition, compute rank-order correlation (Spearman's rho or Kendall's tau) between the perturbed pathway rankings and the clean baseline ranking. Additionally, compute the percentage of top-K pathways (K=5, 10, 20) that remain in the top-K set across noise conditions. Plot correlation or retention percentage against noise severity (or peak dropout rate) to visualize robustness. Methods with higher correlation slopes and higher retention percentages at high noise levels demonstrate greater ranking stability.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Primary pathway ranking tool that decomposes activity levels via PLAGE method; run on both clean and perturbed datasets to generate ranked pathway scores) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive web interface for visualizing and analyzing pathway ranking results; useful for plotting stability results and inspecting top-ranked pathways) — https://pals.glasgowcompbio.org/app/
- **ORA and GSEA (included in PALS)** (Alternative pathway ranking methods included in PALS for benchmarking and comparing robustness to noise and missing peaks) — https://github.com/glasgowcompbio/PALS

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control
```

## Evaluation signals

- Spearman's rho or Kendall's tau correlation values remain ≥0.8 across the intended noise range, indicating rank-order stability.
- Top-K retention percentages (e.g., for K=10) remain ≥80% at intermediate noise levels (e.g., 10–15% Gaussian noise), confirming consistency of highly-ranked pathways.
- Correlation slope (change in correlation per unit noise) is shallow (low negative slope) compared to alternative methods, demonstrating robustness.
- No inverted or unexpected rank reversals (e.g., pathway ranked #1 in clean data should not drop to rank >50 under moderate noise) when inspecting individual pathway trajectories.
- Tabulated results show systematic degradation of correlation with increasing noise/dropout, not erratic jumps, confirming the stability curve is monotonic and interpretable.

## Limitations

- This skill assumes that Gaussian noise and uniform random peak dropout are representative of real-world metabolomics measurement error; in practice, systematic bias (calibration drift, ion suppression) may not be captured.
- Rank-order correlation does not account for the biological meaningfulness of the top-ranked pathways—a method may preserve rank order by chance while identifying biologically irrelevant pathways.
- Results are specific to the pathway database, decomposition method (e.g., PLAGE), and intensity preprocessing parameters (log2 transformation, standardization) used; changing any of these may alter robustness.
- Computational cost grows with the number of noise/dropout conditions tested and the size of the pathway database; the workflow may be infeasible for very large pathway collections or limited compute resources.

## Evidence

- [other] How does the rank-order stability of top-scoring pathways in PALS degrade as Gaussian noise and random peak removal increase in severity across a metabolomics dataset?: "How does the rank-order stability of top-scoring pathways in PALS degrade as Gaussian noise and random peak removal increase in severity"
- [other] PALS demonstrates robustness to noise and missing peaks in metabolomics data, outperforming ORA and GSEA alternatives on these dimensions.: "PALS demonstrates robustness to noise and missing peaks in metabolomics data, outperforming ORA and GSEA alternatives"
- [other] Compute rank-order correlation (Spearman's rho or Kendall's tau) between perturbed pathway rankings and clean baseline ranking for each noise condition.: "Compute rank-order correlation (Spearman's rho or Kendall's tau) between perturbed pathway rankings and clean baseline ranking"
- [other] Compute the percentage of top-K pathways (K=5, 10, 20) that remain in the top-K set across noise conditions.: "Compute the percentage of top-K pathways (K=5, 10, 20) that remain in the top-K set across noise conditions"
- [other] For each noise level (0%, 5%, 10%, 15%, 20%, 25% Gaussian noise intensity and 0%, 5%, 10%, 15%, 20% random peak removal rate), create a perturbed copy of the dataset.: "For each noise level (0%, 5%, 10%, 15%, 20%, 25% Gaussian noise intensity and 0%, 5%, 10%, 15%, 20% random peak removal rate)"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data"
