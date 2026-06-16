---
name: activity-score-computation-and-reporting
description: Use when you have preprocessed metabolite intensity data (log2-transformed, zero-mean unit-variance standardized) mapped to compound annotations, and you need to derive activity scores for a set of metabolite groups (pathways, Molecular Families, Mass2Motifs, or custom metabolite sets) to rank them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - PALS Viewer
  - PALS (Pathway Activity Level Scoring)
  - GNPS
  - MS2LDA
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
- PALS Viewer
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

# Activity-Score Computation and Reporting

## Summary

Compute pathway or metabolite set activity levels from intensity data using singular value decomposition (PLAGE method), then format and return scored results with statistical confidence metrics. This skill transforms raw metabolite intensities into ranked pathway activity tables suitable for downstream interpretation and visualization.

## When to use

Apply this skill when you have preprocessed metabolite intensity data (log2-transformed, zero-mean unit-variance standardized) mapped to compound annotations, and you need to derive activity scores for a set of metabolite groups (pathways, Molecular Families, Mass2Motifs, or custom metabolite sets) to rank them by significance and identify the most dysregulated biochemical processes.

## When NOT to use

- Input intensity data has not been log2-transformed and standardized to zero mean and unit variance—preprocessing must occur first.
- Metabolite set collection is empty or contains no metabolites present in the annotation dataframe—validation will fail or yield no results.
- Experimental design dictionary is missing or malformed (missing 'groups' or 'comparisons' keys)—the decomposition pipeline requires explicit case–control specifications.

## Inputs

- intensity dataframe (rows=peak features with IDs, columns=samples; preprocessed to log2 scale, zero-mean unit-variance standardized)
- annotation dataframe (two columns: peak_id and entity_id as KEGG/ChEBI/UniProt identifiers)
- metabolite set collection file (CSV or JSON: set names, metabolite identifiers, set membership)
- experimental design dictionary (groups mapping samples to group labels; comparisons listing case/control pairs)

## Outputs

- pathway/metabolite set ranking dataframe (columns: set_id, set_name, activity_score, p_value, fold_change, unq_pw_F, tot_ds_F, F_coverage)
- scored results table (user-friendly tabular format compatible with PALS Viewer)

## How to apply

Parse and validate the user-supplied metabolite set structure (CSV or JSON format containing metabolite identifiers and set membership) against the PALS database schema. Dispatch the validated metabolite sets through the existing PLAGE decomposition pipeline, which applies singular value decomposition to the intensity submatrix of each metabolite group to compute a single activity score per set per experimental comparison. Compute statistical confidence metrics (p-values, fold-changes) for each scored metabolite set by comparing case vs. control groups as specified in the experimental design dictionary. Format the results into a scored table with columns for metabolite set name, activity level score, p-value, and coverage (proportion of pathway metabolites detected in the dataset), then return in tabular format compatible with PALS Viewer display or export as CSV.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Core decomposition engine; implements PLAGE method via singular value decomposition to compute metabolite set activity scores from intensity data.) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface (Streamlit-based) for executing activity score computation, visualizing ranked pathway/metabolite set results, and inspecting significantly changing sets.) — https://pals.glasgowcompbio.org/app/
- **GNPS** (Source of Molecular Families metabolite groupings; PALS can score user-downloaded Molecular Families collections.) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of Mass2Motifs metabolite groupings; PALS can score user-downloaded Mass2Motifs collections.) — http://ms2lda.org/

## Examples

```
from pals.PLAGE import PLAGE; from pals.feature_extraction import DataSource; ds = DataSource(int_df, annotation_df, experimental_design, database_name='COMPOUND', min_replace=5000); method = PLAGE(ds); df = method.get_pathway_df(); df.to_csv('activity_scores.csv', index=False)
```

## Evaluation signals

- Output dataframe columns match expected schema: set_id, set_name, activity_score, p_value, fold_change, unq_pw_F, tot_ds_F, F_coverage are all present and non-null for each metabolite set.
- Activity scores are numeric (float) and represent meaningful decomposition output (e.g., principal component or latent score); p-values fall within [0, 1] and are computed from case–control comparisons.
- F_coverage (proportion of detected metabolites in each set) is between 0 and 1; metabolite sets with zero coverage should be either excluded or flagged.
- Results can be sorted by p-value or activity score; top-ranked metabolite sets correspond qualitatively to expected biology (e.g., known dysregulated pathways in the study design).
- Output is compatible with PALS Viewer display (tabular format, column names recognized, no missing or malformed values in rows that passed validation).

## Limitations

- PLAGE decomposition assumes linear relationships within metabolite sets; highly non-linear or context-dependent metabolite associations may not be captured.
- Results are robust to noise and missing peaks compared to ORA and GSEA, but performance degrades when metabolite set membership is sparse (few detected metabolites per set).
- Custom metabolite sets must be supplied in validated CSV or JSON format with metabolite identifiers matching the PALS database schema (KEGG, ChEBI, UniProt, or ENSEMBL); mismatches will result in zero coverage or failure.
- Statistical confidence depends on the number and replicate structure of experimental samples; designs with very few replicates per group may yield unreliable p-values.
- Data imputation (zero-replacement with minimum or group mean) occurs before standardization; extreme or missing-not-at-random data patterns may bias activity scores.

## Evidence

- [other] Parse user-uploaded metabolite set file (CSV or JSON format) to extract metabolite identifiers and set membership: "Parse user-uploaded metabolite set file (CSV or JSON format) to extract metabolite identifiers and set membership."
- [intro] PLAGE decomposition pipeline to compute pathway activity scores: "decomposes activity levels in pathways via the PLAGE method"
- [other] Generate scored results table with statistical confidence metrics: "Generate scored results table containing metabolite set names, activity level scores, and statistical confidence metrics."
- [intro] Extensibility beyond currently shipped set types: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] More robust to noise and missing peaks: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [other] User-friendly tabular output compatible with PALS Viewer: "Format and return results in a user-friendly tabular output compatible with PALS Viewer display."
- [readme] Data preprocessing standardization: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples."
- [readme] Output columns include coverage and formula hits: "The column `unq_pw_F` lists the unique formulae found in that pathway, `tot_ds_F` lists the formula hits found in the dataset, and `F_coverage` is the proportion of `tot_ds_F` to `unq_pw_F`."
