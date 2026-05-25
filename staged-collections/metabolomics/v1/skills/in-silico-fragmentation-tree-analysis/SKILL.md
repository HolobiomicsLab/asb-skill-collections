---
name: in-silico-fragmentation-tree-analysis
description: Use when analyzing metabolomics data through LC-MS or GC-MS untargeted lipidomics by employing in-silico fragmentation trees and molecular fingerprinting (Sirius) to clarify the structure of ambiguous metabolite features.
when_to_use_negative:
- Input MS2 spectrum is below signal-to-noise threshold (SNR < 3:1) or contains <4 diagnostic fragments — in-silico prediction becomes unreliable without sufficient experimental fragmentation data.
- Molecular formula has already been conclusively validated by high-confidence spectral matching (dot-product similarity > 0.85) to a reference standard in MassBank — further in-silico analysis adds no discriminatory value.
- The feature is known to arise from an artifact (impurity, adduct, isotope, or in-source fragmentation of the parent) — fragmentation tree analysis is misaligned with the true source.
edam_operation: http://edamontology.org/operation_3632
edam_topics:
- http://edamontology.org/topic_0153
- http://edamontology.org/topic_3375
tools:
- name: Sirius
  role: Performs in-silico fragmentation tree generation and molecular fingerprint prediction to elucidate metabolite structure from MS2 spectra and molecular formula
- name: GenForm
  role: Upstream tool that assigns molecular formulas to metabolite features; output (formula string and filtered MS2 spectrum) serves as Sirius input
- name: OrgMassSpecR
  role: Calculates dot-product similarity scores between experimental MS2 spectra and in-silico fragmentation spectra for confidence assessment
- name: mzR
  role: Extracts experimental MS2 spectra from data-dependent LC–HRMS2 acquisition (mzML format) prior to in-silico fragmentation analysis
- name: incubatoR
  role: Orchestrates the full metabolite identification workflow including in-silico fragmentation tree analysis as part of structure elucidation
  repo: https://github.com/chufz/incubatoR
provenance:
  source_task_ids:
  - task_004
  source_papers:
  - doi: 10.1021/acs.analchem.1c00972
    title: Improving the Screening Analysis of Pesticide Metabolites in Human Biomonitoring by Combining High-Throughput <i>In Vitro</i> Incubation and Automated LC–HRMS Data Processing
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/pesticide_full_2026-05-10_v2/skills/in-silico-fragmentation-tree-analysis/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/in-silico-fragmentation-tree-analysis/skill.md
    merged_at: '2026-05-25T06:57:01.619978+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/in-silico-fragmentation-tree-analysis@sha256:de1f47a3ec423e6865d2b0ae81b9f149acd2c5da724f91c6d2ee675994f611ca
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# in-silico-fragmentation-tree-analysis

## Summary

Uses computational fragmentation prediction and molecular fingerprinting (Sirius) to elucidate the structure of ambiguous metabolite features by examining in-silico fragmentation trees for diagnostic parent-like fragments and functional group assignments. This skill bridges formula assignment and structural confirmation when MS2 spectra alone are insufficient.

## When to use

Apply this skill when a metabolite feature has been assigned a molecular formula by GenForm but the MS2 fragmentation pattern is complex, ambiguous, or lacks clear diagnostic fragments that unambiguously distinguish the proposed structure. Specifically, use it after mass defect filtering (−100 to +50 mmu) and formula generation have narrowed the candidate set but fragmentation-based disambiguation is needed before spectral library inclusion.

## When NOT to use

- Input MS2 spectrum is below signal-to-noise threshold (SNR < 3:1) or contains <4 diagnostic fragments — in-silico prediction becomes unreliable without sufficient experimental fragmentation data.
- Molecular formula has already been conclusively validated by high-confidence spectral matching (dot-product similarity > 0.85) to a reference standard in MassBank — further in-silico analysis adds no discriminatory value.
- The feature is known to arise from an artifact (impurity, adduct, isotope, or in-source fragmentation of the parent) — fragmentation tree analysis is misaligned with the true source.

## Inputs

- MS2 mass spectrum (mzML or centroided text format with m/z and intensity pairs)
- Assigned molecular formula (string, e.g. 'C17H27NO3')
- Parent pesticide elemental composition constraints (e.g. C 0–20 H 0–∞ N 0–2 O 0–5)

## Outputs

- Fragmentation tree structure (Sirius tree XML or graphical representation)
- Molecular fingerprint prediction (Sirius .fpt file or class probabilities)
- Dot-product similarity score between experimental and in-silico MS2 spectra (scalar, 0–1)
- Candidate structure with confidence assessment (annotated SMILES or InChI, pass/fail)

## How to apply

Extract the MS2 spectrum and assigned molecular formula for the prioritized metabolite feature. Run Sirius version 4.4.27 with the experimental MS2 spectrum and molecular formula as input to generate an in-silico fragmentation tree and molecular fingerprint prediction. Examine the fragmentation tree for fragments consistent with the parent pesticide structure (diagnostic loss of side chains, characteristic rearrangements) and functional group annotations (e.g., hydroxyl, carbonyl, amine oxidation state changes). Cross-reference in-silico fragment masses and intensities against the experimental MS2 spectrum using dot-product similarity scoring (OrgMassSpecR SpectrumSimilarity function with default t=0.01, b=10 parameters). Retain the candidate structure only if the fragmentation tree explains ≥ 80% of major experimental peaks and functional group predictions are consistent with known pesticide metabolism (Phase I oxidations, reductions, hydroxylations). Reject candidates if in-silico and experimental fragmentation patterns are incongruent or if the fragmentation tree suggests structural transformations not supported by the parent pesticide chemistry.

## Related tools

- **Sirius** (Performs in-silico fragmentation tree generation and molecular fingerprint prediction to elucidate metabolite structure from MS2 spectra and molecular formula)
- **GenForm** (Upstream tool that assigns molecular formulas to metabolite features; output (formula string and filtered MS2 spectrum) serves as Sirius input)
- **OrgMassSpecR** (Calculates dot-product similarity scores between experimental MS2 spectra and in-silico fragmentation spectra for confidence assessment)
- **mzR** (Extracts experimental MS2 spectra from data-dependent LC–HRMS2 acquisition (mzML format) prior to in-silico fragmentation analysis)
- **incubatoR** (Orchestrates the full metabolite identification workflow including in-silico fragmentation tree analysis as part of structure elucidation) — https://github.com/chufz/incubatoR

## Evaluation signals

- Fragmentation tree contains ≥2 diagnostic fragments (mass and intensity) that match major peaks in the experimental MS2 spectrum with <5 ppm error tolerance
- Dot-product similarity score between experimental and in-silico MS2 spectra is ≥0.7 when calculated using OrgMassSpecR SpectrumSimilarity with parameters t=0.01, b=10
- Molecular fingerprint prediction from Sirius assigns high probability (>0.6) to functional groups consistent with known Phase I pesticide metabolism (e.g., hydroxylation, oxidative deamination, N-oxide formation)
- The proposed fragmentation pathway in the tree accounts for the mass difference between parent pesticide and metabolite (e.g., +16 u for hydroxylation, −2 u for dehydrogenation) by loss of/addition of explainable neutral fragments
- Manual inspection of the fragmentation tree structure shows no contradictory rearrangements (e.g., gain of mass not explained by neutral loss or radical addition) that would be inconsistent with low-energy collision-induced dissociation of a small organic molecule

## Limitations

- In-silico fragmentation prediction assumes collision-induced dissociation fragmentation mechanisms; does not model novel or unusual rearrangements unique to pesticide metabolites (e.g., consecutive hydroxylations or reduction reactions not predicted by BioTransformer).
- Sirius fingerprint prediction has lower accuracy for small fragments (<m/z 100) and for uncommon functional groups not well-represented in training data; metabolites with unusual structures (e.g., ring-opened or rearranged intermediates) may receive low confidence scores despite being correct.
- Performance degrades when MS2 spectrum has low spectral purity (contamination from co-eluting compounds) or when the actual metabolite structure is a positional isomer of the predicted structure — fragmentation trees may be identical for regioisomers.
- Not applicable to metabolites that do not fragment readily under standard LC–HRMS/MS conditions (e.g., stable conjugates, very hydrophilic compounds that evaporate inefficiently) — missing or weak MS2 spectra prevent tree generation.
- Elemental composition constraints must be correctly specified based on parent pesticide formula; if constraints are too loose or too tight, Sirius may generate false-positive or false-negative candidate structures.

## Evidence

- [methods] structure elucidation was performed using the in silico fragmentation and molecular fingerprint prediction of Sirius version 4.4.27: "structure elucidation was performed using the in silico fragmentation and molecular fingerprint prediction of Sirius version 4.4.27."
- [other] examining fragmentation trees for parent pesticide-like fragments and functional group assignments: "For features with ambiguous or complex fragmentation patterns, perform structure elucidation using Sirius version 4.4.27 in silico fragmentation and molecular fingerprint prediction, examining"
- [methods] Dot-product scores were calculated using the function SpectrumSimilarity in OrgMassSpecR: "Dot-product scores were calculated using the function SpectrumSimilarity in OrgMassSpecR."
- [methods] all spectra corresponding to the metabolite features were extracted from the data-dependent MS2 acquisition using mzR: "all spectra corresponding to the metabolite features were extracted from the data-dependent MS2 acquisition using mzR."
- [methods] The corresponding molecular formula was calculated using the GenForm command line tool.: "The corresponding molecular formula was calculated using the GenForm command line tool."
- [discussion] In vitro metabolites, which were not predicted, were mainly formed by reduction reactions (dehydrogenation), two consecutive hydroxylations or the breaking of a weak bond: "In vitro metabolites, which were not predicted, were mainly formed by reduction reactions (dehydrogenation), two consecutive hydroxylations or the breaking of a weak bond in the molecule"
