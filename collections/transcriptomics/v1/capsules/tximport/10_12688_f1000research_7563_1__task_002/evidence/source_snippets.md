# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Do transcript-level estimates obtained via tximport with txOut=TRUE produce identical gene-level count matrices after summarization with summarizeToGene as compared to direct gene-level import using txOut=FALSE?: 'These matrices can then be summarized afterwards using the function `summarizeToGene`. This then gives the identical list of matrices as using `txOut=FALSE` (default) in the first `tximport` call.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Gene-level count matrices derived from transcript-level tximport output (txOut=TRUE) followed by summarizeToGene are identical to those produced by direct gene-level tximport (txOut=FALSE), as verified by all.equal() comparison.: 'all.equal(txi$counts, txi.sum$counts)'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Salmon quantification output files (quant.sf) from tximportData package: 'tximportData salmon files'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Transcript-to-gene mapping data.frame (tx2gene) with transcript IDs and corresponding gene IDs: 'Transcripts need to be associated with gene IDs for gene-level summarization'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Gene-level count matrix from two-step workflow (transcript import + summarizeToGene): 'resulting count matrix is identical to a direct tximport call'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Gene-level count matrix from direct single-step import (txOut=FALSE): 'direct tximport call with txOut=FALSE'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Boolean confirmation that both matrices are identical: 'verify the resulting count matrix is identical'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] tximport: 'Importing transcript abundance with tximport'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] readr: 'significantly faster to read in files using the readr package'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history provided for tximport package or source repository: '_No changelog found._'
