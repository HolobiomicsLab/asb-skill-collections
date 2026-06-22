---
name: reference-peak-matching-retention-time-alignment
description: Use when you have training LC-HRMS chromatograms (rt × m/z matrix format) from which you have already extracted peak candidates using smoothing and gradient-descent peak detection, and you possess a curated reference list of isolated single chromatographic peaks (ground truth).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - OpenMS/TOPPView
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# reference-peak-matching-retention-time-alignment

## Summary

Match chromatographic peaks detected via smoothing and gradient-descent algorithms against a user-defined reference list of isolated single peaks, using retention time and m/z alignment criteria to link detected peaks across training chromatograms. This enables consistent feature tracking and refinement of reference feature properties for subsequent CNN model training.

## When to use

You have training LC-HRMS chromatograms (rt × m/z matrix format) from which you have already extracted peak candidates using smoothing and gradient-descent peak detection, and you possess a curated reference list of isolated single chromatographic peaks (ground truth). Use this skill when you need to link detected peaks from training data to reference features so that you can update reference properties (retention time, m/z, peak shape) and generate augmented training instances for model training.

## When NOT to use

- Input chromatograms have not yet been processed with smoothing and gradient-descent peak detection—apply detection first
- Reference list is unavailable or not curated from isolated single peaks—reference matching requires ground-truth peak definitions
- Goal is real-time peak detection in unknown samples—use the trained CNN model on new data instead of re-matching training features

## Inputs

- Training chromatogram data (retention time × m/z matrix, e.g., NetCDF or mzML export)
- User-defined reference list of isolated single chromatographic peaks (ground-truth features)

## Outputs

- Updated reference feature list with refined retention time, m/z, and peak shape parameters
- Matched peak assignments linking detected training peaks to reference features
- Augmented training instance dataset for CNN model training

## How to apply

Load training chromatogram data in standardized two-dimensional (retention time × m/z) format. Apply a smoothing filter to reduce noise, then execute gradient-descent algorithm to locate peak maxima, estimate peak borders, and calculate peak centers. Match detected peaks to the user-defined reference list using retention time and m/z alignment criteria (specific tolerance thresholds should be set based on instrument precision and chromatographic variability). For each successful match, update the corresponding reference feature properties to best fit the detected peaks from the training chromatograms. This matched reference set then serves as ground truth for generating large numbers of augmented training instances by iterative combination, with optional isotopolog extension.

## Related tools

- **PeakBot** (Implements smoothing, gradient-descent peak detection, reference list matching, property update, and augmented training instance generation for LC-HRMS chromatograms) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Implements CNN model training on augmented training instances generated after reference peak matching) — https://www.tensorflow.org/
- **OpenMS/TOPPView** (Visualizes detected chromatographic features exported as featureML files after reference matching and peak detection) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Evaluation signals

- All detected peaks in training chromatograms have a corresponding match in the reference list (100% assignment rate within retention time and m/z tolerance thresholds)
- Updated reference feature properties show convergence: retention time and m/z values remain stable or show consistent drift across training samples; peak shape parameters cluster within expected range for the compound
- Reference list size remains constant or increases only via explicit isotopolog extension—spurious matches should not create orphan references
- Augmented training instances generated from matched references have expected count and composition: number of instances = reference count × iteration combinations, with documented peak/background/distraction ratios
- Export validation: featureML-exported peaks from matched references can be visualized in TOPPView without parsing errors and align visually with original chromatogram maxima

## Limitations

- Matching accuracy depends critically on retention time and m/z tolerance thresholds; if set too loose, different peaks may be conflated; if too tight, valid peaks may fail to match. Article does not specify default thresholds—these must be tuned per instrument and chromatographic method.
- Reference list must be manually curated from isolated single peaks; contaminated or misidentified reference peaks will propagate errors through training instance generation and CNN model training.
- Matching is deterministic and does not account for isomeric or isobaric compounds that share retention time or m/z; the CNN model accounts for isomers via left/right flag, but reference matching alone cannot distinguish them.
- GPU acceleration for training instance generation is available but requires CUDA-enabled Nvidia GPU, CUDA toolkit, and cuDNN; CPU-only mode is slower and may be impractical for large-scale augmentation.

## Evidence

- [intro] PeakBot matches detected peaks with a user-defined reference list to use the same chromatographic peak from different samples: "matched with a user-defined reference list (the ground-truth; isolated single chromatographic peaks) with the aim of using the same chromatographic peak but from different samples"
- [intro] Reference properties are updated to best fit detected peaks from training chromatograms: "the properties of the reference features are also updated to best fit the chromatographic peaks from the reference chromatograms"
- [intro] Gradient-descent algorithm locates peaks and estimates borders and centers: "searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step"
- [intro] Matched references are used to generate augmented training instances: "The matched references are then used to generate a large number of training instances by iteratively combining them."
- [readme] Input data format is standardized two-dimensional retention time × m/z matrix: "uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz), which is used as the input for a machine-learning CNN model"
