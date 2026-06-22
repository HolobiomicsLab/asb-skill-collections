---
name: peak-annotation-with-bounding-boxes
description: Use when you have isolated reference peaks from training chromatograms (ground-truth, single compounds per sample) and need to create a diverse, labelled training set large enough to train a CNN peak detector.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - OpenMS (TOPPView)
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

# peak-annotation-with-bounding-boxes

## Summary

Generate large-scale labelled training datasets for CNN peak detection by iteratively combining matched reference features from LC-HRMS chromatograms, assigning each synthetic instance a peak type (chromatographic peak with isomeric variants or background), bounding box, and peak center. This augmentation strategy enables the CNN to generalize across peak morphologies and background noise types.

## When to use

Use this skill when you have isolated reference peaks from training chromatograms (ground-truth, single compounds per sample) and need to create a diverse, labelled training set large enough to train a CNN peak detector. Specifically, apply it after matching detected peaks to a user-defined reference list and before feeding instances to the CNN model for training.

## When NOT to use

- Input consists only of raw LC-HRMS spectra without matched reference features—first extract and match peaks to a reference list.
- Reference list is incomplete, biased to few compound types, or lacks isotopologs—the augmented dataset quality depends on reference diversity.
- Goal is to annotate existing peaks in a single chromatogram rather than generate a reusable training set—use peak detection and matching instead.

## Inputs

- Matched reference features (peaks with borders, centers, and compound identities from reference chromatograms)
- User-defined reference list (ground-truth, isolated single chromatographic peaks)
- LC-HRMS profile mode data (retention time × m/z arrays)
- Background signal samples (including wall-type signals)

## Outputs

- Labelled training instances (two-dimensional areas: retention time × m/z)
- Instance metadata: peak type, bounding box, peak center
- Augmented training dataset (large number of synthetic training instances)
- Standardized dataset ready for CNN model input (TensorFlow format)

## How to apply

Load matched reference features (peaks with estimated borders, centers, and assigned identities from reference chromatograms). Iteratively combine these matched references by mixing them in various proportions and spatial arrangements to create synthetic two-dimensional areas (retention time × m/z), simulating co-eluting peaks and background noise. Assign labels to each generated instance indicating peak type (true chromatographic peak with left/right isomeric variants, or background signal like walls), bounding box coordinates, and peak center position. Use GPU (CUDA) acceleration to rapidly generate the large volume of training instances required for CNN model convergence. Support multiple background types (e.g., walls—signals spanning entire or large portions of the chromatogram) to ensure the model differentiates true peaks from false signals. Export the labelled training set as standardized two-dimensional areas with associated metadata (peak type, bounding box, center) for direct input to the TensorFlow CNN model.

## Related tools

- **PeakBot** (Python package that implements reference matching, iterative combination of matched references, and GPU-accelerated training instance generation; handles smoothing, gradient-descent peak detection, reference list extension with isotopologs, and CNN-based peak annotation with bounding boxes) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Deep learning framework used to implement and train the CNN model that consumes the generated labelled training instances) — https://www.tensorflow.org/
- **OpenMS (TOPPView)** (Visualization tool that can display detected chromatographic peaks exported from PeakBot in featureML format) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Evaluation signals

- Number of generated training instances matches or exceeds the expected output volume given the number of matched references and combination iterations.
- Each synthetic instance is a valid two-dimensional area (retention time × m/z) with non-null bounding box and peak center coordinates.
- Peak type labels are correctly assigned: instances with true peaks differ structurally from background-only instances; isomeric variants are distinguishable.
- Augmented dataset exhibits diversity in peak morphologies, spatial arrangements, and background types (e.g., walls vs. noise).
- CNN trained on the augmented dataset converges to acceptable loss and achieves measurable detection accuracy on held-out validation chromatograms.

## Limitations

- GPU memory constraints may require reduction of exportBatchSize (e.g., from 2048 to 1024 or 512 if less than 4 GB available), reducing generation throughput.
- Blockdim and griddim CUDA parameters must be tuned to match the specific Nvidia GPU; suboptimal choices reduce performance or cause failures.
- Quality of augmented dataset depends critically on the completeness and accuracy of the reference list; missing or mislabeled references propagate into synthetic instances.
- Iterative combination strategies may not generate sufficient coverage of rare peak morphologies or edge cases not well-represented in the reference set.
- On Windows 10, WDMM TDR timeout must be increased manually via Registry Editor to avoid GPU compute timeouts during large batch generation.

## Evidence

- [other] Matched references are used to generate a large number of training instances by iteratively combining them, which serve as the labelled dataset for training the CNN model.: "Matched references are used to generate a large number of training instances by iteratively combining them, which serve as the labelled dataset for training the CNN model."
- [other] Iteratively combine matched reference features by mixing them in various proportions and spatial arrangements to create synthetic training instances.: "Iteratively combine matched reference features by mixing them in various proportions and spatial arrangements to create synthetic training instances."
- [readme] Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize (augmentation of the training dataset). Moreover, also different background types are supported by PeakBot so that it differentiates between true chromatographic peaks and irrelevant background information (e.g., walls, which are signals present throughout the entire or large parts of the chromatograms).: "Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize (augmentation of the training dataset). Moreover, also"
- [readme] As a large number of training instances is required to train the CNN model and to achieve a high performance of the model, a GPU (CUDA) based approach is implemented that decreases the time required for their generation.: "As a large number of training instances is required to train the CNN model and to achieve a high performance of the model, a GPU (CUDA) based approach is implemented that decreases the time required"
- [readme] If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512.: "If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512."
- [readme] Note: Different GPUs have a different number of streaming-processors. Thus, the blockdim and griddim need to be chosen accordingly.: "Note: Different GPUs have a different number of streaming-processors. Thus, the blockdim and griddim need to be chosen accordingly."
