# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does extract_ri extract Kovats retention index values from a NIST ri.dat file, and how does assign_ri then populate those RI values into a compiled EI library object?: 'compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed)'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The mspcompiler workflow includes two sequential operations: extract_ri() to extract experimental RI from NIST files, and assign_ri() to assign experimental RI to the combined library.: 'Extract experimental RI from NIST files'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Compiled EI mass spectral library object in R (e.g., result of read_lib or combined libraries via c() operator): 'After read in and organize all these libraries, we can now combine them into a single file, assign experimental RI'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NIST ri.dat file (retention index database file from NIST installation): 'Extract experimental RI from the "ri.dat" and "USER.DBU" files. Once you have NIST library installed, these files can be found in, for example, "~/Programs/nist14/mssearch/nist_ri"'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NIST USER.DBU file (user database file from NIST installation): 'Extract experimental RI from the "ri.dat" and "USER.DBU" files. Once you have NIST library installed, these files can be found in, for example, "~/Programs/nist14/mssearch/nist_ri"'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] EI library object with RI field populated for each compound based on median experimental RI from capillary columns, excluding records with standard deviation > 30: 'This function will only keep RI records from "capillary" columns and "Lee RI" will be removed. When there are multiple records for a single compound, the median RI will be used and if the standard'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] mspcompiler: 'library(mspcompiler)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'library(mspcompiler)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NIST: 'Extract experimental RI from the "ri.dat" and "USER.DBU" files. Once you have NIST library installed'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history is documented: 'No changelog found.'
