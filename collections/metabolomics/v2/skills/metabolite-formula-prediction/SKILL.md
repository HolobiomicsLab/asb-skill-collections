---
name: metabolite-formula-prediction
description: Use when when you have a known drug's chemical formula and need to generate a comprehensive list of predicted metabolite formulas to match against experimental mzML mass spectrometry data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - R
  - MetIDfyR
  - MetApp
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.0c02281
  title: MetIDfyR
evidence_spans:
- open-source, cross-platform and versatile R script
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metidfyr_cq
    doi: 10.1021/acs.analchem.0c02281
    title: MetIDfyR
  dedup_kept_from: coll_metidfyr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c02281
  all_source_dois:
  - 10.1021/acs.analchem.0c02281
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-formula-prediction

## Summary

Predict candidate metabolite chemical formulas from a parent drug's raw formula by systematically applying phase I and phase II biotransformation rules. This skill enables rapid enumeration of plausible metabolite structures for subsequent validation against high-resolution mass spectrometry data.

## When to use

When you have a known drug's chemical formula and need to generate a comprehensive list of predicted metabolite formulas to match against experimental mzML mass spectrometry data. Apply this skill when phase I (oxidation, reduction, hydrolysis) and phase II (conjugation, acetylation) metabolic pathways are relevant to your drug class and you require a structured catalog of candidate formulas before peak-picking or metabolite detection.

## When NOT to use

- When your experimental data is already peak-picked and matched to reference metabolites; this skill generates candidate formulas, not peak detection or matching.
- When the parent drug's chemical formula is unknown or unavailable; the skill requires an accurate starting formula.
- When you lack domain knowledge to configure appropriate biotransformation rules for your drug class; misconfigured rules will produce irrelevant candidates.

## Inputs

- Parent drug chemical formula (TSV file with structure matching TEMPLATE_start_mlc.tsv)
- Configuration file specifying phase I and phase II biotransformation rules (R script, template: TEMPLATE_config.R)
- MetIDfyR R script and dependency environment

## Outputs

- Structured TSV or CSV table of predicted metabolite formulas
- Associated transformation type annotations for each predicted metabolite

## How to apply

Load the parent drug's raw chemical formula into MetIDfyR as a TSV file (see TEMPLATE_start_mlc.tsv). Configure biotransformation rules via a config file (TEMPLATE_config.R) specifying which phase I and phase II transformations to apply. Execute the MetIDfyR R script with command-line arguments pointing to the input formula file, output directory, and config file. The script systematically enumerates all combinatorial metabolite formulas by applying each selected transformation rule to the parent formula. Collect the resulting predicted metabolite formulas and their associated transformation types into a structured TSV output table; this output serves as the reference set for matching against detected peaks in subsequent mass spectrometry analysis.

## Related tools

- **MetIDfyR** (Core R script that implements systematic biotransformation rule application and metabolite formula enumeration) — https://github.com/agnesbrnb/MetIDfyR
- **MetApp** (Shiny visualization application for displaying and filtering predicted metabolites and generating PDF reports) — https://github.com/GIELCH/MetApp
- **R** (Execution environment (version 3.6.1 or later, tested through R 4.0))

## Examples

```
Rscript MetIDfyR.R -i input/lgd_DIA_peak-picked.tsv -o LGD4033_results -c input/config_LGD.R
```

## Evaluation signals

- Output TSV contains all predicted metabolite formulas with no duplicate entries and one transformation type per row
- Predicted formulas are chemically valid (respecting valence and oxidation state rules; Rdisop package validates structure)
- Row count in output table matches the combinatorial product of (parent formula) × (number of applicable transformations)
- Transformation type annotations match the configured phase I and phase II rules (e.g., 'oxidation', 'acetylation', 'conjugation')
- Output file is readable as TSV and integrable into downstream mass spectrometry peak-matching workflows (e.g., as input to MetApp or custom m/z matching scripts)

## Limitations

- Prediction accuracy depends on completeness and correctness of configured biotransformation rules; missing or misconfigured rules will omit plausible metabolites.
- The skill generates formulas only; it does not validate whether predicted metabolites are thermodynamically feasible or enzymatically probable for the specific organism or tissue.
- No changelog is provided in the repository, making it difficult to track which biotransformation rules or parameter defaults have changed across versions.
- Computational cost scales with the number of applicable transformation rules and their combinatorial interactions; highly complex rule sets may be slow on large datasets.

## Evidence

- [readme] MetIDfyR predicts and detects metabolites in mass spectrometry data based on the raw formula of the drug of interest: "open-source, cross-platform and versatile R script to predict and detect metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest"
- [other] Systematic biotransformation rules are applied to enumerate candidate metabolite formulas: "Execute MetIDfyR's prediction module in R to enumerate candidate metabolite formulas based on systematic phase I and phase II biotransformation rules"
- [other] Output is formatted as structured TSV/CSV with metabolite formulas and transformation types: "Collect and format predicted metabolite formulas and associated transformation types into a structured output table (CSV or TSV)"
- [readme] Configuration file and parent drug formula are required inputs: "Need a configuration file with the parameter (see TEMPLATE_config.R) and a tsv file containing the parent drug informations (see TEMPLATE_start_mlc.tsv)"
- [readme] Execution command-line interface: "Rscript MetIDfyR.R -i path-to-input-file -o output-directory -c config-file"
