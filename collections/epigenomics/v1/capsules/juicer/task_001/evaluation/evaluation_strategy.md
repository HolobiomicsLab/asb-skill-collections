# Evaluation Strategy

## Direct Checks

- verify file_exists: .hic output file is generated in the pipeline working directory
- verify file_format_is: output .hic file conforms to HiC file format specification (byte signature and internal structure)
- verify script_runs: Juicer pipeline execution completes without fatal errors on test FASTQ dataset
- verify row_count_equals or value_in_range: output .hic file size is non-zero and within expected range for Hi-C maps (robust to parameter choices in alignment and resolution settings)
- verify output_matches_reference: generated .hic file can be loaded and parsed by standard Hi-C analysis tools (e.g., Juicer Tools), indicating structural validity

## Expert Review

- Confirm that Hi-C contact matrix statistics (e.g., read pair counts, chromosome interaction distribution, cis/trans ratio) are consistent with expected values for the input dataset
- Assess whether the generated .hic artifact exhibits expected biological signal (e.g., TAD structure, centromeric clustering) when visualized, versus artifactual patterns
