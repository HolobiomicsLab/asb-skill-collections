---
name: cosine-similarity-computation
description: Use when when comparing two MS/MS spectra (query and reference) to quantify their spectral resemblance for compound identification or molecular networking, particularly when you need a simple, symmetric measure that is insensitive to precursor mass differences and does not require peak alignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - cosine_neutral_loss repository
  - github.com/bittremieux/cosine_neutral_loss
  - spectrum_utils
  techniques:
  - CE-MS
derived_from:
- doi: 10.1021/jasms.2c00153
  title: Neutral-loss similarity
- doi: 10.1016/1044-0305
  title: ''
evidence_spans:
- Code repository implements cosine similarity, modified cosine similarity, and neutral loss similarity measures
- github.com__bittremieux__cosine_neutral_loss
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neutral_loss_similarity_cq
    doi: 10.1021/jasms.2c00153
    title: Neutral-loss similarity
  dedup_kept_from: coll_neutral_loss_similarity_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.2c00153
  all_source_dois:
  - 10.1021/jasms.2c00153
  - 10.1016/1044-0305
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cosine-similarity-computation

## Summary

Compute cosine similarity between two MS/MS spectra by normalizing their fragment peak intensity vectors and calculating their dot product. This foundational similarity measure is used to discover structurally related molecules in mass spectral library searching.

## When to use

When comparing two MS/MS spectra (query and reference) to quantify their spectral resemblance for compound identification or molecular networking, particularly when you need a simple, symmetric measure that is insensitive to precursor mass differences and does not require peak alignment across m/z shifts.

## When NOT to use

- When spectra have different precursor masses and you want to align peaks allowing for mass offset — use modified cosine similarity instead.
- When you want to compare spectra using neutral loss peaks (fragments relative to precursor m/z) — use neutral loss similarity instead.
- When input spectra contain unfiltered noise or very weak peaks; consider preprocessing to remove low-intensity peaks first.

## Inputs

- Query MS/MS spectrum (m/z array and intensity array)
- Reference MS/MS spectrum (m/z array and intensity array)

## Outputs

- Cosine similarity score (float, range 0–1)

## How to apply

Extract the m/z and intensity values from both the query and reference MS/MS spectra. Create normalized intensity vectors for all fragment peaks in each spectrum. Compute the cosine similarity as the dot product of the two normalized intensity vectors, which ranges from 0 (orthogonal/completely dissimilar spectra) to 1 (identical spectra). The measure is symmetric and does not account for mass offsets between spectra; if such offsets matter, use modified cosine similarity instead. Return the cosine similarity score as a float between 0 and 1.

## Related tools

- **spectrum_utils** (MS/MS spectrum data structure and I/O, used to load and manipulate spectra for similarity computation) — github.com/bittremieux/cosine_neutral_loss
- **cosine_neutral_loss repository** (Reference implementation of cosine, modified cosine, and neutral loss similarity measures for spectrum comparison) — github.com/bittremieux/cosine_neutral_loss

## Examples

```
import spectrum_utils.spectrum as sus
spectrum1 = sus.MsmsSpectrum.from_usi('mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00000424840')
spectrum2 = sus.MsmsSpectrum.from_usi('mzspec:MSV000086109:BD5_dil2x_BD5_01_57213:scan:760')
plot.plot_mirror(spectrum1, spectrum2, 'cosine', 'cosine.png')
```

## Evaluation signals

- Output score is a float in the range [0, 1] with no NaN or infinite values.
- Identical spectra (same peaks and intensities) yield a cosine similarity of ~1.0.
- Completely disjoint spectra (no overlapping m/z peaks) yield a cosine similarity of 0.
- The measure is symmetric: cosine_similarity(spectrum_A, spectrum_B) == cosine_similarity(spectrum_B, spectrum_A).
- Normalized intensity vectors have magnitude 1 before dot product computation (unit vector check).

## Limitations

- Cosine similarity is insensitive to precursor mass differences; spectra with the same fragments but different parent ions will score high, which may or may not reflect true structural similarity.
- The measure treats all peak matches equally regardless of their m/z values; it does not penalize mass offset or peak alignment errors.
- Very low-intensity peaks contribute minimally to the similarity score after normalization, potentially obscuring minor structural differences.
- No built-in handling for isotope patterns, in-source fragmentation, or adduct variants.

## Evidence

- [readme] Similarity measures that are currently implemented are: - Cosine similarity: "Similarity measures that are currently implemented are: - Cosine similarity"
- [readme] Stein, S. E. & Scott, D. R. Optimization and testing of mass spectral library search algorithms for compound identification: "Stein, S. E. & Scott, D. R. Optimization and testing of mass spectral library search algorithms for compound identification"
- [intro] Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules: "Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules"
- [other] Compute cosine similarity on the aligned peak intensities. Return the modified cosine similarity score as a float between 0 and 1.: "Compute cosine similarity on the aligned peak intensities. Return the modified cosine similarity score as a float between 0 and 1."
