---
name: fold-change-calculation-from-replicate-intensities
description: Use when calculating fold-change (FC) values in metabolomics by dividing mean intensity of pesticide-incubated replicate groups by mean intensity of negative control samples, applying FC > 4 threshold and presence in ≥2 of 3 replicates to filter features in LC–HRMS metabolite screening.
when_to_use_negative:
- Input feature table lacks biological replicates (n < 2) or has no negative control group (e.g., S9 + NADPH only samples).
- Feature intensities have not been blank-subtracted or isotope/adduct-annotated; applying FC filter to raw data will inflate false positives.
- Study design does not include in vitro incubation or metabolite discovery; FC filtering is optimized for xenobiotic biotransformation assays, not general metabolomics screening.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0625
- http://edamontology.org/topic_3172
tools:
- name: R v 3.6.1
  role: Statistical computation and fold-change arithmetic; used in the automated incubatoR workflow to calculate mean intensities, FC values, and replicate-based filtering
  repo: https://github.com/chufz/incubatoR
- name: Rvolcano v 1.0
  role: Robust visualization of log2 fold-change against p-value; detects outliers and produces volcano plots for manual evaluation of FC thresholds
  repo: https://github.com/chufz/incubatoR
- name: XCMS v 3.8
  role: Upstream feature detection, alignment, and retention time correction that produces the intensity matrix required as input for FC calculation
- name: CAMERA v 1.40
  role: Upstream feature componentization and grouping (isotopes, adducts) that precedes blank subtraction and FC filtering
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
    - outputs/pesticide_full_2026-05-10_v2/skills/fold-change-calculation-from-replicate-intensities/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/fold-change-calculation-from-replicate-intensities/skill.md
    merged_at: '2026-05-25T07:15:31.033785+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/fold-change-calculation-from-replicate-intensities@sha256:ccbba5b780b8a414c69d59bdec92fb6d75b13fa6faaf5526bf3ed10516591626
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# fold-change-calculation-from-replicate-intensities

## Summary

Calculate fold-change (FC) values by dividing mean intensity of pesticide-incubated replicate groups by mean intensity of negative control samples (S9 + NADPH only), then apply FC > 4 threshold combined with presence in ≥2 of 3 replicates to filter features in LC–HRMS metabolite screening. This abundance filter reduces false positives and prioritizes reproducible metabolic signals.

## When to use

When you have a blank-subtracted LC–HRMS feature table with intensity values for multiple biological replicates of pesticide-incubated samples and corresponding negative control samples (S9 + NADPH), and you need to distinguish genuine metabolite features from noise or contamination by requiring both statistical fold-enrichment (FC > 4) and reproducible detection across replicates (≥2 of 3).

## When NOT to use

- Input feature table lacks biological replicates (n < 2) or has no negative control group (e.g., S9 + NADPH only samples).
- Feature intensities have not been blank-subtracted or isotope/adduct-annotated; applying FC filter to raw data will inflate false positives.
- Study design does not include in vitro incubation or metabolite discovery; FC filtering is optimized for xenobiotic biotransformation assays, not general metabolomics screening.

## Inputs

- blank-subtracted feature table (mzML or feature matrix format with intensity values)
- replicate group assignment metadata (pesticide incubation vs. negative control labels)
- intensity values for each feature across ≥3 biological replicates and control samples

## Outputs

- fold-change filtered feature table (subset of input with FC > 4 and ≥2/3 replicate detection)
- fold-change values per feature (numeric, log2 or linear scale)
- feature prioritization report (e.g., diffplot.png, volcano plot showing FC vs. p-value)

## How to apply

Load the blank-subtracted feature table. For each feature, calculate mean intensity across the n=3 replicate measurements of the pesticide-incubated group and across the negative control group using the formula FC = (∑(I_replicate)/n_replicate) / (∑(I_control)/n_control). Retain only features with FC > 4. Cross-reference against replicate detection: keep features that appear in at least two of the three biological replicates per pesticide. Remove features from structurally similar pesticide groups (e.g., atrazine, terbuthylazine, terbutryn) that may share metabolites and cause false exclusions in the control group. Output the reduced feature table containing only features meeting both FC and replication criteria; this step typically reduces feature count by ~60% relative to the blank-subtracted input.

## Related tools

- **R v 3.6.1** (Statistical computation and fold-change arithmetic; used in the automated incubatoR workflow to calculate mean intensities, FC values, and replicate-based filtering) — https://github.com/chufz/incubatoR
- **Rvolcano v 1.0** (Robust visualization of log2 fold-change against p-value; detects outliers and produces volcano plots for manual evaluation of FC thresholds) — https://github.com/chufz/incubatoR
- **XCMS v 3.8** (Upstream feature detection, alignment, and retention time correction that produces the intensity matrix required as input for FC calculation)
- **CAMERA v 1.40** (Upstream feature componentization and grouping (isotopes, adducts) that precedes blank subtraction and FC filtering)

## Evaluation signals

- Fold-change values are consistent across replicates: mean(FC_replicate_i) should vary by <25% between any two replicates from the same pesticide-control pair.
- Feature count reduction is ~60%: the number of features in the FC-filtered output should be approximately 40% of the input feature count from the blank-subtracted table.
- Retained features show detection in ≥2 of 3 replicates: 100% of output features must have presence calls (non-zero or above LOD intensity) in at least 2 of the 3 replicate injections per pesticide.
- No features from structurally similar pesticide groups appear in the negative control: cross-check metabolites from atrazine, terbuthylazine, and terbutryn groups against S9 + NADPH blanks; overlap indicates possible false exclusions requiring manual review.
- Diffplot and volcano plot visualization show clear separation: FC > 4 features should cluster in the upper-right quadrant (high log2 FC, low p-value), visually confirming the threshold is neither too strict nor too lenient.

## Limitations

- FC threshold (>4) is generic and may be too strict for low-abundance metabolites or too lenient for high-background samples; the README acknowledges that individual filtering steps can be adapted for more or less strict prioritization.
- Replication-based filtering (≥2 of 3 replicates) assumes uniform sampling and may exclude genuine metabolites that form stochastically in only 1 or 2 replicates, especially for low-ionization-efficiency products.
- Method does not detect metabolites present in negative controls at similar intensity; compounds that are present in blanks or controls will be incorrectly filtered out, requiring separate curation.
- FC calculation assumes no missing data and equal injection volume/sample normalization across replicates; systematic variation in MS sensitivity across runs can inflate or deflate FC estimates.
- Some predicted metabolites cannot be detected despite formation due to low ionization efficiencies or losses during extraction/cleanup, reducing true positive rate of the filtered metabolite set.
- The approach is optimized for S9 liver enzyme incubation metabolite screening; applicability to other in vitro or in vivo incubation modes is not validated in the article.

## Evidence

- [methods] fold-change calculation formula and threshold application: "We used a generic cutoff value of >4 for the fold change and kept only the features that were detected in at least two of three replicates"
- [methods] blank-subtracted input and FC calculation methodology: "Mean intensity values in the samples were compared to the injection and sample blanks. Features with a higher mean intensity in the blanks were removed."
- [methods] quantitative reduction in feature count from FC and replication filtering: "The application of a blank subtraction combined with isotope/adduct peak removal steps reduced the number of peaks by about 60% in both ESI+ and ESI−."
- [other] replicate-level detection requirement and filtering rationale: "FC = (∑(I_replicate)/n_replicate) / (∑(I_control)/n_control). 2. Select all features with FC > 4. 3. Retain only features detected in at least two of the three biological replicates per pesticide."
- [other] removal of shared metabolites from structurally similar pesticide groups: "Remove features from structurally similar pesticide groups (atrazine, terbuthylazine, terbutryn) that may share metabolites to avoid false exclusions in the control group."
- [discussion] adaptive tuning of filtering strictness: "The individual filtering steps provided in this workflow can be adapted for a more or less strict prioritization of features"
- [readme] implementation in R-based incubatoR workflow with statistical comparison: "Calculation of the statistical comparisson by `Rscripts/statistics.R`... Filtering of non-metabolic features by several cut-off values and plotting for manual evaluation by `Rscripts/metabolites.R`"
