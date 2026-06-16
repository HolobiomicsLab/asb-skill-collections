# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How does the doAnalysis function process a SummarizedExperiment object to identify outliers and mis-injections, and what corrected assay does it produce?: 'The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio. Furthermore, Study Samples are tested for mis-injections'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] doAnalysis with parameters removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 tests QC samples for outliers using Compound/Internal Standard ratio, tests Study Samples for mis-injections using Internal Standard areas, and produces a ratio_corrected assay in the output experiment.: 'exp <- doAnalysis(
    exp = exp, 
    removeOutliers = TRUE, 
    useWithinBatch = TRUE, 
    removeBadCompounds = TRUE,
    qcPercentage = 80,
    backgroundPercentage = 40,
    nonReportableRSD ='

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] SummarizedExperiment object with raw compound area and internal standard area assays, sample metadata (type, batch, injection_time), and compound annotations: 'The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] SummarizedExperiment object with 'ratio_corrected' assay containing batch-corrected Compound/Internal Standard ratios: 'batch-correction using pooled study quality control samples (SQC)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Outlier annotations on QC samples flagged by Compound/Internal Standard ratio analysis: 'The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mis-injection annotations on study samples identified via Internal Standard area thresholds: 'Furthermore, Study Samples are tested for mis-injections using their Internal Standard areas.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Optional: absolute concentration values calculated via linear regression for compounds in calibration samples with known spike concentrations: 'mzQuality can calculate absolute concentrations by using calibration line samples and known concentrations for spiked compounds.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] mzQuality: 'mzQuality requires a specific format for the input data.'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'library(mzQuality)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] SummarizedExperiment: 'Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data.'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, bug fixes, or parameter changes to doAnalysis function: '_No changelog found._'
