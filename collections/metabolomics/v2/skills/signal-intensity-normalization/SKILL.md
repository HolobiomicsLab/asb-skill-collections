---
name: signal-intensity-normalization
description: Use when after loading raw LC-MS data from multiple disease groups when
  you need to compute correlations between metabolite signals and disease classes,
  or before training a deep learning model on metabolomics profiles.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - DeepMSProfiler
  - Python (seaborn, matplotlib)
  - TensorFlow / Keras
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41467-024-51433-3
  title: DeepMSProfiler
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepmsprofiler_cq
    doi: 10.1038/s41467-024-51433-3
    title: DeepMSProfiler
  dedup_kept_from: coll_deepmsprofiler_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-51433-3
  all_source_dois:
  - 10.1038/s41467-024-51433-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# signal-intensity-normalization

## Summary

Normalize LC-MS metabolite signal intensities across samples to enable fair correlation analysis and disease classification. This preprocessing step removes batch effects and technical variation that would otherwise confound the relationship between metabolite abundance and disease phenotype.

## When to use

Apply this skill after loading raw LC-MS data from multiple disease groups when you need to compute correlations between metabolite signals and disease classes, or before training a deep learning model on metabolomics profiles. Use it when sample-to-sample variation in total ion current or detector response could obscure true metabolite-disease associations.

## When NOT to use

- Input is already a correlation matrix or feature table—normalization has already been applied
- Analyzing a single disease group or single sample (no cross-sample variation to normalize)
- Data is from a highly standardized platform with negligible batch effects or detector drift

## Inputs

- Raw LC-MS data files (.npy format or .mzML format, auto-converted)
- Per-sample metabolite signal intensities (from model outputs)
- Sample disease type labels (.txt file with FilePath and Label columns)

## Outputs

- Normalized metabolite signal intensity matrix (samples × metabolites)
- Correlation coefficients between metabolites and disease classes
- Metabolite-disease correlation heatmap (.npy or image format)

## How to apply

Load per-sample metabolite signal intensities (in .npy or mzML format, auto-converted by DeepMSProfiler) from the raw metabolomics data directory. Apply intensity normalization within the model training pipeline (via run_train) to scale all metabolite signals to a common reference frame—this is embedded in the feature extraction step. The normalized intensities are then used to compute correlation coefficients (Pearson or Spearman) between each metabolite and disease class labels across all samples. Verify normalization correctness by checking that correlation coefficients fall within [-1, 1] and that heatmap cell values reflect both magnitude and direction of metabolite-disease association.

## Related tools

- **DeepMSProfiler** (End-to-end platform that handles signal normalization as part of the training and feature extraction pipeline (run_train, run_feature)) — https://github.com/yjdeng9/DeepMSProfiler
- **Python (seaborn, matplotlib)** (Visualization of normalized signal intensities and correlation heatmaps after normalization)
- **TensorFlow / Keras** (Deep learning framework used by DeepMSProfiler to embed and apply intensity normalization during model training)

## Examples

```
python mainRun.py -data ../example/data/ -label ../example/label.txt -out ../jobs -run_train -run_pred -run_feature
```

## Evaluation signals

- Correlation coefficients for each metabolite-disease pair fall within the valid range [-1, 1]
- Heatmap cell colors show symmetric magnitude distribution (no extreme outliers caused by unnormalized scales)
- After normalization, metabolite signals across samples have comparable dynamic ranges (inspectable in feature_results/ensemble_RISE.npy)
- Confusion matrix and AUC curves from downstream classification improve or stabilize compared to pre-normalization runs

## Limitations

- Normalization is performed internally by DeepMSProfiler during training; explicit control over normalization method (e.g., z-score vs. quantile vs. median) is not exposed in the command-line interface
- The tool assumes all samples are comparable in biological relevance; strong biological outliers may skew normalization parameters
- No changelog or explicit discussion of normalization algorithm provided; method details must be inferred from TensorFlow/Keras model code

## Evidence

- [other] Load the per-sample model outputs (sample predictions and metabolite signal intensities) from the trained DeepMSProfiler model: "Load the per-sample model outputs (sample predictions and metabolite signal intensities) from the trained DeepMSProfiler model."
- [other] Compute correlation coefficients (e.g., Pearson or Spearman) between each metabolite signal and disease class labels for all samples: "Compute correlation coefficients (e.g., Pearson or Spearman) between each metabolite signal and disease class labels for all samples."
- [readme] It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite: "It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite"
- [readme] The demo files are in. npy format. If you upload a file in. mzML format, and the script will automatically convert to. npy format automatically.: "The demo files are in. npy format. If you upload a file in. mzML format, and the script will automatically convert to. npy format automatically."
