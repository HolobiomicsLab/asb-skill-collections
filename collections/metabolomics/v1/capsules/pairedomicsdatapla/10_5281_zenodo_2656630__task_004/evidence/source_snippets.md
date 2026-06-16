# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How should the validation system detect and flag URL fields in project JSON documents that contain whitespace characters, which are invalid in URLs?: 'Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The platform stores paired omics data projects using a JSON schema format (app/public/schema.json) that defines project structure, which serves as the basis for implementing field-level validation rules including URL format constraints.: 'The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Project JSON document with URL-typed fields: 'Each project page on [https://pairedomicsdata.bioinformatics.nl](https://pairedomicsdata.bioinformatics.nl) has a download button, which gives you the JSON document of the project.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Validation report listing all URL fields containing whitespace, with field names and flagged values: 'Warning to not include spaces in urls'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] npm: 'make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Which specific fields in the project JSON schema are designated as URL-typed and should be subject to the whitespace validation rule?: 'Warning to not include spaces in urls ([#75]'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] What constitutes 'spaces' in the context of URL validation—only space characters, or all whitespace (tabs, newlines, etc.)?: 'Warning to not include spaces in urls ([#75]'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Should the validation rule reject the document submission, issue a warning, or auto-correct by removing/encoding spaces?: 'Warning to not include spaces in urls ([#75]'
