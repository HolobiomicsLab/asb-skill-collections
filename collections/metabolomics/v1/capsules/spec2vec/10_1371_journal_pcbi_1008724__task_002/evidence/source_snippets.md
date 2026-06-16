# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How do Spec2Vec similarity scores compare to cosine and modified cosine scores in terms of true-to-false-positive rate during library matching on the AllPositive dataset?: 'Spec2Vec model was trained only on the library set and Spec2Vec and cosine similarity scores were compared with h cosine similarity scores for library matching (Fig 4). Both Spec2Vec and cosine'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Spec2Vec resulted in a notably better true/false positive ratio at all thresholds compared to cosine and modified cosine scores during library matching, achieving up to 88% accuracy and higher retrieval rates.: 'Spec2Vec resulted in a notably better true/false positive ratio at all thresholds. Spec2Vec also allowed to correctly match the query spectra with up to 88% accuracy and showed both higher accuracy'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] AllPositive dataset (95,320 positive-mode LC-MS spectra with InChIKey annotations): 'The here used subset contains all spectra with positive ionization mode containing 112,956 spectra, out of which 92,954 with InChIKey'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pre-trained Word2Vec models (15-epoch and 50-epoch) trained on AllPositive dataset: 'The two most important trained Word2Vec models used in this work can be downloaded from https://zenodo.org/record/4173596 (trained on AllPositive dataset)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Cosine similarity score implementation from matchms package (>=0.6.0): 'the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (> = 0.6.0)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Modified cosine similarity score implementation from matchms package: 'Following Watrous [11], our modified cosine score combines both the matching peak m/z and the m/z shifted by the difference in precursor m/z'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Library matching results table with true-positive rates, false-positive rates, and area-under-curve for cosine, modified cosine, and Spec2Vec (15-epoch and 50-epoch) similarity scores: 'high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] ROC curves comparing performance of cosine, modified cosine, and Spec2Vec similarity scores on AllPositive library matching task: 'The poorer correlation between cosine and modified cosine similarity and structural similarity can largely be explained by high false positive rates'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Quantitative performance metrics (TP/FP counts and rates) for each similarity scoring method: 'ignoring scores based on fewer than min_match matching peak ks (here: min_match = 10)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] spec2vec: 'spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available and can be installed via conda'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] matchms: 'the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[abstract] Word2Vec: 'inspired by a natural language processing algorithm—Word2Vec'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] gensim: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Numpy: 'Spec2Vec by making extensive use of Numpy [24] and Numba [25]'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Numba: 'by making extensive use of Numpy [24] and Numba [25], the library'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pandas: 'Spec2Vec by making extensive use of Numpy [24] and Numba [25], the library was optimised by making extensive use of Pandas [40]'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scipy: 'An additional cosine score implementation (Fig C in S3 Text) relies on scipy [41]'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact number of spectra used as queries vs. library spectra in the reported library matching experiment is not specified: 'each removed 'query' spectrum was compared to the dataset by only using the Spec2Vec similarity score'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The specific figure or table location in the paper where library matching true-positive and false-positive rates are reported is not identified in the provided discussion text: 'Here, the performance was assessed based on library matching and unknown compound matching results'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Minimum matching peaks threshold (min_match) specified for Spec2Vec models in library matching is not explicitly stated in the provided discussion: 'Spec2Vec scores correlate better with structural similarity than cosine-based scores'

## ev_021

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Whether the reported library matching results use the same AllPositive dataset for both training the Word2Vec model and evaluating performance, or use a held-out test set, is not clearly specified: 'A separate Word2Vec model was trained on the remaining data of 76,062 spectra'
