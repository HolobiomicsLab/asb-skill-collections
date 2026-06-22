---
name: json-parsing-motifset-extraction
description: Use when you have completed the MS2LDA LDA modeling phase and possess motifset.json or motifset_optimized.json files containing inferred Mass2Motifs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - MS2LDA
  - Python
  techniques:
  - LC-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# JSON Parsing for Motifset Extraction

## Summary

Extract Mass2Motif definitions from MS2LDA's JSON output files (motifset.json or motifset_optimized.json) to retrieve fragment and neutral-loss compositions for downstream network construction and spectral similarity analysis.

## When to use

You have completed the MS2LDA LDA modeling phase and possess motifset.json or motifset_optimized.json files containing inferred Mass2Motifs. You need to access the underlying fragment and neutral-loss probability distributions within each motif to compute motif-level pseudo-spectra or build a motif network graph for visualization and export.

## When NOT to use

- Your input is a raw MS/MS spectra file (mzML, mzXML, etc.) rather than a motifset JSON — preprocessing and LDA modeling must occur first.
- You need only to visualize raw spectra or annotate single compounds — motif extraction is unnecessary for basic spectral browsing.
- The JSON file is corrupted or missing required keys (fragments, neutral_losses) — error handling must precede downstream use.

## Inputs

- motifset.json (JSON file containing inferred Mass2Motifs from LDA)
- motifset_optimized.json (optional alternative JSON file with optimized motif parameters)

## Outputs

- In-memory motifset dictionary or DataFrame mapping motif ID → {fragments, neutral_losses, metadata}
- Validated motif fragment-probability and neutral-loss-probability mappings ready for pseudo-spectra reconstruction

## How to apply

Read the motifset JSON file using Python's json module or equivalent JSON parser. Iterate through the motif objects, extracting for each Mass2Motif: (1) motif ID, (2) fragment mass–probability pairs, (3) neutral loss mass–probability pairs, and (4) metadata such as spectral loading counts. Store these in an in-memory data structure (dict, DataFrame, or custom class) indexed by motif ID for fast lookups during subsequent pseudo-spectra reconstruction or similarity computation. Validate that all expected keys are present and probability distributions sum to ~1.0 (with tolerance for floating-point rounding).

## Related tools

- **MS2LDA** (Produces the motifset JSON files containing Mass2Motif definitions and LDA model outputs) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Language and runtime for executing JSON parsing and data structure construction)

## Examples

```
import json
with open('motifset.json', 'r') as f:
    motifset = json.load(f)
for motif_id, motif_data in motifset.items():
    fragments = motif_data.get('fragments', {})
    losses = motif_data.get('neutral_losses', {})
    print(f'Motif {motif_id}: {len(fragments)} fragments, {len(losses)} losses')
```

## Evaluation signals

- All motif objects in the JSON are successfully parsed without deserialization errors.
- Each motif contains expected keys: ID, fragment compositions with probabilities, neutral-loss compositions with probabilities, and metadata (e.g., spectral counts).
- Probability distributions within each motif sum to approximately 1.0 (within ±0.01 floating-point tolerance).
- Extracted motif data can be indexed by ID and retrieved in O(1) time for use in downstream pseudo-spectra or similarity calculations.
- No missing or null values in critical fields; metadata fields are consistent across motifs (e.g., all records have the same keys).

## Limitations

- JSON schema must match MS2LDA's output format; other JSON motif formats are not automatically compatible.
- Large motifsets (thousands of motifs) may require memory optimization (e.g., streaming or lazy loading) to avoid heap exhaustion.
- Probability normalization assumes clean floating-point arithmetic; edge cases with extreme precision loss or non-normalized raw counts require explicit validation.
- No built-in validation of chemical feasibility of fragments or losses; garbage-in-garbage-out if the LDA model is poorly parameterized or trained on noisy input spectra.

## Evidence

- [other] Load the inferred motifset from motifset.json or motifset_optimized.json, extracting Mass2Motif definitions (fragment and neutral-loss compositions).: "Load the inferred motifset from motifset.json or motifset_optimized.json, extracting Mass2Motif definitions (fragment and neutral-loss compositions)."
- [methods] MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework that brings the concept of topic modeling to the world of tandem mass spectrometry: "MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework that brings the concept of topic modeling to the world of tandem mass spectrometry"
- [methods] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns"
- [other] Retrieve or reconstruct pseudo-spectra representations from each motif's probability-weighted fragments and losses.: "Retrieve or reconstruct pseudo-spectra representations from each motif's probability-weighted fragments and losses."
