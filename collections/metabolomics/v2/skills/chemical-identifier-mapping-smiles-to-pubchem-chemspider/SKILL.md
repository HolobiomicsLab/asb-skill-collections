---
name: chemical-identifier-mapping-smiles-to-pubchem-chemspider
description: Use when you have a chemical structure in SMILES format and need to find
  matching compound records and standardized identifiers (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3070
  tools:
  - PubChem
  - ChemSpider
  - ChEBI
  - NP Atlas
  - PHP
  - Symfony
  - Norine
  - COCONUT
  - SmilesDrawer
  - React
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-021-00530-2
  title: MassSpecBlocks
evidence_spans:
- find structures on other chemical projects like Pubchem
- find structures on other chemical projects like ChemSpider
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

# Chemical identifier mapping: SMILES to PubChem, ChemSpider

## Summary

Maps chemical structures represented as SMILES strings to standardized compound identifiers across multiple external chemical repositories (PubChem, ChemSpider, Norine, ChEBI, COCONUT, NP Atlas) via conditional per-repository dispatch logic. This enables unified cross-database chemical lookup and consolidation of structure metadata from diverse sources.

## When to use

Use this skill when you have a chemical structure in SMILES format and need to find matching compound records and standardized identifiers (e.g., CID, CSID) across multiple chemical databases—particularly when working with natural products, NRPs, or specialized compound classes where different repositories have different coverage or when you need to cross-validate structure identity and retrieve consolidated metadata.

## When NOT to use

- Input is a molecular formula or common chemical name rather than a structure; use nomenclature or formula lookup instead
- You need only local or proprietary database lookups; this skill is specific to cross-referencing external public repositories
- SMILES string is already known to be invalid or malformed; validate structure format before dispatch

## Inputs

- SMILES string (validated chemical structure representation)
- Repository selection flags or scope constraints (optional)

## Outputs

- Unified consolidated match table with per-repository results
- Compound identifiers (PubChem CID, ChemSpider CSID, Norine ID, ChEBI ID, etc.)
- Per-repository match status and metadata (names, synonyms, molecular properties)

## How to apply

Parse and validate the input SMILES string format. Apply conditional routing logic to determine which external repositories are applicable based on structure properties or repository scope (e.g., Norine focuses on nonribosomal peptides). Dispatch parallel or sequential structure lookup queries to the applicable repository APIs (PubChem, ChemSpider, Norine, ChEBI, COCONUT, NP Atlas) using their respective chemical structure search endpoints, typically via exact or similarity match modes. Normalize and extract per-repository match records, collecting compound identifiers, systematic names, and metadata fields. Consolidate results into a unified output table with per-repository match status, identifiers, and hit details, enabling downstream cross-referencing and chemical validation.

## Related tools

- **PubChem** (External repository for chemical structure lookups and compound identifier resolution) — https://pubchem.ncbi.nlm.nih.gov
- **ChemSpider** (External repository for chemical structure queries and cross-database compound matching) — http://www.chemspider.com
- **Norine** (Specialized repository for nonribosomal peptide structures and lookups) — https://bioinfo.lifl.fr/norine/
- **ChEBI** (External chemical database for chemical entity lookups and metabolite identification) — https://www.ebi.ac.uk/chebi/
- **COCONUT** (Natural products chemical database for structure queries and compound matching) — https://coconut.naturalproducts.net
- **NP Atlas** (Natural products structure database for compound lookups and identifier mapping) — https://www.npatlas.org
- **SmilesDrawer** (SMILES string parsing and chemical structure validation prior to repository dispatch) — https://github.com/privrja/smilesDrawer
- **Symfony** (PHP backend framework implementing conditional routing logic and API dispatch orchestration) — https://github.com/privrja/thesis
- **React** (Frontend framework presenting consolidated cross-repository results to user) — https://github.com/privrja/thesis-frontend-react

## Evaluation signals

- All dispatched repository queries return normalized response payloads with valid compound identifiers and match status (hit/miss/error)
- Consolidated output table contains non-null entries for each repository that returned results, with per-repository metadata present and consistent
- Cross-repository duplicate detection: if the same compound (e.g., same InChI or canonical SMILES) is matched in multiple repositories, identifiers are correctly linked in the consolidated table
- SMILES input validation passes (correct chemical syntax, parseable by SmilesDrawer); malformed SMILES result in explicit parse error, not silent failure
- Repository-specific ID formats are preserved (e.g., numeric CID for PubChem, alphanumeric CSID for ChemSpider) and are consistent with each repository's documented identifier scheme

## Limitations

- Conditional routing logic success depends on accurate classification of structure properties and repository scope; misclassified structures may not be queried against applicable repositories
- External repository API availability and rate limits are not managed by the skill itself; timeouts or quota exhaustion may produce incomplete consolidated results
- Normalization of per-repository metadata is lossy; repository-specific fields not included in the unified schema are discarded
- SMILES representation ambiguities (e.g., chiral centers, double-bond stereochemistry) may result in non-matching lookups even for chemically identical compounds across different stereoisomer encodings

## Evidence

- [other] how does MassSpecBlocks route chemical structure queries to multiple external repositories: "How does MassSpecBlocks route chemical structure queries to multiple external repositories (PubChem, ChemSpider, Norine, ChEBI, COCONUT, NP Atlas) with conditional per-repository dispatch logic?"
- [other] cross-database lookup and consolidation: "MassSpecBlocks enables users to find chemical structures across multiple external repositories including PubChem, ChemSpider, Norine, ChEBI, COCONUT, and NP Atlas through integrated lookups."
- [other] workflow: parse SMILES, apply routing logic, dispatch queries, normalize results, consolidate: "1. Parse input SMILES string and validate structure format. 2. Apply conditional routing logic to determine which repositories are applicable for query (based on structure properties or repository"
- [readme] open-source web application to manage and find structures: "MassSpecBlocks: Database of Sequences and Building Blocks of Microbial Metabolites for Mass Spectra Analysis is an open-source web application to manage own user databases of chemical structures like"
- [readme] SmilesDrawer for SMILES parsing: "The application uses many other libraries like SmilesDrawer from Daniel Probst to draw chemical structures from SMILES format"
