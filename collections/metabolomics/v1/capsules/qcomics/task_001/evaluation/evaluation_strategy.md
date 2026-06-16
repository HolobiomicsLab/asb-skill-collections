# Evaluation Strategy

## Direct Checks

- verify that inputs include a concrete Sciex Multiquant TXT export file (from github:ricoderks__QComics repository or a publicly deposited dataset)
- verify file_format_is TXT or plain text
- verify that expected_outputs table contains at least these named fields: sample_name, injection_index, sequence_position, qcpool_status (or equivalent structured record)
- verify row_count_equals is non-zero (at least one QCpool identified)
- verify script_runs successfully on the input TXT file without errors
- verify output_matches_reference if a reference QCpool annotation file exists in the repository; otherwise, no canonical answer — multiple valid parsing strategies may exist depending on Multiquant TXT format version and QCpool naming conventions

## Expert Review

- confirm that sample identification logic correctly distinguishes QCpool samples from analytical samples (relies on domain knowledge of metabolomics nomenclature and Sciex Multiquant export conventions)
- confirm that injection_index and sequence_position assignments are accurate and semantically meaningful for quality control assessment
- confirm that detected QCpool interval regularity is biologically and analytically plausible (expert judgment on what constitutes 'regular intervals')
