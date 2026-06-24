---
name: spectral-correlation-interpretation
description: Use when you have preprocessed 1H NMR spectral data (e.g., from plasma
  or biological samples acquired on a 600 MHz instrument) and need to identify the
  chemical composition of a prominent but structurally ambiguous peak.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0081
  tools:
  - Statistical Total Correlation Spectroscopy (STOCSY)
  - R
  - Bioconductor
  - MWASTools
  - TopSpin 3.2
  techniques:
  - NMR
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
evidence_spans:
- metabolite assignment using Statistical Total Correlation Spectroscopy (STOCSY)
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
- Here, we present a package to perform MWAS using univariate hypothesis testing
- '"MWASTools" is an R package designed to provide an integrated and user-friendly
  pipeline'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwastools_cq
    doi: 10.1093/bioinformatics/btx477
    title: MWASTools
  dedup_kept_from: coll_mwastools_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btx477
  all_source_dois:
  - 10.1093/bioinformatics/btx477
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-correlation-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Use STOCSY (Statistical Total Correlation Spectroscopy) to assign chemical identity to unknown NMR spectral features by analyzing their covariance and correlation patterns with a chosen driver signal. This skill enables metabolite identification when peak assignments are ambiguous by leveraging the inherent correlation structure in high-resolution NMR data.

## When to use

Apply this skill when you have preprocessed 1H NMR spectral data (e.g., from plasma or biological samples acquired on a 600 MHz instrument) and need to identify the chemical composition of a prominent but structurally ambiguous peak. Use it specifically when you have localized an unknown signal by chemical shift (e.g., δ 1.04 ppm) and want to disambiguate its identity by detecting co-varying signals across the full spectrum that would be characteristic of a known metabolite (e.g., valine's characteristic doublet pattern).

## When NOT to use

- Input NMR data is not preprocessed (still contains baseline distortion, phase errors, or misaligned chemical shifts) — apply baseline correction in TopSpin and spectral alignment before STOCSY.
- You already have high-confidence metabolite assignments from 2D NMR (COSY, HSQC) or independent standards — STOCSY is most valuable for ambiguous 1D signals.
- Your NMR sample contains very few replicates (n < ~10–20) — correlation patterns may be unstable and unreliable.

## Inputs

- Preprocessed 1H NMR spectral matrix (e.g., Bioconductor SummarizedExperiment object with samples × chemical shifts)
- Query chemical shift value (ppm) corresponding to the driver signal of interest
- Metadata mapping samples to known metabolite concentrations or phenotypes (optional, for validation)

## Outputs

- STOCSY correlation profile (correlation coefficients for each chemical shift relative to driver signal)
- Annotated STOCSY plot highlighting significant co-varying signals
- Metabolite assignment (e.g., 'valine' based on characteristic doublet pattern at δ 1.04 and δ 0.99)
- Exported correlation data matrix for statistical or visualization follow-up

## How to apply

Load preprocessed NMR spectral data into R with Bioconductor (e.g., the metabo_SE object containing aligned chemical shifts). Select a query ppm value corresponding to your driver signal (e.g., δ 1.04). Apply the STOCSY function with that query parameter to generate a correlation profile across all chemical shifts, computing Pearson correlation coefficients between the driver signal intensity and all other ppm bins across all samples. Extract and visualize the resulting correlation coefficients; significant peaks (positive or negative correlations) indicate signals that co-vary with your driver. Cross-reference any highlighted doublets or multiplets against literature chemical shift libraries (e.g., δ 0.99 and δ 1.04 for valine) to confirm metabolite assignment. Generate an annotated STOCSY plot showing the correlation structure and export the correlation coefficient matrix for downstream analysis.

## Related tools

- **MWASTools** (R package providing the STOCSY implementation and integrated workflow for quality control, metabolite assignment, and visualization in metabolome-wide association studies) — github.com/AndreaRMICL/MWASTools
- **R** (Programming environment (≥3.3) for running STOCSY analysis and data manipulation)
- **Bioconductor** (Framework for loading and manipulating preprocessed NMR spectral data as SummarizedExperiment objects)
- **TopSpin 3.2** (NMR acquisition and preprocessing software for phasing, baseline correction, and export of spectral data prior to STOCSY analysis)

## Examples

```
# In R with MWASTools and Bioconductor loaded: stocsy_result <- STOCSY(metabo_SE, query.ppm = 1.04); plot(stocsy_result); annotate_metabolite(stocsy_result, peaks = c(1.04, 0.99), reference = 'valine')
```

## Evaluation signals

- Highlighted peaks in the STOCSY correlation plot exhibit characteristic multiplet splitting (e.g., doublets for valine) matching literature chemical shift assignments.
- Correlation coefficients for co-varying signals are statistically significant (e.g., |r| > 0.5–0.7) and consistent across independent sample cohorts.
- Driver signal and identified co-varying peaks maintain expected intensity ratios consistent with the molecular structure of the assigned metabolite.
- Metabolite assignment is reproducible across different preprocessing parameters (e.g., different alignment or baseline correction thresholds) and validated against external standards or 2D NMR if available.
- No spurious correlations (signals with high |r| that do not match known metabolite patterns) dominate the STOCSY output, indicating signal quality and specificity.

## Limitations

- STOCSY assumes linear covariance relationships; non-linear or context-dependent metabolite correlations may be missed or misinterpreted.
- Spectral overlap and baseline artifacts can inflate or reduce correlation coefficients, requiring high-quality preprocessing (phasing, baseline correction in TopSpin 3.2) as a prerequisite.
- Chemical shift assignments depend on literature reference data; novel metabolites or variant isotopologue assignments may not be correctly identified if reference standards are unavailable.
- Small sample sizes (n < ~10–20) yield unstable correlation estimates; larger cohorts are needed to distinguish true metabolic correlations from noise.
- MWASTools does not account for non-linear confounding factors or sample-level batch effects after preprocessing; additional epidemiological adjustment may be needed in association studies.

## Evidence

- [other] STOCSY analysis using δ 1.04 as the driver signal identified two highlighted doublets at δ 1.04 and δ 0.99, indicating the unknown signal corresponds to valine.: "STOCSY analysis using δ 1.04 as the driver signal identified two highlighted doublets at δ 1.04 and δ 0.99, indicating the unknown signal corresponds to valine."
- [other] Statistical Total Correlation Spectroscopy (STOCSY) function with query ppm parameter set to 1.04 to generate a correlation profile across all chemical shifts: "Apply STOCSY (Statistical Total Correlation Spectroscopy) function with query ppm parameter set to 1.04 to generate a correlation profile across all chemical shifts."
- [intro] metabolite assignment using Statistical Total Correlation Spectroscopy (STOCSY): "metabolite assignment using Statistical Total Correlation Spectroscopy (STOCSY)"
- [abstract] MWASTools provides quality control analysis, metabolite-phenotype association models, data visualization tools, and metabolite assignment using STOCSY: "MWASTools provides quality control analysis, metabolite-phenotype association models, data visualization tools, and metabolite assignment using statistical total correlation"
- [intro] Following phasing and baseline correction in TopSpin 3.2 software: "Following phasing and baseline correction in TopSpin 3.2 software"
- [other] Load the preprocessed NMR spectral data (metabo_SE) into R with Bioconductor.: "Load the preprocessed NMR spectral data (metabo_SE) into R with Bioconductor."
