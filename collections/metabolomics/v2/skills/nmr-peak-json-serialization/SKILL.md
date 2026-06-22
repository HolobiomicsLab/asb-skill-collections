---
name: nmr-peak-json-serialization
description: Use when you have proton (1H) and carbon-13 (13C) NMR peak measurements from a molecular sample and need to classify the molecule using the SMART 3 deep learning API. The peaks must be reformatted from their native instrument output into JSON before submission to the /api/smart3/search endpoint.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3474
  tools:
  - TensorFlow Serving
  - DeepSAT
  techniques:
  - NMR
derived_from:
- doi: 10.1186/s13321-023-00738-4
  title: DeepSAT
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepsat_cq
    doi: 10.1186/s13321-023-00738-4
    title: DeepSAT
  dedup_kept_from: coll_deepsat_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-023-00738-4
  all_source_dois:
  - 10.1186/s13321-023-00738-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-peak-json-serialization

## Summary

Serialize nuclear magnetic resonance peak data into JSON dictionary format with 1H and 13C headers for programmatic submission to the SMART 3 classification API. This skill bridges raw NMR spectroscopic measurements and machine learning-ready molecular classification requests.

## When to use

You have proton (1H) and carbon-13 (13C) NMR peak measurements from a molecular sample and need to classify the molecule using the SMART 3 deep learning API. The peaks must be reformatted from their native instrument output into JSON before submission to the /api/smart3/search endpoint.

## When NOT to use

- Input peaks are already in a pre-computed feature table or embedding space — use direct model inference instead.
- NMR data is malformed, missing 1H or 13C headers, or contains null/NaN values — validate and clean the data first.
- Model input schema has changed without code update — check /model/metadata endpoint and update field names before serialization.

## Inputs

- 1H NMR peak list (chemical shift and intensity values)
- 13C NMR peak list (chemical shift and intensity values)
- JSON dictionary with '1H' and '13C' keys
- TensorFlow Serving model metadata (from /model/metadata endpoint)

## Outputs

- JSON-formatted peak payload (list of dictionaries)
- Classification response from /api/smart3/search endpoint
- Molecular structure prediction(s) with confidence scores

## How to apply

Extract or prepare lists of 1H and 13C chemical shift and intensity values from your NMR instrument output or processing software. Construct a JSON payload as a list of dictionaries, where each dictionary contains '1H' and '13C' keys with their respective peak data. Before submission, query the TensorFlow Serving /model/metadata endpoint to confirm the expected input schema and field names, since model input names may change and require code updates. Format the peaks as a JSON list of dicts and POST to the /api/smart3/search endpoint. Parse the returned JSON classification response to extract molecular structure predictions or confidence scores.

## Related tools

- **TensorFlow Serving** (Hosts the SMART 3 classification model and provides /model/metadata schema endpoint and /api/smart3/search inference endpoint for peak-based molecular classification)
- **DeepSAT** (Source repository containing the SMART 3 deep learning architecture for NMR-based molecular classification) — github:mwang87__DeepSAT

## Examples

```
import json; peaks = [{"1H": [1.2, 2.5, 7.3], "13C": [20.1, 45.6, 128.9]}]; requests.post('http://tensorflow-serving:8501/api/smart3/search', json=peaks, headers={'Content-Type': 'application/json'})
```

## Evaluation signals

- JSON payload passes schema validation against /model/metadata endpoint output names (no missing or misnamed keys)
- 1H and 13C peak lists are non-empty and contain numeric chemical shift and intensity values within expected ranges (e.g., 1H: 0–14 ppm, 13C: 0–220 ppm)
- /api/smart3/search endpoint returns HTTP 200 with a valid JSON response containing molecular classification results
- Classification response includes molecular structure predictions with associated confidence scores or probability distributions
- Round-trip serialization and deserialization preserve peak data fidelity (no loss of precision or truncation)

## Limitations

- Model input names may change across TensorFlow Serving deployments, requiring manual code updates and /model/metadata re-inspection
- No changelog is available to track model schema or endpoint breaking changes
- Peak data quality and format depend on upstream NMR preprocessing; malformed or incomplete peak lists will fail classification
- The skill assumes TensorFlow Serving is accessible at the documented URL and /model/metadata endpoint is available

## Evidence

- [intro] You can put in your peaks as a json list of dicts, with 1H,13C as headers: "You can put in your peaks as a json list of dicts, with 1H,13C as headers"
- [other] The SMART 3 API accepts peak data programmatically through the /api/smart3/search endpoint as a JSON list of dictionaries with proton (1H) and carbon-13 (13C) nuclear magnetic resonance headers for molecular classification.: "The SMART 3 API accepts peak data programmatically through the /api/smart3/search endpoint as a JSON list of dictionaries with proton (1H) and carbon-13 (13C) nuclear magnetic resonance headers"
- [intro] We pass through tensorflow serving at this url: /model/metadata: "We pass through tensorflow serving at this url: /model/metadata"
- [intro] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
