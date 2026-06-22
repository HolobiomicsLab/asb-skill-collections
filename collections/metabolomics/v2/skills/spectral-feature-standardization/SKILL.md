---
name: spectral-feature-standardization
description: Use when after peak-picking stage completes on centroided mzML or netCDF raw LC-MS data via any of the three wrapped algorithms (Centwave, FeatureFinderMetabo, ADAP), when you need to pass the detected features to downstream SLAW stages (alignment, isotope/adduct grouping, gap-filling, MS2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Centwave
  - FeatureFinderMetabo
  - ADAP
  - SLAW
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans:
- 'Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw_cq
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02687
  all_source_dois:
  - 10.1021/acs.analchem.1c02687
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Feature Standardization

## Summary

Convert peak-picking output from heterogeneous algorithms (Centwave, FeatureFinderMetabo, ADAP) into a unified internal feature matrix representation with consistent m/z, retention time, and intensity columns. This standardization enables seamless downstream integration of algorithm-specific results into common alignment, grouping, and gap-filling workflows.

## When to use

After peak-picking stage completes on centroided mzML or netCDF raw LC-MS data via any of the three wrapped algorithms (Centwave, FeatureFinderMetabo, ADAP), when you need to pass the detected features to downstream SLAW stages (alignment, isotope/adduct grouping, gap-filling, MS2 extraction) that expect a unified schema regardless of which peak picker was invoked.

## When NOT to use

- Input is already a unified feature table from a prior standardization step — re-standardizing introduces redundancy and potential schema conflicts.
- Profile (non-centroided) mzML data — SLAW requires centroided input; standardization assumes peaks are already resolved.
- DIA-MS (data-independent acquisition) experiments — SLAW and its wrapped algorithms target DDA only; MS2 spectra from DIA will be skipped.

## Inputs

- Peak table from Centwave (algorithm-native format)
- Peak table from FeatureFinderMetabo (algorithm-native format)
- Peak table from ADAP (algorithm-native format)
- Algorithm metadata (algorithm name, version, parameter set used)

## Outputs

- Standardized feature matrix (m/z, retention time, intensity columns)
- Algorithm provenance metadata (algorithm name, execution context)
- Feature identifiers linked to algorithm-specific peak IDs

## How to apply

Receive the algorithm-specific peak table output from whichever peak-picking algorithm was routed based on the configuration key (Centwave, FeatureFinderMetabo, or ADAP). Extract the essential feature attributes: m/z (mass-to-charge ratio), retention time (RT), and intensity values. Map algorithm-native column names and units to the SLAW canonical schema (e.g., resolving differences in intensity normalization or RT scale). Assemble these into a standardized feature matrix where rows are features and columns are [m/z, RT, intensity, sample_id, algorithm_source]. This standardized format decouples downstream stages from algorithm-specific quirks and allows the same alignment, grouping, and gap-filling logic to operate identically on Centwave, FeatureFinderMetabo, or ADAP results.

## Related tools

- **Centwave** (Peak-picking algorithm whose output is standardized)
- **FeatureFinderMetabo** (Peak-picking algorithm whose output is standardized)
- **ADAP** (Peak-picking algorithm whose output is standardized)
- **SLAW** (Wrapper framework that invokes peak-picking, receives native output, and coordinates standardization before downstream stages) — https://github.com/zamboni-lab/SLAW

## Evaluation signals

- All features from the algorithm-native peak table are present in the standardized matrix with no loss or duplication.
- Every row in the standardized matrix has valid numeric values for m/z (positive), retention time (non-negative), and intensity (non-negative or zero).
- Column schema matches the SLAW canonical schema (m/z, RT, intensity, sample_id, algorithm_source) regardless of input algorithm.
- Downstream alignment step can consume the standardized matrix and produce consistent RT correction parameters across samples without requiring algorithm-specific post-processing.
- Algorithm metadata is preserved and retrievable, allowing users to trace which peak picker generated each feature.

## Limitations

- Standardization assumes all three algorithms (Centwave, FeatureFinderMetabo, ADAP) produce functionally equivalent peak definitions (m/z, RT, intensity); systematic differences in peak boundary detection or intensity normalization between algorithms are not harmonized beyond schema unification.
- mzML and netCDF format support is fixed; other raw MS formats (e.g., vendor-native .raw or .d) must first be converted to mzML/netCDF before reaching peak-picking and standardization stages.
- DDA-only scope: standardization is designed for DDA (data-dependent acquisition) experiments; DIA-MS2 spectra will be skipped and not integrated into the feature matrix.

## Evidence

- [other] Standardize the output peak table to a common internal format (e.g., feature matrix with m/z, retention time, intensity columns).: "Standardize the output peak table to a common internal format (e.g., feature matrix with m/z, retention time, intensity columns)."
- [other] SLAW wraps three independent peak picking algorithms—Centwave, FeatureFinderMetabo, and ADAP—enabling configurable selection among them for the peak-picking stage of untargeted LC-MS processing.: "SLAW wraps three independent peak picking algorithms—Centwave, FeatureFinderMetabo, and ADAP—enabling configurable selection among them"
- [readme] Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP: "Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP"
- [other] Return the standardized peak table and algorithm metadata to the caller for downstream SLAW stages (alignment, grouping, gap-filling).: "Return the standardized peak table and algorithm metadata to the caller for downstream SLAW stages (alignment, grouping, gap-filling)."
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained"
