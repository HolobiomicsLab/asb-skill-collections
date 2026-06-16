# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How does edgeR::DGEListFromTximport with divide=TRUE process tximport inferential replicates to generate transcript-level divided counts for differential expression analysis?: 'If the `tximport` output contains inferential replicates, then `DGEListFromTximport` will also estimate the count overdispersion that arises from the fact that reads have to assigned to transcripts'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] DGEListFromTximport with divide=TRUE estimates count overdispersion from inferential replicates and produces divided counts suitable for transcript-level differential expression analysis, accounting for the probabilistic assignment of reads to transcripts.: 'If the `tximport` output contains inferential replicates, then `DGEListFromTximport` will also estimate the count overdispersion that arises from the fact that reads have to assigned to transcripts'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] tximportData salmon_gibbs files with Gibbs sample replicates and transcript-level abundance estimates: 'Using a tximport output that includes inferential replicates (salmon_gibbs files from tximportData) with txOut=TRUE'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] DGEList object with divided transcript-level counts, library size normalization factors, and overdispersion estimates: 'call edgeR::DGEListFromTximport with divide=TRUE to produce a DGEList containing divided counts suitable for transcript-level differential expression'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Verification report confirming DGEList structure integrity and presence of count overdispersion estimates: 'Verify the DGEList structure and presence of count overdispersion estimates'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] tximport: 'Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] edgeR: 'use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] salmon: 'tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history is documented for the tximport package or its integration with edgeR::DGEListFromTximport: '_No changelog found._'
