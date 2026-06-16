# Evaluation Strategy

## Direct Checks

- verify that _mass_grid_mapping.csv file exists in expected output location
- verify file format is CSV with expected columns for m/z alignment mappings
- verify script runs without errors when processing mzML inputs through COMP_MASSGRID dispatcher
- verify that studies with ≤10 samples invoke ALG_PAIRWISE_ALIGN by checking function call logs or code execution trace
- verify that studies with >10 samples invoke ALG_LANDMARK_PEAKS and/or ALG_NN_CLUSTERING by checking function call logs or code execution trace
- verify output _mass_grid_mapping.csv row count is greater than zero and contains valid m/z alignment records
- verify that all input mzML files are successfully parsed by pymzml without parse errors

## Expert Review

- expert review of alignment quality: assess whether m/z alignment in _mass_grid_mapping.csv achieves expected mass separation and alignment precision given high mass resolution settings
- expert review of algorithm selection logic: confirm that the conditional dispatch (sample count threshold ≤10 vs >10) is correctly implemented and produces scientifically defensible alignments for both small and large studies
- expert review of mass track consistency: verify that aligned mass tracks in the output grid are reproducible and trackable back to original EICs per the asari design principle
