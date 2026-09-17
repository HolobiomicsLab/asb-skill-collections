---
name: peak-border-center-estimation
description: Use when you have LC-HRMS chromatograms in retention time × m/z matrix
  format and need to automatically localize chromatographic peak positions and extents
  prior to matching against a reference peak library or generating CNN training instances.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - OpenMS / TOPPView
  techniques:
  - mass-spectrometry
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: christophuv/PeakBot
  license_tier: noncommercial
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btac344
  title: PeakBot
evidence_spans:
- PeakBot is a python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakbot_cq
    doi: 10.1093/bioinformatics/btac344
    title: PeakBot
  dedup_kept_from: coll_peakbot_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac344
  all_source_dois:
  - 10.1093/bioinformatics/btac344
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-border-center-estimation

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Estimate chromatographic peak borders and centers from LC-HRMS profile mode data using smoothing and gradient-descent algorithms. This skill prepares detected peaks for matching against reference feature lists and training data generation.

## When to use

Apply this skill when you have LC-HRMS chromatograms in retention time × m/z matrix format and need to automatically localize chromatographic peak positions and extents prior to matching against a reference peak library or generating CNN training instances.

## When NOT to use

- Input chromatograms are already centroided or in processed feature format (use peak picking on centroided data instead).
- Peaks have already been manually validated and entered into a reference database (use direct reference matching without re-estimation).
- Signal-to-noise ratio is extremely poor such that smoothing cannot recover peak structure reliably.

## Inputs

- LC-HRMS chromatogram data (retention time × m/z matrix format)
- Smoothing filter parameters (kernel size, method)
- Gradient-descent search parameters (step size, convergence threshold)

## Outputs

- Detected chromatographic peaks with estimated center coordinates (retention time, m/z)
- Peak border estimates (left and right retention time / m/z boundaries)
- Peak properties (bounding box, apex location)

## How to apply

First, apply a smoothing filter to the chromatographic signal to reduce noise. Then execute a gradient-descent algorithm to locate local maxima representing chromatographic peak positions. For each detected maximum, estimate the peak center (apex position in retention time and m/z space) and the peak borders (the left and right retention time / m/z boundaries where the peak signal rises above and falls below background). The gradient-descent approach identifies both the precise center coordinate and the bounding envelope of each peak. Output the set of peaks with their estimated centers, left borders, and right borders for downstream matching or augmentation.

## Related tools

- **PeakBot** (Python package implementing smoothing and gradient-descent peak border/center estimation for LC-HRMS data) — https://github.com/christophuv/PeakBot
- **TensorFlow** (CNN model training and inference backend (used by PeakBot for peak classification after border/center estimation)) — https://www.tensorflow.org/
- **OpenMS / TOPPView** (Visualization and validation of detected chromatographic peaks and featureML exports) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Evaluation signals

- Detected peak centers align with local maxima visible in the smoothed chromatographic profile (visual inspection or correlation test).
- Peak borders enclose the full width at half maximum (FWHM) or baseline-defined extent of each peak without false inclusion of neighboring peaks.
- Matched reference features (after border/center matching step) have updated retention time and m/z values that are tighter and more consistent than the original reference list estimates.
- Training instances generated from the detected peaks and borders show improved CNN model performance (lower false positive/negative rate) compared to training without border/center refinement.
- Left and right border coordinates are consistent across replicates of the same sample (low inter-replicate variance in border estimates).

## Limitations

- Smoothing filter performance depends on noise characteristics and peak width; aggressive smoothing may merge adjacent peaks or distort peak shapes.
- Gradient-descent algorithm may converge to local maxima rather than the true peak center if the smoothed signal has multiple local extrema.
- Peak borders estimated by this method may be inaccurate for severely overlapping or poorly resolved peaks, requiring manual review or stricter matching criteria.
- Algorithm performance is sensitive to GPU parameters (blockdim, griddim) which must be tuned for each graphics card; CUDA memory constraints may require reducing exportBatchSize for large datasets.

## Evidence

- [readme] searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step: "searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step"
- [readme] matched with a user-defined reference list (the ground-truth; isolated single chromatographic peaks) with the aim of using the same chromatographic peak but from different samples: "matched with a user-defined reference list (the ground-truth; isolated single chromatographic peaks) with the aim of using the same chromatographic peak but from different samples"
- [readme] the properties of the reference features are also updated to best fit the chromatographic peaks from the reference chromatograms: "the properties of the reference features are also updated to best fit the chromatographic peaks from the reference chromatograms"
- [other] Apply smoothing filter to the chromatographic signal to reduce noise. 3. Execute gradient-descent algorithm to locate chromatographic peak maxima and estimate peak borders and centers.: "Apply smoothing filter to the chromatographic signal to reduce noise. 3. Execute gradient-descent algorithm to locate chromatographic peak maxima and estimate peak borders and centers."
- [readme] uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz): "uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz)"
