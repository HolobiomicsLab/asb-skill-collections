# Evaluation Strategy

## Direct Checks

- verify that github:enveda/ccs-prediction repository is accessible and contains trained model artifacts
- verify that input molecular graphs (in common formats such as .sdf, .mol, .graph, or .json) exist in the repository
- verify that model outputs (predictions or intermediate activations) are retrievable from the repository or can be computed from stored model weights and input graphs
- verify that a post-hoc attribution method (node ablation, edge ablation, gradient-based saliency, or SHAP) can execute without errors on the model and input data
- verify that the attribution analysis produces a ranked feature-importance table or figure with named features and quantitative importance scores
- verify that the importance scores are in a valid numeric range appropriate to the attribution method (e.g., non-negative for ablation-based methods, bounded for normalized saliency)
- verify that the output includes at least one structural feature class (e.g., atom type, bond type, degree, functional group, or graph property) with an assigned importance rank or score

## Expert Review

- assess whether the choice of attribution method (ablation, gradient, SHAP, or other) is justified and appropriate for the GNN architecture and task
- assess whether the ranked features identified as driving CCS predictions are chemically and biophysically plausible (e.g., molecular weight, spatial extent, polarity-related features)
- assess whether the feature-importance results show consistency across different molecular subsets or test splits if multiple attribution runs are reported
- assess whether the interpretation of feature importance aligns with known physical principles governing collision cross section in mass spectrometry
