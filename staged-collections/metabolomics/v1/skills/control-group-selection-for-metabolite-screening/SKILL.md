---
name: control-group-selection-for-metabolite-screening
description: Use when selecting and preparing negative control samples (S9 + NADPH without xenobiotic incubation) for fold-change calculations in untargeted LC-MS screening of pesticide metabolites to distinguish true metabolite signals from background signals and instrumental noise.
when_to_use_negative:
- If the input data consists only of a single timepoint or single biological replicate per pesticide; the control group selection method relies on at least two replicates to assess consistency.
- If negative control samples were not processed in parallel with pesticide-incubated samples in the same analytical batch; controls must be contemporaneous to account for instrumental drift and batch effects.
- If the study uses a different biotransformation system (e.g., pooled human liver S9 from a single donor, or recombinant P450 enzymes) without re-optimization of the FC threshold; the absolute fold-change threshold of >4 may require adjustment based on signal-to-noise ratio specific to that system.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0602
- http://edamontology.org/topic_3172
tools:
- name: XCMS
  role: Feature detection, alignment, and retention time correction of all LC–HRMS samples (pesticide-incubated and negative control) prior to fold-change calculation
- name: CAMERA
  role: Componentization of features (isotope and adduct grouping) to reduce redundancy and improve signal clarity before control-based fold-change filtering
- name: R v3.6.1
  role: Statistical computation environment for mean intensity calculation, fold-change computation, and generation of volcano and diff plots for visualization of control-based filtering thresholds
  repo: https://github.com/chufz/incubatoR
- name: incubatoR
  role: Automated workflow implementation that orchestrates XCMS, CAMERA, statistical comparison (fold-change calculation against negative controls), and metabolite filtering steps
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
    - outputs/pesticide_full_2026-05-10_v2/skills/control-group-selection-for-metabolite-screening/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/control-group-selection-for-metabolite-screening/skill.md
    merged_at: '2026-05-25T07:15:31.001427+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/control-group-selection-for-metabolite-screening@sha256:0069c3b7ded2ffdf9a8bed0152225305c54add67475846af6099c8edc5c76db3
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# control-group-selection-for-metabolite-screening

## Summary

Selection and preparation of negative control samples (S9 + NADPH without xenobiotic incubation) for use as the denominator in fold-change calculations during untargeted LC–HRMS screening of pesticide metabolites. Proper control definition ensures that true metabolite signals are distinguished from background signals and instrumental noise.

## When to use

When designing or executing an in vitro metabolite screening workflow using S9 liver enzyme fractions (or other biotransformation systems) in parallel incubation experiments with multiple pesticides or xenobiotics. The control group must be established before abundance filtering and fold-change calculation, and should include replicates (at minimum two or three) of the incubation matrix without the xenobiotic compound.

## When NOT to use

- If the input data consists only of a single timepoint or single biological replicate per pesticide; the control group selection method relies on at least two replicates to assess consistency.
- If negative control samples were not processed in parallel with pesticide-incubated samples in the same analytical batch; controls must be contemporaneous to account for instrumental drift and batch effects.
- If the study uses a different biotransformation system (e.g., pooled human liver S9 from a single donor, or recombinant P450 enzymes) without re-optimization of the FC threshold; the absolute fold-change threshold of >4 may require adjustment based on signal-to-noise ratio specific to that system.

## Inputs

- mzML files from negative control samples (S9 + NADPH, no xenobiotic)
- mzML files from pesticide-incubated replicate samples
- Feature table (peaklist.tsv) with intensity values for all detected m/z features across all samples
- Sample class/group assignment file (class.csv) identifying which mzML files belong to which treatment or control group
- Metadata from XCMS and CAMERA processing (xcms.rds, camera.rds)

## Outputs

- Fold-change values (FC) for each feature, calculated as ratio of mean pesticide-incubated intensity to mean negative control intensity
- Prioritized feature list filtered by FC > 4 and replicate detection criteria
- Abundance-filtered feature table (reduced by ~60% compared to blank-subtracted table)
- Volcano plot and diff plot visualizations showing fold-change thresholds and statistical significance
- Metabolites.txt file containing peak IDs (mass@rt) of features meeting FC and replication criteria

## How to apply

Prepare negative control samples by incubating the S9 enzyme preparation with NADPH cofactor under identical temperature, incubation time (e.g., 3 hours), and sample handling conditions as the pesticide-incubated replicates, but omit the xenobiotic substrate. Measure these negative controls alongside pesticide-incubated replicates in the same analytical batch using the same LC–HRMS acquisition method. After feature detection and componentization (XCMS + CAMERA), calculate mean intensity for each feature in the negative control group. For each pesticide-incubated replicate group, compute fold-change (FC) as FC = (mean intensity of pesticide-incubated replicates) / (mean intensity of negative control group). Apply a generic FC threshold of >4 and require detection in at least two of three biological replicates to prioritize true metabolite signals. Document the control group composition and incubation parameters (S9 lot, NADPH concentration, incubation time, temperature) in the analysis metadata for reproducibility and troubleshooting.

## Related tools

- **XCMS** (Feature detection, alignment, and retention time correction of all LC–HRMS samples (pesticide-incubated and negative control) prior to fold-change calculation)
- **CAMERA** (Componentization of features (isotope and adduct grouping) to reduce redundancy and improve signal clarity before control-based fold-change filtering)
- **R v3.6.1** (Statistical computation environment for mean intensity calculation, fold-change computation, and generation of volcano and diff plots for visualization of control-based filtering thresholds) — https://github.com/chufz/incubatoR
- **incubatoR** (Automated workflow implementation that orchestrates XCMS, CAMERA, statistical comparison (fold-change calculation against negative controls), and metabolite filtering steps) — https://github.com/chufz/incubatoR

## Evaluation signals

- Fold-change values are computed correctly: verify that FC = (sum of intensities in pesticide replicates / n_replicates) / (sum of intensities in negative controls / n_controls) for a spot-checked subset of features.
- Approximately 60% feature reduction is observed after applying FC > 4 and ≥2/3 replicate detection thresholds to the blank-subtracted feature table.
- Volcano plot shows clear separation between features retained (high FC, low p-value) and those filtered out (low FC or high p-value), with the FC threshold visibly marked.
- No features from the negative control group alone appear in the final prioritized metabolite list; all retained features must have higher mean intensity in pesticide-incubated samples than in controls.
- The number and identity of metabolites detected per pesticide are consistent with literature reports or BioTransformer predictions (e.g., ~two-thirds of in vitro metabolites should be reported in literature or predicted, as noted in the reference workflow).

## Limitations

- S9 incubation does not cover all potential or existing mammalian metabolites; some registered metabolites may not be formed in vitro (e.g., fipronil: 6 rat urinary metabolites reported but only fipronil-sulfone observed in S9 incubation).
- Some metabolites may be formed but not detected due to low ionization efficiencies or losses during sample extraction and cleanup; the FC filter will not recover these metabolites.
- The generic FC threshold of >4 may be suboptimal for all pesticides or biotransformation systems; compound-specific optimization may be required if background signal or enzyme activity varies substantially.
- False exclusions can occur if structurally similar pesticides (e.g., atrazine, terbuthylazine, terbutryn) share metabolites; these require manual removal from the control group or post-hoc curation.
- Incomplete replication data (e.g., one or more replicates missing or below detection threshold) will reduce statistical power to distinguish true metabolites from noise.

## Evidence

- [methods] Fold-change definition and threshold: "We used a generic cutoff value of >4 for the fold change and kept only the features that were detected in at least two of three replicates"
- [methods] Feature reduction outcome from control-based filtering: "The application of a blank subtraction combined with isotope/adduct peak removal steps reduced the number of peaks by about 60% in both ESI+ and ESI−."
- [readme] Negative control composition and incubation setup: "The sample set should contain measurements of incubated replicates of each compound, a reference standard solution, negative controls and injection/sample preparation blanks."
- [discussion] S9 incubation limitations for complete metabolite coverage: "A comparison with the literature data and metabolization prediction showed that the S9 incubation does not cover all potential or existing metabolites."
- [discussion] Incomplete metabolite detection in specific compounds: "For metazachlor, 12 mammalian metabolites are described in the registration dossier, but we only observed three in the incubation experiment."
- [other] Fold-change calculation formula and control group role: "calculate fold-change (FC) values for each feature by dividing mean intensity of each pesticide-incubated replicate group by mean intensity of negative control samples (S9 + NADPH only)"
