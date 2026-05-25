---
name: mass-spectrometry-molecular-formula-assignment
description: Use when assigning molecular formulas to high-resolution LC–HRMS metabolite features by applying GenForm to MS1 m/z values and tandem MS2 spectra, constrained by parent pesticide elemental composition rules and validated through MS2 fragment explainability and in silico fragmentation prediction.
when_to_use_negative:
- Input features already have validated reference spectra or confirmed structural identifications (use instead for confirmation or structure refinement).
- MS2 spectra are missing or of poor quality (low signal, sparse fragments); GenForm requires informative fragmentation patterns to constrain formula space.
- Parent pesticide elemental composition is unknown or highly ambiguous; the fuzzy formula constraint is essential to avoid combinatorial explosion of candidates.
edam_operation: http://edamontology.org/operation_3632
edam_topics:
- http://edamontology.org/topic_0625
- http://edamontology.org/topic_3370
tools:
- name: GenForm
  role: command-line tool for calculating molecular formulas from MS1 m/z and MS2 spectra, constrained by fuzzy formula; outputs scored candidate formulas and fragment explainability
- name: Sirius version 4.4.27
  role: in silico fragmentation and molecular fingerprint prediction for resolving ambiguous formulas; examines fragmentation trees and functional group assignments
- name: mzR
  role: extraction of cleaned MS2 spectra and associated metadata from data-dependent MS2 acquisition in mzML or vendor formats
- name: OrgMassSpecR
  role: calculation of dot-product similarity scores (SpectrumSimilarity function with t=0.01, b=10) between experimental and reference MS2 spectra for confidence assessment
- name: incubatoR
  role: automated R-based workflow for feature detection, filtering, statistical prioritization, and MS2 spectrum extraction upstream of molecular formula assignment
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
    - outputs/pesticide_full_2026-05-10_v2/skills/mass-spectrometry-molecular-formula-assignment/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/mass-spectrometry-molecular-formula-assignment/skill.md
    merged_at: '2026-05-25T07:15:31.025176+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/mass-spectrometry-molecular-formula-assignment@sha256:6987ca22c32bb9242c873b4d2ec218962705f1ddfbb01d6f6f40edd55fae24a4
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# mass-spectrometry-molecular-formula-assignment

## Summary

Assignment of unambiguous molecular formulas to high-resolution LC–HRMS metabolite features by applying GenForm to MS1 m/z values and tandem MS2 spectra, constrained by parent pesticide elemental composition rules and validated through MS2 fragment explainability and in silico fragmentation prediction.

## When to use

Apply when you have isolated, prioritized metabolite features from LC–HRMS data (after blank subtraction, abundance filtering, mass defect filtering −100 to +50 mmu, and standard impurity removal) and require unambiguous molecular formula assignments to support structure elucidation and biomarker identification. Use when both high-resolution MS1 m/z and data-dependent MS2 spectra are available for the same features, and the parent compound elemental composition is known (e.g., pesticide formula).

## When NOT to use

- Input features already have validated reference spectra or confirmed structural identifications (use instead for confirmation or structure refinement).
- MS2 spectra are missing or of poor quality (low signal, sparse fragments); GenForm requires informative fragmentation patterns to constrain formula space.
- Parent pesticide elemental composition is unknown or highly ambiguous; the fuzzy formula constraint is essential to avoid combinatorial explosion of candidates.

## Inputs

- prioritized metabolite features (m/z and retention time)
- extracted MS2 spectra (tandem mass spectra in .txt or mzML format)
- MS1 m/z values at high resolution (HRMS, ≤8 ppm accuracy)
- parent pesticide molecular formula (elemental composition as string)
- reference MS2 spectra (MassBank or generated standards)

## Outputs

- assigned molecular formulas (unambiguous: one formula per feature)
- GenForm output (.out files) with scored candidate formulas
- cleaned MS2 spectra (fragments explained by assigned formula only)
- Sirius fragmentation trees and molecular fingerprint predictions
- dot-product similarity scores between experimental and reference spectra
- structured metabolite annotations with identification confidence level (** unambiguous structure, * formula only)

## How to apply

Extract MS2 spectra for prioritized metabolite features from data-dependent acquisition using mzR. Supply GenForm with (1) MS1 m/z value at ≤8 ppm accuracy, (2) full MS2 spectrum, and (3) a fuzzy formula (FF) constraint derived from the parent pesticide elemental composition (e.g., C 0−X_C H 0−∞ N 0−X_N O 0−(X_O +3) P 0−X_P S 0−X_S F 0−X_F Cl 0−X_Cl Br 0−X_Br, allowing systematic expansion from parent atoms). GenForm outputs candidate formulas; filter by removing any formula that cannot explain observed MS2 fragments (i.e., retain only peaks with calculated m/z ≤15 ppm deviation). For ambiguous or complex spectra with multiple candidate formulas, apply Sirius 4.4.27 in silico fragmentation and molecular fingerprint prediction, examining fragmentation trees for parent pesticide-like fragments and functional group assignments. Validate selected formula by calculating dot-product similarity (OrgMassSpecR SpectrumSimilarity, t=0.01, b=10) between observed and reference spectra (from MassBank or incubation controls) to assess spectral quality and confidence.

## Related tools

- **GenForm** (command-line tool for calculating molecular formulas from MS1 m/z and MS2 spectra, constrained by fuzzy formula; outputs scored candidate formulas and fragment explainability)
- **Sirius version 4.4.27** (in silico fragmentation and molecular fingerprint prediction for resolving ambiguous formulas; examines fragmentation trees and functional group assignments)
- **mzR** (extraction of cleaned MS2 spectra and associated metadata from data-dependent MS2 acquisition in mzML or vendor formats)
- **OrgMassSpecR** (calculation of dot-product similarity scores (SpectrumSimilarity function with t=0.01, b=10) between experimental and reference MS2 spectra for confidence assessment)
- **incubatoR** (automated R-based workflow for feature detection, filtering, statistical prioritization, and MS2 spectrum extraction upstream of molecular formula assignment) — https://github.com/chufz/incubatoR

## Evaluation signals

- GenForm assigns exactly one unambiguous molecular formula (no ties or multiple top-scored candidates) for each prioritized feature.
- All peaks in the observed MS2 spectrum can be explained by the assigned formula (i.e., calculated fragment m/z values match observed peaks within ≤15 ppm or tool tolerance); cleaned spectrum contains only explicable fragments.
- Dot-product similarity score between experimental MS2 and reference spectrum ≥0.5–0.7 (article context: t=0.01, b=10 parameters); scores <0.5 indicate poor spectral match and require re-evaluation or Sirius fragmentation analysis.
- For Sirius-validated formulas, fragmentation tree contains parent pesticide-characteristic fragments or expected Phase I metabolic modifications (e.g., hydroxylation, dehydrogenation, cleavage); functional group assignments are consistent with known pesticide metabolism pathways.
- Assigned formulas are consistent with parent pesticide elemental composition constraints (e.g., no more O atoms added than chemically plausible for Phase I metabolism; Cl/Br/F counts do not exceed parent formula counts unless justified).

## Limitations

- GenForm may generate multiple candidate formulas for low-resolution or sparse MS2 spectra; fuzzy formula constraints must be carefully tuned to avoid both over-restriction and over-permissiveness.
- MS2 fragmentation patterns for some metabolites (e.g., those formed by reduction, consecutive hydroxylations, or weak bond breaking) may not be well-represented in reference libraries or Sirius training data, leading to ambiguous or incorrect formula assignments.
- Some metabolites predicted by computational tools (e.g., BioTransformer) or literature sources may not be detectable in vitro due to low ionization efficiencies, sample extraction losses, or incomplete metabolic coverage in the S9 incubation assay; assigned formulas reflect only detected features.
- Unambiguous molecular formula assignment alone does not constitute full structure elucidation; multiple isomers or regio-/stereoisomers may share the same formula. Confirmation requires reference standards, 2D NMR, or high-resolution MS/MS fragmentation analysis.
- GenForm MS2 acceptance threshold (acc=8 ppm) and rejection threshold (rej=15 ppm) are empirically tuned; altered thresholds may affect formula scoring and require re-validation.

## Evidence

- [methods] By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI− for the 22 pesticides.: "By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI− for the 22 pesticides."
- [methods] The corresponding molecular formula was calculated using the GenForm33 command line tool.: "The corresponding molecular formula was calculated using the GenForm33 command line tool."
- [methods] all spectra corresponding to the metabolite features were extracted from the data-dependent MS2 acquisition using mzR.32: "all spectra corresponding to the metabolite features were extracted from the data-dependent MS2 acquisition using mzR.32"
- [methods] structure elucidation was performed using the in silico fragmentation and molecular fingerprint prediction of Sirius version 4.4.27.14: "structure elucidation was performed using the in silico fragmentation and molecular fingerprint prediction of Sirius version 4.4.27.14"
- [methods] Dot-product scores were calculated using the function SpectrumSimilarity in OrgMassSpecR.34: "Dot-product scores were calculated using the function SpectrumSimilarity in OrgMassSpecR.34"
- [readme] Molecular formula annotation - implementation of GenForm [6] (`bash/jobsubmit_6genform.sh` for parallel job submission). **INPUT:** `class.csv`, `compound/MSMS/*`, `compound/MSMS/*/MS1.txt`, `FF_compound.txt`, `parameter_genform.sh`, `globalvar.sh` **OUTPUT:** `compound/MSMS/*/*.out` `compound/MSMS/*/Clean_*.txt`: "Molecular formula annotation - implementation of GenForm [6] (`bash/jobsubmit_6genform.sh` for parallel job submission). **INPUT:** `class.csv`, `compound/MSMS/*`, `compound/MSMS/*/MS1.txt`,"
- [methods] For mass defect filtering, features with a mass defect shift of <−100 and >+50 mmu were removed.: "For mass defect filtering, features with a mass defect shift of <−100 and >+50 mmu were removed."
- [readme] `compound/MSMS/*/Clean_*.txt`: Spectra only containing the fragments that can be explained by the given formula: "`compound/MSMS/*/Clean_*.txt`: Spectra only containing the fragments that can be explained by the given formula"
