---
name: fragment-ion-difference-counting
description: Use when when preparing tandem MS/MS data for spectral alignment and
  similarity comparison, particularly when you have loaded raw fragmentation spectra
  and need to extract and quantify mass difference patterns that capture the fragmentation
  process.
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
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
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

# fragment-ion-difference-counting

## Summary

Compute mass difference feature counts from tandem mass spectra using both m/z differences between fragment pairs and precursor-based neutral loss differences. This skill generates a unified difference-count table that serves as input to SIMILE's spectral similarity and alignment algorithm.

## When to use

When preparing tandem MS/MS data for spectral alignment and similarity comparison, particularly when you have loaded raw fragmentation spectra and need to extract and quantify mass difference patterns that capture the fragmentation process. Use this skill if you want to leverage both fragment-to-fragment m/z relationships AND neutral loss relationships (fragment m/z relative to precursor mass) to enrich the feature representation.

## When NOT to use

- Input spectra lack reliably identified precursor masses or contain fewer than ~3–5 fragment ions per spectrum (insufficient pairwise differences for robust counting).
- You have already computed a pre-existing feature table or embedding; difference counting is an upstream feature engineering step, not applicable to downstream analyses.
- Spectra are from data types where neutral loss is not chemically meaningful (e.g., native MS or ion mobility, where precursor structure is unknown).

## Inputs

- tandem mass spectra in mzML format or internal spectrum objects
- spectrum collection with extracted precursor m/z and fragment m/z values
- mass tolerance threshold (e.g., 1 Da or instrument precision)

## Outputs

- unified difference-count table indexed by spectrum ID and difference mass
- difference-count table in CSV or HDF5 format
- frequency histogram of MZ differences per spectrum
- frequency histogram of neutral loss differences per spectrum

## How to apply

Extract precursor mass and all fragment ion m/z values from each loaded spectrum (in mzML or internal spectrum object format). Compute pairwise m/z differences between all fragment ions and count their frequency to generate MZ difference counts. Independently, calculate precursor-based neutral loss differences by subtracting each fragment m/z from the precursor mass, then count pairwise differences between these neutral loss values. Combine both count tables into a single unified difference-count table indexed by spectrum ID and difference mass (rounded to a consistent tolerance, typically 1 Da or mass spectrometry precision). The rationale is that fragment ion similarity arises from two properties: common mass differences between fragments (property a) and structural relationships between ancestors and descendants in the fragmentation tree (property b); counting both m/z and neutral loss differences captures these complementary relationships for downstream graph-based alignment.

## Related tools

- **SIMILE** (accepts the unified difference-count table as input to build a transition matrix for fragment ion similarity scoring and spectral alignment) — https://github.com/biorack/simile
- **Python** (primary implementation language for difference-counting logic, array operations, and export to CSV/HDF5)

## Examples

```
import simile as sml; mzs, pmzs = load_spectra('input.mzml'); S, spec_ids = sml.similarity_matrix(mzs, pmzs=pmzs, tolerance=1.0)
```

## Evaluation signals

- Difference-count table is non-empty and indexed consistently by spectrum ID and mass difference bins (no gaps or NaN values in the index).
- Total count across all differences per spectrum is equal to the number of pairwise fragment combinations (n*(n-1)/2 for n fragments) for MZ differences, and identical for neutral loss differences.
- All mass difference values fall within the expected range (0 to precursor m/z for MZ differences; 0 to precursor m/z for neutral losses).
- Precursor-based neutral loss differences are strictly positive and do not exceed the precursor m/z value.
- Export file (CSV or HDF5) is readable and contains no truncated or corrupted entries; row and column counts match the input spectrum set size and the unique difference mass bins.

## Limitations

- Counting is sensitive to mass tolerance and binning strategy; overly coarse tolerance may conflate distinct neutral losses, while overly fine tolerance may fragment real mass differences into separate bins.
- Spectra with very few fragments (n < 3) yield very few pairwise differences and weak signal; such spectra may not contribute meaningfully to downstream similarity scoring.
- Neutral loss differences assume the precursor mass is accurately known; errors in precursor assignment will propagate directly into neutral loss counts.
- The method does not account for isotope peaks or adducts; these must be pre-processed or filtered from the fragment list.
- Very high-abundance noise or unresolved multiplets can artificially inflate difference counts if not handled during spectrum preprocessing.

## Evidence

- [other] Extract precursor mass and fragment ion m/z values from each spectrum. Compute MZ difference counts between all fragment pairs using the original SIMILE difference-counting method. Calculate precursor-based neutral loss differences by subtracting each fragment m/z from the precursor mass, then count neutral loss differences between all fragment pairs.: "Extract precursor mass and fragment ion m/z values from each spectrum. Compute MZ difference counts between all fragment pairs using the original SIMILE difference-counting method. Calculate"
- [readme] Precursor-based neutral loss difference counts can be used in addition to the original MZ difference counts: "Precursor-based neutral loss difference counts can be used in addition to the original MZ difference counts"
- [readme] Fragment ions are similar if the difference in mass between them is common. Fragment ions are similar if their ancestor and descendent fragment ions are similar.: "Fragment ions are similar if the difference in mass between them is common. Fragment ions are similar if their ancestor and descendent fragment ions are similar."
- [other] Combine both MZ difference counts and neutral loss difference counts into a single unified difference-count table indexed by spectrum and difference mass. Export the combined difference-count table as a structured output file (CSV or HDF5 format).: "Combine both MZ difference counts and neutral loss difference counts into a single unified difference-count table indexed by spectrum and difference mass. Export the combined difference-count table"
