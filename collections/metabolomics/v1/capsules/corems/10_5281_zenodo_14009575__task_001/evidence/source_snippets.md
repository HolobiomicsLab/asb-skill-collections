# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does the CoreMS FT-ICR data processing pipeline (Hanning apodization, log-based noise thresholding, MzDomainCalibration, and SearchMolecularFormulas) successfully assign molecular formulas to ESI_NEG_SRFA.d data with quantified mass error metrics?: 'MSParameters.transient.apodization_method = "Hanning"
MSParameters.transient.number_of_zero_fills = 1
MSParameters.mass_spectrum.noise_threshold_method ='

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The pipeline executes complete molecular formula assignment by applying Hanning apodization with zero-fill, noise thresholding, MzDomainCalibration against SRFA.ref reference data, and SearchMolecularFormulas with CHO constraints, producing assigned peaks with mass error and abundance metrics exportable to CSV.: 'mass_spectrum.to_csv("test")
df = mass_spectrum.to_dataframe()
df.head()'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] ESI_NEG_SRFA.d raw FT-ICR mass spectrometry data file: 'file_location =  "tests/tests_data/ftms/ESI_NEG_SRFA.d"'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] SRFA.ref calibration reference file for mass calibration: 'ref_file_location = 'tests/tests_data/ftms/SRFA.ref''

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] CSV table of assigned molecular formulas with mass error and score fields: 'from corems.encapsulation.factory.parameters import MSParameters'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] CoreMS: 'from corems.encapsulation.factory.parameters import MSParameters'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] pandas: 'import pandas as pd'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] numpy: 'import numpy as np'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: '_No changelog found._'
