---
name: transition-group-feature-extraction
description: Use when when you have loaded a TransitionGroup (extracted ion chromatogram or mobilogram from DIA mass spectrometry data) and need to identify precise peak boundaries, apex retention/drift time, and intensity values for quantitative feature detection.
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
  - massdash (massdash.peakPickers module)
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

# transition-group-feature-extraction

## Summary

Extract quantitative peak features (boundaries, apex position, intensity) from chromatographic or ion-mobility TransitionGroup signals using deep learning-based peak picking. This skill converts raw one-dimensional traces into structured TransitionGroupFeature records suitable for downstream peptide quantification and identification workflows.

## When to use

When you have loaded a TransitionGroup (extracted ion chromatogram or mobilogram from DIA mass spectrometry data) and need to identify precise peak boundaries, apex retention/drift time, and intensity values for quantitative feature detection. This skill is essential before feature-level statistical filtering (e.g., Q-value cutoff) or integration into a search results table.

## When NOT to use

- Input is already a feature table or summary statistics table — skip to filtering/visualization steps.
- TransitionGroup contains no signal or is entirely below noise threshold — peak picking will fail or produce unreliable boundaries.
- Model weights or onnxruntime session are not initialized — the inference step cannot proceed.

## Inputs

- TransitionGroup (one-dimensional chromatogram or mobilogram trace)
- Data1D structure (preprocessed intensity array with time/drift dimension)
- onnxruntime session with loaded conformer peak-picking model weights

## Outputs

- TransitionGroupFeature record (containing peak start, apex, end coordinates and intensity)
- Peak boundary timestamps or drift times
- Quality scores or confidence metrics for detected peaks

## How to apply

Initialize a ConformerPeakPicker instance with an onnxruntime session and pretrained conformer-based model weights. Load the TransitionGroup data as a Data1D structure (normalized intensity values with handling for missing data points). Run onnxruntime inference on the preprocessed signal to predict peak regions and apex positions. Extract peak boundaries (start, apex, end retention time) and intensity values from the model output tensor. Construct TransitionGroupFeature records containing detected peak parameters and quality scores. The rationale for using deep learning is to capture subtle peak morphologies and handle noisy or coeluting transitions better than traditional rule-based methods; conformer-based architectures are suited to chromatographic signal shapes.

## Related tools

- **onnxruntime** (Executes inference on preprocessed chromatogram/mobilogram signals using trained conformer model to predict peak boundaries and apex positions)
- **massdash (massdash.peakPickers module)** (Provides ConformerPeakPicker class that wraps onnxruntime inference, handles Data1D preprocessing, and constructs TransitionGroupFeature output records) — https://github.com/Roestlab/massdash
- **Pytest** (Used to validate ConformerPeakPicker output against expected TransitionGroupFeature schemas and peak boundary correctness)
- **Syrupy** (Snapshot testing tool used to compare ConformerPeakPicker output to previous expected output states across test runs) — https://github.com/syrupy-project/syrupy

## Examples

```
from massdash.peakPickers import ConformerPeakPicker
import onnxruntime as ort
session = ort.InferenceSession('conformer_model.onnx')
picker = ConformerPeakPicker(session=session)
feature = picker.pick(transition_group)
```

## Evaluation signals

- TransitionGroupFeature records are produced with non-null peak start, apex, and end coordinates
- Peak boundaries (start < apex < end) obey temporal/drift-time ordering invariants
- Intensity values are within expected range (e.g., non-negative, consistent with input signal max)
- Snapshot tests (Syrupy) confirm output matches previous validated peak boundaries for regression test set
- Peak picking produces boundaries consistent with manual visual inspection or OpenSwath reference boundaries

## Limitations

- Conformer model performance depends on availability and quality of pretrained weights; model must be initialized before inference.
- Peak picking may fail or produce unreliable boundaries on low-signal-to-noise TransitionGroups or heavily coeluting traces.
- onnxruntime inference speed and memory usage scale with signal length; very long chromatograms may require batch processing or windowing.
- No guidance provided in the article on handling edge cases such as truncated peaks near scan boundaries or multipeak TransitionGroups.

## Evidence

- [other] The ConformerPeakPicker is a massdash.peakPickers class that operates using onnxruntime to identify peak boundaries on TransitionGroup objects and produces TransitionGroupFeature records as output.: "The ConformerPeakPicker is a massdash.peakPickers class that operates using onnxruntime to identify peak boundaries on TransitionGroup objects and produces TransitionGroupFeature records as output."
- [other] Initialize ConformerPeakPicker with onnxruntime session and model weights for conformer-based peak detection. Load a TransitionGroup (chromatogram or mobilogram data) into memory as a Data1D structure. Preprocess the signal by normalizing intensity values and handling missing data points. Run the onnxruntime inference on the preprocessed signal to predict peak regions and apex positions. Extract peak boundaries (start, apex, end retention time) and intensity values from model output. Construct TransitionGroupFeature records containing detected peak parameters and quality scores.: "Initialize ConformerPeakPicker with onnxruntime session and model weights for conformer-based peak detection. Load a TransitionGroup (chromatogram or mobilogram data) into memory as a Data1D"
- [readme] On the fly parameter optimization - Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches.: "On the fly parameter optimization - Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches."
- [other] Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms: "Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms"
- [other] Syrupy is used to compare output to previous expected output states: "Syrupy is used to compare output to previous expected output states"
