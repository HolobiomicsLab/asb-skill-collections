# Evaluation Strategy

## Direct Checks

- verify file 'hatch.toml' exists in the repository root
- verify file 'pyproject.toml' exists in the repository root
- script_runs: execute 'hatch run hatch-test' in the scanpy repository directory and confirm exit code is 0
- script_runs: execute 'hatch test' in the scanpy repository directory and confirm exit code is 0
- output_matches_reference: verify that test execution log contains no non-skipped test failures (robust to test count and parameter changes)

## Expert Review

- Verify that the Hatch environment configuration in hatch.toml correctly specifies the test environment and pytest invocation
- Confirm that all declared test dependencies in the Hatch configuration are correctly resolved and available
