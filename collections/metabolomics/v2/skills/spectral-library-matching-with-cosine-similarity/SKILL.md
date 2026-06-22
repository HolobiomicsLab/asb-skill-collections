---
name: spectral-library-matching-with-cosine-similarity
description: Use when you have a query spectrum and a reduced candidate set of library spectra (via approximate nearest neighbor indexing), and need to search for exact unmodified peptide matches with high confidence before proceeding to variable-mass-shift modification searches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_gpu_feature_hashing_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_gpu_feature_hashing_cq
schema_version: 0.2.0
---

# Spectral Library Matching with Cosine Similarity

## Summary

Cosine similarity scoring is used within a cascade search strategy to confidently match query mass spectra to unmodified peptides in a spectral library after approximate nearest neighbor filtering. This scoring method forms the first-pass identification layer before attempting open modification searches on spectra without confident matches.

## When to use

Apply this skill when you have a query spectrum and a reduced candidate set of library spectra (via approximate nearest neighbor indexing), and need to search for exact unmodified peptide matches with high confidence before proceeding to variable-mass-shift modification searches. Use this as the first stage of a cascade search to maximize unmodified identifications while controlling false discovery rate.

## When NOT to use

- Input is already a curated list of peptide identifications with validated FDR — re-scoring is redundant.
- Query spectra are from a different instrument class or mass range than the spectral library, causing systematic score distribution shifts.
- Modification-rich proteomes where the majority of spectra have post-translational modifications that violate the 'unmodified match' assumption in the first cascade pass.

## Inputs

- Query mass spectrum (m/z and intensity pairs)
- Approximate nearest neighbor filtered candidate library spectra (m/z and intensity pairs)
- Library spectrum annotations (peptide sequences)

## Outputs

- Ranked list of library matches with cosine similarity scores
- Assigned spectrum-level or peptide-level FDR values
- Binary classification: spectra with confident unmodified matches vs. spectra requiring modification search

## How to apply

After retrieving a limited candidate set via approximate nearest neighbor search, apply cosine similarity scoring to compare each query spectrum against candidate library spectra. Rank candidates by cosine similarity score and apply spectrum-level or peptide-level false discovery rate filtering to assign confidence thresholds. Spectra with confident unmodified matches are identified and removed from downstream processing; only spectra without confident matches proceed to open modification search using the shifted dot product score. This two-stage approach maximizes sensitivity for unmodified identifications while maintaining strict FDR control across the full pipeline.

## Related tools

- **ANN-SoLo** (Spectral library search engine implementing cascade search with cosine similarity scoring for unmodified peptide identification, followed by shifted dot product scoring for open modification search) — https://github.com/bittremieux/ANN-SoLo

## Evaluation signals

- Cosine similarity scores follow a bimodal distribution with clear separation between true matches and false matches, enabling FDR filtering at a meaningful threshold.
- Spectrum-level or peptide-level FDR values assigned to all identifications are ≤ the specified control threshold (e.g., ≤ 1% or ≤ 5%).
- Spectra identified via cosine similarity in the cascade pass show minimal overlap with spectra subsequently identified via shifted dot product scoring in the modification search pass, confirming non-redundant cascade stages.
- Total number of identified spectra (unmodified + modified) exceeds what would be achieved by either method alone, validating the cascade strategy's sensitivity gain.
- When the same query spectrum is searched against alternative libraries with different composition, rank order of top candidates by cosine similarity remains consistent for true matches.

## Limitations

- Cosine similarity scoring assumes query and library spectra are comparable in instrument resolution, ionization method, and dynamic range; cross-instrument searches may require score recalibration.
- The method is designed for spectral library matching and does not perform de novo sequencing; it requires a curated library and does not identify novel peptides.
- Python 3.6 to 3.9 are required; Python 3.10 and newer are not currently supported by the ANN-SoLo implementation.
- FDR control is performed post-hoc via statistical filtering; the confidence threshold depends on library quality and may vary across datasets.

## Evidence

- [other] first search candidates for exact unmodified peptide matches using cosine similarity scoring: "first search candidates for exact unmodified peptide matches using cosine similarity scoring"
- [readme] cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [other] Rank all identified matches (unmodified and modified) by score and apply false discovery rate control via spectrum-level or peptide-level FDR filtering: "Rank all identified matches (unmodified and modified) by score and apply false discovery rate control via spectrum-level or peptide-level FDR filtering"
- [other] For spectra without confident unmodified matches, perform open modification search on the same candidates, allowing variable mass shifts: "For spectra without confident unmodified matches, perform open modification search on the same candidates, allowing variable mass shifts"
