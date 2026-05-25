---
name: metadata-validation-cross-check
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to cross-validate computed chemical properties such as monoisotopic mass, adduct, and structure identifiers derived from SMILES or compound names against metadata fields in mass spectral library records.
when_to_use_negative:
- Spectrum records lack SMILES or compound name metadata to begin with — use basic metadata harmonization or manual curation first.
- The repair filter did not run (e.g., 'repair_smiles_of_salts' was skipped) — cross-validation assumes an upstream repair step has been applied.
- Input is already a curated, externally-validated library with known-good annotations — validation is redundant and adds computational cost.
edam_operation: http://edamontology.org/operation_3096
edam_topics:
- http://edamontology.org/topic_0625
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: Framework for loading, filtering, and validating mass spectral library records; provides filter objects (e.g., repair_smiles_of_salts, repair_adduct_and_parent_mass_based_on_smiles) whose outputs are cross-checked.
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Parses SMILES strings and computes monoisotopic mass for direct comparison against parent_mass metadata field.
- name: PubChem
  role: Source of canonical SMILES, InChI, and InChIKey used in 'derive_annotation_from_compound_name' filter; outputs are validated against spectrum metadata.
provenance:
  source_task_ids:
  - task_004
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/metadata-validation-cross-check/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/metadata-validation-cross-check/skill.md
    merged_at: '2026-05-25T07:15:30.869703+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/metadata-validation-cross-check@sha256:35b212bf448852ed71ed8860896c053d7a4c324e2058951cd7364e5ab35e5ad1
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# metadata-validation-cross-check

## Summary

Cross-validate computed chemical properties (monoisotopic mass, adduct, structure identifiers) derived from SMILES or compound names against their corresponding metadata fields in mass spectral library records. This skill detects inconsistencies that would silently corrupt library curation, enabling targeted repair before removal.

## When to use

Apply this skill when you have repaired or derived SMILES, InChI, or InChIKey from metadata (e.g., via PubChem lookup or salt-splitting) and need to verify that the resulting chemical properties match the existing parent_mass, adduct, or annotation fields. Specifically use it after running repair filters like 'repair_smiles_of_salts', 'derive_annotation_from_compound_name', or 'repair_adduct_and_parent_mass_based_on_smiles' to catch mismatches that indicate either successful repair or persistent errors requiring manual review.

## When NOT to use

- Spectrum records lack SMILES or compound name metadata to begin with — use basic metadata harmonization or manual curation first.
- The repair filter did not run (e.g., 'repair_smiles_of_salts' was skipped) — cross-validation assumes an upstream repair step has been applied.
- Input is already a curated, externally-validated library with known-good annotations — validation is redundant and adds computational cost.

## Inputs

- mass spectral records with SMILES or compound name metadata (matchms Spectrum objects or equivalent)
- repaired or newly derived SMILES strings (from salt-splitting, PubChem lookup, or InChI conversion)
- parent_mass and adduct metadata fields in spectrum records
- reference monoisotopic mass values (computed from SMILES via RDKit)

## Outputs

- validation report with counts of: successful matches, mismatches, missing parent_mass fields, and missing adduct assignments
- flagged spectra with discrepancy details (expected vs. observed monoisotopic mass, adduct mismatch codes)
- summary statistics on repair success rate (% of repaired spectra with now-matching metadata)

## How to apply

Parse the repaired SMILES (or derived InChI/InChIKey) using RDKit to compute monoisotopic mass and extract structural properties. Compare each computed value against the corresponding metadata field (parent_mass, adduct, or canonical SMILES). Flag mismatches as separate categories: (1) spectra where repair succeeded and values now align; (2) spectra where values still diverge despite repair (indicating data quality issues or ambiguous compound names); (3) spectra with missing metadata fields that cannot be validated. Aggregate counts and discrepancy summaries into a structured report. The rationale is that wrong chemical annotations consistent with measured mass will otherwise go unnoticed; this cross-check surfaces silent failures before they propagate into curated libraries.

## Related tools

- **matchms** (Framework for loading, filtering, and validating mass spectral library records; provides filter objects (e.g., repair_smiles_of_salts, repair_adduct_and_parent_mass_based_on_smiles) whose outputs are cross-checked.) — https://github.com/matchms/matchms
- **RDKit** (Parses SMILES strings and computes monoisotopic mass for direct comparison against parent_mass metadata field.)
- **PubChem** (Source of canonical SMILES, InChI, and InChIKey used in 'derive_annotation_from_compound_name' filter; outputs are validated against spectrum metadata.)

## Evaluation signals

- Percentage of repaired spectra for which computed monoisotopic mass matches parent_mass (target: >99.97% based on article results; threshold depends on mass tolerance, typically ±0.01 Da).
- Count of spectra with missing parent_mass or adduct metadata before and after repair; repair success is demonstrated by closing these gaps.
- Mismatch report shows no new inconsistencies introduced by repair — i.e., spectra that matched before repair still match after.
- Discrepancy categories are clearly labeled (e.g., '52,084 spectra repaired and now validated' vs. 'X spectra still mismatched despite repair').
- Validation summary includes both aggregate statistics and a subset of example spectra for spot-checking (especially those in the 'still mismatched' category).

## Limitations

- The skill assumes SMILES parsing and monoisotopic mass calculation via RDKit are correct; errors in RDKit or malformed SMILES will propagate into false negatives.
- Mass tolerance and adduct assignment logic must be pre-defined; the skill does not infer appropriate thresholds from data. The article does not specify exact tolerance; practitioners must set it based on instrument accuracy.
- Cross-validation cannot detect wrong chemical annotations that are consistent with the measured parent mass — these will pass all checks but may be chemically incorrect. Future work is needed to validate fragments against annotations.
- The skill operates on metadata only and does not check fragmentation patterns; spectra with correct metadata but incorrect or missing peaks will not be caught.
- Processing large libraries (e.g., GNPS 500,569 spectra) is computationally intensive; the article reports 6 h 45 min for the full cleaning pipeline on a single machine.

## Evidence

- [other] repair_smiles_of_salts filter successfully repaired metadata of 52,084 spectra by removing salt notation: "The repair_smiles_of_salts filter successfully repaired metadata of 52,084 spectra by removing salt notation and matching the resulting SMILES monoisotopic mass to the parent_mass field"
- [discussion] Current publicly available libraries often have incorrect or incomplete metadata and lack plausibility checks: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments."
- [discussion] Wrong chemical annotations consistent with measured mass will go unnoticed: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline."
- [abstract] The 'Repair adduct and parent mass based on SMILES' filter had 0.02% with no derived adduct and 0.024% with incorrect adduct: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
- [abstract] RDKit is used to load and compare SMILES, InChI and InChIKey: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] Structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization: "structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
