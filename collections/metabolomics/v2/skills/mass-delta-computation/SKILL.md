---
name: mass-delta-computation
description: Use when when you have parsed two or more MS/MS spectra (precursor m/z
  and fragment ion lists) and need to quantify all pairwise mass differences between
  fragment ions before alignment or similarity scoring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SIMILE
  - Python
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-022-30118-9
  title: SIMILE
evidence_spans:
- SIMILE (Significant Interrelation of MS/MS Ions via Laplacian Embedding) is a Python
  library
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

# mass-delta-computation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute pairwise mass differences (m/z deltas) between fragment ions across tandem mass spectra, using either direct fragment-to-fragment differences or precursor-based neutral loss differences. This foundational operation enables graph-based matching and significance estimation in spectrum alignment workflows.

## When to use

When you have parsed two or more MS/MS spectra (precursor m/z and fragment ion lists) and need to quantify all pairwise mass differences between fragment ions before alignment or similarity scoring. This is essential when building a transition matrix for Laplacian embedding, constructing a bipartite graph for maximum weight matching, or generating a difference-count feature table for spectral interrelation.

## When NOT to use

- Input spectra lack clear precursor mass or fragment ion peak assignments—missing or malformed m/z data will produce invalid deltas.
- Mass differences have already been pre-computed and stored in a standardized format; recomputing would duplicate effort and introduce inconsistency.
- Analysis goal does not require Laplacian embedding or graph-based matching; simpler cosine similarity or spectral entropy metrics may be more appropriate.

## Inputs

- tandem mass spectra in mzML or internal spectrum object format
- precursor m/z values (one per spectrum)
- fragment ion m/z lists (per spectrum)
- fragment ion intensity values (optional, for weighting)
- mass tolerance parameter (e.g., 0.1 Da or ppm threshold)

## Outputs

- pairwise mass difference matrix or sparse representation
- precursor-based neutral loss difference counts
- difference-count table (indexed by spectrum ID and mass difference)
- transition probability matrix (row-normalized difference counts)
- structured output file (CSV or HDF5 format)

## How to apply

Extract the precursor mass and all fragment m/z values from each input spectrum. For direct MZ difference counts, compute all pairwise differences between fragment ions within and across spectra; optionally apply a mass tolerance (e.g., 0.1 Da or a specified ppm window) to bin similar differences. For precursor-based neutral loss difference counts, subtract each fragment m/z from the precursor mass to obtain neutral losses, then compute pairwise differences between these neutral loss values. Aggregate both methods (or either alone) into a unified difference-count table indexed by spectrum identifier and mass difference bin. Use these counts as transition probabilities (after row normalization) in the Laplacian embedding or as edge weights in the bipartite matching graph.

## Related tools

- **SIMILE** (Python library that encapsulates mass delta computation, Laplacian embedding, and maximum weight matching for spectrum alignment with significance estimation) — https://github.com/biorack/simile
- **Python** (Programming language for implementing mass difference calculations, row normalization, and matrix/graph operations)

## Examples

```
import simile as sml; import numpy as np; mzs = [list of fragment m/z arrays]; pmzs = [list of precursor m/z]; S, spec_ids = sml.similarity_matrix(mzs, pmzs=pmzs, tolerance=0.1)
```

## Evaluation signals

- All pairwise differences are computed; verify by checking that the number of unique mass deltas equals the binomial coefficient of fragment count pairs plus neutral loss pairs.
- Transition matrix sums to 1.0 when row-normalized, confirming proper probability distribution.
- Difference-count table schema includes spectrum identifier, mass difference bin, and count; spot-check several entries against manual calculations.
- Laplacian embedding can be computed from the transition matrix without singularity errors, indicating valid graph structure.
- Neutral loss differences are strictly non-negative and bounded by precursor mass; verify no m/z reversals or physical impossibilities.

## Limitations

- Mass tolerance choice (Da or ppm) directly impacts binning resolution and reproducibility; must be documented and calibrated per instrument.
- Spectra with very few fragment ions (e.g., <3 peaks) yield sparse or degenerate transition matrices that may not support robust Laplacian embedding.
- Precursor mass ambiguity (e.g., multiply charged ions) can distort neutral loss calculations if not resolved before mass delta computation.
- Very large spectra (hundreds of fragments) generate O(n²) pairwise comparisons, increasing memory and computational cost.

## Evidence

- [other] Compute pairwise mass differences (m/z deltas) between all fragment ions across the two spectra: "Compute all pairwise mass differences (m/z deltas) between fragment ions of the two spectra."
- [readme] Precursor-based neutral loss difference counts method: "Precursor-based neutral loss difference counts can be used in addition to the original MZ difference counts"
- [readme] Laplacian embedding uses mass difference transition matrix: "constructing a transition matrix with row-normalized mass difference frequencies as transition probabilites"
- [other] Neutral loss calculation: "Calculate precursor-based neutral loss differences by subtracting each fragment m/z from the precursor mass"
- [other] Output format: "Export the combined difference-count table as a structured output file (CSV or HDF5 format)."
