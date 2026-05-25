---
name: monoisotopic-mass-calculation-from-smiles
description: Use when calculating the exact monoisotopic mass of a chemical structure from its SMILES representation in the domain of metabolomics using RDKit, applying it to validate and correct parent mass metadata in tandem mass spectrometry library records.
when_to_use_negative:
- SMILES is invalid, malformed, or cannot be parsed by RDKit; skip mass calculation for that spectrum and flag it for manual curation.
- Parent mass metadata is missing or marked as unknown; monoisotopic mass calculation alone cannot fill the gap without external reference data.
- Input is already a validated, high-confidence parent mass from direct precursor m/z measurement (e.g., from high-resolution MS1 calibration); calculation is redundant and risks overwriting trusted values.
edam_operation: http://edamontology.org/operation_0235
edam_topics:
- http://edamontology.org/topic_0218
- http://edamontology.org/topic_3172
tools:
- name: RDKit
  role: Parses SMILES strings and computes exact monoisotopic mass of molecular structures for validation against metadata parent_mass fields
- name: matchms
  role: Provides spectrum data structure and integrates monoisotopic mass calculation into repair filters (repair_parent_mass_is_molar_mass, repair_smiles_of_salts, repair adduct and parent mass based on SMILES)
  repo: https://github.com/matchms/matchms
- name: matchms 0.26.4
  role: Specific version used in the library cleaning pipeline that implements salt-splitting and parent mass repair workflows relying on RDKit monoisotopic mass calculation
- name: PubChem
  role: External reference source for canonical SMILES and structure data used to validate and correct annotations before monoisotopic mass calculation
provenance:
  source_task_ids:
  - task_005
  - task_004
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
merged_aliases:
- monoisotopic-mass-calculation-from-structure
schema_version: 0.2.0
merged_alias_records:
- alias: monoisotopic-mass-calculation-from-structure
  slug: monoisotopic-mass-calculation-from-structure
  jaccard_score: 0.6
  method: token-set-jaccard
  decision: needs_review
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/monoisotopic-mass-calculation-from-smiles/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/monoisotopic-mass-calculation-from-smiles/skill.md
    merged_at: '2026-05-25T07:33:56.280588+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/monoisotopic-mass-calculation-from-smiles@sha256:4a2a0813fcbe9e0f7a35196fee6c3c75ab912524986a004650c1d1ebb2fa5948
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# Monoisotopic mass calculation from SMILES

## Summary

Calculate the exact monoisotopic mass of a chemical structure from its SMILES representation using RDKit, enabling validation and correction of parent mass metadata in tandem mass spectrometry library records. This skill is essential for detecting and repairing metadata errors where parent mass was incorrectly derived from molar mass instead of monoisotopic mass.

## When to use

Apply this skill when you have SMILES strings in spectrum metadata and need to verify or correct parent_mass fields, especially after salt-splitting repairs or when validating whether annotated structures are consistent with observed precursor m/z values. Use it as part of library cleaning workflows to identify spectra where parent_mass may have been computed from molar mass (a common mistake) rather than monoisotopic mass, or to validate repaired SMILES after removing salt notation.

## When NOT to use

- SMILES is invalid, malformed, or cannot be parsed by RDKit; skip mass calculation for that spectrum and flag it for manual curation.
- Parent mass metadata is missing or marked as unknown; monoisotopic mass calculation alone cannot fill the gap without external reference data.
- Input is already a validated, high-confidence parent mass from direct precursor m/z measurement (e.g., from high-resolution MS1 calibration); calculation is redundant and risks overwriting trusted values.

## Inputs

- SMILES string (from spectrum metadata)
- Parent mass metadata field (numeric, observed or claimed parent m/z)
- Spectrum records in matchms format or equivalent (containing both SMILES and parent_mass fields)

## Outputs

- Calculated monoisotopic mass (numeric, exact mass)
- Mass validation result (match/mismatch flag)
- Corrected parent_mass value (numeric, if repair applied)
- Audit table with spectrum_id, original_parent_mass, computed_monoisotopic_mass, SMILES, and correction status

## How to apply

Parse the SMILES string using RDKit to instantiate the molecular structure. Call RDKit's monoisotopic mass calculation (e.g., Descriptors.MonoisotopicMass or similar mass property) to obtain the exact mass based on the most abundant isotope of each element. Compare the computed monoisotopic mass against the parent_mass field in the spectrum metadata; flag spectra where the values differ significantly (beyond instrument mass accuracy tolerance, typically <5 ppm for high-resolution instruments). Use this comparison within the repair pipeline to correct parent_mass values and prevent the removal of otherwise valid spectra from library curation. Document the original and corrected mass values alongside the SMILES for audit trails.

## Related tools

- **RDKit** (Parses SMILES strings and computes exact monoisotopic mass of molecular structures for validation against metadata parent_mass fields)
- **matchms** (Provides spectrum data structure and integrates monoisotopic mass calculation into repair filters (repair_parent_mass_is_molar_mass, repair_smiles_of_salts, repair adduct and parent mass based on SMILES)) — https://github.com/matchms/matchms
- **matchms 0.26.4** (Specific version used in the library cleaning pipeline that implements salt-splitting and parent mass repair workflows relying on RDKit monoisotopic mass calculation)
- **PubChem** (External reference source for canonical SMILES and structure data used to validate and correct annotations before monoisotopic mass calculation)

## Evaluation signals

- Computed monoisotopic mass falls within instrument mass accuracy tolerance (e.g., <5 ppm) of the parent_mass field for valid annotations; significant deviations (>10 ppm) flag potential molar-mass confusion or structural errors.
- RDKit successfully parses the input SMILES without errors or warnings; unparseable SMILES are logged and excluded from mass comparison.
- Corrected parent_mass values derived from monoisotopic mass calculation restore consistency between annotation and observed precursor m/z, preventing false removal of spectra during library curation.
- Comparison of corrected values against original parent_mass shows systematic pattern (e.g., original values ~1.0005× computed mass, indicating molar-mass confusion) consistent with the article's finding that this was a common mistake.
- All spectrum records in the output audit table have non-null computed_monoisotopic_mass and validation status; no silent failures or missing calculations.

## Limitations

- RDKit monoisotopic mass calculation assumes the SMILES is chemically valid and correctly represents the neutral parent compound; errors in SMILES notation (e.g., incorrect valence, misplaced charges, or salt inclusion) propagate to incorrect mass values.
- Calculation provides the exact mass of the neutral molecule; it does not account for in-source ionization, adduct formation, or isotope patterns observed in the MS experiment, which may differ from the neutral monoisotopic mass.
- The skill cannot detect wrong chemical annotations that happen to be consistent with the measured parent m/z; as noted in the article, 'Wrong chemical annotations that are consistent with the measured mass…will go unnoticed in the current pipeline.'
- Monoisotopic mass alone is insufficient to validate annotations if multiple isomers or constitutional isomers have identical monoisotopic masses; additional structure comparison (e.g., InChI, InChIKey) or fragment matching is required.
- Performance on very large libraries (e.g., 500,000+ spectra) depends on RDKit parsing speed; the article reports 6 hours 45 minutes for the full GNPS cleaning pipeline, meaning per-spectrum overhead is small but cumulative at scale.

## Evidence

- [abstract] Repair parent mass is molar mass field. A common mistake is that the parent mass is calculated from the molar mass instead of the monoisotopic mass: "Repair parent mass is molar mass field. A common mistake is that the parent mass is calculated from the molar mass instead of the monoisotopic mass"
- [other] The repair_smiles_of_salts filter successfully repaired metadata of 52,084 spectra by removing salt notation and matching the resulting SMILES monoisotopic mass to the parent_mass field: "The repair_smiles_of_salts filter successfully repaired metadata of 52,084 spectra by removing salt notation and matching the resulting SMILES monoisotopic mass to the parent_mass field"
- [abstract] SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] Repair adduct and parent mass based on SMILES: "Repair adduct and parent mass based on SMILES"
- [discussion] Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline.: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline."
