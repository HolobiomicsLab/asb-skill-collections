---
name: consensus-scoring-meta-analysis
description: Use when when you have harmonized metabolite data from multiple studies with identifier, fold-change direction, and trend classification columns available, but lack standard deviations or variance estimates needed for quantitative meta-analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3474
  tools:
  - R
  - amanida
  - webchem
  - PubChem
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

# Consensus Scoring via Vote-Counting Meta-Analysis

## Summary

Qualitative meta-analysis method that assigns directional votes (+1 for up-regulation, −1 for down-regulation, 0 for no trend) to each metabolite across multiple studies and sums them to produce a consensus measure of compound behaviour. This approach is designed for metabolomics datasets where standard deviations or raw effect sizes are unavailable but trend direction and study counts are known.

## When to use

When you have harmonized metabolite data from multiple studies with identifier, fold-change direction, and trend classification columns available, but lack standard deviations or variance estimates needed for quantitative meta-analysis. Use vote-counting when you need a simple, transparent qualitative consensus measure that combines trend directionality and study agreement without assuming normal distributions or requiring effect size calculations.

## When NOT to use

- Input data already includes standard deviations, confidence intervals, or sufficient sample-level statistics to perform quantitative meta-analysis (use compute_amanida with mode='quan' instead).
- Trend direction is not clearly defined or is ambiguous across studies (vote-counting requires unambiguous +1/−1/0 classification per study).
- Only a single study is available; vote-counting gains consensus power from multiple reports and is not meaningful for individual studies.

## Inputs

- Harmonized metabolite dataset (CSV, XLS/XLSX, or TXT) with columns: compound identifier, trend/behaviour label (up-regulated, down-regulated, or no trend), and bibliographic reference
- Study count (N) for each compound-study pair (implicit in dataset structure)
- Fold-change values (optional; used to infer trend if behaviour label absent)

## Outputs

- Vote-counting results table (S4 object slot @vote) with columns: compound identifier, total vote score, count of +1 votes, count of −1 votes, count of 0 votes
- Vote plot (bar chart) showing vote distribution across compounds
- Explore plot (bar chart with trend breakdown) showing reports divided by trend direction and total vote-counting
- Optional: Enhanced results table with PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank identifiers (if comp.inf=T)

## How to apply

Load the harmonized metabolite dataset (with columns: identifier, trend/behaviour label, and reference) using amanida_read with mode='qual'. For each compound across all studies, assign votes: +1 for up-regulation (positive trend or fold-change > 1), −1 for down-regulation (negative trend or fold-change < 1), and 0 for no significant trend. Sum the votes for each compound across all studies to produce a final vote count. Generate a vote-counting table with compound identifier, total vote score, and the distribution of individual votes (+1, −1, 0 counts). Restrict visualizations to the top compounds (≤30 for vote_plot, ≤25 for explore_plot) for readability. Optionally retrieve compound descriptors from PubChem using webchem to cross-validate identifiers and detect duplicates before voting.

## Related tools

- **amanida** (R package that implements vote-counting via amanida_vote() function and integrates vote-counting with quantitative meta-analysis in compute_amanida(); provides amanida_read() for data import, check_names() for ID harmonization, and vote_plot()/explore_plot() for visualization.) — https://github.com/mariallr/amanida
- **webchem** (R package used by amanida to retrieve PubChem IDs from chemical identifiers (InChI, InChIKey, SMILES, names) for compound ID harmonization before vote-counting.)
- **PubChem** (Public chemical database queried via webchem to standardize compound identifiers and retrieve molecular descriptors (SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank) for validation and cross-referencing.)
- **R** (Programming environment for executing amanida functions and custom vote-counting workflows.)

## Examples

```
coln = c("Compound Name", "Behaviour", "References"); data_votes <- amanida_read("dataset.csv", mode = "qual", coln, separator = ","); vote_result <- amanida_vote(data_votes); vote_plot(vote_result)
```

## Evaluation signals

- Vote counts for each compound sum to the total number of studies reporting that compound (invariant: sum of +1, −1, and 0 votes = number of reports).
- Vote scores are symmetric around zero (e.g., −3 to +3 for 3 studies); total vote always equals number of reports or lies within [−N, +N] range where N = number of studies.
- All input compounds appear in the output vote-counting table with valid vote assignments; no compounds are dropped without explicit logging.
- Vote plot and explore plot output contain no more than 30 and 25 compounds respectively; verify readability threshold is applied.
- If comp.inf=T is used, all returned compounds include valid PubChem IDs and molecular descriptors; no missing or empty descriptor fields in final table.

## Limitations

- Vote-counting assigns equal weight to each study regardless of sample size (N); for studies with very different N values, consider using quantitative meta-analysis (weighted Fisher's method) instead to incorporate study size.
- Vote-counting is sensitive to the number of studies: with only 2–3 studies, vote scores (e.g., +1, −1) are coarse and may not distinguish subtle disagreement from strong consensus; more studies increase resolution.
- Missing data is ignored during import, potentially biasing vote counts if missingness is not random (e.g., non-significant results may be under-reported).
- Vote-counting does not account for statistical significance of individual study results; a weakly significant up-regulation and a strongly significant up-regulation both contribute +1.
- Negative fold-change values are transformed to positive (1/value) for computational convenience, but this transformation may obscure the magnitude of very small fold-changes; ensure fold-changes are pre-processed and meaningful before voting.

## Evidence

- [intro] votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend: "votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend"
- [other] Sum votes across all studies for each compound to produce final vote counts: "Sum votes across all studies for each compound to produce final vote counts"
- [intro] amanida computes qualitative meta-analysis performing vote-counting for compounds, including the option of only using identifier and trend labels: "Amanida also computes qualitative meta-analysis performing a vote-counting for compounds, including the option of only using identifier and trend labels"
- [intro] Vote plot output is restricted to 30 compounds for readability; Explore plot output is restricted to 25 compounds for readability: "output is restricted to 30 compounds to facilitate the readability"
- [readme] For qualitative analysis the check_names can be also used, following the same procedure explained in Section 2: "For qualitative analysis the `check_names` can be also used, following the same procedure"
- [readme] Compound vote-counting: votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend. The total votes are divided by the number of reports.: "Compound vote-counting: votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend"
- [intro] When raw data is not available to perform a meta-analysis, there are different approaches that require the standard deviation for effect size estimate calculation and weighted methods: "When raw data is not available to perform a meta-analysis, there are different approaches that can be applied but them require the standard deviation"
