---
name: drug-database-record-extraction
description: Use when when you have obtained a DrugBank release file (requiring access credentials) and need to integrate drug chemical structure, name, and identifier information into a metadata cleanup or chemical enrichment pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3375
  tools:
  - drugbank_extraction.py
  - jobs.py
  - metadata_cleanup_prefect.py
  techniques:
  - GC-MS
derived_from:
- doi: 10.1038/s41592-025-02813-0
  title: MSnLib
evidence_spans:
- run `drugbank_extraction.py` on that file
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msnlib_cq
    doi: 10.1038/s41592-025-02813-0
    title: MSnLib
  dedup_kept_from: coll_msnlib_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02813-0
  all_source_dois:
  - 10.1038/s41592-025-02813-0
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# drug-database-record-extraction

## Summary

Extract and parse structured drug information from DrugBank release files using the drugbank_extraction.py script to populate a standardized drug metadata table for downstream chemical and biomedical queries. This skill transforms raw DrugBank XML or tabular releases into validated, queryable drug records with consistent schema.

## When to use

When you have obtained a DrugBank release file (requiring access credentials) and need to integrate drug chemical structure, name, and identifier information into a metadata cleanup or chemical enrichment pipeline. Trigger: raw DrugBank file is available locally and downstream workflows expect normalized drug records with consistent column names and minimum required fields (name, structure, identifiers).

## When NOT to use

- DrugBank access credentials are unavailable or expired; use alternative drug sources (Broad Institute Drug Repurposing Hub, DrugCentral) instead.
- Input file is already a validated, normalized drug table conforming to the metadata template; skip extraction and proceed directly to metadata cleanup.
- Downstream workflow does not require DrugBank-specific fields (e.g., only PubChem or LOTUS natural product data is needed).

## Inputs

- DrugBank release file (XML or tabular format from https://go.drugbank.com/releases/latest)
- DrugBank access credentials (username/password or API key)

## Outputs

- Parsed drug records in standardized tabular format (CSV/TSV or structured object)
- Extracted drug information including: drug name, chemical structure (SMILES or InChI), DrugBank accession ID, synonyms, and cross-references
- Validated artifact conforming to metadata template schema

## How to apply

Download or obtain the DrugBank release file from the official DrugBank portal (https://go.drugbank.com/releases/latest), which requires account access. Execute drugbank_extraction.py on the downloaded file to parse and extract drug records into a structured format (matching the metadata template with standardized column names). Validate the output artifact by confirming that (1) all expected drug records are present, (2) mandatory fields (drug name, structure/SMILES, accession IDs) are populated, and (3) the schema matches downstream workflow expectations. The script should produce a tabular or structured output suitable for import into the metadata cleanup pipeline.

## Related tools

- **drugbank_extraction.py** (Primary extraction and parsing script that reads the DrugBank release file and outputs normalized drug records) — https://github.com/corinnabrungs/msn_tree_library
- **jobs.py** (Configuration file for enabling/disabling DrugBank extraction as a local query source in the metadata cleanup pipeline) — https://github.com/corinnabrungs/msn_tree_library
- **metadata_cleanup_prefect.py** (Prefect workflow orchestration that consumes the extracted drug records in downstream metadata standardization steps) — https://github.com/corinnabrungs/msn_tree_library

## Examples

```
python drugbank_extraction.py --input drugbank_release.xml --output drug_records.csv
```

## Evaluation signals

- Output file exists and contains non-zero rows of drug records with expected column names (drug name, structure, accession ID, synonyms).
- All mandatory fields are populated for ≥95% of extracted records; document any missing-value patterns or records with incomplete structures.
- Schema validation: output column names and data types match the metadata template (https://docs.google.com/spreadsheets/d/1v6_IlGS3VgycGc-mSSdNeocY-CFXpONVZbuh3XNLX2E/edit?usp=sharing).
- Spot-check: sample 10–20 extracted records against the original DrugBank release file to verify name, structure, and identifier accuracy.
- Downstream integration: extracted records can be successfully loaded into the metadata cleanup pipeline without schema or type errors.

## Limitations

- DrugBank requires active account access and periodic credential renewal; extraction will fail if credentials are expired or invalid.
- Script is tightly coupled to the specific DrugBank file format and release version; updates to DrugBank schema may require script modifications.
- DrugBank may contain incomplete or outdated structure information for some compounds; users should cross-validate against PubChem if needed.
- No changelog is documented in the repository, making it difficult to track upstream changes to the extraction script.

## Evidence

- [intro] run `drugbank_extraction.py` on that file: "DrugBank (access needed): [Download](https://go.drugbank.com/releases/latest) and run `drugbank_extraction.py` on that file"
- [other] parse and extract drug information into a structured format: "The drugbank_extraction.py script is executed on a downloaded DrugBank release file to extract and parse drug information for use in the metadata cleanup pipeline."
- [other] Validate the output artifact contains the expected drug records and fields required by downstream metadata cleanup workflows: "Validate the output artifact contains the expected drug records and fields required by downstream metadata cleanup workflows."
- [readme] same column names and minimum needed information for the query: "Please use the [template] for your metadata for having same column names and minimum needed information for the query"
- [readme] access needed: "DrugBank (access needed): [Download](https://go.drugbank.com/releases/latest)"
