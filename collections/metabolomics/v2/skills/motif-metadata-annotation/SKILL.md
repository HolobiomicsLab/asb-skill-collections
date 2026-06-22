---
name: motif-metadata-annotation
description: Use when after LDA inference has produced a trained motifset (motifset.json or motifset_optimized.json) with Mass2Motif probability distributions over fragments and neutral losses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MS2LDA
  - Python
  - MAG (Mass2Motif Annotation Guidance)
  - Spec2Vec
  - MotifDB
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
---

# motif-metadata-annotation

## Summary

Annotate discovered Mass2Motifs with structural substructure meaning, fragment/neutral-loss composition, and spectral loading counts to enable biological interpretation and downstream network visualization. This skill transforms raw motif probability distributions into human-interpretable annotations that bridge fragmentation patterns to chemical structure.

## When to use

After LDA inference has produced a trained motifset (motifset.json or motifset_optimized.json) with Mass2Motif probability distributions over fragments and neutral losses. Apply this skill when you need to assign chemical or biological meaning to motifs, export motif metadata for network construction, or prepare motifs for MotifDB comparison and publication.

## When NOT to use

- Input motifset has not yet undergone LDA inference or contains only raw spectral data without learned motif parameters.
- Goal is preliminary motif discovery only, without need for downstream visualization or database integration.
- Spectra are already annotated with known compound identities; use direct structure-based annotation instead.

## Inputs

- motifset.json or motifset_optimized.json (inferred LDA motif definitions with fragment/loss probabilities)
- MS2LDA model output (motif-spectrum loading matrix or theta matrix)
- Optionally: MotifDB library or Spec2Vec embeddings for automated annotation

## Outputs

- Annotated motif metadata (JSON or tsv: motif_id, name, top_fragments, top_losses, spectra_count, annotations)
- Annotated network nodes ready for GraphML serialization
- Motif annotation report (human-readable summary of motif compositions)

## How to apply

Load the inferred motifset and extract Mass2Motif definitions (fragment and neutral-loss probability compositions). For each motif, compute or retrieve the pseudo-spectra representation by extracting the top-weighted fragments and losses ranked by probability. Annotate each motif node with: (1) motif ID and name, (2) ranked list of characteristic fragments and neutral losses with their probabilities, (3) count of spectra assigned to or loading significantly on that motif, and (4) optionally link to known compound or substructure databases (e.g. MotifDB via Spec2Vec similarity or MAG automated annotation). Record these metadata as node attributes before serializing to GraphML or exporting for visualization. Validate annotations by checking that high-probability fragments correspond to chemically sensible neutral losses and that motif loadings sum appropriately across the spectral corpus.

## Related tools

- **MS2LDA** (Orchestrates LDA inference and provides motifset outputs; core platform within which annotation occurs) — https://github.com/vdhooftcompmet/MS2LDA
- **MAG (Mass2Motif Annotation Guidance)** (Automated annotation of Mass2Motif meanings using spectral similarity and knowledge bases) — https://github.com/vdhooftcompmet/MS2LDA
- **Spec2Vec** (Spectral embedding model used by MAG to match motifs against known MotifDB entries for automated substructure assignment) — https://zenodo.org/records/15688609
- **MotifDB** (Searchable reference database of Mass2Motifs for comparison and validation of discovered motif annotations) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Scripting environment for loading motifset JSON, computing pseudo-spectra, and assembling node metadata)

## Examples

```
# Python snippet to annotate motifs from MS2LDA output:
import json
from ms2lda.postprocessing import load_motifset, annotate_motif_nodes
motifset = json.load(open('motifset_optimized.json'))
for motif_id, motif_def in motifset['motifs'].items():
    top_frags = sorted(motif_def['fragments'].items(), key=lambda x: x[1], reverse=True)[:10]
    top_losses = sorted(motif_def['neutral_losses'].items(), key=lambda x: x[1], reverse=True)[:10]
    metadata[motif_id] = {'fragments': top_frags, 'losses': top_losses, 'count': spectrum_loadings[motif_id].sum()}
```

## Evaluation signals

- Each motif node has a non-empty, ordered list of top-K fragments and neutral losses ranked by probability; probabilities sum to expected values.
- Motif spectra_count (loading) is positive and consistent with the corpus size and motif-spectrum loading matrix (theta).
- If MAG/Spec2Vec annotations are applied, each motif has a ranked list of MotifDB matches with cosine similarity scores; top match exceeds a reasonable threshold (e.g. > 0.7).
- Annotated metadata is serializable to GraphML and can be rendered by visualization tool without schema errors.
- Manual spot-check: review a sample of 3–5 motifs; verify that high-probability fragments and losses form chemically coherent neutral-loss pairs (e.g., loss of H₂O from hydroxyl groups, loss of CO₂ from carboxylic acids).

## Limitations

- Automated annotation (MAG/Spec2Vec) depends on MotifDB coverage; rare or novel motifs may lack good reference matches.
- Pseudo-spectra reconstruction relies on top-K fragment selection; low-probability tail fragments are discarded, potentially losing nuanced structural information.
- Motif interpretability is subjective; high-probability fragments alone do not guarantee chemical correctness without expert validation or external structural evidence.
- No established significance threshold for motif-spectrum loading; unclear which spectra 'belong' to a motif when loadings are distributed across many motifs (soft assignment problem inherent to LDA).

## Evidence

- [other] Extract Mass2Motif definitions (fragment and neutral-loss compositions): "Load the inferred motifset from motifset.json or motifset_optimized.json, extracting Mass2Motif definitions (fragment and neutral-loss compositions)"
- [other] Annotate nodes with motif metadata: "Annotate nodes with motif metadata (ID, fragment/loss composition, spectra count loading on motif) and edges with similarity scores"
- [methods] Automated annotation of M2M using MAG: "Automated annotation of M2M using MAG"
- [methods] Spec2Vec for annotation guidance: "Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec"
- [readme] Motif discovery accelerates structure elucidation: "identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification, thus accelerating structure elucidation and analysis"
- [methods] Comparison of motifs to known entries in MotifDB: "Compare motifs to known entries in MotifDB"
