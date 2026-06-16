# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] What is the structure and content of the output returned by filter_summary() when applied to a filtered mpactr object with the 'mispicked' filter?: 'If you are interested in viewing the passing and failing ions for a single filter, use the `filter_summary()` function.  You must specify which filter you are interested in, either "mispicked",'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] filter_summary() returns a named list containing two components: failed_ions and passed_ions, both of which can be displayed as data tables using head() to view a subset of ions.: 'Failed ions: 
```{r}
head(mispicked_summary$failed_ions, 100)
```

Passing ions:
```{r}
head(mispicked_summary$passed_ions, 100)
```'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] A filtered mpactr R6 object that has undergone filter_mispicked_ions with merge_peaks=TRUE and merge_method='sum': 'data_filtered <- data |> filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum")'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Data table of ions that failed the mispicked filter (removed or merged due to isotopic pattern misidentification): 'filter_summary(data_mispicked, "mispicked")$failed_ions'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Data table of ions that passed the mispicked filter (retained in feature table): 'filter_summary(data_mispicked, "mispicked")$passed_ions'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'This table can be used for a variety of analyses that can be conducted in R'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] mpactr: 'library(mpactr)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] data.table: 'library(data.table)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting mpactr versions, filter_summary() function signature changes, or expected output schema over time.: 'No changelog found.'
