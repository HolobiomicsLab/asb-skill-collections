# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Does champ.filter() applied to the HumanMethylation450 test dataset remove probes with detection p-value > 0.01 and probes with fewer than 3 beads in at least 5% of samples?: 'First filter is for probes with detection p-value (default > 0.01). This utilises detection p-value stored in .idat file. Second, ChAMP will filter out probes with <3 beads in at least 5% of samples'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples per probe.: 'First filter is for probes with detection p-value (default > 0.01). This utilises detection p-value stored in .idat file. Second, ChAMP will filter out probes with <3 beads in at least 5% of samples'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] HumanMethylation450 test dataset (450k lung tumor data with 8 samples: 4 tumor, 4 control): 'The 450k lung tumor data set contains only 8 samples, 4 lung tumor samples (T) and 4 control samples (C)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Filtered methylation matrix with low-quality probes removed: 'ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Quality control report documenting probe filtering statistics (detection p-value and bead count thresholds applied): 'provides a pipeline that integrates currently available 450k and EPIC analysis methods'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] ChAMP: 'ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting filter() function behavior or parameter defaults: 'No changelog found.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No methods section provided describing the champ.filter() function implementation or default parameter values: 'Document contains only title metadata and introduction; no methods section present'
