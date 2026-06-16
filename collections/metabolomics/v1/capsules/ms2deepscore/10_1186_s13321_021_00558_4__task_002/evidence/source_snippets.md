# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does MS2DeepScore outperform classical spectral similarity measures (modified Cosine) and the unsupervised Spec2Vec method in retrieving chemically related compound pairs from mass spectral datasets?: 'MS2DeepScore clearly outperforms both classical measures (two forms of the modified Cosine) as well as the unsupervised spectral similarity measure Spec2Vec, with respect to identifying high Tanimoto'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] MS2DeepScore demonstrates superior precision and recall across the full range of similarity thresholds compared to modified Cosine and Spec2Vec when identifying structurally related compounds (Tanimoto > 0.6) from the test set of 3601 spectra.: 'MS2DeepScore gives notably better precision/recall combination over the entire range, followed by Spec2Vec and only then modified Cosine'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pretrained MS2DeepScore Siamese network model weights and architecture: 'The fully trained model used to create Fig. 2, 4, 5, 7, 8 can be downloaded from zenodo: https:// zenodo. org/ record/ 46993 56'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Test set spectra (3,601 spectra of 500 unique InChIKeys) with binned peak vectors and structural annotations: 'for the final evaluation on the reserved test set, we used all possible spectrum pairs between the 3601 for the test set (n = 6,485,401 unique spectrum pairs)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Ground-truth Tanimoto scores matrix (500 × 500) computed from RDKit Daylight fingerprints: 'we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities. For every unique 14-character InChIKey the most common InChI was selected (if different'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Spec2Vec and classical spectral similarity baseline predictions on test set pairs: 'The precision/recall plot in Fig. 4 was created by measuring how many pairs with Tanimoto scores above a set threshold were among a subset of all pairs for which the spectral similarity score was >'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Precision-recall curve plot comparing MS2DeepScore, Spec2Vec, and classical spectral similarity methods across Tanimoto score thresholds: 'The precision/recall plot in Fig. 4 was created by measuring how many pairs with Tanimoto scores above a set threshold were among a subset of all pairs for which the spectral similarity score was >'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MS2DeepScore: 'we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] RDKit: 'we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'Our MS2DeepScore Python library offers two types of data generators'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scikit-learn: 'Using the t-SNE [28] implementation from scikit-learn [29]'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No specification of which two baseline scoring methods are used for comparison in precision-recall curves or their exact parameter configurations: 'MS2DeepScore can generally be used to complement -or replace- common currently used spectral similarity measures'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No reporting of computational time or inference speed benchmarks comparing MS2DeepScore to baseline methods on the test set: 'MS2DeepScore is very fast and scalable.'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No discussion of how the Tanimoto threshold parameter affects precision-recall trade-offs or guidance on threshold selection for practical use: 'We demonstrate that the accuracy of the predictions can be improved notably by using various ensemble learning techniques'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No information on model ensemble method details (how many Monte-Carlo Dropout samples, how scores are aggregated, uncertainty filtering thresholds) used during precision-recall evaluation: 'by applying Monte-Carlo Dropout to sample from random model variations'
