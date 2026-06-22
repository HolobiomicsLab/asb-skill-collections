---
name: internal-standard-intensity-extraction
description: Use when you have lipidomics data from LipidSearch or LIQUID output that includes internal lipid standards spiked into samples at known concentrations, and your goal is to convert relative intensities to absolute concentration values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0591
  - http://edamontology.org/topic_3172
  tools:
  - LipidSearch
  - LIQUID
  - ADViSELipidomics
derived_from:
- doi: 10.1093/bioinformatics/btac706
  title: ADViSELipidomics
evidence_spans:
- outputs from LipidSearch and LIQUID for lipid identification and quantification
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

# internal-standard-intensity-extraction

## Summary

Extract and identify signal intensities for internal lipid standards across all samples in a lipidomics data matrix, serving as the foundation for computing normalization factors that convert raw intensities to absolute lipid concentrations. This skill bridges raw instrument output and quantitative lipidomics by anchoring measurements to known reference standards.

## When to use

Apply this skill when you have lipidomics data from LipidSearch or LIQUID output that includes internal lipid standards spiked into samples at known concentrations, and your goal is to convert relative intensities to absolute concentration values. Specifically, use it when internal standard signals are present in the data matrix and you need to establish the normalization baseline before computing per-lipid normalization factors.

## When NOT to use

- The experiment does not include spiked internal lipid standards (use relative intensity normalization or other approaches instead).
- Internal standard intensities are already pre-computed or aggregated; skip directly to normalization factor computation.
- Raw data are already in absolute concentration units rather than relative intensities.

## Inputs

- Lipidomics data matrix (samples × lipids intensities) from LipidSearch or LIQUID
- Internal lipid standard reference table (standard identity, expected absolute concentration, lipid class)
- Sample metadata (sample identifiers)

## Outputs

- Extracted internal standard intensity submatrix (internal standards × samples)
- Mapping of internal standards to their expected absolute concentrations
- Quality control flags for missing or zero-intensity standards per sample

## How to apply

Load the lipidomics data matrix (samples × lipids) from LipidSearch or LIQUID output alongside the internal standard reference table that specifies which lipid species are standards and their expected absolute concentrations. Identify all rows in the data matrix corresponding to internal standard lipid species by cross-referencing against the reference table. Extract the signal intensity values for each internal standard across all samples, creating a standards-by-samples intensity submatrix. Verify that all expected internal standards are present and have measurable signal (non-zero intensities) in every sample; missing or zero-intensity standards indicate failed normalization and should be flagged. Store these intensity values indexed by standard identity and sample identifier for downstream computation of per-lipid normalization factors.

## Related tools

- **LipidSearch** (Source of lipidomics data matrix and lipid identification output; provides raw intensity measurements and lipid annotations)
- **LIQUID** (Alternative source of lipidomics data matrix and lipid identification output; provides raw intensity measurements and lipid annotations)
- **ADViSELipidomics** (Shiny application that integrates standard intensity extraction into the normalization workflow; automates identification and extraction of internal standard signals from LipidSearch or LIQUID outputs) — https://github.com/ShinyFabio/ADViSELipidomics

## Evaluation signals

- All expected internal standards from the reference table are successfully located in the data matrix and matched by lipid identity (e.g., using LIPID MAPS classification).
- Extracted intensity values for each internal standard are non-zero across all samples, indicating adequate signal strength for normalization.
- Intensity values for replicate internal standards (if present) show consistent magnitude and rank-order across samples, indicating measurement reproducibility.
- No sample has missing intensity data for any internal standard; completeness check confirms no NaN or null values in the extracted submatrix.
- Extracted standards can be successfully paired with their expected absolute concentrations from the reference table, enabling downstream ratio computation for normalization factors.

## Limitations

- Internal standard identification relies on exact matching to the reference table; misannotations or naming inconsistencies between the data matrix and reference table will cause standards to be missed.
- If internal standard intensities are extremely low or undetectable in some samples, those samples may fail normalization or produce unreliable absolute concentration estimates.
- The skill assumes internal standards are labeled and differentiated from endogenous lipids; co-eluting or structurally ambiguous standards may be incorrectly extracted or confused with endogenous species.
- Extraction accuracy depends on the quality and completeness of the internal standard reference table; outdated or incomplete reference data will compromise downstream normalization.

## Evidence

- [intro] internal_standard_extraction_definition: "Identify and extract signal intensities for internal lipid standards across all samples."
- [intro] normalization_workflow_context: "Load the lipidomics data matrix (samples × lipids) and internal standard reference table from LipidSearch or LIQUID output."
- [intro] absolute_concentration_foundation: "In the presence of internal lipid standards in the experiment, ADViSELipidomics can normalize the data matrix, providing absolute values of concentration per lipid and sample."
- [readme] standards_normalization_usage: "It copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification"
