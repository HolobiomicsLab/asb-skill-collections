---
name: mass-spectrometry-data-preprocessing
description: Use when you have raw LCMS data in mzML or mzXML format from DDA, DIA,
  or fullscan analyses and need to extract metabolite features with unified m/z, retention
  time, and intensity values across multiple samples before performing MS2 annotation
  or in-source fragment analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0769
  tools:
  - ISFrag
  - R
  - XCMS
  - RStudio
  - MEISTER
  - msFeaST
  - jupyter-notebook
  - pandas
  - openNAU
  - MetaQC
  - MARC
  - PS2MS
  - PS²MS
  - NEIMS
  - DeepEI
  - MsBackendMgf
  - MsFeatures
  - MsDataHub
  - MassSpecWavelet
  - xcms
  - Spectra
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c01644
  title: ISFrag
- doi: 10.1038/s41592-024-02171-3
  title: ''
- doi: 10.1093/bioinformatics/btae584
  title: ''
- doi: 10.21147/j.issn.1000-9604.2023.05.11
  title: ''
- doi: 10.1021/acs.analchem.3c05019
  title: ''
- doi: 10.1021/ac051437y
  title: ''
evidence_spans:
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS
  metabolite feature table.
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS
  metabolite feature table
- To install ISFrag package R version 4.0.0 or above is required
- github.com/richardxie1119/MEISTER
- github.com__kevinmildau__msFeaST
- jhhung/PS2MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isfrag_cq
    doi: 10.1021/acs.analchem.1c01644
    title: ISFrag
  - build: coll_meister_cq
    doi: 10.1038/s41592-024-02171-3
    title: MEISTER
  - build: coll_msfeast_cq
    doi: 10.1093/bioinformatics/btae584
    title: msFeaST
  - build: coll_opennau_cq
    doi: 10.21147/j.issn.1000-9604.2023.05.11
    title: OpenNAU
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  - build: coll_xcms_cq
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_isfrag_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c01644
  all_source_dois:
  - 10.1021/acs.analchem.1c01644
  - 10.1038/s41592-024-02171-3
  - 10.1093/bioinformatics/btae584
  - 10.21147/j.issn.1000-9604.2023.05.11
  - 10.1021/acs.analchem.3c05019
  - 10.1021/ac051437y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-preprocessing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Preprocessing of raw LCMS data through centroiding, noise filtering, peak detection, and alignment to produce a feature table compatible with downstream metabolite annotation and in-source fragment identification. This is Part 2 of the ISFrag workflow and serves as the foundation for MS2 annotation and ISF analysis.

## When to use

You have raw LCMS data in mzML or mzXML format from DDA, DIA, or fullscan analyses and need to extract metabolite features with unified m/z, retention time, and intensity values across multiple samples before performing MS2 annotation or in-source fragment analysis.

## When NOT to use

- Input data is already a processed feature table in ISFrag-compatible CSV format — use custom.featuretable() to load it directly instead
- You need only MS2 spectra annotation without MS1 feature extraction — skip to Part 3 (MS2 Annotation) if feature table is already available
- Raw data is in a format other than mzXML or mzML — convert to supported format first or use alternative preprocessing tool

## Inputs

- raw LCMS data files (mzML or mzXML format)
- directory path containing one or multiple mzXML files

## Outputs

- feature table (CSV or dataframe format)
- MSnbase object containing MS1 feature data
- unified feature matrix with columns: mz, rt, rtmin, rtmax, and sample intensities

## How to apply

Load raw LCMS files (mzML/mzXML format) into R using XCMS and apply centroiding and noise filtering to MS1 spectra. Use XCMS peak-picking with appropriate peakwidth parameters (e.g., 5–20 seconds) to detect peaks across all samples. For multi-sample analyses, align peaks across samples using XCMS to create a unified feature matrix with m/z and retention time dimensions, then fill missing values for peaks detected in some samples but not others. Finally, integrate peak intensities and export the feature table as CSV with columns in order: m/z, retention time (seconds), min retention time, max retention time, followed by intensity columns for each sample. The resulting feature table format is essential for ISFrag compatibility.

## Related tools

- **XCMS** (Performs centroiding, noise filtering, peak detection, alignment, and missing value imputation on MS1 spectra to generate the feature table) — https://rdrr.io/bioc/xcms/man/
- **R** (Programming language environment required to run XCMS and ISFrag preprocessing functions (version 4.0.0 or above))
- **RStudio** (Recommended IDE for executing preprocessing scripts and managing ISFrag workflow)
- **ISFrag** (R package that wraps XCMS preprocessing via XCMS.featuretable() function and validates feature table format for downstream in-source fragment analysis) — https://github.com/HuanLab/ISFrag.git

## Examples

```
xcmsFT <- XCMS.featuretable(MS1directory = "X:/Users/Sam_Shen/ISFtest20210127/RP(-)/RP(-)1/fullscan", type = "single", peakwidth = c(5,20))
```

## Evaluation signals

- Feature table is successfully exported as CSV with exactly 5 columns in the specified order (mz, rt, rtmin, rtmax, intensity) before sample intensity columns, with all retention time values in seconds
- For multi-sample analyses, XCMS peak alignment and missing value filling are completed without errors, indicated by presence of features across all samples with no NaN values in m/z or rt columns
- Peak detection parameters (peakwidth) are appropriate for instrument—peaks should be detected across expected chromatographic width range (typical 5–20 seconds for HPLC-MS)
- Feature table can be successfully loaded into ISFrag using custom.featuretable() or XCMS.featuretable() function without schema errors, and row count and column structure match input data
- Intensity values are numeric and integrate peak areas across the full chromatographic peak boundary (rtmin to rtmax), not just single-point intensities

## Limitations

- XCMS peak alignment may perform poorly on samples with very different retention time shifts or peak capacity; manual parameter tuning or alternative alignment methods may be required
- CAMERA adduct and isotope annotation are only available when using XCMS-extracted features, not custom feature tables from other tools (MS-DIAL, MZmine2, etc.)
- For DIA (data-independent acquisition) or fullscan data, XCMS feature extraction is supported but peak alignment and filling may be less reliable than for DDA analyses due to different acquisition patterns
- Missing value filling assumes missing peaks are true absences rather than detection failures; very low-intensity or noisy peaks may be incorrectly filled or omitted

## Evidence

- [intro] ISFrag includes MS1 feature extraction as Part 2 of its workflow, with XCMS feature extraction as a sub-component (Section 2.1), which produces a feature table that serves as input for downstream MS2 annotation and in-source fragment identification.: "MS1 feature extraction using XCMS within the ISFrag package…produces a feature table that serves as input for downstream MS2 annotation and in-source fragment identification"
- [methods] 1. Load raw LCMS data files (mzML or mzXML format) into R using XCMS. 2. Perform centroiding and noise filtering on MS1 spectra. 3. Detect peaks across all samples using XCMS peak-picking algorithm. 4. Align peaks across samples to create a unified feature matrix with retention time and m/z dimensions. 5. Fill missing values for peaks detected in some samples but not others. 6. Integrate peak intensities to generate a feature table with rows as metabolite features and columns as samples, storing mass, retention time, and intensity values. 7. Export the feature table as a CSV or tabular format compatible with ISFrag input requirements.: "Perform centroiding and noise filtering on MS1 spectra…Detect peaks across all samples using XCMS peak-picking algorithm…Align peaks across samples to create a unified feature matrix with retention"
- [readme] ISFrag supports multiple ways to generate an MS1 feature table. Users can choose to use XCMS to extract features from mzXML files (Section 2.1), upload their own feature table in csv format (Section 2.2), or combine both features extracted by XCMS with their own feature table (both Section 2.1 and Section 2.2).: "ISFrag supports multiple ways to generate an MS1 feature table. Users can choose to use XCMS to extract features from mzXML files…or upload their own feature table in csv format"
- [readme] In order for ISFrag to successfully read the provided csv file, it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an additional column containing the intensities of features detected in each sample. Note: column 3 and column 4 are the retention time of the feature edges, and all three columns containing retention time information should be in seconds.: "it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an additional column containing the intensities of features detected in"
- [readme] One or multiple mzXML files from DDA, DIA, or fullscan analyses can be analyzed at once using XCMS to extract MS1 features…for multi-sample analyses, peak alignment and filling will be performed by XCMS.: "One or multiple mzXML files from DDA, DIA, or fullscan analyses can be analyzed at once using XCMS to extract MS1 features…peak alignment and filling will be performed by XCMS"
