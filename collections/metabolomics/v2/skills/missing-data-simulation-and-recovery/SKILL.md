---
name: missing-data-simulation-and-recovery
description: Use when you have metabolomics peak intensity data with pathway annotations and want to benchmark whether a pathway scoring method (PALS, ORA, GSEA) degrades gracefully under conditions of missing peaks and measurement noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0602
  tools:
  - PALS
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  - scipy.stats
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Missing-Data Simulation and Recovery

## Summary

Systematically introduce controlled missing peaks and noise into metabolomics peak intensity data, then re-analyze using pathway activity scoring methods to assess robustness. This skill evaluates how well pathway analysis methods withstand realistic data quality degradation common in metabolomics.

## When to use

You have metabolomics peak intensity data with pathway annotations and want to benchmark whether a pathway scoring method (PALS, ORA, GSEA) degrades gracefully under conditions of missing peaks and measurement noise. Use this when robustness to data quality is a selection criterion between methods, or when you need to document confidence in pathway rankings under realistic peak detection failure rates.

## When NOT to use

- Input is non-metabolomics data (e.g., RNA-seq, proteomics) without evidence that peak detection dropout and instrumental noise are comparable failure modes.
- Pathway scores or intensity data are already aggregated or summarized; you need raw peak-level intensity matrix to introduce realistic peak-level perturbations.
- You are performing a one-off analysis on a single, high-quality dataset where robustness is not a stated requirement; this skill adds computational cost and complexity.

## Inputs

- Metabolomics peak intensity matrix (CSV: rows=peaks with column 1 = peak_id, columns 2+ = sample intensities)
- Peak annotation file (CSV: two columns, peak_id and metabolite_id as KEGG or ChEBI identifier)
- Experimental design specification (groups and pairwise comparisons)
- Pathway database (PiMP_KEGG, Reactome COMPOUND, or ChEBI)

## Outputs

- Baseline pathway activity score table (method-specific ranking)
- Perturbed pathway score tables (one per noise/missing-peak scenario)
- Stability metrics table (perturbation level vs. correlation/error for each method)
- Statistical significance table (paired t-test or non-parametric p-values)
- Robustness visualization (line plot or heatmap: method × perturbation level)

## How to apply

Start with baseline pathway activity scores computed from clean data using your chosen method (PALS via PLAGE, ORA, or GSEA). Create multiple perturbed copies of the intensity matrix by: (1) introducing Gaussian noise at controlled levels (5%, 10%, 20% of signal intensity), and (2) randomly removing peaks at controlled rates (5%, 10%, 20%). Re-compute pathway scores on each perturbed dataset using the same method and parameters. Calculate stability metrics (Spearman rank correlation, mean absolute difference) between baseline and perturbed scores for each perturbation level. Use paired statistical tests (t-test or non-parametric alternative) to assess whether score degradation is significant. Visualize robustness as line plots or heatmaps showing correlation or error vs. perturbation level; methods with flatter slopes or higher correlations are more robust. The rationale is that metabolomics peak data inherently suffers from instrument noise and detection failures; a robust method produces consistent pathway rankings despite these perturbations.

## Related tools

- **PALS** (Compute baseline and perturbed pathway activity scores via PLAGE decomposition method; primary method under evaluation for robustness) — https://github.com/glasgowcompbio/PALS
- **ORA (Over-Representation Analysis)** (Alternative pathway scoring method for benchmarking robustness against PALS and GSEA) — https://github.com/glasgowcompbio/PALS
- **GSEA (Gene Set Enrichment Analysis)** (Alternative pathway scoring method adapted for metabolite sets; used for robustness comparison) — https://github.com/glasgowcompbio/PALS
- **scipy.stats** (Calculate stability metrics (Spearman correlation, mean absolute difference) and paired statistical tests)

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df_perturbed_10pct_noise.csv notebooks/test_data/HAT/annotation_df.csv test_output_perturbed.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- Baseline pathway scores are reproducible and stable (re-running on clean data yields identical scores).
- Spearman correlation between baseline and perturbed scores decreases monotonically (or near-monotonically) with increasing perturbation level (5% → 10% → 20%).
- One method shows significantly higher correlation retention across all perturbation levels (e.g., PALS ρ > 0.9 at 20% noise vs. ORA ρ < 0.8), evidenced by paired t-test p < 0.05.
- Mean absolute difference between baseline and perturbed scores scales roughly linearly or sub-linearly with perturbation intensity (not exponential breakdown).
- Robustness ranking is consistent across independent runs with different random seeds for peak removal and noise injection.

## Limitations

- Perturbation model (uniform random peak removal, Gaussian noise at fixed % of signal intensity) may not reflect real instrument failure modes (e.g., clustered missing peaks, non-Gaussian noise artifacts, or systematic bias).
- Robustness is evaluated only at three discrete perturbation levels (5%, 10%, 20%); true dose–response may require finer granularity or higher perturbation rates to discriminate methods.
- Conclusion assumes pathway annotations are correct and complete; missing or incorrect annotations confound the measurement of true robustness to peak-level noise.
- Statistical power of paired tests depends on number of pathways and replicates; sparse pathway databases or single-replicate studies may yield inconclusive p-values.

## Evidence

- [other] Introduce controlled levels of noise (Gaussian noise at 5%, 10%, 20% of signal intensity) into copies of the peak data.: "Introduce controlled levels of noise (Gaussian noise at 5%, 10%, 20% of signal intensity) into copies of the peak data."
- [other] Introduce controlled missing peak scenarios (random peak removal at 5%, 10%, 20% of peaks) into copies of the peak data.: "Introduce controlled missing peak scenarios (random peak removal at 5%, 10%, 20% of peaks) into copies of the peak data."
- [other] Calculate stability metrics (Spearman correlation, mean absolute difference) between baseline scores and perturbed scores for each method across all perturbation levels.: "Calculate stability metrics (Spearman correlation, mean absolute difference) between baseline scores and perturbed scores for each method across all perturbation levels."
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [other] Generate line plots or heatmaps visualizing score stability (correlation or error vs. perturbation level) for PALS, ORA, and GSEA side-by-side.: "Generate line plots or heatmaps visualizing score stability (correlation or error vs. perturbation level) for PALS, ORA, and GSEA side-by-side."
