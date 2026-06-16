# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does training MiMeNet on all metabolites (annotated + unannotated) improve prediction accuracy for annotated metabolites compared to training only on annotated metabolites?: 'by training on the entire set of metabolites, the number of well-predicted metabolites for the annotated set increased from 333 to 366. Additionally, the SCCs of the annotated metabolites'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Training MiMeNet on all metabolites improved mean Spearman correlation coefficients for annotated metabolites from 0.259 to 0.309 (P < 10−47), with well-predicted metabolites increasing from 333 to 366 out of 466 annotated metabolites in the IBD (PRISM) dataset.: 'by training on the entire set of metabolites, the number of well-predicted metabolites for the annotated set increased from 333 to 366. Additionally, the SCCs of the annotated metabolites'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] IBD (PRISM) microbiome abundance data (OTU/ASV table, relative abundance format): 'The first dataset was taken from a published study of patients with inflammatory bowel disease (IBD). It includes one cohort from the Prospective Registry (PRISM), which enrolled patients with a'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] IBD (PRISM) metabolomic abundance data (LC-MS/MS, both annotated and unannotated metabolites): 'A total of 201 microbial species and 8848 metabolites were identified for the IBD (PRISM) and IBD (External) datasets'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Metabolite annotation status (binary flag indicating annotated versus unannotated metabolites): 'trained only on the annotated metabolites'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Scatterplot (PNG/PDF) comparing mean Spearman correlation coefficients for annotated metabolites: x-axis = SCC (MiMeNet trained on all metabolites), y-axis = SCC (MiMeNet trained on annotated metabolites only): 'Scatterplot of mean predicted Spearman's correlation over 10 iterations of 10-fold cross-validation for each metabolite between MiMeNet'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Numeric table (CSV) containing per-metabolite mean SCC values for both training regimes (all metabolites vs. annotated-only) and computed delta: 'mean SCC and (B) mean PCC values of the members within the module'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Summary statistics: overall mean SCC (all metabolites regime), overall mean SCC (annotated-only regime), mean delta, and 95% CI or standard deviation: 'the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundances'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] MiMeNet: 'MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome based on a microbiome'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] neural networks: 'An MLPNN model is composed of multiple fully connected hidden layers composed of perceptrons'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ADAM optimizer: 'MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python (scikit-learn, seaborn, or matplotlib for visualization): 'using Seaborn's clustermap function in Python'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The discussion states that MiMeNet prediction on annotated metabolites 'benefited from including tasks of predicting the rest of the unannotated metabolites' but does not provide the exact numeric correlation values or deltas for annotated metabolites in the two training scenarios.: 'Indeed, our results of the IBD data demonstrated that the MiMeNet prediction on the set of the annotated metabolites benefited from including tasks of predicting the rest of the unannotated'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The discussion acknowledges that 'not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation' but does not specify what fraction of the annotated metabolite set falls into this category or how this affects the comparison.: 'We note that since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The section references Fig 2D–2F to support the claim about improved prediction of annotated metabolites when training on all metabolites, but the referenced figure images and their numeric legends are not included in the provided discussion text.: 'Indeed, our results of the IBD data demonstrated that the MiMeNet prediction on the set of the annotated metabolites benefited from including tasks of predicting the rest of the unannotated'
