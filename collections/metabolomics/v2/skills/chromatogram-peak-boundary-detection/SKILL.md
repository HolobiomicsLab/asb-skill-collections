---
name: chromatogram-peak-boundary-detection
description: Use when when you have loaded a TransitionGroup (extracted ion chromatogram or mobilogram from DIA-MS data) and need to identify precise peak boundaries and apex positions for feature extraction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
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

# chromatogram-peak-boundary-detection

## Summary

Automated detection of peak boundaries (start, apex, end retention time) in extracted ion chromatograms and mobilograms using deep learning inference via onnxruntime. This skill produces quantitative peak parameters and quality scores for downstream feature integration and validation in DIA-MS workflows.

## When to use

When you have loaded a TransitionGroup (extracted ion chromatogram or mobilogram from DIA-MS data) and need to identify precise peak boundaries and apex positions for feature extraction. Use this skill when automated, reproducible peak detection is required across many transitions, or when you want to experiment with neural network-based peak picking models instead of traditional signal processing heuristics.

## When NOT to use

- Input is raw, unextracted MS/MS spectrum data (not a chromatogram or mobilogram trace).
- You require real-time or ultra-low-latency peak detection and cannot support onnxruntime inference overhead.
- The peak picking algorithm has already been applied and boundaries are already present in the input feature records.

## Inputs

- TransitionGroup object (extracted ion chromatogram or mobilogram data)
- Data1D structure (intensity values indexed by retention time or ion mobility)
- onnxruntime InferenceSession with loaded model weights
- Model artifact (ONNX model file for conformer-based peak detection)

## Outputs

- TransitionGroupFeature records
- Peak boundary parameters (start, apex, end retention time)
- Peak intensity values and quality scores

## How to apply

Initialize a ConformerPeakPicker instance with a pre-trained onnxruntime model session and the corresponding model weights for conformer-based peak detection. Load the TransitionGroup (a Data1D structure containing intensity values keyed by retention time or ion mobility) into memory. Preprocess the signal by normalizing intensity values and handling missing or zero data points. Run onnxruntime inference on the preprocessed signal to predict peak regions and apex positions; the model outputs predicted peak boundaries and confidence scores. Extract peak boundaries (start, apex, end retention time) and intensity values from the model output tensors. Construct TransitionGroupFeature records populated with the detected peak parameters, quality metrics, and metadata. Return the populated TransitionGroupFeature as the output for downstream validation and integration.

## Related tools

- **massdash** (Python package providing ConformerPeakPicker class and TransitionGroup/TransitionGroupFeature data structures; hosts peak picking workflows and integration with onnxruntime inference) — https://github.com/Roestlab/massdash
- **onnxruntime** (Executes inference on the conformer-based peak detection model to predict peak boundaries and apex positions from preprocessed signal data)
- **Pytest** (Executes unit and integration tests to validate peak boundary detection correctness and model output consistency)
- **Syrupy** (Snapshot testing plugin for pytest; compares peak detection output (TransitionGroupFeature records) to previously recorded expected output states to detect regressions) — https://github.com/syrupy-project/syrupy

## Evaluation signals

- TransitionGroupFeature records are non-empty and contain peak_start, peak_apex, and peak_end retention time values in ascending order (start < apex < end).
- Intensity values extracted from model output are numeric, non-negative, and peak apex intensity is ≥ intensities at start and end boundaries.
- Quality scores (if provided) are within expected range (e.g. [0, 1]); low quality scores should correlate with ambiguous or noisy signal regions.
- Snapshot tests (via Syrupy) pass, confirming detected peak boundaries match expected output on reference test data.
- Peak boundaries align visually with manual inspection of the extracted chromatogram trace in the MassDash Bokeh/interactive visualization.

## Limitations

- ConformerPeakPicker performance depends on the quality and representativeness of the onnxruntime model weights; model must be pre-trained on chromatographic data similar in origin and preprocessing to your input.
- Preprocessing step (normalization, missing data handling) can significantly affect inference results; edge cases such as negative intensities, zero traces, or extreme noise may not be handled gracefully.
- Model inference via onnxruntime introduces computational overhead and memory requirements proportional to trace length; may become a bottleneck for very large datasets or real-time applications.
- No adaptive thresholding or parameter tuning for peak detection; model outputs fixed peak boundaries without sensitivity analysis or uncertainty quantification per transition.

## Evidence

- [other] The ConformerPeakPicker is a massdash.peakPickers class that operates using onnxruntime to identify peak boundaries on TransitionGroup objects and produces TransitionGroupFeature records as output.: "The ConformerPeakPicker is a massdash.peakPickers class that operates using onnxruntime to identify peak boundaries on TransitionGroup objects and produces TransitionGroupFeature records as output."
- [other] Initialize ConformerPeakPicker with onnxruntime session and model weights for conformer-based peak detection. Load a TransitionGroup (chromatogram or mobilogram data) into memory as a Data1D structure. Preprocess the signal by normalizing intensity values and handling missing data points. Run the onnxruntime inference on the preprocessed signal to predict peak regions and apex positions. Extract peak boundaries (start, apex, end retention time) and intensity values from model output. Construct TransitionGroupFeature records containing detected peak parameters and quality scores.: "1. Initialize ConformerPeakPicker with onnxruntime session and model weights for conformer-based peak detection. 2. Load a TransitionGroup (chromatogram or mobilogram data) into memory as a Data1D"
- [other] Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms: "Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms"
- [readme] On the fly parameter optimization - Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches.: "On the fly parameter optimization - Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches."
- [other] Syrupy is used to compare output to previous expected output states: "Syrupy is used to compare output to previous expected output states"
