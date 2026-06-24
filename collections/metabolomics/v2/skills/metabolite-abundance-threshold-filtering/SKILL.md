---
name: metabolite-abundance-threshold-filtering
description: Use when you have intracellular metabolomics data paired with constraint-based
  metabolic model predictions and need to identify metabolically controlled reactions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0176
  - http://edamontology.org/topic_2258
  - http://edamontology.org/topic_3407
  tools:
  - constraint-based stoichiometric metabolic models
  - createMetabolicDataset.py
  - MassHunter ProFinder
  techniques:
  - LC-MS
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
  - build: coll_integrate_cq
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate_cq
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

# metabolite-abundance-threshold-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter metabolites and reactions based on quantification completeness and statistical abundance thresholds to ensure robust concordance analysis between reaction flux predictions and substrate availability. This skill removes incomplete or low-confidence metabolomics data before computing concordance coefficients between reaction propensity scores and feasible flux distributions.

## When to use

Apply this skill when you have intracellular metabolomics data paired with constraint-based metabolic model predictions and need to identify metabolically controlled reactions. Use it specifically when: (1) you want to compute concordance between RPS (Reaction Propensity Score based on substrate availability) and FFD (Feasible Flux Distribution); (2) your metabolomics dataset has incomplete substrate coverage across cell lines or replicates; (3) you need to filter out low-abundance metabolites that may introduce noise into substrate-flux correlation analysis.

## When NOT to use

- If your metabolomics dataset already has comprehensive coverage (all reaction substrates quantified) and no missing values, the filtering step is redundant — proceed directly to concordance analysis.
- If you are not integrating metabolomics with flux predictions; this skill is specific to multi-omics metabolic control characterization and is not appropriate for standalone metabolomics or transcriptomics analysis.
- If your research goal is to study metabolite abundance patterns independent of flux or transcriptional control — use standard metabolomics QC and normalization instead.

## Inputs

- Intracellular metabolomics quantification data (CSV format with metabolite IDs and abundance values per cell line/replicate)
- Metabolic model with reaction substrate stoichiometry (SBML or JSON format, e.g. ENGRO2)
- Metabolite ID conversion table (e.g., metsEngroVsMetabolomics.csv mapping metabolomics IDs to model metabolite IDs)
- Statistical test results from pairwise cell line metabolite comparisons (t-test p-values and log₂ fold-change ratios)

## Outputs

- Filtered metabolomics dataset (CSV) containing only reactions with complete substrate quantification
- Set of 81 reactions (in ENGRO2 context) eligible for concordance analysis after filtering
- Log₂ ratio matrix between cell line pair means for quantified metabolites (used to classify abundance direction)
- Quality-controlled metabolomics dataset ready for RPS and FFD concordance computation

## How to apply

Load intracellular metabolomics quantification data for all metabolites across all cell lines and replicates. For each reaction in the metabolic model, check whether all required substrates have quantified abundances in the metabolomics dataset. Exclude reactions with any missing substrate abundance measurements from concordance analysis. Additionally, apply a statistical fold-change threshold (log₂ ratio ≥ 1.2 between cell line pair means) to classify metabolite abundance as 'significantly different' or not, which informs the RPS calculation. Retain only reactions where substrate quantification is complete and abundance data meet quality criteria. This filtering step occurs before concordance coefficient computation and ensures that observed RPS–FFD concordance reflects genuine metabolic control rather than missing data artifacts.

## Related tools

- **constraint-based stoichiometric metabolic models** (Provides reaction substrate stoichiometry and metabolite definitions to determine which reactions have complete substrate coverage in metabolomics data)
- **createMetabolicDataset.py** (Performs the actual statistical filtering of metabolomics data, including data quality filtering, log₂ ratio computation, and output of mean abundances per cell line) — https://github.com/qLSLab/integrate
- **MassHunter ProFinder** (Performs isotopic natural abundance correction on raw LC-MS/MS data prior to metabolite quantification and filtering)

## Examples

```
python pipeline/createMetabolicDataset.py --data_quality_filter 1 --valLog 1.2 --metabolic_model ENGRO2_irrev.xml --metabolic_data metabolomics_LM.csv --dict_to_convert_metnames metsEngroVsMetabolomics.csv
```

## Evaluation signals

- Verify that the output reaction set has no missing substrate measurements: for each retained reaction, all substrates in its stoichiometric equation must appear in the filtered metabolomics CSV.
- Check that the number of retained reactions matches documented benchmarks (81 reactions for ENGRO2 model in the paper) and document the filtering-out rate to ensure thresholds are appropriate.
- Confirm that log₂ fold-change values for all retained metabolites meet the threshold (log₂ ratio ≥ 1.2 or ≤ 1.2 depending on direction) and are not NaN or undefined.
- Validate that the filtered dataset produces non-zero, interpretable RPS (Reaction Propensity Score) values computed from substrate ratios; RPS should correlate meaningfully with FFD when concordance analysis is applied.
- Cross-check filtered metabolite IDs against the conversion table (metsEngroVsMetabolomics.csv) to ensure no ID mapping errors introduced during filtering.

## Limitations

- Limited metabolite coverage in the metabolomics dataset constrains the number of reactions that can be analyzed; reactions with unmeasured substrates are automatically excluded, potentially missing important metabolic control signals.
- Enzymatic activity and allosteric regulation are not captured through metabolomics substrate abundance alone; the filtering approach relies on mass action kinetics and cannot discriminate product inhibition, cofactor/prosthetic group effects, or allosteric effects without additional experimental data.
- The quality filter threshold (log₂ ratio ≥ 1.2) and data quality filter parameter (default = 1) are user-configurable and may require optimization for datasets with different noise profiles or dynamic range; no principled guideline is provided for threshold selection across different cell types or tissues.

## Evidence

- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [results] Fig 4A reports the concordance level variations for the 81 metabolic reactions of ENGRO2 for which quantification of all substrate abundances was available: "Fig 4A reports the concordance level variations for the 81 metabolic reactions of ENGRO2 for which quantification of all substrate abundances was available"
- [results] The heatmap in Fig 4B reports the RPSvsRAS and the RPSvsFFD concordance scores for reactions having a level of concordance between RPS and FFD greater than 0.2: "reactions having a level of concordance between RPS and FFD greater than 0.2"
- [readme] valLog: value above which the ratio between the means of two cell lines are considered statistically different. Default value: 1.2: "value above which the ratio between the means of two cell lines are considered statistically different. Default value: 1.2"
- [readme] data_quality_filter: quality filter. Default value: 1 and valLog: value above which the ratio between the means of two cell lines are considered statistically different. Default value: 1.2: "data_quality_filter: quality filter. Default value: 1"
