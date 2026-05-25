---
name: rdkit-smiles-inchi-cross-validation
description: Use when validating the internal consistency of chemical structure annotations (SMILES, InChI, and InChIKey) in mass spectral library records in the domain of metabolomics using RDKit, applying to mass spectral data from LC-MS and GC-MS untargeted lipidomics.
when_to_use_negative:
- Input library contains only a single chemical structure representation (e.g., SMILES alone) — this skill requires at least two independent representations to cross-validate.
- Spectra are already known to have been validated by a prior RDKit consistency check or by manual curation with identical stringency.
- The analysis goal is to repair broken annotations rather than identify and remove them — use repair functions ('Repair SMILES of salts', 'Repair adduct and parent mass based on SMILES') first, then apply this validation as a final gate.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0602
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: Framework that wraps RDKit validation into the 'require_valid_annotation' filter and applies it to mass spectral libraries; provides the Spectrum object model and I/O for MS/MS data.
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Molecular toolkit that loads and parses SMILES, InChI, and InChIKey; generates canonical molecular graphs to check structural consistency across representations.
  repo: https://github.com/rdkit/rdkit
- name: PubChem
  role: Reference source for canonical SMILES, InChI, and InChIKey used to derive and validate annotations.
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
    - outputs/article_878_full_2026-05-10_v5/skills/rdkit-smiles-inchi-cross-validation/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/rdkit-smiles-inchi-cross-validation/skill.md
    merged_at: '2026-05-25T07:15:30.825705+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/rdkit-smiles-inchi-cross-validation@sha256:872c136417ee9540b4972ceb246373f4eb816fe3ab76968eef2154342751eb65
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# RDKit SMILES/InChI/InChIKey Cross-Validation

## Summary

This skill validates the internal consistency of chemical structure annotations (SMILES, InChI, and InChIKey) in mass spectral library records using RDKit, identifying and removing spectra with missing or mutually inconsistent annotation fields. It is essential for ensuring that curated MS/MS libraries contain chemically coherent metadata that can reliably support downstream compound identification and structure analysis.

## When to use

Apply this skill when you have a mass spectral library with multiple chemical structure representations (SMILES, InChI, InChIKey) and need to detect spectra where these representations are absent, malformed, or internally inconsistent (e.g., SMILES and InChIKey do not correspond to the same molecular structure). This is the right choice when library quality assurance demands both detection and removal of annotation errors, and when you want to quantify how many spectra fail validation before and after repair operations.

## When NOT to use

- Input library contains only a single chemical structure representation (e.g., SMILES alone) — this skill requires at least two independent representations to cross-validate.
- Spectra are already known to have been validated by a prior RDKit consistency check or by manual curation with identical stringency.
- The analysis goal is to repair broken annotations rather than identify and remove them — use repair functions ('Repair SMILES of salts', 'Repair adduct and parent mass based on SMILES') first, then apply this validation as a final gate.

## Inputs

- Mass spectral library with annotated spectra (e.g., GNPS, MoNA, MassBank formats)
- Spectrum metadata: SMILES string, InChI string, InChIKey string for each spectrum
- matchms Spectrum objects or equivalent tabular representation

## Outputs

- Validation report (CSV or JSON) with per-spectrum pass/fail status
- Aggregated statistics: counts and fractions of spectra failing each validation checkpoint
- List of spectrum IDs or indices that failed validation and should be removed
- Final retention count and retention rate

## How to apply

Use RDKit to load and parse each spectrum's SMILES, InChI, and InChIKey fields in sequence. For each annotation triple, RDKit generates a canonical molecular graph and checks that all three representations encode the same molecular structure. Flag any spectrum that lacks one or more of these three fields as missing metadata. Flag any spectrum where RDKit cannot parse a field (malformed SMILES or InChI) or where the parsed structures do not match as inconsistent. Accumulate counts and fractions of spectra failing each checkpoint. Output a structured validation report (CSV or JSON) with total spectra processed, counts and percentages of spectra removed at each criterion (missing SMILES, missing InChI, missing InChIKey, SMILES–InChI mismatch, SMILES–InChIKey mismatch, InChI–InChIKey mismatch), and the final retention count and rate. This approach reveals both the prevalence of missing annotations and the prevalence of incorrect annotations that survived earlier curation steps.

## Related tools

- **matchms** (Framework that wraps RDKit validation into the 'require_valid_annotation' filter and applies it to mass spectral libraries; provides the Spectrum object model and I/O for MS/MS data.) — https://github.com/matchms/matchms
- **RDKit** (Molecular toolkit that loads and parses SMILES, InChI, and InChIKey; generates canonical molecular graphs to check structural consistency across representations.) — https://github.com/rdkit/rdkit
- **PubChem** (Reference source for canonical SMILES, InChI, and InChIKey used to derive and validate annotations.)

## Evaluation signals

- Spectrum count before and after validation matches reported library sizes (e.g., GNPS library before 500,569 spectra, after 448,485 spectra).
- Removal counts and percentages are consistent with documented repair efficacy; e.g., if repair functions are applied before this filter, the number of removed spectra should decrease by the sum of repaired counts.
- All three fields (SMILES, InChI, InChIKey) are present and non-empty in 100% of retained spectra.
- Spot-check retained spectra by manually verifying that RDKit can parse each annotation and that the three representations encode the same molecular structure (e.g., using RDKit's Chem.MolFromSmiles, Chem.MolFromInchi, and Descriptors.InChIKey).
- Validation report shows zero mismatches between SMILES and InChI, zero mismatches between SMILES and InChIKey, and zero mismatches between InChI and InChIKey for all retained spectra.

## Limitations

- This filter does not detect wrong chemical annotations that are consistent with the measured precursor m/z (e.g., isomers or different compounds with the same exact mass). Validation based on SMILES/InChI/InChIKey consistency alone cannot rule out chemically incorrect but structurally plausible annotations.
- RDKit may fail to parse malformed or non-standard SMILES or InChI strings, resulting in false negatives (acceptance of broken annotations) if error handling is not strict. The skill requires that RDKit's parsing throw an exception on unparseable input.
- InChIKey collisions (two different structures yielding the same InChIKey) are theoretically possible but extremely rare; this skill assumes InChIKey collisions do not occur in practice.
- The skill does not validate whether the parent mass or adduct annotations are consistent with the chemical structure; use the 'Repair adduct and parent mass based on SMILES' filter to address that separately.
- Performance on very large libraries (e.g., >500,000 spectra) is I/O and CPU bound; the GNPS library of 500,569 spectra took 6 hours 45 minutes to process through the full matchms pipeline.

## Evidence

- [methods] require_valid_annotation: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] removal counts for GNPS library: "a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed"
- [abstract] repair efficacy and cross-validation rationale: "combined the newly introduced repair functions repaired the metadata of 52,084"
- [methods] annotation consistency definition: "Require valid annotation. A spectrum is only retained if it contains all three fields (SMILES, InChI and InChIKey) and if these are internally consistent"
- [abstract] library size and processing context: "Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min"
