---
name: lcms-peak-detection-and-alignment
description: Use when you have one or more raw mzXML or mzML LCMS data files (from
  DDA, DIA, or fullscan acquisition) and need to extract quantitative metabolite features
  for multi-sample comparative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0591
  tools:
  - ISFrag
  - R
  - XCMS
  - CAMERA
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c01644
  title: ISFrag
evidence_spans:
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS
  metabolite feature table.
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS
  metabolite feature table
- To install ISFrag package R version 4.0.0 or above is required
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isfrag_cq
    doi: 10.1021/acs.analchem.1c01644
    title: ISFrag
  dedup_kept_from: coll_isfrag_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c01644
  all_source_dois:
  - 10.1021/acs.analchem.1c01644
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LCMS Peak Detection and Alignment

## Summary

Detect peaks across MS1 spectra from multiple LCMS samples and align them into a unified feature matrix indexed by m/z and retention time. This is the core preprocessing step in ISFrag that transforms raw mzXML/mzML data into a feature table suitable for downstream MS2 annotation and in-source fragment identification.

## When to use

You have one or more raw mzXML or mzML LCMS data files (from DDA, DIA, or fullscan acquisition) and need to extract quantitative metabolite features for multi-sample comparative analysis. Apply this skill before MS2 annotation or when you require a standardized feature table format compatible with ISFrag's in-source fragment workflow.

## When NOT to use

- Input is already a feature table in CSV format from MS-DIAL, MZmine2, or another tool—use custom.featuretable() instead to load the pre-extracted table.
- You only have a single mzXML file and do not require peak alignment across samples—single-file peak detection alone may be sufficient depending on your downstream goal.
- CAMERA adduct and isotope annotation is required—these features are only available when XCMS-based extraction is used; custom feature tables cannot use CAMERA.

## Inputs

- One or multiple mzXML or mzML files in a single directory
- Directory path containing LCMS raw data files

## Outputs

- Feature table (dataframe) with columns: m/z, retention time, rtmin, rtmax, and intensity/maxo
- MSnbase object (R object containing mass spectrometry data)
- CSV or tabular export compatible with ISFrag input format

## How to apply

Load raw mzXML/mzML files into XCMS via the XCMS.featuretable() function, specifying the directory containing all mzXML files and appropriate peakwidth parameters (typically 5–20 seconds for small-molecule metabolomics). XCMS performs centroiding and noise filtering on MS1 spectra, applies peak-picking to detect features across all samples, aligns peaks by m/z and retention time, and fills missing values for features detected in some samples but not others. The function outputs a feature table with columns for m/z, retention time (rt), retention time edges (rtmin, rtmax), and intensity or maximum intensity (maxo) for each feature. Verify that alignment is correct by inspecting feature counts across samples and that retention time values are in seconds as required by ISFrag.

## Related tools

- **XCMS** (Performs peak-picking, alignment, and filling on MS1 spectra to generate the feature table. Called via XCMS.featuretable() in ISFrag.) — https://rdrr.io/bioc/xcms/man/
- **ISFrag** (R package that wraps XCMS feature extraction and provides downstream MS2 annotation and in-source fragment identification. Requires XCMS feature table as Part 2 of its workflow.) — https://github.com/HuanLab/ISFrag.git
- **R** (Language and runtime environment required to execute XCMS and ISFrag; version 4.0.0 or above.)
- **CAMERA** (Optional post-processing for adduct and isotope annotation; only compatible with XCMS-extracted features, not custom feature tables.)

## Examples

```
xcmsFT <- XCMS.featuretable(MS1directory = "X:/Users/Sam_Shen/ISFtest20210127/RP(-)/RP(-)1/fullscan", type = "single", peakwidth = c(5,20)); head(xcmsFT)
```

## Evaluation signals

- Feature table contains no missing m/z, retention time, or intensity values; all rows correspond to detected peaks.
- Retention time values (rt, rtmin, rtmax) are in seconds and consistent within expected chromatographic range (typically 0–2500 seconds).
- m/z values span the expected mass range for the target analytes and chemical ionization mode (e.g., 50–1500 m/z for small-molecule metabolomics).
- For multi-sample analyses, the number of features per sample is comparable (no sample has drastically fewer or more features than others, indicating successful alignment).
- Peak intensity or maxo values are positive and vary across features and samples, confirming quantitative signal recovery.

## Limitations

- Peak-picking performance depends on peakwidth parameter selection; incorrect peakwidth can lead to missed features or over-segmentation of wide peaks.
- Retention time alignment may fail or produce duplicates if samples have very different chromatographic offsets or if the XCMS algorithm parameters are not tuned to the data.
- Missing value fill-in is performed only within XCMS; features present in only one sample may not be reliably filled across all samples if the feature signal is weak or near the noise threshold.
- XCMS feature extraction assumes centroided spectra; non-centroided (profile-mode) mzXML files may produce suboptimal results.
- CAMERA adduct and isotope annotation is lost if a custom feature table from another tool is used; ISFrag only provides adduct/isotope annotation for XCMS-extracted features.

## Evidence

- [other] Detect peaks across all samples using XCMS peak-picking algorithm. 4. Align peaks across samples to create a unified feature matrix with retention time and m/z dimensions.: "Detect peaks across all samples using XCMS peak-picking algorithm. 4. Align peaks across samples to create a unified feature matrix with retention time and m/z dimensions."
- [other] Perform centroiding and noise filtering on MS1 spectra. 3. Detect peaks across all samples using XCMS peak-picking algorithm.: "Perform centroiding and noise filtering on MS1 spectra. 3. Detect peaks across all samples using XCMS peak-picking algorithm."
- [other] Fill missing values for peaks detected in some samples but not others. 6. Integrate peak intensities to generate a feature table with rows as metabolite features and columns as samples: "Fill missing values for peaks detected in some samples but not others. 6. Integrate peak intensities to generate a feature table with rows as metabolite features and columns as samples"
- [readme] One or multiple mzXML files from DDA, DIA, or fullscan analyses can be analyzed at once using XCMS to extract MS1 features. All mzXML file(s) need to be placed in a separate folder containing no other irrelevant mzXML files. Note: for multi-sample analyses, peak alignment and filling will be performed by XCMS.: "One or multiple mzXML files from DDA, DIA, or fullscan analyses can be analyzed at once using XCMS to extract MS1 features. All mzXML file(s) need to be placed in a separate folder containing no"
- [readme] To use a custom feature table (eg. from MS-DIAL, MZmine2, etc) for `ISFrag` analysis. In order for `ISFrag` to succesfully read the provided csv file, it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an additional column containing the intensities: "To use a custom feature table (eg. from MS-DIAL, MZmine2, etc) for `ISFrag` analysis. In order for `ISFrag` to succesfully read the provided csv file, it must contain only columns in the following"
