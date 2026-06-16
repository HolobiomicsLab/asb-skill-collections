# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Does the rescore model training script freeze the TCN spectrum encoder and train only the FormulaEncoder and RescoreHead components?: 'The rescore model has been redesigned (Siamese architecture)'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The rescore model has been redesigned with a Siamese architecture in version 2.0.0, indicating a structural change to the model components that would affect encoder freezing and training behavior.: 'The rescore model has been redesigned (Siamese architecture), see details in [CHANGELOG.md](./CHANGELOG.md).'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pre-trained TCN spectrum encoder checkpoint: 'freeze the TCN spectrum encoder'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Training dataset with MS/MS spectra and molecular formula annotations: 'train FormulaEncoder + RescoreHead'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Validation dataset for formula accuracy monitoring: 'formula_acc (with H) improves'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Best model checkpoint containing formula_encoder_state_dict and rescore_head_state_dict: 'output stores formula_encoder_state_dict and rescore_head_state_dict'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Training log recording formula_acc (with H) and loss metrics per epoch: 'formula_acc (with H) improves'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] msfiddle: 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No explicit specification of the required input data format, expected file paths, or configuration file schema for train_rescore.py: '`train_rescore.py`: Siamese rescore trainer. Freezes the TCN spectrum encoder; trains `FormulaEncoder` + `RescoreHead` with BCE loss.'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No documentation of the expected hyperparameters (learning rate, batch size, number of epochs, optimizer type) for train_rescore.py: '`train_rescore.py`: Siamese rescore trainer. Freezes the TCN spectrum encoder; trains `FormulaEncoder` + `RescoreHead` with BCE loss.'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No specification of the exact structure or naming convention of checkpoint files or the directory where checkpoints are saved: 'Checkpoint stores `formula_encoder_state_dict` and `rescore_head_state_dict`.'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No definition of what constitutes an 'improvement' in formula_acc (with H) or the baseline/tolerance threshold for checkpoint saving: 'checkpoint saved only when `formula_acc` (with H) improves.'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No details on the data pipeline, required preprocessing steps, or data format expected by train_rescore.py before execution: '`prepare_augment_rescore.py`: unified rescore data preparation script.'
