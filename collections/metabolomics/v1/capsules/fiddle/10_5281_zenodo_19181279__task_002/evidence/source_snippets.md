# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What data preparation operations does the prepare_augment_rescore.py script apply to TCN train and test sets before rescore model training?: 'FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The document does not provide explicit details about the prepare_augment_rescore.py script's operations, data augmentation procedures, or rescore training data generation mechanisms within the available text.: 'The rescore model has been redesigned (Siamese architecture), see details in [CHANGELOG.md](./CHANGELOG.md).'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] TCN training dataset (spectra and formula annotations): 'No usage/docs found.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] TCN test dataset (spectra and formula annotations): 'No usage/docs found.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Augmented rescore training set with capped positives, cross-spectrum negatives, and 1:1 ratio: 'No usage/docs found.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Augmented rescore test set with capped positives, cross-spectrum negatives, and 1:1 ratio: 'No usage/docs found.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] msfiddle: 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No specification of the concrete file paths, formats, or availability status of the TCN train and test sets that serve as inputs to prepare_augment_rescore.py: 'Takes the TCN train and test sets directly, runs inference on both, and augments the train split'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No guidance on default or recommended values for --pos_cap, --tolerance (ppm), and --num_workers parameters, nor explanation of parameter sensitivity: 'capping positives per formula (`--pos_cap`), generating cross-spectrum negatives within a precursor m/z window (`--tolerance` ppm), and downsampling to 1:1 positive:negative ratio. Formula refinement'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No explicit definition of how formula refinement is performed or what atoms are included in the extended refinement search space: '`refine_atom_type` is now extended with atoms present in the predicted formula before calling `formula_refinement`'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No quantitative reporting of the augmented dataset statistics (e.g., total row count, distribution of positives/negatives, or average number of negatives generated per positive): 'The test split is saved without augmentation'
