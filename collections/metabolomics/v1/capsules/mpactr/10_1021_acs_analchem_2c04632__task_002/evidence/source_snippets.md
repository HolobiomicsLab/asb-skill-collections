# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] What is the structure and content of the data.table returned by qc_summary() when applied to a fully-filtered mpactr object?: 'A data.table reporting the compound id (`compounds`) and if it failed or passed filtering. If the ion failed filtering, its status will report the name of the filter it failed.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The qc_summary() function returns a data.table with compound IDs and filtering status for each ion, where passing ions are marked as passed and failing ions report the name of the filter they failed.: 'A data.table reporting the compound id (`compounds`) and if it failed or passed filtering. If the ion failed filtering, its status will report the name of the filter it failed.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] cultures_peak_table.csv — Progenesis-format peak table with columns: compound, m/z, retention time (min), raw abundance for each sample injection: 'import_data(example_path("cultures_peak_table.csv"), example_path("cultures_metadata.csv"), format = "Progenesis")'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] cultures_metadata.csv — sample metadata table with columns: Injection, Sample_Code, Biological_Group (minimum required); example contains solvent blanks, media blanks, and biological replicates: 'example_path("cultures_metadata.csv")'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] qc_summary data.table with rows corresponding to input compounds and columns: compound ID, status (indicating which filter each ion failed or if the ion passed all applied filters): 'This function returns a `data.table` reporting the ion status for each input ion. This includes which filter each ion failed or passed, or if the ion passed all applied filters.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] mpactr: 'library(mpactr)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'This table can be used for a variety of analyses that can be conducted in R'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] data.table: 'library(data.table)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: 'No changelog found.'
