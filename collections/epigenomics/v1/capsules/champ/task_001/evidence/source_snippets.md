# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Do champ.load() and champ.import() correctly load the expected numbers of probes before filtering for the HumanMethylation450 and EPIC array types?: 'for 450k bead array data, before filtering for low quality probes, the dataset will include 485,512 probes. And for EPIC bead array data, before filtering probes the dataset, will include 867,531'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] The ChAMP loading functions should return 485,512 probes for 450K arrays and 867,531 probes for EPIC arrays before any quality-based filtering is applied.: 'for 450k bead array data, before filtering for low quality probes, the dataset will include 485,512 probes. And for EPIC bead array data, before filtering probes the dataset, will include 867,531'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] HumanMethylation450 test dataset (450K lung tumor data: 8 samples, 4 tumor + 4 control): 'The 450k lung tumor data set contains only 8 samples, 4 lung tumor samples (T) and 4 control samples (C)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] EPICSimData test dataset: 'For the EPIC Simulation Data Set, user may use following code to load it: data(EPICSimData)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Loaded 450K dataset object with pre-filter probe count of 485,512 probes: 'ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Loaded EPIC dataset object with pre-filter probe count of 867,531 probes: 'ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] ChAMP: 'ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog provided in document: 'No changelog found.'
