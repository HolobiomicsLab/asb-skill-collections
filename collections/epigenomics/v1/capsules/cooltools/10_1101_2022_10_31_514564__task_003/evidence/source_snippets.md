# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What is the format and valid range of insulation scores produced by cooltools.insulation when applied to Hi-C cooler files?: 'The recently-introduced cooler format readily handles storage of high-resolution datasets'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Cooltools provides computational tools for analyzing high-resolution Hi-C datasets stored in the cooler format, enabling extraction of quantitative genomic features.: 'tools for your .cools'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Public cooler file (.cool format) from deposited Hi-C dataset: 'the recently-introduced cooler format readily handles storage of high-resolution datasets'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Window size parameter for insulation score calculation (e.g., 100 kb or 1 Mb): 'The new cooltools.insulation method includes a thresholding step to detect strong boundaries, using either the Li or the Otsu method'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Optional genomic view dataframe (view_df) to restrict analysis to specific regions: 'Most functions now take an optional view_df argument. A pandas dataframe defining a genomic view can be provided to limit the analyses to regions included in the view.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Insulation score table (TSV or CSV) with columns: region1, region2, insulation_score, is_boundary_{window}, and associated metadata: 'The result of thresholding for each window size is stored as a boolean in a new column is_boundary_{window}.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] BED-format file of annotated insulating boundaries with genomic coordinates and boundary scores: 'cooltools.insulation for insulation score and annotation of insulating boundaries'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] cooler: 'the recently-introduced cooler format readily handles storage of high-resolution datasets'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'enabling high-resolution Hi-C analysis in Python'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] New functionality for smoothing P(s) and derivatives has an API that is not yet stable: 'New functionality for smoothing P(s) and derivatives (API is not yet stable)'
