# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Which descriptor subgroups have the greatest impact on bitter/not-bitter prediction accuracy when systematically removed from the BitterPredict classifier?: 'BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] BitterPredict.m accepts CSV or EXCEL files containing molecular descriptors as input and produces bitter/not-bitter predictions for each molecule, enabling descriptor ablation studies through systematic manipulation of descriptor subgroups in the input data.: 'BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Descriptor CSV file with required molecular descriptors and bitter/not-bitter labels: 'BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Table of per-descriptor-group prediction-change rates showing how many molecules change prediction label when each descriptor subgroup is ablated: 'systematically ablate or zero-out descriptor subgroups and record how the bitter/not-bitter prediction label changes per molecule, producing a table of per-descriptor-group prediction-change rates'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] BitterPredict: 'BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history provided: '_No changelog found._'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Repository synthesis timestamp and exact commit or release tag for BitterPredict1 not specified; only synthesis date given: 'Synthesized at: 2026-06-15T13:58:45+00:00'
