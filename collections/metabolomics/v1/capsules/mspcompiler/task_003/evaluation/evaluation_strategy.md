# Evaluation Strategy

## Direct Checks

- Verify that mspcompiler package contains extract_ri function (file_exists: function definition in package source or documentation)
- Verify that mspcompiler package contains assign_ri function (file_exists: function definition in package source or documentation)
- Verify script_runs: R script that calls library(mspcompiler); extract_ri() on a NIST ri.dat file completes without error
- Verify script_runs: R script that calls assign_ri() to populate RI field in compiled EI library object completes without error
- Verify field_present: resulting R object or MSP output file contains 'RI' field or equivalent retention index metadata field
- Verify value_in_range or contains_substring: RI values in output are numeric and match expected format for Kovats retention indices (typically integer or decimal values in range ~500–3500)

## Expert Review

- Confirm that RI values extracted from NIST ri.dat file are chemically and analytically plausible for the corresponding compounds (expert judgment of retention index correctness)
- Confirm that RI assignment to library entries is chemically consistent — i.e., compounds are matched to correct RI values and not transposed or corrupted
