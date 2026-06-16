# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How does the parser convert a tagged tabular file (using export tags like #<table_name>.id and #.<field_name>) into the nested JSON structure required by the directive resolvers?: 'This structure can be mimicked using the export part of the tagging system mentioned in the :doc:`tagging` section of this documentation, and tagged tabular files are acceptable input for the'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Tagged tabular files are converted to nested JSON by mapping each table column with #<table_name>.id tags to record names and each column with #.<field_name> tags to field names and values, producing a JSON structure where table names contain records with field key-value pairs.: 'The JSON structure above is shown below using export tags.

+--------+---------------------+-------------------+-------------------+
| #tags  | #<table_name_1>.id  | #.<field_name_1>  |'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Tagged tabular file (CSV or TSV format) with export tags in column headers: 'The extract command of MESSES supports turning tabular data into JSON. This is done by adding a layer of tags on top of the data.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Nested JSON object with table-record-field hierarchy matching tagged column structure: 'The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history found in source material: '_No changelog found._'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No concrete specification, code snippet, or reference implementation of the tag syntax (#<table_name>.id, #.<field_name>) or parser logic provided in accessible documentation: '_No changelog found._'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No example input (tagged tabular file) or expected output (nested JSON structure) is provided to validate parser behavior: '_No changelog found._'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Definition of 'nested JSON structure consumed by directive resolvers' is not explicitly specified in available material: '_No changelog found._'
