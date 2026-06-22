---
name: metabolon-excel-format-handling
description: Use when you have raw Metabolon Excel workbooks (metabolon_v1.1_example.xlsx or metabolon_v1.2_example.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
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
---

# metabolon-excel-format-handling

## Summary

Parse and import Metabolon untargeted metabolomics Excel workbooks (v1.1 and v1.2 formats) into structured R data objects for downstream quality control and analysis. This skill handles the specifics of Metabolon's OrigScale sheet layout and converts vendor-specific formats into a standardized Metaboprep object.

## When to use

You have raw Metabolon Excel workbooks (metabolon_v1.1_example.xlsx or metabolon_v1.2_example.xlsx) containing untargeted metabolite abundance data, sample metadata, and feature annotations, and you need to import them into R for quality control filtering, batch normalization, or statistical analysis using the metaboprep pipeline.

## When NOT to use

- Input is already a pre-processed feature table or abundance matrix in tab-delimited or CSV format; use read.csv() or direct matrix construction instead.
- Metabolon data has already been parsed into separate R objects; use Metaboprep() constructor directly rather than re-parsing Excel.
- Data format is from a different vendor (Nightingale, Olink, SomaLogic); use the corresponding read_nightingale(), read_olink(), or read_somalogic() functions.

## Inputs

- Metabolon Excel workbook (.xlsx): metabolon_v1.1_example.xlsx or metabolon_v1.2_example.xlsx with OrigScale sheet
- OrigScale sheet containing: abundance matrix (metabolites × samples), sample metadata row(s), feature metadata column(s)

## Outputs

- Metaboprep S7 object with 'input' data layer containing abundance matrix, sample metadata, and feature metadata
- List (if return_Metaboprep=FALSE): contains $data (matrix), $samples (data.frame), $features (data.frame)

## How to apply

Use the read_metabolon() function with sheet='OrigScale' and return_Metaboprep=FALSE to parse the Excel file into a list containing three components: a data matrix (abundance values), a samples metadata frame (per-sample covariates and identifiers), and a features metadata frame (metabolite identifiers, pathways, platforms). Extract these three tables and pass them to the Metaboprep() constructor to instantiate an S7 object. Verify successful import by inspecting object dimensions, layer names, and metadata column structure using summary(). This approach preserves the vendor's metadata annotations (e.g., platform, pathway, KEGG identifiers, lot information) while standardizing the internal representation for downstream QC operations.

## Related tools

- **metaboprep** (R package providing read_metabolon() function and Metaboprep S7 class for standardized metabolomics data import and QC) — https://github.com/MRCIEU/metaboprep
- **R** (Programming environment for executing read_metabolon() and Metaboprep object construction)

## Examples

```
mydata <- read_metabolon(system.file("extdata", "metabolon_v1.2_example.xlsx", package = "metaboprep"), sheet="OrigScale", return_Metaboprep=FALSE); mydata <- Metaboprep(data=mydata$data, features=mydata$features, samples=mydata$samples); summary(mydata)
```

## Evaluation signals

- Object successfully instantiated: class(mydata) == 'Metaboprep' and no import errors or warnings during read_metabolon()
- Data dimensions match expected counts: summary(mydata) reports non-zero Samples, Features, and Data Layers with layer names including 'input'
- Metadata integrity: sample metadata contains expected columns (e.g., sample_id, platform, run_day, lot); feature metadata contains metabolite_id, pathway, kegg, platform columns
- No missing/NA rows in critical identifiers: all samples have unique sample_id; all features have unique feature_id and metabolite_id
- Layer structure correct: mydata@data[['input']] is a numeric matrix; mydata@samples and mydata@features are data.frames with matching row/column counts to data matrix

## Limitations

- Function only handles Metabolon v1.1 and v1.2 Excel formats (OrigScale sheet); other Metabolon versions or sheet names require format specification or alternative parsing.
- Requires explicit sheet name ('OrigScale') to be specified; will fail silently or read incorrect sheet if workbook structure deviates from expected layout.
- Return type (list vs. Metaboprep object) controlled by return_Metaboprep parameter; setting to TRUE bypasses manual Metaboprep() construction but may obscure data structure details during import debugging.
- No built-in validation that all samples have complete metadata or all features have taxonomic/pathway annotations; missing data in metadata will propagate into Metaboprep object without warning.

## Evidence

- [other] The metaboprep package provides a read_metabolon function that imports (un)targeted metabolite data from Metabolon example workbook files (metabolon_v1.1_example.xlsx and metabolon_v1.2_example.xlsx): "The metaboprep package provides a read_metabolon function that imports (un)targeted metabolite data from Metabolon example workbook files (metabolon_v1.1_example.xlsx and metabolon_v1.2_example.xlsx)"
- [other] Load the metaboprep R package and read the Metabolon v1.2 example Excel file (metabolon_v1.2_example.xlsx) from the OrigScale sheet using read_metabolon() with return_Metaboprep=FALSE to obtain a list containing data, samples, and features tables.: "Load the metaboprep R package and read the Metabolon v1.2 example Excel file (metabolon_v1.2_example.xlsx) from the OrigScale sheet using read_metabolon() with return_Metaboprep=FALSE to obtain a"
- [other] Construct a Metaboprep S7 object by calling Metaboprep(data=data, samples=samples, features=features). Verify object creation by calling summary(mydata): "Construct a Metaboprep S7 object by calling Metaboprep(data=data, samples=samples, features=features). Verify object creation by calling summary(mydata)"
- [readme] mydata <- read_metabolon(system.file("extdata", "metabolon_v1.1_example.xlsx", package = "metaboprep"), sheet = "OrigScale", return_Metaboprep = FALSE); mydata <- Metaboprep(data = mydata$data, features = mydata$features, samples = mydata$samples): "mydata <- read_metabolon(system.file("extdata", "metabolon_v1.1_example.xlsx", package = "metaboprep"), sheet = "OrigScale", return_Metaboprep = FALSE); mydata <- Metaboprep(data = mydata$data,"
- [readme] Read in and processes (un)targeted metabolite data, saving datasets in tab-delimited format for use elsewhere: "Read in and processes (un)targeted metabolite data, saving datasets in tab-delimited format for use elsewhere"
