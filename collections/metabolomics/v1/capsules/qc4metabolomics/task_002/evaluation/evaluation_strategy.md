# Evaluation Strategy

## Direct Checks

- verify file exists in v1.0.0 release at github.com/stanstrup/QC4Metabolomics tagged v1.0.0
- file_format_is for workflow definition file (YAML, JSON, or XML)
- contains_substring in workflow file of 'workflow' or equivalent root declaration key
- output_matches_reference: workflow schema structure conforms to declared metabolomics QC domain (presence of quality control or metabolomics configuration elements — multiple defensible approaches to validation)

## Expert Review

- whether workflow definition semantically represents 'one complete workflow' as intended for metabolomics QC systems
- whether workflow structure is internally consistent and non-circular
- whether workflow parameters and task definitions are scientifically coherent for metabolomics quality control
