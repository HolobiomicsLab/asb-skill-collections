---
name: neural-network-model-deployment-in-python
description: Use when you have a trained conformer-based peak-picking model (in ONNX format) and need to apply it to chromatographic or ion-mobility mass spectrometry data (TransitionGroup objects) to detect peak boundaries and apex positions, generating TransitionGroupFeature records for downstream analysis or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - onnxruntime
  - Pytest
  - Syrupy
  - massdash
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
---

# neural-network-model-deployment-in-python

## Summary

Deploy trained neural network models for peak detection in mass spectrometry data using onnxruntime, enabling inference on chromatogram and mobilogram TransitionGroup structures within a Python-based workflow. This skill bridges model training and production use by initializing a runtime session, preprocessing signals, executing inference, and extracting structured feature outputs.

## When to use

You have a trained conformer-based peak-picking model (in ONNX format) and need to apply it to chromatographic or ion-mobility mass spectrometry data (TransitionGroup objects) to detect peak boundaries and apex positions, generating TransitionGroupFeature records for downstream analysis or visualization in MassDash.

## When NOT to use

- Model weights or ONNX file are not available or incompatible with the onnxruntime version in use.
- Input data is already a processed feature table or peak-picked result; re-running peak detection would be redundant.
- TransitionGroup data has not been loaded or preprocessed; raw mass spectrometry files must be converted to TransitionGroup structures first.

## Inputs

- TransitionGroup (chromatogram or mobilogram Data1D structure)
- onnxruntime session with loaded model weights
- Signal intensity array with optional missing data points

## Outputs

- TransitionGroupFeature records
- Peak parameters (start, apex, end retention time)
- Peak intensity values
- Quality scores

## How to apply

Initialize the ConformerPeakPicker class with an onnxruntime session and model weights for conformer-based peak detection. Load a TransitionGroup (chromatogram or mobilogram data represented as Data1D structures) into memory and preprocess the signal by normalizing intensity values and handling missing data points. Run onnxruntime inference on the preprocessed signal to predict peak regions and apex positions. Extract peak boundaries (start, apex, end retention time) and intensity values from the model output. Construct TransitionGroupFeature records containing detected peak parameters and quality scores. The workflow prioritizes signal normalization before inference to ensure consistent model performance across varying signal intensities, and quality scores enable downstream filtering or prioritization of detected features.

## Related tools

- **onnxruntime** (Executes neural network inference on preprocessed signal data to predict peak boundaries and apex positions.)
- **massdash** (Python package providing ConformerPeakPicker class, TransitionGroup and TransitionGroupFeature data structures, and integration with the Streamlit GUI for visualization and parameter optimization.) — https://github.com/Roestlab/massdash
- **Pytest** (Testing framework for validating ConformerPeakPicker output and model inference behavior.)
- **Syrupy** (Snapshot testing plugin used to compare ConformerPeakPicker output to previous expected output states and detect regressions.) — https://github.com/syrupy-project/syrupy

## Evaluation signals

- Verify that TransitionGroupFeature records are populated with all required fields: start, apex, end retention time, intensity values, and quality scores.
- Confirm that peak boundaries are within the expected retention time or ion-mobility range of the input TransitionGroup.
- Check that quality scores are in a valid range and correlate with peak shape characteristics (e.g., symmetry, signal-to-noise ratio).
- Run Syrupy snapshot tests to ensure consistency of model outputs across commits and to detect unintended changes in inference behavior.
- Validate that preprocessed signal intensities are normalized (e.g., 0–1 range or z-score normalized) before inference.

## Limitations

- Model performance depends on signal preprocessing (normalization and missing data handling); poorly preprocessed signals may produce inaccurate or spurious peak detections.
- onnxruntime version compatibility must be maintained; model weights may not be compatible across major runtime versions.
- Peak detection quality is limited by the training data and model capacity; novel or atypical peak shapes may be misidentified if not represented in the training set.
- Inference speed and memory usage depend on signal length and hardware; very long chromatograms or high-resolution ion-mobility data may cause performance bottlenecks.

## Evidence

- [other] The ConformerPeakPicker is a massdash.peakPickers class that operates using onnxruntime to identify peak boundaries on TransitionGroup objects and produces TransitionGroupFeature records as output.: "The ConformerPeakPicker is a massdash.peakPickers class that operates using onnxruntime to identify peak boundaries on TransitionGroup objects and produces TransitionGroupFeature records as output."
- [other] Initialize ConformerPeakPicker with onnxruntime session and model weights for conformer-based peak detection; load a TransitionGroup (chromatogram or mobilogram data) into memory as a Data1D structure; preprocess the signal by normalizing intensity values and handling missing data points.: "Initialize ConformerPeakPicker with onnxruntime session and model weights for conformer-based peak detection. 2. Load a TransitionGroup (chromatogram or mobilogram data) into memory as a Data1D"
- [other] Run the onnxruntime inference on the preprocessed signal to predict peak regions and apex positions; extract peak boundaries (start, apex, end retention time) and intensity values from model output.: "Run the onnxruntime inference on the preprocessed signal to predict peak regions and apex positions. 5. Extract peak boundaries (start, apex, end retention time) and intensity values from model"
- [other] MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI): "MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)"
- [other] Syrupy is used to compare output to previous expected output states: "Syrupy is used to compare output to previous expected output states"
