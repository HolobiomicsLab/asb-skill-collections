---
name: robustness-analysis-under-perturbation
description: Use when you have completed pathway analysis using multiple competing methods (e.g., PALS, ORA, GSEA) on a metabolomics peak intensity dataset and need to verify that ranking results remain stable when input data is intentionally corrupted.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PALS (Pathway Activity Level Scoring)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11020103
  all_source_dois:
  - 10.3390/metabo11020103
  - 10.1186/1471-2105-6-225
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Robustness Analysis Under Perturbation

## Summary

Systematically evaluate the stability of pathway activity scoring results under controlled degradation of input data (noise injection, missing peaks) to demonstrate comparative robustness across competing methods. This skill is essential for metabolomics pathway analysis where data artifacts are prevalent and method reliability must be quantified.

## When to use

Apply this skill when you have completed pathway analysis using multiple competing methods (e.g., PALS, ORA, GSEA) on a metabolomics peak intensity dataset and need to verify that ranking results remain stable when input data is intentionally corrupted. This is particularly important in metabolomics, where noise and missing peaks are endemic artifacts that may confound pathway interpretations.

## When NOT to use

- Input peak data already lacks missing values or noise—robustness analysis is only meaningful when you have reason to suspect data quality variation
- Single pathway analysis method is being used—comparison requires at least two competing methods (ORA, GSEA, or PLAGE) to establish relative robustness
- Results do not need to be compared across methods or methods are already known to perform identically—robustness analysis cost is not justified

## Inputs

- Peak intensity CSV (rows=peak features with column 1=peak ID; columns 2+=sample intensities; optional row 2=group labels)
- Annotation CSV (peak ID to KEGG/ChEBI metabolite ID mappings)
- Pathway database (KEGG, Reactome/COMPOUND, or ChEBI)
- Experimental design specification (groups and pairwise comparisons)

## Outputs

- Robustness metrics table (method × dropout level, with rank correlation / effect size / p-value stability metrics)
- Comparison visualization (method robustness curves across noise levels)
- Pathway ranking outputs for each perturbed dataset variant (from PALS, ORA, GSEA)

## How to apply

Load the original peak intensity CSV (with peak IDs and sample intensities) and annotation CSV (peak ID to metabolite ID mappings) that were used in the original pathway analysis. For each method (PALS/PLAGE, ORA, GSEA), systematically introduce dropout at controlled levels (e.g., 10%, 25%, 50% of peak intensities set to zero) to create perturbed dataset variants. Re-run all three methods on each perturbed variant using identical parameters (same pathway database, comparisons, and data imputation thresholds). After each run, compute robustness metrics between the original and perturbed result rankings—use rank correlation (Spearman or Kendall τ), pathway rank stability, or effect size preservation (e.g., p-value reproducibility). Generate a comparison table and visualization (e.g., line plot of metric vs. dropout level) showing how each method's rankings degrade under increasing noise. Methods with flatter degradation curves or higher correlation preservation demonstrate greater robustness.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Primary pathway analysis method under test; implements PLAGE decomposition method for computing pathway activity scores) — https://github.com/glasgowcompbio/PALS
- **ORA (Over-Representation Analysis)** (Baseline comparison method using hypergeometric test for pathway enrichment) — https://github.com/glasgowcompbio/PALS
- **GSEA (Gene Set Enrichment Analysis)** (Baseline comparison method using ranked scoring approach) — https://github.com/glasgowcompbio/PALS

## Examples

```
python pals/run.py PLAGE int_df_perturbed_10pct.csv annotation_df.csv output_plage_10pct.csv --db PiMP_KEGG --comparisons case/control; python pals/run.py ORA int_df_perturbed_10pct.csv annotation_df.csv output_ora_10pct.csv --db PiMP_KEGG --comparisons case/control; python pals/run.py GSEA int_df_perturbed_10pct.csv annotation_df.csv output_gsea_10pct.csv --db PiMP_KEGG --comparisons case/control
```

## Evaluation signals

- Rank correlation (Spearman ρ or Kendall τ) between original and perturbed pathway rankings should remain >0.7 for robust methods even at 50% dropout; methods differ in correlation preservation curves
- Pathway p-value rank stability: top N pathways (N=10–20) identified in original analysis should remain in top N ranks after perturbation; count how many rank positions shift
- Comparison table rows should show increasing metric degradation with increasing dropout level (10% → 25% → 50%) for all methods; steeper degradation indicates lower robustness
- Effect size preservation: log2 fold-change or pathway activity score magnitudes should correlate between original and perturbed results (R² > 0.6 for robust methods)
- Visualization should show non-overlapping or well-separated robustness curves for PALS vs. ORA/GSEA, allowing visual discrimination of relative robustness

## Limitations

- Robustness analysis is computationally expensive: re-running all three methods across multiple dropout levels (3–5 levels × 3 methods) multiplies runtime
- Dropout mechanism (random peak intensity zeroing) may not reflect real-world missing peak patterns; peaks below detection limit or co-eluting features may be missing non-randomly
- Robustness metrics (rank correlation, effect size) assume pathway rankings are the primary output; if individual pathway activity scores are the goal, other stability measures may be more appropriate
- Results are specific to the chosen dropout levels and pathway database; robustness findings from 10–50% dropout on KEGG pathways may not generalize to Reactome or different dropout patterns

## Evidence

- [other] Systematically introduce noise and missing peaks at controlled levels (e.g., 10%, 25%, 50% dropout) to the original peak data. Re-run all three methods (PALS, ORA, GSEA) on each noise-perturbed dataset variant.: "Systematically introduce noise and missing peaks at controlled levels (e.g., 10%, 25%, 50% dropout) to the original peak data. Re-run all three methods (PALS, ORA, GSEA) on each noise-perturbed"
- [other] Compute robustness metrics (e.g., rank correlation, result stability, or effect size preservation) between original and perturbed results for each method.: "Compute robustness metrics (e.g., rank correlation, result stability, or effect size preservation) between original and perturbed results for each method."
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [other] Generate comparison table and visualization showing PALS robustness advantage over ORA and GSEA across noise levels.: "Generate comparison table and visualization showing PALS robustness advantage over ORA and GSEA across noise levels."
