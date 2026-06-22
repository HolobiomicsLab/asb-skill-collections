---
name: lipid-concentration-normalization
description: Use when your lipidomics experiment includes spiked internal lipid standards with known absolute concentrations, and you have a data matrix of signal intensities (samples × lipids) from LipidSearch or LIQUID output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3564
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0625
  tools:
  - LipidSearch
  - LIQUID
  - LIPID MAPS
  - ADViSELipidomics
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btac706
  title: ADViSELipidomics
evidence_spans:
- outputs from LipidSearch and LIQUID for lipid identification and quantification
- parsing lipid species (using LIPID MAPS classification)
- ADViSELipidomics can normalize the data matrix, providing absolute values of concentration per lipid and sample
- ADViSELipidomics is a novel Shiny app for the preprocessing, analysis, and visualization of lipidomics data.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_adviselipidomics_cq
    doi: 10.1093/bioinformatics/btac706
    title: ADViSELipidomics
  dedup_kept_from: coll_adviselipidomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac706
  all_source_dois:
  - 10.1093/bioinformatics/btac706
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-concentration-normalization

## Summary

Convert raw lipidomics signal intensities to absolute lipid concentration values by normalizing against internal lipid standards. This skill bridges quantitative lipidomics identification (from LipidSearch or LIQUID) to concentration-based downstream analysis.

## When to use

Your lipidomics experiment includes spiked internal lipid standards with known absolute concentrations, and you have a data matrix of signal intensities (samples × lipids) from LipidSearch or LIQUID output. Use this skill when you need absolute concentration per lipid and sample rather than relative intensity ranks for statistical comparison or biomarker discovery.

## When NOT to use

- Your experiment does not include internal lipid standards or their concentrations are unknown.
- Your input is already a relative intensity matrix and standards are not available in raw data.
- You only need qualitative lipid identification without quantitative concentration estimates.

## Inputs

- Raw lipidomics data matrix (samples × lipids) with signal intensities from LipidSearch or LIQUID
- Internal lipid standard reference table with expected absolute concentrations
- LIPID MAPS lipid species annotations or identifiers

## Outputs

- Normalized lipid concentration matrix (samples × lipids) with absolute concentration values
- Normalization factors applied per lipid class or globally
- Annotated concentration matrix with LIPID MAPS classification

## How to apply

Load the raw lipidomics data matrix (samples × lipids, intensity values) and the internal standard reference table containing expected absolute concentrations for each standard lipid species. Identify which lipids in your data matrix correspond to internal standards. For each standard, compute a normalization factor as the ratio of expected absolute concentration (from reference) to the observed mean intensity across samples. Apply this factor to all lipid measurements in the corresponding lipid class or use a global factor if a single standard is representative. The output is a concentration matrix with the same dimensions as the input, annotated with LIPID MAPS classification, ready for differential abundance testing or exploratory analysis.

## Related tools

- **LipidSearch** (Generates raw lipidomics data matrix and internal standard intensities from mass spectrometry output)
- **LIQUID** (Alternative tool for lipid identification and quantification, producing data matrix compatible with normalization workflow)
- **LIPID MAPS** (Provides standardized lipid species classification used to annotate and organize normalized concentration matrix) — https://www.lipidmaps.org
- **ADViSELipidomics** (Shiny application implementing internal standard normalization as part of preprocessing pipeline) — https://github.com/ShinyFabio/ADViSELipidomics

## Evaluation signals

- Normalized values are in absolute concentration units (e.g., µM, pmol) matching the internal standard reference scale, not intensity counts.
- Internal standard lipids themselves show normalized intensity = expected concentration (within measurement precision), validating normalization factor calculation.
- All samples and lipids in the output matrix are present with no missing values introduced by normalization (unless originally missing).
- Relative ranking or fold-changes between samples are preserved after normalization compared to raw intensity ratios, confirming linear scaling.
- Concentration values are non-negative and within biologically plausible ranges for the lipid class and tissue/biofluid type.

## Limitations

- Normalization accuracy depends critically on the stability and accurate quantification of internal standards; degraded or misidentified standards will propagate errors.
- A single internal standard may not accurately represent the ionization efficiency or response of chemically diverse lipid classes; class-specific standards improve accuracy but increase complexity.
- Lipids not represented by an internal standard rely on interpolation or global factors, reducing confidence in their absolute values.
- Matrix effects and ion suppression can vary between samples; this method assumes constant response across the cohort unless sample-specific corrections are applied.

## Evidence

- [intro] Data normalization using internal lipid standards: "In the presence of internal lipid standards in the experiment, ADViSELipidomics can normalize the data matrix, providing absolute values of concentration per lipid and sample."
- [other] Workflow steps for internal standard normalization: "For each lipid species, compute a normalization factor as the ratio of expected absolute concentration (from standard reference) to observed intensity for the corresponding internal standard. Apply"
- [other] Input and output specifications: "Load the lipidomics data matrix (samples × lipids) and internal standard reference table from LipidSearch or LIQUID output. Output the normalized concentration matrix with lipids annotated using"
- [readme] Tool integration for normalization: "ADViSELipidomics copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification"
