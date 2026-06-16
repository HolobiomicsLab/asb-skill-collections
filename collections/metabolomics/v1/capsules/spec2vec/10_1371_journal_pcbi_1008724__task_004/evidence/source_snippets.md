# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How does the fraction of peak coverage achieved by a Spec2Vec Word2Vec model vary as a function of training corpus size, and can a 97% coverage threshold be reproduced with the AllPositive dataset trained for 15 epochs?: 'In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] A Word2Vec model trained on the AllPositive dataset for 15 iterations achieves approximately 97% peak coverage, quantified by computing the missing-fraction statistic (1 − Σ√w_i / Σ√w_i) across spectra.: 'Training a model on the UniqueInchikey dataset takes about 30 minutes on an Intel i7-8550U CPU.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] AllPositive dataset (95,320 positive ionization mode spectra with InChIKey), filtered to m/z ∈ [0, 1000] and ≥10 peaks: 'We removed all peaks with m/z ratios outside the range [0, 1000] and discarded all spectra with less than 10 peaks. This left us with 95,320 spectra'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pre-trained Word2Vec model (gensim, CBOW, window-size=500, negative=5, 15 epochs) trained on AllPositive dataset: 'training a model with negative sampling (negative = 5) and 15 (AllPositive) up to 50 (UniqueInchikey) epochs were best suited for obtaining close to optimal model performance'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Spec2Vec library (Python package) and matchms ≥0.6.0 for spectrum document conversion and word embedding lookup: 'The underlying code was developed into two Python packages to handle and compare mass spectra, matchms (https://github.com/matchms/matchms) and spec2vec (https://github.com/iomega/spec2vec)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Missing-fraction statistics table (CSV) with columns: spectrum_id, missing_fraction, coverage (1 − missing_fraction), cumulative_corpus_size: 'missing fraction = 1 − (Σ√w_i for model words) / (Σ√w_i all words), where w_i is normalized intensity'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Coverage-vs-corpus-size curve (PNG/PDF) showing mean peak/loss coverage increasing from 0 to 97% as corpus size grows to 95,320 spectra: 'models we trained on AllPositive (95,320 spectra) with 2-decimal rounding contained about 97% of all possible peaks and losses'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Summary metrics JSON: mean_missing_fraction, median_missing_fraction, final_coverage_percent, spectra_with_coverage_above_95_percent: 'having different peak filtering for the different similarity scores, we also repeated the library matching with cosine scores computed based on the Spec2Vec-processed data'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Spec2Vec: 'The underlying code was developed into two Python packages to handle and compare mass spectra, matchms (https://github.com/matchms/matchms) and spec2vec (https://github.com/iomega/spec2vec)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Word2Vec: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] matchms: 'the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] gensim: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NumPy: 'optimized by making extensive use of Numpy [24] and Numba [25]'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Numba: 'optimized by making extensive use of Numpy [24] and Numba [25]'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pandas: 'was optimized using Pandas [40]'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact formula or implementation reference for computing missing-fraction statistic (1 − Σ√w_i / Σ√w_i) and definition of w_i weighting scheme: 'For many cases, we expect that a model pre-trained on a large spectra dataset will cover a large enough fraction of the features to work well without the need for additional re-training (see Fig G in'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specific corpus size sampling strategy (which intermediate corpus sizes were tested to generate the coverage curve toward 97% coverage): 'training the embedding on 95,320 spectra took 40 minutes (when training for 15 iterations)'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Location and format of reported 97% peak coverage curve (whether in Figure G of S3 Text, a supplementary table, or main figure): 'For many cases, we expect that a model pre-trained on a large spectra dataset will cover a large enough fraction of the features to work well without the need for additional re-training (see Fig G in'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Detailed definition of how peak weights (w_i) are computed from spectra (intensity-based, frequency-based, or other metric): 'In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part'
