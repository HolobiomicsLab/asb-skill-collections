# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How do the smiles.py and sanitizing.py scripts transform raw SMILES strings from the gathering layer into standardized, deduplicated structural identifiers?: 'run smiles.py followed by sanitizing.py to produce the translated unique structure table'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The LOTUS processor applies two consecutive file-to-file transformations: smiles.py converts raw SMILES from interim/tables/0_original/structure/smiles.tsv.gz, and sanitizing.py then produces the final standardized unique structure table at interim/tables/1_translated/structure/unique.tsv.gz.: 'interim/tables/0_original/structure/smiles.tsv.gz, available in the lotusnprod/lotus-processor repository), run smiles.py followed by sanitizing.py to produce the translated unique structure table'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] interim/tables/0_original/structure/smiles.tsv.gz — raw SMILES table from gathering layer: '220([interim/tables/0_original/structure/smiles.tsv.gz]) --> 221[[smiles.py]] --> 222([interim/tables/1_translated/structure/smiles.tsv.gz])'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] interim/tables/1_translated/structure/unique.tsv.gz — deduplicated, sanitised SMILES table with standardised chemical structures: '250([interim/tables/1_translated/structure/unique.tsv.gz]) --> 260[[3_cleaningAndEnriching/sanitizing.py]]'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: '221[[smiles.py]], 260[[3_cleaningAndEnriching/sanitizing.py]]'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting updates, bug fixes, or version history for the smiles.py and sanitizing.py scripts.: 'No changelog found.'
