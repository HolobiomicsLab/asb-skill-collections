# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Can tximport successfully import transcript-level quantification data from oarfish-quantified long-read RNA-seq samples using the type='oarfish' parameter with txOut=TRUE to produce transcript-level matrices?: 'Long read data quantified with *oarfish* can be imported using *tximport*. The following example shows import of three samples from SG-Nex.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] tximport with type='oarfish' and txOut=TRUE successfully imports transcript-level abundance, count, and length matrices from oarfish quant.gz files for SG-Nex replicates, as demonstrated with three samples (sgnex_rep2, sgnex_rep3, sgnex_rep4) from the tximportData package.: 'files <- file.path(dir,"oarfish", 
  paste0(sgnex_file, "_rep", 2:4, ".quant.gz")
) 
names(files) <- paste0("sgnex-rep",2:4)
txi.oar <- tximport(files, type="oarfish", txOut=TRUE)'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Three SG-Nex oarfish quant.gz files from tximportData package: 'oarfish quant.gz files for three SG-Nex replicates from the tximportData package'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Transcript-level abundance matrix (3 samples × transcripts): 'produce transcript-level abundance, count, and length matrices'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Transcript-level count matrix (3 samples × transcripts): 'produce transcript-level abundance, count, and length matrices'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Transcript-level length matrix (3 samples × transcripts): 'produce transcript-level abundance, count, and length matrices'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] tximport: 'Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, bug fixes, or feature updates for tximport package: '_No changelog found._'
