# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Can the MIST-CF formula transformer architecture be extended to support negative-mode adducts, and what is the resulting top-k formula ranking accuracy on negative-mode MS/MS spectra?: 'Considering multiple adduct types beyond [M+H]+ (still only positive mode)'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MIST-CF currently considers multiple adduct types beyond [M+H]+ but is still restricted to positive mode only.: 'Considering multiple adduct types beyond [M+H]+ (still only positive mode)'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Negative-mode MS/MS spectra with annotated molecular formulas and adduct assignments from a public dataset (MassIVE or MetaboLights): 'No usage/docs found.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Pretrained MIST-CF model checkpoint with positive-mode formula transformer weights: 'MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Fine-tuned MIST-CF model checkpoint with negative-mode adduct support: 'No usage/docs found.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Top-k formula ranking accuracy metrics (top-1, top-5, top-10) on negative-mode test set, reported as accuracy_metrics.csv: 'MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MIST: 'an extension of MIST for annotating MS1 precursor masses from MS/MS data'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] SCARF: 'Utilizing sinusoidal formula embeddings as developed in our previous work SCARF'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history provided documenting when or whether negative-mode adduct support was implemented: 'No changelog found.'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The discussion section provides no specific details on negative-mode adduct types, training datasets, or accuracy results for negative-mode formula ranking: '_No changelog found._'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Synthesis timestamp and source repository are recorded, but the section does not report any empirical findings, results, or implementation status for negative-mode extension: 'Synthesized at: 2026-06-16T07:03:43+00:00'
