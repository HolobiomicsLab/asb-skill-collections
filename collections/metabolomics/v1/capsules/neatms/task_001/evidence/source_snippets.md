# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Does applying NeatMS default preprocessing to example mzML and feature-table inputs produce a peak matrix with the documented result_matrix_shape dimensions?: 'The source code and related materials (e.g. tutorials, example data, neural network model) are available at [https://github.com/bihealth/NeatMS](https://github.com/bihealth/NeatMS).'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] NeatMS is an open source python package for untargeted LCMS signal labelling and filtering that enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: '**NeatMS** is an open source python package for untargeted LCMS signal labelling and filtering. **NeatMS** enables automated filtering of false positive MS<sup>1</sup> peaks reported by commonly used'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Raw LC-MS data in mzML format from NeatMS example data (github.com/bihealth/NeatMS/data folder): 'Raw data files in mzML format'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Feature table in CSV format exported from mzMine or XCMS (github.com/bihealth/NeatMS/data/test_data folder): 'One feature table file in .csv format'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Peak matrix arrays with shape (2, 120) per peak, where dimension 0 encodes signal intensity and dimension 1 encodes binary margin/peak classification: 'The resulting matrix size for one peak is therefore (2, 120)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Verification report confirming first and last 40 values represent signal margins (value 0) and middle 40 values represent peak signal (value 1): 'the first and last 40 values of the peak will represent the margins (surrounding signal), the middle 40 values represent the peak itself'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Batch split statistics (training, test, validation sample counts) matching 80:10:10 default split: 'By default, the split between training:test:validation batches is 80:10:10'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] NeatMS: 'NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Python: 'After installation, you should be able to import NeatMS'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] NumPy: 'import numpy as np'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] pandas: 'import pandas as pd'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history provided: 'No changelog found.'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Location and format of documented result_matrix_shape artifact not specified in provided text: 'No changelog found.'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Expected peak matrix shape dimensions (rows, columns) and data type not documented in provided section: 'No changelog found.'
