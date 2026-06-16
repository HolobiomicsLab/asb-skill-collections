# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How does the matrix directive handler resolve a matrix-type record from conversion directives against input JSON to produce a list of dictionaries, including support for headers, collation, field exclusion, sorting, filtering, and custom code?: 'The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON, and that that information is contained within a single table. By'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The matrix directive handler operates by iterating over records in a specified input JSON table to build dictionaries, with capabilities to sort and filter records using sort_by, sort_order, and test fields; collate records by a grouping field; map record fields to dictionary keys via headers; exclude fields with exclusion_headers; convert values to strings with values_to_str; or execute custom Python code for complex transformations.: 'The "headers" field will create a new dictionary for every record in the indicated table, but sometimes you might need to pull data from multiple records into a single new dictionary, and the'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Conversion directives file specifying matrix-type record transformation rules: 'The convert command of MESSES supports converting JSON data to another JSON format or another supported format. This is done by using conversion directives'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Input JSON data containing records to be transformed: 'The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] List of dictionaries representing resolved matrix-type records with mapped headers and applied transformations: 'To support the JSON-to-JSON conversion a relatively simple set of directives were developed'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] jsonschema: 'utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history provided in the discussion section: '_No changelog found._'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Source material was synthesized at 2026-06-15 but no concrete reference documentation, specification document, or code examples for the matrix directive handler are present in the provided section text: 'Synthesized at: 2026-06-15T14:01:02+00:00'
