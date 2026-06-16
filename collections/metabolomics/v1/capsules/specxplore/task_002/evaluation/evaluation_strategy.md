# Evaluation Strategy

## Direct Checks

- verify file exists at the path specified in inputs (session data object .pkl or equivalent serialized format)
- script_runs: execute the dashboard initialization code without raising exceptions
- verify dashboard HTTP endpoint becomes accessible (e.g., responds to GET request or binds to expected port within timeout)
- verify no error logs or warnings appear in application stderr during initialization, robust to minor logging variation
- verify dashboard process remains running for at least 10 seconds after initialization completes

## Expert Review

- confirm that the loaded session data object contains the expected schema (presence of t-SNE embeddings, metadata, spectral similarity matrices, and network graph structures)
- validate that all interactive UI elements (spectral selection, filtering, embedding navigation) respond to user input without hangs or crashes
- assess whether the initialized dashboard state matches the original session configuration saved in the input file (embedding parameters, selected features, view settings)
