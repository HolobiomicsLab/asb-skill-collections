---
name: feature-intensity-quantification
description: Use when after features have been identified in LC-MS data via peak picking, MS2 recognition, or targeted-list matching, and you need to measure their signal magnitude (peak height or area) across samples for quantitative comparison, normalization, or statistical testing in metabolomics studies.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - JPA
  - R
  - XCMS
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

# feature-intensity-quantification

## Summary

Quantify metabolic feature intensities from LC-MS data by extracting and measuring peak heights or areas for identified m/z and retention time features. This is a core output of JPA's feature extraction workflows (MS1 peak picking, MS2 recognition, and targeted-list extraction) that produces intensity values for downstream sample alignment and statistical analysis.

## When to use

After features have been identified in LC-MS data via peak picking, MS2 recognition, or targeted-list matching, and you need to measure their signal magnitude (peak height or area) across samples for quantitative comparison, normalization, or statistical testing in metabolomics studies.

## When NOT to use

- Input is already an aligned feature table from another tool—JPA expects unaligned single-sample feature tables or raw data
- Processing full-scan or DIA (data-independent acquisition) datasets—MS2 recognition (which can inform intensity assignment) should not be used for these modes
- Intensity normalization or batch-effect correction is needed—quantification alone does not address these post-extraction steps

## Inputs

- mzXML or netCDF raw LC-MS data files
- Feature table (CSV format with columns: m/z, retention time, rtmin, rtmax, intensity)
- User-supplied target list (m/z values, retention times, tolerances)

## Outputs

- Feature table (dataframe with columns: mz, rt, rtmin, rtmax, maxo, sample, level)
- Quantified feature intensities (maxo column) for each feature across samples
- Exported CSV or tabular format feature table with intensity values

## How to apply

The JPA package automatically quantifies feature intensities during feature extraction by recording the maximum observed signal (maxo column) for each detected peak. For MS1 peak picking, the XCMS.featureTable() function processes raw mzXML/netCDF files with parameters including peakwidth (typically c(5,20) seconds) and noise threshold to define peak boundaries and compute intensity. For targeted-list extraction, features matching user-supplied m/z and retention time windows are extracted and their intensities recorded. The resulting feature table contains intensity values aligned with corresponding m/z, retention time, sample identifiers, and feature level (PP for peak picking or MR for MS2 recognition). These intensity values form the quantitative matrix for downstream alignment and annotation steps.

## Related tools

- **JPA** (Comprehensive R package performing MS1 peak picking (XCMS.featureTable), MS2 recognition, and targeted-list extraction; outputs feature tables with quantified intensities (maxo) for each feature) — https://github.com/HuanLab/JPA.git
- **XCMS** (Embedded peak picking algorithm within JPA used to detect peaks, define peak boundaries (peakwidth parameter), and compute maximum intensity (maxo) from raw LC-MS data)
- **R** (Programming language and environment required (version 4.0.0 or above) to execute JPA functions and manipulate the quantified feature table)

## Examples

```
featureTable <- XCMS.featureTable(dir = "X:/Users/JPAtest_20210330/multiDDA", mz.tol = 10, ppm=10, peakwidth=c(5,20), mzdiff = 0.01, snthresh = 6, integrate = 1, prefilter = c(3,100), noise = 100); head(featureTable[,c('mz','rt','maxo','sample')])
```

## Evaluation signals

- Feature table contains a non-empty 'maxo' column with numeric intensity values ≥ noise threshold (default 100)
- All extracted features have positive, non-zero intensity values consistent with peak height from the raw LC-MS data
- Number of rows (features) and columns (mz, rt, rtmin, rtmax, maxo, sample, level) match expected structure for the extraction method used (PP, MR, or targeted-list)
- Intensity values are reproducible across re-runs with identical input data and parameters; variance across technical replicates is minimal
- Exported CSV feature table rows correspond 1:1 to identified peaks, with intensity values within expected range for the mass spectrometry instrument and ionization method

## Limitations

- XCMS peak picking may underestimate or miss non-Gaussian shaped peaks; JPA addresses this by extracting both Gaussian and non-Gaussian features, but users should visually inspect extracted intensities for irregular peak morphology
- Peak intensity is sensitive to noise threshold and peakwidth parameters; suboptimal settings can lead to false negatives (missed features) or false positives (noise misidentified as signal)
- For multi-sample analysis, sample alignment must be performed after intensity quantification (Part 5 in JPA manual) to enable cross-sample comparison; raw intensity values are not directly comparable between samples without alignment
- MS2 recognition should not be used for full-scan or DIA data, limiting the applicability of intensity quantification via MS2 recognition in those acquisition modes
- Intensity values alone do not account for instrument drift, ionization suppression, or other analytical biases; normalization and batch-effect correction are required before statistical testing

## Evidence

- [readme] The XCMS.featureTable() function outputs a dataframe formatted featuretable as well as an MSnbase object. The 'level' column shows the level of each feature.: "The XCMS.featureTable() function outputs a dataframe formatted featuretable as well as an MSnbase object. The 'level' column shows the level of each feature."
- [readme] It extract both Gaussian and non-Gaussian shaped metabolic features.: "It extract both Gaussian and non-Gaussian shaped metabolic features."
- [other] Compile extracted features into a feature table (rows = features, columns = samples/measurements and m/z, retention time, intensity values).: "Compile extracted features into a feature table (rows = features, columns = samples/measurements and m/z, retention time, intensity values)."
- [readme] peakwidth=c(5,20), mzdiff = 0.01, snthresh = 6, integrate = 1, prefilter = c(3,100), noise = 100: "peakwidth=c(5,20), mzdiff = 0.01, snthresh = 6, integrate = 1, prefilter = c(3,100), noise = 100"
- [readme] for multi-sample analysis, sample alignment is performed after feature extraction: "for multi-sample analysis, sample alignment is performed after feature extraction"
