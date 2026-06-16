# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How does MetaboDirect construct biochemical transformation networks from FT-ICR MS peak data, and what are the input requirements and output formats for this mass-difference network generation step?: 'The last step of MetaboDirect produces molecular transformation networks for each of the samples. These networks are generated ab initio from the masses that are determined through high-resolution'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] MetaboDirect generates transformation networks ab initio from high-resolution mass spectrometry data by identifying chemically transformed species using clearly defined mass differences, with the networks designed to quantify differences in microbial metabolic pathways and identify hub metabolites involved in many reactions.: 'These networks are generated ab initio from the masses that are determined through high-resolution mass spectrometry and are based on the fact that the ultra-high mass accuracy of the method allows'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Filtered peak list CSV containing peak identifiers, m/z values, assigned molecular formulas, compound class, and normalized intensities from preprocessing step: 'This pre-processing step generates several .csv files containing the list of filtered peaks with their respective thermodynamic and molecular indices and the normalized and unnormalized intensities'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Reference biochemical transformation key containing predefined masses of common metabolic reactions, optionally user-specific for analyzed system: 'comparing them to the list of pre-defined masses of common metabolic reactions (biochemical transformations key)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Edge CSV file(s) per sample containing source peak m/z, target peak m/z, mass difference, transformation type (biotic/abiotic), and ppm error: 'The results are exported as .csv "edge" files containing the potential transformations occurring between the masses in each sample.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Node CSV file containing all detected peaks with m/z, molecular formula, compound class, and sample presence: 'nodes represent peaks detected in the different samples and edges represent the putative chemical transformations happening between the nodes'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Transformation statistics CSV reporting number of transformations occurring per sample and transformation frequency: 'Additional files with the number of transformations occurring per sample are also generated.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Network visualization files and statistics tables exported as CSV and bar plots: 'network statistics will be calculated and reported as .csv tables and bar plots'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MetaboDirect: 'Molecular transformation networks for each sample (mass difference network-based approach) are generated in this step'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Cytoscape: 'Networks are then constructed using Cytoscape [79] and colored based on their molecular class.'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No explicit specification of which reference transformation table (e.g., KEGG database, custom in-house library, or published biochemical transformation catalog) should be used for mass-difference matching in the standalone module: 'calculation of mass-based chemical transformations'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No documented mass tolerance (ppm or Da) for matching observed mass differences to reference transformation masses: 'mass-based chemical transformations'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No description of how the script handles or filters transformations with multiple equally plausible biochemical identities at the same observed mass difference: 'transformation networks'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] No specification of input file format requirements (column headers, delimiter, data type for m/z and formula columns, row order): 'The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No documented output schema or example node/edge list file showing expected column names, data types, and edge weight definitions for Cytoscape import: 'transformation networks'
