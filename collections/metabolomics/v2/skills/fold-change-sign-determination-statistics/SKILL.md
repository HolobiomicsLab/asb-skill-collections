---
name: fold-change-sign-determination-statistics
description: Use when you have paired measurements (e.g., gene expression counts,
  protein abundance, or sampled flux distributions) from two cell lines or conditions
  and need to assign a directional sign to each reaction or gene for downstream concordance
  analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_0821
  tools:
  - t-test
  - Mann–Whitney U test
  - Benjamini–Hochberg FDR correction
  - COBRApy (optGpSampler)
  - getRASscore.py
  - rasTtest.py
  - mannWhitneyUTest.py
  - createMetabolicDataset.py
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009337
  all_source_dois:
  - 10.1371/journal.pcbi.1009337
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fold-change-sign-determination-statistics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Determine whether a metabolic reaction or gene shows significant up-regulation (+1), down-regulation (−1), or no change (0) between two biological conditions using statistical tests on fold-change measurements. This skill classifies directional changes in transcriptomics (RAS), proteomics (RPS), and flux distribution data (FFD) to enable concordance analysis across regulatory layers.

## When to use

Apply this skill when you have paired measurements (e.g., gene expression counts, protein abundance, or sampled flux distributions) from two cell lines or conditions and need to assign a directional sign to each reaction or gene for downstream concordance analysis. Use it as the first step before computing Cohen's kappa coefficients to classify reactions into regulatory categories (transcriptional, metabolic, combined, or unclassified).

## When NOT to use

- Do not use if input measurements are already pre-computed as discrete signs (e.g., a file with sign assignments already made) — this skill is for deriving signs from raw or normalized quantitative data.
- Do not use if the fold-change threshold or statistical test parameters have not been justified for your biological context or sample size — the skill requires explicit threshold specification.
- Do not use if reactions lack gene-protein-reaction (GPR) associations for RAS computation or if protein or flux data are missing; the workflow notes that reactions without GPR associations are excluded from RAS-RPS concordance analysis.

## Inputs

- RAS scores (Reaction Activity Scores) per reaction and cell line from transcriptomics data
- RPS scores (Reaction Protein Scores) or protein abundance data per reaction and cell line
- FFD (Flux Fate Distribution) sampled flux distributions (Mann–Whitney U test ready format) per reaction pair-wise comparison
- Fold-change threshold parameters (default: ≥20% for RAS/RPS, log₂ threshold for FFD)
- P-value significance threshold (default: p < 0.05)
- FDR correction threshold (default: FDR < 5% after Benjamini–Hochberg)
- List of pairwise cell-line comparisons (10 pairs for 5 cell lines)

## Outputs

- Sign matrix (reactions × pairwise comparisons) with entries in {+1, −1, 0}
- CSV file with columns: Reaction ID, pairwise comparison identifier, assigned sign (+1/−1/0), fold-change value, test statistic (t-statistic or Mann–Whitney U), raw p-value, FDR-adjusted p-value
- Separate sign tables for RAS vs FFD, RPS vs FFD, and RAS vs RPS comparisons
- Quality flags indicating which comparisons passed significance and fold-change thresholds

## How to apply

For each reaction or gene pair-wise comparison between two conditions: (1) Apply a t-test (for RAS transcriptomics scores) or Mann–Whitney U test (for RPS protein activity and FFD flux distribution samples; p < 0.05) to determine if the measurements differ significantly. (2) Compute the fold-change ratio (or log₂ fold-change for FFD flux samples) and set a fold-change threshold (typically ≥20% or log₂ fold-change ratio determined from metabolomic statistical tests). (3) Assign the sign: +1 if fold-change meets threshold AND statistical test is significant (up-regulated), −1 if fold-change is reversed AND significant (down-regulated), 0 if fold-change is below threshold or not significant (no change). (4) Repeat for all 10 pairwise cell-line comparisons to create a sign vector per reaction. (5) Apply Benjamini–Hochberg FDR correction to empirical p-values from randomized sampling (target FDR < 5%) to set the final significance threshold. The result is a sign matrix (reactions × pairwise comparisons) suitable for Cohen's kappa concordance computation.

## Related tools

- **t-test** (Statistical test for comparing RAS (transcriptomics-derived reaction activity scores) between two cell lines; p-value threshold p < 0.05 used to validate fold-change significance)
- **Mann–Whitney U test** (Non-parametric statistical test for comparing RPS protein scores and FFD flux distribution samples between two conditions; p-value threshold p < 0.05 used to determine significance of fold-change)
- **Benjamini–Hochberg FDR correction** (Multiple-testing correction applied to empirical p-values derived from randomized RPS sampling to set overall significance threshold at FDR < 5%)
- **COBRApy (optGpSampler)** (Generates uniform samples from the flux feasible region for FFD analysis; samples are compared using Mann–Whitney U test to compute fold-change signs) — https://github.com/opencobra/cobrapy
- **getRASscore.py** (Pipeline step that computes RAS scores from GPR rules and transcriptomics read counts; output is input to t-test for fold-change sign determination) — https://github.com/qLSLab/integrate
- **rasTtest.py** (Pipeline step that applies t-test to RAS scores across cell-line pairs to compute fold-change signs (up/down/no-change) for transcriptional regulation assessment) — https://github.com/qLSLab/integrate
- **mannWhitneyUTest.py** (Pipeline step that applies Mann–Whitney U test to FFD flux samples and RPS protein data across cell-line pairs; outputs p-values and fold-change signs for metabolic regulation) — https://github.com/qLSLab/integrate
- **createMetabolicDataset.py** (Prepares FFD log₂ fold-change ratios and metabolomic statistical test outputs (t-test, log₂ fold-change ratio between cell-line means) for downstream Mann–Whitney U test and sign assignment) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/rasTtest.py && python pipeline/mannWhitneyUTest.py timeStampInput nSamples
```

## Evaluation signals

- Sign matrix contains only values in {+1, −1, 0} with no missing or invalid entries for reactions that have GPR associations (or metabolomics data for FFD).
- All p-values reported alongside sign assignments; FDR-adjusted p-values match Benjamini–Hochberg correction formula applied to empirical p-values from randomized sampling.
- Fold-change values (or log₂ fold-change ratios) are reported and match the stated threshold (≥20% or equivalent log₂ cutoff); sign assignment is consistent with fold-change direction (positive fold-change → +1, negative → −1).
- Reactions excluded from analysis (those without GPR rules, or with missing protein/metabolomics data) are explicitly flagged in output; counts of excluded reactions align with data completeness.
- Cross-validation: sign matrices for RAS-vs-FFD and RPS-vs-RAS are independent and can be used for downstream Cohen's kappa concordance computation without missing pairwise entries.

## Limitations

- Reactions without gene-protein-reaction (GPR) associations cannot be included in RAS fold-change sign analysis, limiting coverage of the metabolic model.
- When a single reaction substrate is missing from metabolomics measurements, the entire reaction is omitted from FFD fold-change sign analysis, creating data gaps.
- Direct determination of metabolic fluxes through labeled substrates lags behind omic technologies, so flux sign determination relies on constraint-based model sampling (optGpSampler) rather than direct measurement, introducing model dependency.
- The choice of fold-change threshold (default ≥20% or log₂ cutoff) is empirical and may require biological justification or sensitivity analysis for different tissue types or conditions.
- Multiple testing correction (Benjamini–Hochberg) controls FDR at 5%, but in sparse datasets or when most reactions show no significant change, this threshold may be overly stringent or permissive depending on the biological question.

## Evidence

- [other] For each of the 10 pairwise cell-line comparisons, compute the sign of variation (up +1, down −1, no-change 0) for RAS and RPS using t-test and Mann–Whitney U test (p<0.05) with fold-change threshold ≥20%.: "For each of the 10 pairwise cell-line comparisons, compute the sign of variation (up +1, down −1, no-change 0) for RAS and RPS using t-test and Mann–Whitney U test (p<0.05) with fold-change threshold"
- [other] Compute the sign of FFD variation for each pair using Mann–Whitney U test on sampled flux distributions with log₂ fold-change ratio.: "Compute the sign of FFD variation for each pair using Mann–Whitney U test on sampled flux distributions with log₂ fold-change ratio"
- [other] Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR<5%.: "Apply Benjamini–Hochberg FDR correction to empirical p-values derived from randomized RPS sampling to set significance threshold at FDR<5%"
- [full_text] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset.: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [full_text] Missing RPSvsRAS values occur when a reaction is not associated with a GPR.: "Missing RPSvsRAS values occur when a reaction is not associated with a GPR"
- [full_text] Direct determination of metabolic fluxes through the use of labeled substrates lags behind other omic technologies, mainly due to technical difficulties: "Direct determination of metabolic fluxes through the use of labeled substrates lags behind other omic technologies, mainly due to technical difficulties"
- [readme] Users may decided to leave the following inputs associated to their default values or set them as preferred: valLog: value above which the ratio between the means of two cell lines are considered statistically different. Default value: 1.2: "valLog: value above which the ratio between the means of two cell lines are considered statistically different. Default value: 1.2"
- [readme] For each pair of input cell line c_1 and c_2, a file returning the output of t-test named 'ras_' + c_1 +'_vs_' + c_2 + '.csv': "For each pair of input cell line c_1 and c_2, a file returning the output of t-test named 'ras_' + c_1 +'_vs_' + c_2 + '.csv'"
