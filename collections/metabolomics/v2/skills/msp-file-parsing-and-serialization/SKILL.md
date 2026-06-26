---
name: msp-file-parsing-and-serialization
description: Use when you have raw .msp files containing mass spectra records and
  need to extract spectrum identifiers (compound name, precursor mass, retention time)
  as structured data for enrichment via external web services, or you have enriched
  spectrum objects and must write them back to .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MSMetaEnhancer
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - RDKit
  - Python
  - pytest
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- '**MSMetaEnhancer** is a tool used for `.msp` files annotation'
- '`MSMetaEnhancer/libs/converters/web/` named after your service'
- 'fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation)'
- __all__ = ['IDSM', 'CTS', 'CIR', 'PubChem', 'BridgeDb', 'MyService']
- '[CTS](https://cts.fiehnlab.ucdavis.edu/)'
- '[PubChem](https://pubchem.ncbi.nlm.nih.gov/)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer_cq
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.04494
  all_source_dois:
  - 10.21105/joss.04494
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msp-file-parsing-and-serialization

## Summary

Parse mass spectrometry library (.msp) files into structured spectrum records (compound name, mass, metadata) and serialize enriched spectra back to .msp format while preserving original structure. Essential for loading and exporting annotated metabolite data in mass spectrometry workflows.

## When to use

You have raw .msp files containing mass spectra records and need to extract spectrum identifiers (compound name, precursor mass, retention time) as structured data for enrichment via external web services, or you have enriched spectrum objects and must write them back to .msp format for downstream analysis or sharing.

## When NOT to use

- Input is already a parsed spectrum object in memory — use direct field access instead of re-parsing.
- You need real-time streaming of spectra without materialization to disk — MSMetaEnhancer's file-based approach requires batch load/save cycles.
- Target output format is not .msp (e.g., CSV, JSON, or proprietary database) — use format-specific serializers instead.

## Inputs

- .msp file (mass spectrometry library format)
- spectrum records with compound identifiers (name, mass, m/z)
- optional: existing metadata fields to preserve

## Outputs

- Spectrum objects (structured records with parsed fields)
- .msp file with enriched metadata (SMILES, InChI, CAS number, etc.)
- enriched spectrum records ready for downstream analysis

## How to apply

Use MSMetaEnhancer's Spectra or DataFrame data class to load the .msp file, which parses each spectrum record into compound identifiers and associated metadata fields. Extract key attributes (compound_name, mass) needed for conversion jobs. After enrichment via external converters, merge response dictionaries into the spectrum record, applying error handling to skip missing or malformed responses. Finally, serialize the enriched spectra back to .msp using MSMetaEnhancer's export method, ensuring original file structure is preserved and new metadata fields are appended to each record.

## Related tools

- **MSMetaEnhancer** (Primary library for loading, parsing, and serializing .msp files via Spectra and DataFrame data classes; handles spectrum record extraction and metadata field merging) — https://github.com/RECETOX/MSMetaEnhancer
- **pytest** (Testing framework to validate parse correctness and round-trip serialization (load → enrich → save) integrity)

## Examples

```
from MSMetaEnhancer import Application

app = Application()
app.load_data('sample.msp', file_format='msp')
app.save_data('sample_out.msp', file_format='msp')
```

## Evaluation signals

- Round-trip integrity: load .msp → serialize → verify field counts and values match original (no loss of spectrum records or identifiers)
- Schema validation: parsed spectrum objects contain all expected fields (compound_name, mass, metadata keys) with correct types
- Error handling: malformed or missing metadata in input .msp does not crash parsing; gracefully handled records appear in output with partial data
- Enrichment merge: new metadata fields (SMILES, InChI) from converters appear in serialized .msp without overwriting or corrupting original fields
- Format compliance: output .msp follows standard structure (spectrum records separated by blank lines, key-value pairs per line) readable by external tools

## Limitations

- Parser assumes well-formed .msp syntax; non-standard delimiters or malformed spectrum blocks may cause parsing errors or data loss.
- Large .msp files (>10k spectra) require in-memory materialization; streaming or chunked parsing not documented, may cause memory pressure.
- Metadata field order and naming conventions in output .msp depend on converter response format; inconsistency may arise when multiple sources provide overlapping fields.
- Special characters or Unicode in compound names may not be preserved correctly across parse → serialize cycles depending on file encoding.

## Evidence

- [other] Load the input .msp file using MSMetaEnhancer's Spectra or DataFrame data class to parse spectrum records and extract identifiers (compound name, mass).: "Load the input .msp file using MSMetaEnhancer's Spectra or DataFrame data class to parse spectrum records and extract identifiers (compound name, mass)."
- [other] Write the enriched spectra back to an .msp file, preserving original structure and adding new metadata fields.: "Write the enriched spectra back to an .msp file, preserving original structure and adding new metadata fields."
- [readme] MSMetaEnhancer is a tool used for `.msp` files annotation. It adds metadata like SMILES, InChI, and CAS number fetched from the following services: "MSMetaEnhancer is a tool used for `.msp` files annotation. It adds metadata like SMILES, InChI, and CAS number"
- [other] Parse and merge response dictionaries from each converter into the spectrum record, applying error handling to gracefully skip missing or malformed responses.: "Parse and merge response dictionaries from each converter into the spectrum record, applying error handling to gracefully skip missing or malformed responses."
