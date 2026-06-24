---
name: candidate-set-generation-for-annotation
description: Use when when you have raw or unprocessed PubChem compound records and
  need to produce a curated set of candidate metabolite structures for input to MAGMa
  job calculations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MAGMa
  - pubchem (eMetabolomics subproject)
  license_tier: restricted
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma_cq
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5702/massspectrometry.S0033
  all_source_dois:
  - 10.5702/massspectrometry.S0033
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# candidate-set-generation-for-annotation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract, standardize, and validate chemical structures from the PubChem database to generate a candidate structure set compatible with MAGMa's mass-spectrometry annotation pipeline. This skill bridges public chemical databases to metabolite identification by ensuring structural data meets format, schema, and completeness requirements.

## When to use

When you have raw or unprocessed PubChem compound records and need to produce a curated set of candidate metabolite structures for input to MAGMa job calculations. Use this skill when starting a new metabolite annotation workflow that requires a lookup database of known chemical structures with standardized molecular properties.

## When NOT to use

- Input is already a pre-validated MAGMa lookup database or candidate set from a prior run.
- You need to filter candidates by biological relevance or organism-specific metabolism; this skill performs chemical standardization only, not metabolic filtering.
- Your annotation task does not require a candidate database (e.g., de novo structure elucidation without reference set).

## Inputs

- PubChem compound records (raw database export or API responses)
- Chemical structure data (SMILES, InChI, or MOL format)
- Molecular property metadata (mass, formula, identifiers)

## Outputs

- Standardized candidate structure set (indexed by identifier)
- Processed molecular properties (mass, formula, inchikey, CID)
- MAGMa-compatible lookup database or export file
- Quality report (row counts, schema validation results, missing-data counts)

## How to apply

Begin by extracting and parsing PubChem compound records from the public database using PubChem's API or bulk download. Filter and standardize chemical structures to ensure compatibility with MAGMa's annotation pipeline—this includes validating molecular formula, handling stereochemistry, and removing duplicates or invalid entries. Generate or compile candidate structure identifiers (e.g., PubChem CID) paired with computed or retrieved molecular properties (mass, formula, inchikey). Validate the candidate set for completeness (all required fields present) and format compliance against MAGMa's input schema. Finally, export the processed candidate structures in the format required by MAGMa job calculation, typically as a structured lookup database or indexed file.

## Related tools

- **MAGMa** (Target annotation engine that consumes the standardized candidate set to annotate mass spectra with in silico generated metabolites) — https://github.com/NLeSC/MAGMa
- **pubchem (eMetabolomics subproject)** (Dedicated module for extracting, parsing, and processing PubChem database records into candidate structure format) — https://github.com/NLeSC/MAGMa

## Evaluation signals

- All PubChem records in the input batch are parsed without structural errors or parsing exceptions.
- Candidate set schema validation passes: all required fields (CID, SMILES/InChI, mass, formula) are present for ≥95% of records.
- Duplicate structures (identical InChIKey or CID) are removed; candidate count is ≤ input record count.
- Exported file loads successfully into MAGMa job launcher and passes pre-flight validation (format, encoding, index integrity).
- Molecular property values are within expected ranges (e.g., mass > 0, formula contains valid atomic symbols; no NaN or malformed entries in export).

## Limitations

- The skill performs chemical standardization and format compliance only; it does not curate or filter candidates by biological relevance, organism metabolism, or chemical space restrictions. Filtering by metabolic pathway must be done as a separate downstream step.
- PubChem contains both experimental and predicted structures; no distinction is made during candidate set generation. Users should be aware that predicted or low-confidence structures may be included.
- Large-scale PubChem processing may encounter rate-limiting or quota issues if using the API; bulk download is recommended for complete datasets.
- Quality of the candidate set is limited by the quality of source PubChem records; inconsistencies or errors in PubChem (e.g., incorrect mass or formula metadata) will propagate to the output.

## Evidence

- [other] Extract and parse PubChem compound records from the public PubChem database.: "Extract and parse PubChem compound records from the public PubChem database."
- [other] Filter and standardize chemical structures to ensure compatibility with MAGMa's annotation pipeline.: "Filter and standardize chemical structures to ensure compatibility with MAGMa's annotation pipeline."
- [other] Generate or compile candidate structure identifiers and molecular properties.: "Generate or compile candidate structure identifiers and molecular properties."
- [other] Validate the candidate set for completeness and format compliance.: "Validate the candidate set for completeness and format compliance."
- [other] Export the processed candidate structures to the format required by MAGMa job calculation.: "Export the processed candidate structures to the format required by MAGMa job calculation."
- [readme] The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application.: "The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application."
- [readme] pubchem - Processing of PubChem database, used to find mass candidates: "pubchem - Processing of PubChem database, used to find mass candidates"
