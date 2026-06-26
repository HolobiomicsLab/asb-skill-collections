---
name: missing-data-simulation-in-omics
description: Use when when comparing the robustness of multiple pathway ranking methods
  (e.g., PLAGE, ORA, GSEA) on metabolomics or other omics data, and you need to establish
  which method is least sensitive to peak dropout, instrumental noise, or annotation
  uncertainty.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - PALS (Pathway Activity Level Scoring)
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  - PALS Viewer
  license_tier: restricted
  provenance_tier: literature
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

# Missing-Data Simulation in Omics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically introduce controlled levels of missing peaks and noise artifacts into omics intensity matrices to assess method robustness and generalization. This skill validates whether pathway analysis methods maintain ranking stability and effect size preservation under realistic data degradation scenarios common in metabolomics.

## When to use

When comparing the robustness of multiple pathway ranking methods (e.g., PLAGE, ORA, GSEA) on metabolomics or other omics data, and you need to establish which method is least sensitive to peak dropout, instrumental noise, or annotation uncertainty. Use this skill to benchmark performance under conditions that reflect real-world data quality challenges rather than assuming perfect measurement.

## When NOT to use

- Input intensity data have not been log-2 transformed and standardized (zero mean, unit variance)—apply preprocessing first
- Comparing only a single pathway analysis method; this skill is designed for benchmarking across multiple methods to identify the most robust alternative
- Peak annotations are missing or sparse; method comparison requires sufficient metabolite set membership for meaningful robustness measurement
- Data quality is already known to be very poor (>50% missing by design); this skill assumes you are simulating realistic degradation from otherwise usable data

## Inputs

- Omics intensity matrix (CSV): rows = peak features with peak ID in column 1, columns = individual samples, with optional second row indicating experimental group membership
- Peak annotation table (CSV): two columns — peak ID and metabolite identifier (KEGG or ChEBI compound ID)
- Pathway/metabolite set database (KEGG, Reactome, GNPS Molecular Families, or MS2LDA Mass2Motifs)
- Experimental design specification: group assignments and case-vs-control comparison pairs

## Outputs

- Robustness comparison table: pathway rankings and p-values for original and each noise-perturbed dataset variant
- Rank correlation matrix: pairwise Spearman or Kendall correlation of pathway rankings between original and perturbed results for each method
- Visualization (line plot or heatmap): robustness metrics (rank correlation, effect size preservation) as a function of dropout/noise level
- Method ranking by robustness: which method maintains highest ranking stability across noise conditions

## How to apply

Load the original omics intensity matrix (log-2 transformed and standardized across samples with zero mean and unit variance). Systematically apply controlled dropout at multiple levels (e.g., 10%, 25%, 50% of peaks set to zero or replaced with background noise) to create perturbed dataset variants. Re-run the pathway analysis method(s) being evaluated on each perturbed variant using identical parameters (same pathway database, comparison design, minimum intensity thresholds). Compute robustness metrics comparing results on perturbed data to the baseline (original) results: rank correlation of pathway p-values, effect size preservation, and pathway ranking stability. Generate a comparison table and visualization showing how each method's ranking consistency degrades as a function of noise level. The method that maintains higher rank correlation and stable pathway identifications across noise levels demonstrates superior robustness—particularly important for metabolomics where noise and missing peaks are prevalent.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Computes pathway activity scores via PLAGE decomposition; primary target method for robustness comparison) — https://github.com/glasgowcompbio/PALS
- **ORA (Over-Representation Analysis)** (Baseline pathway ranking method using hypergeometric test; included in PALS for benchmarking against PLAGE) — https://github.com/glasgowcompbio/PALS
- **GSEA (Gene Set Enrichment Analysis)** (Baseline pathway ranking method using ranked scoring; included in PALS for benchmarking against PLAGE) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive web interface for running pathway analysis and inspecting robustness results) — https://pals.glasgowcompbio.org/app/

## Examples

```
# First: run baseline PLAGE analysis
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv baseline_output.csv --db PiMP_KEGG --comparisons Stage_1/Control --min_replace 5000
# Then: create perturbed variants (10%, 25%, 50% peak dropout) and re-run PLAGE, ORA, GSEA on each
# Finally: compute rank correlation and effect size preservation between baseline and perturbed results
```

## Evaluation signals

- Rank correlation of pathway p-values between original and perturbed results remains >0.8 at 10% dropout, >0.6 at 25% dropout for the robust method
- Effect sizes (log fold-change or pathway activity scores) show <10% median absolute deviation between original and 10% perturbed results for robust method
- Pathway ranking stability metric quantifies consistent top-N pathway identification: robust method recovers ≥80% of top 10 pathways at 25% noise level
- Robustness curve (rank correlation vs. noise level) shows one method consistently above others across all tested dropout percentages (10%, 25%, 50%)
- Perturbed dataset variants are correctly constructed: verify peak dropout fraction matches specification and that intensity standardization is reapplied per variant

## Limitations

- Robustness evaluation assumes dropout is random; real-world missing peaks may be biased (e.g., low-abundance compounds systematically underdetected), which could yield different method rankings
- Results are pathway-database-dependent; robustness ranking may differ if comparing methods using KEGG vs. Reactome vs. user-defined metabolite sets with different coverage
- Minimum intensity imputation threshold (default 5000) and log-transformation choices affect pathway activity computation; robustness conclusions may not transfer if preprocessing parameters differ
- Comparison is retrospective on a single dataset; generalization to other cohorts, instruments, or organism species is not guaranteed without replication

## Evidence

- [other] Systematically introduce noise and missing peaks at controlled levels (e.g., 10%, 25%, 50% dropout) to the original peak data. Re-run all three methods (PALS, ORA, GSEA) on each noise-perturbed dataset variant.: "Systematically introduce noise and missing peaks at controlled levels (e.g., 10%, 25%, 50% dropout) to the original peak data. Re-run all three methods (PALS, ORA, GSEA) on each noise-perturbed"
- [other] Compute robustness metrics (e.g., rank correlation, result stability, or effect size preservation) between original and perturbed results for each method.: "Compute robustness metrics (e.g., rank correlation, result stability, or effect size preservation) between original and perturbed results for each method."
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor. The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "Data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples."
- [other] Generate comparison table and visualization showing PALS robustness advantage over ORA and GSEA across noise levels.: "Generate comparison table and visualization showing PALS robustness advantage over ORA and GSEA across noise levels."
