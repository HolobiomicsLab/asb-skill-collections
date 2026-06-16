# Evaluation Strategy

## Direct Checks

- verify file ARTIFACT-EMPCPD-JSON exists
- verify file_format_is ARTIFACT-EMPCPD-JSON application/json (parse and validate JSON structure)
- verify field_present in ARTIFACT-EMPCPD-JSON for 'list_of_features' (at minimum; robust to schema variants)
- verify field_present in ARTIFACT-EMPCPD-JSON for 'mz' (at minimum; robust to schema variants)
- verify field_present in ARTIFACT-EMPCPD-JSON for 'rt' (at minimum; robust to schema variants)
- verify script_runs: khipu build_empCpds invoked with configurable mz and rt tolerance parameters on input feature table without error

## Expert Review

- assess whether empirical compound groupings in ARTIFACT-EMPCPD-JSON are chemically sensible given the input mz/rt tolerances and feature table composition
- evaluate whether the mz/rt tolerance parameters used are appropriate for the LC-MS platform and metabolomics study design
