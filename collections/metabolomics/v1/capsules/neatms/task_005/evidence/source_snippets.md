# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Does training the NeatMS CNN model from scratch on the provided example dataset under full training conditions produce an AUC ROC score exceeding 0.9 without evidence of overfitting?: 'When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class).'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: '**NeatMS** relies on neural network based classification.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Raw LC-MS data in mzML format: 'Raw data files in mzML format.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Feature table in CSV format (mzMine or XCMS aligned/unaligned peaks): 'One feature table file in .csv format (multiple if peaks are not aligned).'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] NeatMS example dataset (raw_data_folder_path and feature_table_path): 'Now that you feel confident with neural network training, let's dive in and prepare our batches.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Trained neural network model file (HDF5 format): 'nn_handler.class_model.save('my_own_model_020.h5')'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] AUC ROC score (numeric value ≥ 0.95): 'If correctly trained, you should obtain an AUC higher than 95.0.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] ROC curve plot (PNG or similar): 'prob_df_roc.plot(x='False', y='True', figsize=(10,10), grid=True)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Training and validation accuracy curves (matplotlib figure): 'when you see no increase in the accuracy of the training and test set, you can stop the training.'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] NeatMS: 'NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'open source python package'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] TensorFlow: 'calling the training method (1000 by default). NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Keras: 'from keras.optimizers import SGD, Adam'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] scikit-learn: 'from sklearn.metrics import auc'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] pandas: 'import pandas as pd'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] NumPy: 'import numpy as np'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Jupyter Notebook: 'You can install them through the pip command

`pip install notebook dash jupyter-dash`'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: 'No changelog found.'
