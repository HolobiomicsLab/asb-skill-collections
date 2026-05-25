---
name: spectral-metadata-annotation-mismatch-detection
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to detect mismatches between derived chemical structures (SMILES, InChI, InChIKey) and existing spectrum annotations by deriving canonical structures from compound names via PubChem lookup.
when_to_use_negative:
- Spectra lack compound names or existing structure annotations—the filter requires both to perform comparison.
- Ion mode or adduct information is incomplete or missing—the workflow filters for spectra with valid, matching adduct data before annotation derivation.
- You only need to repair missing annotations without validating existing ones; use simpler repair filters (e.g., 'Repair adduct and parent mass based on SMILES') instead.
edam_operation: http://edamontology.org/operation_3094
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: Core framework for loading spectra, applying the 'derive_annotation_from_compound_name' filter, and executing structure comparison workflows
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Canonicalizes and compares SMILES, InChI, and InChIKey structures to detect 2D structural mismatches between derived and existing annotations
- name: PubChem
  role: External reference database queried by the 'derive_annotation_from_compound_name' filter to resolve compound names to canonical SMILES, InChI, and InChIKey
- name: Python
  role: Scripting environment for orchestrating matchms filters, error rate calculations, and generating mismatch reports
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/spectral-metadata-annotation-mismatch-detection/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/spectral-metadata-annotation-mismatch-detection/skill.md
    merged_at: '2026-05-25T07:15:30.810347+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/spectral-metadata-annotation-mismatch-detection@sha256:81ca04d1d4e97615b1ba2adf49978f5a0bf65d898845104b63bfaeef19de57aa
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# Spectral Metadata Annotation Mismatch Detection

## Summary

Detect mismatches between derived chemical structures (SMILES, InChI, InChIKey) and existing spectrum annotations by deriving canonical structures from compound names via PubChem lookup and comparing them against recorded annotations. This skill identifies both unannotated spectra and spectra with incorrect or inconsistent 2D structural assignments that would otherwise propagate errors through downstream analysis.

## When to use

When you have mass spectra with both compound names and existing chemical structure annotations (SMILES, InChI, or InChIKey), and you need to validate annotation integrity across a large library. Apply this skill to detect systematic mismatches (e.g., when 1.62% of successfully annotated spectra differ from PubChem canonical structures) or to identify which spectra lack derivable annotations (e.g., when 27.6% of compound names fail to resolve to structures in PubChem).

## When NOT to use

- Spectra lack compound names or existing structure annotations—the filter requires both to perform comparison.
- Ion mode or adduct information is incomplete or missing—the workflow filters for spectra with valid, matching adduct data before annotation derivation.
- You only need to repair missing annotations without validating existing ones; use simpler repair filters (e.g., 'Repair adduct and parent mass based on SMILES') instead.

## Inputs

- Mass spectra with valid ion mode, compound name, and matching adduct information
- Spectrum metadata fields: compound_name, annotation (SMILES/InChI/InChIKey), ionmode, precursor_mz
- GNPS or similar public/private spectral library in matchms-compatible format

## Outputs

- Filtered spectrum table with derived canonical structures (SMILES, InChI, InChIKey)
- Error report quantifying failure rates (% of spectra from which SMILES could not be derived)
- Mismatch report quantifying % of annotated spectra assigned a different 2D structure
- Quality metrics: percentage of successfully derived annotations, percentage of structural conflicts

## How to apply

Load spectra with valid ion mode, compound name, and matching adduct into matchms (version 0.26.4 or later). Apply the 'derive_annotation_from_compound_name' filter, which queries PubChem to retrieve canonical SMILES, InChI, and InChIKey for each compound name. Use RDKit to canonicalize and compare the derived structures against the spectrum's existing annotation fields. Stratify results into three groups: (1) spectra for which SMILES could not be derived from the compound name (report failure rate, target ≤27.6%), (2) successfully annotated spectra with no structural mismatch (report as passing), and (3) annotated spectra assigned a different 2D structure than derived from PubChem (report mismatch rate, target ≤1.62%). Document both the filtered spectrum table and an error report quantifying these rates to enable reproducible quality assessment across library versions.

## Related tools

- **matchms** (Core framework for loading spectra, applying the 'derive_annotation_from_compound_name' filter, and executing structure comparison workflows) — https://github.com/matchms/matchms
- **RDKit** (Canonicalizes and compares SMILES, InChI, and InChIKey structures to detect 2D structural mismatches between derived and existing annotations)
- **PubChem** (External reference database queried by the 'derive_annotation_from_compound_name' filter to resolve compound names to canonical SMILES, InChI, and InChIKey)
- **Python** (Scripting environment for orchestrating matchms filters, error rate calculations, and generating mismatch reports)

## Evaluation signals

- Failure rate (% of spectra from which SMILES could not be derived from compound name) matches expected threshold (target: ≤27.6%)
- Mismatch rate among successfully annotated spectra (% assigned a different 2D structure) is within tolerance (target: ≤1.62%)
- No structural conflicts are silently dropped; all mismatches are explicitly documented in the error report with spectrum IDs and conflicting structure pairs
- Derived structures are canonical (RDKit InChIKey and canonical SMILES are identical across reruns) and traceable to PubChem source records
- Filtered spectrum table contains only spectra with valid ion mode, matching adduct, and derivable or existing annotations; removal count matches expected library reduction (e.g., GNPS: 500,569 → 448,485 spectra after full cleaning pipeline)

## Limitations

- PubChem lookup fails for 27.6% of compound names, meaning spectra with ambiguous, proprietary, or misspelled compound names cannot be validated and are marked as unannotated.
- The pipeline detects structural mismatches only when a different 2D structure is assigned; it does not identify wrong chemical annotations that are consistent with the measured precursor m/z (e.g., isomers with identical mass but different connectivity).
- Additional metadata fields such as instrument type, collision energies, and fragment-level plausibility (whether measured fragments are consistent with the annotated structure) are not yet cleaned or validated by the current matchms filters.
- Comparison relies on compound name and PubChem availability; spectra lacking compound names or drawn from libraries with inconsistent naming conventions will fail annotation derivation.

## Evidence

- [methods] derive_annotation_from_compound_name: "This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [abstract] 27.6% could not be derived; 1.62% mismatch rate: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [methods] RDKit structure comparison: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [discussion] Current libraries lack plausibility checks: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments"
- [discussion] Wrong annotations consistent with mass go unnoticed: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline"
