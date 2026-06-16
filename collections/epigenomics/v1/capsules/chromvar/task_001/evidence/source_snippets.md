# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What is the structure and composition of a chromVARDeviations object produced by applying the standard chromVAR preprocessing and motif deviation workflow to the example_counts dataset?: 'chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The computeDeviations function returns a SummarizedExperiment object containing deviation scores that quantify motif-associated variability in chromatin accessibility across samples, with dimensions and assay structure determined by the number of samples and motifs after applying filterSamples, filterPeaks, addGCBias, computeExpectations, and getBackgroundPeaks preprocessing steps.: 'The function `computeDeviations` returns a SummarizedExperiment with two "assays"'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] example_counts: bundled chromVAR example dataset (RangedSummarizedExperiment with counts assay): 'data(example_counts, package = "chromVAR")'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] BSgenome.Hsapiens.UCSC.hg19: human genome sequence reference required for GC bias and motif matching: 'library(BSgenome.Hsapiens.UCSC.hg19)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] chromVARDeviations object: RangedSummarizedExperiment with two assays (deviations and deviationScores) containing bias-corrected accessibility deviations and Z-scores for each motif (rows) and sample (columns): 'The output from the computeDeviations function is a chromVARDeviations object. This object inherits from the RangedSummarizedExperiment object'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Deviations matrix: numeric matrix of bias-corrected deviations in accessibility for each motif-sample pair, accessible via deviations(): 'The deviations are the bias corrected deviations in accessibility. For each motif or annotation (rows), there is a value for each cell or sample (columns)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] DeviationScores matrix: numeric matrix of Z-scores for bias-corrected deviations, accessible via deviationScores(): 'The deviationScores are the Z-scores for each bias corrected deviations.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] chromVAR: 'chromVAR is an R package for the analysis of sparse chromatin accessibility'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R: 'An R package for the analysis of sparse chromatin accessibility'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] motifmatchr: 'library(motifmatchr)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] SummarizedExperiment: 'library(SummarizedExperiment)'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Matrix: 'library(Matrix)'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] BiocParallel: 'library(BiocParallel)'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] BSgenome.Hsapiens.UCSC.hg19: 'library(BSgenome.Hsapiens.UCSC.hg19)'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: '_No changelog found._'
