# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] How does tximport process transcript-level quantification files from tximportData to produce a gene-level count matrix suitable for DESeqDataSetFromTximport?: 'you could import the data with *tximport*, which produces a list, and then you can use `DESeqDataSetFromTximport()`'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] tximport ingests transcript-level quantification files and produces a list object that contains un-normalized counts aggregated to the gene level, which serves as input to DESeqDataSetFromTximport for constructing a DESeqDataSet.: 'you could import the data with *tximport*, which produces a list, and then you can use `DESeqDataSetFromTximport()`'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Sample metadata table from tximportData package (samples.txt with run IDs, population, center, and condition information): 'samples <- read.table(file.path(dir,"samples.txt"), header=TRUE)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Salmon quant.sf.gz quantification files for each sample: 'files <- file.path(dir,"salmon", samples$run, "quant.sf.gz")'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Transcript-to-gene mapping table (tx2gene.gencode.v27.csv): 'tx2gene <- read_csv(file.path(dir, "tx2gene.gencode.v27.csv"))'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Gene-level count matrix (txi list object) containing un-normalized estimated gene counts, transcript lengths, and abundance-weighted library size offsets: 'txi <- tximport(files, type="salmon", tx2gene=tx2gene)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] DESeqDataSet object (ddsTxi) with gene-level counts, sample metadata, and design formula ready for differential expression analysis: 'ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] tximport: 'txi <- tximport(files, type="salmon", tx2gene=tx2gene)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] DESeq2: 'library("DESeq2") ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Salmon: 'files <- file.path(dir,"salmon", samples$run, "quant.sf.gz")'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] tximportData: 'library("tximportData") dir <- system.file("extdata", package="tximportData")'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] readr: 'library("readr") tx2gene <- read_csv(file.path(dir, "tx2gene.gencode.v27.csv"))'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, updates, or reproducibility artifacts for the tximportData package: 'No changelog found.'
