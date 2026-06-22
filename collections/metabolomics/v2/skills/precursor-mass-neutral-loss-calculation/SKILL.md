---
name: precursor-mass-neutral-loss-calculation
description: Use when when analyzing tandem mass spectra (MS/MS data) and you want to incorporate neutral loss patterns—characteristic mass losses from molecular precursors—into your spectral similarity or feature representation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# precursor-mass-neutral-loss-calculation

## Summary

Calculate neutral loss mass differences by subtracting each fragment ion m/z from the precursor mass, then aggregate these differences across all fragment pairs to generate a neutral loss difference count table. This enriches spectral feature representation beyond MZ difference counts alone, enabling improved fragmentation pattern recognition in tandem mass spectrometry.

## When to use

When analyzing tandem mass spectra (MS/MS data) and you want to incorporate neutral loss patterns—characteristic mass losses from molecular precursors—into your spectral similarity or feature representation. Use this skill in addition to MZ difference counts when you need to capture both inter-fragment relationships and the relationship between fragments and their common precursor origin.

## When NOT to use

- Input spectra lack reliable precursor mass information or precursor mass is unknown or poorly characterized.
- Analysis goal is limited to inter-fragment ion relationships only; neutral loss patterns are not relevant to your research question.
- Spectra are already processed into aggregated feature tables; you need raw m/z and precursor values to compute neutral losses.

## Inputs

- tandem mass spectra (MS/MS data in mzML or compatible spectrum object format)
- precursor mass values (m/z) for each spectrum
- fragment ion m/z values for each spectrum

## Outputs

- unified difference-count table indexed by spectrum and difference mass (CSV or HDF5 format)
- precursor-based neutral loss difference counts (frequency table)
- combined MZ and neutral loss difference-count matrix

## How to apply

Extract the precursor mass (m/z) and all fragment ion m/z values from each tandem mass spectrum. For each fragment, compute the neutral loss by subtracting its m/z from the precursor mass. Then count the frequency of neutral loss differences between all fragment pairs—just as you would count MZ differences—by computing mass differences between pairs of neutral loss values. Combine the resulting neutral loss difference counts with the original MZ difference counts into a unified difference-count table indexed by spectrum and difference mass. This dual-count approach allows downstream matching algorithms (like SIMILE's maximum weight matching) to leverage both fragmentation directions: mass gain (fragment-to-fragment) and mass loss (fragment-to-precursor relationships).

## Related tools

- **SIMILE** (Consumes precursor-based neutral loss difference counts alongside MZ difference counts to compute fragment ion similarity and spectral alignment via maximum weight matching) — https://github.com/biorack/simile
- **Python** (Implementation language for reading spectrum objects, extracting m/z and precursor values, and computing neutral loss difference counts)

## Examples

```
```python
import simile as sml

# Extract precursor masses, fragment m/z values from spectra
precursor_masses = [500.1234, 600.5678]  # m/z values
fragment_mzs = [[150.5, 200.3, 250.1], [175.2, 225.8, 280.4]]  # per spectrum

# Compute neutral losses and difference counts
neutral_losses = [[pm - fmz for fmz in fms] for pm, fms in zip(precursor_masses, fragment_mzs)]

# Generate similarity matrix using combined MZ and neutral loss counts
S, spec_ids = sml.similarity_matrix(fragment_mzs, pmzs=precursor_masses, tolerance=0.1)
```
```

## Evaluation signals

- Precursor-based neutral loss differences are computed correctly: (precursor_mz - fragment_mz) for each fragment, and difference counts between all fragment pairs are non-negative integers.
- Unified difference-count table contains entries for both MZ and neutral loss difference masses with no missing or NaN values for valid spectra.
- Neutral loss difference counts capture expected fragmentation patterns (e.g., common neutral losses like 18 Da for water or 44 Da for CO₂).
- Combined table can be successfully ingested by downstream SIMILE functions (similarity_matrix, multiple_match) without type or dimension errors.
- Output file format (CSV or HDF5) is consistent with input specification and downstream tool requirements.

## Limitations

- Relies on accurate and well-calibrated precursor mass values; errors in precursor mass directly propagate to all neutral loss calculations.
- May produce spurious neutral losses if fragments are mislabeled or spectra contain contaminants or in-source fragmentations.
- Neutral loss patterns are most informative for precursor masses in the lower to mid molecular weight range; very large or very small precursors may have limited neutral loss diversity.
- Does not account for multiply charged precursors without prior charge state deconvolution.

## Evidence

- [other] Calculate precursor-based neutral loss differences by subtracting each fragment m/z from the precursor mass, then count neutral loss differences between all fragment pairs.: "Calculate precursor-based neutral loss differences by subtracting each fragment m/z from the precursor mass, then count neutral loss differences between all fragment pairs."
- [readme] Precursor-based neutral loss difference counts can be used in addition to the original MZ difference counts: "Precursor-based neutral loss difference counts can be used in addition to the original MZ difference counts"
- [other] Combine both MZ difference counts and neutral loss difference counts into a single unified difference-count table indexed by spectrum and difference mass.: "Combine both MZ difference counts and neutral loss difference counts into a single unified difference-count table indexed by spectrum and difference mass."
- [readme] Fragment ions are similar if the difference in mass between them is common.: "Fragment ions are similar if the difference in mass between them is common."
