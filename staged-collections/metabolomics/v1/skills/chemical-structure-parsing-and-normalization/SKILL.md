---
name: chemical-structure-parsing-and-normalization
description: Use when parsing chemical structures from metadata such as SMILES, InChI, and compound names in the domain of metabolomics using RDKit and external chemical databases to normalize them to canonical forms.
when_to_use_negative:
- Input spectra lack any chemical structure metadata (SMILES, InChI, or compound name) — parsing has no source material.
- Mass spectra are experimental, unannotated data without assigned chemical identities — structure parsing requires annotation.
- The analysis goal is fragment-level validation (e.g., checking if measured peaks match predicted neutral losses) rather than precursor structure validation — use fragment matching filters instead.
edam_operation: http://edamontology.org/operation_3960
edam_topics:
- http://edamontology.org/topic_0154
- http://edamontology.org/topic_3520
tools:
- name: RDKit
  role: Parse SMILES, InChI, and InChIKey strings; compute monoisotopic mass and molecular properties from chemical structures
- name: matchms
  role: Load and manage spectrum objects with chemical structure metadata; apply repair filters (repair_smiles_of_salts, repair_adduct_and_parent_mass_based_on_smiles) to normalize structures and validate annotations
  repo: https://github.com/matchms/matchms
- name: PubChem
  role: Derive canonical SMILES, InChI, and InChIKey from compound names via lookup; serves as reference for structure canonicalization
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
    - outputs/article_878_full_2026-05-10_v5/skills/chemical-structure-parsing-and-normalization/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/chemical-structure-parsing-and-normalization/skill.md
    merged_at: '2026-05-25T07:15:30.836383+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/chemical-structure-parsing-and-normalization@sha256:eea6a61e9429e76af7f311c03ef6e4eb44a5d19c5bd2e744ae4b4262b3504e67
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# chemical-structure-parsing-and-normalization

## Summary

Parse chemical structures from metadata (SMILES, InChI, compound names) and normalize them to canonical forms using RDKit and external chemical databases. This skill is essential for validating structure annotations in mass spectral libraries and detecting mismatches between chemical identifiers.

## When to use

When a mass spectral library contains chemical structure metadata in multiple formats (SMILES, InChI, InChIKey, compound names) and you need to verify consistency across representations, derive missing identifiers from compound names, or validate that computed monoisotopic masses match the precursor mass field. Apply this skill during library curation when structural annotation is incomplete or potentially erroneous.

## When NOT to use

- Input spectra lack any chemical structure metadata (SMILES, InChI, or compound name) — parsing has no source material.
- Mass spectra are experimental, unannotated data without assigned chemical identities — structure parsing requires annotation.
- The analysis goal is fragment-level validation (e.g., checking if measured peaks match predicted neutral losses) rather than precursor structure validation — use fragment matching filters instead.

## Inputs

- mass spectral library in matchms format with SMILES, InChI, InChIKey, or compound_name metadata fields
- spectrum objects with parent_mass and precursor_mz fields
- chemical structure strings (SMILES, InChI)

## Outputs

- parsed and canonical chemical structures (normalized SMILES, InChI, InChIKey)
- computed monoisotopic mass for each structure
- validation report with mass match/mismatch counts and pass rates
- flagged spectra with structure annotation errors or inconsistencies

## How to apply

Load spectra with chemical structure metadata into matchms format. Use RDKit to parse SMILES, InChI, and InChIKey strings; PubChem's canonical lookup to derive missing identifiers from compound names (noting that ~27.6% of spectra may fail this derivation). Compute monoisotopic mass from the parsed structure using RDKit and compare against the parent_mass metadata field—mismatches indicate annotation errors or salt notation requiring repair. For salts (dot-separated SMILES like 'C1=NC2=NC=NC(=C2N1)N.Cl'), extract the neutral parent compound before mass calculation. Generate a summary report documenting derivation success rates, mass validation pass/fail counts, and structural discrepancies flagged for manual review or repair.

## Related tools

- **RDKit** (Parse SMILES, InChI, and InChIKey strings; compute monoisotopic mass and molecular properties from chemical structures)
- **matchms** (Load and manage spectrum objects with chemical structure metadata; apply repair filters (repair_smiles_of_salts, repair_adduct_and_parent_mass_based_on_smiles) to normalize structures and validate annotations) — https://github.com/matchms/matchms
- **PubChem** (Derive canonical SMILES, InChI, and InChIKey from compound names via lookup; serves as reference for structure canonicalization)

## Evaluation signals

- Monoisotopic mass computed from parsed SMILES matches the parent_mass metadata field within 5 ppm (or library-specific tolerance); document pass/fail counts.
- Canonical SMILES, InChI, and InChIKey derived from the same structure are consistent across all three representations (no round-trip parsing errors).
- For compound-name lookups: report the percentage of spectra successfully annotated (e.g., 72.4% success in article) and the percentage of successful annotations with different 2D structures (e.g., 1.62% mismatch).
- Salt-containing SMILES (dot notation) are correctly split to yield neutral parent structures with monoisotopic masses matching parent_mass (e.g., 52,084 spectra repaired in article).
- Spectra with unparseable or invalid structure strings are flagged for manual review; count and reason for each failure are documented.

## Limitations

- PubChem lookup fails for ~27.6% of compound names, leaving those spectra without derived SMILES; fallback manual curation or alternative databases may be needed.
- Canonicalization via RDKit and PubChem does not detect chemically wrong annotations if the resulting monoisotopic mass happens to match the precursor mass—structure-level validation requires fragment matching or expert review.
- Salt notation repair assumes the dominant (first) fragment in a dot-separated SMILES is the analyte; exceptions must be handled manually.
- Adduct derivation from SMILES fails for 0.02% of spectra; these require manual assignment or removal.
- Current pipeline does not validate whether measured fragments match the parsed structure—only precursor mass and adduct are checked.

## Evidence

- [abstract] SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] This filter derives the canonical SMILES, InChI and InChIKey from PubChem: "This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [abstract] For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [abstract] a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084: "the newly introduced repair functions repaired the metadata of 52,084 spectra"
- [abstract] Repair parent mass is molar mass field. A common mistake is that the parent mass is calculated from the molar mass instead of the monoisotopic mass: "the parent mass is calculated from the molar mass instead of the monoisotopic mass"
- [discussion] Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments.: "Current publicly available libraries often have incorrect or inaccuracies"
