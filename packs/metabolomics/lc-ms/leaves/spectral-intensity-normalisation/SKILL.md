---
name: spectral-intensity-normalisation
description: Use when processing raw MS/MS spectra (in MGF, mzML, mzXML, JSON, or
  MSP format) prior to MS2Query library matching or MS2Deepscore embedding calculation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2Query
  - MZmine
  - matchms
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-intensity-normalisation

## Summary

Standardization of peak intensities across raw MS/MS spectra to a uniform scale before library matching. This preprocessing step ensures that spectral similarity scoring and analogue detection are not biased by differences in absolute intensity values across query spectra.

## When to use

Apply this skill when processing raw MS/MS spectra (in MGF, mzML, mzXML, JSON, or MSP format) prior to MS2Query library matching or MS2Deepscore embedding calculation. Normalization is essential when query spectra originate from different instruments, acquisition conditions, or have varying dynamic ranges that could otherwise skew cosine similarity and random forest re-ranking scores.

## When NOT to use

- Input spectra are already normalized or pre-processed by an upstream tool (e.g., GNPS or MZmine output already includes normalization).
- Relative intensity ranking rather than absolute scale is the only concern; in that case, rank-based normalization may be more appropriate than intensity scaling.
- Peak picking or noise filtering have not yet been performed; normalization should follow clustering and feature selection, not precede it.

## Inputs

- Raw MS/MS spectra (MGF, mzML, mzXML, JSON, or MSP format)
- Peak list with m/z and intensity values
- Metadata including precursor m/z and ionization mode

## Outputs

- Normalized MS/MS spectra with standardized intensity scale
- Preprocessed spectrum objects compatible with MS2Deepscore and MS2Query matching

## How to apply

After peak picking and feature selection (e.g., via MZmine clustering), load raw query spectra and apply intensity normalization to standardize spectral peak heights to a common scale. The normalization should be applied sequentially within a preprocessing pipeline before spectral similarity scoring. MS2Query does not perform peak picking internally, so normalization must be part of an upstream or integrated preprocessing step. Verify that normalized spectra retain the relative intensity relationships between peaks while bringing absolute intensities into a comparable range suitable for the MS2Deepscore embeddings and random forest model that re-ranks library matches.

## Related tools

- **MS2Query** (Performs spectral-based library matching on preprocessed (normalized) query spectra using MS2Deepscore embeddings and random forest re-ranking) — https://github.com/iomega/ms2query
- **MZmine** (Performs upstream peak picking, clustering, and feature selection to reduce redundant spectra before normalization and MS2Query processing)
- **matchms** (Python library for spectrum object representation and manipulation, supports normalization operations on MS/MS spectra)

## Evaluation signals

- Normalized spectra have maximum intensity peaks within expected range (e.g., 0–1 or 0–100) across all query spectra.
- Relative peak height ratios within individual spectra are preserved after normalization (compare rank order before and after).
- MS2Query model prediction scores and library match rankings remain consistent or improve when normalized spectra are compared to non-normalized query spectra (validated on dummy or benchmark datasets).
- No spectra are lost or truncated during normalization; output spectrum count equals input count.
- Normalized spectra pass schema validation and format checks required by MS2Query and MS2Deepscore (e.g., all peaks have m/z and intensity values, no NaN or inf values).

## Limitations

- MS2Query documentation does not explicitly detail the normalization function signature or algorithm used internally; practitioners must implement or choose normalization logic independently based on domain knowledge.
- Normalization effectiveness depends on upstream peak picking quality; poor peak detection or excessive noise cannot be fully corrected by intensity scaling alone.
- The optimal normalization method may vary by ionization mode (positive vs. negative) and instrument type, requiring validation on reference spectra for each experimental context.
- Normalized spectra are no longer directly comparable to raw intensity measurements; archival of raw spectra is necessary for reproducibility and manual validation.

## Evidence

- [readme] MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or feature selection.: "MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or"
- [other] 1. Define spectrum pre-processing function signatures for normalisation and filtering operations on raw query spectral data. 2. Implement normalisation logic to standardize spectral intensities across raw query spectra.: "Define spectrum pre-processing function signatures for normalisation and filtering operations on raw query spectral data. Implement normalisation logic to standardize spectral intensities across raw"
- [other] Validate cleaned spectra meet expected format and quality criteria before library matching.: "Validate cleaned spectra meet expected format and quality criteria before library matching."
- [readme] The top 2000 spectra with the highest MS2Deepscore are selected. MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features.: "The top 2000 spectra with the highest MS2Deepscore are selected. MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features."
- [readme] As input for MS2Query you can use the MGF file of the FBMN output of MZMine: "As input for MS2Query you can use the MGF file of the FBMN output of MZMine"
