# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Can tximport successfully import salmon transcript-level quantification files and produce gene-level counts, abundance, and length matrices using a pre-constructed tx2gene mapping?: 'The tximport package has a single function for importing transcript-level estimates. The `type` argument is used to specify what software was used for estimation. A simple list with matrices,'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] tximport with type='salmon' and a tx2gene mapping produces a list containing gene-level abundance, counts, and length matrices from salmon quant.sf.gz files.: 'library(tximport)
txi <- tximport(files, type="salmon", tx2gene=tx2gene)
names(txi)
head(txi$counts)'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Six salmon quant.sf.gz quantification files from tximportData package: 'Importing transcript abundance with tximport'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] tx2gene.gencode.v27.csv file mapping transcript IDs to gene IDs: 'pre-built tx2gene.gencode.v27.csv'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Gene-level counts matrix (rows: genes, columns: samples): 'A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Gene-level abundance matrix in TPM (rows: genes, columns: samples): 'A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Gene-level length matrix of effective transcript lengths (rows: genes, columns: samples): 'A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] tximport: 'Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] readr: 'While tximport works without any dependencies, it is significantly faster to read in files using the readr package'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history documented for the tximportData package: '_No changelog found._'
