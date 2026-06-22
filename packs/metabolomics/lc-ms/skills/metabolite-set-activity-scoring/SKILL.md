---
name: metabolite-set-activity-scoring
description: Use when when you have log2-normalized, standardized peak intensity data (rows=peaks, columns=samples) with compound annotations (peak-to-metabolite mappings via KEGG/ChEBI IDs) and need to collapse individual peak signals into pathway-level summary scores for statistical comparison across.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  - Reactome database
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS2LDA
  techniques:
  - LC-MS
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
  - build: coll_pals
    doi: 10.3390/metabo11020103
    title: pals
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

# metabolite-set-activity-scoring

## Summary

Compute single pathway or metabolite set activity scores from peak intensity matrices using decomposition-based methods (PLAGE), enabling robust summarization of multi-metabolite pathway activity that resists noise and missing peaks common in LC-MS/MS metabolomics data.

## When to use

When you have log2-normalized, standardized peak intensity data (rows=peaks, columns=samples) with compound annotations (peak-to-metabolite mappings via KEGG/ChEBI IDs) and need to collapse individual peak signals into pathway-level summary scores for statistical comparison across experimental groups. Apply this especially when peak data contain significant noise or missing values, as PLAGE decomposition is more robust than ORA or GSEA under these conditions.

## When NOT to use

- Input peak intensity data has not been log2-transformed and standardized to zero mean and unit variance — preprocessing is mandatory.
- Peaks lack reliable metabolite annotations; if >50% of peaks are unmapped, pathway coverage will be too sparse for robust decomposition.
- Your goal is to rank individual metabolites (peaks) rather than aggregate pathway activity; use univariate statistical tests instead.

## Inputs

- Peak intensity matrix (CSV: rows=peak IDs, columns=samples with optional group labels row)
- Peak-to-metabolite annotation matrix (CSV: peak ID → KEGG/ChEBI ID)
- Pathway database (KEGG, Reactome COMPOUND/ChEBI, or user-defined metabolite set list)
- Experimental design specification (group labels and case/control comparisons)

## Outputs

- Pathway activity score matrix (rows=pathways, columns=experimental groups/samples)
- Pathway ranking table with p-values, coverage metrics (unique formulae in pathway vs. detected in dataset), and effect sizes
- Stability metrics if perturbation testing is performed (Spearman correlations, MAE vs. baseline across noise/missingness levels)

## How to apply

Load your peak intensity matrix (pre-processed: log2-transformed, zero-mean unit-variance standardized) and annotation matrix (peak ID → KEGG/ChEBI ID mappings). Query a pathway database (KEGG via PiMP, Reactome COMPOUND, or user-defined metabolite sets from GNPS/MS2LDA) to retrieve pathway memberships. For each pathway, extract the subset of peaks annotated to metabolites in that pathway. Apply PLAGE (Pathway Level Analysis of Gene Expression, adapted for metabolites via singular value decomposition) to compute a single activity score per pathway per experimental group by decomposing the pathway submatrix and extracting the first principal component. Perform data imputation before decomposition: replace all-zero intensities in a factor with the minimum intensity threshold (default 5000), and partially-zero intensities with the factor mean. Repeat scoring across all pathways; optionally validate robustness by re-scoring on noise-perturbed (Gaussian ±5–20% of signal) or peak-deletion-perturbed (random removal 5–20%) copies of the intensity matrix, comparing Spearman correlation and mean absolute difference to baseline scores.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Primary implementation of PLAGE decomposition method for metabolite set activity scoring, including database queries, data imputation, and result visualization) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface (Streamlit-based) for interactive PALS execution, result inspection, and prioritization of GNPS Molecular Families and MS2LDA Mass2Motifs by activity level) — https://pals.glasgowcompbio.org/app/
- **ORA (Over-Representation Analysis)** (Included comparative method for pathway enrichment; useful for benchmarking but less robust to noise/missing peaks than PLAGE)
- **GSEA (Gene Set Enrichment Analysis)** (Included comparative method adapted for metabolite sets; enables ranking validation but shows lower robustness than PLAGE on noisy metabolomics data)
- **Reactome database** (Pathway/metabolite set reference source; supports offline (pre-downloaded) or online (Neo4j server) query modes for human and other common species)
- **GNPS (Global Natural Products Social Molecular Networking)** (Source of Molecular Families metabolite groupings, which can be analyzed in PALS as alternative to canonical pathways) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs metabolite groupings for spectral-based metabolite set analysis in PALS) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- Pathway activity scores must be numeric (one value per pathway per group) with no NaN or infinite values in output matrix; pathways with <2 detected metabolites should be filtered out.
- Comparison of Spearman correlation between baseline and noise-perturbed scores should show PLAGE correlation ≥0.85 (at 10% noise level), and exceed ORA/GSEA correlation by >5–10 percentage points on the same perturbation.
- P-values from pathway ranking must follow monotonic relationship with effect size; applying Benjamini–Hochberg FDR correction should yield interpretable sets of significant pathways (typically FDR <0.05 for biologically validated pathways).
- Coverage metrics (F_coverage = detected formulae / total pathway formulae) should be inspectable; pathways with >50% coverage are generally more reliable than those with <20%.
- Re-running PALS on the same input with fixed random seed should produce identical pathway scores (deterministic output); sensitivity analysis across min_replace thresholds (5000–20000) should show pathway rankings stable within top-10 to top-20.

## Limitations

- PLAGE assumes pathway metabolite intensities follow a low-rank structure (well-captured by first principal component); pathways with heterogeneous metabolite profiles may show inflated or deflated scores.
- Requires reliable peak-to-metabolite annotation; multiple peaks mapping to one metabolite or vice versa will increase noise; peaks without any annotation are excluded from analysis.
- Data imputation strategy (mean value for partial zeros, minimum intensity for all-zero factors) is heuristic; extreme minimum intensity thresholds (very low or very high) may bias downstream scores.
- Metabolite set membership is fixed from reference database; pathway definitions may be incomplete or organism-specific (e.g., Reactome coverage varies by species); user-defined sets require manual curation.
- PLAGE activity scores are relative (pathway-specific decomposition); absolute magnitude is not directly comparable across pathways without normalization; direct peak-level interpretation is not possible from pathway scores alone.

## Evidence

- [readme] decomposes activity levels in pathways via the PLAGE method: "decomposes activity levels in pathways via the PLAGE method"
- [readme] robust to noise and missing peaks: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] data imputation on missing values: "Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity"
- [readme] preprocessing and standardization: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples."
- [readme] amenable to analysis of metabolite sets beyond pathways: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways. As demonstrated in PALS Viewer, metabolite sets obtained from the grouping of"
- [readme] coverage metric definition: "The column `unq_pw_F` lists the unique formulae found in that pathway, `tot_ds_F` lists the formula hits found in the dataset, and `F_coverage` is the proportion of `tot_ds_F` to `unq_pw_F`."
