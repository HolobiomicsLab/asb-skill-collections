# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Does the memo_from_unaligned component correctly generate a MemoMatrix object with the expected structure and content when applied to unaligned MS2 spectra files?: 'The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MEMO generates MS2 fingerprints by counting the occurrence of MS2 peaks and neutral losses in each sample, which are then aligned to compare different samples.: 'The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample. These fingerprints can in a second stage be aligned'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Unaligned MS2 spectra files in matchms-compatible format (MGF, mzML, or mzXML): 'MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Repository-provided example datasets from mandelbrot-project/memo_publication_examples or mandelbrot-project/memo: 'You can clone the Github package repository to get the demo files and the tutorial!'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MemoMatrix object: a structured sample-by-feature matrix with MS2 fingerprint counts indexed by sample and peak/loss identifiers: 'The occurrence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Matrix metadata including sample identifiers, feature annotations, and alignment statistics: 'These fingerprints can in a second stage be aligned to compare different samples'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] memo-ms: 'pip install memo-ms'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] matchms: 'MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] spec2vec: 'MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python 3.8: 'conda create --name memo python=3.8'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] numpy: 'pip install numpy'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scikit-bio: 'conda install -c conda-forge scikit-bio'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No specific reference to test data location or format for memo_from_unaligned input: 'test for memo_from_unaligned'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No description of expected MemoMatrix structure, dimensions, or schema documented in changelog: 'New `MemoMatrix` class, replacing the former `MemoContainer`'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Changelog does not detail what filtering or preprocessing memo_from_unaligned applies to raw unaligned spectra: 'Changed classes.py to avoid erasing when filtering'
