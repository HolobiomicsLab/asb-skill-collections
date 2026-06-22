---
name: eic-data-extraction-from-xcms
description: Use when after running XCMS getEIC() to generate xcmsEIC objects and fillPeaks() to produce a filled xcmsSet object, before computing the 12 peak-quality metrics (Apex Max-Boundary Ratio, Elution Shift, FWHM2Base, Jaggedness, Modality, Symmetry, Sharpness, Gaussian Similarity, Retention-Time.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3185
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - MetaClean
  - XCMS
  - R
  techniques:
  - LC-MS
derived_from:
- doi: 10.1007/s11306-020-01738-3
  title: MetaClean
- doi: 10.1186/1471-2105-15-s11-s5
  title: ''
evidence_spans:
- MetaClean is a package for building classifiers to identify low quality integrations in untargeted metabolomics data.
- '`MetaClean` provides 8 classification algorithms (implemented with the R package `caret`) for building a predictive model.'
- The package is designed for use with the preprocessing package XCMS and can be easily integrated into existing untargeted metabolomics pipelines.
- A peak table (like that returned by xcms::peakTable())
- getEvalObj is called to extract the relevant data from the three objects provided by ther user and store them in an object of class evalObj
- It is an R package and can be easily incorporated
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaclean_cq
    doi: 10.1007/s11306-020-01738-3
    title: MetaClean
  dedup_kept_from: coll_metaclean_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01738-3
  all_source_dois:
  - 10.1007/s11306-020-01738-3
  - 10.1186/1471-2105-15-s11-s5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# EIC Data Extraction from XCMS

## Summary

Extract retention time, intensity, and peak characteristic data from XCMS-derived EIC and filled peak objects into a structured evalObj for downstream peak-quality metric computation. This skill bridges XCMS preprocessing output and quality assessment in untargeted LC-MS metabolomics workflows.

## When to use

After running XCMS getEIC() to generate xcmsEIC objects and fillPeaks() to produce a filled xcmsSet object, before computing the 12 peak-quality metrics (Apex Max-Boundary Ratio, Elution Shift, FWHM2Base, Jaggedness, Modality, Symmetry, Sharpness, Gaussian Similarity, Retention-Time Consistency, TPASR, Zig-Zag Index, and related metrics) used to classify low-quality peaks in untargeted metabolomics data.

## When NOT to use

- XCMS preprocessing has not yet been completed; getEIC() and fillPeaks() must have already been run.
- Input is raw MS data in mzML or netCDF format; this skill operates on post-XCMS objects, not raw instrument data.
- Peak-quality metrics have already been computed; getEvalObj is a prerequisite step, not a replacement for existing metric tables.

## Inputs

- xcmsEIC object (from XCMS getEIC())
- filled xcmsSet object (from XCMS fillPeaks())
- optional EIC labels CSV with columns for EIC number and class label

## Outputs

- evalObj with slots eicPts (list of retention time–intensity pairs per EIC), eicPeakData (peak characteristics: apex, start, end, intensity), and eicNos (EIC identifiers)

## How to apply

Call the getEvalObj function on the xcmsEIC object (output from XCMS getEIC()) and the filled xcmsSet object (output from fillPeaks()) to extract and structure peak data. The function populates an evalObj with three key slots: eicPts (retention time and intensity vectors from each EIC), eicPeakData (peak characteristics such as apex position, start/end boundaries, and intensity), and eicNos (EIC identifiers). Optionally supply an EIC labels CSV to annotate peaks with class labels (e.g., metabolite identity or manual quality flags). The evalObj serves as the standardized input for getPeakQualityMetrics in the subsequent step, ensuring that all retention time, intensity, and boundary data are properly aligned and indexed by EIC number.

## Related tools

- **MetaClean** (R package that provides getEvalObj function to extract and structure EIC data from XCMS objects) — https://github.com/KelseyChetnik/MetaClean
- **XCMS** (LC-MS preprocessing software that produces xcmsEIC and xcmsSet objects consumed by getEvalObj)
- **R** (Runtime environment for executing getEvalObj and downstream MetaClean functions)

## Examples

```
evalObj <- getEvalObj(xcmsEIC = eic_object, xcmsSet = filled_set, eicLabels = label_df)
```

## Evaluation signals

- evalObj contains three populated slots: eicPts (list of numeric vectors with length ≥ 1 per EIC), eicPeakData (data frame or list with columns for apex, start boundary, end boundary, and apex intensity), and eicNos (vector of unique EIC identifiers matching the number of rows in eicPeakData)
- All retention time values in eicPts are numeric and ordered monotonically within each EIC
- Peak characteristics in eicPeakData satisfy boundary constraints: start < apex < end for each peak
- If EIC labels are provided, the number of rows in the resulting labeled output equals the number of peaks, with no missing class assignments
- evalObj can be successfully passed to getPeakQualityMetrics without schema errors or missing data exceptions

## Limitations

- Requires successful prior execution of XCMS getEIC() and fillPeaks(); missing or malformed xcmsEIC or xcmsSet objects will cause extraction failure.
- EIC label CSV, if supplied, must have matching EIC numbers; unmatched EICs will either be dropped or assigned missing values depending on join semantics (not fully specified in the article).
- Peak extraction assumes that XCMS peak-picking has already identified and characterized peaks; getEvalObj does not perform de novo peak detection.

## Evidence

- [other] Call getEvalObj on the xcmsEIC and fill objects to extract retention time, intensity, and peak characteristic data into an evalObj with slots eicPts, eicPeakData, and eicNos.: "Call getEvalObj on the xcmsEIC and fill objects to extract retention time, intensity, and peak characteristic data into an evalObj with slots eicPts, eicPeakData, and eicNos."
- [methods] The function getEvalObj is called to extract the relevant data from the three objects provided by the user.: "The function getEvalObj is called to extract the relevant data from the three objects provided by the user"
- [other] Load the xcmsEIC object (from XCMS getEIC()) and filled xcmsSet object (from fillPeaks()) and optional EIC labels CSV.: "Load the xcmsEIC object (from XCMS getEIC()) and filled xcmsSet object (from fillPeaks()) and optional EIC labels CSV."
- [readme] can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS: "can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS"
