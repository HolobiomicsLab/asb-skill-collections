# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What are the input and output specifications for the cooltools.saddle function when applied to binned eigenvector track data from a cooler Hi-C matrix file?: 'The recently-introduced cooler format readily handles storage of high-resolution datasets'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Cooltools provides saddle analysis functionality as part of its high-resolution Hi-C analysis toolkit, operating on cooler-format datasets that store high-resolution contact matrices and associated genomic tracks.: 'The recently-introduced cooler format readily handles storage of high-resolution datasets via a'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Cooler file (.cool) containing balanced Hi-C contact matrix: 'The recently-introduced cooler format readily handles storage of high-resolution datasets via a sparse data model.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Eigenvector track (pandas DataFrame or BED-like file) from prior eigs_cis or eigs_trans calculation: 'Shouldn't affect the results when using eigenvectors calculated from the same data.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] NPZ file containing untransformed saddledata matrix indexed by digitized compartment bins: 'compute-saddle now saves saddledata without transformation, and the scale argument (with options log or linear) now only determines how the saddle is plotted.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Saddle strength scalar (float) quantifying compartment interaction asymmetry: 'Make saddle strength work with NaNs'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] cooltools: 'cooltools leverages this format to enable flexible and reproducible analysis of high-resolution data.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] cooler: 'The recently-introduced cooler format readily handles storage of high-resolution datasets via a sparse data model.'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'enabling high-resolution Hi-C analysis in Python'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] API stability status and exact output format (NPZ structure, field names, metadata) for cooltools.saddle function and compute-saddle CLI: 'New functionality for smoothing P(s) and derivatives (API is not yet stable)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Whether digitize and saddle handle NaN values in eigenvector tracks and cooler matrices, and whether mask_bad_bins is automatically applied during compute-saddle execution: 'Make saddle strength work with NaNs'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact cooler file format version, resolution, and reference organism/assembly required as input to saddle computation: 'Upgrade bioframe dependency'
