# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does applying Monte-Carlo Dropout ensemble filtering (IQR < 0.025) to MS2DeepScore predictions significantly reduce root mean squared error across different Tanimoto score ranges, particularly in low (< 0.4) and high (> 0.8) bins?: 'For instance, all predictions within IQR < 0.025—which will discard about 75% of the scores—will result in a drop of the average RMSE from about 0.17 to about 0.11 (Fig. 7A). It is important to note,'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement) with most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges, while slightly increasing error in the mid score range (0.5–0.7).: 'all predictions within IQR < 0.025—which will discard about 75% of the scores—will result in a drop of the average RMSE from about 0.17 to about 0.11 (Fig. 7A). The RMSE drops most significantly in'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Trained MS2DeepScore base network model (200-dimensional embedding layer) and test-set spectrum pair labels from Zenodo deposit zenodo.org/record/4699356: 'The fully trained model used to create Fig. 2, 4, 5, 7, 8 can be downloaded from zenodo'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Test set of 3,601 spectra with 500 unique InChIKeys and corresponding reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits): 'For the final evaluation on the reserved test set, we used all possible spectrum pairs between the 3601 for the test set (n = 6,485,401 unique spectrum pairs)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Per-Tanimoto-bin RMSE table (10 bins from 0.0–1.0) before uncertainty filtering, showing RMSE values for each bin across all 6,485,401 test pairs: 'MS2DeepScore generally performs very well and can predict Tanimoto scores between 0.1 and 0.9 with a RMSE between 0.13 and 0.2'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Per-Tanimoto-bin RMSE table (10 bins from 0.0–1.0) after IQR < 0.025 filtering, showing RMSE reduction and pair count per bin: 'filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Summary comparison figure or table showing RMSE values and improvements (unfiltered vs. IQR-filtered) for low (< 0.4) and high (> 0.7) Tanimoto bins, matching reported findings: 'we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MS2DeepScore: 'Our MS2DeepScore Python library offers two types of data generators'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'Our MS2DeepScore Python library offers two types of data generators'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Monte-Carlo Dropout: 'To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles [17]. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] RDKit: 'we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scikit-learn: 'Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No specification of the number of Monte-Carlo Dropout iterations or ensemble size for uncertainty quantification: 'by applying Monte-Carlo Dropout to sample from random model variations'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No definition of IQR filtering threshold or justification for the specific cutoff value used: 'by merging predicted scores of spectra belonging to the same compound pair or by applying Monte-Carlo Dropout'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No quantitative RMSE results reported in discussion; claims about accuracy improvement lack specific numerical values: 'the accuracy of the predictions can be improved notably by using various ensemble learning techniques'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No information on which specific Tanimoto score bins (e.g., low < 0.4, high > 0.7) show the most improvement: 'The accuracy of the predictions can be improved notably by using various ensemble learning techniques'
