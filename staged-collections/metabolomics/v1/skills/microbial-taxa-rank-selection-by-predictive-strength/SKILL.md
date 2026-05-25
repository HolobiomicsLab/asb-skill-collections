---
name: microbial-taxa-rank-selection-by-predictive-strength
description: Select the most predictive microbial taxa from mmvec conditional-probability output by ranking taxa according to their conditional probability values across all metabolites. This skill identifies the subset of microbes with the strongest quantitative associations to a curated set of metabolites, reducing noise and focusing downstream interaction analysis on taxa with robust predictive power.
when_to_use_negative:
- mmvec conditional probability output has not yet been computed—first run the mmvec neural network on your microbe and metabolite abundance tables.
- You have not yet curated or filtered metabolites to a set of interest (e.g., shared annotated metabolites)—this skill is applied *after* metabolite curation, not before.
- The analysis goal is to detect rare or low-abundance taxa; this skill specifically selects high-strength predictors and will discard rare taxa regardless of biological relevance.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0625
- http://edamontology.org/topic_3174
tools:
- name: mmvec
  role: Generates conditional probability matrices encoding the likelihood of observing each metabolite given each microbial taxon; output is filtered and ranked by this skill.
- name: QIIME2 microbe-metabolite vectors plugin
  role: Plugin interface for running mmvec within the QIIME2 framework; exports conditional probability artifact that serves as input.
- name: R
  role: Used for ranking taxa by conditional probability strength and exporting filtered results to CSV.
  repo: https://github.com/jhaffner09/core_metabolome_2021
provenance:
  source_task_ids:
  - task_004
  source_papers:
  - doi: 10.1128/msystems.00710-22
    title: Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_haffner_v2/skills/microbial-taxa-rank-selection-by-predictive-strength/SKILL.md
    - outputs/audit_haffner_v2/skills/microbial-taxa-rank-selection-by-predictive-strength/skill.md
    merged_at: '2026-05-25T07:15:30.905790+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/microbial-taxa-rank-selection-by-predictive-strength@sha256:320a107aae1cc4338925e22f709df52838355cf7d62f10779821420e281456fb
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1128/msystems.00710-22
---

# microbial-taxa-rank-selection-by-predictive-strength

## Summary

Select the most predictive microbial taxa from mmvec conditional-probability output by ranking taxa according to their conditional probability values across all metabolites. This skill identifies the subset of microbes with the strongest quantitative associations to a curated set of metabolites, reducing noise and focusing downstream interaction analysis on taxa with robust predictive power.

## When to use

After running mmvec (microbe-metabolite vectors) neural network to generate conditional probability scores, when you need to prioritize which microbial taxa to examine for mechanistic interaction with metabolites. Apply this skill when the full mmvec output contains too many taxa (e.g., hundreds of ASVs or species) and you wish to focus on the most influential members—typically when you have already filtered to a curated set of metabolites (e.g., shared annotated metabolites) and want to identify which taxa drive co-occurrence with those metabolites.

## When NOT to use

- mmvec conditional probability output has not yet been computed—first run the mmvec neural network on your microbe and metabolite abundance tables.
- You have not yet curated or filtered metabolites to a set of interest (e.g., shared annotated metabolites)—this skill is applied *after* metabolite curation, not before.
- The analysis goal is to detect rare or low-abundance taxa; this skill specifically selects high-strength predictors and will discard rare taxa regardless of biological relevance.

## Inputs

- mmvec conditional probability matrix (rows: annotated metabolites, columns: all microbial taxa; format: CSV or QIIME2 artifact)
- metadata specifying number of top taxa to retain (e.g., 27)

## Outputs

- Filtered conditional probability table (annotated metabolites × top predictive taxa; CSV format)
- Ranked list of taxa by conditional probability strength metric
- Summary interaction table linking metabolites to their most probable microbial associates

## How to apply

Load the mmvec conditional probability matrix (output from QIIME2 microbe-metabolite vectors plugin), where rows are metabolites and columns are taxa. For each taxon, compute a summary statistic of predictive strength—such as the maximum conditional probability across all metabolites, the mean conditional probability, or the number of metabolites exceeding a threshold (e.g., > 0.1). Rank taxa by this strength metric in descending order and retain the top N taxa (e.g., 27 taxa as in this study) that show the highest and most consistent conditional probabilities. Export the filtered conditional probability table (metabolites × top taxa) to CSV format. The rationale is that taxa with high conditional probability values across metabolites are more likely to represent genuine ecological drivers of metabolite profiles rather than rare or noise-associated members.

## Related tools

- **mmvec** (Generates conditional probability matrices encoding the likelihood of observing each metabolite given each microbial taxon; output is filtered and ranked by this skill.)
- **QIIME2 microbe-metabolite vectors plugin** (Plugin interface for running mmvec within the QIIME2 framework; exports conditional probability artifact that serves as input.)
- **R** (Used for ranking taxa by conditional probability strength and exporting filtered results to CSV.) — https://github.com/jhaffner09/core_metabolome_2021

## Evaluation signals

- Ranked taxa list is sorted in descending order by conditional probability strength (max, mean, or other metric); top N taxa are retained without gaps or ties unresolved.
- Filtered conditional probability matrix has shape (number of metabolites) × (N top taxa); all entries are numeric and in valid probability range [0, 1].
- No missing values (NaN, null) are present in the output matrix; all selected taxa appear in all rows.
- Top-ranked taxa show visually or statistically higher conditional probabilities compared to taxa excluded from the top N; the separation is non-arbitrary (not all taxa clustered at similar strength).
- Exported CSV file is parseable and matches the structure of the input mmvec matrix; row and column identifiers are preserved and match the original metabolite and taxon names.

## Limitations

- The choice of rank threshold (e.g., top 27 taxa) is somewhat arbitrary; the paper does not provide a principled statistical justification for this cutoff. Practitioners should perform sensitivity analysis (e.g., try top 20, 27, 40) to assess robustness.
- Conditional probability alone does not imply causality or mechanism; high predictive strength reflects co-occurrence in the training data and may be confounded by shared ecological niches or indirect associations.
- mmvec is trained on the full metabolite feature set; if the input mmvec model was trained on unfiltered or poorly curated metabolites, the taxa rankings may reflect spurious associations rather than true metabolite–microbe interactions.
- This skill discards low-strength taxa entirely, which may hide rare but mechanistically important members if they associate strongly with a single metabolite of interest.

## Evidence

- [results] After subsetting results to our 67 shared annotated metabolites and their major predictive taxa (27 total), several probable interactions between key gut metabolite features and microbes were observed: "After subsetting results to our 67 shared annotated metabolites and their major predictive taxa (27 total), several probable interactions between key gut metabolite features and microbes were observed"
- [results] we used the neural network platform microbe-metabolite vectors (mmvec) (69): "we used the neural network platform microbe-metabolite vectors (mmvec) (69)"
- [results] Our mmvec analysis used microbial amplicon sequencing variants (ASVs) derived from earlier sample analyses (24) (see Materials and Methods for more details) that were assigned to taxonomic: "Our mmvec analysis used microbial amplicon sequencing variants (ASVs) derived from earlier sample analyses (24) that were assigned to taxonomic"
- [other] Five Sporobacter species and one unknown Anaeroplasmataceae member were identified as the most influential taxa, with N-acetyl-L-phenylalanine showing strong predictive interactions: "Five Sporobacter species and one unknown Anaeroplasmataceae member were identified as the most influential taxa"
