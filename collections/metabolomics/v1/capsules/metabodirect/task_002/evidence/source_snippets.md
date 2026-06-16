# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Do the wall-clock runtimes of MetaboDirect's main pipeline on real FT-ICR MS datasets match the reported performance benchmarks of <1 min for 40 samples and ~2 min for 120 samples?: '40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min to generate all the figures, plots, and outputs'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] For the bacterium-phage dataset (36 samples with average 495 assigned molecular formulas per sample), the main MetaboDirect pipeline steps without KEGG mapping or transformation network calculation completed in less than 1 min (~36 s), and for the S. fallax dataset (4 samples with average 1793 assigned molecular formulas), the main pipeline completed in around 30 s.: 'The main steps of the MetaboDirect pipeline (without KEGG database mapping or calculating transformation networks) took less than 1 min (~36 s) for this data set. For this data set, the main steps of'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Peak-abundance and molecular formula .csv files for bacterium-phage model system (36 samples) and S. fallax leachate incubation (4 samples) from OSF repository: 'The first came from the exometabolome of a marine phage-host model system that uses a known, ecologically relevant marine bacterium (Pseudoalateromonas) and two contrastingly different infecting'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MetaboDirect v0.3.4 source code from GitHub repository and Zenodo deposit: 'The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and is available to install through the Python Package Index'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Wall-clock runtime (in seconds) for phage dataset main pipeline execution: '40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Wall-clock runtime (in seconds) for S. fallax leachate dataset main pipeline execution: 'The main steps of the MetaboDirect pipeline (without KEGG database mapping or calculating transformation networks) took less than 1 min (~36 s)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] CSV files containing filtered peaks, thermodynamic indices, normalized intensities, diagnostic tables, and diversity metrics for each dataset: 'This pre-processing step generates several .csv files containing the list of filtered peaks with their respective thermodynamic and molecular indices and the normalized and unnormalized intensities'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Comparison table or report documenting observed runtimes vs. reported benchmarks with percent deviation: 'The main steps of the MetaboDirect pipeline (without KEGG database mapping or calculating transformation networks) took less than 1 min (~36 s)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] MetaboDirect: 'develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python 3.8: 'The MetaboDirect pipeline was developed in Python 3.8'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R 4.0.2: 'The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NumPy: 'It requires the Python dependencies NumPy'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] pandas: 'It requires the Python dependencies NumPy [40], pandas'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] seaborn: 'It requires the Python dependencies NumPy [40], pandas [41, 42], seaborn'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] matplotlib: 'It requires the Python dependencies NumPy [40], pandas [41, 42], seaborn [43], py4cytoscape, and matplotlib'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] vegan: 'diversity metrics using functions from the R packages vegan'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] SYNCSA: 'diversity metrics using functions from the R packages vegan [63] and SYNCSA'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Specific wall-clock runtime for S. fallax dataset (4 samples) main pipeline execution is not reported; only benchmarks for 40 and 120 samples are stated: '40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Exact number of peaks detected and peaks with assigned molecular formula for S. fallax dataset is not provided in the results section: 'The data set had an average of 1025 peaks detected across the whole data set (n = 36 samples) and an average of 495 peaks that got assigned a molecular formula'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No documentation provided regarding system hardware specifications (CPU, RAM, OS) used for the reported runtime benchmarks, limiting reproducibility of timing comparisons across different computational environments: '40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min to generate all the figures, plots, and outputs'

## ev_021

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Specific MetaboDirect command-line invocation parameters and configuration options used for the runtime benchmarks are not detailed in the methods or results: 'The main steps of the MetaboDirect pipeline (without KEGG database mapping or calculating transformation networks) took less than 1 min (~36 s)'
