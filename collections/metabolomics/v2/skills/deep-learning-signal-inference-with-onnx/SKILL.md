---
name: deep-learning-signal-inference-with-onnx
description: Use when when you have a TransitionGroup structure containing normalized intensity traces (1D signal data from chromatograms or mobilograms) and you want to automatically detect peak regions with high precision by leveraging a conformer-based deep learning model.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-signal-inference-with-onnx

## Summary

Use a pre-trained deep learning model loaded via onnxruntime to perform inference on preprocessed mass spectrometry signal data (chromatograms or mobilograms) to detect peak boundaries and apex positions. This skill enables rapid, learned pattern recognition for peak picking without hand-crafted feature engineering.

## When to use

When you have a TransitionGroup structure containing normalized intensity traces (1D signal data from chromatograms or mobilograms) and you want to automatically detect peak regions with high precision by leveraging a conformer-based deep learning model. This approach is appropriate when traditional rule-based peak pickers are insufficient or when you need to experiment with novel peak detection approaches on-the-fly.

## When NOT to use

- Input signal is already segmented into discrete peaks or a feature table has already been constructed—use this skill upstream, before feature aggregation.
- The onnxruntime model weights or session is unavailable or incompatible with your runtime environment.
- Your mass spectrometry data have not been normalized or preprocessed; this skill expects clean, unit-scaled intensity traces, not raw detector counts.

## Inputs

- TransitionGroup (chromatogram or mobilogram data structure)
- Data1D (preprocessed 1D signal array with normalized intensities)
- onnxruntime model session with loaded conformer-based peak detection weights

## Outputs

- TransitionGroupFeature records with detected peak parameters
- Peak boundary coordinates (start retention time, apex, end retention time)
- Apex intensity values and quality scores for each peak

## How to apply

Initialize an onnxruntime session with a pre-trained conformer-based model and load it with the appropriate model weights. Preprocess your TransitionGroup data by normalizing intensity values and handling missing or invalid data points to create a Data1D structure. Run inference on the preprocessed signal through the onnxruntime session to predict peak regions and apex positions. Extract the model output predictions (peak start time, apex retention time, end time, and intensity values) and map these back to the original signal coordinates. Construct TransitionGroupFeature records containing the detected peak parameters and associated quality scores. Validate that the predicted boundaries are temporally ordered and that intensity values fall within physically plausible ranges relative to the input signal.

## Related tools

- **onnxruntime** (Inference engine for executing the pre-trained deep learning model on preprocessed signal data)
- **massdash** (Python package providing ConformerPeakPicker class, TransitionGroup and TransitionGroupFeature data structures, and integration point for onnxruntime-based peak detection) — https://github.com/Roestlab/massdash
- **Pytest** (Test framework for validating peak detection outputs and model inference correctness)
- **Syrupy** (Snapshot testing plugin for comparing onnxruntime model outputs to baseline expected outputs and detecting regressions) — https://github.com/syrupy-project/syrupy

## Examples

```
from massdash.peakPickers import ConformerPeakPicker; import onnxruntime as ort; session = ort.InferenceSession('conformer_model.onnx'); picker = ConformerPeakPicker(session); features = picker.pick(transition_group)
```

## Evaluation signals

- Peak boundary coordinates are strictly ordered: start < apex < end in retention time (or ion mobility) space.
- Predicted apex intensity is less than or equal to the maximum intensity in the input signal within the predicted peak region.
- Predicted peaks do not overlap and do not extend beyond the boundaries of the input trace.
- Snapshot tests using Syrupy confirm that model outputs match expected peak parameters from previous runs, detecting any regression in inference quality.
- TransitionGroupFeature records are successfully constructed and contain valid values for all required fields (peak times, intensities, quality scores).

## Limitations

- Model inference depends on the quality and representativeness of the pre-trained weights; performance may degrade on mass spectrometry data from different instruments, sample preparation protocols, or ionization methods not well represented in the training set.
- Preprocessing steps (intensity normalization, missing data handling) are critical; poorly normalized or corrupted input signals may produce spurious or missed peak predictions.
- onnxruntime inference latency and memory usage scale with signal length; very long chromatograms or mobilograms may require batching or downsampling.
- The skill does not address peptide/small molecule mass or retention time filtering; post-inference filtering against external databases or Q-value thresholds must be applied downstream.

## Evidence

- [other] The ConformerPeakPicker is a massdash.peakPickers class that operates using onnxruntime to identify peak boundaries on TransitionGroup objects and produces TransitionGroupFeature records as output.: "The ConformerPeakPicker is a massdash.peakPickers class that operates using onnxruntime to identify peak boundaries on TransitionGroup objects and produces TransitionGroupFeature records as output."
- [other] Initialize ConformerPeakPicker with onnxruntime session and model weights for conformer-based peak detection. Load a TransitionGroup (chromatogram or mobilogram data) into memory as a Data1D structure. Preprocess the signal by normalizing intensity values and handling missing data points. Run the onnxruntime inference on the preprocessed signal to predict peak regions and apex positions.: "Initialize ConformerPeakPicker with onnxruntime session and model weights for conformer-based peak detection. Load a TransitionGroup (chromatogram or mobilogram data) into memory as a Data1D"
- [other] Extract peak boundaries (start, apex, end retention time) and intensity values from model output. Construct TransitionGroupFeature records containing detected peak parameters and quality scores.: "Extract peak boundaries (start, apex, end retention time) and intensity values from model output. Construct TransitionGroupFeature records containing detected peak parameters and quality scores."
- [other] Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches.: "Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches."
- [other] Syrupy is used to compare output to previous expected output states: "Syrupy is used to compare output to previous expected output states"
