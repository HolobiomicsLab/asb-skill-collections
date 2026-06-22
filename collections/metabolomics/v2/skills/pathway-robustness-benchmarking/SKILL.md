---
name: pathway-robustness-benchmarking
description: Use when when selecting a pathway analysis method for metabolomics peak data where noise and missing peaks are prevalent, or when validating that a chosen method performs consistently across realistic data quality variations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PALS (Pathway Activity Level Scoring)
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  - PALS Viewer
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways,
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pathway-robustness-benchmarking

## Summary

Systematically compare pathway activity scoring methods (PALS, ORA, GSEA) under controlled noise and missing peak perturbations to evaluate robustness for metabolomics data. This skill quantifies method stability across signal degradation scenarios common in mass spectrometry.

## When to use

When selecting a pathway analysis method for metabolomics peak data where noise and missing peaks are prevalent, or when validating that a chosen method performs consistently across realistic data quality variations. Use this skill if your peak intensity matrix has Gaussian noise artifacts or incomplete peak detection, and you need evidence that pathway activity scores remain stable across 5–20% perturbation levels.

## When NOT to use

- Input is already a collapsed feature table or pre-computed pathway scores rather than raw peak intensities—no perturbation baseline to compare.
- Metabolomics data has already undergone aggressive quality filtering or denoising, reducing noise and missing peak artifacts below 5% naturally; perturbation thresholds may be unrealistic.
- Analysis goal is a single point-in-time pathway ranking for interpretation, not method validation; benchmark overhead is not justified.

## Inputs

- peak intensity CSV (rows=peak features with IDs, columns=sample intensities; optional second row with group labels)
- peak annotation CSV (two columns: peak ID and metabolite identifier as KEGG or ChEBI ID)
- reference metabolite pathway annotation or metabolite set grouping
- perturbation parameters (noise levels: 5%, 10%, 20% Gaussian; missing peak rates: 5%, 10%, 20%)

## Outputs

- baseline pathway activity scores (PALS, ORA, GSEA)
- perturbed pathway activity scores for each method and perturbation scenario
- stability metrics table (Spearman correlation, mean absolute difference, p-values)
- line plots or heatmaps of score stability versus perturbation level
- robustness comparison summary with statistical significance

## How to apply

Load metabolomics intensity and annotation CSV files and compute baseline pathway activity scores using PALS (via PLAGE decomposition), ORA, and GSEA on the same reference metabolite pathway annotation. Then systematically introduce controlled perturbations: add Gaussian noise at 5%, 10%, and 20% of signal intensity to copies of the peak data, and separately remove peaks at 5%, 10%, and 20% to simulate missing peaks. Re-compute all three methods' scores on each perturbed dataset. Calculate stability metrics (Spearman correlation and mean absolute difference) between baseline and perturbed scores for each method at each perturbation level. Apply paired t-tests or non-parametric alternatives to assess statistical significance of differences in robustness. Summarize results in a table and generate line plots or heatmaps showing correlation or error versus perturbation level side-by-side for all three methods. PALS should show higher correlation retention and lower error growth than ORA and GSEA across noise and missing peak scenarios.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Primary decomposition method (PLAGE) for computing pathway activity scores on baseline and perturbed metabolomics peak data; serves as reference method expected to show superior robustness.) — https://github.com/glasgowcompbio/PALS
- **ORA (Over-Representation Analysis)** (Alternative pathway ranking method included in PALS for benchmarking; comparison baseline for robustness evaluation.) — https://github.com/glasgowcompbio/PALS
- **GSEA (Gene Set Enrichment Analysis)** (Alternative pathway ranking method adapted for metabolite sets; second comparison baseline for robustness evaluation.) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface for PALS analysis and interactive visualization of pathway ranking results and stability metrics.) — https://pals.glasgowcompbio.org/app/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv baseline.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control; # then loop: add 10% Gaussian noise, re-run, compute Spearman correlation vs baseline
```

## Evaluation signals

- Baseline pathway activity scores are computed and match known pathway biology (e.g., expected metabolic pathways rank high in relevant disease/condition).
- Spearman correlation between baseline and perturbed scores is >0.85 for PALS at 5% perturbation, >0.75 at 10%, >0.65 at 20%; ORA and GSEA show steeper decay.
- Mean absolute difference in pathway scores grows monotonically with perturbation level for all methods; PALS shows smallest gradient.
- Paired statistical tests (t-test or Mann–Whitney U) show significant differences in robustness favoring PALS over ORA and GSEA (p < 0.05).
- Heatmaps or line plots display no crossing of method curves; PALS remains above ORA and GSEA across all perturbation levels for both noise and missing peak scenarios.

## Limitations

- Benchmark assumes Gaussian noise model and random peak removal; real noise patterns may be non-Gaussian or systematic (e.g., low-intensity bias).
- Perturbation thresholds (5%, 10%, 20%) are illustrative; actual metabolomics noise levels vary by instrument, ionization mode, and sample complexity—thresholds should be calibrated to your platform.
- Robustness ranking (PALS > ORA/GSEA) holds for decomposition-based pathway score aggregation; results are specific to metabolomics peak data and may not generalize to gene expression or proteomics.
- Benchmark does not account for computational cost or scalability; PLAGE decomposition may be slower on very large metabolite sets.
- Missing peaks are simulated uniformly at random; real peak loss may be biased toward low-intensity features, which could alter relative method performance.

## Evidence

- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] decomposes activity levels in pathways via the PLAGE method: "decomposes activity levels in pathways via the PLAGE method"
- [other] Introduce controlled levels of noise (Gaussian noise at 5%, 10%, 20% of signal intensity) into copies of the peak data. 6. Introduce controlled missing peak scenarios (random peak removal at 5%, 10%, 20% of peaks) into copies of the peak data.: "Introduce controlled levels of noise (Gaussian noise at 5%, 10%, 20% of signal intensity) into copies of the peak data. 6. Introduce controlled missing peak scenarios (random peak removal at 5%, 10%,"
- [other] Calculate stability metrics (Spearman correlation, mean absolute difference) between baseline scores and perturbed scores for each method across all perturbation levels.: "Calculate stability metrics (Spearman correlation, mean absolute difference) between baseline scores and perturbed scores for each method"
- [other] Generate line plots or heatmaps visualizing score stability (correlation or error vs. perturbation level) for PALS, ORA, and GSEA side-by-side.: "Generate line plots or heatmaps visualizing score stability (correlation or error vs. perturbation level) for PALS, ORA, and GSEA side-by-side"
