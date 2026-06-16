# Evaluation Strategy

## Direct Checks

- verify file standard_data.csv exists in github:castratton__uafR repository
- script_runs: execute spreadOut(standard_data.csv) function without error in R environment
- output_matches_reference: returned list structure contains all fields specified in ARTIFACT-spreadOut-output documentation (byte-for-byte field names and count)
- field_present: verify each required output field is non-null in returned list object
- verify output list is compatible with downstream function inputs (mzExacto, categorate, exactoThese) — robust to parameter choices in downstream calls

## Expert Review

- assess whether spreadOut() output semantics (retention time sorting, m/z aggregation, CSV normalization) align with documented contract and support claimed data preparation workflow
- evaluate whether field names and structure match Agilent Unknowns Analysis default format as described
