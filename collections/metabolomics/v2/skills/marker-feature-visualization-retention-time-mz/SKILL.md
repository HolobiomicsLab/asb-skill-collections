---
name: marker-feature-visualization-retention-time-mz
description: Use when after NPFimg's automated detection algorithm has identified marker features from a two-dimensional MS map (m/z vs retention time), especially when you need to validate feature positions, inspect co-localization patterns, or communicate results to stakeholders.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - NPFimg
  - XCMS
derived_from:
- doi: 10.1021/acs.analchem.1c03163?ref=
  title: NPFimg
- doi: 10.1021/acs.analchem.1c03163
  title: ''
evidence_spans:
- github.com__poomcj__NPFimg
- We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npfimg_cq
    doi: 10.1021/acs.analchem.1c03163?ref=
    title: NPFimg
  dedup_kept_from: coll_npfimg_cq
schema_version: 0.2.0
---

# marker-feature-visualization-retention-time-mz

## Summary

Visualize identified chemo-/biomarker features on a two-dimensional chromatography–mass spectrometry map (m/z vs retention time) to enable spatial interpretation and validation of discriminative analytes. This skill is essential for confirming marker detection results and communicating feature localization in untargeted metabolomics workflows.

## When to use

Apply this skill after NPFimg's automated detection algorithm has identified marker features from a two-dimensional MS map (m/z vs retention time), especially when you need to validate feature positions, inspect co-localization patterns, or communicate results to stakeholders. Use it when working with GC–MS or LC–MS data where both m/z and retention time dimensions are available and marker discrimination is the primary analytical goal.

## When NOT to use

- Input is already a feature table or pre-processed peak list; use this skill on raw or minimally processed MS maps to avoid loss of spatial context.
- One-dimensional or time-series data without both m/z and retention time dimensions; the skill requires 2D chromatography–MS data.
- Targeted metabolomics with pre-defined feature lists; this skill is designed for untargeted marker discovery where spatial visualization aids validation.

## Inputs

- two-dimensional MS map (m/z vs retention time) in NetCDF or vendor-specific format
- structured marker feature predictions table (m/z, retention time, feature scores)

## Outputs

- annotated 2D visualization (m/z vs retention time plot with overlaid marker features)
- marker feature coordinates (m/z, retention time) with visual confidence encoding

## How to apply

Load the two-dimensional MS map (m/z vs retention time) along with the structured marker feature predictions (m/z values, retention times, feature scores) output by NPFimg's automated detection. Plot the detected features as overlays or highlighted points on the original m/z–retention time space. Ensure feature scores or discriminative power are visually encoded (e.g., via color intensity or size) to rank confidence. Examine spatial clustering and separation between case and control analytes to confirm that identified markers occupy distinct regions and do not overlap with noise or background signals. This visualization step grounds the statistical findings in the raw data topology and enables manual verification before exporting final marker lists.

## Related tools

- **NPFimg** (automated marker feature detection and scoring pipeline that generates m/z, retention time, and feature scores as input to visualization) — github.com/poomcj/NPFimg
- **XCMS** (alternative peak picking and feature detection tool for comparison; NPFimg shows lower error rates than XCMS in marker identification)

## Evaluation signals

- Marker features are plotted at correct (m/z, retention time) coordinates matching the exported predictions table.
- Spatial separation or clustering of marker features is visually distinct from background noise regions on the 2D map.
- Feature scores or confidence metrics are consistently encoded and readable in the visualization (e.g., color gradient or size scale).
- No marker features overlap with regions flagged as false positives or high-noise zones in the original MS map.
- Visualization is reproducible: re-running the same input data produces identical feature positions and visual encoding.

## Limitations

- Visualization fidelity depends on the quality of the input MS map; noisy or poorly calibrated m/z or retention time scales will distort spatial interpretation.
- Feature score encoding (color, size) is heuristic and subjective; no universal threshold is provided for distinguishing high-confidence from low-confidence markers in the visualization alone.
- The skill does not automate peak shape assessment or isotope pattern validation; manual inspection may still be required for complex or overlapping features.
- Visualization of very high-density marker regions (e.g., >1000 features) may suffer from overplotting, obscuring individual feature positions.

## Evidence

- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features.: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [other] Identify marker features through NPFimg's automated detection algorithm (avoiding conventional peak picking). Visualize identified marker features on the m/z–retention time space.: "Identify marker features through NPFimg's automated detection algorithm (avoiding conventional peak picking). Visualize identified marker features on the m/z–retention time space."
- [other] Export marker feature predictions with m/z values, retention times, and feature scores to a structured table.: "Export marker feature predictions with m/z values, retention times, and feature scores to a structured table."
- [intro] NPFimg avoids conventional peak picking process, which suffers from false peak detections.: "NPFimg avoids conventional peak picking process, which suffers from false peak detections."
