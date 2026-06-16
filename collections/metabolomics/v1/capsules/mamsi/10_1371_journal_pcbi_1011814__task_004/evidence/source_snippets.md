# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How do structural cluster outputs (cluster count and size distribution) differ between using all adducts versus only the most-common adducts in the MAMSI framework's adduct signature search?: 'the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MAMSI enables clustering of LC-MS features by structural properties through adduct signature detection, which can be parameterized to search either all common adducts or a restricted set of most-common adducts.: 'This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Selected LC-MS feature intensity table (rows: samples, columns: features with naming convention (AssayName)_(RTsec)_(m/z)m/z, e.g. HPOS_233.25_149.111m/z): 'Load Selected LC-MS Features
struct.load_lcms(selected)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Structural cluster results table containing cluster ID, cluster size, member features, isotopologue group, adduct group, and cross-assay link status for 'all adducts' mode: 'get_structural_clusters(adducts = 'all', annotate = True)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Structural cluster results table for 'most-common adducts' mode with identical columns as 'all adducts' mode output: 'get_structural_clusters(adducts = 'most-common', annotate = True)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Comparative summary table with rows for each adduct mode, columns: Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage (%): 'Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters'

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

[methods] matplotlib: 'from matplotlib import pyplot as plt'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MAMSI (MamsiStructSearch): 'A class for performing structural search on multi-modal MS data using'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, bug fixes, or feature changes for the py-mamsi package.: 'No changelog found.'
