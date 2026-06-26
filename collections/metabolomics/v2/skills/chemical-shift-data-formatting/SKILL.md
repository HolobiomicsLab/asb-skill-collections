---
name: chemical-shift-data-formatting
description: Use when you have collected or parsed 1H and 13C NMR peak data (chemical
  shift values and intensities) and need to submit it to the SMART 3 /api/smart3/search
  endpoint or similar TensorFlow Serving-backed molecular classification system that
  expects peaks as JSON rather than raw spectroscopic files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - TensorFlow Serving
  - DeepSAT
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-shift-data-formatting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Format nuclear magnetic resonance (NMR) peak data as JSON dictionaries with proton (1H) and carbon-13 (13C) chemical shift headers for programmatic submission to machine learning classification APIs. This skill bridges raw spectroscopic measurement into the structured input required by deep learning molecular classifiers.

## When to use

You have collected or parsed 1H and 13C NMR peak data (chemical shift values and intensities) and need to submit it to the SMART 3 /api/smart3/search endpoint or similar TensorFlow Serving-backed molecular classification system that expects peaks as JSON rather than raw spectroscopic files.

## When NOT to use

- Input is already a feature table or pre-computed molecular fingerprint—this skill reformats raw spectra, not derived features.
- You are working with 2D NMR (COSY, HSQC) or other multi-dimensional experiments that require matrix-based data structures rather than simple peak lists.
- The target API does not use TensorFlow Serving or does not document JSON peak list input format.

## Inputs

- 1H NMR chemical shift values (ppm scale)
- 13C NMR chemical shift values (ppm scale)
- Peak intensities or integration values
- Model metadata schema (from /model/metadata endpoint)

## Outputs

- JSON list of dictionaries with '1H' and '13C' keys
- Structured payload ready for /api/smart3/search POST request
- Classification response (molecular class predictions)

## How to apply

Extract proton (1H) and carbon-13 (13C) chemical shift values and corresponding peak intensities from your NMR acquisition or parsing pipeline. Organize the data as a list of dictionaries, with '1H' and '13C' as keys, mapping to arrays or nested objects containing shift values and peak metadata. Before formatting, query the TensorFlow Serving /model/metadata endpoint to retrieve the current expected input schema—model input names may change and require code updates. Construct the JSON payload with peaks formatted exactly as the endpoint schema specifies, then POST to /api/smart3/search. Validate the response structure and check that classification scores or predictions are returned.

## Related tools

- **TensorFlow Serving** (Hosts the SMART 3 molecular classification model and exposes /model/metadata and /api/smart3/search endpoints for programmatic inference)
- **DeepSAT** (Source repository for SMART 3 classification framework and NMR model implementation) — https://github.com/mwang87/DeepSAT

## Examples

```
import json; peaks = [{'1H': [7.2, 7.5], '13C': [128.5, 129.1]}]; requests.post('http://localhost:8501/api/smart3/search', json={'peaks': peaks})
```

## Evaluation signals

- JSON payload is valid and parses without schema errors when submitted to the endpoint.
- Peaks are formatted as a list of dicts with exactly '1H' and '13C' keys as documented in the /model/metadata schema.
- HTTP 200 response received with classification predictions (not 400 or 422 validation errors).
- Returned molecular class predictions are semantically plausible (e.g., predicted compounds match known NMR patterns for the input peaks).
- Peak counts and value ranges (ppm scales) are preserved from input to output without truncation or loss of precision.

## Limitations

- Model input names may change between deployments; code must query /model/metadata endpoint dynamically rather than hard-coding schema assumptions.
- No changelog is publicly available to track breaking changes to the endpoint or input/output format.
- Skill assumes 1D 1H and 13C NMR data only; multi-dimensional or edited NMR experiments are not addressed by the documented JSON peak list format.
- Chemical shift reference frame (e.g., TMS for 1H, CDCl3 for 13C) must be consistent with the model's training data; no documented reference-shifting or calibration step is provided.

## Evidence

- [intro] JSON list with 1H and 13C headers: "You can put in your peaks as a json list of dicts, with 1H,13C as headers"
- [intro] TensorFlow Serving metadata endpoint: "We pass through tensorflow serving at this url: /model/metadata"
- [intro] Model input schema changes: "If the model input names change, then we need to change it in the code"
- [intro] Classification endpoint and payload structure: "Classify programmatically via /api/smart3/search endpoint by passing peaks as JSON list"
