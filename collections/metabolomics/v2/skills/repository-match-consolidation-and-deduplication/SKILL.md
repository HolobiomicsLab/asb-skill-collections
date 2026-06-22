---
name: repository-match-consolidation-and-deduplication
description: 'Use when use this skill after parallel or sequential dispatch queries to multiple chemical repositories have returned results. Specifically: (1) you have received match records from two or more of {PubChem, ChemSpider, Norine, ChEBI, COCONUT, NP Atlas} with differing schemas or identifiers;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3906
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0602
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
  - PHP/Symfony
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# repository-match-consolidation-and-deduplication

## Summary

Consolidate and normalize chemical structure search results returned from multiple external repositories (PubChem, ChemSpider, Norine, ChEBI, COCONUT, NP Atlas) into a unified output table with per-repository match status, deduplication, and standardized metadata. This skill is essential when cross-repository queries return heterogeneous result formats and you need a single canonical view of which compounds match across sources.

## When to use

Use this skill after parallel or sequential dispatch queries to multiple chemical repositories have returned results. Specifically: (1) you have received match records from two or more of {PubChem, ChemSpider, Norine, ChEBI, COCONUT, NP Atlas} with differing schemas or identifiers; (2) you need to detect and handle duplicates (the same compound reported under different identifiers across repositories); (3) you want a unified output that shows per-repository presence/absence and normalized compound metadata (identifiers, names, source provenance); (4) your downstream analysis (e.g., mass spectra matching, structure validation) requires a single authoritative record per compound rather than per-repository silos.

## When NOT to use

- Input results are from a single repository only — no consolidation is needed.
- You require preservation of repository-specific idiosyncrasies and do not need normalized cross-repository comparison.
- Deduplication is not desired because you need to retain all repository-specific records as separate entities for audit or lineage purposes.

## Inputs

- Raw API response objects from PubChem lookup endpoint
- Raw API response objects from ChemSpider lookup endpoint
- Raw API response objects from Norine lookup endpoint
- Raw API response objects from ChEBI lookup endpoint
- Raw API response objects from COCONUT lookup endpoint
- Raw API response objects from NP Atlas lookup endpoint
- Input SMILES string or molecular structure identifier (for deduplication anchor)

## Outputs

- Unified consolidated results table (per-repository match status and normalized metadata)
- Compound deduplication map (canonical ID → list of repository-specific IDs)
- Standardized compound metadata record (ID, name, source provenance)

## How to apply

After receiving response payloads from each repository's lookup endpoint, parse and extract the compound identifiers (e.g., PubChem CID, ChemSpider ID, ChEBI accession), compound names, and any repository-specific metadata (molecular weight, SMILES, InChI). Normalize identifier formats and structure representation (e.g., canonicalize SMILES strings or compare InChI keys) to enable cross-repository deduplication. Group results by canonical compound identifier or structural fingerprint; when the same compound is reported by multiple repositories under different IDs, merge those records into a single row. Construct a consolidated output table with columns for compound ID (canonical), name, and per-repository match status (present/absent) and details. This normalization step ensures downstream workflows (e.g., CycloBranch export, mass spectrum annotation) operate on a deduplicated, schema-consistent dataset rather than repository-specific fragments.

## Related tools

- **PubChem** (Source repository for chemical structure lookup and compound metadata) — https://pubchem.ncbi.nlm.nih.gov
- **ChemSpider** (Source repository for chemical structure lookup and compound metadata) — http://www.chemspider.com
- **Norine** (Source repository for non-ribosomal peptide structures and metadata) — https://bioinfo.lifl.fr/norine/
- **ChEBI** (Source repository for chemical entities of biological interest) — https://www.ebi.ac.uk/chebi/
- **COCONUT** (Source repository for natural product chemical structures) — https://coconut.naturalproducts.net
- **NP Atlas** (Source repository for natural product structures and biosynthesis data) — https://www.npatlas.org
- **SmilesDrawer** (Parse and canonicalize SMILES structure representations for deduplication) — https://github.com/privrja/smilesDrawer
- **PHP/Symfony** (Backend framework for implementing consolidation and normalization logic) — https://github.com/privrja/thesis

## Evaluation signals

- Consolidated output table has exactly one row per unique compound (verified by canonical ID uniqueness); no duplicate compounds appear across rows.
- All per-repository columns show consistent presence/absence markers (e.g., match found vs. no match) with no internal contradictions.
- Compound metadata (name, molecular weight, SMILES) is identical across all repository rows for the same canonical compound, indicating successful normalization.
- Cross-repository deduplication map correctly links repository-specific identifiers (e.g., PubChem CID 12345 and ChemSpider ID 67890) to the same canonical compound when SMILES or InChI comparison confirms identity.
- Export format (e.g., for CycloBranch) preserves all consolidated metadata and per-repository provenance without loss or truncation.

## Limitations

- Deduplication accuracy depends on the quality and consistency of structure representation across repositories; if SMILES or InChI data are missing or malformed in some repositories, false negatives (same compound treated as distinct) may occur.
- Repository APIs may have rate limits or intermittent availability; if one repository times out during a dispatch query, its results will be absent from consolidation, leading to incomplete per-repository coverage.
- Naming conflicts (same compound name used for different structures in different repositories) can confound normalization if only name-based matching is applied; structure-based matching (SMILES/InChI) is required to avoid false positives.
- No changelog or versioning strategy is documented in the MassSpecBlocks repository, so consolidated results may become stale if external repository schemas or identifier systems change without notice.

## Evidence

- [other] Collect and normalize match records from each repository response, extracting compound identifiers, names, and metadata.: "Collect and normalize match records from each repository response, extracting compound identifiers, names, and metadata."
- [other] Consolidate results into a unified output table with per-repository match status and details.: "Consolidate results into a unified output table with per-repository match status and details."
- [other] MassSpecBlocks enables users to find chemical structures across multiple external repositories including PubChem, ChemSpider, Norine, ChEBI, COCONUT, and NP Atlas through integrated lookups.: "MassSpecBlocks enables users to find chemical structures across multiple external repositories including PubChem, ChemSpider, Norine, ChEBI, COCONUT, and NP Atlas through integrated lookups."
- [readme] open-source web application to manage own user databases of chemical structures like NRPs and to find structures on other chemical projects like Pubchem, ChemSpider, Norine, ChEBI, COCONUT and NP Atlas: "open-source web application to manage own user databases of chemical structures like NRPs and to find structures on other chemical projects like Pubchem, ChemSpider, Norine, ChEBI, COCONUT and NP"
