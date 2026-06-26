---
name: pathway-database-integration
description: Use when you have intensity measurements (peak features, protein intensities,
  or gene expression values) with compound or gene annotations (KEGG IDs, ChEBI IDs,
  UniProt IDs, or ENSEMBL IDs), and you need to aggregate them into biologically meaningful
  pathway groups for differential analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - PALS (Pathway Activity Level Scoring)
  - Reactome
  - KEGG
  - ChEBI
  - PALS Viewer
  license_tier: restricted
  provenance_tier: literature
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

# pathway-database-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate metabolomics or proteomics peak/feature data with public pathway databases (KEGG, Reactome, ChEBI) to enable pathway-level statistical analysis. This skill is essential when you need to map measured compounds or genes to biological pathways before applying decomposition or enrichment methods.

## When to use

You have intensity measurements (peak features, protein intensities, or gene expression values) with compound or gene annotations (KEGG IDs, ChEBI IDs, UniProt IDs, or ENSEMBL IDs), and you need to aggregate them into biologically meaningful pathway groups for differential analysis. Use this skill when your goal is to move beyond individual metabolite/gene ranking to pathway-level inference.

## When NOT to use

- Your annotations are already aggregated into pathway-level activity scores; you would be re-mapping already-summarized data.
- You have no compound or gene annotations for your peaks/features; pathway mapping requires identifications.
- Your species or pathway database is not represented in the PALS offline mode and you cannot connect to a Reactome Neo4j server.

## Inputs

- intensity CSV matrix (rows=peak/feature IDs, columns=sample measurements; optional second row for group assignments)
- annotation CSV (two columns: peak/feature ID, metabolite/gene database ID from KEGG/ChEBI/UniProt/ENSEMBL)
- experimental design dictionary specifying groups and comparisons (case vs. control pairs)
- pathway database choice (PiMP_KEGG, COMPOUND, ChEBI, UniProt, ENSEMBL)

## Outputs

- DataSource object with preprocessed and normalized intensity matrix linked to pathway annotations
- Pathway-to-compound/gene membership mappings from selected database
- Log2-transformed, standardized intensity matrix (zero mean, unit variance across samples)
- imputation-flagged intensity matrix (zeros replaced according to experimental design)

## How to apply

Prepare two input files: an intensity CSV matrix (rows=peak features with peak IDs, columns=individual samples; optionally include a second row for group labels) and an annotation CSV with two columns (peak/feature ID and KEGG/ChEBI/UniProt/ENSEMBL database ID). Select a pathway database matching your data type (PiMP_KEGG or ChEBI for metabolomics; UniProt or ENSEMBL for proteomics/transcriptomics). Initialize a DataSource object with your intensity and annotation dataframes, specify the database name, species (defaults to Homo sapiens), and whether to query metabolic pathways only or all pathways. The DataSource will perform data imputation (replacing all-zero values in a factor with the minimum intensity, partial zeros with the factor mean), log2-transform, and standardize the intensity matrix to zero mean and unit variance. This preprocessing enables downstream pathway decomposition methods like PLAGE to operate on normalized, comparable pathway activity profiles.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Primary pathway analysis framework that wraps database integration into a complete decomposition and ranking workflow via PLAGE/ORA/GSEA) — https://github.com/glasgowcompbio/PALS
- **Reactome** (Primary pathway database providing compound, protein, and gene pathway memberships; queried in online mode via Neo4j server or offline via downloaded metabolic pathway files)
- **KEGG** (Metabolite and gene pathway database; integrated via PiMP_KEGG export or compound/gene ID matching)
- **ChEBI** (Chemical entities of biological interest database for metabolite identification and pathway mapping)
- **PALS Viewer** (Web interface (Streamlit-based) for interactive pathway database selection, analysis execution, and result inspection) — https://pals.glasgowcompbio.org/app/

## Examples

```
from pals.common import *; from pals.feature_extraction import DataSource; ds = DataSource(int_df, annotation_df, experimental_design, database_name='COMPOUND', reactome_species='Homo sapiens', reactome_metabolic_pathway_only=True, reactome_query=False, min_replace=5000)
```

## Evaluation signals

- Intensity matrix after preprocessing has zero mean and unit variance (standardization check); verify by computing mean ≈ 0 and std ≈ 1 across all samples.
- No missing values remain in the intensity matrix after imputation; zero counts replaced according to experimental design rules (all-zero factor → min_replace; partial-zero factor → factor mean).
- All annotated peaks map to at least one compound/gene in the selected pathway database; audit coverage by comparing unique peak IDs in input vs. mapped peak IDs in output.
- Pathway membership is non-empty for all pathways returned; verify no pathway groups contain zero compounds/genes after filtering unmapped annotations.
- Experimental design groups match column headers in the intensity CSV; spot-check that case/control assignments are correctly parsed and applied to intensity subsets.

## Limitations

- Offline Reactome mode provides only metabolic pathways for a fixed set of common species; access to all Reactome pathways or rare species requires online mode with a local Neo4j server.
- Multiple peaks can map to multiple compounds and vice versa, creating ambiguity in annotation; the skill does not resolve these 1-to-many or many-to-1 relationships automatically—users must handle or accept them.
- Data imputation assumes that missing values are missing-completely-at-random within experimental factors; if dropout is systematic (e.g., correlated with sample quality), imputation may introduce bias.
- Log2 transformation and standardization assume intensity distributions are approximately normal after log2 transform; highly skewed or zero-inflated data may require alternative preprocessing.
- Pathway database content and version are fixed at download time (offline mode); users must manually re-download to incorporate new pathways or corrections.

## Evidence

- [readme] performs database queries of pathways, decomposes activity levels in pathways via the PLAGE method, as well as presents the results in a user-friendly manner: "performs database queries of pathways, decomposes activity levels in pathways via the PLAGE method"
- [readme] The first is a matrix is of individual peak intensities (rows are peak features with column one containing the peak id, further columns representing individual samples): "matrix is of individual peak intensities (rows are peak features with column one containing the peak id, further columns representing individual samples)"
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value: "Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value"
- [readme] The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance"
- [readme] As a result of the uncertainty in peak identification, multiple peak IDs may be mapped to multiple compound IDs and vice versa.: "multiple peak IDs may be mapped to multiple compound IDs and vice versa"
- [readme] PiMP_KEGG, COMPOUND and ChEBI are for metabolomics use, while UniProt and ENSEMBL are for proteomics and transcriptomics use respectively.: "PiMP_KEGG, COMPOUND and ChEBI are for metabolomics use, while UniProt and ENSEMBL are for proteomics and transcriptomics use respectively"
- [readme] If true, we limit to metabolic pathways only. Otherwise all pathways will be queried.: "If true, we limit to metabolic pathways only. Otherwise all pathways will be queried."
