# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does the MS2DeepScore model trained on RDKit Daylight fingerprints achieve the reported prediction accuracy (RMSE ~0.15 without uncertainty filtering, ~0.10 with IQR < 0.025 filtering) when run on the held-out test set of 3,601 spectra from 500 unique compounds?: 'we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] MS2DeepScore predicts Tanimoto scores on the 3,601-spectrum test set with root mean squared error of approximately 0.15 without uncertainty filtering and 0.1 when applying interquartile range (IQR < 0.025) thresholds to remove high-uncertainty predictions.: 'all predictions within IQR < 0.025—which will discard about 75% of the scores—will result in a drop of the average RMSE from about 0.17 to about 0.11'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pre-trained MS2DeepScore model (Daylight Tanimoto condition) with Siamese network weights and architecture specification: 'The fully trained model used to create Fig. 2, 4, 5, 7, 8 can be downloaded from zenodo: https:// zenodo. org/ record/ 46993 56'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Reserved test set: 3,601 preprocessed MS/MS spectra and corresponding ground-truth Tanimoto structural similarity labels (15×15 matrix subset for 500 unique InChIKeys): 'For the final evaluation on the reserved test set, we used all possible spectrum pairs between the 3601 for the test set (n = 6,485,401 unique spectrum pairs).'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GNPS-derived cleaned dataset with metadata including InChIKey, SMILES/InChI, and peak information for test subset: 'The full cleaned dataset (210,407 spectra, 184,698 annotated with InChIKey and SMILES and/or InChI) can be found on zenodo: https:// zenodo. org/ record/ 46993 00'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] RMSE value (single float) comparing predicted Tanimoto scores to ground-truth for full test set (no uncertainty filter), reported as ~0.15: 'we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] RMSE value (single float) comparing predicted Tanimoto scores to ground-truth after filtering with IQR < 0.025 threshold, reported as ~0.10: 'and down to 0.1 with stronger restrictions on model uncertainty'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] CSV table with columns: spectrum_pair_id, spectrum_1_idx, spectrum_2_idx, predicted_tanimoto, ground_truth_tanimoto, prediction_uncertainty_iqr, passed_iqr_filter: 'At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were created from an ensemble of these networks with dropout enabled. This resulted in a'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] MS2DeepScore: 'MS2DeepScore to predict structural similarity scores for spe'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] RDKit: 'we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'Our MS2DeepScore Python library offers two types of data generators'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] matchms: 'Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] Monte-Carlo Dropout: 'different model varieties through Monte-Carlo Dropout is u'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No specification of how many spectrum pairs (total cardinality) were evaluated or whether all possible pairs from 3,601 spectra were tested: 'MS2DeepScore is very fast and scalable. We conclude that this makes MS2DeepScore a powerful novel tool for running large scale comparisons and analy­ses'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No details on inference time, computational requirements (CPU/GPU), or memory footprint needed to run the full test set inference: 'MS2DeepScore is very fast and scalable.'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No confidence intervals, standard deviations, or statistical significance tests reported for the RMSE values (0.15 and 0.10): 'a root mean squared error of about 0.15'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No discussion of failure cases, edge cases where the model performs poorly, or structural similarity ranges where prediction accuracy degrades: 'MS2DeepScore can infer structural similarities between mass spectra with high overall precision, without requiring any additional meta­data or library data.'
