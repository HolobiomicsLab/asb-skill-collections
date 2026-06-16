# Evaluation Strategy

## Direct Checks

- verify file exists: samtools executable or library at version >=1.9 installed in pipeline environment
- verify script_runs: samtools view command executes without error on a test BAM input file
- verify script_runs: samtools sort command executes without error on unsorted BAM input
- verify script_runs: samtools index command executes without error on coordinate-sorted BAM file, producing .bai index
- verify file_format_is: output BAM file conforms to SAM/BAM specification (magic number 'BAM1' or equivalent binary header)
- verify file_format_is: output .bai index file is valid samtools BAI format
- verify row_count_equals or value_in_range: number of aligned records in output BAM matches expected count from input SAM (within tolerance for filtering rules applied)
- verify output_matches_reference: sorted BAM file coordinate ordering is valid (read positions are non-decreasing within reference sequences)

## Expert Review

- confirm that SAM/BAM filtering criteria (e.g., MAPQ threshold, flag filters) are appropriate for Hi-C data and match documented pipeline defaults
- confirm that sort order (coordinate vs. queryname) and indexing strategy are consistent with downstream normalization and analysis stages
- assess whether samtools version constraint (>=1.9) is justified by feature or performance requirements in the SAM processing stage
