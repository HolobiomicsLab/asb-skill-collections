---
name: noise-perturbation-sensitivity-analysis
description: Use when when comparing pathway analysis methods on metabolomics peak data and you need evidence that one method is more robust than another to the noise and missing peaks that are prevalent in real metabolomics experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - PALS
  - ORA
  - GSEA
  - PALS Viewer
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

# noise-perturbation-sensitivity-analysis

## Summary

Systematically introduce controlled levels of noise and missing data into metabolomics peak intensity data, then recompute pathway activity scores across all three methods (PALS, ORA, GSEA) to assess robustness. This skill evaluates which method maintains score stability under realistic data degradation, using correlation and error metrics to rank methods.

## When to use

When comparing pathway analysis methods on metabolomics peak data and you need evidence that one method is more robust than another to the noise and missing peaks that are prevalent in real metabolomics experiments. Apply this skill before recommending a method for production use or claiming superior robustness in a publication.

## When NOT to use

- Input is already preprocessed pathway activity scores rather than raw peak intensity data; this skill requires access to raw intensities to introduce controlled perturbations.
- You are analyzing gene expression or proteomics data where missing values and noise characteristics differ fundamentally from metabolomics peaks; the perturbation levels (5%, 10%, 20%) are calibrated for metabolomics.
- Your goal is to rank or select a single pathway for a specific sample rather than to evaluate method robustness across many samples; this skill is for method comparison, not pathway prioritization.

## Inputs

- metabolomics peak intensity CSV (rows: peak features with peak ID in column 1, columns: individual sample intensities; optional second line specifying group labels)
- peak annotation CSV (two columns: peak ID and metabolite identifier [KEGG or ChEBI ID])
- reference metabolite pathway annotation database (KEGG, Reactome COMPOUND, or ChEBI)

## Outputs

- robustness comparison table with Spearman correlation and mean absolute difference metrics for PALS, ORA, and GSEA across all noise and missing peak perturbation levels
- line plots or heatmaps visualizing score stability (correlation or error) versus perturbation level for all three methods
- statistical significance test results (paired t-test or non-parametric alternative p-values comparing method pairs)

## How to apply

First, compute baseline pathway activity scores for all three methods (PALS via PLAGE decomposition, ORA, and GSEA adapted for metabolite sets) on clean reference metabolomics peak data with known metabolite pathway annotations. Then, create perturbed datasets by introducing Gaussian noise at 5%, 10%, and 20% of signal intensity levels, and separately by randomly removing 5%, 10%, and 20% of peaks. Re-compute activity scores for each method on each perturbed dataset. For each method and perturbation level, calculate stability metrics: Spearman correlation between baseline and perturbed scores, and mean absolute difference. Perform paired statistical tests (paired t-test or non-parametric Wilcoxon) to determine if differences in stability between methods are significant. Visualize results as line plots or heatmaps showing correlation or error versus perturbation level for all three methods side-by-side to directly compare robustness.

## Related tools

- **PALS** (Pathway activity scoring method using PLAGE (Partial Least Squares) decomposition; one of the three methods compared in the robustness analysis) — https://github.com/glasgowcompbio/PALS
- **ORA** (Over-Representation Analysis; alternative pathway ranking method included in PALS for benchmarking and robustness comparison) — https://github.com/glasgowcompbio/PALS
- **GSEA** (Gene Set Enrichment Analysis adapted for metabolite sets; alternative pathway ranking method included in PALS for benchmarking and robustness comparison) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive Streamlit-based web interface for running PALS, visualizing robustness results, and inspecting significantly changing pathways) — https://pals.glasgowcompbio.org/app/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv baseline_scores.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control; # then repeat with noise-perturbed and peak-removed versions of int_df.csv; compute Spearman correlation between baseline and perturbed output scores for each method.
```

## Evaluation signals

- Robustness table shows quantitative Spearman correlation values between 0 and 1 for each method at each perturbation level; correlation should remain stable (not drop sharply) as perturbation increases if the method is truly robust
- Mean absolute difference metric increases monotonically (or near-monotonically) with perturbation level; method with smallest error increase across all perturbation levels is most robust
- Paired statistical tests show p-value < 0.05 between methods only if robustness differences are genuine (i.e., not due to random variation); multiple comparisons correction applied if comparing >2 methods
- Line plots or heatmaps visually show one method (e.g., PALS) maintaining high correlation or low error across all noise/missing peak levels while alternatives (ORA, GSEA) degrade more sharply
- At least 3 independent noise perturbation levels (5%, 10%, 20%) and 3 missing peak levels (5%, 10%, 20%) each show consistent ranking of methods; no reversal of robustness ranking across levels suggests robust conclusion

## Limitations

- Perturbation levels (5%, 10%, 20% Gaussian noise and random peak removal) are calibrated for metabolomics and may not reflect realistic noise profiles in other modalities (transcriptomics, proteomics) or other mass spectrometry modes (e.g., imaging MS).
- Data imputation strategy (replacement of zero-valued intensity samples by minimum value or factor-level mean) occurs before noise introduction, so robustness analysis reflects method resilience to noise on imputed data, not raw missing data.
- Statistical significance depends on sample size (number of comparisons/pathway repeats); small sample sizes may fail to detect true robustness differences; paired tests require balanced comparison data.
- Robustness ranking may depend on choice of metabolite pathway database (KEGG, Reactome, ChEBI) and species; pathways with very few annotated peaks may show unstable scores regardless of method.

## Evidence

- [other] Introduce controlled levels of noise (Gaussian noise at 5%, 10%, 20% of signal intensity) into copies of the peak data. Introduce controlled missing peak scenarios (random peak removal at 5%, 10%, 20% of peaks) into copies of the peak data.: "Introduce controlled levels of noise (Gaussian noise at 5%, 10%, 20% of signal intensity) into copies of the peak data. Introduce controlled missing peak scenarios (random peak removal at 5%, 10%,"
- [other] Calculate stability metrics (Spearman correlation, mean absolute difference) between baseline scores and perturbed scores for each method across all perturbation levels.: "Calculate stability metrics (Spearman correlation, mean absolute difference) between baseline scores and perturbed scores"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent"
- [other] Summarize robustness comparison in a table showing correlation and error metrics, with statistical significance testing (paired t-test or non-parametric alternative).: "Summarize robustness comparison in a table showing correlation and error metrics, with statistical significance testing (paired t-test or non-parametric alternative)"
- [other] Generate line plots or heatmaps visualizing score stability (correlation or error vs. perturbation level) for PALS, ORA, and GSEA side-by-side.: "Generate line plots or heatmaps visualizing score stability (correlation or error vs. perturbation level) for PALS, ORA, and GSEA side-by-side"
