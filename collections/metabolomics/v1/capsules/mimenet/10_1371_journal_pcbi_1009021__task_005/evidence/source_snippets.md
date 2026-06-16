# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does per-partition hyperparameter tuning improve MiMeNet's metabolite prediction performance compared to tuning hyperparameters once on the first partition?: 'we evaluated the IBD (PRISM) and cystic fibrosis datasets using a single shared hyper-parameter set learned on the first partition against cross-validation where hyper-parameters are tuned every'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Using the IBD (PRISM) dataset, per-partition tuning increased mean SCC while cystic fibrosis showed a slight decrease, yet 141 of 143 significantly correlated metabolites were still identified with shared hyperparameters.: 'Using the IBD (PRISM) dataset, we observed an increase in mean SCC when tuning every iteration, while in the cystic fibrosis dataset, we observed a decrease in mean SCC. Despite the decrease of'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] IBD (PRISM) microbiome (16S rRNA OTU abundance in relative abundance format) and paired metabolomic data (LC-MS/MS, 121 IBD patients + 34 controls, 201 microbial species, 8848 metabolites): 'The first dataset was taken from a published study of patients with inflammatory bowel disease (IBD) [15]. It includes one cohort from the Prospective Registry (PRISM), which enrolled patients with a'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Cystic fibrosis lung sputum microbiome (16S rRNA, genus-level, 657 unique features from 172 samples) and paired metabolomic data (LC-MS/MS, 168 unique metabolites): 'The second dataset was taken from a study that collected 172 lung sputum samples from patients with cystic fibrosis. Microbial features were generated using 16S rRNA gene sequencing and abundance was'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Comparison table with mean SCC and standard deviation, and count of well-predicted metabolites (SCC >95th percentile background threshold) for Tune Once and Tune Every Partition conditions across 10-fold CV iterations: 'Using 10 iterations of 10-fold cross-validation, evaluations using shared hyper-parameters tuned from the first partition (Tune Once) were compared against evaluations with tuning for each partition'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Scatterplot or line plot showing per-metabolite mean SCC correlation comparison between Tune Once and Tune Every Partition conditions, with well-predicted metabolite threshold indicated: 'evaluations using shared hyper-parameters tuned from the first partition (Tune Once) were compared against evaluations with tuning for each partition (Tune Every Partition)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] neural networks: 'we present MiMeNet, a neural network framework for modeling microbe-metabolite relationships'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] MiMeNet: 'MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome based on a microbiome'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No specification of which hyperparameters are tuned 'once' in the Tune Once condition versus tuned 'every partition' in the Tune Every Partition condition; number of hidden layers, hidden layer sizes, L2 regularization penalty, and learning rate tuning strategy across folds not detailed: 'The network architecture in MiMeNet is first determined for each paired dataset by tuning the hyperparameters for the number and size of the hidden layers, the L2 regularization penalty parameter,'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No explicit reporting of mean SCC and well-predicted metabolite counts separately stratified by ablation condition (Tune Once vs. Tune Every Partition); only aggregate cross-dataset results provided in abstract: 'MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No documentation of the number of iterations of 10-fold CV performed under each ablation condition or whether the same data splits are reused across conditions for fair comparison: 'Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Computational cost, runtime, and convergence properties of Tune Once versus Tune Every Partition not reported; no analysis of whether tuning every partition provides improvement commensurate with increased training time: 'MiMeNet then trains multiple network models using 10-fold cross-validation'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] No specification of whether ablation study is restricted to one dataset (IBD PRISM) or applied across all three datasets (IBD PRISM, Cystic Fibrosis, Soil); unclear if sensitivity to tuning strategy is dataset-dependent: 'The first dataset was taken from a published study of patients enrolled in PRISM (the Prospective Registry in Inflammatory Bowel Disease Study at Massachusetts General Hospital) containing 121 IBD'
