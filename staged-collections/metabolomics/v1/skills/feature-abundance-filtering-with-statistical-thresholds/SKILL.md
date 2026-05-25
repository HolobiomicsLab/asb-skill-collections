---
name: feature-abundance-filtering-with-statistical-thresholds
description: Filter LC–HRMS metabolomics feature tables by applying fold-change thresholds and replication criteria to remove background noise and prioritize genuine metabolite features. This skill combines abundance-based statistical filtering with biological replication requirements to reduce false positives in untargeted screening of pesticide metabolites.
when_to_use_negative:
- Input feature table already contains only manually curated or literature-validated metabolites; statistical filtering is redundant.
- Sample set lacks ≥2 biological replicates per treatment group; the replication criterion cannot be applied and false-positive rate will increase.
- Target analytes are suspected to be low-abundance biomarkers with expected FC < 4; this threshold will exclude true signals.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0625
- http://edamontology.org/topic_3370
tools:
- name: XCMS
  role: Feature detection, alignment, and retention time correction upstream of abundance filtering; outputs peaklist and metadata tables consumed by statistical filtering
- name: CAMERA
  role: Componentization and annotation of isotopic and adduct peaks before abundance filtering; removes redundant features
- name: R (v3.6.1)
  role: Statistical computing environment for calculating fold-change, applying cutoff thresholds, and generating diagnostic plots
  repo: https://github.com/chufz/incubatoR
- name: incubatoR
  role: Automated R workflow implementing abundance filtering (Rscripts/statistics.R and Rscripts/metabolites.R) with fold-change and replication cutoffs on XCMS/CAMERA outputs
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
    - outputs/pesticide_full_2026-05-10_v2/skills/feature-abundance-filtering-with-statistical-thresholds/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/feature-abundance-filtering-with-statistical-thresholds/skill.md
    merged_at: '2026-05-25T07:15:31.017850+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/feature-abundance-filtering-with-statistical-thresholds@sha256:810881633b4a7700612f3c34cb942098d3e5b33c4782bade27e176e807670a5a
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# feature-abundance-filtering-with-statistical-thresholds

## Summary

Filter LC–HRMS metabolomics feature tables by applying fold-change thresholds and replication criteria to remove background noise and prioritize genuine metabolite features. This skill combines abundance-based statistical filtering with biological replication requirements to reduce false positives in untargeted screening of pesticide metabolites.

## When to use

Apply this skill after blank subtraction and isotope/adduct removal when you have a blank-corrected feature table from LC–HRMS analysis with replicated samples (≥2 replicates per treatment group). Use it when you need to distinguish pesticide metabolites from background features by requiring both a minimum fold-change between incubated and negative-control samples AND detection consistency across biological replicates, typically in high-throughput in vitro metabolism studies.

## When NOT to use

- Input feature table already contains only manually curated or literature-validated metabolites; statistical filtering is redundant.
- Sample set lacks ≥2 biological replicates per treatment group; the replication criterion cannot be applied and false-positive rate will increase.
- Target analytes are suspected to be low-abundance biomarkers with expected FC < 4; this threshold will exclude true signals.

## Inputs

- blank-subtracted feature table (tab-separated format: m/z @ retention time, intensity per sample)
- sample class assignment file identifying incubated replicates, negative controls, and reference standards
- parent pesticide m/z values and retention times for each compound

## Outputs

- filtered feature table containing only features meeting FC > 4 and ≥2/3 replicate criteria
- metabolite priority list (peakids: mass@rt) with fold-change and replication annotations
- visualization plots (fold-change scatter, volcano plot) for manual evaluation

## How to apply

Calculate fold-change (FC) for each feature by dividing the mean intensity of the incubated replicate group by the mean intensity of negative control samples (e.g., S9 + NADPH only) using FC = (∑intensity_replicate / n_replicate) / (∑intensity_control / n_control). Retain only features with FC > 4. Further filter to keep only features detected in at least 2 of 3 biological replicates per pesticide compound. Remove features from structurally similar pesticide groups (e.g., atrazine, terbuthylazine, terbutryn) that may share metabolites and cause false exclusions in the control group. Output the reduced feature table. This combination of thresholds typically reduces feature count by ~60% while enriching for true metabolites over instrumental and procedural artifacts.

## Related tools

- **XCMS** (Feature detection, alignment, and retention time correction upstream of abundance filtering; outputs peaklist and metadata tables consumed by statistical filtering)
- **CAMERA** (Componentization and annotation of isotopic and adduct peaks before abundance filtering; removes redundant features)
- **R (v3.6.1)** (Statistical computing environment for calculating fold-change, applying cutoff thresholds, and generating diagnostic plots) — https://github.com/chufz/incubatoR
- **incubatoR** (Automated R workflow implementing abundance filtering (Rscripts/statistics.R and Rscripts/metabolites.R) with fold-change and replication cutoffs on XCMS/CAMERA outputs) — https://github.com/chufz/incubatoR

## Evaluation signals

- Feature count reduction by ~60% compared to blank-subtracted input table, consistent with literature examples
- All retained features show FC ≥ 4 (mean intensity in incubated replicates / mean intensity in negative controls); verify via fold-change scatter plot (diffplot.png)
- All retained features are present in ≥ 2 of 3 biological replicates for their respective pesticide; check peaklist metadata and EIC extraction success rate
- Volcano plot shows retained features cluster in the high fold-change, low p-value quadrant; absence of high-intensity features in blanks or reference standards
- Metabolite count per pesticide is biologically plausible (typically 1–10 metabolites per parent compound in 3 h S9 incubation); cross-check against literature or BioTransformer predictions

## Limitations

- FC > 4 threshold is generic and may not suit all compound classes; low-abundance metabolites with FC < 4 or weakly ionizing compounds will be excluded regardless of biological relevance.
- Replication requirement (≥2/3) assumes balanced, replicated sample design; missing or failed replicates reduce statistical power and may exclude real metabolites.
- Cannot distinguish true metabolites from standard impurities or co-incubating structurally similar pesticides without additional filtering (e.g., mass defect, mass difference criteria); removal of atrazine/terbuthylazine/terbutryn cluster must be done manually to avoid false exclusion in controls.
- In vitro S9 metabolism does not recapitulate all mammalian Phase I and Phase II modifications; some predicted or literature metabolites may not be formed or detected despite correct parameters (e.g., reduction reactions, consecutive hydroxylations, hydrophilic conjugates with low ionization efficiency).
- Low ionization efficiency or sample losses during extraction/cleanup can suppress detection of real metabolites below the FC threshold; integration of complementary methods (e.g., pH-dependent ionization, targeted SRM) recommended for validation.

## Evidence

- [methods] fold_change_formula: "We used a generic cutoff value of >4 for the fold change and kept only the features that were detected in at least two of three replicates"
- [methods] blank_subtraction_workflow: "The application of a blank subtraction combined with isotope/adduct peak removal steps reduced the number of peaks by about 60% in both ESI+ and ESI−."
- [methods] structural_group_removal: "Features from structurally similar pesticide groups (atrazine, terbuthylazine, terbutryn) that may share metabolites to avoid false exclusions in the control group"
- [readme] automated_workflow_implementation: "Filtering of non-metabolic features by several cut-off values and plotting for manual evaluation by Rscripts/metabolites.R"
- [discussion] variable_strictness_flexibility: "The individual filtering steps provided in this workflow can be adapted for a more or less strict prioritization of features"
