---
name: spectral-graph-construction-from-fragments
description: Use when after you have aligned fragment ion pairs between two MS/MS spectra using maximum weight matching and need to compute statistical significance scores for the matched pairs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SIMILE
  - Python
  - scipy
  - numpy
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

# spectral-graph-construction-from-fragments

## Summary

Construct a Laplacian embedding graph from matched fragment ion pairs across MS/MS spectra to model spectral relationships and enable statistical significance testing. This graph representation captures both direct mass difference frequencies and ancestor–descendant similarity relationships among fragments.

## When to use

After you have aligned fragment ion pairs between two MS/MS spectra using maximum weight matching and need to compute statistical significance scores for the matched pairs. Apply this skill when your input includes pairwise fragment ion matches with m/z values and you need to model how fragment similarity propagates through the fragmentation hierarchy.

## When NOT to use

- When spectra have not yet been aligned using maximum weight matching—construct the graph only after fragment pairs are identified.
- When input is a single spectrum; the Laplacian embedding is designed for interspectra comparison and significance estimation.
- When only pairwise m/z differences are available without structural relationship context; the method requires at least intraspectra fragment relationships to generate a meaningful null distribution.

## Inputs

- MS/MS fragmentation spectrum pair (precursor m/z, fragment m/z values, intensities)
- Maximum weight-matched fragment ion pairs with alignment scores
- Mass difference frequency matrix or transition probability matrix

## Outputs

- Laplacian embedding (pseudo-inverse of normalized Laplacian matrix)
- Pairwise commute-time distances between fragment ions
- Statistical significance scores (p-values or Z-scores) for matched pairs
- Matching ions report with scores, mass deltas, and significance metrics

## How to apply

Construct a transition matrix from the matched ion pairs by normalizing mass difference frequencies as transition probabilities. Convert this transition matrix into the pseudo-inverse of its normalized Laplacian to compute pairwise distances that reflect 'average commute time' between fragments—a measure that captures both direct similarity (property a: common mass differences) and indirect relationships through ancestor and descendant fragments (property b). This Laplacian embedding ensures that fragment ions sharing parents or children are recognized as similar, even if their direct mass difference is uncommon. Use the resulting embedding to perform statistical significance testing on each matched pair, yielding p-values or Z-scores that reflect the likelihood that matches are siblings rather than random co-occurrences.

## Related tools

- **SIMILE** (Python library that implements Laplacian embedding construction, maximum weight matching, and significance testing for MS/MS spectrum comparison) — https://github.com/biorack/simile
- **Python** (Runtime environment; SIMILE v2 provides example usage for constructing similarity matrices and Laplacian embeddings)
- **scipy** (Provides linear algebra functions (Laplacian matrix computation, matrix inversion) required for embedding construction)
- **numpy** (Array operations and numerical computation for transition matrix normalization and distance calculation)

## Examples

```
import simile as sml; S, spec_ids = sml.similarity_matrix(mzs, pmzs=pmzs, tolerance=tolerance); M = sml.multiple_match(S, spec_ids); spec_scores, pval, null_dist = sml.z_test(S, M, sml.sym_compare(M, spec_ids), spec_ids, return_dist=True); df = sml.matching_ions_report(S, M, sml.sym_compare(M, spec_ids), mzs, pmzs)
```

## Evaluation signals

- Laplacian matrix is positive semi-definite and symmetric; pseudo-inverse is well-conditioned (no singular values near machine epsilon).
- Commute-time distances between fragment ions with common ancestors/descendants are shorter than distances between unrelated fragments, confirming property (b) is captured.
- Significance p-values derived from the embedding show enrichment for matched pairs vs. null distribution generated from permuted intra/inter-spectral scores.
- Matching ions report contains non-null entries for all input matched pairs, with mass deltas and Z-scores spanning expected ranges (typically p < 0.05 for true positive matches).
- Symmetric matches (bidirectional) receive pro-score (+1) in comparison matrix; asymmetric matches receive con-score (−1), confirming graph structure reflects fragment relationship asymmetry.

## Limitations

- Performance depends on quality of upstream maximum weight matching; incorrectly matched pairs will propagate noise into the Laplacian embedding.
- Null distribution generation via permutation-based testing scales quadratically with spectrum count; larger datasets may require subsampling or approximate permutation schemes.
- Method assumes fragmentation follows a predictable tree-like hierarchy (parent–child relationships); spectra with complex, non-linear fragmentation pathways may show reduced specificity.
- Current implementation (SIMILE v2) explores but does not fully optimize multiple comparison correction across many spectrum pairs; asymmetry-based null distributions are ongoing research.

## Evidence

- [other] Construct a Laplacian embedding from the matched ion pairs to model the spectral graph structure and significance relationships.: "Construct a Laplacian embedding from the matched ion pairs to model the spectral graph structure and significance relationships."
- [readme] Fragment ions are similar if the difference in mass between them is common and if their ancestor and descendant fragment ions are similar.: "Fragment ions are similar if the difference in mass between them is common. Fragment ions are similar if their ancesetor and descendent fragment ions are similar."
- [readme] The pseudo-inverse of the normalized laplacian corresponds to an 'average commute time' distance between fragment ions.: "converting the transition matrix of (a) into the pseudo-inverse of its (normalized) laplacian. This corresponds to an 'average commute time' distance between fragment ions"
- [readme] A null distribution for spectral similarity leverages intraspectral comparisons to add confidence to interspectral comparisons.: "A null distribution for spectral similarity which leverages intraspectral comparisons to add confidence to interspectral comparisons."
- [intro] Maximum weight matching is used instead of original monotonic alignment method with improved performance.: "Maximum weight matching is used instead of original monotonic alignment method with improved performance"
