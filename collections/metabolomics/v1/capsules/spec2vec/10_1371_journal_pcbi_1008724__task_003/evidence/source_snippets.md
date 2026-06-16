# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] How does the Spec2Vec method convert a pre-processed MS/MS spectrum into a fixed-length vector representation suitable for efficient similarity comparisons?: 'A spectrum can then be represented by a low-dimensional vector calculated as the weighted sum of all its fragment (and loss) vectors'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Spec2Vec converts spectra into documents by representing each peak as a word ("peak@xxx.xx") and adding neutral losses ("loss@xxx.xx") between 5.0–200.0 Da calculated as precursor − peak. The spectrum is then represented as a low-dimensional vector calculated as the weighted sum of all its fragment and loss vectors from a trained Word2Vec model.: 'every peak is represented by a word that contains its position up to a defined decimal precision ("peak@xxx.xx"). In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pre-processed MS/MS spectra in mzML, mzXML, or tabular format (m/z, intensity, precursor m/z per spectrum): 'After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pre-trained Word2Vec model (gensim format) from reference dataset (e.g., AllPositive or UniqueInchikey): 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Spectrum vector file containing spectrum identifiers and their corresponding Word2Vec-aggregated embedding vectors (one vector per spectrum): 'v_S = ∑_{i=1}^{n} √w_i · v_i, with w_i the intensity (normalized to maximum intensity = 1) and v_i the word vector of peak i'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Word2Vec: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] gensim: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] matchms: 'the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31]'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] spec2vec: 'spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available and can be installed via conda'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Numpy: 'by making extensive use of Numpy [24] and Numba [25]'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Numba: 'by making extensive use of Numpy [24] and Numba [25]'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Pandas: 'using Pandas [40]'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact Word2Vec embedding dimensionality is not specified; article refers to pre-trained models but does not state vector dimension: 'The two most important trained Word2Vec models used in this work can be downloaded from https://doi.org/10.5281/zenodo.3978054'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Precise weighted summation formula for aggregating word vectors into spectrum vector is not provided; method description states aggregation occurs but does not give mathematical formulation: 'After processing, spectra are converted to documents. For this, every peak is represented by a word'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Specification of peak decimal precision for peak@xxx.xx token generation is not stated numerically; only that peaks are represented 'up to a defined decimal precision': 'every peak is represented by a word that contains its position up to a defined decimal precision'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Handling of spectrum vectors with unknown peaks (peaks absent from trained Word2Vec model) during aggregation is described qualitatively but no algorithm for missing word imputation is provided: 'In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact'
