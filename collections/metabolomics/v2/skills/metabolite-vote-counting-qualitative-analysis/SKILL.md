---
name: metabolite-vote-counting-qualitative-analysis
description: Use when you have metabolomic results from multiple studies with only compound identifiers, directional trend labels (up-regulated, down-regulated, or no trend), and bibliographic references — and you want to quantify agreement on metabolite behavior direction across studies without requiring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0821
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

# metabolite-vote-counting-qualitative-analysis

## Summary

Qualitative meta-analysis method that assigns directional votes (+1, −1, 0) to metabolites across multiple studies based on trend classification, then sums votes per compound to produce a consensus measure of consistency and direction. Used when raw data or standard deviations are unavailable but trend direction and study counts are present.

## When to use

Apply this skill when you have metabolomic results from multiple studies with only compound identifiers, directional trend labels (up-regulated, down-regulated, or no trend), and bibliographic references — and you want to quantify agreement on metabolite behavior direction across studies without requiring p-values, fold-changes, or study sizes. Particularly valuable when comparing studies where only qualitative trend information is disclosed.

## When NOT to use

- When quantitative effect sizes (fold-change, p-values) are available: use weighted quantitative meta-analysis instead to leverage statistical power and effect magnitude.
- When analyzing a single study or single metabolite: vote-counting requires multiple studies and compounds to provide meaningful consensus signals.
- When the goal is effect size estimation or statistical significance testing: vote-counting is qualitative only and does not produce point estimates or confidence intervals.

## Inputs

- Harmonized metabolite dataset (csv, xls/xlsx, or txt format)
- Columns: compound identifier (name, InChI, InChIKey, or SMILES), trend label (up-regulated/down-regulated/no trend), bibliographic reference
- Optional: harmonized compound IDs (PubChem format) from prior check_names() step

## Outputs

- Vote-counting table with columns: compound identifier, total vote score, count of +1 votes, count of −1 votes, count of 0 votes, number of reports
- S4 object (amanida result) with @vote slot containing vote-counting results
- Vote plot visualization (bar chart of vote counts, limited to 30 compounds for readability)
- Explore plot visualization (mixed-mode showing compounds with discrepancies and vote distribution)

## How to apply

Load the harmonized metabolite dataset using amanida_read() in mode='qual' with columns: compound identifier, trend label (up/down-regulated or no trend), and reference. Assign votes per compound per study: +1 for up-regulation, −1 for down-regulation, and 0 for no significant trend. Sum the votes across all studies for each compound to obtain the final vote count. The result is typically divided by the number of reports to produce a normalized consensus score. Generate a vote-counting table showing compound identifier, total vote score, count of +1 votes, count of −1 votes, count of 0 votes, and the number of studies reporting each compound. The interpretation: compounds with vote sums close to the number of studies (all +1) or far below zero (all −1) show strong directional consistency; sums near zero indicate conflicting trends across studies.

## Related tools

- **amanida** (R package providing amanida_read(), amanida_vote(), vote_plot(), and explore_plot() functions for qualitative vote-counting meta-analysis) — https://github.com/mariallr/amanida
- **R** (Statistical computing environment in which amanida functions are executed)
- **webchem** (Optional: used by check_names() to harmonize compound identifiers to PubChem IDs before vote-counting)
- **PubChem** (Reference database for standardizing metabolite identifiers across studies)

## Examples

```
coln = c("Compound Name", "Behaviour", "References")
data_votes <- amanida_read("metabolites_qual.csv", mode = "qual", coln, separator = ",")
vote_result <- amanida_vote(data_votes)
vote_plot(vote_result)
explore_plot(vote_result, type = "mix", counts = 1)
```

## Evaluation signals

- Vote-counting table contains all input compounds with no missing entries; each compound row sums correctly (sum of +1, −1, 0 counts equals total reports for that compound).
- Vote scores range from −(number of studies) to +(number of studies); compounds with all concordant trends show vote = ±(number of reports), while discordant compounds show vote closer to 0.
- Vote plot and explore plot visualizations render without errors and restrict output to ≤30 and ≤25 compounds respectively for readability; explore plot with type='mix' correctly identifies and highlights compounds with mixed up/down trends.
- Cross-validation: compounds appearing in vote-counting output match the input dataset; no spurious compounds are introduced; compound identifiers match the input exactly (or are correctly mapped if PubChem harmonization was applied).
- Consistency check: compounds with vote = +(number of reports) appear as fully up-regulated in all explore plot and vote plot outputs; compounds with vote = −(number of reports) appear as fully down-regulated; compounds with mixed votes show heterogeneous trend distribution in explore plot.

## Limitations

- Vote-counting is a qualitative, unweighted method: it treats all studies equally regardless of sample size, statistical power, or effect magnitude; cannot incorporate p-values or confidence intervals.
- Sensitive to discrepant trend assignments: if the same study reports a metabolite as both up- and down-regulated across different analyses or subgroups, vote counts may cancel out, obscuring the true inconsistency.
- Requires harmonized compound identifiers: if input identifiers are not standardized (e.g., chemical name variants, synonym ambiguity), duplicates may be missed, inflating vote counts.
- Vote plot and explore plot outputs are truncated to 30 and 25 compounds respectively; large metabolomic datasets require manual filtering or multiple invocations to inspect all compounds.
- No statistical significance test: vote-counting does not provide p-values, confidence intervals, or a quantitative null hypothesis framework; consensus is measured only by direction consistency, not statistical evidence strength.

## Evidence

- [intro] votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend: "the vote-counting, that is computed by the sum of votes assigned as follows: votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend"
- [other] Assign votes per compound per study, then sum across all studies for each compound: "Assign votes per compound per study: +1 for up-regulation (fold-change > 1 or positive trend), −1 for down-regulation (fold-change < 1 or negative trend), 0 for no significant trend. 3. Sum votes"
- [intro] Qualitative meta-analysis performs vote-counting for compounds using identifier and trend labels: "Amanida also computes qualitative meta-analysis performing a vote-counting for compounds, including the option of only using identifier and trend labels"
- [readme] amanida_read supports mode='qual' with compound identifier, trend, and reference columns: "For qualitative meta-analysis include the following parameters: Indicate mode = "qual" coln: vector containing the column names, which need to be in this order: Id: compound name or unique"
- [intro] Vote plot and explore plot are restricted to 30 and 25 compounds for readability: "Vote plot output is restricted to 30 compounds to facilitate the readability output is restricted to 25 compounds to facilitate the readability"
- [readme] Vote-counting result is accessed via @vote slot of amanida result object: "In this step you will obtain an S4 object with one table: vote-counting access by `vote_results@vote`"
- [readme] Explore plot type='mix' identifies compounds with discrepancies and vote-counting: "type = "mix": subset the data by a cut-off value indicated by the counts parameter and show compounds with discrepancies (reports up-regulated and down-regulated)"
- [readme] Vote-counting divided by number of reports in amanida documentation: "Compound vote-counting: votes are +1 for up-regulation, -1 for down-regulation and 0 if no trend. The total votes are divided by the number of reports."
