---
name: retention-time-alignment
description: Use when after peak detection in untargeted metabolomics when you have
  identified ion signals across mass-to-charge and retention-time dimensions from
  replicate injections of the same samples, and you need to group peaks from different
  runs that represent the same metabolite before building a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3370
  tools:
  - openNAU (MetaQC module)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.21147/j.issn.1000-9604.2023.05.11
  title: OpenNAU
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_opennau_cq
    doi: 10.21147/j.issn.1000-9604.2023.05.11
    title: OpenNAU
  dedup_kept_from: coll_opennau_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21147/j.issn.1000-9604.2023.05.11
  all_source_dois:
  - 10.21147/j.issn.1000-9604.2023.05.11
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-alignment

## Summary

Aligns retention time values across replicate LC-MS injections to consolidate peaks from the same analyte into unified features. This step is essential in untargeted metabolomics to correct for systematic retention time drift and enable accurate cross-sample intensity comparison.

## When to use

Apply this skill after peak detection in untargeted metabolomics when you have identified ion signals across mass-to-charge and retention-time dimensions from replicate injections of the same samples, and you need to group peaks from different runs that represent the same metabolite before building a feature abundance matrix.

## When NOT to use

- Input is already a feature table or intensity matrix — alignment has already been performed.
- Analysis uses targeted metabolomics with predetermined retention times — peaks are matched by identity, not alignment.
- Single-injection analysis — no replicates to align.

## Inputs

- Peak list with m/z, retention time (RT), and intensity from replicate LC-MS injections
- Retention-time tolerance threshold (e.g., ±0.1–0.5 min, instrument and method dependent)
- Mass-to-charge (m/z) tolerance for grouping (e.g., 5 ppm)

## Outputs

- Unified feature table with consolidated peaks across replicates
- Feature identifiers (m/z, standardized retention time, internal ID)
- Aligned feature list ready for intensity matrix construction

## How to apply

Load peak detection output (peak list with m/z, retention time, and intensity for each detection) from replicate LC-MS injections. Apply retention-time alignment to correct for chromatographic drift between runs by matching peaks within a retention-time tolerance window and assigning them to unified feature identifiers. This is typically performed as part of peak alignment and feature grouping before intensity value extraction. The alignment consolidates redundant detections of the same ion across replicates into a single feature row, with retention time standardized (often as the mean or median across aligned peaks). Verify alignment quality by inspecting the distribution of retention-time differences within feature groups; poor alignment may indicate instrument instability or sample preparation issues.

## Related tools

- **openNAU (MetaQC module)** (Performs peak detection, retention-time alignment, and feature grouping in untargeted metabolomics workflows) — https://github.com/zjuRong/openNAU

## Evaluation signals

- All replicate injections of the same sample show the same unified feature identifiers (m/z and standardized RT) with non-zero intensities in replicate columns.
- Retention-time standard deviation within each aligned feature group falls within the specified tolerance (e.g., ±0.1–0.5 min).
- Feature abundance matrix has consistent dimensions (rows = features, columns = samples) with no missing entries after alignment.
- Comparison of raw peak list size before and after alignment shows expected reduction in row count (consolidation of replicates).
- No systematic biases in RT differences between early and late-eluting features (indicates uniform drift correction).

## Limitations

- Alignment quality depends critically on retention-time tolerance threshold; too loose results in false feature grouping, too tight misses true replicates.
- Significant chromatographic drift between runs (e.g., > tolerance threshold) can cause legitimate replicates to be split into separate features.
- Co-eluting isomers with identical m/z may be incorrectly grouped into a single feature if they fall within RT and m/z tolerances.
- Algorithm assumes similar sample composition and injection order across replicates; violation can introduce systematic misalignment.

## Evidence

- [other] Workflow step: peak alignment and feature grouping: "Perform peak alignment and feature grouping to consolidate peaks from replicate injections into unified features."
- [other] Data consolidation rationale: "Extract intensity values for each feature across all samples and compile into a feature abundance matrix."
- [readme] Software functionality in openNAU: "It includes the extraction of raw mass data and quality control for the identification of differential metabolic ion peaks."
