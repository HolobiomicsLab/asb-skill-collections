---
name: database-repository-retrieval
description: Use when when you need to obtain a specific curated database (e.g., DNA adduct compounds) that is published in a GitLab or GitHub repository and available in structured formats (SDF, Excel, Word).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2422
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0089
  tools:
  - RDKit
  - Git / GitLab CLI
derived_from:
- doi: 10.3389/fchem.2022.908572
  title: DNA adduct database
evidence_spans:
- compound database in SDF format
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dna_adduct_database_cq
    doi: 10.3389/fchem.2022.908572
    title: DNA adduct database
  dedup_kept_from: coll_dna_adduct_database_cq
schema_version: 0.2.0
---

# database-repository-retrieval

## Summary

Locate, access, and download curated scientific database files from version-controlled repositories in their native formats (SDF, Excel, online). This skill ensures reproducibility by establishing a traceable chain from authoritative repository source to local validated copy.

## When to use

When you need to obtain a specific curated database (e.g., DNA adduct compounds) that is published in a GitLab or GitHub repository and available in structured formats (SDF, Excel, Word). Use this skill as the first step before parsing, validation, or analysis to ensure you have the canonical version and can document provenance.

## When NOT to use

- The database is already cached or available in your analysis environment — retrieve it from local cache instead.
- The repository or file requires credentials you do not have — contact the maintainers or check for publicly mirrored versions.
- The database is only available via a web form or proprietary API that cannot be scripted — manual download may be necessary.

## Inputs

- Repository URL (GitLab, GitHub, or institutional server)
- Project name and database file name from article or README
- Optional: specific file format preference (SDF, Excel, online access)

## Outputs

- Downloaded database file in native format (SDF, Excel, Word, or other)
- Metadata record: retrieval URL, date, format, file size, checksum
- Confirmation of file integrity (file exists, readable, non-corrupted)

## How to apply

Identify the authoritative repository URL from the article or project documentation (e.g., gitlab.com/nexs-metabolomics/projects/dna_adductomics_database). Navigate to the repository and locate the database file in the format suited to your downstream task (SDF for cheminformatics workflows, Excel for tabular summaries). Download the file to local storage, preserving its filename and extension. Document the retrieval date, repository commit/branch, and file checksum to ensure reproducibility. If multiple formats are available, select the format that is native to the tool or workflow you will apply next (e.g., RDKit requires SDF or SMILES).

## Related tools

- **Git / GitLab CLI** (Clone or browse repository and retrieve versioned database files) — https://gitlab.com/nexs-metabolomics/projects/dna_adductomics_database
- **RDKit** (Downstream parsing and validation of SDF-format compound records after retrieval)

## Examples

```
git clone https://gitlab.com/nexs-metabolomics/projects/dna_adductomics_database.git && ls -la dna_adductomics_database/ | grep -E '\.(sdf|xlsx|csv)$'
```

## Evaluation signals

- File downloaded successfully and matches expected filename and format (e.g., .sdf, .xlsx)
- File size and checksum are consistent with repository metadata or prior retrieval
- File opens and reads without I/O errors in the intended downstream tool (e.g., RDKit for SDF)
- File modification date is recent and matches the retrieval session date
- Number of records or entries in the file matches documentation (e.g., 'compound database contains N DNA adducts')

## Limitations

- Repository availability and network access required; files behind authentication or deprecated repositories may be unavailable.
- Multiple formats (Excel, Word, online, SDF) for the same database may diverge; verify consistency or select the canonical format stated in recent documentation.
- No changelog documented in the source article; version history and breaking changes may not be transparent.
- File size and accessibility may vary depending on repository hosting; very large SDF or Excel files may require chunked download or alternative access (e.g., online browser interface).

## Evidence

- [intro] Repository reference for database location: "Access the nexs-metabolomics GitLab repository (gitlab.com/nexs-metabolomics/projects/dna_adductomics_database) and locate the SDF format compound database file."
- [intro] Multiple formats and access points available: "The following files are available: [Excel format, Word format, online, SDF format, experimental fragments online, predicted fragments online, collection of Excel file, online databases, CFM-ID]"
- [other] Downstream validation task following retrieval: "Parse the SDF file using RDKit to verify structural validity and extract the number of molecular records."
- [other] Expected output documentation: "generate a validation report documenting file integrity, record count, and parseable structure verification"
