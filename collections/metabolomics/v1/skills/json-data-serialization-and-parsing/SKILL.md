---
name: json-data-serialization-and-parsing
description: Use when you have discovered Mass2Motifs via LDA and need to (1) load a pre-computed motifset JSON file (e.g., motifset_optimized.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - MS2LDA
  - Python json module
  - MS2LDAViz
  - Spec2Vec
  - MAG (Mass2Motif Annotation Guidance)
derived_from:
- doi: 10.1093/bioinformatics/btx582
  title: ms2lda
evidence_spans:
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1093/bioinformatics/btx582
    title: ms2lda
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
---

# json-data-serialization-and-parsing

## Summary

Load trained motifsets and annotation records in JSON format, and export per-motif annotation results as JSON compatible with MS2LDAViz. This skill enables interoperability between MS2LDA's Mass2Motif discovery pipeline and downstream visualization/analysis tools by parsing structured JSON representations of motifs and their assigned substructure annotations.

## When to use

Apply this skill when you have discovered Mass2Motifs via LDA and need to (1) load a pre-computed motifset JSON file (e.g., motifset_optimized.json) containing all motif definitions and fragmentation patterns, or (2) export computed per-motif annotation records (with similarity scores and confidence metrics) in a format compatible with MS2LDAViz for interactive exploration.

## When NOT to use

- Input motifset is already loaded in memory as a native Python object and does not need round-trip serialization.
- Annotation results are intended for a non-JSON downstream tool that requires a different format (e.g., CSV, HDF5, database schema).
- Real-time streaming of motif annotations is required; JSON serialization introduces latency unsuitable for live annotation feedback.

## Inputs

- motifset JSON file (e.g., motifset_optimized.json containing Mass2Motif definitions)
- Per-motif annotation records (dictionaries or lists with motif IDs, labels, and scores)

## Outputs

- Parsed motifset object (dictionary or pandas DataFrame with motif metadata)
- JSON-serialized per-motif annotation records (JSON file compatible with MS2LDAViz)

## How to apply

First, load the trained motifset JSON file using Python's json module or pandas, validating that the structure contains expected motif identifiers and their associated fragment and neutral loss lists. After annotation (whether via Spec2Vec similarity lookup or other methods), serialize the per-motif annotation output—mapping each motif ID to suggested labels, similarity scores, and confidence metrics—into a JSON object following the MS2LDAViz schema. Ensure the output JSON is parseable and contains all required fields so that MS2LDAViz can ingest and render the results. The rationale is that JSON serialization provides a human-readable, schema-agnostic interchange format that decouples the MS2LDA computation pipeline from visualization and external database integration workflows.

## Related tools

- **Python json module** (Core library for parsing motifset JSON and serializing annotation records)
- **MS2LDAViz** (Target visualization application that consumes JSON-serialized per-motif annotations) — https://github.com/vdhooftcompmet/MS2LDA
- **Spec2Vec** (Generates similarity scores and annotations that are serialized into JSON output)
- **MAG (Mass2Motif Annotation Guidance)** (Produces per-motif annotation records that are exported as JSON) — https://github.com/vdhooftcompmet/MS2LDA

## Examples

```
import json
with open('motifset_optimized.json', 'r') as f:
    motifset = json.load(f)
annotations = {m['motif_id']: {'label': m.get('annotation', ''), 'score': 0.85} for m in motifset['motifs']}
with open('annotations.json', 'w') as f:
    json.dump(annotations, f, indent=2)
```

## Evaluation signals

- Loaded motifset JSON is parseable and contains expected keys (motif identifiers, fragments, neutral losses) with no missing or malformed entries.
- Exported per-motif annotation JSON validates against MS2LDAViz schema (contains required fields: motif ID, label, similarity score, confidence metric).
- JSON round-trip test: deserialize exported JSON, re-serialize, and confirm byte-for-byte or semantic equivalence (no data loss or corruption).
- MS2LDAViz successfully ingests and renders the exported JSON without import errors or missing visualization elements.
- All motif identifiers in the annotation JSON map back to entries in the original motifset JSON with no orphaned or duplicate IDs.

## Limitations

- JSON serialization does not enforce schema validation at write time; downstream tools (MS2LDAViz) may fail silently on malformed or incomplete records.
- Large motifsets (>10,000 motifs) may produce JSON files large enough to cause memory or parsing latency in some environments.
- JSON does not natively represent numerical precision for very large or very small similarity scores; floating-point rounding may occur.
- Complex nested annotation metadata (e.g., per-spectrum evidence or hierarchical substructure annotations) may require custom JSON structure design not covered by MS2LDAViz's default schema.

## Evidence

- [other] Load the trained motifset JSON file (motifset_optimized.json) containing all discovered Mass2Motifs.: "Load the trained motifset JSON file (motifset_optimized.json) containing all discovered Mass2Motifs."
- [other] Generate annotation records mapping each motif identifier to suggested labels, similarity scores, and confidence metrics.: "Generate annotation records mapping each motif identifier to suggested labels, similarity scores, and confidence metrics."
- [other] Export the per-motif annotation output in JSON format compatible with MS2LDAViz.: "Export the per-motif annotation output in JSON format compatible with MS2LDAViz."
- [methods] Automated annotation of M2M using MAG: "Automated annotation of M2M using MAG"
- [methods] Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec: "Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec"
