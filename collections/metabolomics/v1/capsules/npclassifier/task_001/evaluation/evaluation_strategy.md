# Evaluation Strategy

## Direct Checks

- verify file exists at github:mwang87__NP-Classifier
- script_runs: execute Docker Compose startup sequence (docker network create nginx-net, make server-compose) without errors
- script_runs: send HTTP GET request to /classify endpoint with valid SMILES string (e.g., 'CC(=O)Oc1ccccc1C(=O)O') to running local server
- file_format_is: response body is valid JSON
- field_present: response JSON contains 'output' field
- field_present: response JSON contains 'input_2048' field (or evidence of input layer name)
- field_present: response JSON contains 'input_4096' field (or evidence of input layer name)
- value_in_range: HTTP status code equals 200
- robust to parameter choices: verify endpoint responds with structurally consistent JSON across multiple valid SMILES inputs

## Expert Review

- Assess whether returned classification scores or labels are chemically plausible for the input SMILES string (requires natural product chemistry expertise)
- Verify that response structure matches the documented API contract in the repository README or API specification (if available)
