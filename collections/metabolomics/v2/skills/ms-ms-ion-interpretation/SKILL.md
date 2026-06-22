---
name: ms-ms-ion-interpretation
description: Use when when you have two MS/MS spectra (each with a precursor m/z and a list of fragment ion m/z values) and need to identify which fragment ions correspond between them, especially when structural differences make simple monotonic alignment unreliable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3938
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SIMILE
  - Python
  - scipy
  - numpy
  - pandas
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
---

# MS/MS Ion Interpretation via Maximum Weight Matching

## Summary

Aligns fragment ions between two tandem mass spectra by computing mass difference frequencies and applying maximum weight matching to identify the optimal set of non-overlapping ion pair alignments that maximize statistical significance. This replaces monotonic alignment with a graph-based approach that captures both direct mass similarities and indirect relationships through ancestor/descendant fragment ions.

## When to use

When you have two MS/MS spectra (each with a precursor m/z and a list of fragment ion m/z values) and need to identify which fragment ions correspond between them, especially when structural differences make simple monotonic alignment unreliable. Use this when you want alignment scores to reflect not just mass deltas but also the broader fragmentation network structure.

## When NOT to use

- Input spectra have <3 fragment ions each—matching algorithms require sufficient graph density to compute meaningful weight distributions.
- You are comparing a single spectrum to itself (use intra-spectral matching properties instead).
- Your goal is fragment ion structure elucidation rather than spectrum-to-spectrum comparison—this skill aligns ions, it does not identify their chemical structures.

## Inputs

- MS/MS spectrum 1 (precursor m/z + fragment ion m/z list)
- MS/MS spectrum 2 (precursor m/z + fragment ion m/z list)
- Mass tolerance (ppm or m/z units)
- Optional: neutral loss difference counts (precursor-based)

## Outputs

- Bipartite matching matrix M (fragment ion pairs and weights)
- Comparison matrix C (symmetric vs. asymmetric match indicators)
- Spectral similarity score with p-value
- Null distribution (from permutation z-test)
- Matching ions report (DataFrame with matched fragment m/z, mass deltas, all scores, and metadata)

## How to apply

Parse both input spectra into structured format (precursor m/z and fragment ion m/z lists). Compute all pairwise mass differences (m/z deltas) between fragment ions across spectra and construct a transition matrix with row-normalized mass difference frequencies. Convert the transition matrix to the pseudo-inverse of its normalized Laplacian to capture 'average commute time' distances—this satisfies two properties: (a) fragments with common mass differences are similar, and (b) fragments with similar ancestors/descendants are similar. Build a bipartite graph where nodes are fragment ions and edge weights derive from the Laplacian-based similarity scores. Apply maximum weight matching (Hungarian algorithm or equivalent) to identify the optimal non-overlapping ion pair alignments. Calculate significance via z-test using a null distribution built from intra- and inter-spectral permutations to generate p-values, then extract and report aligned ion pairs with matched m/z values, mass deltas, and matching scores.

## Related tools

- **SIMILE** (Python library implementing maximum weight matching, Laplacian-based ion similarity, and significance testing for MS/MS alignment) — https://github.com/biorack/simile
- **Python** (Runtime environment for SIMILE library and numerical workflows)
- **scipy** (Provides linear algebra (Laplacian pseudo-inverse computation) and statistical functions)
- **numpy** (Underlying array operations for mass delta matrices and graph weights)
- **pandas** (Data structure for matching ions report output)

## Examples

```
import simile as sml
S, spec_ids = sml.similarity_matrix(mzs, pmzs=pmzs, tolerance=0.1)
M = sml.multiple_match(S, spec_ids)
C = sml.sym_compare(M, spec_ids)
spec_scores, pval, null_dist = sml.z_test(S, M, C, spec_ids, return_dist=True, log_size=5)
df = sml.matching_ions_report(S, M, C, mzs, pmzs)
```

## Evaluation signals

- Verify the bipartite graph has no overlapping edges in the final matching—each fragment ion appears in at most one pair.
- Check that the total edge weight of the matched set is maximal: no alternative matching yields a higher sum of weights.
- Confirm the p-value is correctly computed from the null distribution; p-values should range [0, 1] and reflect the rarity of the observed score under permutation.
- Validate that symmetric matches (present in both M[i,j] and M[j,i]) are marked as +1 in the comparison matrix C, and asymmetric matches as −1.
- Inspect the matching ions report for rows with missing m/z values or NaN scores—these indicate unmatched or low-confidence ions and should be flagged.

## Limitations

- Algorithm assumes fragment ions arise from the same or structurally similar precursors; large chemical structural differences may yield uninformative alignments even with statistical significance.
- Laplacian-based similarity is sensitive to mass tolerance parameter; tight tolerance may fragment the graph into isolated nodes, while loose tolerance may collapse distinct ion clusters.
- Multiple comparison statistics in SIMILE V2 are still under active research; the null distribution generated by permutation may underestimate variance in some chemical classes.
- Computational cost scales with the number of fragment ions; very large spectra (>1000 ions) may require optimized or parallelized graph matching.
- Current implementation assumes no multi-charge fragments; if both singly- and multiply-charged ions are present in the same spectrum, the mass delta computation must account for charge state explicitly.

## Evidence

- [readme] Maximum weight matching replaces monotonic alignment method with improved performance: "Maximum weight matching is used instead of original monotonic alignment method with improved performance"
- [readme] Laplacian-based similarity measure captures ancestor/descendant relationships: "Property (b) is satisfied by converting the transition matrix of (a) into the pseudo-inverse of its (normalized) laplacian. This corresponds to an "average commute time" distance between fragment ions"
- [readme] Fragment similarity is defined by common mass differences and ancestral relationships: "Fragment ions are similar if the difference in mass between them is common. Fragment ions are similar if their ancesetor and descendent fragment ions are similar."
- [readme] Null distribution generated using intra- and inter-spectral comparisons: "By leveraging SIMILE's fragment ion similarity measure which conforms to this analogy, we can ask how likely it is that the fragment ions matched up between fragmentation spectra by SIMILE are"
- [intro] Workflow includes multiple matching in addition to pairwise matching: "Multiple matching in addition to original pairwise matching for fragment centric analyses"
- [intro] SIMILE V2 offers faster mass delta counting and significance testing: "SIMILE V2 features much faster mass delta counting and significance testing"
