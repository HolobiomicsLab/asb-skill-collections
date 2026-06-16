# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How does Olden's method derive microbe-metabolite feature attribution scores from MLPNN network weights, and how are these scores subsequently used to construct functional modules via biclustering?: 'using the learned network models, MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites. Then MiMeNet biclusters the score'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] MiMeNet computes feature attribution scores for all microbe-metabolite pairs from trained MLPNN network weights, then applies biclustering to group microbes and metabolites into modules where members share similar attribution patterns. Positive attribution scores indicate microbes that contribute positively to metabolite abundance prediction, while negative scores indicate negative contributions.: 'A positive score means that the microbe contributes positively to the prediction of the abundance of the metabolite. Likewise, a negative score contributes negatively to the prediction of the'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Trained MLPNN models (100 models from 10 iterations of 10-fold cross-validation with saved weight tensors): 'we calculated the mean feature attribution score matrix, which was then flattened into a feature vector and a threshold was set at the 97.5 percentile'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Well-predicted metabolites list (metabolites with Spearman correlation coefficient above 95th percentile of background distribution): 'We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] IBD (PRISM) microbiome and metabolome data (centered log-ratio transformed, 201 microbes × 8848 metabolites): 'A total of 201 microbial species and 8848 metabolites were identified for the IBD (PRISM) and IBD (External) datasets'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Background feature attribution score distribution (from 100 models with randomly shuffled microbiome-metabolome samples): 'we calculated feature attribution score matrices from the network models used to generate the background correlation distribution'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Normalized microbe-metabolite feature attribution score matrix (microbes × metabolites, values clipped to [-1, 1]): 'We normalized the values in each feature attribution score matrix S_i by dividing the significant threshold score identified from the background and clipped values to be between -1 and 1'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Microbial module assignments (list of microbe IDs grouped by cluster number k*): 'The final set of microbial and metabolite modules are then determined by biclustering S* using k* and k* to cluster the rows and columns respectively'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Metabolite module assignments (list of metabolite IDs grouped by cluster number k**): 'The final set of microbial and metabolite modules are then determined by biclustering S* using k* and k* to cluster the rows and columns respectively'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Module-based interaction network edge list (microbe module–metabolite module pairs with average normalized attribution scores, filtered to |score| ≥ 0.25): 'For visualization of the microbe-metabolite interaction network, the score between a pair of modules was calculated as the average normalized feature attribution between each microbe and metabolite'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] neural networks: 'we present MiMeNet, a neural network framework for modeling microbe-metabolite relationships'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] WGCNA: 'compared the microbial modules in the IBD (PRISM) dataset identified by MiMeNet to those identified by the Weighted Correlation Network Analysis (WGCNA)'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Seaborn clustermap: 'using Seaborn's clustermap function in Python'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Cytoscape: 'using Cytoscape'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python scikit-learn: 'using Python's sci-kit-learn package'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact hyperparameter settings (soft threshold power, minimum module size, cut height threshold) for WGCNA consensus clustering applied to feature attribution score matrix for IBD (PRISM) dataset are not reported.: 'MiMeNet then trains multiple network models using 10-fold cross-validation'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Method for deriving feature attribution scores (attribution method name beyond mention of 'network weights') and mathematical formulation are not explicitly detailed in the provided discussion excerpt.: 'the feature attribution scores derived from the network weights could be used to construct modules'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Threshold or criteria for selecting microbes that enter the feature attribution score matrix are partially specified ('163 microbes that had at least one significant attribution score') but the initial filtering criteria (10% prevalence, abundance cutoff) and final filtering logic are not fully justified.: 'We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Computational time, memory requirements, and scalability characteristics of the feature attribution + WGCNA pipeline are not reported.: 'Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Sensitivity analysis of module assignments to variations in WGCNA parameters (e.g., soft threshold power, merge cut height) is not presented; robustness of biological findings to parameter choices is not assessed.: 'construct modules of microbes with similar positive or negative effects on a set of metabolites'
