---
name: trend-classification-from-fold-change
description: Use when when you have harmonized metabolomics data with fold-change and p-value columns from multiple studies and need to assign trend categories prior to vote-counting meta-analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - R
  - amanida
  - webchem
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions for computing a weighted meta-analysis
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Trend classification from fold-change

## Summary

Assign directional trend labels (+1 for up-regulation, −1 for down-regulation, 0 for no trend) to metabolite compounds based on fold-change thresholds and statistical significance. This classification enables qualitative vote-counting meta-analysis in metabolomics studies where raw variance data are unavailable.

## When to use

When you have harmonized metabolomics data with fold-change and p-value columns from multiple studies and need to assign trend categories prior to vote-counting meta-analysis. Specifically, use this skill when comparing metabolite behaviour across studies but lack standard deviation or variance estimates required by traditional weighted meta-analysis methods.

## When NOT to use

- Input data lack fold-change or p-value columns — standard trend classification requires both magnitude and significance information.
- Analysis goal is quantitative meta-analysis combining effect sizes and confidence intervals — use weighted Fisher's method or logarithmic fold-change combination instead.
- Metabolite identifiers are not harmonized to a common nomenclature (e.g., PubChem ID) — perform identifier harmonization via `check_names` before classification to avoid spurious trend splits across synonym variants.

## Inputs

- Harmonized metabolite dataset with columns: compound identifier, fold-change (numeric), statistical significance (p-value or significance flag)
- Study-level fold-change and trend classification data

## Outputs

- Trend-classified metabolite table with vote assignments (+1, −1, 0) per compound per study
- Compound trend vote distribution (count of +1, −1, 0 votes across studies)

## How to apply

For each metabolite compound in each study, assign a trend vote based on fold-change magnitude and direction: assign +1 if fold-change > 1 (up-regulation) and statistically significant, −1 if fold-change < 1 (down-regulation) and statistically significant, and 0 if no significant trend is observed. Apply a fold-change cutoff of ≥2 for biological meaningfulness (values below this threshold may represent noise). Handle negative fold-change values by transforming them to positive using the reciprocal (1/value) before comparison. This classification preserves effect direction and allows subsequent aggregation via vote-counting across all studies for each compound, producing a consensus trend measure.

## Related tools

- **amanida** (R package that implements trend classification and vote-counting via amanida_read (data import) and amanida_vote (vote assignment and aggregation) functions; also provides visualization via vote_plot and explore_plot) — https://github.com/mariallr/amanida
- **R** (Statistical computing environment for executing amanida functions and manipulating fold-change and trend data)
- **webchem** (R package used upstream (via check_names) to harmonize metabolite identifiers to PubChem ID before trend classification)

## Examples

```
coln = c("Compound Name", "Behaviour", "References"); data_votes <- amanida_read(input_file, mode = "qual", coln, separator = ";"); vote_result <- amanida_vote(data_votes)
```

## Evaluation signals

- Vote distribution table sums to total number of studies per compound (no missing or double-counted studies).
- All vote values are exactly {−1, 0, +1}; no other numeric values appear.
- Compounds with fold-change |log₂(FC)| < 1 (i.e., raw FC < 2 or > 0.5) consistently receive vote = 0 unless overridden by explicit significance threshold.
- Negative fold-change values (e.g., −0.8) are transformed to reciprocals (1/0.8 = 1.25) before comparison; no negative fold-changes remain in the classified output.
- Vote plot and explore plot outputs restrict to ≤30 and ≤25 compounds respectively (per output readability constraints); verify the limitation is applied when generating visualizations.

## Limitations

- Vote-counting is qualitative and loses magnitude information — two compounds with fold-changes of 1.1 and 10 both receive vote = +1 if statistically significant, conflating weak and strong effects.
- Missing data (studies that did not report a metabolite) are ignored during voting, which may bias consensus toward studies with more complete metabolite coverage.
- No threshold for p-value significance is enforced at the skill level; practitioners must pre-filter data or define p-cutoff externally (typically p < 0.05) before classification.
- Fold-change direction is absolute (1/value transformation); if the original sign convention differs between studies (e.g., some report concentration ratio A/B, others B/A), harmonization must occur before trend classification to avoid spurious sign reversals.

## Evidence

- [intro] votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend: "votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend"
- [other] Assign votes per compound per study: +1 for up-regulation (fold-change > 1 or positive trend), −1 for down-regulation (fold-change < 1 or negative trend), 0 for no significant trend.: "Assign votes per compound per study: +1 for up-regulation (fold-change > 1 or positive trend), −1 for down-regulation (fold-change < 1 or negative trend), 0 for no significant trend"
- [intro] in case of fold-change we recommend values higher than 2, where it is considered to have biological meaningfulness: "in case of fold-change we recommend values higher than 2, where it is considered to have biological meaningfulness"
- [intro] negative values of fold-change are transformed to positive (1/value): "negative values of fold-change are transformed to positive (1/value)"
- [readme] Compound vote-counting: votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend. The total votes are divided by the number of reports.: "Compound vote-counting: votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend"
