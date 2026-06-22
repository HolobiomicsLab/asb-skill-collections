---
name: lcms-data-format-handling
description: Use when you have raw LC-MS data from a vendor instrument or in netCDF format and need to ingest it into SLAW or similar untargeted LC-MS workflows. Use this skill when raw data must be converted to mzML, validated for centroiding and polarity uniformity, and prepared for peak-picking dispatch.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Centwave
  - FeatureFinderMetabo
  - ADAP
  - ProteoWizard
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lcms-data-format-handling

## Summary

Prepare and validate raw LC-MS data in vendor or open formats (mzML, netCDF) for automated peak-picking and downstream processing. This skill ensures data is centroided, of uniform polarity, and properly formatted before routing to algorithm-specific wrappers.

## When to use

You have raw LC-MS data from a vendor instrument or in netCDF format and need to ingest it into SLAW or similar untargeted LC-MS workflows. Use this skill when raw data must be converted to mzML, validated for centroiding and polarity uniformity, and prepared for peak-picking dispatch.

## When NOT to use

- Input data is already in a standardized, validated feature table or peak matrix format (e.g., CSV with m/z, retention time, intensity columns).
- Data contains a mixture of positive and negative polarity scans in the same file; separate files by polarity first.
- Profile-mode (non-centroided) data cannot be centroided with available vendor tools or ProteoWizard filters.

## Inputs

- Raw LC-MS data files (mzML or netCDF format)
- Vendor-supplied MS data (profile or centroided)
- Data polarity metadata (positive or negative)

## Outputs

- Centroided mzML files with uniform polarity
- Validated, preprocessed LC-MS data ready for peak-picking
- Polarity classification log (positive/negative detection)

## How to apply

Accept raw LC-MS data in mzML or netCDF format and validate that all files are centroided (not profile mode) and of a single polarity (positive or negative only). If profile data is present, use vendor tools (e.g., ProteoWizard with peakPicking filter) to extract centroided data; apply the filter `peakPicking vendor msLevel=1-2` to retain only vendor-provided centroids and discard low-confidence peaks. Verify that MS1 and optional DDA-MS2 scans are present and that DIA-MS data is not included (not supported). Standardize all input files to mzML format with consistent naming. Log or extract the detected polarity from at least one representative file to confirm uniformity across the batch. Output the validated, centroided mzML files ready for the peak-picking routing stage.

## Related tools

- **ProteoWizard** (Convert vendor raw data to centroided mzML; apply peakPicking vendor filter to extract MS1-2 centroids)
- **SLAW** (Downstream workflow that ingests validated mzML files and routes them to Centwave, FeatureFinderMetabo, or ADAP peak pickers) — https://github.com/zamboni-lab/SLAW

## Examples

```
# Using ProteoWizard to convert and centroid raw data to mzML
msConvert vendor_raw_data.raw --mzML --filter "peakPicking vendor msLevel=1-2" --outdir ./mzml_output/
# Validate and stage centroided files in SLAW input folder for peak-picking dispatch
```

## Evaluation signals

- All output mzML files are readable by peak-picking tools (Centwave, FeatureFinderMetabo, ADAP) without errors.
- Data contains only centroided peaks; no profile-mode scans remain.
- All files in a batch share a single polarity (positive or negative); no mixed-polarity files are present.
- MS1 and (optional) MS2 scans are retained; DIA-MS scans are absent or flagged separately.
- File headers and metadata (mzML schema, polarity flags) validate against SLAW input schema.

## Limitations

- DIA-MS data is not supported by SLAW; files with DIA-only MS2 must be excluded or flagged separately.
- Profile-mode data cannot be converted to centroided format after acquisition; vendor tools must be applied at conversion time.
- Mixed-polarity files must be split into separate positive and negative mzML files before processing; no within-file demultiplexing is performed.
- Low-abundance centroids removed during preprocessing may reduce feature detection sensitivity; archival of unfiltered raw data is recommended.

## Evidence

- [readme] Raw MS data in mzML format. Files can include MS1 and DDA-MS2 scans. DIA-MS is not supported. **All data must be centroided and of unique polarity**.: "Raw MS data in mzML format. Files can include MS1 and DDA-MS2 scans. DIA-MS is not supported. **All data must be centroided and of unique polarity**."
- [readme] Centroided mzML can be obtained with ProteoWizard. Discard all profile data and always prioritize the centroid data provided by vendor's software, e.g. with the filter `peakPicking vendor msLevel=1-2`.: "Centroided mzML can be obtained with ProteoWizard. Discard all profile data and always prioritize the centroid data provided by vendor's software, e.g. with the filter `peakPicking vendor"
- [other] Accept a configuration specification naming the target peak-picking algorithm (Centwave, FeatureFinderMetabo, or ADAP) and raw LC-MS data (mzML or netCDF format).: "Accept a configuration specification naming the target peak-picking algorithm (Centwave, FeatureFinderMetabo, or ADAP) and raw LC-MS data (mzML or netCDF format)."
- [readme] Guessing polarity from file:DDA1.mzML ... Polarity detected: positive: "Guessing polarity from file:DDA1.mzML ... Polarity detected: positive"
