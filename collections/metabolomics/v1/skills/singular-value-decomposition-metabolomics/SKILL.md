---
name: singular-value-decomposition-metabolomics
description: Use when when you have a log2-normalized, zero-mean, unit-variance intensity matrix (rows=metabolites, columns=samples) and a curated metabolite set database (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - KEGG
  - Reactome
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS2LDA
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pals
    doi: 10.3390/metabo11020103
    title: pals
  dedup_kept_from: coll_pals
schema_version: 0.2.0
---

# singular-value-decomposition-metabolomics

## Summary

Apply singular value decomposition (SVD) to metabolite intensity subsets within defined pathways to extract the first principal component as a pathway activity score. This decomposition-based approach is more robust to noise and missing peaks than ORA and GSEA methods, making it well-suited for metabolomics data where such artifacts are prevalent.

## When to use

When you have a log2-normalized, zero-mean, unit-variance intensity matrix (rows=metabolites, columns=samples) and a curated metabolite set database (e.g., KEGG pathways, Reactome, or user-defined molecular families), and you need to rank pathways or metabolite groups by their activity level in a way that tolerates missing data and measurement noise. Particularly appropriate when individual metabolite measurements are sparse or unreliable.

## When NOT to use

- Input intensity matrix has not been log2-transformed and standardized (unit variance, zero mean); preprocessing must be completed first
- Metabolite annotations are unavailable or unreliable; pathways cannot be mapped to the observed features
- You require gene-level or transcript-level pathway analysis (use transcriptomics/proteomics database IDs such as ENSEMBL or UniProt instead of metabolite IDs)

## Inputs

- Log2-normalized intensity matrix: rows are metabolite/peak features with feature ID in column one; subsequent columns are sample intensities; optional second row contains sample group assignments (CSV format)
- Annotation matrix: two-column CSV with peak/feature IDs (column one) mapped to metabolite database IDs (column two, e.g., KEGG compound ID, ChEBI ID, or UniProt ID); multiple IDs can be assigned to a single peak
- Metabolite set database: pathway or molecular family definitions mapping metabolite identifiers to set membership (e.g., KEGG pathway, Reactome metabolic pathway, GNPS Molecular Families, MS2LDA Mass2Motifs)
- Experimental design specification: comparisons as case/control group pairs (e.g., 'beer1/beer2', 'Stage_1/Control') to define which samples constitute each factor

## Outputs

- Pathway ranking table: CSV with columns for pathway identifier, pathway name, activity score (first principal component magnitude), p-value (permutation test), coverage metric (unique metabolites detected / total pathway metabolites), and unique formulae/metabolites found in that pathway
- Ranked pathways sorted by activity score magnitude or p-value, enabling interpretation of which pathway activities distinguish the compared groups

## How to apply

For each pathway or metabolite set in the database, extract the subset of the intensity matrix corresponding to metabolites assigned to that set. Apply SVD to the subset matrix and extract the first left singular vector (principal component). Use the magnitude of this first principal component as the pathway activity score for that set. Standardize scores across all pathways (zero mean, unit variance) and optionally compute p-values via permutation testing to assess significance. Rank pathways by activity magnitude and compile results into a ranked output table with pathway identifiers, activity scores, and statistical measures (p-value, coverage). The robustness of this approach stems from SVD's ability to capture dominant variance patterns even when some metabolites within a pathway are missing or noisy.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Implements the complete SVD-based decomposition pipeline including database queries, data imputation, SVD per pathway, score normalization, and statistical significance testing) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface (Streamlit-based) for running PALS, visualizing ranked pathway results, inspecting significantly changing pathways, and analyzing molecular families from GNPS and Mass2Motifs from MS2LDA) — https://pals.glasgowcompbio.org/app/
- **KEGG** (Pathway and compound database used for metabolite ID matching and pathway definitions)
- **Reactome** (Metabolic and signaling pathway database queryable in online (Neo4j) or offline mode; supports metabolite, protein, and gene-level analysis)
- **GNPS (Global Natural Products Social Molecular Networking)** (Source of Molecular Families metabolite groupings that can be analyzed using PALS decomposition) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs metabolite groupings that can be analyzed using PALS decomposition) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- SVD is computed successfully for each pathway subset without numerical errors (singular matrix, rank deficiency); verify that the first singular value is larger than subsequent singular values, indicating dominance of the principal component
- Pathway activity scores sum to zero across all pathways after standardization; min and max scores should be symmetric around zero
- P-values are computed via permutation test and fall in range [0, 1]; pathways with low p-values (< 0.05) should show consistent activity direction across biological replicates
- Coverage metric (detected metabolites / pathway size) should be > 0 for included pathways; pathways with very low coverage (< 10% of metabolites detected) may have inflated p-values due to sparse data
- Ranked results show biological coherence: pathways known to be active in the experimental condition (case group) rank higher than control-specific pathways; results are stable under resampling or cross-validation

## Limitations

- Pathway activity score depends on the first principal component only; if metabolites within a pathway show opposing activity trends, the first component may cancel signal and produce low scores despite biological relevance
- Requires complete pathway definitions and metabolite-to-ID mappings; poor annotation quality or missing pathways will reduce coverage and statistical power
- Data imputation (replacing zero intensities with minimum or group mean) may bias SVD if a large proportion of values are missing or below detection limit
- P-value computation via permutation testing is computationally expensive for large pathway databases or high-dimensional sample sets; no correction for multiple hypothesis testing is performed within PALS output (user responsibility)
- SVD-based scores are sensitive to outliers and extreme values; robust preprocessing (log transformation, standardization, outlier handling) is essential

## Evidence

- [other] For each pathway, apply PLAGE (Pathway Level Analysis of Gene Expression) decomposition via singular value decomposition (SVD) on the subset of metabolites assigned to that pathway. Extract the first principal component (singular vector) from each pathway's SVD as the pathway activity score.: "For each pathway, apply PLAGE (Pathway Level Analysis of Gene Expression) decomposition via singular value decomposition (SVD) on the subset of metabolites assigned to that pathway. Extract the first"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] decomposes activity levels in pathways via [the PLAGE method]: "decomposes activity levels in pathways via the PLAGE method"
- [readme] The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples."
- [readme] the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
