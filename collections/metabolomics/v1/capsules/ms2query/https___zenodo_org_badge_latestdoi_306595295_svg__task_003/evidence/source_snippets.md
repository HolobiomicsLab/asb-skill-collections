# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] How does the scoring module compute average InChIKey score and neighbourhood score for candidate matches in MS2Query?: 'No verbatim evidence available in provided text'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The provided document is a README file containing installation and usage instructions, workflow steps, and repository links, but does not include technical descriptions of the scoring module implementation, score computation methods, or output record structures.: 'MS2Query - Reliable and fast MS/MS spectral-based analogue search'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Candidate match records from library-matching step: 'You want to make some kind of change to the code base (e.g. to fix a bug, to add a new feature, to update documentation)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Scored candidate matches with average InChIKey score and neighbourhood score fields: 'add your own tests (if necessary)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Test results verifying score computation correctness: 'make sure the existing tests still work by running ``python setup.py test``'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MS2Query: 'MS2Query - Reliable and fast MS/MS spectral-based analogue search'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'make sure the existing tests still work by running ``python setup.py test``'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GitHub: 'fork the repository to your own Github profile and create your own feature branch off of the latest master commit'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The specific mathematical definition, aggregation method (e.g., mean, median, weighted average), and input data sources for computing the 'average InChIKey score' are not provided in the changelog entry.: 'Average inchikey score and neighbourhood score [#78]'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The specific mathematical definition, distance/similarity metric, and neighbourhood selection criteria for computing the 'neighbourhood score' are not provided in the changelog entry.: 'Average inchikey score and neighbourhood score [#78]'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The structure and field names of the output record produced by the scoring module (e.g., JSON keys, column names if tabular) are not documented in the changelog.: 'Average inchikey score and neighbourhood score [#78]'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The relationship between the scoring module (PR #78) and the library-matching refactoring (PR #65) — specifically how scores are passed between these workflow steps — is not documented in the changelog.: 'Refactored library matching [#65]'
