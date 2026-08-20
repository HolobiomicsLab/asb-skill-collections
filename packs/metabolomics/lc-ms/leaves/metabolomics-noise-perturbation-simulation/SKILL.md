---
name: metabolomics-noise-perturbation-simulation
description: Use when when benchmarking or validating a pathway analysis method (such as PALS, ORA, or GSEA) on metabolomics data, you need quantitative evidence that the method's pathway rankings remain stable despite noise and missing peaks—conditions prevalent in real LC-MS/MS datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0593
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PLAGE method
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  techniques:
  - LC-MS
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

# metabolomics-noise-perturbation-simulation

## Summary

Systematically degrade a metabolomics peak intensity matrix with controlled levels of Gaussian noise and random peak dropout to assess the robustness of pathway ranking algorithms. This skill evaluates how rank-order stability of pathway activity scores decays under realistic data quality conditions.

## When to use

When benchmarking or validating a pathway analysis method (such as PALS, ORA, or GSEA) on metabolomics data, you need quantitative evidence that the method's pathway rankings remain stable despite noise and missing peaks—conditions prevalent in real LC-MS/MS datasets. Use this skill before deploying a method for clinical or comparative studies.

## When NOT to use

- Your pathway analysis method has already been formally validated on noise-perturbed datasets in peer-reviewed literature; re-running perturbation analysis is redundant.
- Your metabolomics dataset has been pre-filtered, imputed, and quality-controlled such that missing data and noise are already negligible; perturbation tests will not reflect realistic operating conditions.
- You are analyzing a single, non-replicated sample or a very small dataset where statistical robustness testing is not feasible.

## Inputs

- peak intensity matrix (CSV: row IDs, sample columns with numeric intensities)
- compound annotation file (CSV: peak ID, KEGG/ChEBI entity ID pairs)
- experimental design specification (group assignments and case/control comparisons)
- baseline pathway rankings (from clean dataset)

## Outputs

- perturbed peak intensity matrices (one per noise/dropout condition)
- perturbed pathway ranking results (one per noise/dropout condition)
- rank-order correlation table (Spearman rho or Kendall tau vs. noise level)
- top-K pathway retention table (percentage of top-5, top-10, top-20 pathways retained)
- stability plot (correlation or retention percentage on y-axis vs. noise intensity or dropout rate on x-axis)

## How to apply

Start with a clean baseline metabolomics dataset (peak intensity matrix with row IDs and intensity columns across samples, plus compound annotation file mapping peaks to KEGG or ChEBI IDs). Run your pathway analysis method (e.g., PALS with PLAGE decomposition) on the unperturbed data and record ranked pathway activity scores. Then, create perturbed copies of the dataset at each noise level: apply Gaussian noise at intensities 0%, 5%, 10%, 15%, 20%, 25%, and independently apply random peak removal (missing data) at rates 0%, 5%, 10%, 15%, 20%. For each perturbed dataset, run the same pathway method with identical parameters and record the new ranked scores. Compute Spearman's rho or Kendall's tau correlation between perturbed and baseline rankings, and measure the percentage of top-K pathways (K=5, 10, 20) that remain in the top-K set. Generate a stability plot (correlation or retention vs. noise level) and a results table. The rationale is that noise robustness is particularly important for metabolomics peak data, where data quality is often compromised by instrumental artifacts and sample complexity.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (primary pathway ranking method under test; decomposes activity levels via PLAGE and compares robustness to noise and missing peaks against ORA and GSEA) — https://github.com/glasgowcompbio/PALS
- **PLAGE method** (pathway decomposition method used by PALS to compute pathway activity scores from peak intensity data) — https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-6-225
- **ORA (Over-Representation Analysis)** (alternative pathway ranking method included in PALS for benchmarking robustness) — https://github.com/glasgowcompbio/PALS
- **GSEA (Gene Set Enrichment Analysis)** (alternative pathway ranking method included in PALS for benchmarking robustness) — https://github.com/glasgowcompbio/PALS

## Examples

```
# After installing PALS and preparing int_df.csv and annotation_df.csv:
python pals/run.py PLAGE int_df.csv annotation_df.csv baseline_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control; # Then perturb int_df.csv at noise levels 0%-25% and dropout 0%-20%, re-run PLAGE on each, compute Spearman rho between baseline and perturbed rankings, and plot correlation vs. noise level.
```

## Evaluation signals

- Rank-order correlation (Spearman's rho or Kendall's tau) between perturbed and baseline pathway rankings should remain ≥ 0.8 for the most robust method at 25% Gaussian noise and 20% peak dropout combined, indicating strong stability.
- Top-K pathway retention should show a monotonic (or near-monotonic) decline as noise intensity and dropout rate increase, with no erratic jumps or reversals.
- Comparison plots should visually demonstrate that PALS (PLAGE) outperforms ORA and GSEA on the same perturbation conditions, with higher correlation and retention across noise levels.
- All perturbed datasets should successfully pass through the pathway analysis pipeline without crashes or missing output ranks, confirming data format and imputation robustness.
- The stability results should be reproducible when re-run with the same random seed or noise parameters, indicating no algorithmic instability in the perturbation or ranking procedure.

## Limitations

- Perturbation simulations use Gaussian noise, which may not capture all real-world noise distributions (e.g., instrument drift, batch effects, or non-random missing mechanisms in LC-MS/MS data).
- Random peak removal is uniform across all peaks; real metabolomics datasets often show non-random missingness (e.g., low-intensity peaks are more likely to be missed), which this model does not capture.
- Robustness results are specific to the pathway database and metabolite annotation quality used; different KEGG, ChEBI, or Reactome pathway sets may show different stability profiles.
- The skill tests only rank-order stability of pathway scores, not the biological interpretability or clinical validity of the top-ranking pathways.
- Results depend on the choice of pathway decomposition method (PLAGE vs. alternatives) and data preprocessing (log-transformation, standardization, imputation thresholds); different preprocessing can yield different robustness profiles.

## Evidence

- [other] How does the rank-order stability of top-scoring pathways in PALS degrade as Gaussian noise and random peak removal increase in severity across a metabolomics dataset?: "How does the rank-order stability of top-scoring pathways in PALS degrade as Gaussian noise and random peak removal increase in severity"
- [other] PALS demonstrates robustness to noise and missing peaks in metabolomics data, outperforming ORA and GSEA alternatives on these dimensions.: "PALS demonstrates robustness to noise and missing peaks in metabolomics data, outperforming ORA and GSEA alternatives"
- [other] Compute rank-order correlation (Spearman's rho or Kendall's tau) between perturbed pathway rankings and clean baseline ranking for each noise condition.: "Compute rank-order correlation (Spearman's rho or Kendall's tau) between perturbed pathway rankings and clean baseline ranking"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [other] For each noise level (0%, 5%, 10%, 15%, 20%, 25% Gaussian noise intensity and 0%, 5%, 10%, 15%, 20% random peak removal rate), create a perturbed copy of the dataset.: "For each noise level (0%, 5%, 10%, 15%, 20%, 25% Gaussian noise intensity and 0%, 5%, 10%, 15%, 20% random peak removal rate), create a perturbed copy"
