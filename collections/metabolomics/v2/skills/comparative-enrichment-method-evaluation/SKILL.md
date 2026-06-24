---
name: comparative-enrichment-method-evaluation
description: Use when you are selecting a pathway enrichment method for metabolomics
  peak data and need to assess which method will remain stable when your data contains
  noise, dropout, or missing identifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - PALS (Pathway Activity Level Scoring)
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  - PALS Viewer
  license_tier: restricted
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

# comparative-enrichment-method-evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically benchmark pathway/metabolite set enrichment methods (PALS, ORA, GSEA) by introducing controlled levels of noise and missing peaks into metabolomics peak data, then measuring robustness using rank correlation and effect size preservation. This skill is essential for validating that a chosen enrichment method will produce stable results even when real-world peak data contains artifacts.

## When to use

You are selecting a pathway enrichment method for metabolomics peak data and need to assess which method will remain stable when your data contains noise, dropout, or missing identifications. Apply this skill if your dataset has high missingness rates or you expect preprocessing artifacts to affect downstream analysis.

## When NOT to use

- Your input is already a pre-computed pathway activity score matrix or feature table — this skill operates on raw peak intensity and annotation data, not pre-ranked results.
- You have clean, high-confidence peak identifications with negligible dropout — robustness testing is most valuable when noise/missingness is a known problem.
- You need to evaluate method performance on a specific biological signal (e.g., recovery of known disease-associated pathways) rather than tolerance to artifacts — use supervised benchmarking instead.

## Inputs

- metabolomics peak intensity matrix (CSV: peak_id × sample_id with group labels)
- compound annotation file (peak_id to KEGG/ChEBI ID mappings)
- pathway/metabolite set database (KEGG, Reactome, or custom)
- experimental design specification (case/control comparisons)

## Outputs

- robustness comparison table (method × noise_level with rank correlation and stability metrics)
- visualization of robustness across noise levels (e.g., line plot showing rank correlation degradation)
- ranked list of enriched pathways/metabolite sets for each method on original data
- quantitative ranking of methods by robustness score

## How to apply

Load a metabolomics peak intensity matrix (CSV with peaks as rows, samples as columns) and a compound annotation file (peak ID to KEGG/ChEBI ID mappings). Run candidate methods (PALS with PLAGE decomposition, ORA with hypergeometric test, GSEA with ranked scoring) on the original, unperturbed dataset to establish baseline pathway activity scores. Systematically introduce noise and missing data at multiple levels (e.g., 10%, 25%, 50% random peak dropout) to create degraded versions of the intensity matrix while keeping annotations constant. Re-run all three methods on each perturbed variant. Compare robustness by computing rank correlation of pathway rankings between original and perturbed results, measuring result stability via effect size preservation, and computing precision/recall metrics if ground-truth pathways are known. Choose the method with the highest robustness across noise levels, as it will generalize better to real noisy metabolomics data.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (primary enrichment method using PLAGE decomposition for pathway activity scoring) — https://github.com/glasgowcompbio/PALS
- **ORA (Over-Representation Analysis)** (baseline enrichment method using hypergeometric test for comparison) — https://github.com/glasgowcompbio/PALS
- **GSEA (Gene Set Enrichment Analysis)** (baseline enrichment method using ranked scoring approach for comparison) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (interactive web interface for running PALS and visualizing results) — https://pals.glasgowcompbio.org/app/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control
```

## Evaluation signals

- Rank correlation between original and 10%/25%/50% perturbed results is ≥0.7 for the chosen method, indicating stable pathway ranking despite data loss
- Effect sizes (e.g., p-values or pathway activity scores) are preserved with <20% relative change across noise levels for the selected method
- The method ranking is consistent: same method shows highest robustness at all three noise levels (10%, 25%, 50%), not just one
- Comparison table includes all three methods with identical noise-injection seeds and parameters, confirming fair benchmarking
- Visualization shows clear separation between methods — the winning method's curve should not overlap substantially with losers at mid-to-high noise levels

## Limitations

- Noise injection via random peak dropout is a simplified model; real metabolomics artifacts may have systematic patterns (e.g., signal suppression, non-random missingness by compound class).
- Robustness rankings may be data-dependent: a method robust on one metabolomics dataset (e.g., beer metabolites) may not rank identically on another (e.g., clinical serum samples with different ionization biases).
- Results assume accurate compound annotations; if annotations are sparse or error-prone, all methods may degrade similarly, masking true algorithmic differences.
- Robustness to noise does not measure biological validity — a method may be robust to artifacts yet miss real biological pathways; combine with supervised benchmarking if ground truth is available.

## Evidence

- [other] Systematically introduce noise and missing peaks at controlled levels (e.g., 10%, 25%, 50% dropout) to the original peak data. Re-run all three methods (PALS, ORA, GSEA) on each noise-perturbed dataset variant.: "Systematically introduce noise and missing peaks at controlled levels (e.g., 10%, 25%, 50% dropout) to the original peak data. Re-run all three methods (PALS, ORA, GSEA) on each noise-perturbed"
- [other] Compute robustness metrics (e.g., rank correlation, result stability, or effect size preservation) between original and perturbed results for each method.: "Compute robustness metrics (e.g., rank correlation, result stability, or effect size preservation) between original and perturbed results for each method."
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [other] Apply ORA (Over-Representation Analysis) on the same dataset using standard hypergeometric test. Apply GSEA (Gene Set Enrichment Analysis) on the same dataset using ranked scoring approach.: "Apply ORA (Over-Representation Analysis) on the same dataset using standard hypergeometric test. Apply GSEA (Gene Set Enrichment Analysis) on the same dataset using ranked scoring approach."
- [other] Load metabolomics peak dataset and pathway/metabolite set database. Apply PALS decomposition using the PLAGE method to compute pathway activity scores.: "Load metabolomics peak dataset and pathway/metabolite set database. Apply PALS decomposition using the PLAGE method to compute pathway activity scores."
