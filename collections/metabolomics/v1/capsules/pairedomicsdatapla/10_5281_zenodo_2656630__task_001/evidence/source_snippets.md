# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What is the formal specification for the structure and constraints that uploaded JSON project documents must satisfy in the Pairing Omics Data Platform?: 'The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] A JSON schema file located at app/public/schema.json defines the required format for paired omics data projects in the platform.: 'The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Candidate JSON project document from user upload: 'You are free to add projects on [https://pairedomicsdata.bioinformatics.nl/add](https://pairedomicsdata.bioinformatics.nl/add). After submission, the project will be reviewed'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] JSON Schema definition file (app/public/schema.json): 'schema validation step that checks an uploaded JSON project document against app/public/schema.json'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Validation report (JSON) containing pass/fail status and list of schema violation errors (if any): 'reporting pass/fail and any validation errors'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] npm: 'make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact location and format of app/public/schema.json schema file (e.g., JSON Schema draft version, structure): 'Validate uploaded JSON documents ([#78]'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specification of which fields in a project document are mandatory versus optional for validation to pass: 'Made which fields are required more clear ([#42]'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Expected behavior and error message format when JSON validation fails (e.g., which validation library, error granularity): 'Validate uploaded JSON documents ([#78]'
