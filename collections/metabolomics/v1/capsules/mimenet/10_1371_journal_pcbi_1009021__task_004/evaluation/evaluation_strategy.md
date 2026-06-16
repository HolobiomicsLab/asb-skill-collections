# Evaluation Strategy

## Direct Checks

- file_exists: verify that IBD (PRISM) dataset microbiome and metabolome input files are accessible in the MiMeNet repository or cited deposit (Zenodo/GEO/MetaboLights)
- script_runs: execute MiMeNet training pipeline with configuration parameter 'train_on_all_metabolites=True' on IBD (PRISM) dataset and verify no runtime errors
- script_runs: execute MiMeNet training pipeline with configuration parameter 'train_on_all_metabolites=False' (annotated only) on IBD (PRISM) dataset and verify no runtime errors
- output_matches_reference: mean Spearman correlation on annotated metabolites for all-metabolites model is between 0.45 and 0.50 (robust to minor numerical precision differences), matching Fig 2D–2F context or SI Table
- output_matches_reference: mean Spearman correlation on annotated metabolites for annotated-only model is lower than all-metabolites model, with delta (improvement) reported in Fig 2D–2F or supplementary materials
- file_format_is: scatterplot output file (PNG/PDF/SVG) exists and contains two-dimensional visualization of prediction correlations across annotated metabolites for both training conditions
- contains_substring: Fig 2D–2F caption or associated text explicitly states numeric mean correlation values and/or delta improvements for annotated metabolites across the two training regimes

## Expert Review

- assess whether the reported improvement in mean Spearman correlation when including unannotated metabolites during training is biologically plausible and consistent with the stated hypothesis that shared information across metabolites improves prediction
- evaluate whether the comparison controls for confounding factors (network architecture, hyperparameters, cross-validation scheme, random seed) between the two training conditions to isolate the effect of metabolite set composition
- determine whether the annotated metabolite set is clearly defined and reproducibly extracted from the input metabolomic data, and verify no data leakage or label contamination between conditions
