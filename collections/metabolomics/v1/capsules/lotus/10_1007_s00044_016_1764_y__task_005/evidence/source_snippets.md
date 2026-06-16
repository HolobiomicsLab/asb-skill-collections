# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does the 5_addingOTL.R script enrich cleaned organism names with Open Tree of Life identifiers?: '5_addingOTL.R'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The 5_addingOTL.R script processes the cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) to map organism names to Open Tree of Life identifiers, producing an OTL-enriched organism dictionary output in interim/dictionaries/organism/.: 'R
- Python 3
- Java >= 17'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) containing standardized and verified organism names: '122([interim/tables/2_cleaned/organism/cleaned.tsv.gz]) --> 123[[5_addingOTL.R]]'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] OTL-enriched organism dictionary in SQLite format (interim/dictionaries/organism/otl.sqlite): '123[[5_addingOTL.R]] --> 124([interim/dictionaries/organism/otl.sqlite])'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: '5_addingOTL.R'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found.: '_No changelog found._'
