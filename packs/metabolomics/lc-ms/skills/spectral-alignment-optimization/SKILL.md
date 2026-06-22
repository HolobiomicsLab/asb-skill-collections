---
name: spectral-alignment-optimization
description: Use when when you have two MS/MS fragmentation spectra (with precursor m/z values and fragment ion lists) and need to establish correspondence between their fragment ions beyond simple pairwise comparison.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
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

# Reconstruct the maximum weight matching alignment of MS/MS spectra in SIMILE

## Summary

Replace monotonic alignment with maximum weight matching to optimally align fragment ion pairs between two tandem mass spectra, maximizing the total edge weight of matched ions and improving alignment performance. This skill applies graph-based optimization to MS/MS fragmentation data to identify the globally optimal set of non-overlapping ion pair correspondences.

## When to use

When you have two MS/MS fragmentation spectra (with precursor m/z values and fragment ion lists) and need to establish correspondence between their fragment ions beyond simple pairwise comparison. Use this skill when you require globally optimal alignment rather than greedy or monotonic matching, particularly when ions may have variable mass accuracy, structural complexity, or when you need to report confidence scores for each matched pair.

## When NOT to use

- When you have only a single MS/MS spectrum (no second spectrum to align against)
- When your spectra contain fewer than 2 fragment ions each (insufficient data for meaningful graph-based matching)
- When you need to preserve the sequential order of ions as they appear in the fragmentation pattern (monotonic alignment is more appropriate than maximum weight matching if order preservation is a requirement)

## Inputs

- Two MS/MS fragmentation spectra, each containing: precursor m/z value and list of fragment ion m/z values
- Mass tolerance threshold (in ppm or Da) for defining valid pairwise m/z differences
- Similarity scoring function (e.g., cosine similarity, statistical significance of mass delta)

## Outputs

- Set of aligned ion pairs with matched fragment m/z values from both spectra
- Mass delta (m/z difference) for each matched pair
- Matching score for each aligned pair
- Structured matching ions report with all scores and metadata

## How to apply

First, parse the two input MS/MS spectra into structured lists of precursor m/z and fragment ion m/z values. Compute all pairwise mass differences (m/z deltas) between fragment ions from the two spectra and assign edge weights derived from mass delta similarity or cosine similarity scores. Construct a bipartite graph where fragment ions from each spectrum form the two node sets and edge weights reflect the quality of potential matches. Apply maximum weight matching (using the Hungarian algorithm or equivalent) to identify the optimal set of non-overlapping ion pair alignments that maximize total edge weight. Extract and report the aligned ion pairs with their matched m/z values, mass deltas, and matching scores.

## Related tools

- **SIMILE** (Python library that implements maximum weight matching for MS/MS spectrum alignment with Laplacian-based fragment ion similarity and significance estimation) — https://github.com/biorack/simile
- **Python** (Programming environment for implementing the alignment workflow and calling SIMILE library functions)

## Examples

```
import simile as sml
S, spec_ids = sml.similarity_matrix(mzs, pmzs=pmzs, tolerance=tolerance)
M = sml.multiple_match(S, spec_ids)
df = sml.matching_ions_report(S, M, C, mzs, pmzs)
```

## Evaluation signals

- All fragment ions from both input spectra are assigned to at most one match (non-overlapping constraint is satisfied)
- The sum of edge weights for all matched pairs is greater than or equal to any alternative matching of the same ions (global optimality check)
- Each matched pair has a well-defined mass delta and matching score within expected ranges (e.g., mass delta < tolerance threshold)
- Symmetric matches (ion A from spectrum 1 matched to ion B from spectrum 2, and vice versa) are identified and distinguished from asymmetric matches in comparison statistics
- The output matching ions report contains metadata for all matched pairs including precursor m/z, fragment m/z, mass deltas, and significance scores

## Limitations

- Maximum weight matching optimizes global alignment but does not preserve the sequential order of fragment ions as they appear in spectra; if monotonic progression matters for your interpretation, this approach may not be appropriate
- Performance depends on the quality and resolution of mass delta scoring; spectra with poor mass calibration or high noise may produce suboptimal alignments
- The method currently implements pairwise matching between two spectra; multiple matching across three or more spectra requires separate extension (though SIMILE V2 supports multiple matching for fragment-centric analyses)
- Significance estimation relies on a null distribution generated from intraspectral and interspectral permutations; small datasets or spectra with very few ions may produce unreliable p-values

## Evidence

- [intro] Maximum weight matching is used instead of original monotonic alignment method with improved performance: "Maximum weight matching is used instead of original monotonic alignment method with improved performance"
- [other] Build a bipartite graph where nodes represent fragment ions from each spectrum and edge weights are derived from the mass delta scores: "Build a bipartite graph where nodes represent fragment ions from each spectrum and edge weights are derived from the mass delta scores (e.g., cosine similarity or statistical significance of the mass"
- [other] Apply maximum weight matching to identify the optimal set of non-overlapping ion pair alignments that maximize total edge weight: "Apply maximum weight matching (e.g., using the Hungarian algorithm or similar graph matching approach) to identify the optimal set of non-overlapping ion pair alignments that maximize total edge"
- [other] Extract and report the aligned ion pairs, including matched fragment m/z values, mass deltas, and matching scores: "Extract and report the aligned ion pairs, including matched fragment m/z values, mass deltas, and matching scores in a structured output"
- [intro] Multiple matching in addition to original pairwise matching for fragment centric analyses: "Multiple matching in addition to original pairwise matching for fragment centric analyses"
- [readme] If x and y are similar, then their parents and children are similar; and if fragment ions are similar, then the transition probability between them is high: "If x and y are similar, then their parents and children are similar; and if fragment ions are similar, then the transition probability between them is high"
