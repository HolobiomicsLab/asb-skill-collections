---
name: biotransformation-enumeration
description: Use when you have a known parent drug chemical formula and aim to predict its metabolite landscape prior to or during high-resolution mass spectrometry analysis (mzML).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3520
  tools:
  - R
  - MetIDfyR
  - MetApp
  - R (v3.6.1 – v4.0)
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

# Biotransformation Enumeration

## Summary

Systematically enumerate candidate metabolite chemical formulas from a parent drug's raw formula by applying phase I and phase II biotransformation rules. This skill predicts the chemical space of plausible metabolites for subsequent mass spectrometry validation.

## When to use

Apply this skill when you have a known parent drug chemical formula and aim to predict its metabolite landscape prior to or during high-resolution mass spectrometry analysis (mzML). Use it to generate a reference set of expected phase I (oxidation, reduction, hydrolysis) and phase II (conjugation) transformation products to guide feature annotation and reduce false-positive metabolite assignments.

## When NOT to use

- Input formula is unknown or unavailable — the skill requires an explicit, validated parent drug formula as a starting point.
- Only phase III (transporter-mediated) metabolism is relevant to your organism or context — MetIDfyR focuses on phase I/II chemistry, not active transport or efflux.
- You seek to identify metabolites de novo from mass spectra without prior knowledge of the parent drug — this skill is a top-down formula prediction tool, not a spectral deconvolution or database search tool.

## Inputs

- parent drug chemical formula (raw molecular composition string or as field in TSV)
- configuration file specifying biotransformation rule parameters (TEMPLATE_config.R)
- optional: mzML file containing mass spectrometry sample data for matching

## Outputs

- predicted metabolite formulas (enumerated set of chemical compositions)
- transformation type annotations (phase I or II biotransformation labels)
- structured output table (TSV or CSV) with metabolite formula, transformation type, and metadata

## How to apply

Load the parent drug's raw chemical formula (e.g. from a TSV file with molecular composition data) into MetIDfyR's prediction module in R. Execute the biotransformation rule engine, which systematically applies phase I and phase II transformation functions to enumerate candidate metabolite formulas. Collect predicted formulas and their associated transformation types (e.g. 'hydroxylation', 'glucuronidation') into a structured output table (CSV or TSV). The enumeration is exhaustive within the rule set, so the output represents all possible single-transformation products; subsequent mass spectrometry matching will filter to observed species.

## Related tools

- **MetIDfyR** (Executes the biotransformation rule engine; enumerates phase I and II metabolite formulas from parent drug input) — https://github.com/agnesbrnb/MetIDfyR
- **MetApp** (Visualization and reporting of predicted and annotated metabolites from MetIDfyR output; generates PDF reports) — https://github.com/GIELCH/MetApp
- **R (v3.6.1 – v4.0)** (Runtime environment; dependency manager (pacman) and computation) — https://www.r-project.org/

## Examples

```
Rscript MetIDfyR.R -i input/lgd_DIA_peak-picked.tsv -o LGD4033_results -c input/config_LGD.R
```

## Evaluation signals

- Output TSV/CSV contains all expected phase I transformation types (e.g. 'hydroxylation', 'oxidation', 'demethylation') with corresponding modified formulas
- Output TSV/CSV contains all expected phase II transformation types (e.g. 'glucuronidation', 'sulfation', 'acetylation') with corresponding conjugated formulas
- Predicted metabolite formulas follow chemical mass rules (e.g. hydroxylation adds O1H1; glucuronidation adds C6H8O6 or isotopic variant)
- Output row count reflects plausible metabolite burden (typically 10–100+ metabolites per drug depending on rule depth and parent complexity)
- When matched against real mzML spectra, predicted metabolite masses align with observed m/z values within instrument mass accuracy (e.g. <5 ppm for high-resolution MS)

## Limitations

- Enumeration is limited to explicitly defined biotransformation rules in the configuration; unknown or organism-specific metabolic pathways will not be predicted.
- Tool was developed and tested on R versions 3.6.1 to 4.0; compatibility with R >4.0 is not guaranteed and may require dependency updates.
- No changelog is available in the repository, making it difficult to track which biotransformation rule sets or bug fixes are included in any given version.
- Phase I and II predictions do not account for stereo- or regio-selectivity; all chemically feasible transformation positions are enumerated as separate entries.
- Output requires subsequent validation against mass spectrometry data; predicted formulas alone do not confirm metabolite existence or abundance.

## Evidence

- [intro] MetIDfyR predicts and detects metabolites in mass spectrometry data based on the raw formula of the drug of interest: "predict and detect metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest"
- [readme] Biotransformation rules are applied systematically to enumerate candidate metabolite formulas: "predict and detect metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest"
- [full_text] Tool applies phase I and phase II biotransformation rules: "enumerate candidate metabolite formulas based on systematic phase I and phase II biotransformation rules"
- [full_text] Output is a structured table with predicted metabolite formulas and transformation types: "Collect and format predicted metabolite formulas and associated transformation types into a structured output table (CSV or TSV)"
- [readme] Configuration file is required to parameterize biotransformation rules: "a configuration file with the parameter (see TEMPLATE_config.R)"
- [readme] Parent drug information is provided as a TSV file: "a tsv file containing the parent drug informations (see TEMPLATE_start_mlc.tsv)"
