---
name: chemical-formula-manipulation
description: Use when when you have a parent drug's raw chemical formula and need
  to predict its potential metabolites in mass spectrometry data (mzML format) to
  match against observed peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0820
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3375
  tools:
  - R
  - MSnbase
  - Rdisop
  - MetApp
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-formula-manipulation

## Summary

Systematically enumerate candidate metabolite chemical formulas from a parent drug's raw formula by applying phase I and phase II biotransformation rules. This skill enables high-throughput metabolite prediction for mass spectrometry-based drug metabolism studies.

## When to use

When you have a parent drug's raw chemical formula and need to predict its potential metabolites in mass spectrometry data (mzML format) to match against observed peaks. Apply this skill when performing untargeted metabolite detection or when validating metabolite hypotheses against high-resolution MS data.

## When NOT to use

- When the parent drug formula is unavailable or ambiguous; MetIDfyR requires a precise starting formula.
- When working with low-resolution MS data that cannot resolve mass differences between predicted metabolites (requires accurate mass for filtering candidate formulas).
- When mzML files have not been peak-picked; the tool expects preprocessed peak-picked mzML input.

## Inputs

- Parent drug raw chemical formula (string or from TSV file)
- Configuration file (R script with parameters: TEMPLATE_config.R)
- mzML file containing mass spectrometry sample data
- TSV file with parent drug information (TEMPLATE_start_mlc.tsv)

## Outputs

- Structured table (CSV or TSV) of predicted metabolite formulas
- Associated biotransformation types for each predicted metabolite
- Annotated mass spectrometry peaks matched to predicted formulas

## How to apply

Load the drug's raw chemical formula (e.g., from a TSV file with parent drug information) into MetIDfyR's prediction module in R. The module systematically applies phase I (oxidation, reduction, hydrolysis) and phase II (conjugation) biotransformation rules to enumerate all plausible metabolite formulas. Execute the prediction with a configuration file specifying parameters, then collect predicted metabolite formulas and their associated transformation types into a structured output table (CSV or TSV). Validate predictions by matching generated formulas against mass peaks extracted from the mzML file, using mass accuracy tolerance (typically in ppm range) as a filter criterion.

## Related tools

- **R** (Execution environment and scripting language for running MetIDfyR formula enumeration and biotransformation rule application) — https://www.r-project.org/
- **MSnbase** (R package dependency for parsing and processing mzML mass spectrometry data files)
- **Rdisop** (R package dependency for precise isotope distribution and formula calculation)
- **MetApp** (Shiny application for visualization and interactive exploration of predicted and detected metabolites) — https://github.com/GIELCH/MetApp

## Examples

```
Rscript MetIDfyR.R -i input/lgd_DIA_peak-picked.tsv -o LGD4033_results -c input/config_LGD.R
```

## Evaluation signals

- Output TSV contains all predicted metabolite formulas with corresponding parent formula, transformation type, and mass delta.
- Number of predicted metabolites matches expected enumeration given the biotransformation rule set (phase I + phase II rules applied).
- Predicted metabolite masses match observed peaks in mzML data within the configured mass accuracy tolerance (verify via mass error in ppm).
- Transformation type annotations correctly map each predicted formula to its corresponding phase I or phase II reaction (e.g., +16 for oxidation, +162 for glucuronidation).
- Output can be successfully imported into MetApp visualization without schema errors or missing required columns.

## Limitations

- MetIDfyR has been developed and tested on R versions 3.6.1 to 4.0; compatibility with newer R versions is not explicitly documented.
- The tool enumerates formulas but does not validate stereochemistry or confirm that predicted metabolites are biologically feasible or observed in vivo.
- Prediction accuracy depends on the completeness and accuracy of the configured biotransformation rules; phase I and phase II rules are user-configurable and may require domain expertise to customize.
- No changelog is available, making it difficult to track bug fixes or method refinements across versions.

## Evidence

- [intro] MetIDfyR predicts and detects metabolites in mass spectrometry data based on the raw formula of the drug of interest: "predict and detect metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest"
- [readme] Systematic enumeration of candidate metabolite formulas using biotransformation rules: "enumerate candidate metabolite formulas based on systematic phase I and phase II biotransformation rules"
- [readme] Output is a structured table of predicted metabolites with transformation types: "Collect and format predicted metabolite formulas and associated transformation types into a structured output table (CSV or TSV)"
- [readme] MetIDfyR is an open-source R script: "MetIDfyR is an open-source, cross-platform and versatile R script to predict and detect metabolites in mass spectrometry data"
- [readme] Requires configuration file, mzML file, and parent drug information file as inputs: "Need - a configuration file with the parameter (see TEMPLATE_config.R). - a mzML file containing the sample informations - a tsv file containing the parent drug informations (see"
- [readme] Command-line invocation syntax for running the tool: "Rscript MetIDfyR.R -i path-to-input-file -o output-directory -c config-file"
