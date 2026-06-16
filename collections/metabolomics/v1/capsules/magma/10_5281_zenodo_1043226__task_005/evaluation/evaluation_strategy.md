# Evaluation Strategy

## Direct Checks

- verify file docker-compose.yml exists in expected_outputs[0]
- file_format_is docker-compose.yml text/yaml or application/x-yaml
- contains_substring 'magmaweb' in docker-compose.yml
- contains_substring 'joblauncher' in docker-compose.yml
- contains_substring 'job' in docker-compose.yml (as a service name distinct from joblauncher)
- contains_substring 'pubchem' in docker-compose.yml
- contains_substring 'services:' in docker-compose.yml
- script_runs docker-compose config -f docker-compose.yml without errors (validates YAML syntax and service definitions)

## Expert Review

- expert_review: verify that docker-compose.yml service definitions correctly reflect component responsibilities (magmaweb=web interface, joblauncher=job queue manager, job=compute worker, pubchem=data source) as implied by NLeSC/MAGMa architecture
- expert_review: assess whether inter-service networking (environment variables, ports, volumes) enables the expected data flow among four components; no canonical answer without MAGMa deployment documentation
- expert_review: assess whether the composition extends or decomposes the single deployable artifact mentioned in scope in a chemically/informatically sensible way
