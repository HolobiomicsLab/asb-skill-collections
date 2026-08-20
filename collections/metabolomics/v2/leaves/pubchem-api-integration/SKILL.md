---
name: pubchem-api-integration
description: Use when when you have raw chemical structures in diverse input formats
  (SMILES, SDF, or other molecular representations) from multiple sources and need
  to produce a uniform, canonicalized representation before molecular descriptor calculation,
  fingerprinting, or retention time modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  tools:
  - PubChem standardization
  - rcdk
  license_tier: open
derived_from:
- doi: 10.1038/s41592-023-02143-z
  title: RepoRT (retention-time repository)
evidence_spans:
- structures are standardized using the PubChem standardization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_report_retention_time_repository_cq
    doi: 10.1038/s41592-023-02143-z
    title: RepoRT (retention-time repository)
  dedup_kept_from: coll_report_retention_time_repository_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-023-02143-z
  all_source_dois:
  - 10.1038/s41592-023-02143-z
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pubchem-api-integration

## Summary

Apply PubChem standardization to normalize raw chemical structures (SMILES, SDF, or other molecular formats) into canonical representations suitable for downstream cheminformatics analysis. This skill is essential when ingesting heterogeneous chemical data for retention time prediction, molecular fingerprinting, or classification workflows.

## When to use

When you have raw chemical structures in diverse input formats (SMILES, SDF, or other molecular representations) from multiple sources and need to produce a uniform, canonicalized representation before molecular descriptor calculation, fingerprinting, or retention time modeling. Particularly critical in multi-source data collection pipelines where structural inconsistency or salt/counter-ion contamination would compromise downstream model training.

## When NOT to use

- Structures are already validated and canonicalized by upstream processing
- Salt and counter-ion removal is undesirable for your research question (e.g., studying ion-pair behavior)
- You require strict preservation of input stereochemistry or tautomeric variants that PubChem standardization may alter

## Inputs

- Raw chemical structures in SMILES format
- Raw chemical structures in SDF format
- Raw chemical structures in other molecular formats
- Multi-source chemical structure dataset

## Outputs

- Standardized canonical chemical structures
- Validated structure set (pass/fail annotations)
- Structures in canonical output format (e.g., canonical SMILES or SDF)

## How to apply

Load raw chemical structures from your input dataset in their native format. Apply the PubChem standardization procedure to each structure; this step normalizes representation, removes salts and counter-ions, and canonicalizes connectivity according to PubChem rules. Validate each standardized structure for chemical validity and discard any structures that fail standardization without error. Export only passing structures to a canonical output format (e.g., canonical SMILES or SDF) for use in subsequent fingerprinting, descriptor calculation, or machine learning steps. The standardization acts as a gatekeeping filter: structures that pass demonstrate structural integrity and PubChem compliance, reducing noise in downstream models.

## Related tools

- **PubChem standardization** (Applies normalization, salt removal, and canonicalization to raw molecular structures to produce uniform representations)
- **rcdk** (Calculates molecular fingerprints and chemical descriptors downstream of standardized structures)

## Evaluation signals

- All input structures are assigned a pass/fail validation status; failed structures are excluded from downstream analysis
- Canonical SMILES or SDF output is deterministic: re-running the same input structure yields identical standardized output
- Salts and counter-ions are removed and not present in standardized structures (verify by inspecting molecular formula or charge state)
- Standardized structures can be successfully parsed and used by downstream tools (rcdk fingerprinting, ClassyFire classification) without error
- Structure count after standardization is ≤ input structure count (due to validation filtering); expect 90–100% retention for high-quality input data

## Limitations

- PubChem standardization may alter stereochemistry or tautomeric forms; structures with ambiguous or non-standard stereo representation may be flagged or lost
- Very large structures or unusual chemistry outside PubChem's rule set may fail standardization and be excluded from analysis
- The standardization procedure does not correct for drawing errors or chemical implausibility in the input; it assumes input structures are chemically reasonable

## Evidence

- [other] Load raw chemical structures (SMILES, SDF, or other molecular format) from input dataset.: "Load raw chemical structures (SMILES, SDF, or other molecular format) from input dataset"
- [other] Apply PubChem standardization procedure to each structure to normalize representation, remove salts, and canonicalize connectivity.: "Apply PubChem standardization procedure to each structure to normalize representation, remove salts, and canonicalize connectivity"
- [other] Validate standardized structures for chemical validity and retain only structures that pass standardization without error.: "Validate standardized structures for chemical validity and retain only structures that pass standardization without error"
- [readme] From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk.: "From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk"
