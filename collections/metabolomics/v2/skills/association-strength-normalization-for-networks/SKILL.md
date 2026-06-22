---
name: association-strength-normalization-for-networks
description: Use when after generating metabolite-disease correlations and protein association predictions from a deep learning module (e.g., DeepMSProfiler's feature extraction), before constructing a bipartite network graph for publication.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_2259
  tools:
  - DeepMSProfiler
  - Python (NumPy, scikit-learn)
  - NetworkX or graph visualization library (e.g., Cytoscape, Gephi)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# association-strength-normalization-for-networks

## Summary

Normalize and scale metabolite-protein association strengths to enable comparable node sizing and edge weighting in bipartite disease-associated networks. This ensures visual and quantitative consistency across heterogeneous association metrics derived from deep learning predictions.

## When to use

After generating metabolite-disease correlations and protein association predictions from a deep learning module (e.g., DeepMSProfiler's feature extraction), before constructing a bipartite network graph for publication. Use this skill when association scores from different prediction methods or disease cohorts need to be rendered at comparable visual scales, or when edge transparency and node size must reflect confidence uniformly across disease groups.

## When NOT to use

- If association values are already normalized or ranked by the deep learning module and no further visual homogenization is needed.
- If the network is exploratory/draft and publication-grade visual consistency is not required.
- If association strengths are categorical (e.g., 'strong', 'weak') rather than continuous numeric values.

## Inputs

- Metabolite-disease correlation matrix (numeric, real-valued; rows=metabolites, columns=disease classes or correlation coefficients)
- Protein association prediction scores (numeric; confidence/probability values)
- Disease class labels (categorical; maps nodes to disease groups)

## Outputs

- Normalized association strength matrix (numeric, interval [0, 1] or [-1, 1])
- Scaled node attributes (node size, color intensity indexed by normalized association)
- Scaled edge attributes (opacity/transparency indexed by normalized association strength)

## How to apply

Load the metabolite-disease correlation data and protein association predictions produced by the deep learning module. Identify the range of association strength values across all metabolites, proteins, and disease classes. Apply min-max normalization or z-score standardization to scale all association values to a common interval (e.g., [0, 1] for node sizing; 0–1 for edge opacity). Document the normalization function and parameters used. Apply the same normalization transform to all edges and nodes to maintain relative ordering. Validate that the normalized values produce visually distinct node sizes and edge transparencies suitable for publication-quality rendering without saturation or loss of discriminative power.

## Related tools

- **DeepMSProfiler** (generates raw metabolite-disease correlations and protein association predictions that serve as input to normalization) — https://github.com/yjdeng9/DeepMSProfiler
- **Python (NumPy, scikit-learn)** (implements min-max scaling, z-score standardization, and normalization transforms)
- **NetworkX or graph visualization library (e.g., Cytoscape, Gephi)** (consumes normalized edge/node attributes for layout and rendering)

## Examples

```
from sklearn.preprocessing import MinMaxScaler; import numpy as np; scaler = MinMaxScaler(feature_range=(0, 1)); associations_norm = scaler.fit_transform(associations_raw.reshape(-1, 1)).flatten()
```

## Evaluation signals

- Normalized association values fall within the target interval (e.g., all values in [0, 1]; no values outside range).
- Node size and edge opacity are visually distinct across disease groups and association confidence levels in rendered network plot.
- Relative ordering of association strengths is preserved: if association A > association B in raw data, then normalized(A) > normalized(B).
- Normalization parameters (scale min, max, mean, std) are logged and reproducible across runs.
- High-resolution exported network plot exhibits no saturation (all nodes/edges remain distinguishable) and is suitable for publication.

## Limitations

- Normalization method choice (min-max vs. z-score vs. robust scaling) can significantly affect visual appearance; method must be documented and justified.
- Outlier association values (e.g., single very high correlation) may compress the dynamic range of other values under min-max scaling; robust scaling or percentile-based methods may be preferable.
- Normalization is applied independently per metabolite, protein, or disease group; cross-disease comparability requires careful choice of global vs. local normalization strategy.
- No universal standard for 'correct' association strength scaling exists; domain expertise and peer feedback are required to validate publication-readiness.

## Evidence

- [other] weighted by association strength and disease class: "Construct a bipartite network graph with metabolites and proteins as nodes, weighted by association strength and disease class."
- [other] node size scaled by association strength, and edge transparency reflecting confidence: "Render the network plot with disease-type color coding, node size scaled by association strength, and edge transparency reflecting confidence."
- [readme] provides three main outputs: sample disease type labels, heatmaps of metabolite-disease correlations, and disease-associated metabolite-protein networks: "It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite"
