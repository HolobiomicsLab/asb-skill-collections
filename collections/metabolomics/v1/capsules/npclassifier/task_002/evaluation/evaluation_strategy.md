# Evaluation Strategy

## Direct Checks

- verify file exists: docker-compose.yml or equivalent orchestration file in github:mwang87__NP-Classifier repository
- script_runs: 'docker network create nginx-net' completes without error on agent system with Docker daemon
- script_runs: 'make server-compose' (or equivalent build command from repository) completes without error and yields running containerized NP-Classifier service
- file_format_is: TensorFlow Serving model artifact in models_folder directory is valid SavedModel format (contains saved_model.pb and variables/)
- script_runs: HTTP GET request to http://localhost:8501/v1/models/<model_name>/metadata (or configured TensorFlow Serving port) returns valid JSON response without connection error
- format_is: /metadata endpoint response is valid JSON conforming to TensorFlow Serving metadata schema
- field_present: response JSON contains 'signature_def' or equivalent model signature metadata block
- contains_substring: response JSON includes input layer names 'input_2048' and 'input_4096' (case-sensitive, byte-for-byte exact match)
- contains_substring: response JSON includes output layer name 'output' (case-sensitive, byte-for-byte exact match)

## Expert Review

- verify that returned metadata input/output layer names match the documented schema in the article (input_2048, input_4096, output) and are consistent with the Keras model architecture
- confirm that TensorFlow Serving is correctly proxying through the ARCH_TENSORFLOW_SERVING passthrough layer as described in README, not failing silently or returning cached/default metadata
