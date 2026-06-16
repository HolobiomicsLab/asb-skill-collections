# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Does calling filter_mispicked_ions() with copy_object=FALSE modify the original named object in place, such that both the original object and a separately assigned result object reflect the same post-filter row count?: 'mpactr is built on an R6 class-system, meaning it operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy,'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Running filter_mispicked_ions with copy_object=FALSE (the default setting) updates the original data object in place: data2 had 1407 ions before filtering, and after assigning the filtered result to data2_mispicked with copy_object=FALSE, both data2_mispicked and the original data2 contain 644 ions, confirming in-place modification rather than creation of independent copies.: 'Running the `filter_mispicked_ions` filter, with default setting `copy_object = FALSE` (operates on reference semantics) results in 644 ions in the feature table. Even though we created an object'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Peak table in Progenesis CSV format (compound, m/z, retention time, raw abundance) and corresponding metadata file with sample information (injection, sample_code, biological_group): 'To export a compatible peak table in Progenesis format is expected. To export a compatible peak table in Progenesis, navigate to the *Review compounds* tab then File -> Export compound Measurements.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Numeric verification that pre-filter and post-filter row counts are identical in both the original object (data2) and the assigned result object (data2_mispicked), demonstrating reference semantics behavior: 'any changes to the original data object, regardless if they are assigned to a new object, result in changes to the original data object'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'This table can be used for a variety of analyses that can be conducted in R'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] mpactr: 'library(mpactr)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] data.table: 'library(data.table)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found.: 'No changelog found.'
