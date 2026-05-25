---
name: annotation-error-rate-calculation
description: Use when calculating error rates in metabolomics using LC-MS or GC-MS techniques to assess the efficacy of annotation-repair or annotation-derivation filters on mass spectral libraries.
when_to_use_negative:
- Input spectra are unannotated or lack compound name, parent mass, or adduct metadata — filter will have no reference for comparison and error rate will be meaningless.
- Filter is not applied yet — error rate calculation requires both original and filtered annotation fields; do not use this skill on unfiltered data.
- Comparison field (reference annotation) is not chemically standardized (e.g., raw user-entered SMILES with variable aromaticity) — RDKit comparison will fail or give false mismatches; canonicalize reference annotations first.
edam_operation: http://edamontology.org/operation_3096
edam_topics:
- http://edamontology.org/topic_0602
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: load, filter, and manage spectrum objects; apply annotation-derivation filters and structure comparison workflows
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: parse, canonicalize, and compare SMILES, InChI, and InChIKey; detect structural equivalence and mismatches
- name: PubChem
  role: source for canonical SMILES, InChI, and InChIKey lookup from compound names; used by 'derive_annotation_from_compound_name' filter
- name: Python
  role: scripting environment for tabular output generation, percentage calculations, and error aggregation
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
    - outputs/article_878_full_2026-05-10_v5/skills/annotation-error-rate-calculation/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/annotation-error-rate-calculation/skill.md
    merged_at: '2026-05-25T07:33:56.267314+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/annotation-error-rate-calculation@sha256:5ffb67ca31a67d4fa87b700b525758cd4bd4bdb9b7e95c2405ef9d0224bdd961
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# annotation-error-rate-calculation

## Summary

Calculate and report error rates when applying annotation-repair or annotation-derivation filters to mass spectral libraries, quantifying the proportion of spectra that could not be annotated, were left unannotated, or received structurally divergent annotations compared to originals. This skill validates filter efficacy and identifies systematic failure modes in library cleaning pipelines.

## When to use

After applying a filter that derives or repairs chemical structure annotations (SMILES, InChI, InChIKey) from metadata fields (e.g., compound name, parent mass, adduct), compare the resulting annotations against the original or reference annotations to quantify failure rates. Use this skill when you need to report reproducible, quantitative evidence of filter performance on large spectral cohorts (e.g., >10k spectra) and must distinguish between spectra that remain unannotated, could not be processed, or were assigned structurally different compounds.

## When NOT to use

- Input spectra are unannotated or lack compound name, parent mass, or adduct metadata — filter will have no reference for comparison and error rate will be meaningless.
- Filter is not applied yet — error rate calculation requires both original and filtered annotation fields; do not use this skill on unfiltered data.
- Comparison field (reference annotation) is not chemically standardized (e.g., raw user-entered SMILES with variable aromaticity) — RDKit comparison will fail or give false mismatches; canonicalize reference annotations first.

## Inputs

- mass spectral library (matchms Spectrum objects with valid original annotation, compound name, and ion-mode-matching adduct)
- filter output spectra (annotated with derived SMILES, InChI, InChIKey from PubChem or similar source)
- reference annotation field (original SMILES, InChI, or InChIKey for comparison)

## Outputs

- error-rate report (tabular: per-spectrum derivation success/failure, structural match/mismatch status)
- aggregate error statistics (percentage of spectra with failed derivation, percentage with structural mismatch among successfully annotated, percentage with matching annotations)
- filtered spectrum table (spectra grouped by outcome: unannotated, mismatch, match)

## How to apply

Load the input spectrum collection (e.g., 413,314 filtered GNPS spectra) and the filter output into matchms. Use RDKit to parse and canonicalize the derived SMILES, InChI, and InChIKey from the filter (e.g., PubChem lookup via 'derive_annotation_from_compound_name'). For each spectrum, compare the derived structure representations against the original annotation: record three non-overlapping counts: (1) spectra from which SMILES could not be derived (numerator: count where PubChem lookup failed or returned null; denominator: total input spectra); (2) spectra successfully annotated but assigned a *different* 2D structure, detected by InChIKey mismatch or RDKit canonical SMILES equivalence check (numerator: structural mismatch; denominator: successfully annotated spectra only); (3) spectra with matching annotations (success). Express each as a percentage. Document thresholds used for structural comparison (e.g., InChIKey exact match vs. Tanimoto similarity cutoff if applicable). Generate a tabular error report with per-spectrum outcomes and aggregate summary statistics.

## Related tools

- **matchms** (load, filter, and manage spectrum objects; apply annotation-derivation filters and structure comparison workflows) — https://github.com/matchms/matchms
- **RDKit** (parse, canonicalize, and compare SMILES, InChI, and InChIKey; detect structural equivalence and mismatches)
- **PubChem** (source for canonical SMILES, InChI, and InChIKey lookup from compound names; used by 'derive_annotation_from_compound_name' filter)
- **Python** (scripting environment for tabular output generation, percentage calculations, and error aggregation)

## Evaluation signals

- Percentages sum to 100% or documented category overlap (e.g., unannotated + successfully annotated = 100%; of successfully annotated, mismatch + match = 100%).
- Error rates are stable when re-run on the same input with identical filter parameters and RDKit canonicalization settings (reproducibility check).
- Per-spectrum outcome labels (derivation_success, structural_match, structural_mismatch, unannotated) are mutually exclusive or explicitly hierarchical, with no spectra missing a label.
- InChIKey or canonical SMILES comparisons agree on structural equivalence (spot-check a sample of 10–50 mismatches by visual inspection or alternative structural comparison method).
- Reported error rates align with domain expectations (e.g., <5% failed derivation for well-curated compound names; <2% structural mismatch for high-confidence reference annotations).

## Limitations

- Filter will not detect wrong chemical annotations that are consistent with measured precursor m/z — structural mismatches detected only against reference annotation, not against fragment peaks.
- PubChem lookup may fail or return ambiguous results for non-standard or proprietary compound names; derivation failure rate is sensitive to name quality and PubChem coverage.
- Structural comparison via InChIKey or canonical SMILES assumes reference annotation is correctly standardized; if reference SMILES are non-canonical or contain errors, false mismatch rates will inflate.
- For salts and adducts, SMILES repair ('Repair SMILES of salts') must be applied before comparison; raw SMILES may include counter-ions that inflate mismatch counts.
- Error rates are snapshot statistics at the time of filter application; they do not account for evolving PubChem entries or changes in matchms filter logic across versions.

## Evidence

- [abstract] For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [abstract] This filter derives the canonical SMILES, InChI and InChIKey from PubChem: "This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [abstract] SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [discussion] Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline"
- [abstract] structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization: "structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
