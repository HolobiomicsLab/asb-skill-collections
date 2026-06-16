# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Does the NMR2Struct model maintain accurate structure recovery performance when applied to molecules with more than 19 heavy atoms, or does accuracy degrade significantly beyond this training scope?: 'We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms, a size for which there are trillions of possibl'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms, establishing a known performance limit beyond which generalization is uncharacterized.: 'We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Pretrained or fine-tuned NMR2Struct model checkpoint (transformer + CNN weights): 'a transformer architecture can be constructed to efficiently solve the task... Integrating this capability with a convolutional neural network, we build an end-to-end model'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Held-out test set of molecules exceeding 19 heavy atoms from PubChem or equivalent public chemical database: 'held-out set of molecules exceeding 19 heavy atoms (sourced from a public chemical database such as PubChem or the deposited dataset)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] 1D ¹H and/or ¹³C NMR spectra for out-of-scope molecules (experimental or simulated): 'predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] In-scope baseline accuracy metrics (top-k structure recovery for molecules ≤19 heavy atoms): 'We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Top-1, top-3, and top-5 structure recovery accuracy scores for out-of-scope molecules (>19 heavy atoms): 'measure the degradation or retention of top-k structure recovery accuracy relative to the in-scope condition'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Comparative accuracy degradation table (out-of-scope vs. in-scope baseline, absolute and relative loss): 'measure the degradation or retention of top-k structure recovery accuracy relative to the in-scope condition'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Summary report documenting failure modes, error distribution, and molecular size/complexity thresholds at which model performance drops significantly: 'held-out set of molecules exceeding 19 heavy atoms'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] transformer architecture: 'a transformer architecture can be constructed to efficiently solve the task'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] convolutional neural network: 'Integrating this capability with a convolutional neural network, we build an end-to-end model'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No changelog or version history provided; unknown whether models, datasets, or evaluation code have been updated since publication date: '_No changelog found._'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No explicit statement of the upper heavy-atom threshold tested (19 atoms mentioned as demonstration scope in intro, but no explicit out-of-scope test boundary stated in discussion): '[Section contains no technical details; only header and metadata]'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] No reference to deposited code, model weights, or held-out test set location (only GitHub source cited generically; specific branch, release tag, or supplementary data accession not identified): 'Source: github:MarklandGroup__NMR2Struct'
