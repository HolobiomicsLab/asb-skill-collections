# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Does setting copy_object=FALSE in filter_mispicked_ions() cause the original data object to be modified in-place, whereas copy_object=TRUE preserves the original object's state?: 'Running the `filter_mispicked_ions` filter, with default setting `copy_object = FALSE` (operates on reference semantics) results in changes to the original `data2` object'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] When filter_mispicked_ions() is called with copy_object=FALSE, the original data object is updated in-place; the raw data object with 7269 ions was reduced to 6625 ions, and the original data2 object was also updated despite assigning the result to a new variable data2_mispicked.: 'Even though we created an object called `data2_mispicked`, the original `data2` object was also updated and now has `r nrow(get_peak_table(data2))` ions in the feature table'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] cultures_peak_table.csv: 'import_data(example_path("cultures_peak_table.csv"'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] cultures_metadata.csv: 'example_path("cultures_metadata.csv")'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Comparison table (data.frame or data.table) with rows for copy_object=FALSE and copy_object=TRUE, columns: condition, original_object_rowcount, assigned_object_rowcount, object_identity_match: 'operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory,'

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

[discussion] No changelog found: 'No changelog found.'
