---
name: peak-boundary-definition-and-validation
description: Use when after nontargeted peak detection has identified candidate peaks in LC-MS chromatograms, when you need to establish exact peak start/end retention times and extract peak-level metadata (intensity, width, shape) for downstream feature quality evaluation and annotation workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3370
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-boundary-definition-and-validation

## Summary

Define and validate precise chromatographic peak boundaries in LC-MS data to extract quantitatively accurate peak characteristics (m/z, retention time, intensity, peak width). This skill ensures that detected peaks are correctly segmented and quality-evaluated before downstream feature annotation and metabolite identification.

## When to use

Apply this skill after nontargeted peak detection has identified candidate peaks in LC-MS chromatograms, when you need to establish exact peak start/end retention times and extract peak-level metadata (intensity, width, shape) for downstream feature quality evaluation and annotation workflows. Use it when raw peak detection outputs require refinement to eliminate false positives or overlapping signals.

## When NOT to use

- Input is already a curated, pre-segmented feature table (e.g., from vendor software or a prior processing run); re-segmentation risks losing validated boundaries.
- Peak detection has not yet been performed; apply nontargeted peak detection first.
- Data contains only targeted (SRM/MRM) acquisitions rather than full-scan LC-MS; targeted methods do not require nontargeted segmentation.

## Inputs

- raw LC-MS data in mzML format
- raw LC-MS data in vendor format
- peak detection results (retention time coordinates, m/z values, intensity estimates)

## Outputs

- feature table in CSV format with detected peaks and metadata
- feature table in feather format with detected peaks and metadata
- peak characteristics: m/z, retention time, intensity, peak width
- quality metrics per peak

## How to apply

Load the raw LC-MS data (mzML or vendor format) and peak detection results into MassCube. Apply the peak segmentation algorithm to define precise peak boundaries by analyzing chromatographic intensity profiles and m/z trajectories. For each detected peak, extract and validate the following characteristics: m/z value, retention time at peak apex, peak intensity (height or area), and peak width at baseline or half-height. Generate a feature table (CSV or feather format) containing all detected peaks with their metadata and quality metrics. Validate segmentation accuracy by visual inspection of a subset of peaks (e.g., comparing detected boundaries against raw chromatograms) and by checking that peak widths and intensities fall within biologically plausible ranges for the instrument and method.

## Related tools

- **masscube** (performs peak segmentation, extracts peak boundaries and characteristics, generates validated feature table with quality metrics) — https://github.com/huaxuyu/masscube/
- **Python** (runtime environment for masscube package execution and custom validation workflows)

## Evaluation signals

- Feature table contains non-null, physically plausible values for m/z (within expected mass range), retention time (within data acquisition window), intensity (positive values), and peak width (consistent with chromatographic resolution).
- Peak count and intensity distribution match or exceed those from vendor software or published benchmarks for the same dataset.
- Manual spot-check of 5–10 peaks shows that detected boundaries align visually with chromatographic peaks in the raw LC-MS image and do not overlap incorrectly with adjacent peaks.
- Quality metrics (e.g., peak shape scores, signal-to-noise ratios if calculated) show expected distributions and correlate inversely with known artifact peaks.
- Export schema is valid (all rows have matching column counts, data types match specification) and file format (CSV or feather) is readable by downstream tools.

## Limitations

- Highly accurate peak segmentation depends on appropriate tuning of detection algorithm parameters (e.g., smoothing window, intensity threshold) for the specific LC-MS instrument, column, and metabolite class; parameter transfer across methods may degrade accuracy.
- Overlapping or co-eluting peaks may not be resolved correctly; manual review or complementary high-resolution MS/MS data may be required.
- No changelog is available in the repository, limiting traceability of algorithm changes across software versions.

## Evidence

- [other] Apply nontargeted peak detection algorithm to identify chromatographic peaks across the full retention time range. 3. Perform peak segmentation to define precise peak boundaries and extract peak characteristics (m/z, retention time, intensity, peak width).: "Perform peak segmentation to define precise peak boundaries and extract peak characteristics (m/z, retention time, intensity, peak width)."
- [other] Generate and export feature table in tabular format (CSV or feather) containing detected peaks with their metadata and quality metrics.: "Generate and export feature table in tabular format (CSV or feather) containing detected peaks with their metadata and quality metrics."
- [readme] Highly accurate nontargeted peak detection and segmentation.: "Highly accurate nontargeted peak detection and segmentation."
- [readme] Comprehensive feature quality evaluation.: "Comprehensive feature quality evaluation."
- [readme] masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.: "masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing."
