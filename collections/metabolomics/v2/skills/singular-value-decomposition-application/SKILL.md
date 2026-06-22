---
name: singular-value-decomposition-application
description: Use when you have a metabolite intensity matrix (samples × metabolites, log₂-transformed and standardized) and pathway definitions (pathway IDs mapped to metabolite sets), and you need to score pathway activity across samples in a way that tolerates noise and missing peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - PALS
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - Scipy preprocessing
  - Reactome
  - KEGG
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways
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
---

# singular-value-decomposition-application

## Summary

Apply singular value decomposition (SVD) to pathway-specific metabolite intensity submatrices to extract a single dominant activity level vector per pathway across all samples. This decomposition-based approach to pathway scoring is more robust to noise and missing peaks than enrichment methods (ORA, GSEA), particularly for metabolomics data.

## When to use

You have a metabolite intensity matrix (samples × metabolites, log₂-transformed and standardized) and pathway definitions (pathway IDs mapped to metabolite sets), and you need to score pathway activity across samples in a way that tolerates noise and missing peaks. Use this when you want a single activity score per pathway per sample rather than per-metabolite statistics.

## When NOT to use

- Input metabolite intensities are not log₂-transformed or standardized; preprocessing must occur first.
- You require per-metabolite pathway membership scores rather than a single aggregate pathway activity per sample.
- Pathway definitions are empty or contain fewer than 2 metabolites; SVD requires at least rank-1 decomposition and is more stable with multiple features.

## Inputs

- Metabolite intensity matrix (samples × metabolites, log₂-transformed and standardized with zero mean and unit variance)
- Pathway definitions (mapping of pathway identifiers to sets of metabolite identifiers)
- Annotation dataframe (peak IDs mapped to metabolite database IDs such as KEGG or ChEBI)

## Outputs

- Pathway activity level matrix (pathways × samples)
- Ranked pathway results with p-values and coverage metrics

## How to apply

For each pathway, extract the corresponding columns from the standardized intensity matrix to form a pathway-specific metabolite submatrix (samples × metabolites in pathway). Apply SVD to decompose this submatrix into U, S, V^T. Multiply the first left singular vector (U[:, 0]) by the first singular value (S[0]) to obtain the pathway activity level vector across all samples. This first principal component captures the dominant mode of variation in metabolite intensities for that pathway. Compile these activity vectors into a final pathway × sample matrix. The method's robustness stems from using the dominant singular vector rather than simple aggregation, which dampens the influence of individual noisy or missing values.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Complete implementation of SVD-based pathway decomposition; orchestrates database queries, data preprocessing (log₂ transformation, standardization, imputation), SVD application per pathway, and result compilation) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface (Streamlit-based) for interactive pathway analysis, result inspection, and prioritization of Molecular Families or Mass2Motifs by activity level) — https://pals.glasgowcompbio.org/app/
- **Scipy preprocessing** (Standardization of intensity matrix to zero mean and unit variance before SVD)
- **Reactome** (Pathway database source; queried for pathway definitions (metabolic or all pathways) matched by compound ID (KEGG, ChEBI) or protein/gene ID (UniProt, ENSEMBL))
- **KEGG** (Pathway and compound database source; used for metabolomics pathway definitions)

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- SVD is computed successfully for each pathway (no singular matrix or rank-deficiency errors); U and S tensors have expected dimensions (samples and pathway metabolite count respectively).
- First singular value S[0] is the largest in the spectrum for each pathway, confirming it captures the dominant mode of variation.
- Pathway activity vectors have zero mean and unit standard deviation when recomputed across all samples (or fall in expected range for the intensity scale).
- Pathway activity values correlate with known biological contrasts or experimental factors (e.g., case vs. control groups show significant p-values in downstream statistical tests).
- Coverage metric (proportion of dataset formula hits to unique pathway metabolites) is > 0 for pathways included in output; very low coverage (< 10%) may indicate weak signal.

## Limitations

- SVD is sensitive to the quality of compound annotations; peaks without annotations are excluded, reducing coverage if annotation is incomplete.
- Data imputation (replacement of all-zero factors with minimum intensity, or partial-zero factors with group mean) can introduce bias if missingness is not random; the minimum intensity threshold (default 5000) must be tuned per dataset.
- Method assumes that metabolite intensities within a pathway share a common underlying activity; if a pathway contains unrelated metabolite clusters with anticorrelated intensities, the first singular vector may not represent a true biological activity.
- Performance depends on prior log₂ transformation and standardization; omitted or incorrectly applied preprocessing can invalidate results.
- For very small pathways (< 3 metabolites), SVD may be unstable; the article does not specify a minimum pathway size filter.

## Evidence

- [other] PALS uses the PLAGE decomposition method as its core mechanism to decompose activity levels in pathways from metabolite intensity data: "PALS uses the PLAGE decomposition method as its core mechanism to decompose activity levels in pathways from metabolite intensity data, operating on pathway definitions retrieved from database"
- [other] For each pathway, extract the corresponding subset of metabolite columns from the intensity matrix. Apply singular value decomposition (SVD) to each pathway-specific metabolite submatrix. Extract the first left singular vector and multiply by the first singular value to obtain the pathway activity level vector across all samples.: "For each pathway, extract the corresponding subset of metabolite columns from the intensity matrix. 3. Apply singular value decomposition (SVD) to each pathway-specific metabolite submatrix. 4."
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance"
- [readme] If all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor.: "if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values"
- [readme] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
