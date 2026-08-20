---
name: metabolite-set-file-parsing-and-validation
description: Use when when a user has prepared a custom collection of metabolite sets
  (e.g., from spectral fragmentation clustering, literature curation, or domain-specific
  grouping) in CSV or JSON format and wants to score their activity levels using PALS
  without modifying the core PALS codebase.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3172
  tools:
  - PALS Viewer
  - PALS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
- PALS Viewer
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

# metabolite-set-file-parsing-and-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse user-uploaded metabolite set files (CSV or JSON format) to extract metabolite identifiers and set membership, then validate the structure and identifiers against the PALS database schema before downstream decomposition analysis. This skill enables extensibility of pathway activity scoring to custom metabolite groupings beyond the three shipped set types (pathways, Molecular Families, and Mass2Motifs).

## When to use

When a user has prepared a custom collection of metabolite sets (e.g., from spectral fragmentation clustering, literature curation, or domain-specific grouping) in CSV or JSON format and wants to score their activity levels using PALS without modifying the core PALS codebase. Specifically when the metabolite identifiers and set membership must be validated against KEGG, ChEBI, or other database schemas before feeding into the PLAGE decomposition pipeline.

## When NOT to use

- Input metabolite sets are already in PALS's native internal format (no parsing/validation needed)
- Metabolite identifiers cannot be mapped to any supported database (ChEBI, KEGG, Reactome); validation will fail
- File format is neither CSV nor JSON, or the CSV/JSON structure does not follow a two-column or named-list convention

## Inputs

- User-supplied metabolite set file (CSV or JSON format)
- Metabolite identifier type specification (KEGG, ChEBI, or other)
- Target PALS database schema (PiMP_KEGG, COMPOUND, ChEBI, etc.)

## Outputs

- Validated metabolite set collection in PALS-compatible format
- Validation report (success/failure with details on problematic identifiers or sets)
- Formatted input ready for PLAGE decomposition pipeline

## How to apply

First, read and deserialize the user-supplied metabolite set file (CSV with rows of peak IDs and metabolite entity IDs, or JSON with named sets and member lists). Extract the metabolite identifiers (KEGG IDs, ChEBI IDs, or other entity types specified by the user) and map them to internal set identifiers. Validate that (1) all metabolite IDs conform to the target database schema (e.g., KEGG format 'Cxxxxx' or ChEBI 'CHEBI:xxxxx'), (2) the set structure contains at least one metabolite per set, and (3) metabolite identifiers can be resolved in the PALS database. Report validation errors (unrecognized IDs, malformed structure, empty sets) to the user. If validation passes, format the validated metabolite set into the internal data structure expected by the PLAGE decomposition method (compatible with the pathway activity scoring pipeline) and proceed to pathway/set activity scoring.

## Related tools

- **PALS** (Accepts validated metabolite sets as input to PLAGE decomposition for activity scoring) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web interface that displays parsed and scored results from custom metabolite sets in a user-friendly tabular format) — https://pals.glasgowcompbio.org/app/

## Examples

```
from pals.common import *; import pandas as pd; user_sets = pd.read_csv('custom_metabolites.csv', header=None, names=['peak_id', 'entity_id']); validated_sets = DataSource.validate_metabolite_annotation(user_sets, database_name='COMPOUND'); method = PLAGE(DataSource(int_df, validated_sets, experimental_design, 'COMPOUND'))
```

## Evaluation signals

- All metabolite identifiers in the input file are successfully resolved to entries in the target database (KEGG, ChEBI, or Reactome)
- Each metabolite set contains at least one validated metabolite member and has a non-empty set name
- The output data structure conforms to the expected PALS internal representation (comparable to the annotation_df structure documented in the README)
- Validation errors are reported with specific line numbers, problematic IDs, and reasons (e.g., 'C99999 not found in KEGG' or 'set X has zero members')
- The formatted metabolite set can be successfully passed to the PLAGE decomposition method without schema errors

## Limitations

- Parsing and validation are limited to CSV and JSON formats; other serializations (Excel, TSV, XML) require format conversion first
- Validation depends on the availability and integrity of the target database (KEGG, ChEBI, Reactome); offline mode may have outdated entries
- Metabolite identifiers must use standard database IDs (KEGG Cxxxx, ChEBI CHEBI:xxx); custom or non-standard IDs will fail validation
- Sets with very few metabolites (e.g., 1–2 members) may produce unstable or unreliable activity scores when decomposed via PLAGE, though validation itself does not enforce a minimum set size

## Evidence

- [other] Parse user-uploaded metabolite set file (CSV or JSON format) to extract metabolite identifiers and set membership.: "Parse user-uploaded metabolite set file (CSV or JSON format) to extract metabolite identifiers and set membership"
- [other] Validate metabolite set structure and identifiers against the PALS database schema.: "Validate metabolite set structure and identifiers against the PALS database schema"
- [readme] The decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways.: "the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] Users provide a list of compound annotations assigned to peak features as another matrix having two columns. The first column is the peak ID while the second column is the assigned metabolite annotation as either KEGG or ChEBI database IDs.: "users also provide a list of compound annotations assigned to peak features... The first column (or DataFrame index) is the peak ID while the second column is the assigned metabolite annotation as"
- [other] Format and return results in a user-friendly tabular output compatible with PALS Viewer display.: "Format and return results in a user-friendly tabular output compatible with PALS Viewer display"
