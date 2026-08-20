---
name: api-query-routing-conditional-per-database
description: Use when when you have a chemical structure query (as a SMILES string
  or molecular identifier) and need to search across multiple external chemical repositories
  simultaneously, but only some repositories are relevant for your specific compound
  class (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
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
  - React/TypeScript
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

# api-query-routing-conditional-per-database

## Summary

Route chemical structure queries to multiple external repositories (PubChem, ChemSpider, Norine, ChEBI, COCONUT, NP Atlas) using conditional logic that determines which repositories are applicable based on query properties. This skill enables parallel or sequential dispatch of SMILES-formatted queries and consolidates normalized results across heterogeneous external APIs.

## When to use

When you have a chemical structure query (as a SMILES string or molecular identifier) and need to search across multiple external chemical repositories simultaneously, but only some repositories are relevant for your specific compound class (e.g., natural products, synthetic drugs, peptides). Use this skill when you want unified results that preserve per-repository match status and metadata rather than searching each repository independently.

## When NOT to use

- Input is not a valid SMILES string or molecular structure representation; pre-validate chemical format before routing.
- You only need to search a single repository; conditional multi-repository dispatch adds latency and complexity unnecessarily.
- Results must be merged into a single canonical record; this skill preserves per-repository distinctions, which may not suit use cases requiring a unified compound identity.

## Inputs

- SMILES string (chemical structure in Simplified Molecular Input Line Entry System format)
- Molecular identifier or InChI string
- Repository applicability flags or compound classification metadata

## Outputs

- Unified consolidated results table with per-repository match status
- Normalized compound records (identifiers, names, metadata from each repository)
- Repository-specific match details and confidence indicators

## How to apply

Parse the input SMILES string and validate its chemical structure format. Apply conditional routing logic to determine which of the six target repositories (PubChem, ChemSpider, Norine, ChEBI, COCONUT, NP Atlas) are applicable based on the structure's properties or the repository's documented scope (e.g., Norine specializes in non-ribosomal peptides, NP Atlas in natural products). Dispatch queries to applicable repositories using their respective API endpoints—either in parallel for speed or sequentially to manage rate limits. Collect and normalize match records from each repository response, extracting compound identifiers, common names, and metadata. Consolidate results into a unified output table that preserves per-repository match status, allowing downstream analysis to filter or weight results by source.

## Related tools

- **PubChem** (External chemical repository for structure lookup and standardized compound data) — https://pubchem.ncbi.nlm.nih.gov
- **ChemSpider** (External chemical repository for structure search and property lookup) — http://www.chemspider.com
- **Norine** (External repository specialized in non-ribosomal peptide (NRP) structure lookup) — https://bioinfo.lifl.fr/norine/
- **ChEBI** (External repository for chemical entities of biological interest) — https://www.ebi.ac.uk/chebi/downloadsForward.do
- **COCONUT** (External repository for natural product chemical structures) — https://coconut.naturalproducts.net
- **NP Atlas** (External repository for natural product structures and metadata) — https://www.npatlas.org
- **SmilesDrawer** (Library for parsing and validating SMILES strings before routing) — https://github.com/privrja/smilesDrawer
- **Symfony** (Backend framework in PHP used to implement conditional routing and API orchestration logic) — https://github.com/privrja/thesis
- **React/TypeScript** (Frontend framework for displaying consolidated multi-repository results and managing query submission) — https://github.com/privrja/thesis-frontend-react

## Evaluation signals

- Validate that all queries dispatched to applicable repositories received a response (no timeouts or dropped requests).
- Verify that per-repository match records are normalized and include consistent identifiers, names, and metadata fields across all sources.
- Confirm that the consolidated output table preserves repository-specific match status and does not merge records across repositories unless explicitly deduplicated.
- Check that conditional routing logic correctly excluded repositories that were not applicable for the input compound class (e.g., NRP queries should not return empty or erroneous results from non-NRP repositories).
- Inspect a sample of multi-repository queries to ensure result latency is acceptable for the chosen dispatch strategy (parallel vs. sequential).

## Limitations

- Repository API availability and rate limits may introduce latency or failure modes; sequential vs. parallel dispatch must be tuned per repository SLA.
- Conditional routing logic depends on accurate classification of input structures; misclassified compounds may be routed to inapplicable repositories or miss relevant matches.
- Each external repository uses different identifier schemes, naming conventions, and metadata formats; normalization may lose fine-grained information or introduce collation errors.
- No changelog found in the MassSpecBlocks project; versioning and breaking changes to external API endpoints may not be tracked.

## Evidence

- [intro] MassSpecBlocks enables users to find chemical structures across multiple external repositories including PubChem, ChemSpider, Norine, ChEBI, COCONUT, and NP Atlas through integrated lookups.: "find structures on other chemical projects like Pubchem, ChemSpider, Norine, ChEBI, COCONUT and NP Atlas"
- [other] Parse input SMILES string and validate structure format. Apply conditional routing logic to determine which repositories are applicable for query (based on structure properties or repository scope). Dispatch parallel or sequential queries to external APIs using their respective lookup endpoints.: "Parse input SMILES string and validate structure format. 2. Apply conditional routing logic to determine which repositories are applicable for query (based on structure properties or repository"
- [other] Collect and normalize match records from each repository response, extracting compound identifiers, names, and metadata. Consolidate results into a unified output table with per-repository match status and details.: "Collect and normalize match records from each repository response, extracting compound identifiers, names, and metadata. 5. Consolidate results into a unified output table with per-repository match"
- [readme] Backend is written in PHP with Symfony framework, used to implement API orchestration and conditional routing logic.: "Backend is written in PHP with Symfony framework"
- [readme] Application uses SmilesDrawer library to validate and parse chemical structures from SMILES format.: "Application uses many other libraries like SmilesDrawer from Daniel Probst to draw chemical structures from SMILES format"
