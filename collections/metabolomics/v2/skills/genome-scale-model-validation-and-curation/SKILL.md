---
name: genome-scale-model-validation-and-curation
description: Use when you have multiple draft genome-scale metabolic reconstructions in standard formats (JSON, XML, SBML) representing individual community members or assembly variants, and you need to verify they are structurally sound and consistently annotated before merging them into a consensus model or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - COMMIT
derived_from:
- doi: 10.1371/journal.pcbi.1009906
  title: COMMIT
evidence_spans:
- community-dependent gap-filling using COMMIT for communites sampled from
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_commit_cq
    doi: 10.1371/journal.pcbi.1009906
    title: COMMIT
  dedup_kept_from: coll_commit_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009906
  all_source_dois:
  - 10.1371/journal.pcbi.1009906
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# genome-scale-model-validation-and-curation

## Summary

Validate and curate draft genome-scale metabolic models by parsing, checking structural integrity, and ensuring annotation consistency before integration into consensus reconstructions. This skill ensures input models meet quality standards required for reliable community-level metabolic analysis.

## When to use

You have multiple draft genome-scale metabolic reconstructions in standard formats (JSON, XML, SBML) representing individual community members or assembly variants, and you need to verify they are structurally sound and consistently annotated before merging them into a consensus model or using them for gap-filling.

## When NOT to use

- Input models are already manually curated and have been published in a peer-reviewed database (e.g., BIGG, ModelSEED); re-validation may be unnecessary.
- You are working with a single genome-scale model rather than multiple drafts; validation is still useful but consensus merging is not applicable.
- The input is not a genome-scale metabolic model (e.g., it is a gene expression table, taxonomic profile, or phenotype matrix).

## Inputs

- Draft genome-scale metabolic models in JSON format
- Draft genome-scale metabolic models in XML format
- Draft genome-scale metabolic models in SBML format

## Outputs

- Validated metabolic model objects with confirmed structural integrity
- Validation report flagging missing or inconsistent annotations
- Curated model set ready for consensus merging

## How to apply

Load each draft metabolic model in standard format using COMMIT. Parse and validate the model to verify structural integrity—checking that reactions, metabolites, and gene associations are properly defined and interconnected. Verify annotation consistency across models to identify conflicting or incomplete metadata. Remove or flag models with critical validation errors before proceeding to consensus merging. Models that pass validation are eligible for community-dependent gap-filling and conflict resolution in the consensus-building workflow.

## Related tools

- **COMMIT** (Parses, validates, and merges draft metabolic models using community-dependent gap-filling logic to generate consensus reconstructions) — https://zenodo.org/badge/latestdoi/363932874

## Evaluation signals

- All input models parse without structural errors (reactions, metabolites, and gene associations are well-formed).
- Annotation fields (gene IDs, EC numbers, metabolite identifiers) are present and formatted consistently across validated models.
- No critical gaps or orphaned reactions remain after validation (all reactions have defined reactants, products, and at least partial gene associations where applicable).
- Validated models proceed successfully to COMMIT's consensus-merging algorithm without downstream parsing failures.
- Models flagged as invalid are documented with specific error messages (e.g., unmatched metabolite references, disconnected reaction subnetworks) to inform curation decisions.

## Limitations

- Validation checks structural and annotation consistency but does not assess biological accuracy or pathway completeness; additional domain expert review may be required for curation.
- Models with identical reactions but different annotation schemes (e.g., alternative metabolite identifiers for the same compound) may pass validation but introduce redundancy during consensus merging.
- Validation cannot distinguish between genuinely missing pathways and false-negative annotations in incomplete or low-coverage draft reconstructions.

## Evidence

- [other] Load multiple draft metabolic models into COMMIT for validation: "Load multiple draft metabolic models (in standard format such as JSON or XML) representing individual community members or assembly variants."
- [other] Parse and validate each input model for structural integrity and annotation consistency: "Parse and validate each input model using COMMIT to ensure structural integrity and annotation consistency."
- [intro] Community-dependent gap-filling is applied after validation to resolve conflicts and gaps: "community-dependent gap-filling using COMMIT for communites sampled from"
