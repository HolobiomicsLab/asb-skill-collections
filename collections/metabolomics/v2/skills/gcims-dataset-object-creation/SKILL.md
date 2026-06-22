---
name: gcims-dataset-object-creation
description: Use when you have raw GCIMS sample files (from a GC–IMS instrument) and an annotations table (Excel, CSV, or TSV) with sample metadata, and you need to begin the GCIMS preprocessing pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GCIMS
derived_from:
- doi: 10.1016/j.chemolab.2023.104938
  title: GCIMS
evidence_spans:
- library(ggplot2) library(cowplot) library(GCIMS)
- library(GCIMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcims_cq
    doi: 10.1016/j.chemolab.2023.104938
    title: GCIMS
  dedup_kept_from: coll_gcims_cq
schema_version: 0.2.0
---

# gcims-dataset-object-creation

## Summary

Create a GCIMSDataset object in R from raw Gas Chromatography–Ion Mobility Spectrometry data files to enable downstream preprocessing (filtering, smoothing, alignment, peak detection). This is the foundational step that wraps raw GCIMS samples and their metadata into a unified object suitable for the GCIMS pipeline.

## When to use

You have raw GCIMS sample files (from a GC–IMS instrument) and an annotations table (Excel, CSV, or TSV) with sample metadata, and you need to begin the GCIMS preprocessing pipeline. The GCIMSDataset object must be created before any filtering, smoothing, decimation, or alignment operations can be applied.

## When NOT to use

- The data is already in a processed feature table or peak table format; use this skill only to wrap raw 2D spectra data.
- You do not have sample metadata or an annotations table; GCIMSDataset requires metadata linking raw files to sample identifiers.
- Your raw files are in a different analytical format (e.g., LC–MS, HPLC) not produced by a GC–IMS instrument.

## Inputs

- raw GCIMS data files (from Gas Chromatography–Ion Mobility Spectrometry instrument)
- annotations table (Excel spreadsheet, CSV, or TSV file with sample metadata)

## Outputs

- GCIMSDataset object (R object storing 2D matrices and sample metadata)

## How to apply

Prepare an annotations table (Excel spreadsheet, CSV, or TSV file) with sample names and their metadata (e.g., group, replicate, treatment). Load your raw GCIMS data files into R along with the GCIMS package. Call the GCIMSDataset constructor (or equivalent function in GCIMS) passing the data file paths and the annotations table to create the object. The resulting GCIMSDataset object will store the raw 2D matrices (drift time × retention time) and metadata in memory-efficient structures using delayed evaluations where possible. Verify that the object contains the expected number of samples and that drift time and retention time dimensions are correctly populated before proceeding to filtering steps.

## Related tools

- **GCIMS** (R package that provides the GCIMSDataset constructor and delayed-evaluation framework for memory-efficient data handling) — https://github.com/sipss/GCIMS
- **R** (Programming language and environment in which GCIMS runs and GCIMSDataset objects are created and manipulated)

## Examples

```
# After installing GCIMS and preparing annotations.xlsx
library(GCIMS)
dataset <- GCIMSDataset(data_path = "./raw_gcims_files/", annotations = "annotations.xlsx")
```

## Evaluation signals

- The GCIMSDataset object is successfully created without errors and is a valid R object of class GCIMSDataset.
- The object contains the correct number of samples matching the annotations table row count.
- Drift time dimension is present and spans the expected range (typically 5–16 ms after filtering).
- Retention time dimension is present and spans the expected range (typically 0–1100 s after filtering).
- The delayed evaluation framework is active (verify via object structure inspection) so that subsequent filtering and smoothing operations do not immediately consume large amounts of RAM.

## Limitations

- The GCIMSDataset object stores raw data and does not perform quality control; data quality issues (e.g., corrupted files, missing samples) may not be caught until downstream steps.
- Memory efficiency via delayed evaluations is relative; very large datasets or machines with limited RAM may still face memory constraints.
- The annotations table must be carefully formatted and match the raw data file naming or organization; mismatches will cause sample metadata to be incorrectly assigned or missing.

## Evidence

- [intro] Annotations table preparation required: "Please start by preparing an Excel spreadsheet (or a CSV/TSV file if you prefer) with your samples and their annotations."
- [intro] GCIMSDataset object creation step: "Create a GCIMSDataset object"
- [intro] Delayed evaluations for efficiency: "GCIMS uses delayed evaluations were possible, so dataset modifications can be executed in a more efficient way and without using too much RAM."
- [readme] Package introduction: "GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples."
- [readme] Installation and startup guidance: "Checkout our Introduction to GCIMS to start."
