---
name: structure-similarity-search-across-repositories
description: Use when you have a SMILES string or chemical structure and need to determine
  whether it exists in public chemical repositories, or locate reference identifiers
  and metadata for the same compound across multiple authoritative sources.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0348
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - ChEBI
  - NP Atlas
  - PHP
  - Symfony
  - PubChem
  - ChemSpider
  - Norine
  - COCONUT
  - SmilesDrawer
  - React + TypeScript
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-021-00530-2
  title: MassSpecBlocks
evidence_spans:
- find structures on other chemical projects like ChEBI
- find structures on other chemical projects like NP Atlas
- Backend is written in PHP with Symfony framework
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massspecblocks_cq
    doi: 10.1186/s13321-021-00530-2
    title: MassSpecBlocks
  dedup_kept_from: coll_massspecblocks_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00530-2
  all_source_dois:
  - 10.1186/s13321-021-00530-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# structure-similarity-search-across-repositories

## Summary

A federated chemical structure lookup skill that routes SMILES-encoded molecular queries to multiple heterogeneous external repositories (PubChem, ChemSpider, Norine, ChEBI, COCONUT, NP Atlas) with conditional per-repository dispatch logic, consolidating matches into a unified results table. Use this to discover where a chemical structure of interest exists across public databases and retrieve standardized metadata (compound IDs, names, repository-specific annotations).

## When to use

You have a SMILES string or chemical structure and need to determine whether it exists in public chemical repositories, or locate reference identifiers and metadata for the same compound across multiple authoritative sources. Particularly valuable when working with natural products, non-ribosomal peptides (NRPs), or any compounds where cross-repository validation or multi-source annotation enrichment is required.

## When NOT to use

- Input is already a list of known compound identifiers or database IDs — use direct lookup or batch retrieval instead of federated search.
- You only need to query a single repository — use the repository's native search API directly.
- The molecular structure is invalid, malformed, or cannot be parsed into SMILES — validate structure format before invoking this skill.

## Inputs

- SMILES string (validated chemical structure notation)
- repository filter settings (which repositories to query)
- search mode parameter (exact match, substructure, similarity)

## Outputs

- consolidated results table with per-repository match status
- compound identifiers (PubChem CID, ChemSpider ID, Norine ID, ChEBI ID, COCONUT ID, NP Atlas ID)
- standardized compound names and synonyms per repository
- repository-specific metadata and links
- match confidence or ranking score per repository

## How to apply

Parse and validate the input SMILES string to ensure correct chemical structure encoding. Apply conditional routing logic to determine which repositories are applicable based on structure properties (e.g., natural product scope for Norine, chemical space coverage for PubChem) or explicit user filter settings. Dispatch queries in parallel or sequential mode to each applicable repository's lookup API endpoint (structure search, substructure search, or exact match modes depending on repository capability). Collect and normalize match records from each repository response, extracting compound identifiers, preferred names, InChI/InChIKey, and repository-specific metadata. Consolidate all results into a unified output table with per-repository match status (found/not found), ranked by relevance or alphabetically, enabling side-by-side comparison of how the same structure is catalogued across sources.

## Related tools

- **PubChem** (external chemical structure repository providing exact and substructure search via REST API) — https://pubchem.ncbi.nlm.nih.gov
- **ChemSpider** (external chemical structure repository with structure search capabilities) — http://www.chemspider.com
- **Norine** (specialized database for non-ribosomal peptide structures) — https://bioinfo.lifl.fr/norine/
- **ChEBI** (Chemical Entities of Biological Interest repository for small-molecule chemical entities) — https://www.ebi.ac.uk/chebi/
- **COCONUT** (Collection of Open Natural Products database for natural compounds) — https://coconut.naturalproducts.net
- **NP Atlas** (Natural Products Atlas for microbial secondary metabolites) — https://www.npatlas.org
- **SmilesDrawer** (SMILES visualization and validation tool to render chemical structures from SMILES notation for user confirmation before search dispatch) — https://github.com/privrja/smilesDrawer
- **Symfony** (PHP backend framework orchestrating conditional routing logic, API dispatch, and result normalization) — https://github.com/privrja/thesis
- **React + TypeScript** (frontend framework handling SMILES input, repository selection, and consolidated results visualization) — https://github.com/privrja/thesis-frontend-react

## Evaluation signals

- All queried repositories return a response (either match found or explicit no-match); no API timeouts or unhandled exceptions.
- Compound identifiers from each repository are normalized and resolvable (e.g., PubChem CID is a numeric integer, ChemSpider ID is numeric, Norine ID is alphanumeric).
- Results table is non-empty for at least one repository when querying a known, widely distributed compound (e.g., caffeine SMILES); empty results should only occur for invalid or extremely novel structures.
- Per-repository match status is accurately recorded (e.g., 'found' vs 'not found' does not contradict the presence/absence of identifiers in the consolidated output).
- Metadata fields from different repositories do not contain corrupted or truncated values; compound names and links are human-readable and clickable.

## Limitations

- Repository API availability and rate limits vary; parallel dispatch may exceed quota thresholds, requiring sequential fallback or request throttling.
- Structure representation differences: the same chemical entity may be encoded with different SMILES strings across repositories due to canonicalization or tautomerization rules, potentially causing false negatives in exact-match search modes.
- Repository scope and coverage differ significantly (e.g., Norine is specialized for NRPs and will not contain most synthetic chemicals; PubChem is very broad); absence of a match does not imply the compound does not exist, only that it is not catalogued in that particular source.
- No changelog found for MassSpecBlocks, limiting traceability of API integration changes or repository endpoint updates that may silently break dispatch logic.

## Evidence

- [intro] MassSpecBlocks enables users to find chemical structures across multiple external repositories including PubChem, ChemSpider, Norine, ChEBI, COCONUT, and NP Atlas through integrated lookups.: "find structures on other chemical projects like Pubchem, ChemSpider, Norine, ChEBI, COCONUT, and NP Atlas"
- [methods] Parse input SMILES string and validate structure format. Apply conditional routing logic to determine which repositories are applicable for query (based on structure properties or repository scope). Dispatch parallel or sequential queries to PubChem, ChemSpider, Norine, ChEBI, COCONUT, and NP Atlas APIs using their respective lookup endpoints. Collect and normalize match records from each repository response, extracting compound identifiers, names, and metadata. Consolidate results into a unified output table with per-repository match status and details.: "Parse input SMILES string and validate structure format. 2. Apply conditional routing logic to determine which repositories are applicable for query (based on structure properties or repository"
- [intro] How does MassSpecBlocks route chemical structure queries to multiple external repositories with conditional per-repository dispatch logic?: "How does MassSpecBlocks route chemical structure queries to multiple external repositories (PubChem, ChemSpider, Norine, ChEBI, COCONUT, NP Atlas) with conditional per-repository dispatch logic?"
- [readme] The application uses many other libraries like SmilesDrawer to draw chemical structures from SMILES format or similar.: "The application uses many other libraries like SmilesDrawer from Daniel Probst to draw chemical structures from SMILES format"
- [readme] Backend is written in PHP with Symfony framework; Application is developed for Mysql 8 /MariaDB 10.: "Backend is written in PHP with Symfony framework, backend repo. Application is developed for Mysql 8 /MariaDB 10"
