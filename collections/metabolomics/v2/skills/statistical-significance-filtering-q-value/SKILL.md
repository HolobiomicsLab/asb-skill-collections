---
name: statistical-significance-filtering-q-value
description: Use when after performing univariate statistical tests (e.g., ANOVA, t-tests) across sample classes in a normalized metabolomic feature table, you need to control false discovery rate and select a high-confidence subset of significantly differentiated metabolites for downstream analysis (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - margheRita
  - R
  - MS-DIAL
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
- The R package margheRita addresses the complete workflow
- The R package margheRita
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Statistical significance filtering by q-value

## Summary

Filter metabolomic features based on multiple-testing-corrected significance thresholds (q-values) to identify features with robust statistical evidence across sample classes. This skill applies Benjamini–Hochberg FDR correction to raw p-values from univariate tests and retains only features meeting a user-specified q-value cutoff.

## When to use

After performing univariate statistical tests (e.g., ANOVA, t-tests) across sample classes in a normalized metabolomic feature table, you need to control false discovery rate and select a high-confidence subset of significantly differentiated metabolites for downstream analysis (e.g., pathway enrichment, metabolite identification). Use this when you have computed p-values for hundreds or thousands of features and want to avoid spurious findings.

## When NOT to use

- The input feature table has not yet been normalized (e.g., raw peak heights without batch correction or probabilistic quotient normalization) — apply preprocessing first.
- You are analyzing a single-class or non-comparative design with no meaningful class structure — univariate testing and q-value filtering require at least two distinct sample groups.
- The sample size is very small (n < 3 per class) — statistical power is too low for reliable p-value computation and FDR correction may be overly conservative or unstable.

## Inputs

- Normalized metabolomic feature table (e.g., Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt from MS-DIAL)
- Sample metadata with class assignments (e.g., AA, DD, MM phenotype labels)
- Univariate test results (p-values from ANOVA or other parametric/non-parametric tests)

## Outputs

- Filtered feature table containing only significant metabolites
- Tabulated results with Feature_ID, metabolite names, ANOVA F-statistics, p-values, and q-values
- Summary statistics (count of features retained at specified q-value threshold)

## How to apply

Load the normalized metabolomic data object (e.g., from MS-DIAL output) with sample metadata including class assignments into margheRita. Apply the univariate() function to compute ANOVA F-statistics and p-values across all class levels for each feature; this step automatically or optionally applies Benjamini–Hochberg FDR correction to generate q-values. Then invoke select_sign_features() with a q-value threshold (typical cutoffs are 0.01, 0.05, or 0.1 depending on stringency required) to filter and retain only features with q-values below the threshold. Extract the resulting feature table, which now contains only significant metabolites with their Feature_ID, metabolite names, ANOVA statistics, p-values, and q-values. Verify the filtering by comparing the input and output feature counts and inspecting the q-value distribution.

## Related tools

- **margheRita** (R package hosting univariate() and select_sign_features() functions for ANOVA testing and q-value-based feature filtering) — https://github.com/emosca-cnr/margheRita
- **R** (Programming language runtime for margheRita and statistical computation)
- **MS-DIAL** (Peak-picking software that generates the raw feature tables downstream of which filtering is applied)

## Examples

```
univariate_results <- univariate(data_object, class_var = "phenotype"); significant_features <- select_sign_features(univariate_results, q_cutoff = 0.05)
```

## Evaluation signals

- Feature count decreases from input to output, confirming that filtering removed non-significant features; the magnitude of reduction should reflect the stringency of the chosen q-value threshold.
- All q-values in the output table are ≤ the specified threshold (e.g., 0.05); spot-check by sorting and confirming the highest q-value in the result does not exceed the cutoff.
- The q-value distribution shows expected behavior: q-values ≥ p-values (due to FDR correction), and features with smallest p-values have the smallest q-values.
- Features retained are biologically plausible (e.g., known metabolites differentially abundant between phenotypes) and match literature or prior studies, indicating the threshold is not too stringent or lenient.
- Benjamini–Hochberg correction has been applied: verify by checking that the total number of tests (features) and correction method are documented in the output metadata or function call parameters.

## Limitations

- Q-value filtering does not account for effect size — a feature with very small fold-change but large sample size may pass the q-value threshold and be retained despite weak biological significance; consider also filtering by fold-change or effect size thresholds.
- The choice of q-value cutoff (e.g., 0.01 vs. 0.05 vs. 0.1) is somewhat arbitrary and affects downstream findings; no single cutoff is universally optimal. Sensitivity analysis across multiple thresholds is recommended.
- FDR correction assumes that the majority of features are truly null (non-significant); if most features are genuinely differentiated, FDR correction may be overly conservative and filter out true signals.
- This filtering step addresses multiple-testing correction but not other sources of bias (e.g., confounding variables, batch effects, or unequal group variances); ensure data has been preprocessed appropriately before applying univariate tests.

## Evidence

- [other] Apply univariate() function to compute ANOVA F-statistics and p-values across the three class levels for each metabolite feature.: "Apply univariate() function to compute ANOVA F-statistics and p-values across the three class levels for each metabolite feature."
- [other] Use select_sign_features() to filter significant features based on q-value threshold (Benjamini–Hochberg FDR correction applied during univariate or select_sign_features step).: "Use select_sign_features() to filter significant features based on q-value threshold (Benjamini–Hochberg FDR correction applied during univariate or select_sign_features step)."
- [other] Extract and tabulate the results including feature identifiers, ANOVA statistics, p-values, q-values, and effect sizes.: "Extract and tabulate the results including feature identifiers, ANOVA statistics, p-values, q-values, and effect sizes."
- [readme] simplified execution of parametric and non-parametric statistical tests over a large number of features: "simplified execution of parametric and non-parametric statistical tests over a large number of features"
- [other] ANOVA testing across AA, DD, and MM class levels in the Urine dataset identified significant metabolic features, with results reported in a table including Feature_ID, metabolite names, and associated q-values for filtering at specified cutoffs.: "ANOVA testing across AA, DD, and MM class levels in the Urine dataset identified significant metabolic features, with results reported in a table including Feature_ID, metabolite names, and"
