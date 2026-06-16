# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] When the secondaryAssay column is not provided to buildExperiment, does the resulting 'ratio' assay equal the primary assay values unchanged?: 'Note that if the `secondaryAssay` column is not provided, its value will be set to `1`, effectively negating the Internal Standard.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] When secondaryAssay is not provided to buildExperiment, its value defaults to 1, which negates the Internal Standard effect, making the ratio assay equal to the primary assay values.: 'Note that if the `secondaryAssay` column is not provided, its value will be set to `1`, effectively negating the Internal Standard.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] example.tsv — tab-delimited metabolomics data file containing columns: aliquot, compound, area, compound_is, area_is, type, injection_time, batch, and concentration: 'The data should be in a tab-delimited format containing at least the following columns: aliquot, compound, area, type, injection_time, batch.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Validation report (CSV or text) confirming that all 'ratio' assay values equal corresponding primary assay values within numerical tolerance (machine epsilon): 'The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] R: 'library(mzQuality)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] mzQuality: 'mzQuality requires a specific format for the input data.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] SummarizedExperiment: 'Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: '_No changelog found._'
