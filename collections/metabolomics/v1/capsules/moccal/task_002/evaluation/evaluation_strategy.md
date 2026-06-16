# Evaluation Strategy

## Direct Checks

- verify that the HinesLab/MOCCal repository is accessible and contains executable code
- verify file_exists: check that example data files (RawDT or UserDT formats) are present in the repository or linked deposits
- script_runs: execute the class-assignment module/function on provided example data without errors
- output_matches_reference: verify that the output table structure contains at least a feature identifier column and a biomolecular class label column
- file_format_is: confirm output is a structured table (CSV, TSV, or DataFrame-exportable format) with no missing required fields
- row_count_equals: verify that the number of rows in output table matches the number of input features in the example data
- field_present: confirm each row contains a valid class label assignment (no null/empty class values)

## Expert Review

- assess whether assigned class labels are biochemically plausible for TWIM-MS lipid, protein, metabolite, or other biomolecular classes given the input arrival-time and m/z features
- evaluate whether the class-assignment logic correctly handles the distinction between arrival time (detector readout) and drift time (cell residence time) as described in the tool documentation
- review whether the assignment operates independently of prior feature identification, as claimed in the finding
