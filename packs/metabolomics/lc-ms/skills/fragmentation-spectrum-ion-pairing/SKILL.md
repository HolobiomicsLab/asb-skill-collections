---
name: fragmentation-spectrum-ion-pairing
description: 'Use when you have two MS/MS spectra (precursor m/z and fragment ion lists) and need to identify the non-overlapping set of fragment ion alignments. Use this skill when: (1) you want to move beyond monotonic alignment to capture complex ion relationships;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# Reconstruct maximum weight matching alignment of MS/MS spectra

## Summary

Apply maximum weight matching (e.g., Hungarian algorithm) to optimally align fragment ion pairs between two tandem MS/MS spectra by maximizing total edge weight in a bipartite graph. This replaces monotonic alignment methods to achieve improved matching performance while accounting for mass difference significance.

## When to use

You have two MS/MS spectra (precursor m/z and fragment ion lists) and need to identify the best non-overlapping set of fragment ion alignments. Use this skill when: (1) you want to move beyond monotonic alignment to capture complex ion relationships; (2) you have computed pairwise mass difference (m/z delta) scores or cosine similarity between all fragment ion pairs; (3) you need the aligned pairs to maximize statistical significance or total similarity, not just preserve order; (4) you are comparing spectra from related but structurally different molecules where multiple plausible alignments exist.

## When NOT to use

- Input spectra are from unrelated compounds with drastically different fragmentation patterns; maximum weight matching assumes meaningful alignments exist across spectra.
- You require one-to-many or many-to-many fragment alignments at the spectrum level; use multiple matching for fragment-centric analyses instead of pairwise matching.
- Fragment ion m/z values or precursor m/z are not calibrated or have unknown systematic mass errors exceeding your chosen tolerance; mass delta scoring will be unreliable.

## Inputs

- Two MS/MS spectra (precursor m/z, fragment ion m/z list for each spectrum)
- Pairwise mass difference matrix or edge weight matrix between all fragment ion pairs
- Mass tolerance parameter (in ppm or Da) for significance computation
- Optional: Precursor-based neutral loss difference counts

## Outputs

- Aligned ion pair list with matched fragment m/z values from each spectrum
- Mass delta values (m/z differences) for each pair
- Matching scores (e.g., cosine similarity, statistical significance p-values)
- Structured matching ions report summarizing all scores and mass deltas with metadata

## How to apply

Parse the two input spectra into structured lists of fragment m/z values and precursor m/z. Compute all pairwise mass deltas (m/z differences) between fragment ions of the two spectra and assign edge weights derived from mass delta significance scores, cosine similarity, or other fragment relationship metrics. Construct a bipartite graph where nodes represent fragment ions from each spectrum and edges carry these weights. Apply a maximum weight matching algorithm (such as the Hungarian algorithm) to identify the optimal set of non-overlapping ion pair alignments that maximize the total edge weight. Extract and report the aligned ion pairs with their matched m/z values, mass deltas, matching scores, and metadata. The rationale is that maximum weight matching ensures global optimality across all ions rather than greedy or sequential alignment, and the weighting by mass delta significance or relationship score ensures alignments reflect the fragmentation process properties (e.g., common mass differences and related ancestor/descendant ions).

## Related tools

- **SIMILE** (Python library implementing maximum weight matching, mass delta significance testing, and matching ions reporting for MS/MS spectrum alignment) — https://github.com/biorack/simile
- **Python** (Core language for executing SIMILE library functions and graph matching algorithms)

## Examples

```
import simile as sml
S, spec_ids = sml.similarity_matrix(mzs, pmzs=pmzs, tolerance=tolerance)
M = sml.multiple_match(S, spec_ids)
df = sml.matching_ions_report(S, M, C, mzs, pmzs)
```

## Evaluation signals

- All matched ion pairs are non-overlapping: each fragment ion from each spectrum appears in at most one pair (bipartite matching invariant).
- Total edge weight (sum of matching scores across all pairs) is globally maximal; no alternative pairing yields a higher total score.
- Matched mass deltas reflect known fragmentation properties: common differences appear frequently, and paired ions exhibit coherent ancestor/descendant relationships (Laplacian embedding validation).
- p-values from z-test against the null distribution (generated by permuting intra- and inter-spectral similarity scores) indicate significance of the alignment; symmetric vs. asymmetric matches can be classified as 'pro' (confidence boosters) vs. 'con' (unreliable alignments).
- Output matching ions report is complete: all aligned pairs include m/z values, mass deltas, similarity scores, and statistical metadata; no NaN or missing values for reported pairs.

## Limitations

- Maximum weight matching assumes a solution exists in the bipartite graph; if fragment ion counts or mass distributions differ drastically between spectra, some ions may remain unmatched (no guarantee of perfect matching for all nodes).
- Performance depends critically on the quality and calibration of mass difference scoring and edge weights; poorly calibrated m/z values or inappropriate mass tolerance settings will degrade alignment quality.
- The method is optimized for pairwise matching between two spectra; for multiple spectra or complex network-level comparisons, separate pairwise alignments must be computed and post-processed.
- SIMILE V2 is pinned to Python 3.7 due to non-SIMILE dependencies, which may limit compatibility with newer Python ecosystems or dependency versions.
- Fragment ion abundance or intensity information is not explicitly incorporated into the bipartite matching; the method relies on m/z differences and structural relationships alone.

## Evidence

- [other] Build a bipartite graph where nodes represent fragment ions from each spectrum and edge weights are derived from the mass delta scores (e.g., cosine similarity or statistical significance of the mass difference). Apply maximum weight matching (e.g., using the Hungarian algorithm or similar graph matching approach) to identify the optimal set of non-overlapping ion pair alignments that maximize total edge weight.: "Build a bipartite graph where nodes represent fragment ions from each spectrum and edge weights are derived from the mass delta scores (e.g., cosine similarity or statistical significance of the mass"
- [intro] Maximum weight matching is used instead of original monotonic alignment method with improved performance: "Maximum weight matching is used instead of original monotonic alignment method with improved performance"
- [readme] Fragment ions are similar if the difference in mass between them is common. Fragment ions are similar if their ancesetor and descendent fragment ions are similar.: "Fragment ions are similar if the difference in mass between them is common. Fragment ions are similar if their ancesetor and descendent fragment ions are similar."
- [intro] Matching ions report summarizing all scores and mass deltas with metadata: "Matching ions report summarizing all scores and mass deltas with metadata"
- [readme] # Generate max weight matching for similarity matrix
M = sml.multiple_match(S, spec_ids)

# Report back mass deltas and scores for simile comparison
df = sml.matching_ions_report(S, M, C, mzs, pmzs): "# Generate max weight matching for similarity matrix
M = sml.multiple_match(S, spec_ids)

# Report back mass deltas and scores for simile comparison
df = sml.matching_ions_report(S, M, C, mzs, pmzs)"
- [readme] By leveraging SIMILE's fragment ion similarity measure which conforms to this analogy, we can ask how likely it is that the fragment ions matched up between fragmentation spectra by SIMILE are siblings.: "By leveraging SIMILE's fragment ion similarity measure which conforms to this analogy, we can ask how likely it is that the fragment ions matched up between fragmentation spectra by SIMILE are"
