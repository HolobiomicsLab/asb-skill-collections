# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What are the True Positive Rate and False Positive Rate values at threshold 0.01 when applying the default NeatMS model under full training conditions?: '**NeatMS** enables automated filtering of false positive MS<sup>1</sup> peaks reported by commonly used LCMS data processing pipelines.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] NeatMS relies on neural network based classification to distinguish true from false positive peaks in untargeted LCMS data.: '**NeatMS** relies on neural network based classification.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Trained NeatMS neural network model file (default model or custom .h5 file): 'Calling the method `get_threshold()` will compute and return the optimal threshold using the validation set that you can then pass everytime you use this neural network.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Validation dataset attached to the NN_handler instance (peaks remain untouched from training/test split): 'The validation set remains untouch and is used later on for hyperparameter tuning.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Recall table (DataFrame) with columns Probability_threshold, True, False, False_low, False_noise, indexed by probability threshold from 0.00 to 0.99: 'Internaly, `get_threshold` call the method `get_true_vs_false_positive_df(label='High_quality')` which returns the following table: | Probablity_threshold | True | False | False_low | False_noise |'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Extracted metrics at threshold 0.01: True Positive Rate = 1.0, False Positive Rate = 0.440, False_low = 0.803, False_noise = 0.206: 'if we were to select a `0.01` threshold, 100% of `High_quality` peaks would be correctly predicted but we would have 44% of false positive (80% of `Low_quality`, and 20% of `Noise` peaks would be'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] NeatMS: 'Calling the method `get_threshold()` will compute and return the optimal threshold'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Python: '# Import the required libraries first
import numpy as np'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] pandas: 'import pandas as pd'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] NumPy: 'import numpy as np'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] scikit-learn: 'from sklearn.metrics import auc'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, modifications, or release notes for the NeatMS package: 'No changelog found.'
