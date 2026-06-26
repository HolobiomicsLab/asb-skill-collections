---
name: phase-i-phase-ii-transformation-rules
description: Use when when you have a parent drug's raw chemical formula and need
  to predict its likely metabolite formulas for subsequent mass spectrometry matching,
  especially in high-resolution MS workflows where exact mass matching requires known
  candidate formulas.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - R
  - MetIDfyR
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

# phase-i-phase-ii-transformation-rules

## Summary

Systematically enumerate candidate metabolite molecular formulas by applying phase I (oxidation, reduction, hydrolysis) and phase II (conjugation) biotransformation rules to a parent drug's raw chemical formula. This skill is essential for constraining the chemical search space in metabolite identification workflows when only the parent drug formula is known.

## When to use

When you have a parent drug's raw chemical formula and need to predict its likely metabolite formulas for subsequent mass spectrometry matching, especially in high-resolution MS workflows where exact mass matching requires known candidate formulas. Apply this skill upstream of spectral matching or when metabolite standards are unavailable.

## When NOT to use

- The parent drug formula is unknown or ambiguous — formula-based prediction requires exact starting composition.
- You already have experimentally observed metabolite m/z values and only need to annotate them post-hoc; use metabolite identification matching instead.
- The drug undergoes phase I/II transformations not covered by the tool's built-in rule set (e.g. rare or non-standard metabolic pathways); manual curation or literature review would be more appropriate.

## Inputs

- Parent drug raw chemical formula (string, e.g. C₂₁H₃₂N₂O₂)
- Configuration file specifying active transformation rules (R script, TEMPLATE_config.R)
- Optional: mzML mass spectrometry data file (for subsequent matching)

## Outputs

- Structured metabolite formula table (TSV or CSV format)
- Predicted metabolite candidate formulas with transformation type annotations
- Mass values derived from predicted formulas (for MS matching)

## How to apply

Load the parent drug's raw chemical formula into MetIDfyR as a TSV input file (see TEMPLATE_start_mlc.tsv). The tool systematically applies phase I biotransformation rules (oxidative and reductive modifications typical of cytochrome P450 metabolism) and phase II rules (glucuronidation, sulfation, acetylation, and other conjugations). Configure the prediction scope via a config file (TEMPLATE_config.R) specifying which transformation types to include. Execute the prediction module, which enumerates all combinatorially valid candidate formulas, then collect and format the output into a structured TSV table annotated with transformation type labels. Validate output formulas by checking they are chemically plausible (e.g., no negative atom counts, reasonable mass increments for the transformation type applied).

## Related tools

- **MetIDfyR** (R script that implements phase I and phase II biotransformation rule enumeration and metabolite formula prediction from parent drug formula) — https://github.com/agnesbrnb/MetIDfyR
- **MetApp** (Shiny application for visualization and reporting of predicted and detected metabolites) — https://github.com/GIELCH/MetApp

## Examples

```
Rscript MetIDfyR.R -i input/lgd_DIA_peak-picked.tsv -o LGD4033_results -c input/config_LGD.R
```

## Evaluation signals

- Output formulas are chemically valid: all atom counts are non-negative, molecular weight is plausible for the parent drug mass plus transformation mass delta.
- Phase I predictions (oxidation, reduction, hydrolysis) show systematic mass shifts consistent with known P450 modifications (e.g., +16 for monooxygenation, -2 for dehydration).
- Phase II predictions include expected conjugation products (e.g., parent formula + 176 for glucuronidation, +80 for sulfation).
- Output TSV schema matches expected structure: columns for predicted_formula, transformation_type, mass_shift, and traceability to parent drug.
- Predicted formulas match subsequently observed m/z values in high-resolution MS data when matched using exact mass tolerance (typically <5 ppm).

## Limitations

- MetIDfyR is tested and validated on R version 3.6.1 up to R 4.0; behavior on newer R versions may be unpredictable.
- The tool enumerates combinatorially — complex drugs with many potential transformation sites may generate very large candidate lists, requiring post-hoc filtering.
- Rule set is limited to common phase I and II pathways; drugs undergoing rare, non-standard, or species-specific metabolism may produce incomplete or inaccurate predictions.
- No changelog is available, limiting ability to track rule updates or bug fixes between versions.

## Evidence

- [other] enumerate candidate metabolite formulas based on systematic phase I and phase II biotransformation rules: "enumerate candidate metabolite formulas based on systematic phase I and phase II biotransformation rules"
- [readme] predict and detect metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest: "predict and detect metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest"
- [readme] a configuration file with the parameter (see TEMPLATE_config.R): "a configuration file with the parameter (see TEMPLATE_config.R)"
- [readme] a tsv file containing the parent drug informations (see TEMPLATE_start_mlc.tsv): "a tsv file containing the parent drug informations (see TEMPLATE_start_mlc.tsv)"
- [other] Collect and format predicted metabolite formulas and associated transformation types into a structured output table (CSV or TSV): "Collect and format predicted metabolite formulas and associated transformation types into a structured output table (CSV or TSV)"
