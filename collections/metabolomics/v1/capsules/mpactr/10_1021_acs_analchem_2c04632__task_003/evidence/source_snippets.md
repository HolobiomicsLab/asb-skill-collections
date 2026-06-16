# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How can filtering results from qc_summary() be visualized as a treemap showing the count and percentage of ions in each filter status category?: 'You can visualize filtering results with a tree map using the filtering summary obtained from `qc_summary()` and the packages `ggplot2` and `treemapify`.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Ion counts and percentages by status are computed from qc_summary() output using data.table syntax, then rendered as a treemap with geom_treemap() and geom_treemap_text() to display status labels, ion counts, and percentages; the visualization can be customized with ggplot2 scale_fill_brewer() and theme() functions.: 'ion_counts <- qc_summary(data_filtered)[, .(count = .N), by = status][, percent := (count / sum(count) * 100)]

Finally, we plot the treemap:

tm <- ggplot(ion_counts) +
  aes(area = percent, fill ='

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Filtered mpactr object (data_filtered) containing peak table and filter metadata: 'Overall, `r nrow(get_peak_table(data_filtered))` ions remain in the feature table. A summary of the filtering, as a tree map is below'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] qc_summary() output: data.table with compound IDs and ion status (passed/failed filters): 'This function returns a `data.table` reporting the ion status for each input ion. This includes which filter each ion failed or passed, or if the ion passed all applied filters.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Treemap PNG file showing ion counts and percentages grouped by filter status (mispicked, group, replicability, insource, passed): 'A summary of the filtering, as a tree map is below'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'This table can be used for a variety of analyses that can be conducted in R'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ggplot: 'creating an interactive plot of input features and the filters they failed, if any, using `ggplot` and `plotly`'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] mpactr: 'library(mpactr)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] data.table: 'library(data.table)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: 'No changelog found.'
