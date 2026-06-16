# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How does the blank_masking command filter features from a metabolomics feature table based on the intensity ratio between unknown samples and blank samples?: 'This is achieved by comapring the intensiy of a feature in a specified set of study samples to those in the blanks.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The blank_masking command removes features by comparing feature intensity in study samples (designated by sample_value) to intensity in blanks (designated by blank_value) using a configurable blank_intensity_ratio parameter; features whose intensity in unknown samples is not at least the specified ratio times more than blank samples are dropped.: 'Will drop all features whose intensity in the unknown samples is not at least 3 times more than the blank samples.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Feature table in TSV or CSV format with features as rows and samples as columns, indexed by feature identifier: 'raw feature tables are rarely used for analyses, normalization and blank masking are some of the common processing steps'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Sample metadata CSV file with at minimum sample names and a categorical field (e.g., 'sample_type') designating blank vs. unknown samples: 'Where query_field is the metadata field to search for the given blank_value and sample_value'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Blank-masked feature table in TSV format with low-intensity background features removed, indexed by feature identifier and sample: 'Will drop all features whose intensity in the unknown samples is not at least 3 times more than the blank samples'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'Python-Centric Pipeline for Metabolomics'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog provided to document versions, bug fixes, or implementation details of the blank_masking step.: '_No changelog found._'
