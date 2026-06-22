---
name: maximum-weight-matching-optimization
description: Use when you have computed pairwise similarity or mass difference scores between all fragment ions across two tandem mass spectra and need to select the non-overlapping set of ion pair matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SIMILE
  - Python
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# maximum-weight-matching-optimization

## Summary

Maximum weight matching identifies the optimal set of fragment ion pairs across two MS/MS spectra that maximizes alignment score while minimizing redundancy, replacing monotonic alignment methods with improved performance. This graph-theoretic approach forms the foundation for subsequent Laplacian embedding and statistical significance testing in spectral comparison.

## When to use

Apply this skill when you have computed pairwise similarity or mass difference scores between all fragment ions across two tandem mass spectra and need to select the best non-overlapping set of ion pair matches. Use it specifically when the alignment problem involves competing fragment pairs with heterogeneous match scores and you want to avoid assigning the same fragment ion to multiple pairs simultaneously.

## When NOT to use

- Input spectra have fewer than 2 fragment ions in each: matching requires at least one edge candidate per spectrum.
- Similarity matrix is already sparse or pre-filtered to a single match per ion: maximum weight matching is designed to resolve many-to-many matching scenarios, not single assignments.
- Monotonic (time-ordered) alignment is required by protocol or regulatory constraint: maximum weight matching is globally optimal but makes no assumption about fragment ion ordering by mass.

## Inputs

- Two MS/MS fragmentation spectra (precursor m/z, fragment m/z values, intensities)
- Similarity matrix (computed from mass difference frequencies and Laplacian transition probabilities)
- Spectrum identifiers and fragment ion indices

## Outputs

- Maximum weight matching matrix (bipartite adjacency matrix encoding optimal fragment ion pairs)
- Matched fragment ion pairs with match scores
- Matched ion indices for input to significance testing

## How to apply

Construct a weighted bipartite graph where nodes represent fragment ions from each spectrum and edge weights are derived from the similarity matrix (computed from mass difference frequencies and fragmentation process properties). Apply a maximum weight matching algorithm to select the subset of edges that maximizes the sum of edge weights while ensuring each node is matched at most once. This optimal matching set is then used as input to downstream Laplacian embedding construction and z-score significance testing. The rationale is that maximum weight matching avoids the redundancy and suboptimality of greedy or monotonic alignment methods, yielding fragment pairs that best reflect the biological relationship between spectra.

## Related tools

- **SIMILE** (Python library implementing maximum weight matching within the spectral comparison workflow; accepts similarity matrix and returns optimal fragment ion pair assignments) — https://github.com/biorack/simile

## Examples

```
import simile as sml; S, spec_ids = sml.similarity_matrix(mzs, pmzs=pmzs, tolerance=tolerance); M = sml.multiple_match(S, spec_ids)
```

## Evaluation signals

- Each fragment ion from either spectrum is assigned to at most one matched pair (bipartite matching property holds).
- The sum of edge weights in the selected matching is greater than or equal to any alternative valid matching of the same size.
- Matched ion pairs have mass differences (m/z deltas) consistent with plausible neutral losses or fragment ion relationships.
- The matching matrix M has the correct dimensions (number of spectra × number of spectra) and encodes only non-zero entries for matched fragment pairs.
- Downstream z-test and significance scores computed from the matching show lower p-values than those computed from greedy or monotonic alignment on the same spectra.

## Limitations

- Requires accurate computation of the similarity matrix beforehand; errors in mass difference frequency estimation or Laplacian pseudo-inverse calculation will propagate to suboptimal matches.
- Performance scales with the size of the similarity matrix (number of fragment ions); sparse spectra are handled efficiently but high-complexity spectra with many fragments may require computational optimization.
- Maximum weight matching is deterministic given a fixed similarity matrix; it does not capture uncertainty in individual match scores or account for alternative plausible alignments.
- Fragment ions with very low intensity or low signal-to-noise ratio may be incorrectly matched if the similarity matrix includes them without intensity weighting or filtering.

## Evidence

- [intro] Maximum weight matching is used instead of original monotonic alignment method with improved performance: "Maximum weight matching is used instead of original monotonic alignment method with improved performance"
- [other] Apply maximum weight matching to identify the optimal set of fragment ion pairs that maximize alignment score while minimizing redundancy: "Apply maximum weight matching to identify the optimal set of fragment ion pairs that maximize alignment score while minimizing redundancy"
- [readme] Generate max weight matching for similarity matrix: "# Generate max weight matching for similarity matrix
M = sml.multiple_match(S, spec_ids)"
- [readme] SIMILE contributes two concepts to the analysis of tandem mass spectrometry: 1. A similarity measure between fragment ions based on the fragmentation process: "SIMILE contributes two concepts to the analysis of tandem mass spectrometry: 1. A similarity measure between fragment ions based on the fragmentation process"
