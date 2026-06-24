---
name: chromatographic-peak-detection-and-segmentation
description: Use when you have raw LC-MS data (mzML or vendor format) and need to
  discover and characterize all chromatographic features present, without prior knowledge
  of target analytes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
  - GC-MS
  - ion-mobility-MS
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: huaxuyu/masscube
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing
- masscube is an integrated Python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_masscube_cq
    doi: 10.1038/s41467-025-60640-5
    title: MassCube
  dedup_kept_from: coll_masscube_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-60640-5
  all_source_dois:
  - 10.1038/s41467-025-60640-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-peak-detection-and-segmentation

## Summary

Nontargeted peak detection and segmentation identifies and delineates chromatographic peaks across the full retention time range in raw LC-MS data (mzML or vendor formats) to extract precise peak boundaries and characteristic metadata. This is a foundational step in untargeted metabolomics workflows for converting raw instrument output into structured feature tables.

## When to use

Apply this skill when you have raw LC-MS data (mzML or vendor format) and need to discover and characterize all chromatographic features present, without prior knowledge of target analytes. Use it as the initial feature extraction step before quality evaluation, annotation, or statistical analysis in untargeted metabolomics studies.

## When NOT to use

- Input is already a processed feature table or peak list; peak detection has already been performed.
- Targeted analysis of known analytes where peak lists are predefined; use targeted extraction instead.
- Data from alternative analytical methods (e.g., GC-MS, ion mobility) not explicitly supported by the tool.

## Inputs

- raw LC-MS data (mzML format)
- raw LC-MS data (vendor format)

## Outputs

- feature table (CSV format)
- feature table (feather format)
- detected peaks with m/z, retention time, intensity, peak width, and quality metrics

## How to apply

Load raw LC-MS data into MassCube and invoke the nontargeted peak detection algorithm to scan across the full retention time range and identify all significant peaks. The algorithm performs peak segmentation to define precise boundaries for each detected peak. For each peak, extract and record characteristic metadata: m/z value, retention time, intensity, and peak width. Export the resulting peak list as a structured feature table (CSV or feather format) containing all detected peaks with their associated quality metrics. Validate output by inspecting peak count, retention time range coverage, and intensity distribution to confirm detection sensitivity and specificity.

## Related tools

- **masscube** (integrated Python package that performs nontargeted peak detection and segmentation on LC-MS data, defines peak boundaries, and exports feature tables) — https://github.com/huaxuyu/masscube/
- **Python** (programming language in which MassCube is implemented and executed)

## Examples

```
from masscube import MassCube; mc = MassCube(); peaks = mc.peak_detection(raw_data_path='sample.mzML'); peaks.to_csv('detected_peaks.csv')
```

## Evaluation signals

- Feature table contains expected number of peaks with realistic m/z range (e.g., 50–2000 m/z for metabolomics) and retention time span matching the LC method.
- Peak width values are consistent with typical chromatographic peak shapes (e.g., 0.01–1 min for UHPLC).
- Intensity values show reasonable distribution; no unexpectedly saturated or near-zero peaks across features.
- Peak segmentation boundaries do not overlap; each detected peak occupies a discrete retention time window.
- Quality metrics reported in feature table (if present) indicate confidence in detection and segmentation for each peak.

## Limitations

- No changelog provided in repository documentation; version tracking and backward compatibility are not explicitly documented.
- Performance on data with high background noise, co-eluting peaks, or unusual chromatographic profiles is not discussed.
- Nontargeted approach may detect instrument noise or artifacts; post-detection quality filtering is recommended.

## Evidence

- [intro] Highly accurate nontargeted peak detection and segmentation: "Highly accurate nontargeted peak detection and segmentation."
- [readme] masscube is an integrated Python package for LC-MS data processing: "masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing."
- [other] Peak detection workflow across full retention time range: "Apply nontargeted peak detection algorithm to identify chromatographic peaks across the full retention time range."
- [other] Peak segmentation defines boundaries and extracts characteristics: "Perform peak segmentation to define precise peak boundaries and extract peak characteristics (m/z, retention time, intensity, peak width)."
- [other] Export feature table in standard formats: "Generate and export feature table in tabular format (CSV or feather) containing detected peaks with their metadata and quality metrics."
