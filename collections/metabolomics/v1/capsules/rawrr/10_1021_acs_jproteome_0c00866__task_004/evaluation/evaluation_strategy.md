# Evaluation Strategy

## Direct Checks

- file_exists: verify that 20181113_010_autoQC01.raw is accessible via ExperimentHub accession EH4547 or MassIVE dataset MSV000086542
- script_runs: verify that rawrr::readIndex(f) executes without error on the sample file and returns a data frame with at least columns 'scan', 'MSOrder', and 'scanType'
- field_present: verify that the returned index data frame contains a 'scanType' or equivalent column that identifies PRM scan events
- output_matches_reference: for all consecutive pairs of PRM scans in the index, verify that the difference in scan number is exactly 22 (byte-for-byte exact match to reported cycle length)
- row_count_equals: robust to parameter choices — count the number of PRM scan events and confirm it is a positive integer consistent with a multi-cycle targeted experiment

## Expert Review

- Verify that the filter string or scanType identifier used to isolate PRM events from the index correctly distinguishes parallel reaction monitoring scans from other MS/MS modes (e.g., DDA, full scan)
- Confirm that a delta of 22 scans between consecutive PRM events is consistent with the documented instrument configuration and expected cycle structure for the autoQC01 experiment
- Assess whether any missing or irregular scan numbers (gaps > 22, or non-uniform spacing) warrant investigation into data quality or scan type classification errors
