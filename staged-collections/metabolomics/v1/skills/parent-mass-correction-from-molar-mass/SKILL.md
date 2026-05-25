---
name: parent-mass-correction-from-molar-mass
description: Use when working in the metabolomics domain with LC-MS or GC-MS techniques to correct spectra by replacing incorrect parent mass values populated with molar mass using chemical structure information (SMILES) to derive the correct monoisotopic mass.
when_to_use_negative:
- Input spectra already have verified monoisotopic masses or have been validated against reference standards—applying this filter again risks unnecessary modification.
- No SMILES, InChI, or other chemical structure annotation is available; the filter requires structural data to calculate the correct monoisotopic mass.
- Working with experimental (unannotated) spectral data without compound identities; this repair is designed for library curation with known annotations.
edam_operation: http://edamontology.org/operation_3436
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: Core library cleaning framework; provides Spectrum objects and the repair_parent_mass_is_molar_mass filter implementation
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Parses SMILES strings and calculates theoretical monoisotopic mass for comparison and correction
- name: PubChem
  role: Source for canonical SMILES derivation when compound name is available, used upstream to ensure correct structure annotations
provenance:
  source_task_ids:
  - task_005
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/parent-mass-correction-from-molar-mass/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/parent-mass-correction-from-molar-mass/skill.md
    merged_at: '2026-05-25T07:15:30.862007+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/parent-mass-correction-from-molar-mass@sha256:09b738668aa8cccb332d9c3bc566ceb00c4fad1c5eb93325a5e19c898205c2be
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# parent-mass-correction-from-molar-mass

## Summary

This skill detects and corrects spectra where the parent mass field has been incorrectly populated with the molar mass instead of the monoisotopic mass—a common annotation error in mass spectral libraries. It uses chemical structure information (SMILES) to calculate the correct monoisotopic mass and repairs the metadata before downstream analysis.

## When to use

Apply this skill when working with annotated mass spectral library data (e.g., from GNPS, MoNA, or MassBank) where you suspect parent mass values may have been derived from molar mass rather than monoisotopic mass, particularly before structure annotation validation or before using the library for spectral matching. This is especially relevant when preparing library data for public release or quality control.

## When NOT to use

- Input spectra already have verified monoisotopic masses or have been validated against reference standards—applying this filter again risks unnecessary modification.
- No SMILES, InChI, or other chemical structure annotation is available; the filter requires structural data to calculate the correct monoisotopic mass.
- Working with experimental (unannotated) spectral data without compound identities; this repair is designed for library curation with known annotations.

## Inputs

- Annotated MS/MS spectrum objects (matchms Spectrum format) with populated parent_mass, compound_name, and SMILES or InChI fields
- SMILES string or InChI representing the compound structure

## Outputs

- Repaired spectrum objects with corrected parent_mass field (monoisotopic mass instead of molar mass)
- Audit log or report listing spectrum_id, original_parent_mass, corrected_monoisotopic_parent_mass, and SMILES used for verification

## How to apply

Load the spectrum objects into matchms (version 0.26.4 or later) and apply the 'repair_parent_mass_is_molar_mass' filter as part of the library cleaning pipeline. The filter uses the associated SMILES string to calculate the theoretical monoisotopic mass via RDKit; if the current parent_mass value is significantly closer to the molar mass than the monoisotopic mass (indicating confusion), the parent_mass field is corrected to the monoisotopic mass. Run this repair before structure annotation validation filters and before final library curation, typically as part of the 'Library cleaning' filter set which includes all default filters plus error repair. Verify correction by inspecting the original and corrected parent_mass values alongside the SMILES and confirming that the corrected value now matches the monoisotopic mass calculated from the molecular formula.

## Related tools

- **matchms** (Core library cleaning framework; provides Spectrum objects and the repair_parent_mass_is_molar_mass filter implementation) — https://github.com/matchms/matchms
- **RDKit** (Parses SMILES strings and calculates theoretical monoisotopic mass for comparison and correction)
- **PubChem** (Source for canonical SMILES derivation when compound name is available, used upstream to ensure correct structure annotations)

## Evaluation signals

- Corrected parent_mass values match the monoisotopic mass calculated from the SMILES via RDKit (difference < 0.01 Da).
- Original parent_mass value was closer to molar mass than monoisotopic mass, confirming the error condition existed.
- No spectra are flagged as corrected if parent_mass was already correct (monoisotopic mass), indicating appropriate selectivity.
- The repaired library metadata is consistent across validation filters (e.g., 'Repair adduct and parent mass based on SMILES' does not further modify parent_mass).
- Audit records show that the number of repaired spectra aligns with the expected prevalence of molar-mass confusion in the input library (historically ~1–2% of public library spectra).

## Limitations

- The repair depends on correct SMILES or InChI annotations; if the structure annotation is itself wrong, the corrected parent_mass will be wrong.
- The filter cannot distinguish between intentional molar-mass usage (e.g., for neutral loss calculations) and erroneous molar-mass assignment; manual review of a sample of corrections is recommended.
- Spectra with ambiguous or multiple structure annotations (salts, isomers) may be over- or under-corrected; preprocessing steps like 'Repair SMILES of salts' should be applied first.
- The filter does not validate that measured fragment ions actually match the corrected structure; wrong chemical annotations consistent with the measured mass may still go undetected.

## Evidence

- [methods] Repair parent mass is molar mass field. A common mistake is that the parent mass is calculated from the molar mass instead of the monoisotopic mass: "Repair parent mass is molar mass field. A common mistake is that the parent mass is calculated from the molar mass instead of the monoisotopic mass"
- [results] a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084: "a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084"
- [methods] SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [methods] structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization: "structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
- [methods] Matchms version 0.26.4 was used to run these pipelines: "Matchms version 0.26.4 was used to run these pipelines"
