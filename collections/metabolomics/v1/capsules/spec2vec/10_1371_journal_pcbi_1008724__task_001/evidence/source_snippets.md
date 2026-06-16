# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How do Spec2Vec, cosine, and modified cosine similarity scores compare in their correlation with structural similarity when computed across all spectral pairs in the UniqueInchikey dataset?: 'Comparing the average structural similarity over the highest 0.1% of each respective spectra similarity score, with 0.1% corresponding to about 80,000 spectra pairs.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Spec2Vec similarity scores correlate stronger with structural similarity than cosine or modified cosine scores when evaluated at the top 0.1% of scoring pairs in the UniqueInchikey dataset.: 'This reveals that a high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores (Fig 3).'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] AllPositive dataset (95,320 spectra with positive ionization mode): 'The here used subset contains all spectra with positive ionization mode containing 112,956 spectra, out of which 92,954 with InChIKey'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] UniqueInchiKeys dataset (12,797 spectra with unique InChIKeys, one spectrum per InChIKey): 'We also worked with the considerably smaller subset UniqueInchiKeys which was reduced on purpose to be accessible for extensive benchmarking. It contains only one spectrum for every unique InChIKey'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pre-trained Word2Vec model trained on UniqueInchiKeys dataset: 'The two most important trained Word2Vec models used in this work can be downloaded from https://doi.org/10.5281/zenodo.3978054 (trained on UniqueInchikey dataset)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pre-trained Word2Vec model trained on AllPositive dataset: 'https://zenodo.org/record/4173596 (trained on AllPositive dataset)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] All-pairs Spec2Vec similarity score matrix for AllPositive dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity y (Tanimoto) for the UniqueInchikey dataset'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] All-pairs cosine similarity score matrix for AllPositive dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] All-pairs modified cosine similarity score matrix for AllPositive dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] All-pairs Spec2Vec similarity score matrix for UniqueInchiKeys dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity y (Tanimoto) for the UniqueInchikey dataset can be found on'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] All-pairs cosine similarity score matrix for UniqueInchiKeys dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity y (Tanimoto) for the UniqueInchikey dataset'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] All-pairs modified cosine similarity score matrix for UniqueInchiKeys dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity y (Tanimoto) for the UniqueInchikey dataset'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Table reporting average Tanimoto structural similarity at top 0.1% of scores for each method (Spec2Vec, cosine, modified cosine) on both datasets: 'high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] Spec2Vec: 'we introduce Spec2Vec, a novel spectral similarity score'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] Word2Vec: 'inspired by a natural language processing algorithm—Word2Vec'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] matchms: 'the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] gensim: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] RDKit: 'Tanimoto similarity (Jaccard index) based on daylight-like molecular fingerprints, version 2020.03.2, 2048 bits, derived using rdkit'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NumPy: 'Spec2Vec was optimised by making extensive use of Numpy [24]'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Numba: 'making extensive use of Numpy [24] and Numba [25]'

## ev_021

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pandas: 'Spec2Vec was optimised by making extensive use of Numpy [24] and Numba [25], the library matching was implemented using Pandas [40]'

## ev_022

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scipy: 'An additional cosine score implementation [in S3 Text] relies on scipy [41]'

## ev_023

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact spectral count and composition details for the AllPositive dataset used in this specific analysis (e.g., confirmation that 95,320 spectra were used and breakdown by ionization mode, source, or acquisition instrument): 'the remaining AllPositive dataset comprised 95,320 positive ionization mode mass spectra'

## ev_024

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Explicit description of how the Tanimoto similarity ground-truth labels were generated from InChIKeys or molecular structures for evaluating Figure 3B results: 'No explicit reference in provided discussion text to Tanimoto similarity computation method; EnrichedIndex references structural similarity but not Tanimoto derivation specifics'

## ev_025

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Confirmation that the Word2Vec embedding dimensionality, window size, and other hyperparameters used for training on both AllPositive and UniqueInchiKeys datasets are documented and reproducible: 'No explicit statement of Word2Vec hyperparameters in provided discussion section'

## ev_026

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Detailed specification of the threshold or method used to determine which spectra pairs constitute the 'top 0.1%' of similarity scores and whether this is computed separately for each method or using a unified ranking: 'Discussion section does not explicitly define the top 0.1% selection criterion or percentile computation methodology'

## ev_027

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Documentation of any post-processing steps, outlier removal, or filtering applied to the computed similarity scores before computing average Tanimoto similarity at the top 0.1% threshold: 'Discussion section does not detail post-scoring filtering or outlier handling for Figure 3B analysis'
