---
name: plage-method-metabolite-scoring
description: Use when use PLAGE when you have log2-transformed, standardized metabolite
  intensity data (rows = peak features, columns = samples) with compound annotations
  (peak ID → metabolite database ID mappings), and you want to rank metabolite groupings
  (pathways, GNPS Molecular Families, MS2LDA.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - GNPS
  - MS2LDA
  - Reactome
  license_tier: open
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs
  database queries of pathways
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs
  database queries of pathways,
- To access our interactive Web application PALS Viewer, please visit [https://pals.glasgowcompbio.org/app/]
- Molecular Families from GNPS
- This includes in particular *Molecular Families* from [GNPS](http://gnps.ucsd.edu/)
- Mass2Motifs from MS2LDA
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

# PLAGE Method for Metabolite Set Activity Scoring

## Summary

The PLAGE (Pathway Level Analysis of Gene Expression) method uses singular value decomposition to compute activity scores for metabolite sets (pathways, Molecular Families, Mass2Motifs) from peak intensity matrices. It is more robust to noise and missing peaks than ORA or GSEA, making it well-suited for metabolomics data where such artifacts are prevalent.

## When to use

Use PLAGE when you have log2-transformed, standardized metabolite intensity data (rows = peak features, columns = samples) with compound annotations (peak ID → metabolite database ID mappings), and you want to rank metabolite groupings (pathways, GNPS Molecular Families, MS2LDA Mass2Motifs) by their aggregate activity across experimental conditions. Apply it when noise and missing peaks are expected in your data and you need scores robust to these artifacts.

## When NOT to use

- If metabolite intensities are already aggregated or preprocessed to pathway/set level — PLAGE requires raw peak-level intensity data.
- If you lack compound annotations or metabolite set memberships; PALS cannot assign unannotated peaks to sets.
- If your data have not undergone quality control (extreme outliers, batch effects) that severely distort intensity distributions — address these before standardization.

## Inputs

- Metabolite feature intensity matrix (CSV: peak_id, sample_1, sample_2, … with optional group labels on row 2)
- Compound annotation matrix (CSV: peak_id, entity_id where entity_id is KEGG/ChEBI/UniProt/ENSEMBL ID)
- Metabolite set definitions (pathway database or GNPS Molecular Families / MS2LDA Mass2Motifs groupings)
- Experimental design specification (group membership, case/control comparisons)

## Outputs

- Metabolite set activity score rankings (CSV: pathway_id, activity_score, p_value, unq_pw_F, tot_ds_F, F_coverage)
- PALS Viewer-compatible results format for interactive inspection of significantly changing sets

## How to apply

First, load your metabolite feature intensity matrix (CSV with peak IDs in column 1, sample intensities in subsequent columns; optional group labels on line 2) and your annotation matrix (two columns: peak ID and entity ID from KEGG/ChEBI/etc.). Apply data imputation: replace zero-intensity samples within a factor with the minimum intensity threshold (default 5000), or where only some samples in a factor are zero, use the mean of non-zero samples. Log2-transform and z-standardize the resulting matrix (zero mean, unit variance across samples). Define experimental comparisons (case vs. control group pairs). Load metabolite set definitions from a pathway database (PiMP_KEGG, Reactome COMPOUND/ChEBI, etc.) or from GNPS/MS2LDA annotation files. Apply PLAGE decomposition via singular value decomposition on the intensity matrix restricted to features in each metabolite set, producing a single activity score per set per comparison. Rank sets by p-value and activity score magnitude.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Command-line tool and Python library implementing PLAGE, ORA, and GSEA decomposition and ranking of metabolite sets with database queries and data imputation.) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface (Streamlit-based) for running PALS, visualizing pathway ranking results, and prioritizing Molecular Families and Mass2Motifs from GNPS analyses.) — https://pals.glasgowcompbio.org/app/
- **GNPS** (Source of Molecular Families metabolite groupings that can be analyzed as metabolite sets via PLAGE.) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs metabolite groupings that can be analyzed as metabolite sets via PLAGE.) — http://ms2lda.org/
- **Reactome** (Pathway database queryable by PALS for metabolite set definitions; can be accessed offline (downloaded subset) or online via Neo4j server.)

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- Output CSV contains expected columns (pathway_id, activity_score, p_value, coverage metrics) with numerical values in correct ranges (p_value ∈ [0,1], F_coverage ∈ [0,1]).
- Metabolite sets are correctly mapped: verify that tot_ds_F ≤ unq_pw_F (total dataset formulae cannot exceed unique pathway formulae) and unq_pw_F > 0.
- Activity scores show expected directionality: sets enriched in upregulated peaks in case vs. control should have positive scores; downregulated sets should be negative or lower-ranked.
- Results are robust to noise: compare rankings before and after artificial addition of zero-intensity noise to ~10% of peaks; top-ranked sets should remain stable (Spearman ρ > 0.8).
- Data preprocessing invariant: after log2 transform and standardization, intensity matrix should have mean ≈ 0 and std ≈ 1 across samples.

## Limitations

- PLAGE assumes a linear, low-dimensional decomposition of the intensity matrix; it may not capture non-linear metabolite interactions or pathway crosstalk.
- Results depend on annotation quality and metabolite set completeness; missing or incorrect peak–ID mappings reduce coverage and can bias scores.
- The method is sensitive to the choice of minimum imputation threshold (default 5000); practitioners should validate this against their instrument's detection limit and blank-sample noise distribution.
- PLAGE produces one activity score per metabolite set per comparison; it does not estimate confidence intervals or sample-level scores, limiting granularity of uncertainty quantification.
- Offline Reactome mode includes only metabolic pathways for most species; full pathway coverage requires online mode with Neo4j server access.

## Evidence

- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor. The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value; if only some of the sample values in a factor are zero then these are"
- [readme] decomposes activity levels in pathways via the PLAGE method: "decomposes activity levels in pathways via the PLAGE method"
- [readme] Molecular Families from GNPS, as well as Mass2Motifs from MS2LDA. From PALS Viewer, you can also prioritise MF and Mass2Motifs from your GNPS analysis based on their activity levels.: "Molecular Families from GNPS, as well as Mass2Motifs from MS2LDA. From PALS Viewer, you can also prioritise MF and Mass2Motifs from your GNPS analysis based on their activity levels."
