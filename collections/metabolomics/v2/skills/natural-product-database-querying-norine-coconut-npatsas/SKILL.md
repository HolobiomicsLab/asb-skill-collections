---
name: natural-product-database-querying-norine-coconut-npatsas
description: Use when you have a chemical structure (as SMILES string or identifier)
  and need to discover matching records across specialized natural product databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0208
  tools:
  - Norine
  - ChEBI
  - COCONUT
  - NP Atlas
  - PHP
  - Symfony
  - SmilesDrawer
  - Symfony (PHP backend)
  - React (TypeScript frontend)
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-021-00530-2
  title: MassSpecBlocks
evidence_spans:
- find structures on other chemical projects like Norine
- find structures on other chemical projects like ChEBI
- find structures on other chemical projects like COCONUT
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

# Natural Product Database Querying (Norine, COCONUT, NP Atlas)

## Summary

Query multiple specialized natural product repositories (Norine, COCONUT, NP Atlas) alongside general chemical databases to locate and retrieve chemical structure records for non-ribosomal peptides and microbial metabolites. This skill enables comprehensive cross-database searches when a user needs to find a compound across repositories with different taxonomic or structural scope.

## When to use

Apply this skill when you have a chemical structure (as SMILES string or identifier) and need to discover matching records across specialized natural product databases. Use it specifically when searching for non-ribosomal peptides (NRPs), microbial metabolites, or compounds known to exist in curated natural product collections. Trigger conditions: input is a validated SMILES string or chemical identifier; search goal is comprehensive multi-repository discovery rather than targeted lookup in a single database.

## When NOT to use

- Input is a mass spectrum or spectral feature list rather than a chemical structure—use mass spectral library search instead
- Goal is to query only general chemical databases (PubChem, ChemSpider) without natural product specialization
- SMILES string is malformed or cannot be validated; pre-validate structure format before invoking this skill

## Inputs

- SMILES string (validated chemical structure notation)
- Chemical identifier (InChI, InChIKey, or database accession)
- Repository scope filter (optional; defaults to all applicable repositories)

## Outputs

- Unified consolidated table with columns: compound_name, SMILES, repository_source, match_type (exact/similarity), repository_identifier, organism_source, confidence_score
- Per-repository match status report
- Deduplicated compound records merged across repositories

## How to apply

Parse and validate the input SMILES string for proper chemical structure format. Apply conditional routing logic to determine which natural product repositories (Norine, COCONUT, NP Atlas) are applicable based on structure properties and repository scope—for example, Norine specializes in non-ribosomal peptides, while COCONUT and NP Atlas cover broader natural product collections. Dispatch parallel or sequential API queries to the applicable repositories using their respective lookup endpoints (structure similarity or exact match modes depending on repository capabilities). Collect and normalize match records from each repository, extracting compound identifiers, chemical names, source organisms, and structural metadata. Consolidate results into a unified output table indexed by repository with per-repository match status, confidence scores, and data provenance.

## Related tools

- **Norine** (Specialized repository for non-ribosomal peptide structures and sequences; API endpoint for NRP-specific structure queries) — https://bioinfo.lifl.fr/norine/
- **COCONUT** (Curated collection of natural product structures; REST API for structure lookup and retrieval across diverse natural products) — https://coconut.naturalproducts.net
- **NP Atlas** (Manually curated natural product database with organism associations; API for structure and metabolite queries) — https://www.npatlas.org
- **SmilesDrawer** (Validates and visualizes SMILES input strings for chemical structure verification before database dispatch) — https://github.com/privrja/smilesDrawer
- **Symfony (PHP backend)** (REST API framework that implements conditional routing logic, parallel repository dispatch, and response normalization) — https://github.com/privrja/thesis
- **React (TypeScript frontend)** (User interface for SMILES input, repository selection, and consolidated result display) — https://github.com/privrja/thesis-frontend-react

## Evaluation signals

- All returned records have valid chemical identifiers (SMILES, InChI, or repository accession) that can be validated against input structure
- Per-repository match counts are non-zero only for repositories that returned results; zero counts are explicitly reported for repositories with no matches
- Consolidated table contains no duplicate compound records (merge on canonical SMILES or InChIKey); if duplicates exist across repositories, they are flagged with source attribution
- Latency and response completeness: all queried repositories return results within documented timeout; partial failures are logged per-repository
- Match metadata is consistent with repository scope (e.g., Norine results contain NRP classification; COCONUT/NP Atlas results include organism source when available)

## Limitations

- Repository API availability and rate limits vary; some repositories may timeout or return incomplete results during high-traffic periods
- Norine is optimized for non-ribosomal peptides; queries for non-peptide natural products may yield no matches despite presence in COCONUT or NP Atlas
- SMILES validation is strict; minor formatting variations (e.g., implicit vs. explicit hydrogens) may cause query failures before dispatch
- Cross-repository deduplication relies on structure normalization (canonical SMILES or InChIKey); isomeric variants or tautomers may be reported separately by different repositories
- Natural product metadata (organism source, bioactivity) completeness varies significantly across repositories; unified table reflects per-repository data quality

## Evidence

- [intro] MassSpecBlocks enables users to find chemical structures across multiple external repositories including PubChem, ChemSpider, Norine, ChEBI, COCONUT, and NP Atlas through integrated lookups.: "find structures on other chemical projects like Pubchem, ChemSpider, Norine, ChEBI, COCONUT and NP Atlas"
- [other] The workflow involves parsing SMILES, applying conditional routing logic, dispatching parallel queries, collecting and normalizing results, and consolidating them into a unified output table.: "1. Parse input SMILES string and validate structure format. 2. Apply conditional routing logic to determine which repositories are applicable for query (based on structure properties or repository"
- [readme] MassSpecBlocks is an open-source web application designed to manage chemical structure databases and find structures on other chemical projects.: "open-source web application to manage own user databases of chemical structures like NRPs and to find structures on other chemical projects"
- [readme] The backend uses Symfony framework in PHP to orchestrate API calls and response processing.: "Backend is written in PHP with Symfony framework"
- [readme] SmilesDrawer is used to validate chemical structure input before database dispatch.: "Application uses many other libraries like SmilesDrawer"
