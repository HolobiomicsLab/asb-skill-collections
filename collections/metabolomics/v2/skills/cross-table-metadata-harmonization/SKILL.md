---
name: cross-table-metadata-harmonization
description: Use when when you have obtained raw metabolite abundance data in a format that separates the measurement matrix from sample-level metadata (e.g., run day, plate ID, cohort variables) and feature-level annotations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac059/6522114
  all_source_dois:
  - 10.1093/bioinformatics/btac059/6522114
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-table-metadata-harmonization

## Summary

Reconcile and integrate sample and feature metadata tables with a primary abundance data matrix into a unified object structure, ensuring consistent identifiers and annotations across all three components. This skill is essential when importing heterogeneous metabolomics data formats (Metabolon Excel, Nightingale, Olink, SomaLogic) that separate measurements, sample descriptors, and feature annotations into separate files or sheets.

## When to use

When you have obtained raw metabolite abundance data in a format that separates the measurement matrix from sample-level metadata (e.g., run day, plate ID, cohort variables) and feature-level annotations (e.g., metabolite name, pathway, KEGG ID, ionization mode), and you need to construct a single validated object for downstream QC filtering and statistical analysis. Common triggers: importing Metabolon .xlsx workbooks with separate OrigScale, Sample annotations, and Feature annotations sheets; reconciling lab-specific sample tracking tables with vendor-provided feature libraries.

## When NOT to use

- Data is already in a single pre-harmonized matrix with all metadata embedded as row/column attributes or a single wide table; use direct matrix import instead.
- Sample or feature identifiers across the three tables are inconsistent or non-overlapping; perform identifier reconciliation and imputation before applying this skill.
- Abundance data and metadata have been collected at different temporal or spatial scales (e.g., batch effects, replicates) that require pre-normalization; apply batch_normalise or other preprocessing first.

## Inputs

- Numeric abundance matrix (samples × features, or features × samples depending on orientation)
- Sample metadata data frame with sample_id as index or primary column
- Feature metadata data frame with feature_id as index or primary column
- Source file(s): Metabolon Excel workbook (metabolon_v1.1_example.xlsx or v1.2), Nightingale .xlsx, Olink .txt, or SomaLogic .adat

## Outputs

- Metaboprep S7 object containing harmonized data, samples, and features layers
- Object attributes: @data (abundance matrix), @samples (metadata frame), @features (metadata frame)
- Layer 'input' containing the original integrated data

## How to apply

Obtain three aligned tables: a numeric data matrix (samples × features), a samples metadata frame indexed by sample_id, and a features metadata frame indexed by feature_id. Load each using the appropriate vendor-specific reader (read_metabolon, read_nightingale, read_olink, read_somalogic) with return_Metaboprep=FALSE to receive a list, or load manually using read.csv. Verify row/column name consistency: all sample identifiers in the data matrix columns must match the sample_id column in the samples table; all feature identifiers in the data matrix rows must match the feature_id column in the features table. Construct the Metaboprep S7 object by calling Metaboprep(data=<matrix>, samples=<frame>, features=<frame>), which validates the three-way correspondence internally. Confirm successful harmonization by calling summary(object) to check total sample and feature counts, layer names, and annotation column lists.

## Related tools

- **metaboprep** (Core R package providing Metaboprep class definition, read_metabolon/read_nightingale/read_olink/read_somalogic readers, and object validation during harmonization) — https://github.com/MRCIEU/metaboprep
- **R** (Host language for Metaboprep object construction and summary operations)

## Examples

```
library(metaboprep); mydata <- read_metabolon(system.file("extdata", "metabolon_v1.2_example.xlsx", package = "metaboprep"), sheet = "OrigScale", return_Metaboprep = FALSE); obj <- Metaboprep(data = mydata$data, samples = mydata$samples, features = mydata$features); summary(obj)
```

## Evaluation signals

- Object creation succeeds without error and summary(object) displays non-zero sample and feature counts matching the input tables.
- Metaboprep @data matrix dimensions equal (number of features, number of samples) and all row/column names are present.
- @samples and @features data frames have row counts equal to the matrix dimensions and contain the expected annotation columns.
- No missing or NA values in the sample_id and feature_id identifier columns; all identifiers in the matrix are present in the corresponding metadata frames.
- Layer attribute contains 'input' layer; sample_summary and feature_summary attributes are generated and non-empty.

## Limitations

- Harmonization assumes one-to-one correspondence between matrix rows/columns and metadata rows; many-to-many relationships or hierarchical sample/feature groupings are not handled and will cause validation errors.
- Metadata frame must be a data.frame or coercible to one; complex nested or ragged structures will fail.
- The read_metabolon and related vendor readers depend on specific Excel sheet names and column orderings; deviations from the example workbooks (metabolon_v1.1_example.xlsx, metabolon_v1.2_example.xlsx) may result in parsing errors or misalignment.
- Metaboprep object creation does not perform automatic identifier deduplication or collision resolution; duplicate sample_id or feature_id values will not be detected until QC filtering steps attempt to subset the data.

## Evidence

- [other] The metaboprep package provides a read_metabolon function that imports (un)targeted metabolite data from Metabolon example workbook files (metabolon_v1.1_example.xlsx and metabolon_v1.2_example.xlsx) and can construct a Metaboprep object for subsequent processing and analysis.: "The metaboprep package provides a read_metabolon function that imports (un)targeted metabolite data from Metabolon example workbook files"
- [readme] mydata <- Metaboprep(data = mydata$data, features = mydata$features, samples = mydata$samples): "mydata <- Metaboprep(data     = mydata$data, features = mydata$features, samples  = mydata$samples)"
- [other] Extract the data matrix, samples metadata frame, and features metadata frame from the returned list. Construct a Metaboprep S7 object by calling Metaboprep(data=data, samples=samples, features=features). Verify object creation by calling summary(mydata) to confirm data dimensions, sample and feature counts, and layer structure.: "Extract the data matrix, samples metadata frame, and features metadata frame from the returned list. Construct a Metaboprep S7 object by calling Metaboprep(data=data, samples=samples,"
- [readme] Metaboprep Object Summary … Samples : 100 Features : 100 Data Layers : 2 Layer Names : input, qc: "Metaboprep Object Summary … Samples      : 100 … Features     : 100 … Data Layers  : 2 … Layer Names  : input, qc"
- [readme] Read in and processes (un)targeted metabolite data: "Read in and processes (un)targeted metabolite data, saving datasets in tab-delimited format for use elsewhere"
