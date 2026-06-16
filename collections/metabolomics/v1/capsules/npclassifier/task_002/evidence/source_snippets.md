# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Does the TensorFlow Serving endpoint at /model/metadata successfully return model metadata including the correct input and output layer names when queried on the running Dockerized NP-Classifier server?: 'We pass through tensorflow serving at this url:

```/model/metadata```

If the model input names change, then we need to change it in the code'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The expected model layer names that should be returned by the /model/metadata endpoint are input layers 'input_2048' and 'input_4096', and output layer 'output'.: 'Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output"'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Running NP-Classifier Docker container with TensorFlow Serving endpoint: 'We pass through tensorflow serving at this url'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Model metadata JSON response containing input and output layer names: 'Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output"'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] docker: 'you need docker and docker-compose'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] docker-compose: 'you need docker and docker-compose'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] TensorFlow Serving: 'We pass through tensorflow serving at this url'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, breaking changes, or release notes for the NP-Classifier project.: '_No changelog found._'
