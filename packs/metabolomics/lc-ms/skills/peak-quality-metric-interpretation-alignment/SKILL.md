---
name: peak-quality-metric-interpretation-alignment
description: Use when when you have loaded aligned peak-alignment data from a molecular networking task and need to distinguish high-confidence, reproducible peak alignments from noise or spurious matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Plotly
  - D3.js
  - pandas
  - Flask / Dash
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/jasms.5c00237
  title: MMSA
evidence_spans:
- interactive visualization
- interactive visualization and analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mmsa_cq
    doi: 10.1021/jasms.5c00237
    title: MMSA
  dedup_kept_from: coll_mmsa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00237
  all_source_dois:
  - 10.1021/jasms.5c00237
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-quality-metric-interpretation-alignment

## Summary

Interpret and apply alignment quality metrics to filter and validate aligned peaks across multiple mass spectra in molecular networking data. This skill ensures that only peaks meeting reproducibility and confidence thresholds are retained for downstream analysis.

## When to use

When you have loaded aligned peak-alignment data from a molecular networking task and need to distinguish high-confidence, reproducible peak alignments from noise or spurious matches. Use this skill before interactive visualization or statistical analysis to enforce data quality constraints based on alignment-specific metrics (e.g., alignment score cutoffs, peak presence/absence criteria).

## When NOT to use

- When alignment data has not been generated or loaded yet; first run the molecular networking alignment task.
- When the peak table lacks alignment quality columns or metrics; verify schema before filtering.
- When the input is already a curated or published feature table that has undergone manual quality review outside this workflow.

## Inputs

- structured peak-alignment table with columns: peak intensity, m/z, retention time, alignment quality metrics, peak presence/absence flags
- alignment quality score cutoff (numeric threshold)
- peak presence/absence criteria (boolean or categorical constraints)

## Outputs

- filtered peak table retaining only rows passing alignment quality thresholds
- count and proportion of peaks retained vs. rejected per quality metric
- metadata describing active filter constraints applied

## How to apply

Parse user-supplied alignment quality filter parameters (alignment score cutoff, peak presence criteria) from the web interface. Apply row-wise boolean filtering to the structured peak table, retaining only peaks that satisfy all active alignment-quality constraints. The filtering logic should evaluate each peak's alignment-quality column against the specified thresholds and reject rows that fall below the cutoff. Validate that all displayed peaks pass the active filter criteria and that the filtered set size and composition match expected distributions for the input molecular networking task. Document the number of peaks retained vs. rejected at each quality threshold to support later reproducibility claims.

## Related tools

- **Plotly** (Render filtered peak sets as interactive multi-spectrum visualizations (overlay plot or heatmap) after quality filtering)
- **D3.js** (Alternative charting library for interactive visualization of quality-filtered peak alignments)
- **pandas** (Data manipulation and row-wise boolean filtering of alignment quality columns)
- **Flask / Dash** (Web framework providing input interface for quality filter parameters and real-time filtering UI updates) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website

## Evaluation signals

- All peaks in the filtered output have alignment quality scores ≥ the specified cutoff; verify by scanning the alignment-quality column for any values below threshold.
- Peak presence/absence criteria are consistently applied: peaks marked 'absent' in X spectra should not appear in those spectrum rows; validate via row-level presence flags.
- The filtered peak count is strictly ≤ the input peak count; document the rejection rate and confirm it matches the expected filtering stringency.
- Re-running the filter with identical parameters on the same input produces identical output (determinism check).
- The distribution of retained alignment quality scores is tighter (lower variance) than the input distribution, indicating successful quality stratification.

## Limitations

- Alignment quality metrics are task-specific and depend on the upstream molecular networking algorithm; metrics may vary between GNPS, FBMN, and custom pipelines.
- No changelog or versioning information is documented for alignment quality metric definitions; changes to metric computation across software versions may render old filter cutoffs non-comparable.
- The README does not specify which alignment quality metric(s) are computed or what their valid ranges are; practitioners must infer thresholds empirically or from GNPS documentation.

## Evidence

- [other] Apply row-wise filtering to the peak table using boolean logic on intensity and alignment-quality columns, retaining only peaks that satisfy all active filter constraints.: "Apply row-wise filtering to the peak table using boolean logic on intensity and alignment-quality columns, retaining only peaks that satisfy all active filter constraints."
- [intro] The application provides advanced filtering and analysis capabilities for aligned peaks across multiple spectra.: "visualize aligned peaks across multiple spectra with advanced filtering and analysis capabilities"
- [other] Parse user-supplied filter parameters (intensity threshold, alignment score cutoff, peak presence/absence criteria) from the web interface input state.: "Parse user-supplied filter parameters (intensity threshold, alignment score cutoff, peak presence/absence criteria) from the web interface input state."
- [other] Validate that all displayed peaks pass the active filter criteria and that the rendering correctly represents the input alignment data without loss or corruption.: "Validate that all displayed peaks pass the active filter criteria and that the rendering correctly represents the input alignment data without loss or corruption."
- [readme] Custom spectrum ordering, m/z range filtering, and top-10 peak intensity analysis are provided.: "Advanced Filtering: Custom spectrum ordering, m/z range filtering, and top-10 peak intensity analysis"
