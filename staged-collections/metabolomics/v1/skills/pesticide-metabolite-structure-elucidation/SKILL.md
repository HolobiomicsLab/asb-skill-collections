---
name: pesticide-metabolite-structure-elucidation
description: Use when conducting metabolomics to elucidate the structure of pesticide metabolites through high-resolution MS/MS fragmentation analysis, molecular formula assignment, and in silico fragmentation prediction applied to LC–HRMS data.
when_to_use_negative:
- Input features have not been filtered for mass defect (±100 mmu lower / +50 mmu upper cutoff) and abundance (fold change >4, detected in ≥2 replicates); run filtering steps first.
- No MS2 spectra are available for the feature; GenForm and Sirius require MS2 fragmentation data for formula and structure elucidation.
- The parent pesticide formula or elemental constraints are unknown or ill-defined; GenForm requires a well-specified fuzzy formula for correct molecular formula assignment.
edam_operation: http://edamontology.org/operation_3632
edam_topics:
- http://edamontology.org/topic_0153
- http://edamontology.org/topic_0943
- http://edamontology.org/topic_3375
tools:
- name: GenForm
  role: Command-line tool for molecular formula calculation from MS1 m/z and MS2 fragmentation spectra, with elemental composition constraints based on parent pesticide formula
- name: Sirius version 4.4.27
  role: In silico fragmentation and molecular fingerprint prediction for structure elucidation of ambiguous metabolites; generates fragmentation trees and functional group assignments
- name: OrgMassSpecR
  role: R package providing SpectrumSimilarity function to calculate dot-product similarity scores between experimental and reference MS2 spectra for confidence assessment
- name: mzR
  role: R package for extraction of MS2 spectra corresponding to prioritized metabolite features from data-dependent MS2 acquisition files
- name: MassBank
  role: Public spectral library providing reference MS2 spectra for dot-product similarity comparison and spectral quality validation
  repo: https://massbank.eu/MassBank
- name: incubatoR
  role: Complete R/bash workflow orchestrating XCMS, CAMERA, statistical filtering, metabolite prioritization, EIC extraction, MS/MS extraction, and GenForm molecular formula annotation
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
    - outputs/pesticide_full_2026-05-10_v2/skills/pesticide-metabolite-structure-elucidation/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/pesticide-metabolite-structure-elucidation/skill.md
    merged_at: '2026-05-25T07:04:57.604430+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/pesticide-metabolite-structure-elucidation@sha256:ada8fcc753cbd57782c27615cfa02942e50168bca0cd9f900bcda001b50c1d8f
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# pesticide-metabolite-structure-elucidation

## Summary

Structural elucidation of pesticide metabolites by combining high-resolution MS/MS fragmentation analysis, molecular formula assignment, and in silico fragmentation prediction to annotate detected metabolite features to unambiguous molecular structures or formulas. This skill assigns chemical identities to pesticide biotransformation products detected in LC–HRMS metabolomics data.

## When to use

Apply this skill when you have prioritized pesticide metabolite features (after filtering by mass defect, abundance, and standard impurity removal) with corresponding high-resolution MS1 m/z values and data-dependent MS2 spectra, and you need to move from mass-to-charge annotation to molecular formula and/or structure assignment for biomonitoring or regulatory reporting.

## When NOT to use

- Input features have not been filtered for mass defect (±100 mmu lower / +50 mmu upper cutoff) and abundance (fold change >4, detected in ≥2 replicates); run filtering steps first.
- No MS2 spectra are available for the feature; GenForm and Sirius require MS2 fragmentation data for formula and structure elucidation.
- The parent pesticide formula or elemental constraints are unknown or ill-defined; GenForm requires a well-specified fuzzy formula for correct molecular formula assignment.

## Inputs

- prioritized metabolite features (mass@rt identifiers from filtering step)
- MS1 m/z values (high-resolution, ≥5 ppm accuracy)
- data-dependent MS2 spectra (centroided, extracted via mzR)
- parent pesticide molecular formula
- reference MS2 spectra (MassBank or in-house standards)

## Outputs

- molecular formula assignments (unambiguous per feature)
- fragmentation trees with assigned functional groups
- dot-product similarity scores to reference spectra
- cleaned MS2 spectra (containing only explicable fragments)
- metabolite structures or formulas with identification confidence level (* or **)

## How to apply

Extract MS2 spectra corresponding to prioritized metabolite features from data-dependent acquisition using mzR. Apply GenForm command-line tool to calculate molecular formulas from MS1 m/z and MS2 spectra, constraining elemental compositions based on the parent pesticide formula (e.g., C 0−X C H 0−∞ N 0−X N O 0−(X O +3) P 0−X P S 0−X S F 0−X F Cl 0−X Cl Br 0−X Br). Filter generated formulas by removing MS2 peaks that cannot be explained by the assigned molecular formula, retaining only explicable fragments. For features with ambiguous or complex fragmentation patterns, perform structure elucidation using Sirius version 4.4.27 in silico fragmentation and molecular fingerprint prediction, examining fragmentation trees for parent pesticide-like fragments and functional group assignments. Calculate dot-product similarity scores between experimental MS2 spectra and reference spectra (from MassBank or generated standards) using OrgMassSpecR SpectrumSimilarity function (parameters: t = 0.01, b = 10) to assess spectral quality and confidence. Report metabolites as unambiguous structures (**) if linked to a single molecular structure, or as molecular formula only (*) if only formula assignment is achieved.

## Related tools

- **GenForm** (Command-line tool for molecular formula calculation from MS1 m/z and MS2 fragmentation spectra, with elemental composition constraints based on parent pesticide formula)
- **Sirius version 4.4.27** (In silico fragmentation and molecular fingerprint prediction for structure elucidation of ambiguous metabolites; generates fragmentation trees and functional group assignments)
- **OrgMassSpecR** (R package providing SpectrumSimilarity function to calculate dot-product similarity scores between experimental and reference MS2 spectra for confidence assessment)
- **mzR** (R package for extraction of MS2 spectra corresponding to prioritized metabolite features from data-dependent MS2 acquisition files)
- **MassBank** (Public spectral library providing reference MS2 spectra for dot-product similarity comparison and spectral quality validation) — https://massbank.eu/MassBank
- **incubatoR** (Complete R/bash workflow orchestrating XCMS, CAMERA, statistical filtering, metabolite prioritization, EIC extraction, MS/MS extraction, and GenForm molecular formula annotation) — https://github.com/chufz/incubatoR

## Evaluation signals

- GenForm output reports ≥1 unambiguous molecular formula per prioritized feature (91 formulas assigned to 82 prioritized features reported for 22 pesticides in this study).
- MS2 spectra contain ≥50% explicable fragments (fragments explained by the assigned molecular formula); cleaned spectra show retention of parent pesticide-like fragments or characteristic functional group losses.
- Dot-product similarity scores to reference MassBank spectra are ≥0.7 (threshold varies by reference quality; lower scores may indicate novel or reference-poor metabolites).
- Fragmentation trees generated by Sirius show logical metabolic transformations consistent with Phase I reactions (hydroxylation, dehydrogenation, oxidation, conjugation with loss of side chains).
- Identification level is reported as ** (unambiguous structure) for metabolites matched to reference standards or literature; * (formula only) for novel metabolites where only elemental composition is assigned.

## Limitations

- S9 liver incubation does not cover all potential or existing mammalian metabolites; for example, metazachlor incubation yielded only 3 of 12 registered mammalian metabolites, suggesting missed pathways such as consecutive hydroxylations or weak bond breaking.
- Some predicted metabolites may not be detected despite formation due to low ionization efficiencies or losses during sample extraction and cleanup, leading to incomplete metabolite inventories.
- GenForm molecular formula assignment requires MS2 fragmentation spectra; features with weak fragmentation or very simple spectra may receive ambiguous or multiple formula candidates, requiring Sirius in silico prediction and manual curation.
- Dot-product similarity scoring depends on availability of high-quality reference spectra in MassBank; novel metabolites without reference standards may have low similarity scores and reduced confidence in structure assignment.
- The accuracy of elemental composition constraints (fuzzy formula) for GenForm is critical; incorrect parent pesticide formula or overly loose/tight elemental bounds will compromise formula assignment.

## Evidence

- [methods] Extract cleaned MS2 spectra and molecular formula assignment workflow: "all spectra corresponding to the metabolite features were extracted from the data-dependent MS2 acquisition using mzR"
- [methods] GenForm formula calculation with elemental constraints: "The corresponding molecular formula was calculated using the GenForm33 command line tool"
- [methods] Fragment explicability filtering step: "Filter generated formulas by removing peaks in MS2 spectra that cannot be explained by assigned molecular formula, retaining only explicable fragments"
- [methods] Sirius in silico structure elucidation for ambiguous metabolites: "structure elucidation was performed using the in silico fragmentation and molecular fingerprint prediction of Sirius version 4.4.27"
- [methods] Dot-product similarity scoring with OrgMassSpecR: "Dot-product scores were calculated using the function SpectrumSimilarity in OrgMassSpecR"
- [methods] Quantitative outcome: 91 unambiguous formulas assigned: "By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI− for the 22 pesticides"
- [supplementary] Identification confidence levels: structure (**) vs. formula (*): "Column ID is the describing if the metabolite could be linked unambiguously to one molecular structure (**) or only to a molecular formula (*)"
- [readme] Workflow orchestration in incubatoR: steps 4–6 covering formula annotation and spectral extraction: "Molecular formula annotation - implementation of GenForm [6] (`bash/jobsubmit_6genform.sh` for parallel job submission). INPUT: `class.csv`, `compound/MSMS/*`, `compound/MSMS/*/MS1.txt`,"
- [supplementary] GenForm parameter settings for MS accuracy and fragment acceptance: "GenForm intensity weighting wi sqrt MS1 accuracy ppm 8 acceptance of MS2 peak acc 8 rejection of MS2 peak rej 15"
- [discussion] Limitation: incomplete metabolite detection for metazachlor: "For metazachlor, 12 mammalian metabolites are described in the registration dossier, but we only observed three in the incubation experiment"
