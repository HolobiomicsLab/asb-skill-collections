# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] When DESeq2::DESeqDataSetFromTximport is called with a tximport output object (txi) and a sample table, does the resulting DESeqDataSet correctly embed the transcript-length-derived offset matrix needed for gene-level differential expression analysis using the 'original counts and offset' method?: 'The functions `edgeR::DGEListFromTximport`, for *edgeR* and *limma*, and `DESeq2::DESeqDataSetFromTximport`, for *DESeq2*, take care of creation of the offset for you.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] DESeq2::DESeqDataSetFromTximport accepts a tximport list object (containing gene-level counts, abundance, and length matrices) and a sample table, and automatically constructs the appropriate offset matrix from the transcript-length estimates to correct for differential isoform usage, producing a DESeqDataSet ready for differential expression analysis.: 'dds <- DESeqDataSetFromTximport(txi, sampleTable, ~ condition)
# dds is now ready for DESeq()'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] tximport list object (txi) containing transcript-level abundance, estimated counts, and transcript length matrices from salmon quantification: 'tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Sample metadata table with two condition groups for DESeqDataSet construction: 'two-condition sample table'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] DESeqDataSet object with embedded offset matrix derived from transcript length estimates: 'offset matrix is correctly embedded in the resulting object'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] tximport: 'Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] DESeq2: 'use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] salmon: 'tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history is available for the tximport repository: '_No changelog found._'
