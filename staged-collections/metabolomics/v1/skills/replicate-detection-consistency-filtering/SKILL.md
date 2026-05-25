---
name: replicate-detection-consistency-filtering
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics requires filtering of LC–HRMS metabolite features based on consistent detection across biological replicates (≥2 of 3) and fold-change thresholding (FC > 4) to minimize noise and false positives.
when_to_use_negative:
- Input already has <2 biological replicates per compound (replication filter has no effect and may remove valid features arbitrarily).
- Feature table has not undergone blank subtraction and isotope/adduct removal; fold-change and replication thresholds are calibrated post-cleanup and may be miscalibrated on uncleaned data.
- Negative controls are missing or poorly matched in intensity distribution to the incubation groups (fold-change calculation will be unstable).
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0625
- http://edamontology.org/topic_3172
tools:
- name: R v 3.6.1
  role: Host language for fold-change calculation, replication counting, and feature filtering logic
  repo: https://github.com/chufz/incubatoR
- name: XCMS version 3.8
  role: Upstream peakpicking and feature detection; output feature table is input to this filtering skill
- name: CAMERA
  role: Upstream isotope and adduct annotation; output used to identify and remove isotopes/adducts before replication filtering
- name: incubatoR
  role: Automated workflow implementing replicate-detection consistency filtering as step 3 (Rscripts/metabolites.R)
  repo: https://github.com/chufz/incubatoR
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1021/acs.analchem.1c00972
    title: Improving the Screening Analysis of Pesticide Metabolites in Human Biomonitoring by Combining High-Throughput <i>In Vitro</i> Incubation and Automated LC–HRMS Data Processing
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/pesticide_full_2026-05-10_v2/skills/replicate-detection-consistency-filtering/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/replicate-detection-consistency-filtering/skill.md
    merged_at: '2026-05-25T07:15:31.029350+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/replicate-detection-consistency-filtering@sha256:a4ca82f5e18ba3b781adc8f199cd72f54fe3ab23540a56f46dc7afe758d0f871
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# replicate-detection-consistency-filtering

## Summary

Filter LC–HRMS metabolite features by requiring consistent detection across biological replicates (≥2 of 3) combined with fold-change thresholding (FC > 4) to remove noise and false positives introduced by blank subtraction and adduct/isotope removal steps. This skill reduces feature table size by ~60% while retaining biologically relevant metabolite signals.

## When to use

Apply this skill after blank subtraction and isotope/adduct peak removal when you have a feature table from replicated LC–HRMS incubation experiments (≥3 biological replicates per compound) and need to discriminate true metabolite features from background noise, especially when fold-change alone would retain spurious single-replicate detections.

## When NOT to use

- Input already has <2 biological replicates per compound (replication filter has no effect and may remove valid features arbitrarily).
- Feature table has not undergone blank subtraction and isotope/adduct removal; fold-change and replication thresholds are calibrated post-cleanup and may be miscalibrated on uncleaned data.
- Negative controls are missing or poorly matched in intensity distribution to the incubation groups (fold-change calculation will be unstable).

## Inputs

- blank-subtracted feature table (with isotope/adduct peaks removed)
- intensity matrix indexed by feature (mass@RT) and sample group
- class file mapping samples to pesticide incubation group or negative control
- list of structurally related pesticide groups to exempt from filtering

## Outputs

- reduced feature table (replicate-filtered)
- feature list containing only features with FC > 4 and ≥2/3 replicate detection
- metadata annotation flagging features passing or failing replication criterion

## How to apply

Calculate fold-change (FC) for each feature by dividing the mean intensity of the pesticide-incubated replicate group by the mean intensity of the negative control group (S9 + NADPH only); retain only features with FC > 4. Next, count detection frequency across the three biological replicates per pesticide and keep only features detected in at least two of three replicates. Remove features from structurally related pesticide groups (e.g., atrazine, terbuthylazine, terbutryn) that may share metabolites to avoid false exclusions in the control group. The rationale is that fold-change alone can inflate significance of low-abundance single-replicate noise, while replication filtering ensures robustness; the pesticide group exemption prevents over-filtering of known cross-metabolites.

## Related tools

- **R v 3.6.1** (Host language for fold-change calculation, replication counting, and feature filtering logic) — https://github.com/chufz/incubatoR
- **XCMS version 3.8** (Upstream peakpicking and feature detection; output feature table is input to this filtering skill)
- **CAMERA** (Upstream isotope and adduct annotation; output used to identify and remove isotopes/adducts before replication filtering)
- **incubatoR** (Automated workflow implementing replicate-detection consistency filtering as step 3 (Rscripts/metabolites.R)) — https://github.com/chufz/incubatoR

## Evaluation signals

- Feature count reduction: ~60% drop in number of features after application compared to blank-subtracted input (invariant observed in the article's results).
- Replication consistency: 100% of retained features must have detection in ≥2 of 3 replicates; no feature with detection in only 1 replicate should remain.
- Fold-change threshold: all retained features must have FC > 4 calculated as (mean(replicate intensities) / mean(control intensities)); no feature with FC ≤ 4 should pass.
- Metabolite coherence: retained features should cluster with predicted or literature-reported metabolites for each pesticide; extreme outliers (e.g., features >+50 mmu from parent) should be absent unless post-hoc annotated.
- Output schema validation: feature table rows contain only entries with non-null FC, replicate count ≥2, and designation as pesticide-group-exempt if applicable.

## Limitations

- FC > 4 is a generic cutoff that may over-filter pesticides with naturally low S9 metabolic conversion or under-filter highly abundant contaminants; the article notes that filtering steps 'can be adapted for a more or less strict prioritization' but does not provide per-pesticide optimization rules.
- Replication filtering assumes equal quality and completeness of all three replicates; if one replicate is systematically noisier or degraded, the 2/3 threshold may pass artifactual features from the two 'good' replicates.
- Pesticide group exemption (atrazine, terbuthylazine, terbutryn) is manually curated; unknown cross-metabolites between other pesticide pairs may still be incorrectly filtered if they appear only in controls or non-target incubations.
- The skill does not account for metabolites formed by unexpected transformations (e.g., reductions, consecutive hydroxylations, weak-bond breaking) that may not appear in all replicates if formation is stochastic or concentration-dependent.

## Evidence

- [methods] abundance_filter_definition: "We used a generic cutoff value of >4 for the fold change and kept only the features that were detected in at least two of three replicates"
- [methods] blank_subtraction_effect: "The application of a blank subtraction combined with isotope/adduct peak removal steps reduced the number of peaks by about 60% in both ESI+ and ESI−."
- [other] fold_change_calculation: "fold-change (FC) values for each feature by dividing mean intensity of each pesticide-incubated replicate group by mean intensity of negative control samples (S9 + NADPH only) using the formula FC ="
- [readme] metabolite_filtering_workflow: "Filtering of non-metabolic features by several cut-off values and plotting for manual evaluation by `Rscripts/metabolites.R`"
- [discussion] adaptive_filtering: "The individual filtering steps provided in this workflow can be adapted for a more or less strict prioritization of features"
