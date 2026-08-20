---
name: drugbank-format-parsing
description: Use when when you have obtained a DrugBank release file (requiring access
  credentials) and need to extract drug records with standardized fields (names, structures,
  identifiers, classification) for integration into a metadata enrichment or cleanup
  workflow that queries multiple drug/natural product.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3407
  tools:
  - drugbank_extraction.py
  - jobs.py
  - metadata_cleanup_prefect.py
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# drugbank-format-parsing

## Summary

Parse and extract structured drug information from DrugBank release files using the drugbank_extraction.py script to populate a metadata cleanup pipeline. This skill transforms raw DrugBank XML or database files into validated, structured records compatible with downstream natural product and drug metadata workflows.

## When to use

When you have obtained a DrugBank release file (requiring access credentials) and need to extract drug records with standardized fields (names, structures, identifiers, classification) for integration into a metadata enrichment or cleanup workflow that queries multiple drug/natural product databases.

## When NOT to use

- DrugBank data has already been extracted and validated in a previous workflow run — reuse the cached output instead of re-parsing to avoid redundant computation.
- You do not have access credentials to download the DrugBank release file — the skill requires authenticated access and cannot proceed without it.
- Your metadata does not require drug information fields — if you are only working with natural product or PubChem compound data, this extraction step is unnecessary.

## Inputs

- DrugBank release file (XML or database export format)
- DrugBank access credentials (username/password or API key as noted in access requirements)

## Outputs

- Structured drug record table or file with standardized column names
- Parsed drug metadata including identifiers, names, structures, and classifications
- Validated artifact compatible with metadata cleanup pipeline

## How to apply

Execute drugbank_extraction.py on a downloaded DrugBank release file to parse and extract drug information into a structured format. The script handles the DrugBank-specific XML or database schema and outputs records with consistent field names matching the metadata template (unique identifiers, chemical names, structure information, drug classifications). Validate the output artifact by checking that (1) the expected number of drug records are present, (2) all required fields defined in the metadata template are populated, and (3) records contain the fields required by downstream metadata cleanup workflows (such as structure data for PubChem cross-referencing or drug classification for filtering).

## Related tools

- **drugbank_extraction.py** (Primary script that parses and extracts drug information from the DrugBank release file into a structured format for downstream metadata cleanup) — https://github.com/corinnabrungs/msn_tree_library
- **jobs.py** (Configuration file that enables or disables DrugBank querying and other data source integrations based on local file availability and access credentials) — https://github.com/corinnabrungs/msn_tree_library
- **metadata_cleanup_prefect.py** (Orchestration workflow that integrates drugbank_extraction.py output with other data cleanup and enrichment steps via Prefect 2 workflow management) — https://github.com/corinnabrungs/msn_tree_library

## Examples

```
python drugbank_extraction.py drugbank_release_file.xml --output drug_records.csv
```

## Evaluation signals

- Output file contains the expected number of drug records with no truncation or parsing errors.
- All required metadata template columns are present in the output and populated for the majority of records (e.g., drug name, identifier, structure information).
- Cross-validation: sample records from the extraction output match the original DrugBank entries when spot-checked.
- Downstream metadata cleanup workflow accepts the extracted file without schema validation errors.
- Structure information extracted from DrugBank can be successfully matched or supplemented by PubChem Name search for records missing structure data.

## Limitations

- DrugBank requires authentication; access is restricted and must be obtained separately before extraction can begin.
- The extraction output quality and completeness depend on the DrugBank release file format and version; format changes may require script updates.
- Some drug records in DrugBank may lack complete structure or classification information, requiring fallback to PubChem Name search or other enrichment steps.
- No changelog is provided in the repository, making it difficult to track changes to the extraction script or identify version-specific compatibility issues.

## Evidence

- [intro] Downloaded release file extraction and parsing: "run `drugbank_extraction.py` on that file"
- [readme] DrugBank access requirement: "DrugBank (access needed): [Download] and run `drugbank_extraction.py` on that file"
- [intro] Metadata template standardization: "use the [template] for your metadata for having same column names and minimum needed information for the query"
- [intro] Integration with downstream workflows: "Metadata cleanup and standardization using template"
- [readme] Structure information fallback: "If no structure information is provided, it is queried from PubChem by Name search"
