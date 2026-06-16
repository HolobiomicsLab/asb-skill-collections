# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What is the sequence of operations in the MS2 library compilation pipeline for loading, completing metadata, assigning chemical structures, separating by ionization polarity, and writing polarity-specific MSP files?: 'compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The mspcompiler system processes MS2 libraries through a sequence of steps: loading libraries from NIST, MoNA, GNPS, or RIKEN sources via read_lib; completing MGF metadata through complete_mgf; assigning SMILES structures via assign_smiles; separating positive and negative ionization modes via separate_polarity; and writing polarity-separated MSP files via write_MS2_msp for use in MS-DIAL.: 'compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] NIST MS2 library MSP file (NIST_msms.MSP): 'nist_ms2 <- read_lib("D:/MS_libraries/NIST_msms.MSP", type = "MS2")'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] NIST MS2 MOL directory containing structure files (NIST_msms.MOL): 'combine_mol2sdf("D:/MS_libraries/NIST_msms.MOL", "D:/MS_libraries/nist_msms.sdf")'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] RIKEN MS2 positive mode library (MSMS-Public-Pos-VS15.msp): 'riken_ms2_pos <- read_lib("D:/MS_libraries/MSMS-Public-Pos-VS15.msp")'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] RIKEN MS2 negative mode library (MSMS-Public-Neg-VS15.msp): 'riken_ms2_neg <- read_lib("D:/MS_libraries/MSMS-Public-Neg-VS15.msp")'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] MoNA MS2 positive mode library (MoNA-export-LC-MS-MS_Positive_Mode.msp): 'mona_ms2_pos <- read_lib("D:/MS_libraries/MoNA-export-LC-MS-MS_Positive_Mode.msp")'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] MoNA MS2 negative mode library (MoNA-export-LC-MS-MS_Negitive_Mode.msp): 'mona_ms2_neg <- read_lib("D:/MS_libraries/MoNA-export-LC-MS-MS_Negitive_Mode.msp")'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] GNPS library in MGF format (ALL_GNPS.mgf): 'gnps <- read_lib("D:/MS_libraries/ALL_GNPS.mgf", format = "mgf")'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Combined MS2 positive mode library in MSP format (combine_ms2_pos.msp): 'write_MS2_msp(combine_ms2_pos, "/D:MS_libraries/combine_ms2_pos.msp")'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Combined MS2 negative mode library in MSP format (combine_ms2_neg.msp): 'write_MS2_msp(combine_ms2_neg, "/D:MS_libraries/combine_ms2_neg.msp")'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] mspcompiler: 'library(mspcompiler)'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] R: 'library(mspcompiler)'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] future: 'library(future)'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] future.apply: 'library(future.apply)'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] parallel: 'library(parallel)'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] NIST: 'The NIST MS2 library can be treated as the same as the NIST EI library'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] RIKEN: 'The RIKEN MS2 libraries can be download from the MS-DIAL homepage'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] MoNA: 'The MoNA MS2 libraries can be downloaded from https://mona.fiehnlab.ucdavis.edu/downloads'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] GNPS: 'The GNPS library can be download from https://gnps.ucsd.edu/ProteoSAFe/libraries.jsp'

## ev_021

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] MS-DIAL: 'both positive and negative modes are in a single file as well. Therefore, we need to separated the polarity'

## ev_022

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history available to document updates, bug fixes, or feature changes to the MS2 pipeline components.: 'No changelog found.'
