# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What is the output format and structure when two separately generated MemoMatrix objects are merged using the merged_memo() function?: 'These fingerprints can in a second stage be aligned to compare different samples.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MEMO enables alignment of MS2 fingerprints generated from separate samples to compare them in a second stage.: 'These fingerprints can in a second stage be aligned to compare different samples.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] First MemoMatrix object (MS2 fingerprint matrix with sample-peak and sample-neutral-loss counts): 'The occurrence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Second MemoMatrix object (MS2 fingerprint matrix with sample-peak and sample-neutral-loss counts from separate sample set): 'The occurrence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Merged MemoMatrix file containing combined MS2 fingerprint data from both input matrices with all sample and feature columns preserved: 'These fingerprints can in a second stage be aligned to compare different samples.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MEMO: '**M**\ s2 bas\ **E**\ d sa\ **M**\ ple vect\ **O**\ rization (**MEMO**) is a method allowing a Retention Time (RT) agnostic alignment'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] memo-ms: 'pip install memo-ms'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python 3.8: 'conda create --name memo python=3.8'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No specification of merged_memo() function signature, parameters, or expected behavior in the provided document: 'test for merged_memo()'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No documentation or examples showing how two MemoMatrix objects are instantiated or what their structure contains: 'New `MemoMatrix` class, replacing the former `MemoContainer`'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No definition of column names or data types expected in a MemoMatrix object: 'possibility to import "memo ready" feature table'
