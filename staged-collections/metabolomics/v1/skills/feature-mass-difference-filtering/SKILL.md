---
name: feature-mass-difference-filtering
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to remove features whose m/z exceeds the parent pesticide m/z by more than +50 u, reducing false positives in automated metabolite screening workflows.
when_to_use_negative:
- Input features have not yet undergone blank subtraction and isotope/adduct removal; apply those filters first to avoid filtering artifacts.
- Analysis goal is to detect phase II conjugation metabolites (e.g., glucuronide or sulfate conjugates); this filter explicitly removes them.
- Parent pesticide m/z value is unknown or unreliable; mass difference filtering requires accurate reference ion mass.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3172
tools:
- name: incubatoR workflow (Rscripts/metabolites.R)
  role: Implements mass difference filtering as step 3 in automated pesticide metabolite detection; applies +50 u threshold and outputs filtered feature list
  repo: https://github.com/chufz/incubatoR
- name: R v3.6.1
  role: Execution environment for mass difference filtering calculations
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1021/acs.analchem.1c00972
    title: Improving the Screening Analysis of Pesticide Metabolites in Human Biomonitoring by Combining High-Throughput <i>In Vitro</i> Incubation and Automated LC–HRMS Data Processing
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/pesticide_full_2026-05-10_v2/skills/feature-mass-difference-filtering/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/feature-mass-difference-filtering/skill.md
    merged_at: '2026-05-25T07:04:57.581827+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/feature-mass-difference-filtering@sha256:d6335957f4759baed8514b62a96b86089a71c66ca379caca6455700ddf86d225
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# feature-mass-difference-filtering

## Summary

Remove features whose m/z exceeds the parent pesticide m/z by more than +50 u, as these are more likely to originate from phase II conjugation reactions rather than true phase I metabolites. This filtering step reduces false positives in automated metabolite screening workflows by eliminating features corresponding to additions of more than three oxygen atoms.

## When to use

Apply this filter after abundance filtering (fold change >4, detected in ≥2 of 3 replicates) and mass defect filtering when screening for pesticide metabolites in LC–HRMS data. Use it when the analysis goal is to prioritize phase I metabolic transformations (oxidation, reduction, bond cleavage) and exclude phase II conjugation products, or when the biological relevance of putative metabolites requires discrimination between simple transformation and complex conjugation.

## When NOT to use

- Input features have not yet undergone blank subtraction and isotope/adduct removal; apply those filters first to avoid filtering artifacts.
- Analysis goal is to detect phase II conjugation metabolites (e.g., glucuronide or sulfate conjugates); this filter explicitly removes them.
- Parent pesticide m/z value is unknown or unreliable; mass difference filtering requires accurate reference ion mass.

## Inputs

- Feature table (TSV or RData format) with m/z, retention time, and intensity per feature
- Parent pesticide m/z value (neutral mass or [M+H]+ or [M−H]− adduct)

## Outputs

- Filtered feature table (TSV or RData format) with features exceeding +50 u mass difference removed
- Visualization (PNG) of mass difference distribution before and after filtering (e.g., MDF.png)

## How to apply

Calculate the nominal mass difference (Δm/z in u) between each remaining feature's m/z value and the parent pesticide's [M+H]+ (or [M−H]− for negative mode) ion m/z. Remove all features with Δm/z > +50 u, since this corresponds to addition of more than three oxygen atoms and is characteristic of conjugation reactions (e.g., glucuronidation, sulfation) rather than phase I metabolism. Apply this threshold after blank subtraction, isotope/adduct removal, and abundance filtering, but before molecular formula assignment and spectral extraction. The threshold of +50 u is calibrated for typical pesticide metabolic profiles and can be adjusted if the workflow is adapted for more or less strict feature prioritization.

## Related tools

- **incubatoR workflow (Rscripts/metabolites.R)** (Implements mass difference filtering as step 3 in automated pesticide metabolite detection; applies +50 u threshold and outputs filtered feature list) — https://github.com/chufz/incubatoR
- **R v3.6.1** (Execution environment for mass difference filtering calculations)

## Evaluation signals

- Number of features before and after filtering; expect ~10–30% reduction depending on parent compound and metabolic profile
- Δm/z distribution histogram: all remaining features should cluster ≤ +50 u relative to parent ion m/z
- Mass difference plot visualization (MDF.png) confirms no features plotted above +50 u threshold
- Retained features correspond to known phase I metabolites (oxidation, reduction, dehydration) when compared to literature or BioTransformer predictions
- Feature count and composition remain consistent across replicates after filtering

## Limitations

- Threshold of +50 u is empirically calibrated for this dataset and may not generalize to all pesticides or conjugation pathways; some genuine phase I metabolites with mass shifts near +50 u may be excluded.
- Does not account for isotope patterns or instrument mass calibration drift, which can shift observed m/z by ±5–10 ppm; apply mass calibration before filtering.
- Assumes parent pesticide ion form ([M+H]+ or [M−H]−) is known and accurately specified; incorrect parent m/z leads to systematic filtering errors.
- Cannot distinguish between conjugation and multiple consecutive oxidation events; a feature with Δm/z = +64 u (four oxygens) could theoretically be two consecutive hydroxylations rather than conjugation.
- Some predicted metabolites matching BioTransformer output were not detected in this study, possibly due to low ionization efficiency or extraction losses rather than true absence; filtering by mass difference alone does not resolve these detection limitations.

## Evidence

- [methods] Mass difference filtering rationale: "all features with a mass difference higher than +50 u to the parent compound, corresponding to an addition of three O atoms, were also not further evaluated."
- [methods] Workflow placement and integration: "The application of a blank subtraction combined with isotope/adduct peak removal steps reduced the number of peaks by about 60% in both ESI+ and ESI−."
- [other] Biological rationale: phase I vs. phase II: "Features with m/z values exceeding the parent pesticide by more than +50 u are more likely to originate from conjugation reactions (beyond phase I oxidation, reduction, or bond cleavage)."
- [readme] Automated workflow implementation: "Filtering of non-metabolic features by several cut-off values and plotting for manual evaluation by `Rscripts/metabolites.R`"
- [discussion] Adaptability of filtering thresholds: "The individual filtering steps provided in this workflow can be adapted for a more or less strict prioritization of features"
