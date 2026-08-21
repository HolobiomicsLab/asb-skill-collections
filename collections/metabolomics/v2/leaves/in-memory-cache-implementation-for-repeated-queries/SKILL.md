---
name: in-memory-cache-implementation-for-repeated-queries
description: Use when when deploying a high-throughput molecular classification API
  (e.g., /classify endpoint) where the same SMILES strings are expected to be queried
  repeatedly across multiple users or time windows, and response latency is a performance
  constraint.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - Python
  - TensorFlow Serving
  - Docker / docker-compose
  - NP Classifier models (Keras/HDF5)
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

# in-memory-cache-implementation-for-repeated-queries

## Summary

Implement server-side in-memory caching to store and retrieve prior classification results for repeated SMILES queries, reducing computational latency and improving API response time for duplicate requests.

## When to use

When deploying a high-throughput molecular classification API (e.g., /classify endpoint) where the same SMILES strings are expected to be queried repeatedly across multiple users or time windows, and response latency is a performance constraint.

## When NOT to use

- When classification results must reflect real-time model updates or retraining; cached results will be stale.
- When SMILES queries are highly diverse and rarely repeated; cache hit rate will be low and memory overhead unjustified.
- When strict reproducibility auditing requires all classification decisions to be logged with timestamps; caching can obscure request timing.

## Inputs

- SMILES string (URL query parameter via /classify?smiles=<string>)
- Optional cached flag (boolean query parameter)

## Outputs

- Natural-product classification result (from cached store or TensorFlow model output)
- Reduced API response latency (for cache hits)

## How to apply

Add optional caching logic to the API endpoint handler that intercepts incoming SMILES query parameters before passing them to the TensorFlow model inference layer. First, check if the query SMILES string exists as a key in an in-memory cache store; if a hit occurs, return the cached classification result immediately without invoking TensorFlow Serving. If a miss occurs, process the SMILES through the full inference pipeline (via TensorFlow Serving using the 'input_2048' and 'input_4096' input layers and 'output' layer), retrieve the classification prediction, store the result in the cache keyed by the SMILES string, and return it to the client. Support a 'cached' boolean flag as an optional query parameter to allow clients to explicitly request cached results or bypass the cache if needed. Use a simple in-memory dictionary or LRU cache structure to manage the store, documenting cache eviction policy and memory bounds.

## Related tools

- **TensorFlow Serving** (Backend inference engine that processes non-cached SMILES queries and returns classification predictions via REST API)
- **Docker / docker-compose** (Containerization and orchestration platform for deploying the API server with persistent in-memory cache across container instances)
- **NP Classifier models (Keras/HDF5)** (Pre-trained neural network models (with 'input_2048', 'input_4096' input layers and 'output' layer) that are invoked for cache misses) — https://github.com/mwang87/NP-Classifier

## Examples

```
curl 'http://localhost:5000/classify?smiles=CC(=O)Oc1ccccc1C(=O)O&cached=true'
```

## Evaluation signals

- Cache hit rate increases over time as repeated SMILES strings are queried; verify via endpoint logging or metrics collection.
- Response time for cached queries is significantly lower (typically <10ms) than uncached queries that invoke TensorFlow Serving.
- Repeated identical SMILES query returns identical classification output from both cache and fresh model inference, ensuring consistency.
- Cache key collisions do not occur; verify by confirming each unique SMILES maps to exactly one cached result.
- Memory consumption of the cache store remains within defined bounds; no unbounded growth as queries accumulate.

## Limitations

- In-memory cache is lost on API server restart; consider persistence layer (e.g., Redis) for production durability.
- Cache coherency issues may arise in multi-instance deployments if each container maintains a separate cache; consider shared cache backend.
- Classification results become stale if underlying TensorFlow models are updated or retrained; cache invalidation strategy must be defined.
- Large SMILES strings or very high query volume can exhaust available memory; LRU eviction or size limits are required.
- Privacy implications: the README notes that structures are logged but not users; verify caching does not inadvertently reveal query patterns.

## Evidence

- [readme] You can also provide cached flag to the params to get the cached version so make it faster: "You can also provide cached flag to the params to get the cached version so make it faster"
- [other] Implement optional caching logic in the endpoint handler to store and retrieve prior classification results.: "Implement optional caching logic in the endpoint handler to store and retrieve prior classification results."
- [readme] We pass through tensorflow serving at this url: "We pass through tensorflow serving at this url"
- [readme] Input layers' names should be "input_2048" and "input_4096"; Output layer's name should be "output": "Input layers' names should be "input_2048" and "input_4096"; Output layer's name should be "output""
