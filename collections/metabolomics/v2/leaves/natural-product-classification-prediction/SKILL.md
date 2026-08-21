---
name: natural-product-classification-prediction
description: Use when you have molecular structures encoded as SMILES strings and
  need to classify them into natural-product chemical classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3361
  tools:
  - Python
  - Docker
  - docker-compose
  - TensorFlow 2.3.0
  - Keras
  - TensorFlow Serving
  - NP Classifier Repository
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- Make sure you have python installed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npclassifier_cq
    doi: 10.1021/acs.jnatprod.1c00399
    title: npclassifier
  dedup_kept_from: coll_npclassifier_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.1c00399
  all_source_dois:
  - 10.1021/acs.jnatprod.1c00399
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# natural-product-classification-prediction

## Summary

This skill deploys a pre-trained deep-learning classifier to predict natural-product chemical classes from SMILES molecular strings via a containerized REST API. It is used when you need to rapidly annotate chemical structures with their likely biosynthetic or functional class.

## When to use

You have molecular structures encoded as SMILES strings and need to classify them into natural-product chemical classes. This skill is appropriate when you want to batch-query a pre-trained model via HTTP, optionally retrieving cached results to improve latency for repeated queries on the same structures.

## When NOT to use

- Input is not a valid SMILES string or contains syntax errors that the parser cannot handle.
- You require real-time model retraining or fine-tuning; this skill uses frozen pre-trained models only.
- Your workflow demands sub-millisecond latency; containerized inference introduces network and serialization overhead.

## Inputs

- SMILES string(s) representing molecular structures
- Optional cached flag (boolean) for retrieval of prior predictions

## Outputs

- Natural-product chemical classification label(s)
- Prediction confidence or probability score(s)

## How to apply

First, download and verify the pre-trained NP Classifier models by running the provided shell script (get_models.sh) and confirming model layer names match the expected schema (input layers 'input_2048' and 'input_4096', output layer 'output'). Convert Keras models to HDF5 TensorFlow 2.3.0 format using Python with TensorFlow. Set up a Docker network (nginx-net) for service communication, then build and deploy the API server via docker-compose (make server-compose). Query the /classify endpoint by passing SMILES strings as the smiles parameter; optionally add a cached flag to retrieve prior classification results instead of re-running inference. Verify predictions by checking the model metadata endpoint (/model/metadata) and spot-checking outputs against known structures.

## Related tools

- **Docker** (Container runtime for isolated, reproducible API server deployment)
- **docker-compose** (Orchestration tool to define and run multi-container services (nginx, TensorFlow Serving, classifier API))
- **TensorFlow 2.3.0** (Framework used to convert Keras models into HDF5 format for TensorFlow Serving)
- **Keras** (Source model architecture format; models are trained and exported as Keras then converted to TF2 HDF5)
- **TensorFlow Serving** (Model serving system that handles predictions routed through the /classify endpoint)
- **NP Classifier Repository** (Source of pre-trained models, deployment configuration, and API endpoint logic) — https://github.com/mwang87/NP-Classifier

## Examples

```
curl 'http://localhost:8080/classify?smiles=CC(=O)Oc1ccccc1C(=O)O&cached=true'
```

## Evaluation signals

- Model metadata endpoint (/model/metadata) returns correctly named input layers ('input_2048', 'input_4096') and output layer ('output').
- Test SMILES strings consistently return valid classification labels from the model's known class vocabulary.
- Repeated queries with cached flag parameter return identical results in faster wall-clock time than non-cached queries.
- API responds with HTTP 200 and JSON-formatted predictions; invalid SMILES strings produce clear error messages.
- Spot-check a sample of predictions against domain knowledge or reference datasets to verify classification accuracy is within expected bounds.

## Limitations

- Model predictions are limited to chemical classes present in the training data; out-of-distribution structures may receive low-confidence or incorrect annotations.
- The skill requires TensorFlow 2.3.0 specifically for model conversion; later or earlier versions may introduce incompatibilities.
- Privacy trade-off: the system logs which structures were classified (for caching) but not which users queried them; query patterns may still be reconstructible.
- Caching assumes SMILES strings are canonicalized; non-canonical representations of the same molecule will be treated as distinct queries and not cached together.

## Evidence

- [readme] NP Classifier models are verified and deployed via Docker with pre-trained layer naming conventions: "Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output""
- [readme] SMILES strings are passed as query parameters to the /classify endpoint for classification: "Classify programmatically /classify?smiles=<>"
- [readme] Optional cached parameter improves performance for repeated structure queries: "You can also provide cached flag to the params to get the cached version so make it faster"
- [readme] Keras models must be converted to HDF5 TensorFlow 2.3.0 format before deployment: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
- [readme] Local deployment via Docker and docker-compose is the standard deployment pattern: "We typically will deploy this locally. To bring everything up, you need docker and docker-compose."
- [readme] TensorFlow Serving routes predictions through a metadata and classification endpoint: "We pass through tensorflow serving at this url: /model/metadata"
