# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] What are the prediction correlation metrics achieved by a MiMeNet model trained on the full IBD (PRISM) dataset when evaluated on the held-out IBD (External) dataset?: 'Even though there was a decrease in overall correlations as expected, we show that MiMeNet can still predict the metabolomic profiles when using smaller sets of training data.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] When training using the entire IBD (PRISM) dataset to predict the IBD (External) test set, MiMeNet identified 308 well-predicted metabolites while MelonnPan identified 186, with mean correlation increased from 0.168 to 0.275 for annotated metabolites.: 'When training using the entire IBD (PRISM) dataset to predict the IBD (External) dataset, MiMeNet identified 308 well-predicted metabolites while MelonnPan identified 186, of which 160 were also'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] IBD (PRISM) microbiome abundance data (201 microbial species, 121 IBD patients + 34 controls): 'A total of 201 microbial species and 8848 metabolites were identified for the IBD (PRISM) and IBD (External) datasets'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] IBD (PRISM) metabolome abundance data (8848 metabolites, 121 IBD patients + 34 controls): 'A total of 201 microbial species and 8848 metabolites were identified for the IBD (PRISM) and IBD (External) datasets'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] IBD (External) microbiome abundance data (two cohorts: 20 healthy subjects from LifeLines-DEEP + 43 subjects from Groningen): 'includes an external validation dataset using two other cohorts. One consists of 20 healthy subjects who participated in LifeLines-DEEP, a general population-based study in the northern Netherlands'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] IBD (External) metabolome abundance data (paired with external microbiome cohorts): 'A total of 201 microbial species and 8848 metabolites were identified for the IBD (PRISM) and IBD (External) datasets'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mean Spearman correlation coefficients (SCC) for metabolite prediction on IBD (External) dataset: 'the average of the correlations between the predicted and observed values for metabolites was reported'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Count of well-predicted metabolites on IBD (External) dataset (those with SCC above 95th percentile threshold): 'We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Per-metabolite prediction correlations table for IBD (External) evaluation: 'the average of the correlations between the predicted and observed values for metabolites was reported'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Comparison metrics (SCC, prediction accuracy) versus benchmark models (MelonnPan, Random Forest, Elastic Net, WGCNA) on IBD (External) data: 'The evaluation was done by training 100 evaluated on the IBD (External) test set using the area under the receiver operating characteristic curve (AUC)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MiMeNet: 'An MLPNN model is composed of multiple fully connected hidden layers composed of perceptrons'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] neural networks: 'An MLPNN model is composed of multiple fully connected hidden layers'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ADAM optimizer: 'MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MelonnPan: 'MelonnPan was downloaded from https://github.com/biobakery/melonnpan and executed using the given instructions'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Random Forest: 'Random Forest models were implemented using RandomForestRegressor with the default parameter set of 100 tree estimators'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Elastic Net: 'Multivariate Elastic Net models were implemented using ElasticNet and GridSearchCV using 5-fold internal cross-validation'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] WGCNA: 'Weighted correlation network analysis (WGCNA) of microbial features was performed using the WGCNA library in R'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] CCA (Canonical Correlation Analysis): 'Canonical correlation analyses were implemented using CCA with 10, 20, and 40 components'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The specific prediction correlation metric values (mean Spearman correlation coefficients, number of well-predicted metabolites, or per-metabolite correlations) achieved when a model trained on the full IBD (PRISM) dataset is evaluated on the held-out IBD (External) dataset are not explicitly stated in the provided discussion section.: 'Our comparison shows that the MiMeNet model is competitive with the NED model in terms of predictive accuracy and the ability to make well-prediction for a larger set of metabolites'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The exact figure, table, or supplementary material location where external validation results on IBD (External) cohorts are reported is not specified in the provided discussion text.: 'Our comparison shows that the MiMeNet model is competitive with the NED model in terms of predictive accuracy'

## ev_021

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The discussion section does not describe the data preprocessing, normalization, or filtering procedures (e.g., the 10% feature presence threshold mentioned for methods) as applied to the external validation IBD cohorts.: 'Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis of metagenomes and metabolomes could be used'

## ev_022

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No statement is provided regarding the handling of missing data, feature alignment, or batch correction between the IBD (PRISM) training cohort and the two external IBD (External) validation cohorts.: 'The predictive model in MiMeNet distinguishes it from MelonnPan [26], which uses a regularized linear regression to model each metabolite separately'
