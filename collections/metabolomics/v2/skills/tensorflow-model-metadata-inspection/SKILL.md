---
name: tensorflow-model-metadata-inspection
description: Use when deploying a TensorFlow model through TensorFlow Serving and you need to verify that the exposed model's input layer names ('input_2048' and 'input_4096') and output layer name ('output') match the specifications required by downstream code.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - TensorFlow Serving
  - Python
  - docker-compose
derived_from:
- doi: 10.1021/jacs.9b13786
  title: CSCS / deep CNN natural-product annotation
evidence_spans:
- We pass through tensorflow serving at this url
- Make sure you have python installed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cscs_deep_cnn_natural_product_annotation_cq
    doi: 10.1021/jacs.9b13786
    title: CSCS / deep CNN natural-product annotation
  dedup_kept_from: coll_cscs_deep_cnn_natural_product_annotation_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jacs.9b13786
  all_source_dois:
  - 10.1021/jacs.9b13786
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tensorflow-model-metadata-inspection

## Summary

Validate TensorFlow model layer names by querying the /model/metadata endpoint exposed through TensorFlow Serving. This skill ensures that input and output layer names conform to expected specifications before performing downstream classification or prediction tasks.

## When to use

Apply this skill when deploying a TensorFlow model through TensorFlow Serving and you need to verify that the exposed model's input layer names ('input_2048' and 'input_4096') and output layer name ('output') match the specifications required by downstream code. Use this as a prerequisite validation step before integrating model predictions into a classification pipeline.

## When NOT to use

- Model is not deployed via TensorFlow Serving but instead loaded directly as a .pb or .h5 file; use static model introspection instead.
- Layer names have already been hardcoded and validated in downstream code and you are not updating the model.

## Inputs

- Running TensorFlow Serving instance with deployed model
- TensorFlow Serving metadata endpoint URL (e.g., http://localhost:8501/v1/models/<model_name>/metadata)

## Outputs

- Parsed JSON metadata object containing input and output layer names
- Verification report documenting metadata query result and layer name validation outcome

## How to apply

Start the TensorFlow Serving container (typically via docker-compose), then send a GET request to the /model/metadata endpoint at the TensorFlow Serving URL (e.g., http://localhost:8501/v1/models/<model_name>/metadata). Parse the returned JSON response to extract the input layer names and output layer name. Compare the extracted names against the expected values: input layers must be exactly 'input_2048' and 'input_4096', and the output layer must be exactly 'output'. If model input or output names deviate from these specifications, the consuming code must be updated accordingly. Document the validation outcome in a verification report that records both the queried metadata and the pass/fail status of layer name validation.

## Related tools

- **TensorFlow Serving** (Exposes model metadata via HTTP /model/metadata endpoint for remote inspection of layer names and signatures)
- **docker-compose** (Orchestrates TensorFlow Serving container startup and networking configuration for local model deployment)
- **Python** (Used to parse JSON response from metadata endpoint and automate validation logic)

## Examples

```
curl http://localhost:8501/v1/models/np_classifier/metadata | python -c "import sys, json; meta = json.load(sys.stdin); print('Input layers:', meta.get('inputs', [])); print('Output layers:', meta.get('outputs', []))"
```

## Evaluation signals

- HTTP GET request to /model/metadata endpoint returns a 200 status code with valid JSON response
- Parsed JSON contains 'input_names' field listing exactly ['input_2048', 'input_4096'] in any order
- Parsed JSON contains 'output_names' field listing exactly ['output']
- Verification report shows PASS status when all three layer name checks succeed
- If names do not match specifications, validation report explicitly identifies which layer names differ and triggers code update workflow

## Limitations

- The skill assumes TensorFlow Serving is running and accessible at the specified URL; network or container startup failures will cause the metadata query to fail.
- If model input or output layer names change in the deployed model, the consuming code must be manually updated—this skill only validates, it does not auto-patch.
- The /model/metadata endpoint format is specific to TensorFlow Serving; other model serving frameworks (e.g., Seldon, KServe) may expose metadata via different endpoints or JSON schemas.

## Evidence

- [readme] We pass through tensorflow serving at this url: /model/metadata: "We pass through tensorflow serving at this url:

```/model/metadata```"
- [readme] Input layers' names should be 'input_2048' and 'input_4096'; output layer's name should be 'output': "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [other] If model input names change from these specifications, the code must be updated accordingly.: "If model input names change from these specifications, the code must be updated accordingly."
- [other] Parse the JSON response to extract input layer names and output layer name and validate that the input layers are exactly 'input_2048' and 'input_4096' and output layer is exactly 'output'.: "Parse the JSON response to extract input layer names and output layer name. 4. Validate that the input layers are exactly 'input_2048' and 'input_4096' and output layer is exactly 'output'."
- [other] Send a GET request to the TensorFlow Serving /model/metadata endpoint: "Send a GET request to the TensorFlow Serving /model/metadata endpoint (typically http://localhost:8501/v1/models/<model_name>/metadata)."
