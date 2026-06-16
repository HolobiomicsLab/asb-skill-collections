# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does the buildExperiment function correctly construct a SummarizedExperiment object with a computed ratio assay when given a data frame with specified column mappings for compounds, samples, and internal standards?: 'The `buildExperiment` function allows you to create a *SummarizedExperiment* object from a data frame by specifying the following columns: `compoundColumn`, `aliquotColumn`, `primaryAssay`,'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The buildExperiment function constructs a SummarizedExperiment object from a data frame by mapping user-specified columns to compound names, sample names, primary assay (compound area), secondary assay (internal standard area), and sample types. The function automatically calculates the compound/internal standard ratio for each sample and stores it in the 'ratio' assay, with the ratio computed as primary assay divided by secondary assay (or set to primary assay if secondary assay is not provided).: 'The `buildExperiment` function will automatically calculate the compound / Internal Standard ratio for each sample and store it in the `ratio` assay. Note that if the `secondaryAssay` column is not'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] example.tsv file from mzQuality package (extdata/example.tsv): 'file <- system.file("extdata/example.tsv", package = "mzQuality")'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] SummarizedExperiment object with rowData, colData, and assays including 'ratio': 'The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] mzQuality: 'library(mzQuality)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] R: 'library(mzQuality)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] SummarizedExperiment: 'The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found.: '_No changelog found._'
