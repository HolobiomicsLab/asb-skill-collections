---
name: metabolic-feature-identification-from-tandem-spectra
description: Use when when processing data with available MS2 spectra (DDA acquisition) after MS1 peak picking has been completed, and you seek to identify additional metabolic features or validate existing peak picking results through MS2 recognition.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - JPA
  - R
  - XCMS
  - MS-Convert
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo12030212
  title: JPA
evidence_spans:
- JPA is a comprehensive and integrated metabolomics data processing software.
- JPA is a comprehensive and integrated metabolomics data processing software
- '''JPA'' is written in R and its source code is publicly available'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  dedup_kept_from: coll_jpa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12030212
  all_source_dois:
  - 10.3390/metabo12030212
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolic-feature-identification-from-tandem-spectra

## Summary

Extract metabolic features from MS2 (tandem mass spectrometry) spectra as an alternative to MS1 peak picking, generating feature tables with m/z, retention time, and intensity values. This workflow is used when MS2 spectral data are available and MS1 peak picking alone may miss or misclassify features.

## When to use

When processing data with available MS2 spectra (DDA acquisition) after MS1 peak picking has been completed, and you seek to identify additional metabolic features or validate existing peak picking results through MS2 recognition. This is optional but recommended for comprehensive feature extraction in untargeted metabolomics. Do not use this function when processing full-scan or DIA data sets.

## When NOT to use

- Input is full-scan or DIA (data-independent acquisition) data, where MS2 recognition is not applicable
- MS2 spectral data are not available or were not acquired during LC-MS/MS analysis
- Feature extraction has not yet been performed with MS1 peak picking; MS2 recognition should follow, not precede, MS1 analysis

## Inputs

- MS2 spectral data (in mzXML format compatible with vendor formats via MS-Convert)
- Existing MS1 peak picking feature table (dataframe with mz, rt, rtmin, rtmax, maxo, sample columns)
- Raw LC-MS/MS data files in vendor-compatible formats

## Outputs

- MS2 recognition feature table (dataframe with mz, rt, rtmin, rtmax, maxo, sample, and level='MR' columns)
- Combined feature table integrating both MS1 peak picking (PP) and MS2 recognition (MR) features
- Structured output file for downstream analysis (alignment, annotation, statistical analysis)

## How to apply

After MS1 peak picking features have been extracted, load the MS2 spectral data into JPA using R and execute the MS2 recognition module to identify and extract features from MS2 spectra. The workflow generates a feature table containing extracted MS2 features (labeled 'MR') with retention time, mass-to-charge ratio, and intensity information. A threshold for determining whether MR features are true positive can be estimated using the provided 'thresholdEstimate.R' script on the GitHub repository. The resulting feature table is then combined with MS1 peak picking results (labeled 'PP') for integrated downstream analysis. MS2 recognition operates as a distinct analytical pathway, positioned separately from MS1 peak picking to enable multi-modal feature discovery.

## Related tools

- **JPA** (Primary metabolomics data processing package providing MS2 recognition module for feature extraction from tandem spectra) — https://github.com/HuanLab/JPA.git
- **R** (Execution environment for JPA package; R version 4.0.0 or above required)
- **XCMS** (Underlying algorithm used for peak picking and feature detection within JPA) — https://rdrr.io/bioc/xcms/man/
- **MS-Convert** (Tool for converting vendor-specific raw mass spectrometry formats to mzXML for JPA input)

## Examples

```
featureTable_MS2 <- MS2.recognition(featureTable = featureTable, dir = dir, mz.tol = 10, threshold = 0.5)
```

## Evaluation signals

- Feature table output contains both 'MR' (MS2 recognition) and 'PP' (MS1 peak picking) level classifications
- MS2-derived features have valid retention time (rt), mass-to-charge (mz), and intensity (maxo) values consistent with expected ranges
- Combined feature table shows increased total feature count compared to MS1 peak picking alone, indicating successful feature augmentation
- Features meet the true positive threshold determined by thresholdEstimate.R, indicating quality filtering
- Feature table structure matches expected format with columns: mz, rt, rtmin, rtmax, maxo, sample, level

## Limitations

- MS2 recognition is optional and should not be applied to full-scan or DIA datasets; only suitable for DDA (data-dependent acquisition)
- True positive threshold determination requires manual estimation using the provided thresholdEstimate.R script; default thresholds are not provided
- MS2 recognition requires prior MS1 peak picking completion; the workflow is sequential, not standalone
- Feature extraction quality depends on MS2 spectral signal intensity and fragmentation patterns; low-intensity MS2 spectra may yield false negatives

## Evidence

- [readme] After PP features have been extracted, extracting features using MS2 recognition (labeled as 'MR') can be performed. This step is optional.: "After PP features have been extracted, extracting features using MS2 recognition (labeled as 'MR') can be performed. This step is optional."
- [readme] Please do not use this function when processing full-scan or DIA data set!: "Please do not use this function when processing full-scan or DIA data set!"
- [intro] JPA provides MS2 recognition as a distinct feature extraction workflow component, positioned separately from MS1 peak picking, to generate feature tables through alternative analytical pathways.: "JPA provides MS2 recognition as a distinct feature extraction workflow component, positioned separately from MS1 peak picking, to generate feature tables through alternative analytical pathways."
- [readme] The threshold used for determining whether the MR features are true positive can be estimated by using the R code 'thresholdEstimate.R' provided on the GitHub.: "The threshold used for determining whether the MR features are true positive can be estimated by using the R code 'thresholdEstimate.R' provided on the GitHub."
- [intro] Generate a feature table containing the extracted MS2 features with retention time, mass-to-charge ratio, and intensity information.: "Generate a feature table containing the extracted MS2 features with retention time, mass-to-charge ratio, and intensity information."
