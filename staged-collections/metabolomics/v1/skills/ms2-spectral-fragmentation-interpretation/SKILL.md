---
name: ms2-spectral-fragmentation-interpretation
description: Use when interpreting MS2 fragmentation spectra in metabolomics to assign molecular formulas and elucidate metabolite structures by combining GenForm formula calculation with Sirius in silico fragmentation analysis and dot-product similarity scoring against reference spectra.
when_to_use_negative:
- Input MS2 spectra contain primarily noise or exhibit poor signal-to-noise ratio; Sirius and GenForm require interpretable fragment patterns.
- Features have already been structurally confirmed by authentic reference standards or orthogonal techniques; re-interpretation adds no value.
- MS1 mass accuracy is worse than 8 ppm or MS2 resolution is insufficient to resolve isobaric fragments; GenForm and Sirius will produce unreliable or ambiguous formulas.
edam_operation: http://edamontology.org/operation_3632
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3172
tools:
- name: GenForm
  role: Command-line tool for calculating molecular formulas from MS1 m/z and MS2 spectra, constrained by parent compound elemental composition; outputs unambiguous formula assignments and explains MS2 peak origins.
- name: Sirius version 4.4.27
  role: In silico fragmentation and molecular fingerprint prediction tool for structure elucidation of ambiguous or complex fragmentation patterns; generates fragmentation trees and identifies parent pesticide-like fragments and functional groups.
- name: OrgMassSpecR
  role: R package providing SpectrumSimilarity function for calculating dot-product similarity scores between experimental and reference MS2 spectra; assesses spectral quality and confidence in formula assignments.
- name: mzR
  role: R package for extracting MS2 spectra corresponding to prioritized metabolite features from data-dependent acquisition in mzML or vendor-native formats.
- name: incubatoR
  role: R/bash workflow pipeline integrating XCMS, CAMERA, statistical filtering, and GenForm/Sirius execution for automated pesticide metabolite identification from LC-HRMS data.
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
    - outputs/pesticide_full_2026-05-10_v2/skills/ms2-spectral-fragmentation-interpretation/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/ms2-spectral-fragmentation-interpretation/skill.md
    merged_at: '2026-05-25T07:33:56.458309+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/ms2-spectral-fragmentation-interpretation@sha256:1afff755c8c270d206121002ffddf414c26bf69d6a9ccaab440485ab534b53a9
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# MS2 Spectral Fragmentation Interpretation

## Summary

Interpret MS2 fragmentation spectra to assign unambiguous molecular formulas and elucidate metabolite structures by combining GenForm formula calculation with Sirius in silico fragmentation analysis and dot-product similarity scoring against reference spectra. This skill distinguishes true metabolite fragments from unexplainable peaks and validates spectral quality.

## When to use

Apply this skill when you have extracted MS2 spectra from data-dependent acquisition for prioritized metabolite features (after filtering and statistical prioritization) and need to assign molecular formulas constrained by the parent compound's elemental composition, or when fragmentation patterns are ambiguous and require structure elucidation to distinguish between candidate isomers or functional group assignments.

## When NOT to use

- Input MS2 spectra contain primarily noise or exhibit poor signal-to-noise ratio; Sirius and GenForm require interpretable fragment patterns.
- Features have already been structurally confirmed by authentic reference standards or orthogonal techniques; re-interpretation adds no value.
- MS1 mass accuracy is worse than 8 ppm or MS2 resolution is insufficient to resolve isobaric fragments; GenForm and Sirius will produce unreliable or ambiguous formulas.

## Inputs

- Extracted MS2 spectra from data-dependent acquisition (mzML or text format)
- MS1 m/z values for prioritized metabolite features
- Parent pesticide molecular formula and elemental composition constraints
- Reference MS2 spectra (from MassBank or in-house library)

## Outputs

- Assigned unambiguous molecular formulas (GenForm .out files)
- Cleaned MS2 spectra containing only explicable fragments
- Sirius fragmentation trees and molecular fingerprint predictions
- Dot-product similarity scores and spectral quality assessment
- Structure elucidation proposals with functional group assignments

## How to apply

First, extract MS2 spectra corresponding to prioritized metabolite features from data-dependent acquisition using mzR. Second, apply GenForm command-line tool to calculate molecular formulas from MS1 m/z and MS2 spectra, constraining elemental compositions based on parent pesticide formula (e.g., C 0−X C H 0−∞ N 0−X N O 0−(X O +3) P 0−X P S 0−X S F 0−X F Cl 0−X Cl Br 0−X Br, with GenForm intensity weighting set to 'sqrt', MS1 accuracy to 8 ppm, acceptance of MS2 peaks at 8 ppm, and rejection at 15 ppm). Third, filter by removing MS2 peaks that cannot be explained by the assigned formula, retaining only explicable fragments. Fourth, for features with ambiguous or complex fragmentation patterns, perform structure elucidation using Sirius version 4.4.27 in silico fragmentation and molecular fingerprint prediction, examining fragmentation trees for parent pesticide-like fragments and functional group assignments. Fifth, calculate dot-product similarity scores between experimental and reference spectra using OrgMassSpecR SpectrumSimilarity function (with t=0.01, b=10) to assess spectral quality and confidence in the assigned formula.

## Related tools

- **GenForm** (Command-line tool for calculating molecular formulas from MS1 m/z and MS2 spectra, constrained by parent compound elemental composition; outputs unambiguous formula assignments and explains MS2 peak origins.)
- **Sirius version 4.4.27** (In silico fragmentation and molecular fingerprint prediction tool for structure elucidation of ambiguous or complex fragmentation patterns; generates fragmentation trees and identifies parent pesticide-like fragments and functional groups.)
- **OrgMassSpecR** (R package providing SpectrumSimilarity function for calculating dot-product similarity scores between experimental and reference MS2 spectra; assesses spectral quality and confidence in formula assignments.)
- **mzR** (R package for extracting MS2 spectra corresponding to prioritized metabolite features from data-dependent acquisition in mzML or vendor-native formats.)
- **incubatoR** (R/bash workflow pipeline integrating XCMS, CAMERA, statistical filtering, and GenForm/Sirius execution for automated pesticide metabolite identification from LC-HRMS data.) — https://github.com/chufz/incubatoR

## Evaluation signals

- GenForm successfully assigns unambiguous molecular formulas (no ambiguous/multiple assignments) for the prioritized features, constrained by parent pesticide elemental composition rules.
- All MS2 fragments in cleaned spectra are explicable by the assigned molecular formula; no unexplained peaks remain after GenForm filtering.
- Dot-product similarity score between experimental and reference spectra is ≥0.7 or meets journal/lab acceptance threshold, indicating high spectral quality and confidence.
- Sirius fragmentation trees contain parent pesticide-like fragments or functionally plausible neutral losses; proposed structures pass chemical reasonableness checks.
- Assigned metabolite formulas and structures are consistent with literature data or BioTransformer predictions (validation against EFSA registration dossiers or metabolite databases).

## Limitations

- Some predicted metabolites may not be detected due to low ionization efficiencies or losses during sample extraction/cleanup, leading to incomplete metabolite coverage even with correct formula assignment.
- S9 in vitro incubation does not cover all potential or existing metabolites; metabolites formed by reduction reactions (dehydrogenation), consecutive hydroxylations, or weak bond breaking may not be captured.
- Fragmentation patterns for structurally similar isomers may be indistinguishable by MS2 alone; Sirius fingerprint predictions can improve confidence but do not guarantee unique structure assignment without orthogonal data.
- GenForm performance depends on MS1 and MS2 accuracy; mass defect shifts outside the optimized range (−100 to +50 mmu for pesticide metabolites) reduce formula assignment success.
- For compounds with complex or atypical fragmentation (e.g., fipronil, where only fipronil-sulfone was detected despite six literature metabolites), MS2 interpretation may fail to identify all true metabolites.

## Evidence

- [methods] MS2 spectra interpretation for formula assignment
- [methods] Filtered MS2 spectra containing only explicable fragments
- [methods] Sirius in silico fragmentation and fingerprint prediction
- [methods] Dot-product similarity scoring for spectral quality
- [methods] GenForm elemental composition constraints from parent pesticide
- [methods] Mass defect filtering removes out-of-range metabolites before formula assignment
- [supplementary] GenForm parameters for MS1 and MS2 accuracy in supplementary
- [discussion] Incomplete metabolite coverage due to ionization or extraction limitations
- [readme] incubatoR README: GenForm applied to extracted MSMS spectra: "Molecular formula annotation - implementation of GenForm [6] (`bash/jobsubmit_6genform.sh` for parallel job submission). INPUT: `class.csv`, `compound/MSMS/*`, `compound/MSMS/*/MS1.txt`,"