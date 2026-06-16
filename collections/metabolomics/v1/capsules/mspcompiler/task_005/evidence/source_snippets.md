# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Does configuring the future::plan(multisession) parallel backend before calling read_multilibs on a directory of MSP files successfully spawn multiple worker sessions while producing a merged library object identical to the serial result?: 'No verbatim evidence in provided text'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] The mspcompiler package provides a read_lib() function for reading MSP files into R, and the future and future.apply packages are available as tools for implementing parallel processing workflows.: 'The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Directory containing multiple MSP spectral library files from in-house or batch-processed standards: 'you will have many msp files to combine. The read_multilibs function give you an easy way to read all of them at once. In this case, what you need to input is the folder that contain all these msp'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Merged library R object containing all spectra from input MSP files, ready for downstream enrichment or export: 'read_multilibs("D:/MS_libraries/in_house")'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] mspcompiler: 'library(mspcompiler)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'library(mspcompiler)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] future: 'library(future)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] future.apply: 'library(future.apply)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] parallel: 'library(parallel)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found.: 'No changelog found.'
