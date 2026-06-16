# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] When champ.DMR() is applied to the EPIC simulation dataset using bumphunter-based detection, how many differentially methylated regions are identified?: 'In this 16 sample dataset, we simulated 8 samples are control and 8 sample as case, samples are marked in pd of EPICSimData object. In this data, we randomly choose 5000 regions from clusterMaker()'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] The EPIC simulation dataset contains fewer than 5000 DMRs (approximately 4700+) because some simulated DMRs contain only 1-2 CpGs, which are not regarded as DMRs in champ.DMR() function.: 'So there should have less than 5000 DMRs (4700+) in this data set, because some simulated DMRs contains only 1-2 CpGs, they will not be regarded as DMR in champ.DMR() function.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] EPICSimData (EPIC simulation dataset): 'For the EPIC Simulation Data Set, user may use following code to load it: data(EPICSimData)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] DMR detection results table with genomic coordinates and statistical metrics: 'For the identification of Differentially Methylated Regions (DMRs), ChAMP offers the new Probe Lasso method, in addition to previous DMR detection functions Bumphunter and DMRcate'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] DMR count (integer, expected ~4700+): 'For the identification of Differentially Methylated Regions (DMRs), ChAMP offers the new Probe Lasso method, in addition to previous DMR detection functions Bumphunter and DMRcate'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] ChAMP: 'ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Bumphunter: 'previous DMR detection functions Bumphunter and DMRcate'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version-specific reproducibility notes found in the discussion section: 'No changelog found.'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact expected DMR count threshold or reference value for bumphunter-based EPIC simulation is not stated in the provided document sections: 'No changelog found.'
