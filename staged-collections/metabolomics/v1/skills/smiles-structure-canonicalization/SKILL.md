---
name: smiles-structure-canonicalization
description: Use when metabolomics involves LC-MS or GC-MS untargeted lipidomics to derive canonical SMILES, InChI, and InChIKey representations from compound names or existing chemical identifiers using RDKit and PubChem reference data.
when_to_use_negative:
- Input records already contain validated canonical SMILES and matching InChIKey without ambiguities.
- Compound names are trade names, metabolite identifiers, or non-IUPAC strings that do not resolve to PubChem entries.
- The analysis goal does not require standardized chemical structure representation (e.g., spectral similarity matching alone).
edam_operation: http://edamontology.org/operation_3346
edam_topics:
- http://edamontology.org/topic_0154
- http://edamontology.org/topic_3375
tools:
- name: RDKit
  role: Parse, canonicalize, and validate SMILES and InChI representations; compare structural representations across formats
- name: PubChem
  role: Reference database for retrieving canonical SMILES, InChI, and InChIKey from compound names and identifiers
- name: matchms
  role: Framework for applying the 'derive annotation from compound name' filter and managing spectrum metadata; version 0.26.4 or later
  repo: https://github.com/matchms/matchms
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/smiles-structure-canonicalization/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/smiles-structure-canonicalization/skill.md
    merged_at: '2026-05-25T07:04:57.408285+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/smiles-structure-canonicalization@sha256:12c9e046c28e4733b21866514d95dc17459c40314a3766c5ed0f189132491509
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# SMILES Structure Canonicalization

## Summary

Derive canonical SMILES, InChI, and InChIKey representations from compound names or existing chemical identifiers using RDKit and PubChem reference data. This skill ensures consistent, machine-readable chemical structure notation across a mass spectral library, enabling reliable downstream annotation validation and adduct repair.

## When to use

Apply this skill when you have mass spectral records with compound names or partial chemical identifiers but lack standardized SMILES representations, or when you need to validate existing SMILES against a reference database. Specifically useful before applying adduct repair or structure validation filters, or when preparing metadata for library harmonization. The matchms pipeline applies this during the 'derive annotation from compound name' step, where 72.4% of spectra require SMILES derivation from their compound names.

## When NOT to use

- Input records already contain validated canonical SMILES and matching InChIKey without ambiguities.
- Compound names are trade names, metabolite identifiers, or non-IUPAC strings that do not resolve to PubChem entries.
- The analysis goal does not require standardized chemical structure representation (e.g., spectral similarity matching alone).

## Inputs

- Mass spectral records with compound names (matchms Spectrum objects or GNPS-format metadata)
- SMILES strings (when present in input annotations)
- PubChem-indexed compound identifiers or InChIKeys

## Outputs

- Canonical SMILES strings (standardized structure representation)
- InChI strings (IUPAC International Chemical Identifier)
- InChIKey strings (hashed InChI for fast lookup)
- Cleaned mass spectral records with validated structure annotations
- Mismatch report: records where derived 2D structure differs from input

## How to apply

Load the mass spectral library records containing compound names or SMILES strings into matchms (version 0.26.4 or compatible). Use RDKit to parse and canonicalize SMILES, then query PubChem to retrieve the canonical SMILES, InChI, and InChIKey for each record. Compare derived SMILES and InChIKeys across all three representations (input SMILES, derived SMILES, and InChIKey) to detect inconsistencies; flag records where the derived 2D structure differs from the input annotation. Accept records where all three representations are consistent; optionally repair or remove records with mismatches depending on confidence thresholds. The filter outputs cleaned records with standardized SMILES and associated InChI/InChIKey fields, enabling robust comparison to reference mass shifts and adduct states in downstream repair steps.

## Related tools

- **RDKit** (Parse, canonicalize, and validate SMILES and InChI representations; compare structural representations across formats)
- **PubChem** (Reference database for retrieving canonical SMILES, InChI, and InChIKey from compound names and identifiers)
- **matchms** (Framework for applying the 'derive annotation from compound name' filter and managing spectrum metadata; version 0.26.4 or later) — https://github.com/matchms/matchms

## Evaluation signals

- Percentage of spectra with successfully derived SMILES: expect ≥72.4% when compound names are available and resolvable in PubChem.
- Consistency check: all three representations (input SMILES, derived SMILES, InChIKey) match for ≥98.38% of annotated spectra (converse of reported 1.62% mismatch rate).
- No missing values in canonical SMILES, InChI, or InChIKey fields after processing; records without derivable structures are either repaired or flagged for removal.
- Downstream adduct repair succeeds on ≥99.98% of records with derived SMILES (indicating usable structure annotations for mass shift validation).
- Output SMILES are RDKit-parseable and conform to SMILES syntax; round-trip validation (SMILES → canonical SMILES → InChI) produces identical InChIKey.

## Limitations

- PubChem reference database does not contain all compounds (e.g., rare metabolites, custom syntheses, trade-name mixtures); canonicalization fails silently for ~27.6% of spectra when compound names are non-standard or absent.
- Canonical SMILES derivation cannot detect wrong chemical annotations that are consistent with the measured mass; incorrect annotations will propagate as valid records.
- InChIKey-based comparison is sensitive to stereochemistry and charge state; isomeric compounds or salt/neutral forms may produce different InChIKeys despite identical connectivity.
- Performance depends on PubChem query latency and availability; batch processing of large libraries (500K+ spectra) may require 6–8 hours for a typical pipeline run.

## Evidence

- [abstract] SMILES, InChI and InChIKey are loaded by RDKit and compared to each other: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] This filter derives the canonical SMILES, InChI and InChIKey from PubChem: "This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [abstract] For 27.6% of spectra, SMILES could not be derived from compound name; of annotated spectra (72.4%), 1.62% had different 2D structure: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [discussion] Wrong chemical annotations consistent with measured mass will go unnoticed in current pipeline: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline."
- [abstract] Repair adduct and parent mass based on SMILES filter did not derive adduct for 0.02%; of 99.98%, 0.024% had incorrect adduct: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
