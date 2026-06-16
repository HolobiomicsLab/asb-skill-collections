# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does the SMART 3 system query the TensorFlow Serving instance to retrieve and validate model metadata, and what information about input names must be extracted?: 'We pass through tensorflow serving at this url: /model/metadata. If the model input names change, then we need to change it in the code'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The SMART 3 system queries model metadata via an HTTP GET call to the /model/metadata endpoint on a TensorFlow Serving instance, from which model input names must be extracted and verified, as changes to these input names require corresponding code updates.: 'We pass through tensorflow serving at this url: /model/metadata. If the model input names change, then we need to change it in the code'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] TensorFlow Serving instance URL and endpoint path (/model/metadata): 'We pass through tensorflow serving at this url: /model/metadata'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Parsed model metadata including input names and response validation status as JSON: 'If the model input names change, then we need to change it in the code'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] tensorflow serving: 'We pass through tensorflow serving at this url'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found for the github:mwang87__DeepSAT repository, making it unclear whether model input names have changed since initial deployment or if breaking changes exist.: '_No changelog found._'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] TensorFlow Serving endpoint URL is referenced but the exact hostname, port, and protocol (http/https) are not provided in the discussion section.: 'Source: github:mwang87__DeepSAT'
