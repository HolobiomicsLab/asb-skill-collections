---
name: custom-metabolite-set-integration
description: Use when you have a user-supplied metabolite set file (CSV or JSON) defining custom groupings of metabolites (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - PALS Viewer
  - PALS (Pathway Activity Level Scoring)
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
- PALS Viewer
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
---

# custom-metabolite-set-integration

## Summary

Extend PALS pathway activity scoring to user-defined metabolite set collections (beyond built-in pathways, Molecular Families, and Mass2Motifs) by validating user-uploaded sets and dispatching them through the PLAGE decomposition pipeline. This enables scoring and prioritization of custom metabolite groupings based on activity levels in comparative metabolomics experiments.

## When to use

You have a user-supplied metabolite set file (CSV or JSON) defining custom groupings of metabolites (e.g., by structural family, spectral similarity, or domain knowledge) and wish to score their activity levels across experimental conditions using the same robust decomposition framework that PALS applies to canonical pathway databases. This is indicated when standard pathway databases are insufficient or when metabolites are grouped by non-canonical criteria (e.g., user-defined spectral clusters or chemical similarity groups).

## When NOT to use

- Your metabolite groupings are already curated and available in standard pathway databases (KEGG, Reactome, GNPS Molecular Families, MS2LDA Mass2Motifs); use the built-in set types instead.
- You lack validated metabolite identifiers (KEGG or ChEBI IDs) for the majority of your dataset; the validation step will fail and most features will be excluded.
- Your goal is gene-level or protein-level pathway analysis rather than metabolite-level analysis; PALS is designed for metabolomics and requires metabolite identifiers.

## Inputs

- user-uploaded metabolite set file (CSV or JSON format) with metabolite identifiers and set membership
- validated metabolite identifiers matching PALS database schema (KEGG compound IDs, ChEBI IDs, or equivalent)
- intensity matrix (peak intensities across samples, log2-transformed and standardized)
- annotation matrix (peak ID to metabolite ID mappings)

## Outputs

- scored results table containing metabolite set names, activity level scores, and statistical confidence metrics (p-values)
- tabular output compatible with PALS Viewer display
- metabolite set coverage metrics (proportion of dataset features matching set membership)

## How to apply

Parse the user-uploaded metabolite set file to extract metabolite identifiers and set membership information, validating that identifiers match the PALS database schema (KEGG IDs, ChEBI IDs, or other supported compound identifiers). Route the validated metabolite set through the existing PLAGE decomposition pipeline, which performs singular value decomposition on the intensity matrix stratified by metabolite membership to compute set activity scores analogous to pathway activity levels. The method is robust because PLAGE decomposes activity at the set level rather than performing over-representation analysis (ORA) or gene set enrichment analysis (GSEA), making it less sensitive to noise and missing peaks prevalent in metabolomics data. Generate a scored results table containing metabolite set names, activity level scores for each experimental comparison, and statistical confidence metrics (p-values, coverage). Format output in a user-friendly tabular format compatible with PALS Viewer display for interactive inspection and sorting by significance.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Performs PLAGE decomposition of user-supplied metabolite sets to compute activity scores; routes validated sets through the existing pipeline) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Interactive Web interface for uploading metabolite set files, triggering decomposition analysis, and visualizing and sorting scored results) — https://pals.glasgowcompbio.org/app/

## Examples

```
from pals.PLAGE import PLAGE
from pals.common import *
from pals.feature_extraction import DataSource
import pandas as pd

# Load user-supplied custom metabolite set and intensity/annotation data
user_sets = pd.read_csv('custom_metabolite_sets.csv')
int_df = pd.read_csv('intensity_matrix.csv', index_col=0)
annot_df = pd.read_csv('annotation_matrix.csv')

# Validate and integrate custom sets into DataSource
ds = DataSource(int_df, annot_df, experimental_design, database_name='COMPOUND',
                custom_sets=user_sets, reactome_species='Homo sapiens')

# Score custom sets using PLAGE decomposition
method = PLAGE(ds)
results_df = method.get_pathway_df()
results_df.to_csv('custom_set_scores.csv')
```

## Evaluation signals

- User-uploaded metabolite set file successfully parses without schema errors; all metabolite identifiers are recognized by the PALS database and pass validation.
- Scored results table is non-empty and contains expected metabolite set names with corresponding activity scores and p-values; at least one set has coverage > 0 (i.e., ≥ 1 metabolite from the set is present in the analyzed dataset).
- Activity scores and p-values fall within expected ranges (scores are continuous; p-values are between 0 and 1); results can be sorted by p-value in PALS Viewer without errors.
- Results are consistent with PLAGE method behavior: sets with more member metabolites detected in the dataset and showing coordinated intensity changes across conditions receive lower p-values and higher activity scores.
- Output table is compatible with PALS Viewer tabular display; user can interactively filter and inspect results without rendering errors.

## Limitations

- Custom metabolite sets must use metabolite identifiers that align with PALS database schema (KEGG, ChEBI, or equivalent); sets with unrecognized identifiers will fail validation and be excluded.
- The method is most robust when metabolite sets contain sufficient members detected in the dataset (low coverage results in weak statistical power); sets with < 2–3 detected members may yield unstable scores.
- PLAGE decomposition assumes coordinated activity across metabolites in a set; heterogeneous sets with metabolites behaving independently may not be well-captured by a single activity score.
- Results are sensitive to data imputation choices (minimum intensity value for zero replacement) and preprocessing (log2 transformation, standardization); these parameters should be set consistently with the main PALS analysis.
- The robustness advantage of PLAGE over ORA and GSEA applies primarily to noisy metabolomics peak data; custom sets with very sparse or poorly-annotated features may still suffer from missing data.

## Evidence

- [other] Can the PLAGE decomposition method in PALS be extended to score user-uploaded custom metabolite sets beyond the three currently supported set types (pathways, Molecular Families, and Mass2Motifs)?: "Can the PLAGE decomposition method in PALS be extended to score user-uploaded custom metabolite sets beyond the three currently supported set types"
- [other] PALS's decomposition approach is amenable to analysis of any group of metabolite sets, not just pathways, suggesting extensibility beyond currently shipped set types.: "PALS's decomposition approach is amenable to analysis of any group of metabolite sets, not just pathways, suggesting extensibility"
- [other] Parse user-uploaded metabolite set file (CSV or JSON format) to extract metabolite identifiers and set membership.: "Parse user-uploaded metabolite set file (CSV or JSON format) to extract metabolite identifiers and set membership"
- [other] Validate metabolite set structure and identifiers against the PALS database schema.: "Validate metabolite set structure and identifiers against the PALS database schema"
- [other] Dispatch validated metabolite set through the existing PLAGE decomposition pipeline to compute pathway activity scores.: "Dispatch validated metabolite set through the existing PLAGE decomposition pipeline to compute pathway activity scores"
- [intro] the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent"
- [readme] For more details including how to analyse user-defined metabolite sets from Jupyter notebooks, see Section 8.: "how to analyse user-defined metabolite sets from Jupyter notebooks"
