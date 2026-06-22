---
name: difference-count-table-integration
description: Use when when analyzing tandem MS/MS spectra with SIMILE V2 and you want to leverage both fragment ion mass differences and neutral loss patterns to improve spectral similarity scoring.
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

# Difference-Count Table Integration

## Summary

Combine multiple mass difference counting methods (MZ difference counts and precursor-based neutral loss difference counts) into a unified, indexed difference-count table for use in SIMILE V2 spectral alignment. This integration enables richer feature representation of fragmentation patterns by capturing both direct fragment-to-fragment mass relationships and neutral loss signatures.

## When to use

When analyzing tandem MS/MS spectra with SIMILE V2 and you want to leverage both fragment ion mass differences and neutral loss patterns to improve spectral similarity scoring. Use this skill when your input spectra include both fragment m/z values and precursor masses, and you aim to compute comprehensive mass difference features that capture multiple aspects of fragmentation chemistry.

## When NOT to use

- Input spectra lack precursor mass information; neutral loss difference counts require valid precursor m/z.
- Spectra have only a single or very few fragment ions per spectrum; difference-count methods require sufficient fragments to generate meaningful pair-wise differences.
- You need only fragment-centric matching without global similarity matrix construction; difference-count integration is primarily useful when feeding into SIMILE's similarity_matrix() or multiple_match() functions.

## Inputs

- Tandem mass spectra (MS/MS data) in mzML or internal spectrum objects with precursor mass and fragment m/z values
- Precursor mass values (one per spectrum)
- Fragment ion m/z values (multiple per spectrum)

## Outputs

- Unified difference-count table (CSV or HDF5 format) indexed by spectrum and difference mass
- Combined MZ difference counts and precursor-based neutral loss difference counts in structured format

## How to apply

Extract precursor mass and fragment ion m/z values from each MS/MS spectrum in mzML or compatible format. Compute MZ difference counts between all fragment ion pairs using SIMILE's original difference-counting method. In parallel, calculate precursor-based neutral loss differences by subtracting each fragment m/z from the precursor mass, then count neutral loss differences between all fragment pairs. Combine both MZ difference counts and neutral loss difference counts into a single unified difference-count table indexed by spectrum and difference mass. The rationale is that neutral loss differences capture structural information orthogonal to direct mass differences, enriching the transition matrix used in SIMILE's Laplacian embedding and leading to more sensitive fragment ion similarity scoring.

## Related tools

- **SIMILE** (Spectral similarity and alignment framework that consumes the unified difference-count table to compute fragment ion similarity, perform maximum weight matching, and generate significance scores via z-test) — https://github.com/biorack/simile
- **Python** (Programming language for implementing the difference-count extraction and table merging workflow)

## Examples

```
import simile as sml; mzs_combined = sml.difference_count_table(mzs, pmzs=pmzs, methods=['mz', 'neutral_loss'], tolerance=0.05); S, spec_ids = sml.similarity_matrix(mzs_combined, pmzs=pmzs, tolerance=tolerance)
```

## Evaluation signals

- The output table contains entries for all pairwise difference masses (both MZ and neutral loss types) without duplicates or omissions.
- Row-normalized mass difference frequencies in the resulting transition matrix sum to 1.0 per row, confirming proper probability normalization.
- Neutral loss differences (precursor – fragment m/z) fall within a chemically plausible range (typically 1–300 Da for small molecules); outliers indicate extraction errors.
- The unified table structure correctly indexes by spectrum ID and difference mass, allowing reproducible lookup in downstream SIMILE similarity_matrix() calls.
- Comparison of similarity matrices before and after integration should show increased fragment ion matching sensitivity when neutral loss counts are included, evidenced by higher z-test scores for known structural variants.

## Limitations

- Precursor-based neutral loss counting assumes accurate precursor mass assignment; deviations or adducts not accounted for will propagate incorrect neutral loss differences.
- Method is sensitive to fragment m/z measurement accuracy and calibration; mass measurement error tolerance (e.g., 5 ppm in SIMILE) must be set appropriately or the difference-count table will contain spurious small-mass differences.
- Neutral loss differences may be less informative for spectra with low fragmentation intensity or few detected fragments; the method's benefits diminish as pair-wise difference statistics become sparse.
- Integration assumes both counting methods (MZ and neutral loss) are equally valid; if a particular spectrum type or instrument produces unreliable neutral loss patterns, separate feature weighting or per-method filtering may be needed.

## Evidence

- [readme] Precursor-based neutral loss difference counts can be used in addition to MZ difference counts: "Precursor-based neutral loss difference counts can be used in addition to the original MZ difference counts"
- [other] Extract precursor mass and fragment ion m/z, compute both types of differences, and combine into indexed table: "Extract precursor mass and fragment ion m/z values from each spectrum. 3. Compute MZ difference counts between all fragment pairs using the original SIMILE difference-counting method. 4. Calculate"
- [readme] SIMILE V2 features much faster mass delta counting: "MUCH faster mass delta counting and significance testing"
- [readme] Fragment ions are similar if the difference in mass between them is common: "Fragment ions are similar if the difference in mass between them is common."
- [readme] Row-normalized mass difference frequencies as transition probabilities: "row-normalized mass difference frequencies as transition probabilites"
