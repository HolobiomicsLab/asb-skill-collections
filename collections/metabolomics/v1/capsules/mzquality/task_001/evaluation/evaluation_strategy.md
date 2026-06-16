# Evaluation Strategy

## Direct Checks

- verify file example.tsv exists in package or accessible repository
- verify readData function runs without error on example.tsv as input
- verify buildExperiment function runs without error given readData output and documented column mappings
- verify output object is of class SummarizedExperiment
- verify output object contains 'ratio' assay (verify assays(output) contains key 'ratio')
- verify output object contains non-empty rowData slot
- verify output object contains non-empty colData slot
- verify output object structure has three expected slots: rowData, colData, assays (robust to parameter choices)

## Expert Review

- verify that the 'ratio' assay contains biologically plausible values for metabolomics ratio data
- verify that rowData annotations (compound identifiers, metadata) align with expected metabolomics quality control metadata
- verify that colData annotations (sample identifiers, types, batch information) align with documented column mappings
