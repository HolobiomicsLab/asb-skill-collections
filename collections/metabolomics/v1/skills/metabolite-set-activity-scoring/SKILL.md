---
name: metabolite-set-activity-scoring
description: Use when you have log2-transformed, standardized peak intensity matrices with metabolite annotations (peak ID → KEGG/ChEBI IDs) and need to test whether groups of peaks co-vary systematically within known pathways or spectral groupings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - GNPS
  - MS2LDA
  - Reactome
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways, decomposes activity levels in pathways
- we introduce PALS (Pathway Activity Level Scoring), a complete tool that performs database queries of pathways, decomposes activity levels in pathways
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

# metabolite-set-activity-scoring

## Summary

Decompose activity levels across user-defined metabolite sets (pathways, molecular families, mass2motifs) from untargeted metabolomics peak intensity data using singular value decomposition (PLAGE method), producing pathway/set-level activity scores robust to noise and missing peaks.

## When to use

You have log2-transformed, standardized peak intensity matrices with metabolite annotations (peak ID → KEGG/ChEBI IDs) and need to test whether groups of peaks co-vary systematically within known pathways or spectral groupings. Apply this skill when noise and missing peaks are prevalent in your data (e.g., from LC-MS/MS peak picking) and you want higher robustness than ORA or GSEA approaches can provide.

## When NOT to use

- Your input is already a feature table or has no metabolite annotations—PLAGE requires mapping peaks to known metabolite sets.
- You need gene-level or transcript-level analysis without metabolomics intensity data; use transcriptomics/proteomics variants (UniProt/ENSEMBL databases) instead.
- Your data lacks standardization or log-transformation; data preprocessing must be completed first (zero mean, unit variance across samples).

## Inputs

- Peak intensity CSV (rows=peak features with column-1 ID; columns=samples; optional row-2=group labels)
- Peak annotation CSV (two columns: peak ID and KEGG/ChEBI/UniProt/ENSEMBL metabolite ID)
- Experimental design dictionary (groups and comparisons: case/control pairs)
- Pathway or metabolite-set database (PiMP_KEGG, COMPOUND, ChEBI, UniProt, ENSEMBL, or custom grouping)

## Outputs

- Pathway ranking dataframe (rows=pathways/metabolite sets; columns include pathway ID, p-value, activity scores, metabolite coverage metrics)
- Activity score matrix (rows=metabolite sets; columns=samples or comparisons)

## How to apply

Prepare two input files: (1) a peak intensity matrix (rows=peak features with IDs, columns=samples; optional second row for group labels) with log2 transformation and zero-mean unit-variance standardization applied; (2) an annotation matrix (peak ID → KEGG/ChEBI/UniProt/ENSEMBL IDs). Load these into a DataSource object with your chosen pathway database (PiMP_KEGG, COMPOUND, ChEBI for metabolomics; UniProt/ENSEMBL for proteomics/transcriptomics). Instantiate a PLAGE decomposition method on the DataSource, which will compute singular value decomposition on the intensity sub-matrix for each metabolite set, extracting the first principal component as the set activity score. Specify experimental design as a dictionary of comparisons (case vs. control group pairs). Call get_pathway_df() to retrieve ranked results. The PLAGE decomposition is amenable to any metabolite grouping (pathways, molecular families from GNPS, mass2motifs from MS2LDA), not just canonical pathways.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Core decomposition framework; wraps PLAGE, ORA, GSEA methods for pathway/metabolite-set activity scoring and ranking) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive web interface (Streamlit-based) for running PALS and visualizing pathway ranking results and metabolite set activity) — https://pals.glasgowcompbio.org/app/
- **GNPS** (Source of Molecular Families spectral groupings that can be analyzed as metabolite sets alongside pathways) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs spectral groupings that can be analyzed as metabolite sets alongside pathways) — http://ms2lda.org/
- **Reactome** (Pathway database for metabolite set definition; supports online (Neo4j server) and offline modes; species-specific metabolic and all pathways)

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control
```

## Evaluation signals

- Verify output pathway ranking table contains columns: pathway ID, p-value, unique pathway metabolites (unq_pw_F), dataset metabolite hits (tot_ds_F), and coverage fraction (F_coverage ≥ 0).
- Check that activity scores remain consistent when noise is systematically introduced at 10%, 25%, 50% peak dropout levels (robustness test via rank correlation or effect-size preservation).
- Confirm that rank correlations between original and noise-perturbed PLAGE results exceed those of ORA and GSEA under same perturbation regimes.
- Validate that pathways with zero metabolite coverage (F_coverage=0) are excluded from output and do not inflate multiple-testing burden.
- Ensure data imputation was applied (zero values in all samples within a factor replaced by min_replace; partial zeros replaced by factor mean).

## Limitations

- Peaks without metabolite annotations are discarded and do not contribute to pathway analysis; high annotation uncertainty (one-to-many peak↔compound mappings) can introduce ambiguity in set membership.
- Offline Reactome mode includes only metabolic pathways for most species; online mode requires Neo4j server access to retrieve all pathways.
- PLAGE extracts only the first principal component per metabolite set; if metabolites within a set are uncorrelated or have heterogeneous response directions, activity scores may lack biological specificity.
- Data standardization (log2 transformation, zero mean, unit variance) is mandatory; poorly standardized or unnormalized intensity data will yield unreliable activity scores.

## Evidence

- [readme] we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways, decomposes activity levels in pathways via the PLAGE method: "performs database queries of pathways, decomposes activity levels in pathways via the PLAGE method"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data"
- [readme] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor. The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "Data imputation...replaced by the minimum intensity value...or by the mean value...transformed to log-2 base and standardised...zero mean and unit variance"
- [readme] Pathways are identified by their id and can be sorted by the `p-value` columns. The column `unq_pw_F` lists the unique formulae found in that pathway, `tot_ds_F` lists the formula hits found in the dataset, and `F_coverage` is the proportion of `tot_ds_F` to `unq_pw_F`.: "`unq_pw_F` lists the unique formulae found in that pathway, `tot_ds_F` lists the formula hits found in the dataset, and `F_coverage` is the proportion"
