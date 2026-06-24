---
name: metabolite-feature-extraction-xcms
description: Use when you have one or multiple raw mzXML/mzML files from DDA, DIA,
  or full-scan LCMS analyses and need to detect, align, and quantify metabolite features
  across samples to create a unified feature matrix before MS2 annotation or in-source
  fragment analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3370
  tools:
  - ISFrag
  - XCMS
  - R
  - RStudio
  - devtools
  - XCMS CentWave
  - Paramounter
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c01644
  title: ISFrag
- doi: 10.1021/acs.analchem.1c04758
  title: ''
evidence_spans:
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS
  metabolite feature table.
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS
  metabolite feature table
- XCMS-based MS1 feature extraction
- 2.1 XCMS Feature Extraction
- To install ISFrag package R version 4.0.0 or above is required
- mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values
  and retention times) extracted by XCMS CentWave
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isfrag_cq
    doi: 10.1021/acs.analchem.1c01644
    title: ISFrag
  - build: coll_paramounter_cq
    doi: 10.1021/acs.analchem.1c04758
    title: Paramounter
  dedup_kept_from: coll_isfrag_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c01644
  all_source_dois:
  - 10.1021/acs.analchem.1c01644
  - 10.1021/acs.analchem.1c04758
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-extraction-xcms

## Summary

Extract and align MS1 metabolite features from raw LCMS data (mzXML/mzML format) using the XCMS algorithm within the ISFrag R package. This produces a feature table with m/z, retention time, and intensity values suitable for downstream MS2 annotation and in-source fragment identification.

## When to use

You have one or multiple raw mzXML/mzML files from DDA, DIA, or full-scan LCMS analyses and need to detect, align, and quantify metabolite features across samples to create a unified feature matrix before MS2 annotation or in-source fragment analysis.

## When NOT to use

- Input is already a processed feature table (use custom.featuretable instead)
- Data format is not mzXML or mzML (XCMS requires these binary/text mass spectrometry formats)
- You need only CAMERA adduct and isotope annotation without full XCMS feature extraction (CAMERA requires XCMS-only analysis path)

## Inputs

- raw LCMS data files (mzXML or mzML format)
- directory path containing one or multiple mzXML files

## Outputs

- feature table (dataframe with columns: mz, rt, rtmin, rtmax, intensity/maxo per sample)
- CSV file in ISFrag-compatible format
- MSnbase object (from XCMS.featuretable function)

## How to apply

Load raw LCMS data files (mzXML or mzML format) into R using XCMS within ISFrag. Apply XCMS peak-picking to detect peaks across all samples, specifying appropriate peakwidth parameters (e.g., c(5,20) seconds). Align peaks across samples to create a unified feature matrix with m/z and retention time dimensions. For multi-sample analyses, XCMS automatically performs peak alignment and missing value filling to generate features detected in some but not all samples. Export the resulting feature table as a CSV with columns: m/z, retention time, min retention time, max retention time, and intensity values per sample. The output dataframe becomes input for ISFrag's MS2 annotation and ISF identification steps.

## Related tools

- **XCMS** (Performs peak detection, alignment, and intensity integration on MS1 spectra) — https://rdrr.io/bioc/xcms/man/
- **ISFrag** (R package wrapper that calls XCMS for feature extraction and integrates with downstream MS2 annotation and ISF identification) — https://github.com/HuanLab/ISFrag.git
- **R** (Runtime environment; version 4.0.0 or above required)
- **RStudio** (Recommended IDE for installation and execution)
- **devtools** (R package used to install ISFrag from GitHub)

## Examples

```
xcmsFT <- XCMS.featuretable(MS1directory = "X:/Users/Sam_Shen/ISFtest20210127/RP(-)/RP(-)1/fullscan", type = "single", peakwidth = c(5,20))
```

## Evaluation signals

- Output feature table contains all required columns (mz, rt, rtmin, rtmax, intensity) with no missing values in metadata columns
- Feature table row count and column count match expected dimensions (features × samples)
- m/z values are numeric and within expected mass range for target metabolites; retention time values are in seconds and span the LC gradient duration
- Intensity values are positive numeric; multi-sample analyses show features with non-zero intensity in at least one sample (successful alignment and filling)
- CSV export successfully loads and parses without encoding errors; schema matches ISFrag input specification (column order: m/z, rt, rtmin, rtmax, then intensity columns)

## Limitations

- XCMS peak-picking quality depends on appropriate peakwidth parameter selection; incorrect values may miss narrow peaks or detect noise
- Multi-sample peak alignment assumes samples have comparable retention time shift; very different LC conditions across samples may reduce alignment accuracy
- CAMERA adduct and isotope annotation features are only available when using XCMS alone, not when combining XCMS features with custom feature tables
- All mzXML files must be placed in a single folder containing no other irrelevant mzXML files to avoid unintended file inclusion

## Evidence

- [readme] One or multiple mzXML files from DDA, DIA, or fullscan analyses can be analyzed at once using XCMS to extract MS1 features.: "One or multiple mzXML files from DDA, DIA, or fullscan analyses can be analyzed at once using XCMS to extract MS1 features."
- [readme] For multi-sample analyses, peak alignment and filling will be performed by XCMS.: "for multi-sample analyses, peak alignment and filling will be performed by XCMS"
- [other] Detect peaks across all samples using XCMS peak-picking algorithm. Align peaks across samples to create a unified feature matrix with retention time and m/z dimensions. Fill missing values for peaks detected in some samples but not others.: "Detect peaks across all samples using XCMS peak-picking algorithm. 4. Align peaks across samples to create a unified feature matrix with retention time and m/z dimensions. 5. Fill missing values for"
- [readme] In order for ISFrag to succesfully read the provided csv file, it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an additional column containing the intensities: "it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an additional column containing the intensities"
- [readme] CAMERA adduct and isotope annotation can only be used for XCMS ONLY ISFrag analysis.: "CAMERA adduct and isotope annotation can only be used for XCMS ONLY ISFrag analysis"
