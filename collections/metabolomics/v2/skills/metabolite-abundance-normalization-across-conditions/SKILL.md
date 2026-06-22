---
name: metabolite-abundance-normalization-across-conditions
description: Use when you have intracellular metabolomics abundance data (measured metabolite concentrations) from multiple biological replicates collected from two or more cell lines or conditions, and you need to create a normalized, cell-line-level metabolite dataset before computing Reaction Propensity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - INTEGRATE
  - Agilent 1290 Infinity UHPLC system + Agilent 6550 iFunnel Q-TOF mass spectrometer
  - constraint-based stoichiometric metabolic models (e.g., ENGRO2)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-abundance-normalization-across-conditions

## Summary

Normalize intracellular metabolite abundance measurements across cell lines or biological conditions to enable comparative analysis of metabolic regulation. This skill aggregates replicate measurements within each condition and scales values to a common reference (e.g., maximum observed abundance) to render metabolite concentrations directly comparable for downstream reaction propensity scoring.

## When to use

You have intracellular metabolomics abundance data (measured metabolite concentrations) from multiple biological replicates collected from two or more cell lines or conditions, and you need to create a normalized, cell-line-level metabolite dataset before computing Reaction Propensity Scores (RPS) or other stoichiometry-based metabolic predictions. This is essential when metabolomics data will be integrated with transcriptomics and constraint-based modeling to discriminate transcriptionally-controlled from metabolically-controlled metabolic fluxes.

## When NOT to use

- Extracellular metabolomics data (spent medium concentrations): extracellular fluxes follow different kinetics and are integrated via YSI bioanalyzer measurements and stoichiometric constraints, not intracellular normalization.
- Metabolite data already normalized or pre-processed by the measurement platform: verify that raw abundances are provided; re-normalization can introduce bias.
- Single replicate per condition: aggregation requires ≥2 biological replicates; with only one replicate, skip aggregation and proceed directly to per-condition normalization.

## Inputs

- Intracellular metabolomics abundance data (LC-MS/MS or equivalent; metabolite concentrations per replicate per cell line, e.g. CSV or TSV)
- List of cell line or condition identifiers
- List of biological replicate labels (e.g., ['_A', '_B'])
- Optional: data quality filter threshold and metabolite-to-model ID mapping file

## Outputs

- Normalized metabolite abundance table (metabolites × cell lines, values in [0, 1])
- Aggregated (mean/median) abundance per metabolite per cell line before normalization (optional, for reporting)
- Log of excluded metabolites and replicates (due to missing data or quality filters)

## How to apply

First, load the intracellular metabolomics abundance dataset organized with metabolites as rows and biological replicates grouped by condition/cell line as columns. Aggregate replicate measurements within each cell line using median or mean (the article indicates both approaches are acceptable, though median is recommended to reduce outlier sensitivity). Next, normalize metabolite abundances within each metabolite across all cell lines by dividing by the maximum abundance value observed for that metabolite, yielding values in the range [0, 1]. This normalization ensures that relative differences in substrate availability are comparable across cell lines without bias from absolute measurement scale. Quality filters can be applied at the replicate level (e.g., excluding metabolites with missing measurements in any cell line) before aggregation. Output the normalized dataset as a table with metabolites as rows, cell lines as columns, and normalized abundance values as entries—this table then serves as input to Reaction Propensity Score (RPS) computation.

## Related tools

- **INTEGRATE** (Framework that uses normalized metabolomics data to compute Reaction Propensity Scores via mass action law; output from this normalization skill feeds directly into Step 9 (Create metabolomic statistical test dataset) and Step 10 (Concordance data analysis)) — https://github.com/qLSLab/integrate
- **Agilent 1290 Infinity UHPLC system + Agilent 6550 iFunnel Q-TOF mass spectrometer** (Instrument platform used to measure intracellular metabolite abundances (LC-MS/MS); data from this instrument is the raw input to this normalization skill)
- **constraint-based stoichiometric metabolic models (e.g., ENGRO2)** (Metabolic network model used downstream to map metabolite IDs and compute RPS scores from normalized abundances; model stoichiometry is required to interpret which metabolites are substrates for each reaction)

## Evaluation signals

- All normalized values fall in the range [0, 1]; maximum normalized value for each metabolite across all cell lines = 1.0.
- No NaN or Inf values in the output table; metabolites with missing measurements in any cell line are either excluded entirely or flagged with a consistent sentinel value (e.g., NA).
- Aggregated (mean/median) replicate values are present for each metabolite–cell-line pair; check that replicate counts and aggregation method are consistent across all pairs.
- Row and column labels match the input metabolite IDs and cell line names; verify that metabolite IDs align with the stoichiometric metabolic model before downstream RPS computation.
- Distribution of normalized values is similar across cell lines (no cell line systematically skewed toward 0 or 1); identify and document any cell lines with consistently low or high abundance signatures.

## Limitations

- If a single metabolite is missing from the metabolomics measurements (not measured in any replicate of a cell line), any reaction that depends on that metabolite as a substrate is omitted from the downstream Reaction Propensity Score dataset, reducing coverage of metabolic reactions.
- Normalization by maximum value assumes the cell line with the highest abundance of a metabolite reflects the true dynamic range; outlier cell lines with extreme values can compress the range for other cell lines.
- Aggregation by mean or median is sensitive to replicate quality and the presence of technical outliers; replicates should pass quality control (e.g., LC-MS peak detection, retention time alignment) before aggregation.
- Normalization does not account for cofactors (ATP, NAD+, etc.) whose absolute levels may vary dramatically across cell lines but are often treated as pool metabolites in constraint-based models; consider stratifying normalization by metabolite functional class if cofactor regulation is a focus.
- Cross-cell-line normalization assumes metabolite measurements are on a comparable absolute scale; batch effects from different MS runs or measurement sessions may bias relative comparisons and should be corrected (e.g., z-score per batch) before normalization.

## Evidence

- [other] For each metabolic reaction and each cell line, identify all substrate metabolites from the model's stoichiometry and retrieve their measured intracellular concentrations; omit reactions missing one or more substrate abundance measurements.: "identify all substrate metabolites from the model's stoichiometry and retrieve their measured intracellular concentrations; omit reactions missing one or more substrate"
- [other] Aggregate RPS values across biological replicates within each cell line (using median or mean as appropriate) to produce a cell-line-level RPS score for each reaction.: "Aggregate RPS values across biological replicates within each cell line (using median or mean as appropriate)"
- [other] Normalize RPS scores within each reaction across all cell lines by dividing by the maximum RPS value observed for that reaction.: "Normalize RPS scores within each reaction across all cell lines by dividing by the maximum RPS value observed for that reaction"
- [results] If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset: "If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset"
- [intro] INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes: "INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability"
- [abstract] The pipeline discriminates whether differential expression of metabolic enzymes originates differences in metabolic fluxes versus whether differences in substrate availability translate into differences in metabolic fluxes: "differences in substrate availability translate into differences in metabolic fluxes"
