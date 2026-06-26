---
name: biomolecule-metadata-handling
description: 'Use when initiating a proteomics or panomics analysis with peptide-
  or protein-level expression data. The trigger is the simultaneous availability of:
  (1) a quantification matrix (rows = biomolecules, columns = samples), (2) sample
  metadata (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pmartR
  - R
  - PMart ShinyApp (Shiny GUI)
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- the bulk of the functionality of the package to be available to the user without
  the need for familiarity with R or the package itself
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pmart_cq
    doi: 10.1021/acs.jproteome.3c00512
    title: PMart
  dedup_kept_from: coll_pmart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.3c00512
  all_source_dois:
  - 10.1021/acs.jproteome.3c00512
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biomolecule-metadata-handling

## Summary

Upload, structure, and track biomolecule-level metadata (e.g., protein IDs, peptide sequences, gene annotations) alongside expression quantification matrices to enable filtering, aggregation, and annotation downstream in omics analysis workflows. This skill ensures that biomolecule identity and properties are preserved and queryable throughout normalization, statistical testing, and biomarker discovery.

## When to use

Use this skill when initiating a proteomics or panomics analysis with peptide- or protein-level expression data. The trigger is the simultaneous availability of: (1) a quantification matrix (rows = biomolecules, columns = samples), (2) sample metadata (e.g., condition, replicate, batch), and (3) biomolecule metadata (e.g., accession numbers, sequence information, UniProt identifiers). This skill is essential before any filtering, normalization, or roll-up operation that depends on biomolecule properties or identity.

## When NOT to use

- When biomolecule identifiers in the expression matrix do not uniquely map to the biomolecule metadata table (ambiguous or missing accessions); resolve this first.
- When sample identifiers in the expression matrix do not match the sample metadata table; reconcile sample naming before upload.
- When working with already-aggregated, protein-level-only quantification that does not require further roll-up; metadata handling is still useful but the motivation is weaker.

## Inputs

- Expression quantification matrix (numeric: rows = biomolecules (peptides or proteins), columns = samples)
- Sample metadata table (rows = samples, columns = condition, replicate, batch, covariates)
- Biomolecule metadata table (rows = biomolecules, columns = accession, sequence, gene annotation, or other properties)

## Outputs

- Structured omics object with expression matrix, sample metadata, and biomolecule metadata linked and indexed
- Validated metadata schema with rowname and columnname consistency checks enforced
- Metadata-annotated expression matrix available for downstream filtering, normalization, and aggregation operations

## How to apply

In the pmartR Shiny GUI, upload three coordinated tables during the data initialization step: (1) the expression data matrix in row-biomolecule, column-sample format; (2) sample information with metadata columns defining experimental groups, covariates, and pairing structure; and (3) biomolecule metadata table with biomolecule identifiers as rownames and columns for properties such as accession numbers, sequence length, or functional annotations. Ensure all rownames in the expression matrix match the biomolecule identifier column in the biomolecule metadata table, and all column names in the expression matrix match the sample identifier column in the sample metadata table. The metadata is then attached to the omics object and persists through subsequent normalization, filtering, and protein quantification steps, enabling queries like 'filter to biomolecules with ≥2 peptides per protein' or 'roll up peptide abundances to protein level using specified aggregation rules'.

## Related tools

- **pmartR** (R package that provides the data model and validation functions for attaching and indexing biomolecule metadata alongside expression matrices)
- **PMart ShinyApp (Shiny GUI)** (Interactive web interface for uploading coordinated expression, sample, and biomolecule metadata tables and initializing an omics object) — https://github.com/pmartR/PMart_ShinyApp

## Evaluation signals

- Rownames of the expression matrix exactly match the biomolecule identifier column in the biomolecule metadata table; no missing or mismatched accessions.
- Column names of the expression matrix exactly match the sample identifier column in the sample metadata table; no orphaned samples.
- The omics object retains both metadata tables and makes them queryable via accessor functions (e.g., in pmartR: fdata(), edata(), pdata()).
- Downstream filtering operations (e.g., 'filter by coefficient of variation' or 'filter by non-missing value threshold') execute without error, indicating metadata is properly indexed.
- Protein quantification (peptide roll-up) succeeds and produces output with correct biomolecule groupings (e.g., peptides grouped by protein accession), confirming metadata was used to drive aggregation.

## Limitations

- The skill assumes biomolecule identifiers (accessions, gene names, peptide sequences) are stable and unique within the metadata table; duplicate or ambiguous identifiers will cause attachment or filtering errors.
- Metadata upload does not perform automated annotation (e.g., adding Gene Ontology terms or pathway assignments); enrichment requires post-hoc queries to external databases.
- The pmartR GUI currently supports a fixed set of metadata column names and types; custom properties may require manual schema extension or scripting in R.
- Large biomolecule metadata tables (e.g., >100,000 rows) may cause UI responsiveness delays in the Shiny app; batch queries or API access recommended for very large panomics studies.

## Evidence

- [readme] Data upload. Upload expression data, sample information, and biomolecule metadata.: "Data upload. Upload expression data, sample information, and biomolecule metadata."
- [intro] Biomolecule metadata is used to enable filtering and aggregation operations.: "Filter biomolecules based on various criteria including minimum non-missing values and coefficient of variation thresholds. Various methods for rolling up peptide data up to the protein level."
- [readme] The Shiny GUI exposes pmartR's bulk functionality without requiring R expertise.: "The aim is for the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself."
