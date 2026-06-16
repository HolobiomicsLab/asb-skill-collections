# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does MiMeNet achieve higher mean Spearman correlation coefficients and identify more well-predicted metabolites compared to MelonnPan, Random Forest, and CCA baselines across IBD (PRISM), Cystic Fibrosis, and Soil datasets using ten iterations of 10-fold cross-validation?: 'we compared the k-fold cross-validated prediction correlations (k = 10, 5, 3, and 2) using the IBD (PRISM) and cystic fibrosis datasets'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] MiMeNet achieves mean Spearman correlation coefficients that increase from 0.108 to 0.309 (IBD PRISM), 0.276 to 0.457 (Cystic Fibrosis), and -0.272 to 0.264 (Soil) compared to MelonnPan, and identifies more well-predicted metabolites: 366 vs 198 (IBD), 143 vs 104 (CF), and 29 vs 4 (Soil).: 'MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264) and identifies more well-predicted'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] IBD (PRISM) microbiome and metabolomic data (121 IBD patients + 34 controls; 201 microbial species, 8848 metabolites): 'This dataset is named as IBD (PRISM). Additionally, it includes an external validation dataset using two other cohorts... A total of 201 microbial species and 8848 metabolites were identified for the'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Cystic Fibrosis lung sputum microbiome and metabolomic data (172 samples; 657 microbial genera, 168 metabolites): 'The second dataset was taken from a study that collected 172 lung sputum samples from patients with cystic fibrosis [31]. Microbial features were generated using 16S rRNA gene sequencing and'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Soil biocrust microbiome and metabolomic data (five time points, four successional stages; 466 microbes, 85 metabolites): 'The third dataset represents microbial and metabolic activity caused by soil wetting at five-time points across four biocrust successional stages [32]. A total of 466 microbes and 85 metabolites were'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] Mean Spearman correlation coefficients (±SD) for MiMeNet and baseline models (Elastic Net, CCA, Random Forest) across ten iterations of 10-fold cross-validation on each dataset: 'MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] Count of well-predicted metabolites (SCC > 95th percentile of background) for MiMeNet and baseline models on each dataset: 'identifies more well-predicted metabolites (increase in the number of well-predicted metabolites from 198 to 366, 104 to 143, and 4 to 29) compared to state-of-art linear models'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Tabular summary of performance metrics (SCC, PCC, MAE) for all models and datasets with mean and standard deviation: 'Mean and standard deviation values for SCC, PCC, and MAE are shown. All data were transformed using centered log-ratio except for IBD microbial input, which was obtained in relative abundance.'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] neural networks (MLPNN with ReLU activation): 'In MiMeNet, φ is set as the rectified linear unit (ReLU).'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MelonnPan (Elastic Net linear regression): 'MelonnPan was downloaded from https://github.com/biobakery/melonnpan and executed using the given instructions.'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Elastic Net regression: 'Multivariate Elastic Net models were implemented using ElasticNet and GridSearchCV using 5-fold internal cross-validation for hyper-parameter tuning where the hyper-parameter grid contained'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Random Forest regression: 'Random Forest models were implemented using RandomForestRegressor with the default parameter set-tings of 100 tree estimators.'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Canonical Correlation Analysis (CCA): 'Canonical correlation analyses were implemented using CCA with 10, 20, and 40 components.'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ADAM optimizer: 'MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scikit-learn (Python): 'these models can predict the entire set of metabolites at once, and all models were evaluated using 10 iterations of 10-fold cross-validation. Random Forest, multivariate Elastic Net, and Canonical'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] No specification of the exact random seed(s) used for the ten iterations of 10-fold cross-validation, making exact reproduction difficult: 'MiMeNet then trains multiple network models using 10-fold cross-validation'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] No explicit reporting of mean and standard deviation of correlation coefficients across the ten iterations, only single reported values: 'mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Hyperparameter values used for each dataset's neural network architecture not reported in main text or accessible supplementary section: 'The network architecture in MiMeNet is first determined for each paired dataset by tuning the hyperparameters'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] No specification of which baseline model (Elastic Net, CCA, or Random Forest) produces which reported correlation coefficients in the abstract: 'mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Threshold value for soil data described as 'higher' than other datasets but exact numerical value not provided in discussion: 'We also observed a higher threshold value for the soil data, which may be due to the longitudinal observations.'

## ev_021

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] No information on computational requirements, training time, or convergence criteria for the neural network models across datasets: 'MiMeNet then trains multiple network models using 10-fold cross-validation'
