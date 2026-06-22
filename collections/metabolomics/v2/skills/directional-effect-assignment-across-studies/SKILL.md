---
name: directional-effect-assignment-across-studies
description: Use when you have harmonized metabolite results from multiple independent studies, each with fold-change or trend classification data but no variance/standard deviation, and you need to produce a qualitative consensus on directionality for each compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - R
  - amanida
  - amanida_read
  - webchem
  - check_names
  - vote_plot
  - explore_plot
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

# directional-effect-assignment-across-studies

## Summary

Assigns directional votes (+1 for up-regulation, −1 for down-regulation, 0 for no trend) to each metabolite compound within individual studies, then sums votes across all studies to produce a qualitative consensus measure. This vote-counting approach enables metabolomic meta-analysis when standard deviation or variance data are unavailable.

## When to use

Apply this skill when you have harmonized metabolite results from multiple independent studies, each with fold-change or trend classification data but no variance/standard deviation, and you need to produce a qualitative consensus on directionality for each compound. Vote-counting is appropriate when raw individual-level data are unavailable and you wish to combine directional signals rather than compute weighted effect sizes.

## When NOT to use

- Raw individual-level metabolomics data are available; use quantitative meta-analysis (weighted p-value and fold-change combination) instead to leverage full statistical power.
- Continuous effect sizes with confidence intervals or standard errors are reported; vote-counting discards magnitude information.
- You require statistical significance testing or confidence intervals around the consensus estimate; vote-counting is purely descriptive and ordinal.

## Inputs

- Harmonized metabolite dataset with columns: compound identifier, fold-change or trend classification, and study reference
- CSV, XLS/XLSX, or TXT file formatted for amanida_read with mode='qual'

## Outputs

- Vote-counting table with compound identifier, total vote score (sum of directional votes), and vote distribution (counts of +1, −1, 0 votes)
- Vote plot visualization (bar chart restricted to ≤30 compounds for readability)
- Explore plot showing vote distribution and reports by trend with optional filtering for consistency

## How to apply

For each compound in each study, assign a vote based on the reported fold-change or trend classification: assign +1 if fold-change > 1 or positive trend is reported, −1 if fold-change < 1 or negative trend is reported, and 0 if no significant trend or change is observed. Aggregate votes by summing across all studies for each compound to produce a final vote count. Optionally divide by the number of studies reporting on that compound to normalize the consensus score. This method requires only the compound identifier, fold-change (or trend label), and study reference; missing data are ignored during computation. Report the vote distribution (count of +1, −1, and 0 votes) alongside the total vote score to show consistency of direction across studies.

## Related tools

- **amanida** (R package that implements vote-counting via amanida_vote() and compute_amanida() functions; performs harmonized metabolite meta-analysis combining quantitative and qualitative methods) — https://github.com/mariallr/amanida
- **amanida_read** (Function within amanida package to load and parse harmonized metabolite datasets in CSV, XLS/XLSX, or TXT format with mode='qual' for qualitative analysis) — https://github.com/mariallr/amanida
- **webchem** (R package used by amanida to harmonize compound identifiers and retrieve PubChem IDs for duplicate checking before vote-counting)
- **check_names** (Function within amanida to standardize compound identifiers by converting chemical names, InChI, InChIKey, and SMILES to PubChem IDs and detecting duplicates) — https://github.com/mariallr/amanida
- **vote_plot** (Visualization function in amanida to display vote-counting results as a bar plot with optional subsetting by vote count threshold) — https://github.com/mariallr/amanida
- **explore_plot** (Visualization function in amanida to show vote distribution and reports stratified by trend, enabling detection of consistency or discrepancies across studies) — https://github.com/mariallr/amanida

## Examples

```
library(amanida); coln = c('Compound Name', 'Behaviour', 'References'); data_votes <- amanida_read('dataset.csv', mode = 'qual', coln, separator = ';'); vote_result <- amanida_vote(data_votes); vote_plot(vote_result)
```

## Evaluation signals

- Total vote score for each compound equals the algebraic sum of +1 (up-regulation), −1 (down-regulation), and 0 (no trend) votes across all studies
- Sum of vote counts (+1s, −1s, and 0s) equals the total number of studies reporting on each compound
- Vote-counting results are restricted to ≤30 compounds in vote_plot output and ≤25 compounds in explore_plot output for readability
- No votes are assigned to missing data; compounds with no reported trend are assigned 0 votes within each study
- Qualitative consensus direction (majority vote direction) aligns with the sign of the final vote score (positive = net up-regulation; negative = net down-regulation; zero = no consensus)

## Limitations

- Vote-counting discards information about effect magnitude (fold-change values > 1 or < 1 are treated identically); use quantitative meta-analysis if magnitude matters.
- The method assumes all studies are equally weighted regardless of sample size or statistical power; study size weighting is not incorporated in vote-counting as it is in amanida's quantitative Fisher p-value combination.
- Vote-counting cannot detect or report statistical significance or confidence intervals; results are ordinal descriptive measures only.
- Missing data are silently ignored, which may bias results if missingness is not random across studies or compounds.
- Compounds with discrepancies (both up- and down-regulated across studies) will have vote scores near zero, masking heterogeneity; use explore_plot to identify such inconsistencies.
- Negative fold-change values are internally transformed to positive (1/value) before vote assignment, which may obscure the original direction if not documented.

## Evidence

- [intro] Finding on vote assignment rule: "votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend"
- [intro] Workflow step: assign votes per compound: "Assign votes per compound per study: +1 for up-regulation (fold-change > 1 or positive trend), −1 for down-regulation (fold-change < 1 or negative trend), 0 for no significant trend"
- [intro] Workflow step: aggregate votes across studies: "Sum votes across all studies for each compound to produce final vote counts"
- [intro] Vote output specification: "Generate vote-counting table with compound identifier, total vote score, and vote distribution (count of +1, −1, 0 votes)"
- [intro] Rationale for qualitative meta-analysis: "Amanida also computes qualitative meta-analysis performing a vote-counting for compounds, including the option of only using identifier and trend labels"
- [readme] Vote-counting computation in README: "Compound vote-counting: votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend. The total votes are divided by the number of reports"
- [intro] Vote plot readability constraint: "output is restricted to 30 compounds to facilitate the readability"
- [intro] Explore plot readability constraint: "output is restricted to 25 compounds to facilitate the readability"
