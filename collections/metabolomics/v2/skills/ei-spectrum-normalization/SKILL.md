---
name: ei-spectrum-normalization
description: Use when you have raw electron ionization mass spectra (m/z and intensity pairs) that you intend to match against a library using the Identity (EI Normal) or Similarity (EI Simple) algorithms. Different ionization runs and instrument conditions produce spectra with varying absolute intensities;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mssearchr
  - R
derived_from:
- doi: 10.1021/jasms.5c00322
  title: mspepsearchr
evidence_spans:
- The primary goal of the `mssearchr` package is to enhance the capabilities of R users for conducting library searches against electron ionization mass spectral databases.
- The primary goal of the `mssearchr` package is to enhance the capabilities of R users
- enhance the capabilities of R users for conducting library searches
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspepsearchr_cq
    doi: 10.1021/jasms.5c00322
    title: mspepsearchr
  dedup_kept_from: coll_mspepsearchr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00322
  all_source_dois:
  - 10.1021/jasms.5c00322
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ei-spectrum-normalization

## Summary

Normalize electron ionization mass spectra by scaling peak intensities to a base peak reference before library matching. This preprocessing step enables fair similarity scoring across spectra with different absolute intensities by converting raw m/z and intensity pairs to a relative intensity scale.

## When to use

Apply this skill when you have raw electron ionization mass spectra (m/z and intensity pairs) that you intend to match against a library using the Identity (EI Normal) or Similarity (EI Simple) algorithms. Different ionization runs and instrument conditions produce spectra with varying absolute intensities; normalization ensures that similarity scoring reflects spectral pattern overlap rather than instrumental gain or sample amount differences.

## When NOT to use

- Input spectra are already in normalized or relative intensity form (e.g., base peak = 100 or 999).
- The library search algorithm does not require intensity normalization (e.g., mass-only matching or exact m/z matching without intensity).
- Working with non-EI mass spectrometry data (e.g., ESI, MALDI, or other ionization methods with different peak intensity semantics).

## Inputs

- Query electron ionization mass spectrum (m/z, intensity pairs)
- Spectral library in MSP file format (containing multiple EI spectra with m/z and intensity values)

## Outputs

- Normalized query spectrum (m/z, relative intensity pairs)
- Normalized spectral library entries (m/z, relative intensity pairs)
- Intensity normalization parameters (base peak values per spectrum)

## How to apply

Extract the base peak (maximum intensity value) from the query spectrum and each library spectrum separately. Divide all intensity values in each spectrum by its base peak intensity, scaling the result to a 0–999 or 0–100 integer range as specified by the Identity (EI Normal) algorithm. Preserve the m/z values unchanged. Apply this transformation consistently to both the query spectrum and all library entries before computing similarity scores. The rationale is that the Identity (EI Normal) algorithm specification requires normalized intensities to make cross-spectrum comparisons; omitting this step will produce invalid scores.

## Related tools

- **mssearchr** (Provides parsers for MSP files and implements the Identity (EI Normal) algorithm that consumes normalized spectra; handles spectrum I/O and similarity scoring downstream of normalization.) — https://github.com/AndreySamokhin/mssearchr
- **R** (Host language for executing normalization via mssearchr package functions and custom intensity-scaling scripts.)

## Evaluation signals

- Base peak intensity in normalized spectrum equals 100 or 999 (depending on algorithm specification) for every spectrum processed.
- All intensity values are ≤ base peak value after normalization (relative scale is monotonically bounded).
- m/z values remain unchanged after normalization; only intensities are scaled.
- Similarity scores computed on normalized spectra are higher for known matches and lower for unrelated spectra compared to unnormalized raw data.
- Normalized spectra from the same compound ionized under different conditions produce consistent high similarity scores.

## Limitations

- Normalization assumes that the base peak is a reliable reference; in very low signal-to-noise spectra, noise peaks may be selected as the base peak, leading to over-normalization of true signals.
- The algorithm specification (0–999 vs. 0–100 scale) must match the library's normalization convention; mixing conventions produces invalid scores.
- Loss of absolute quantitative intensity information after normalization; if absolute peak heights are diagnostically important, they must be preserved separately before normalization.

## Evidence

- [intro] Apply intensity normalization according to Identity (EI Normal) algorithm specification: "custom implementation of the Identity (EI Normal) algorithm as a tool for conducting library searches against electron ionization mass spectral databases"
- [other] Normalize peak intensities and match m/z values: "normalizing peak intensities and matching m/z values according to the algorithm specification"
- [other] Load query and library spectra then normalize before scoring: "Load the query EI mass spectrum (m/z and intensity pairs) from input. 2. Parse the spectral library from the MSP file using mssearchr's msp reader. 3. Apply the Identity (EI Normal) algorithm to"
