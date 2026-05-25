---
name: chemical-structure-consistency-checking
description: Validate the internal consistency of chemical structure annotations (SMILES, InChI, InChIKey) in mass spectral library entries using RDKit to detect and report mismatches. This skill is essential for identifying annotated spectra with conflicting or corrupted structure metadata that would otherwise propagate errors through downstream analysis.
when_to_use_negative:
- Input spectra lack any chemical structure annotation fields (SMILES, InChI, InChIKey); the skill cannot validate what is not present.
- Your goal is to filter on mass accuracy or spectral similarity alone; structure consistency is orthogonal to these signals.
- You are working with experimental (unannotated) spectra; this skill applies only to annotated library data.
edam_operation: http://edamontology.org/operation_3961
edam_topics:
- http://edamontology.org/topic_0218
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3407
tools:
- name: matchms
  role: Framework that orchestrates the require_valid_annotation filter and hosts the RDKit-backed consistency validation logic; version 0.26.4 or later required
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Cheminformatics engine that parses SMILES, derives canonical InChI and InChIKey, and performs field-to-field comparison to detect structure inconsistencies
- name: PubChem
  role: Reference source for canonical SMILES, InChI, and InChIKey used in derive_annotation and repair operations upstream of consistency validation
provenance:
  source_task_ids:
  - task_006
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/chemical-structure-consistency-checking/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/chemical-structure-consistency-checking/skill.md
    merged_at: '2026-05-25T07:15:30.845069+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/chemical-structure-consistency-checking@sha256:f69938338d83de9b0eabf9889324d630924578341eb990b22a51b78cf50ef2bf
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# chemical-structure-consistency-checking

## Summary

Validate the internal consistency of chemical structure annotations (SMILES, InChI, InChIKey) in mass spectral library entries using RDKit to detect and report mismatches. This skill is essential for identifying annotated spectra with conflicting or corrupted structure metadata that would otherwise propagate errors through downstream analysis.

## When to use

Apply this skill when ingesting annotated mass spectral libraries (e.g., GNPS, MoNA, Massbank, NIST) that contain SMILES, InChI, or InChIKey fields, and you need to quantify how many spectra have internally inconsistent or missing structure annotations before proceeding with library-wide analyses or curation. This is especially important after repair operations, where you want to verify that repaired annotations now pass consistency checks.

## When NOT to use

- Input spectra lack any chemical structure annotation fields (SMILES, InChI, InChIKey); the skill cannot validate what is not present.
- Your goal is to filter on mass accuracy or spectral similarity alone; structure consistency is orthogonal to these signals.
- You are working with experimental (unannotated) spectra; this skill applies only to annotated library data.

## Inputs

- GNPS mass spectral library (or equivalent public/private library: MoNA, Massbank, NIST) in matchms-compatible format
- Spectra metadata including SMILES, InChI, and InChIKey annotation fields

## Outputs

- List of spectra passing consistency validation
- List of spectra failing consistency validation, categorized by failure mode (missing field, unparseable field, mismatched field pair)
- Structured report (CSV or JSON) with row counts, removal counts, and per-criterion fractions

## How to apply

Load spectra from the mass spectral library into matchms. For each spectrum with annotation fields, use RDKit to independently parse the SMILES, InChI, and InChIKey, then cross-validate them: RDKit can derive a canonical InChI and InChIKey from the SMILES and compare these to the stored InChI and InChIKey fields; any mismatch flags the spectrum as inconsistent. Record whether each field is missing, present but invalid (RDKit cannot parse it), or present and consistent. Count and categorize spectra passing all checks, failing on missing fields, and failing on inconsistency; generate a structured report (CSV/JSON) with total counts, fractions, and per-criterion breakdowns. Typical threshold: a spectrum is retained only if all three fields are present and mutually consistent; if any field is absent or inconsistent, the spectrum is marked for removal or repair.

## Related tools

- **matchms** (Framework that orchestrates the require_valid_annotation filter and hosts the RDKit-backed consistency validation logic; version 0.26.4 or later required) — https://github.com/matchms/matchms
- **RDKit** (Cheminformatics engine that parses SMILES, derives canonical InChI and InChIKey, and performs field-to-field comparison to detect structure inconsistencies)
- **PubChem** (Reference source for canonical SMILES, InChI, and InChIKey used in derive_annotation and repair operations upstream of consistency validation)

## Evaluation signals

- Retention rate matches expected plausibility: e.g., in GNPS, 'require_valid_annotation' alone removed 16.8% (83,843 spectra); after repair, only 6.4% (31,758) were removed, confirming that consistency checks are catching repairable annotation issues.
- Per-criterion breakdown in output report is consistent with library characteristics: e.g., missing fields, unparseable SMILES, and InChI–InChIKey mismatches are reported in separate counters.
- All spectra marked as 'passing' should have SMILES, InChI, and InChIKey fields that round-trip through RDKit without error or value change (i.e., derived InChI from SMILES matches stored InChI).
- Removal counts sum correctly: total input spectra = retained + (missing field) + (unparseable field) + (inconsistent pairs).
- If repair functions were run before consistency checking, removal rate should drop significantly (as seen in GNPS: 83,843 → 31,758 after repair), indicating that the filter is correctly identifying spectra benefiting from prior repair.

## Limitations

- The current consistency check does not detect wrong chemical annotations that are structurally valid (e.g., isomers, tautomers, or different compounds with the same neutral mass). Only internal SMILES–InChI–InChIKey consistency is validated; semantic correctness cannot be inferred from structure alone.
- The skill cannot detect errors in precursor m/z, adduct, or parent mass that are independent of the chemical structure annotation; additional plausibility checks considering measured fragment ions are not yet implemented in matchms.
- InChIKey collisions (rare but possible) are not addressed; two different compounds can theoretically map to the same InChIKey, so this field alone is insufficient for uniqueness.
- Performance scales linearly with library size (e.g., GNPS 500,569 spectra took ~6 h 45 min for full pipeline including other filters); very large or resource-constrained environments may require batching or sampling.

## Evidence

- [abstract] RDKit-based validation of SMILES, InChI, InChIKey consistency: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] Require_valid_annotation filter removes 83,843 spectra (16.8%) due to inconsistency; reduced to 31,758 (6.4%) after repair: "a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084"
- [methods] The skill identifies both missing and inconsistent annotation fields: "require_valid_annotation filter, which uses RDKit to load SMILES, InChI, and InChIKey and cross-validate their internal consistency"
- [discussion] Wrong annotations that are chemically plausible pass through current validation: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline"
