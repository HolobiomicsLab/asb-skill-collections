---
name: spectral-library-adduct-repair-validation
description: This skill repairs adduct assignments in annotated MS/MS spectra by deriving canonical SMILES from PubChem, recalculating parent mass and adduct from chemical structure, and validates repair success against known error rates. It is essential for correcting inconsistencies between declared adducts, precursor m/z, and chemical annotations in curated spectral libraries.
when_to_use_negative:
- Input spectra lack chemical annotation (SMILES, InChI, or compound name) — the filter requires structure data to derive adducts.
- Precursor m/z or ion mode (positive/negative) metadata is missing — the filter cannot match expected adducts without observed precursor m/z.
- Input is already a fully validated and manually curated adduct table — repair is redundant and risks introducing errors.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0625
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: Framework hosting the 'repair_adduct_based_on_smiles' filter; orchestrates spectrum I/O, metadata access, and filter application
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Derives canonical SMILES, InChI, and InChIKey from chemical annotations; calculates monoisotopic mass from structure
- name: PubChem
  role: Reference database queried (via RDKit) to resolve compound names to SMILES and validate structure canonicalization
- name: Python
  role: Language for implementing the repair pipeline and error-rate statistics generation
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
    - outputs/article_878_full_2026-05-10_v5/skills/spectral-library-adduct-repair-validation/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/spectral-library-adduct-repair-validation/skill.md
    merged_at: '2026-05-25T07:15:30.872040+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/spectral-library-adduct-repair-validation@sha256:f47112cc9b6584c2cb2b0aa6db0ebc5996002df3104e96bd607c98484bd7869a
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# Spectral Library Adduct Repair and Validation

## Summary

This skill repairs adduct assignments in annotated MS/MS spectra by deriving canonical SMILES from PubChem, recalculating parent mass and adduct from chemical structure, and validates repair success against known error rates. It is essential for correcting inconsistencies between declared adducts, precursor m/z, and chemical annotations in curated spectral libraries.

## When to use

Apply this skill when your input is a set of MS/MS spectra with chemical annotations (SMILES, InChI, or compound names) where adduct assignments may be incomplete, incorrect, or inconsistent with the precursor m/z and molar mass. Specifically, when you observe mismatches between the observed precursor m/z and the expected [M+H]⁺, [M-H]⁻, or other adduct forms, or when adduct metadata is missing or uncertain for >1% of your library.

## When NOT to use

- Input spectra lack chemical annotation (SMILES, InChI, or compound name) — the filter requires structure data to derive adducts.
- Precursor m/z or ion mode (positive/negative) metadata is missing — the filter cannot match expected adducts without observed precursor m/z.
- Input is already a fully validated and manually curated adduct table — repair is redundant and risks introducing errors.

## Inputs

- MS/MS spectrum dataset in matchms format with chemical annotations (SMILES, InChI, or compound name) and declared adduct and precursor m/z
- PubChem reference database (queried during repair via RDKit)
- Monoisotopic mass or molar mass field for each spectrum

## Outputs

- Repaired spectrum dataset with corrected adduct assignments and monoisotopic parent mass
- Summary statistics report: count and percentage of spectra with no derived adduct, count and percentage with incorrect adduct among those successfully repaired
- List or flagged spectra where repair failed or disagreement exceeded tolerance

## How to apply

Load the spectrum dataset in matchms format and apply the 'repair_adduct_based_on_smiles' filter. The filter uses RDKit to derive canonical SMILES and InChIKey for each spectrum's chemical annotation (querying PubChem when needed). For each spectrum, calculate the expected precursor m/z for all common adducts ([M+H]⁺, [M-H]⁻, [M+Na]⁺, etc.) from the monoisotopic mass and compare against the observed precursor m/z within a specified tolerance (typically 5 ppm). Assign the adduct corresponding to the closest match. Separately validate that the declared molar mass is replaced with the monoisotopic mass if the two differ. Record the repair outcomes: proportion of spectra for which no adduct could be derived, proportion with a derived adduct, and proportion with an incorrect adduct (e.g., best-match adduct does not fall within mass tolerance). The target error rates are <0.02% failure to derive and <0.024% incorrect assignment among repaired spectra.

## Related tools

- **matchms** (Framework hosting the 'repair_adduct_based_on_smiles' filter; orchestrates spectrum I/O, metadata access, and filter application) — https://github.com/matchms/matchms
- **RDKit** (Derives canonical SMILES, InChI, and InChIKey from chemical annotations; calculates monoisotopic mass from structure)
- **PubChem** (Reference database queried (via RDKit) to resolve compound names to SMILES and validate structure canonicalization)
- **Python** (Language for implementing the repair pipeline and error-rate statistics generation)

## Evaluation signals

- Failure-to-derive rate is ≤0.02% (i.e., ≥99.98% of input spectra receive a derived adduct).
- Incorrect adduct rate among successfully repaired spectra is ≤0.024% (i.e., ≥99.976% of repaired spectra have an adduct consistent with observed precursor m/z within 5 ppm tolerance).
- All output spectra with a derived adduct show precursor m/z within ±5 ppm of the calculated m/z for the assigned adduct and monoisotopic mass.
- Molar mass field is replaced with monoisotopic mass where the two originally differed (spot-check 50–100 repaired spectra).
- Comparison of input vs. output adduct assignments shows 100% consistency for spectra that already had correct adducts and expected repair rate (52,084 out of ~413,314 spectra in the reference case).

## Limitations

- The filter cannot repair adduct assignments for spectra with missing or invalid chemical annotations; it will fail to derive an adduct for ~0.02% of spectra.
- Annotations that are chemically valid and consistent with the observed precursor m/z but semantically incorrect (e.g., a different isomer with the same mass) will not be detected; the filter compares only mass, not biological or chemical plausibility.
- The filter requires manual selection of ion mode (positive or negative) in advance; misclassified ion mode will lead to failed or incorrect adduct assignment.
- Common adducts are checked ([M+H]⁺, [M-H]⁻, [M+Na]⁺, etc.), but rare or exotic adducts will not be recognized if not explicitly enumerated in the filter logic.

## Evidence

- [methods] filter_repair_adduct_based_on_smiles_method: "This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [abstract] filter_repair_adduct_error_rates: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
- [abstract] adduct_repair_saves_spectra: "combined the newly introduced repair functions repaired the metadata of 52,084"
- [methods] parent_mass_monoisotopic_correction: "Repair parent mass is molar mass field. A common mistake is that the parent mass is calculated from the molar mass instead of the monoisotopic mass"
- [abstract] structure_validation_workflow: "structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
