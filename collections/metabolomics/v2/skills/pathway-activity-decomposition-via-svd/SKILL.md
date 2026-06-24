---
name: pathway-activity-decomposition-via-svd
description: Use when when you have a metabolite intensity matrix (samples × metabolites)
  with compound annotations and need to score pathway activity levels for pathway
  enrichment analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS
  - PALS Viewer
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS2LDA
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs
  database queries of pathways
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs
  database queries of pathways,
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

# Pathway Activity Decomposition via SVD

## Summary

Decomposes metabolite intensity data into pathway-level activity scores by applying singular value decomposition (SVD) to pathway-specific metabolite submatrices, yielding a robust activity level vector per pathway across all samples. This approach is particularly suited to metabolomics data where noise and missing peaks are prevalent.

## When to use

When you have a metabolite intensity matrix (samples × metabolites) with compound annotations and need to score pathway activity levels for pathway enrichment analysis. Use this skill especially when your data contains substantial noise or missing peak data, and you wish to avoid limitations of simpler methods like ORA (over-representation analysis) or GSEA that rely on binary membership or ranked lists.

## When NOT to use

- Your input data is already a pathway-level feature matrix or pre-computed activity scores; decomposition should only be applied to raw or preprocessed metabolite intensities.
- You have fewer than 3–4 metabolites annotated per pathway on average; SVD requires sufficient dimensionality to estimate a meaningful dominant singular vector.
- Your analysis requires binary pathway membership decisions (e.g., presence/absence of hits); use ORA instead if you only need over-representation testing.

## Inputs

- Metabolite intensity matrix (CSV, samples × metabolites with group annotations)
- Compound annotation table (peak ID to KEGG/ChEBI/metabolite ID mappings)
- Pathway definitions (pathway ID to metabolite/compound set mappings from KEGG, Reactome, or similar database)

## Outputs

- Pathway activity level matrix (pathway × sample)
- Ranked pathway results with p-values and coverage statistics

## How to apply

Load your log2-transformed, standardized metabolite intensity matrix (zero mean, unit variance across samples) and pathway definitions (pathway identifiers mapped to metabolite sets from a database such as KEGG or Reactome). For each pathway, extract the corresponding subset of metabolite columns from the intensity matrix. Apply SVD to the pathway-specific metabolite submatrix, extract the first left singular vector, and multiply by the first singular value to obtain a single pathway activity level vector across all samples. Compile these vectors into a final pathway × sample matrix. The use of the first singular vector (dominant mode of variation) ensures that the activity score captures the coherent behavior of the pathway's member metabolites, and standardization ensures comparability across pathways with different numbers of member metabolites.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Complete implementation of PLAGE-based pathway activity decomposition with database query integration, data imputation, and statistical ranking) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive web application for running PALS analyses and inspecting pathway ranking results) — https://pals.glasgowcompbio.org/app/
- **ORA (Over-Representation Analysis)** (Baseline method for comparison; performs pathway enrichment based on binary hit counts) — https://github.com/glasgowcompbio/PALS
- **GSEA (Gene Set Enrichment Analysis)** (Baseline method for comparison; uses ranked metabolite statistics) — https://github.com/glasgowcompbio/PALS
- **GNPS (Global Natural Products Social Molecular Networking)** (Source of Molecular Families as alternative metabolite groupings for activity decomposition) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs as alternative metabolite groupings for activity decomposition) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- Pathway activity level vectors have zero mean and unit variance (or are comparable across pathways in magnitude).
- Pathways with high coverage (large fraction of unique pathway metabolites detected in the dataset) produce more stable activity estimates than low-coverage pathways; compare p-value distributions.
- Activity scores for replicate samples within the same experimental group show low variance; between-group variance should exceed within-group variance for true biological differences.
- Comparison with ORA and GSEA results: PLAGE activity scores should be more robust to noise (i.e., pathways ranked as significant should remain stable when a fraction of low-intensity peaks are randomly removed) and to missing peak data.
- Coverage statistics (unq_pw_F, tot_ds_F, F_coverage columns) confirm that metabolites in significant pathways are well-represented in the input dataset.

## Limitations

- SVD assumes a linear dominant mode of variation; if multiple independent metabolite patterns drive pathway activity, the first singular vector may miss important variation.
- The method requires adequate metabolite coverage per pathway; pathways with few annotated member metabolites (< 3–4) may yield unstable or uninformative activity estimates.
- Data imputation (replacing zeros with minimum or mean values) can bias results if missingness is non-random; threshold selection (min_replace parameter) requires domain knowledge.
- The approach is sensitive to outlier metabolites with extreme intensity values; robust scaling or outlier detection may be needed before SVD.
- Database quality and completeness vary; pathways queried from KEGG may differ in coverage and interpretation from Reactome or user-defined metabolite sets.

## Evidence

- [other] For each pathway, extract the corresponding subset of metabolite columns from the intensity matrix. Apply singular value decomposition (SVD) to each pathway-specific metabolite submatrix. Extract the first left singular vector and multiply by the first singular value to obtain the pathway activity level vector across all samples.: "For each pathway, extract the corresponding subset of metabolite columns from the intensity matrix. Apply singular value decomposition (SVD) to each pathway-specific metabolite submatrix. Extract the"
- [readme] decomposes activity levels in pathways via the PLAGE method: "decomposes activity levels in pathways via the PLAGE method"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples."
- [readme] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
