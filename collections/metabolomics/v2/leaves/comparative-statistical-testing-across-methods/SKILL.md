---
name: comparative-statistical-testing-across-methods
description: Use when when you have applied multiple pathway analysis methods to the
  same metabolomics peak intensity dataset and need to determine which method produces
  more stable pathway activity scores under realistic perturbation conditions (noise
  and missing peaks).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_2269
  tools:
  - PALS (Pathway Activity Level Scoring)
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  - PALS Viewer
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pals_cq
    doi: 10.3390/metabo11020103
    title: pals
  dedup_kept_from: coll_pals_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11020103
  all_source_dois:
  - 10.3390/metabo11020103
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Comparative Statistical Testing Across Methods

## Summary

Quantitatively compare pathway activity scoring methods (PALS, ORA, GSEA) under controlled perturbations of metabolomics peak data using stability metrics and statistical significance testing to establish method robustness rankings.

## When to use

When you have applied multiple pathway analysis methods to the same metabolomics peak intensity dataset and need to determine which method produces more stable pathway activity scores under realistic perturbation conditions (noise and missing peaks). This skill is essential when noise and missing peaks are prevalent in your data, as they directly affect pathway scoring reliability.

## When NOT to use

- Your metabolomics data has no noise or missing peaks—robustness testing under perturbation is only meaningful when these conditions are realistic or already present in your raw data
- You have only one pathway analysis method implemented—comparative testing requires at least two independent methods to compare
- Your peak annotations are highly incomplete (>50% of peaks unannotated)—pathway scoring methods cannot score pathways if metabolite assignments are sparse

## Inputs

- Peak intensity matrix (CSV format with peak IDs in column 1, sample intensities in columns 2+, optional group labels in row 2)
- Metabolite annotation matrix (CSV with peak IDs and assigned KEGG/ChEBI compound identifiers)
- Pathway database selection (PiMP_KEGG, COMPOUND, or ChEBI for metabolomics)
- Experimental design specification (case/control group definitions and comparison pairs)

## Outputs

- Robustness comparison table with Spearman correlation and mean absolute difference metrics for PALS, ORA, and GSEA across all perturbation levels
- Statistical significance test results (p-values from paired t-test or non-parametric alternative)
- Line plots showing score stability (correlation or error) versus perturbation level for all three methods
- Heatmaps or summary visualizations ranking method robustness under noise and missing-peak conditions

## How to apply

Compute baseline pathway activity scores using each method (PALS via PLAGE decomposition, ORA, and GSEA adapted for metabolite sets) on your primary metabolomics peak dataset. Then systematically introduce controlled perturbations: add Gaussian noise at 5%, 10%, and 20% of signal intensity to separate copies of the data, and separately create missing-peak scenarios by randomly removing 5%, 10%, and 20% of peaks. Re-compute all three methods' scores on each perturbed dataset. For each method and perturbation level, calculate stability metrics comparing baseline and perturbed scores using Spearman correlation (higher is more robust) and mean absolute difference (lower is more robust). Apply paired statistical testing (paired t-test or non-parametric alternative) across all perturbation levels to assess whether differences in robustness are statistically significant. Visualize results as line plots or heatmaps showing correlation or error metrics versus perturbation level for side-by-side method comparison.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Primary pathway activity scoring method using PLAGE (singular value decomposition) decomposition; one of three methods compared for robustness) — https://github.com/glasgowcompbio/PALS
- **ORA (Over-Representation Analysis)** (Baseline pathway analysis method included in PALS for benchmarking robustness against PLAGE and GSEA) — https://github.com/glasgowcompbio/PALS
- **GSEA (Gene Set Enrichment Analysis)** (Baseline enrichment method adapted for metabolite sets; second comparison point for robustness evaluation) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface for running PALS analyses and visualizing pathway ranking results; facilitates interactive robustness exploration) — https://pals.glasgowcompbio.org/app/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control
```

## Evaluation signals

- Spearman correlation values should decrease monotonically or remain near baseline (>0.8) as perturbation level increases; method with highest correlation at each perturbation level is most robust
- Mean absolute difference in pathway activity scores should remain small and increase gradually with perturbation severity; method with lowest error across all perturbation levels demonstrates superior robustness
- Paired t-test or non-parametric test p-values should indicate statistical significance (p < 0.05) when comparing robustness metrics between PALS and alternatives if one method is substantially more stable
- Line plots should show PALS maintaining flatter slope (smaller error growth) versus ORA and GSEA as noise/missing-peak levels increase from 5% to 20%
- No pathways should drop below the detection threshold or have undefined scores in perturbed datasets; all methods should produce complete pathway rankings across all perturbation conditions

## Limitations

- Robustness comparison is specific to the chosen pathway database and metabolite annotation quality; sparse or incomplete annotations reduce the number of scorable pathways and may bias method comparison
- Controlled perturbations (Gaussian noise at fixed percentages, random peak removal) may not reflect real-world noise characteristics in specific MS instruments or data preprocessing workflows
- Statistical significance testing assumes independence between perturbation replicates, which may not hold if noise is correlated across samples or if the same peaks are repeatedly removed
- ORA and GSEA methods adapted for metabolite sets may perform differently than their original formulations for gene expression; comparative results are specific to metabolomics peak data and may not generalize to genomics

## Evidence

- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [other] Introduce controlled levels of noise (Gaussian noise at 5%, 10%, 20% of signal intensity) into copies of the peak data. Introduce controlled missing peak scenarios (random peak removal at 5%, 10%, 20% of peaks) into copies of the peak data.: "Introduce controlled levels of noise (Gaussian noise at 5%, 10%, 20% of signal intensity) into copies of the peak data. Introduce controlled missing peak scenarios (random peak removal at 5%, 10%,"
- [other] Calculate stability metrics (Spearman correlation, mean absolute difference) between baseline scores and perturbed scores for each method across all perturbation levels.: "Calculate stability metrics (Spearman correlation, mean absolute difference) between baseline scores and perturbed scores for each method across all perturbation levels."
- [other] Summarize robustness comparison in a table showing correlation and error metrics, with statistical significance testing (paired t-test or non-parametric alternative).: "Summarize robustness comparison in a table showing correlation and error metrics, with statistical significance testing (paired t-test or non-parametric alternative)."
- [other] Generate line plots or heatmaps visualizing score stability (correlation or error vs. perturbation level) for PALS, ORA, and GSEA side-by-side.: "Generate line plots or heatmaps visualizing score stability (correlation or error vs. perturbation level) for PALS, ORA, and GSEA side-by-side."
