# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What is the orchestrated sequence of operations for compiling EI mass spectral libraries from multiple sources (NIST, MoNA, RIKEN, SWGDRUG) into a single MSP file in mspcompiler?: 'compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The mspcompiler EI pipeline loads libraries via read_lib or read_multilibs, assigns SMILES structures via assign_smiles, assigns Kovats retention indices via assign_ri, combines the processed libraries, and writes the consolidated result to a single MSP file via write_EI_msp for use in MS-DIAL.: 'compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NIST EI library MSP file exported from Lib2NIST: 'Once you have the \*.MSP file and the correspondent \*.MOL folder exported'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NIST.MOL folder containing MOL structure files corresponding to NIST library: 'Once you have the \*.MSP file and the correspondent \*.MOL folder exported'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] RIKEN EI library MSP file with Kovats RI: 'Please download "All records with Kovats RI...EI-MS..." As it contains Kovats RI'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MoNA GC-MS Spectra MSP file: 'Please download "GC-MS Spectra" in "MSP" form'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] SWGDRUG EI library NIST format (converted to MSP via Lib2NIST) and Agilent format (converted to MOL folder): 'please download both **NIST Format** and **Agilent Format**. Then use *Lib2NIST* to convert'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NIST ri.dat and USER.DBU files containing experimental RI data: 'Extract experimental RI from the "ri.dat" and "USER.DBU" files. Once you have NIST library installed, these files can be found in, for example, "~/Programs/nist14/mssearch/nist_ri"'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Combined EI mass spectral library MSP file containing merged records from all four source libraries with SMILES and Kovats RI annotations: 'write_EI_msp(combine_ei, "/D:MS_libraries/combine_ei.msp")'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] mspcompiler: 'library(mspcompiler)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'library(mspcompiler)'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] future: 'library(future)'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] future.apply: 'library(future.apply)'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] parallel: 'library(parallel)'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Lib2NIST: 'you can transformed it into a msp file by *Lib2NIST*'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MS-DIAL: 'MS-DIAL friendly msp file'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NIST: 'NIST is the most commonly used **commercial** EI library'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MoNA: 'The MassBank of North America (MoNA) has an EI library available'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] RIKEN: 'The MS-DIAL developers have compiled an EI library with Kovat RI included'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: 'No changelog found.'
