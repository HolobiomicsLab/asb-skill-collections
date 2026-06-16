# Evaluation Strategy

## Direct Checks

- verify file test_caffeine.py exists in github:JosieHong__FIDDLE repository
- verify file_format_is CSV or TSV for the inference output produced by test_caffeine.py
- script_runs: test_caffeine.py executes without fatal errors against GNPS spectra for caffeine (C8H10N4O2) using v2.0.0 checkpoint
- verify output contains at least one column with formula predictions or scored candidates
- verify output contains at least one row of data (beyond headers) for caffeine compound
- verify field_present: output includes a score, probability, or ranking column for formula candidates

## Expert Review

- expert_review: caffeine molecular formula C8H10N4O2 is correctly identified or ranked within top-k predictions by the model
- expert_review: the Siamese rescore architecture (FormulaEncoder + RescoreHead) produces chemically plausible formula rankings compared to ground truth or reference mass spectroscopy data
