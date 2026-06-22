---
name: roi-detection-mass-spectrometry
description: Use when you have raw or converted mass spectrometry data (CE-MS or LC-MS in mzXML or mzML format) and need to identify candidate metabolite regions before feature extraction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - ROIpeaks
  - MSroiaug
  - Bioinformatic Toolbox
  - Statistics And Machine Learning Toolbox
  - Wavelet Toolbox
  - Image Processing Toolbox
  - Signal Processing Toolbox
  - msconvert
  - MATLAB R2024a
  - Wavelet Toolbox (MATLAB)
  - Image Processing Toolbox (MATLAB)
  - Signal Processing Toolbox (MATLAB)
  techniques:
  - LC-MS
  - CE-MS
derived_from:
- doi: 10.1007/s00216-023-04715-6
  title: AriumMS
evidence_spans:
- functions (ROIpeaks, MSroiaug) developed by Romà Tauler, Eva Gorrochategui and Joaquim Jaumot
- 'Required toolboxes for the app version: Bioinformatic Toolbox, Statistics And Machine Learning Toolbox, Wavelet Toolbox, Image Processing Toolbox, Signal Processing Toolbox, Parallel Computing'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ariumms_cq
    doi: 10.1007/s00216-023-04715-6
    title: AriumMS
  dedup_kept_from: coll_ariumms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-04715-6
  all_source_dois:
  - 10.1007/s00216-023-04715-6
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ROI Detection in Mass Spectrometry

## Summary

Detect regions of interest (ROIs) in untargeted mass spectrometry data by applying the ROIpeaks algorithm to converted mzXML/mzML files, using parameter-driven configuration to identify feature-rich spectral zones prior to preprocessing and augmentation.

## When to use

You have raw or converted mass spectrometry data (CE-MS or LC-MS in mzXML or mzML format) and need to identify candidate metabolite regions before feature extraction. ROI detection is the first stage of an untargeted metabolomics workflow when you want to automatically discover high-variance spectral zones without prior knowledge of target compounds.

## When NOT to use

- Input data is already a processed feature table or consensus peak list — ROI detection operates on raw or minimally processed spectral arrays and would be redundant.
- Targeted metabolomics where analyte m/z values and retention/migration times are known in advance — use focused extraction or selected-ion monitoring instead.
- Spectral data in non-standard formats (e.g., proprietary vendor formats, NetCDF) without prior conversion to mzXML or mzML via msconvert.

## Inputs

- Converted mass spectrometry data file (mzXML or mzML format)
- ROI search parameter configuration (noise level, morphological structuring element size, spectral smoothing kernel, m/z and time/migration resolution thresholds)

## Outputs

- ROI coordinate matrix (m/z × retention/migration time boundaries for each detected region)
- ROI intensity matrix (feature values within each detected ROI)
- ROI metadata (signal-to-noise ratio, peak height, area estimates per region)

## How to apply

Load converted MS data (mzXML or mzML) into MATLAB R2024a with required toolboxes (Bioinformatic, Statistics and Machine Learning, Wavelet, Image Processing, Signal Processing, Parallel Computing). Configure ROI search parameters (e.g., noise threshold, minimum feature size, spectral smoothing window) and apply the ROIpeaks function, which implements wavelet-based or morphological feature detection on the mass-to-charge and retention-time (or migration-time) dimensions. ROIpeaks outputs detected ROI coordinates and intensity matrices. The selection and tuning of parameters directly determine the sensitivity and specificity of detected regions; conservative parameters reduce false positives but may miss weak metabolite signals, while aggressive parameters increase sensitivity but risk feature fragmentation. Validate detected ROIs by inspecting peak coherence across the time/migration dimension and verifying that m/z intervals contain chemically plausible isotope patterns and adducts.

## Related tools

- **ROIpeaks** (Core algorithm for wavelet-based or morphological detection of high-intensity, contiguous regions in m/z–time 2D spectral arrays)
- **msconvert** (Converts raw proprietary MS data formats to mzXML or mzML standard formats required by ROIpeaks) — http://proteowizard.sourceforge.net/download.html
- **MATLAB R2024a** (Host environment for ROIpeaks execution and parameter configuration)
- **Wavelet Toolbox (MATLAB)** (Provides wavelet decomposition and multi-scale feature detection primitives used internally by ROIpeaks)
- **Image Processing Toolbox (MATLAB)** (Supplies morphological operations (dilation, erosion, connected-component labeling) for ROI boundary delineation)
- **Signal Processing Toolbox (MATLAB)** (Enables spectral smoothing, filtering, and peak detection preprocessing)

## Evaluation signals

- Detected ROI coordinates are contained within the m/z range and time/migration range of the input data and do not overlap spatially in a fragmented manner.
- ROI intensity matrices contain positive values with signal-to-noise ratios above the configured threshold; absence of uniform-valued or noise-only ROIs.
- ROI regions are consistent across replicate MS injections or datasets from the same sample preparation batch (low drift in m/z and retention/migration time coordinates).
- Downstream preprocessing (normalization, denoising) and augmentation steps execute without dimension mismatches or NaN propagation, confirming ROI outputs match expected matrix dimensions.
- Manual inspection of a representative subset of detected ROIs on a 2D heatmap (m/z vs. time/migration) shows contiguous, compact feature clusters rather than isolated pixels or large, featureless zones.

## Limitations

- ROI detection sensitivity is highly parameter-dependent; no universal cutoff values are recommended in the article, requiring empirical tuning per instrument, ionization mode (CE-MS vs. LC-MS), and sample matrix.
- The algorithm may fragment a single metabolite feature into multiple ROIs if spectral intensity varies sharply with time/migration, or merge distinct features if they lie adjacent in m/z–time space; post-detection filtering or manual merging may be necessary.
- Requires MATLAB and multiple licensed toolboxes (Wavelet, Image Processing, Signal Processing); not available as standalone compiled executables or in open-source languages without porting effort.
- No explicit handling of isotope patterns or adduct annotation within the ROI detection stage; validation of chemical plausibility is deferred to downstream preprocessing and interpretation steps.

## Evidence

- [other] Load and parameter configuration for ROI detection: "Load converted MS data (mzXML or mzML format) into MATLAB R2024a environment with required toolboxes (Bioinformatic, Statistics and Machine Learning, Wavelet, Image Processing, Signal Processing,"
- [readme] ROIpeaks function and its authorship: "It uses functions (ROIpeaks, MSroiaug) developed by Romà Tauler, Eva Gorrochategui and Joaquim Jaumot"
- [other] Three-stage pipeline structure with ROI as first stage: "AriumMS implements a three-stage pipeline where user-set parameters drive sequential execution of ROI search, data preprocessing, and data augmentation stages."
- [readme] Tool purpose and untargeted scope: "All in one tool for untargeted Metabolomics by ROI and augmentation of multiple Data sets."
- [readme] Parameter-driven execution and output generation: "Set parameters are then used to perform ROI search, data preprocessing and data augmentation."
- [readme] Required MS data format: "For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed with the ProteoWizard Project"
- [readme] MATLAB version and toolbox requirements: "MATLAB R2024a or newer. Required toolboxes for the app version: Bioinformatic Toolbox, Statistics And Machine Learning Toolbox, Wavelet Toolbox, Image Processing Toolbox, Signal Processing Toolbox,"
