---
name: principal-component-extraction-from-pathway-subsets
description: Use when you have a log2-normalized, zero-mean and unit-variance standardized
  intensity matrix of metabolite features (rows=metabolites, columns=samples) and
  need to compute a single activity score per pathway that reflects the coordinated
  expression behavior of all metabolites assigned to that.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - Reactome
  - GNPS
  - MS2LDA
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs
  database queries of pathways, decomposes activity levels in pathways
- we introduce PALS (Pathway Activity Level Scoring), a complete tool that performs
  database queries of pathways, decomposes activity levels in pathways
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

# Principal component extraction from pathway subsets

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract the first principal component (singular vector) from each metabolite pathway subset using singular value decomposition (SVD) to produce a single quantitative activity score per pathway. This approach is more robust to noise and missing peaks than Over-Representation Analysis or Gene Set Enrichment Analysis alternatives, making it well-suited for metabolomics data.

## When to use

Apply this skill when you have a log2-normalized, zero-mean and unit-variance standardized intensity matrix of metabolite features (rows=metabolites, columns=samples) and need to compute a single activity score per pathway that reflects the coordinated expression behavior of all metabolites assigned to that pathway. Use it particularly when your data contains substantial measurement noise or sparse peak detection, as SVD-based decomposition is more robust than counting-based alternatives.

## When NOT to use

- If the input intensity matrix has not been log2-transformed and standardized to zero mean and unit variance—preprocessing must be completed first
- If you have fewer than 2–3 metabolites assigned to a pathway, as SVD on very small matrices is numerically unstable and the first principal component becomes unreliable
- If your goal is simply to identify which metabolites are significantly differentially abundant (not to score coordinated pathway-level activity), use univariate statistical tests instead

## Inputs

- Intensity matrix (rows=metabolites with KEGG or ChEBI IDs, columns=samples; log2-normalized and standardized to zero mean and unit variance)
- Pathway database (metabolite set definitions mapping metabolites to pathway identifiers)
- Annotation mapping (peak IDs to metabolite compound IDs)
- Experimental design specification (groups and comparisons if applicable)

## Outputs

- Pathway activity scores (first principal component per pathway)
- Ranked pathway results table (pathway identifiers, activity scores, statistical significance metrics)
- Pathway coverage metrics (unique formulae in pathway, formula hits in dataset, coverage proportion)

## How to apply

For each pathway, subset the intensity matrix to include only the metabolites (rows) that are assigned to that pathway according to a pathway database (e.g., KEGG, Reactome, or user-defined metabolite sets). Apply singular value decomposition (SVD) to this pathway-specific submatrix. Extract the first singular vector (principal component) from the SVD result—this vector captures the greatest variance in metabolite intensities across samples within that pathway and serves as the pathway activity score. The magnitude of this first principal component, optionally scaled or normalized across all pathways, ranks the relative activity level of each pathway. Optionally, compute statistical significance (e.g., p-value) to determine whether the pathway's activity differs significantly from baseline or between experimental conditions.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Complete implementation of PLAGE-based pathway decomposition; performs database queries, SVD-based PLAGE decomposition, normalization, ranking, and statistical significance computation) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web-based interactive interface for running PALS, analyzing pathway ranking results, and inspecting significantly changing pathways) — https://pals.glasgowcompbio.org/app/
- **Reactome** (Pathway database source for metabolite set definitions (available for multiple species and can be queried online or offline))
- **GNPS** (Source of Molecular Families (spectral clustering-based metabolite groupings) that can be analyzed as metabolite sets via PALS) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs (spectral motif-based metabolite groupings) that can be analyzed as metabolite sets via PALS) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control
```

## Evaluation signals

- Verify that SVD was applied to each pathway-specific submatrix and that exactly one singular vector (the first, corresponding to maximum variance) was extracted per pathway
- Confirm that the pathway activity score is a scalar value (or small vector per comparison) per pathway, not a matrix or vector of per-metabolite scores
- Check that pathway scores are comparable across pathways (normalized or scaled consistently) and that pathways can be ranked by activity magnitude
- Validate that the output table includes pathway identifiers, activity scores, and at least one statistical significance metric (e.g., p-value or adjusted p-value)
- Spot-check that pathways with more metabolites covered in the dataset and higher coordinate variance produce higher or more significant activity scores, and that results are stable under small perturbations (noise, missing peaks)

## Limitations

- SVD on very small pathway subsets (< 3 metabolites) can be numerically unstable; pathways with few assigned metabolites may not yield reliable activity scores
- The first principal component represents only the direction of greatest variance and does not capture secondary modes of pathway activity that might be biologically meaningful
- Missing data (zero intensities) must be imputed before SVD; the choice of imputation method (mean of non-zero samples, or minimum intensity threshold) can influence the resulting principal component
- Statistical significance of pathway activity depends on the experimental design and number of replicates; studies with few samples may lack power to detect significance
- The method assumes that metabolite intensities within a pathway covary meaningfully; if metabolites in a pathway are independent or anti-correlated, the first principal component may not be biologically representative

## Evidence

- [other] For each pathway, apply PLAGE (Pathway Level Analysis of Gene Expression) decomposition via singular value decomposition (SVD) on the subset of metabolites assigned to that pathway.: "For each pathway, apply PLAGE (Pathway Level Analysis of Gene Expression) decomposition via singular value decomposition (SVD) on the subset of metabolites assigned to that pathway."
- [other] Extract the first principal component (singular vector) from each pathway's SVD as the pathway activity score.: "Extract the first principal component (singular vector) from each pathway's SVD as the pathway activity score."
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples."
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor.: "Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity"
- [readme] the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
