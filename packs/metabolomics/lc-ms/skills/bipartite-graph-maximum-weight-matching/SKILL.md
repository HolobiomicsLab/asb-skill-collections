---
name: bipartite-graph-maximum-weight-matching
description: 'Use when you have two MS/MS fragmentation spectra with fragment ion lists and computed pairwise mass differences (m/z deltas) between them, and you need to find the alignment of ion pairs that: (1) does not reuse any ion from either spectrum, (2) maximizes total matching quality (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SIMILE
  - Python
  - Python (scipy, numpy, pandas)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-022-30118-9
  title: SIMILE
evidence_spans:
- SIMILE (Significant Interrelation of MS/MS Ions via Laplacian Embedding) is a Python library
- is a Python library for interrelating fragmentation spectra with significance estimation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_simile_cq
    doi: 10.1038/s41467-022-30118-9
    title: SIMILE
  dedup_kept_from: coll_simile_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-022-30118-9
  all_source_dois:
  - 10.1038/s41467-022-30118-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Bipartite Graph Maximum Weight Matching

## Summary

Apply maximum weight matching algorithms (e.g., Hungarian algorithm) to a bipartite graph of fragment ions to identify the optimal set of non-overlapping ion pair alignments between two MS/MS spectra. This replaces monotonic alignment methods and maximizes total matching score based on mass delta and statistical significance.

## When to use

You have two MS/MS fragmentation spectra with fragment ion lists and computed pairwise mass differences (m/z deltas) between them, and you need to find the best alignment of ion pairs that: (1) does not reuse any ion from either spectrum, (2) maximizes total matching quality (e.g., cosine similarity or significance score), and (3) captures complex, non-monotonic ion correspondence patterns that linear or greedy methods would miss.

## When NOT to use

- You require monotonic (strictly ordered) ion alignment for regulatory or method-validation reasons; maximum weight matching may produce non-sequential pairings.
- One or both spectra have fewer than two fragment ions; bipartite matching requires at least one node per partition.
- Your fragment ions are already pre-aligned or the alignment method is fixed by protocol (e.g., fixed fragmentation ladders).

## Inputs

- Two MS/MS spectra (precursor m/z and fragment ion m/z lists)
- Pairwise mass difference matrix (m/z deltas between all fragment ion pairs across spectra)
- Edge weight scores (cosine similarity, statistical significance, or other mass delta-derived metric)

## Outputs

- Aligned ion pair list with matched fragment m/z values from both spectra
- Mass deltas (Δm/z) for each aligned pair
- Matching scores for each pair
- Structured matching ions report summarizing all scores and mass deltas with metadata

## How to apply

First, parse the two input MS/MS spectra (precursor m/z and fragment ion lists) into structured format. Compute all pairwise mass differences (m/z deltas) between fragment ions of the two spectra. Build a bipartite graph where nodes represent fragment ions from each spectrum and edge weights are derived from mass delta scores (e.g., based on cosine similarity or statistical significance of the mass difference). Apply a maximum weight matching algorithm (e.g., Hungarian algorithm or similar graph matching approach) to identify the optimal set of non-overlapping ion pair alignments that maximize total edge weight. Extract and report the aligned ion pairs with matched fragment m/z values, mass deltas, and matching scores. The rationale is that maximum weight matching captures both local mass similarity and global context through the graph structure, unlike monotonic alignment which enforces strict ordering and may miss better but non-sequential matches.

## Related tools

- **SIMILE** (Python library that implements maximum weight matching for MS/MS spectrum alignment with significance estimation; core tool for executing this workflow) — https://github.com/biorack/simile
- **Python (scipy, numpy, pandas)** (Numerical and graph algorithm libraries; scipy.optimize provides Hungarian algorithm and other matching implementations)

## Examples

```
import simile as sml
S, spec_ids = sml.similarity_matrix(mzs, pmzs=pmzs, tolerance=0.1)
M = sml.multiple_match(S, spec_ids)
df = sml.matching_ions_report(S, M, C, mzs, pmzs)
```

## Evaluation signals

- All fragment ions from each spectrum appear in at most one matched pair (non-overlapping constraint satisfied).
- Total edge weight of the matching is globally maximal (verify against brute-force or known-optimal solution for small test cases).
- Matched pairs are reported with non-null m/z deltas and matching scores; no NaN or infinity values in output.
- Comparison with monotonic alignment baseline shows equal or improved performance metrics (e.g., spectral similarity p-value, matching accuracy on known standards).
- Matching ions report contains all required metadata: source spectrum IDs, matched m/z pairs, mass deltas, statistical significance scores, and any symmetry/asymmetry flags.

## Limitations

- Computational complexity scales with O(n³) for the Hungarian algorithm; very large fragment ion lists may be slow without optimization.
- Edge weight construction (mass delta scoring) must be tuned carefully; poor scoring will produce high-weight but chemically irrelevant matches.
- Maximum weight matching is agnostic to chemical plausibility; post-hoc filtering or validation against known fragmentation rules may be needed.
- The method assumes edge weights are symmetric or properly normalized; asymmetric or directional relationships between ions are not captured by the basic bipartite model.

## Evidence

- [other] Apply maximum weight matching (e.g., using the Hungarian algorithm or similar graph matching approach) to identify the optimal set of non-overlapping ion pair alignments that maximize total edge weight.: "Apply maximum weight matching (e.g., using the Hungarian algorithm or similar graph matching approach) to identify the optimal set of non-overlapping ion pair alignments that maximize total edge"
- [intro] Maximum weight matching is used instead of original monotonic alignment method with improved performance: "Maximum weight matching is used instead of original monotonic alignment method with improved performance"
- [other] Build a bipartite graph where nodes represent fragment ions from each spectrum and edge weights are derived from the mass delta scores (e.g., cosine similarity or statistical significance of the mass difference).: "Build a bipartite graph where nodes represent fragment ions from each spectrum and edge weights are derived from the mass delta scores (e.g., cosine similarity or statistical significance of the mass"
- [intro] Matching ions report summarizing all scores and mass deltas with metadata: "Matching ions report summarizing all scores and mass deltas with metadata"
- [readme] # Generate max weight matching for similarity matrix
M = sml.multiple_match(S, spec_ids): "# Generate max weight matching for similarity matrix
M = sml.multiple_match(S, spec_ids)"
