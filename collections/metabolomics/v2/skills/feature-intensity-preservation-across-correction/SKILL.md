---
name: feature-intensity-preservation-across-correction
description: Use when when you have loaded a raw MS quantification table (feature-by-sample
  intensity matrix) into QuantyFey and are applying drift-correction strategies (Internal
  Standard correction, statistical drift correction, Custom Bracketing, or Weighted
  Bracketing) but need to maintain traceability.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Shiny
  - QuantyFey
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1016/j.aca.2025.344571
  title: quantyfey
evidence_spans:
- '**QuantyFey** is a Shiny application for the **visualization, analysis, and quantification**
  of **mass spectrometry (MS) data**'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_quantyfey_cq
    doi: 10.1016/j.aca.2025.344571
    title: quantyfey
  dedup_kept_from: coll_quantyfey_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.aca.2025.344571
  all_source_dois:
  - 10.1016/j.aca.2025.344571
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-intensity-preservation-across-correction

## Summary

Preserve feature identifiers and sample metadata while applying intensity drift correction strategies to mass spectrometry quantification matrices. This skill ensures that drift-corrected intensity values retain their association with specific analytes and experimental samples throughout the correction workflow.

## When to use

When you have loaded a raw MS quantification table (feature-by-sample intensity matrix) into QuantyFey and are applying drift-correction strategies (Internal Standard correction, statistical drift correction, Custom Bracketing, or Weighted Bracketing) but need to maintain traceability between corrected intensities and their original feature identifiers and sample metadata for downstream analysis and reporting.

## When NOT to use

- Input intensity table already contains corrected or normalized values from external preprocessing tools
- Feature identifiers or sample metadata are already lost or de-linked from the intensity matrix
- Analysis goal does not require traceability between corrected measurements and their source features or samples (e.g., aggregate statistical comparisons only)

## Inputs

- raw MS quantification table (feature-by-sample intensity matrix)
- feature identifiers (e.g., compound names, m/z values)
- sample metadata (e.g., run sequence, batch information, sample identifiers)

## Outputs

- drift-corrected intensity table with preserved feature identifiers
- drift-corrected intensity table with preserved sample metadata
- feature-by-sample matrix with aligned row and column labels

## How to apply

After selecting and applying one of QuantyFey's available drift-correction strategies (Internal Standard, statistical models, Custom Bracketing, or Weighted Bracketing quantification), the corrected intensity values are automatically preserved alongside their feature identifiers and sample metadata during export. The application maintains the row-column structure of the original feature-by-sample matrix while replacing intensity values with drift-corrected equivalents. Verify that exported tables retain consistent feature ordering and that sample metadata columns remain aligned with the corrected intensity columns. This preserves the link between each corrected measurement and its originating analyte and sample context.

## Related tools

- **QuantyFey** (Shiny application that implements drift-correction strategies and exports intensity tables with feature and sample metadata preserved) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Exported drift-corrected intensity table contains the same number of rows (features) and columns (samples) as the input raw table
- Feature identifiers in the corrected table match exactly (order, naming, count) with the original raw table
- Sample metadata columns are present and aligned with their corresponding intensity columns in the corrected output
- Intensity values have been updated (non-zero difference from raw) but row-column indices and headers remain unchanged
- Corrected table can be directly loaded into downstream analysis tools without requiring re-mapping of features or samples

## Limitations

- QuantyFey is compatible with Windows operating systems only for the standalone version; Linux users must use the Apptainer version (which runs slowly on macOS)
- The application does not provide integration capabilities for raw MS data; it works on already-integrated feature-by-sample matrices
- No changelog is available to document whether feature or metadata preservation behavior has changed across software versions
- Preservation of metadata depends on user correctly exporting the full output table rather than intermediate visualizations

## Evidence

- [other] workflow_step_preservation: "Export the drift-corrected intensity table with preserved feature identifiers and sample metadata."
- [other] input_format_specification: "Load the raw MS quantification table (feature-by-sample intensity matrix) into QuantyFey."
- [readme] correction_strategies_available: "commonly applied drift correction methods: Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification, Weighted Bracketing"
- [readme] tool_purpose: "QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data"
- [readme] drift_correction_rationale: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification."
