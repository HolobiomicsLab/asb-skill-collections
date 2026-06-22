---
name: s7-object-construction-and-validation
description: Use when after successfully parsing vendor-specific metabolomic data files (Metabolon Excel, Nightingale, Olink, SomaLogic) into separate data, samples, and features tables, and before applying quality control or batch normalization pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - R
  - metaboprep
derived_from:
- doi: 10.1093/bioinformatics/btac059/6522114
  title: Metaboprep
evidence_spans:
- library(metaboprep)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboprep_cq
    doi: 10.1093/bioinformatics/btac059/6522114
    title: Metaboprep
  dedup_kept_from: coll_metaboprep_cq
schema_version: 0.2.0
---

# S7 Object Construction and Validation

## Summary

Construct and validate S7 class objects (specifically Metaboprep) from parsed metabolomic data components, ensuring correct integration of data matrices, sample metadata, and feature metadata into a coherent analytical container. This skill verifies object integrity through schema validation and dimensional consistency checks.

## When to use

After successfully parsing vendor-specific metabolomic data files (Metabolon Excel, Nightingale, Olink, SomaLogic) into separate data, samples, and features tables, and before applying quality control or batch normalization pipelines. Use this skill when you have three aligned tabular components (intensity matrix, sample annotations, feature annotations) that must be bound into a single structured object for downstream analysis.

## When NOT to use

- Input is already a Metaboprep object or other formally constructed S7 class instance—use object accessor methods instead.
- Data components are not yet aligned (different row/column counts between data, samples, and features tables)—align dimensions first.
- Metadata frames contain rows with missing sample_id or feature_id keys—validate and deduplicate metadata before construction.

## Inputs

- data matrix (numeric, rows=samples, columns=features)
- samples metadata frame (rows correspond to data matrix rows)
- features metadata frame (rows correspond to data matrix columns)

## Outputs

- Metaboprep S7 object with input data layer
- Object summary report (dimensions, layer names, metadata column inventory)

## How to apply

Call the Metaboprep() constructor with three mandatory arguments: data (numeric matrix of metabolite intensities, rows=samples, columns=features), samples (data frame of sample-level metadata with rows matching data matrix rows), and features (data frame of feature-level metadata with rows matching data matrix columns). Immediately verify object construction by calling summary() on the returned object to confirm: (1) sample count matches the number of rows in data and samples; (2) feature count matches the number of columns in data and features; (3) data layers are correctly initialized (typically 'input' layer for raw data); (4) sample and feature metadata columns are accessible and non-empty. This validation step ensures dimensional alignment before proceeding to quality control filters, which assume a well-formed Metaboprep container.

## Related tools

- **metaboprep** (Provides Metaboprep S7 class definition and constructor; validates object schema and summarizes dimensional integrity) — https://github.com/MRCIEU/metaboprep
- **R** (Execution environment for S7 object instantiation and method dispatch)

## Examples

```
mydata <- Metaboprep(data = mydata$data, samples = mydata$samples, features = mydata$features); summary(mydata)
```

## Evaluation signals

- summary() output confirms Samples and Features counts match input data matrix dimensions (rows and columns respectively)
- Object contains exactly one 'input' data layer after construction, accessible via @data_layers
- Sample and feature metadata are non-empty and structurally aligned: nrow(samples) == nrow(data), nrow(features) == ncol(data)
- Metadata column names are preserved and accessible; sample_id and feature_id are present and unique
- No warnings or errors during Metaboprep() call; object class is 'Metaboprep' as verified by class()

## Limitations

- Metaboprep constructor does not auto-repair misaligned dimensions; all three input components must have consistent row/column counts before construction.
- No automatic deduplication of sample_id or feature_id values; duplicate identifiers in metadata may cause undefined behavior in downstream methods.
- Object construction itself performs no quality control filtering—data quality assessment must follow object creation as a separate pipeline step.
- S7 object is tied to the R environment; export to other languages or long-term storage requires explicit serialization (e.g., export() method).

## Evidence

- [methods] Construct a Metaboprep S7 object by calling Metaboprep(data=data, samples=samples, features=features).: "mydata <- Metaboprep(data = data, samples = samples, features = features)"
- [methods] Verify object creation by calling summary() to confirm data dimensions and layer structure.: "summary(mydata) to confirm data dimensions, sample and feature counts, and layer structure"
- [other] The metaboprep package provides a read_metabolon function that imports metabolite data and can construct a Metaboprep object for subsequent processing and analysis.: "The metaboprep package provides a read_metabolon function that imports (un)targeted metabolite data from Metabolon example workbook files (metabolon_v1.1_example.xlsx and metabolon_v1.2_example.xlsx)"
- [readme] Example summary output showing Samples, Features, Data Layers, Layer Names, and metadata structure.: "Metaboprep Object Summary
--------------------------
Samples      : 100
Features     : 100
Data Layers  : 2
Layer Names  : input, qc

Sample Annotation (metadata):
  Columns: 8
  Names  : sample_id,"
- [methods] Extract and construct components from parsed data before object creation.: "Extract the data matrix, samples metadata frame, and features metadata frame from the returned list."
