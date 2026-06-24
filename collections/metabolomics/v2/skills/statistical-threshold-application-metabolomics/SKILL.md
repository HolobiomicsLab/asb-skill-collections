---
name: statistical-threshold-application-metabolomics
description: Use when when you have completed a weighted meta-analysis of metabolomic
  studies using amanida and need to isolate robust, reproducible metabolite signals
  from the combined results.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - amanida
  - webchem
  - PubChem
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted
  meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions
  for computing a weighted meta-analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_amanida_cq
    doi: 10.1093/bioinformatics/btab591
    title: Amanida
  dedup_kept_from: coll_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab591
  all_source_dois:
  - 10.1093/bioinformatics/btab591
  - 10.3390/metabo13121167
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Statistical Threshold Application in Metabolomics Meta-Analysis

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply combined statistical and effect-size cutoffs (p-value ≤0.05, fold-change ≥3.5) to volcano plot and mixed-mode explore plot outputs to identify metabolites with statistical significance, multiple independent reports, and consistent directional trends across studies. This skill validates candidate biomarkers by rejecting the null hypothesis through quantitative filtering and qualitative consistency voting.

## When to use

When you have completed a weighted meta-analysis of metabolomic studies using amanida and need to isolate robust, reproducible metabolite signals from the combined results. Specifically, apply this skill when: (1) you have computed quantitative meta-analysis results with p-values and fold-changes for multiple compounds, (2) you want to identify compounds appearing in ≥2 independent reports with concordant directional trends, (3) you seek to balance statistical stringency (p≤0.05) with biological meaningfulness (fold-change≥3.5), and (4) your goal is to short-list candidates for further validation or mechanistic investigation.

## When NOT to use

- Input data lacks multiple independent studies per compound — threshold filtering requires ≥2 reports for consistency voting to be meaningful.
- Fold-change values are already on absolute scale and sign is not meaningful — the mixed-mode explore plot relies on directional trend (up vs. down regulation) to assess consistency.
- Statistical power is low (very small N per study, few studies total) — stringent cutoffs (p≤0.05, FC≥3.5) may eliminate true signals or retain noise-driven false positives when weighted meta-analysis is underpowered.

## Inputs

- amanida quantitative meta-analysis result object (S4 object with @stat and @vote slots)
- Compound metadata: identifier, p-value, fold-change, study size (N), reference
- Sample data in csv/xlsx/txt format with columns: Compound Name, P-value, Fold-change, N total, References

## Outputs

- Filtered compound list meeting volcano plot cutoffs (p≤0.05, |fold-change|≥3.5)
- Filtered compound list with multi-report consistency (counts≥1, unanimous trend direction)
- Intersection set of compounds passing both statistical and consistency thresholds
- Volcano plot visualization with labeled significant compounds
- Explore plot visualization showing report counts, trend direction, and vote-counting scores

## How to apply

First, generate a volcano plot from amanida's quantitative meta-analysis output using user-defined cutoffs: retain only compounds with p-value ≤0.05 AND absolute fold-change ≥3.5. Second, apply the explore plot with type='mix' and counts=1 to identify compounds represented in ≥1 additional report where all reports show the same directional trend (all up-regulated or all down-regulated, with no discrepancies). Third, cross-validate by confirming that compounds meeting both filters appear in the intersection of volcano-filtered and trend-consistent sets. The rationale is that statistical significance alone (volcano cutoff) guards against false positives from noise, while multi-report consistency (explore plot voting) ensures reproducibility and reduces study-specific artifacts. The counts=1 parameter enforces ≥2 reports per compound; compounds with unanimous trend direction across all their reports are prioritized as high-confidence biomarkers.

## Related tools

- **amanida** (Performs weighted meta-analysis combining p-values (Fisher's method weighted by study size), fold-changes (log-transformed and weighted), and vote-counting for trend consistency; generates volcano and explore plots with user-defined cutoffs) — https://github.com/mariallr/amanida
- **R** (Execution environment for amanida functions (amanida_read, compute_amanida, volcano_plot, explore_plot))
- **webchem** (Harmonizes compound identifiers (chemical names, InChI, InChIKey, SMILES) to PubChem IDs before filtering to ensure consistent nomenclature across studies)
- **PubChem** (Reference database used by webchem to normalize and validate compound identifiers and retrieve metadata (Molecular Formula, Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank))

## Examples

```
```r
library(amanida)
data(sample_data)
amanida_result <- compute_amanida(sample_data, comp.inf = FALSE)
volcano_plot(amanida_result, cutoff = c(0.05, 3.5))
explore_plot(amanida_result, type = "mix", counts = 1)
```
```

## Evaluation signals

- Volcano plot output correctly labels and isolates only compounds with p-value ≤0.05 AND |log2(fold-change)| ≥ log2(3.5) ≈ 1.81; verify by spot-checking axis coordinates against cutoff lines.
- Explore plot with type='mix' and counts=1 returns only compounds with ≥2 reports showing unanimous directional trend (no mixed up/down signals within a compound); vote-counting score should equal the number of reports for filtered compounds.
- Cross-validation: manually verify that all compounds in the intersection set appear in both the volcano plot and explore plot outputs; no compound should pass one filter but fail the other.
- Compound metadata integrity: confirm that p-values, fold-changes, and study sizes (N) are correctly imported and transformed (negative fold-changes inverted to positive; missing data ignored) before threshold application.
- Statistical consistency: for compounds passing filters, the combined p-value and fold-change should reflect consistent directional weighting — i.e., compounds with high fold-change and low p-value in multiple studies should have strong combined signals.

## Limitations

- Threshold cutoffs (p≤0.05, FC≥3.5) are application-specific and may require tuning depending on metabolomic domain, sample size distribution, and prior biological knowledge; no universal optimum is provided.
- Vote-counting (counts=1 minimum) detects consistency in directional trend but cannot distinguish true biological signal from systematic study bias or confounding factors present across all reports.
- Volcano plot output is restricted to 30 compounds and explore plot to 25 compounds for readability; large meta-analyses may require subsetting or multiple visualizations to inspect all filtered results.
- Requires harmonized compound identifiers (PubChem ID) and complete metadata (p-value, fold-change, N, reference) in all input records; missing data is silently ignored, potentially biasing results if missingness is non-random.
- Fold-change combination uses logarithmic transformation and weighting by N but does not account for heterogeneity in study design, analytical platform, or sample phenotype — biological inconsistency may be masked if studies differ systematically in unmeasured confounders.

## Evidence

- [other] p-value ≤0.05 and absolute fold-change ≥3.5: "Filter compounds using volcano plot cutoffs: retain compounds with p-value ≤0.05 and absolute fold-change ≥3.5."
- [other] explore plot with type='mix' and counts=1: "Apply explore plot with type='mix' and counts=1 to identify compounds with more than one report showing consistent trend direction."
- [other] Hippuric acid and Phenol identified with consistency: "Hippuric acid and Phenol are identified as compounds with more than one report and statistical significance, with consistency as all reports results are in the same trend, providing evidence to"
- [intro] weighted meta-analysis combining overall results based on statistical significance, relative change and study size: "The purpose of amanida is to perform a weighted meta-analysis combining overall results based on statistical significance, relative change and study size"
- [intro] volcano plot with user-defined cut-offs for p-values and fold-change: "To observe the results of meta-analysis graphically is done with a volcano plot, where the log10(p-values) are plotted against the log2(fold-change)"
- [intro] explore plot to identify consistency of results: "A bar plot shows the result of vote-counting. With vote plot discrepancies in compounds behaviour are not detected at first glance, and we suggest to combine the results with the explore plot"
- [readme] vote-counting for consistency assessment: "Compound vote-counting: votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend. The total votes are divided by the number of reports."
- [intro] fold-change higher than 2 for biological meaningfulness: "in case of fold-change we recommend values higher than 2, where it is considered to have biological meaningfulness"
