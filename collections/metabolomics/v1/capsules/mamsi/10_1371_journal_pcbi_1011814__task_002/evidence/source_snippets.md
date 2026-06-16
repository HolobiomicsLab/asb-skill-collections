# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does the MamsiStructSearch module group statistically significant LC-MS features into structural clusters using mass-to-charge ratio and retention time information?: 'the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MamsiStructSearch operates by searching retention time windows for isotopologue signatures (mass differences of 1.00335 Da), then searching for common adduct signatures by calculating hypothetical neutral masses from common electrospray ionisation adducts, and finally merging overlapping adduct and isotopologue clusters to form structural clusters.: 'each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 *Da* between mass-to-charge ratios (*m/z*) of the features. This is followed by a search for common'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] LC-MS intensity data (DataFrame) with rows=samples, columns=features in format (AssayName)_(RTsec)_(m/z)m/z; e.g., HPOS_233.25_149.111m/z: 'Data frame with LC-MS intensity data. - rows: samples - columns: features (LC-MS peaks). Column names in the format: **(AssayName)_(RTsec)_(m/z)m/z**. For example: **HPOS_233.25_149.111m/z**'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] List or array of statistically significant feature indices or binary mask selecting features from the full LC-MS matrix: 'Select features with p-value < 0.01. You can also apply multiple testing correction methods to adjust the p-value threshold.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] DataFrame of statistically significant features annotated with structural cluster IDs, adduct group assignments, isotopologue group assignments, adduct labels, cross-assay link IDs, correlation cluster assignments, and (if applicable) compound names from annotation: 'DataFrame of significant features with structural clusters.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Visualizations including isotopologue pattern dendrogram, adduct cluster heatmap, silhouette plot (if silhouette flattening used), and correlation-structure heatmap: 'Clustering for features based on their correlations. The method uses hierarchical clustering to create clusters. To flatten clusters, the method uses either a constant threshold or silhouette score.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'MAMSI is a Python framework'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] pandas: 'import pandas as pd'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] numpy: 'import numpy as np'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scipy: 'scipy'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scikit-learn: 'from sklearn.model_selection import train_test_split'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] matplotlib: 'from matplotlib import pyplot as plt'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] networkx: 'networkx'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MamsiStructSearch: 'A class for performing structural search on multi-modal MS data using.'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found.: 'No changelog found.'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No specification of exact mass tolerance windows or RT tolerance thresholds for adduct and isotopologue clustering: 'not present in provided discussion section'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No detailed specification of the data structure or file format of the structural cluster output artifact: 'not present in provided discussion section'
