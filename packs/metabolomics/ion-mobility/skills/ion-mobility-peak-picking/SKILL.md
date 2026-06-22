---
name: ion-mobility-peak-picking
description: Use when when you have extracted ion mobilograms from DIA-MS experiments and need to automatically identify peak boundaries and apex positions in the ion mobility dimension.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - onnxruntime
  - Pytest
  - Syrupy
  - massdash
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- optional dependencies are also required and can be installed with pip install -r requirements-optional.txt
- Tests are performed using Pytest
- Syrupy is used to compare output to previous expected output states
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massdash_cq
    doi: 10.1021/acs.jproteome.4c00026
    title: MassDash
  dedup_kept_from: coll_massdash_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00026
  all_source_dois:
  - 10.1021/acs.jproteome.4c00026
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-mobility-peak-picking

## Summary

Peak picking on extracted ion mobilograms using deep learning–based boundary detection to identify ion mobility features in Data-Independent Acquisition mass spectrometry. This skill applies neural network inference via onnxruntime to detect apex positions and intensity boundaries on TransitionGroup mobilogram data.

## When to use

When you have extracted ion mobilograms from DIA-MS experiments and need to automatically identify peak boundaries and apex positions in the ion mobility dimension. Use this when manual inspection is impractical or when you want to apply conformer-based neural network models (ConformerPeakPicker) that exploit learned patterns in ion mobility traces across multiple precursor transitions.

## When NOT to use

- Input mobilogram data is already segmented into individual peaks; use this skill on raw, continuous mobilogram traces.
- Ion mobility dimension is not present or is noise-dominated; this skill targets structured mobilogram data from instruments like timsTOF.
- You require deterministic, parameter-free peak picking; ConformerPeakPicker depends on learned model weights and may not guarantee reproducibility without model versioning.

## Inputs

- TransitionGroup (mobilogram data as Data1D structure)
- ConformerPeakPicker model weights and onnxruntime session
- Preprocessed signal with normalized intensity values

## Outputs

- TransitionGroupFeature records
- Peak boundaries (start, apex, end mobility coordinates)
- Intensity values and quality scores per detected peak

## How to apply

Initialize a ConformerPeakPicker instance with a pre-trained onnxruntime session and conformer model weights. Load the TransitionGroup mobilogram data as a Data1D structure and preprocess the signal by normalizing intensity values and handling missing data points. Run onnxruntime inference on the preprocessed mobilogram to predict peak regions and apex positions. Extract the predicted peak boundaries (start, apex, end in mobility space) and intensity values from the model output. Construct TransitionGroupFeature records that encapsulate the detected peak parameters and associated quality scores. Return the populated TransitionGroupFeature as the final output for downstream analysis or visualization.

## Related tools

- **onnxruntime** (Inference engine for running the pre-trained ConformerPeakPicker neural network model on preprocessed mobilogram data)
- **massdash** (Python package providing the ConformerPeakPicker class and TransitionGroup/TransitionGroupFeature data structures for ion mobility peak picking workflow) — https://github.com/Roestlab/massdash
- **Pytest** (Testing framework for validating ConformerPeakPicker output against expected peak boundaries and feature records)
- **Syrupy** (Snapshot testing plugin to verify ConformerPeakPicker output immutability and consistency across test iterations) — https://github.com/syrupy-project/syrupy

## Evaluation signals

- TransitionGroupFeature records are populated with non-null peak boundary coordinates (start, apex, end) in ion mobility space.
- Detected peak apex positions fall within the expected range of the input mobilogram data and are monotonically ordered if multiple peaks are found.
- Quality scores are computed and fall within a valid range (e.g., 0–1 or signal-to-noise ratio); compare snapshots of quality scores across test runs using Syrupy to ensure consistency.
- Peak intensity values extracted from model output are non-negative and exhibit expected rise-and-fall pattern characteristic of ion mobility features.
- Snapshot comparison tests using Syrupy confirm that model output remains unchanged across code refactors and dependency updates, detecting unintended shifts in peak predictions.

## Limitations

- ConformerPeakPicker requires a pre-trained model and onnxruntime session; model availability and versioning must be managed separately.
- Performance depends on signal quality and preprocessing fidelity; poor normalization or excessive missing data points can degrade peak boundary predictions.
- The skill operates only on individual TransitionGroups; scaling to large datasets requires external batching or parallelization logic not addressed in the workflow.
- Model predictions reflect learned patterns from training data; generalization to novel instruments, sample types, or ion mobility ranges is not guaranteed.

## Evidence

- [other] The ConformerPeakPicker is a massdash.peakPickers class that operates using onnxruntime to identify peak boundaries on TransitionGroup objects and produces TransitionGroupFeature records as output.: "The ConformerPeakPicker is a massdash.peakPickers class that operates using onnxruntime to identify peak boundaries on TransitionGroup objects and produces TransitionGroupFeature records as output."
- [other] Initialize ConformerPeakPicker with onnxruntime session and model weights for conformer-based peak detection. Load a TransitionGroup (chromatogram or mobilogram data) into memory as a Data1D structure.: "Initialize ConformerPeakPicker with onnxruntime session and model weights for conformer-based peak detection. Load a TransitionGroup (chromatogram or mobilogram data) into memory as a Data1D"
- [other] Preprocess the signal by normalizing intensity values and handling missing data points. Run the onnxruntime inference on the preprocessed signal to predict peak regions and apex positions.: "Preprocess the signal by normalizing intensity values and handling missing data points. Run the onnxruntime inference on the preprocessed signal to predict peak regions and apex positions."
- [other] Extract peak boundaries (start, apex, end retention time) and intensity values from model output. Construct TransitionGroupFeature records containing detected peak parameters and quality scores.: "Extract peak boundaries (start, apex, end retention time) and intensity values from model output. Construct TransitionGroupFeature records containing detected peak parameters and quality scores."
- [other] The main panel provides visualizations of the extraction ion chromatogram and the extracted ion mobilogram: "The main panel provides visualizations of the extraction ion chromatogram and the extracted ion mobilogram"
- [other] Syrupy is used to compare output to previous expected output states: "Syrupy is used to compare output to previous expected output states"
