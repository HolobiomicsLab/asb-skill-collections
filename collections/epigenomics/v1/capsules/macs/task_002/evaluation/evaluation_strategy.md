# Evaluation Strategy

## Direct Checks

- verify file CTCF_ChIP_200K.bed.gz exists in github:macs3-project__MACS/test directory
- verify file CTCF_Control_200K.bed.gz exists in github:macs3-project__MACS/test directory
- script_runs: macs3 filterdup on CTCF_ChIP_200K.bed.gz and CTCF_Control_200K.bed.gz without error
- script_runs: macs3 predictd on filtered ChIP file without error
- script_runs: macs3 pileup on filtered ChIP file with fragment length parameter without error
- file_exists: pileup BEDGRAPH output file with format .bdg
- script_runs: macs3 bdgcmp comparing pileup BEDGRAPH and control lambda track without error
- file_exists: local_lambda.bdg file in output directory
- file_exists: p-value or q-value score BEDGRAPH file in output directory
- script_runs: macs3 bdgopt on score BEDGRAPH without error
- script_runs: macs3 bdgpeakcall on optimized score track without error
- file_format_is: all output BEDGRAPH files conform to BEDGRAPH specification (chromosome, start, end, value columns)
- row_count_equals: pileup BEDGRAPH is non-empty (at least one data row beyond header)

## Expert Review

- pileup BEDGRAPH coverage values are realistic for ChIP-Seq signal (positive, reasonable magnitude relative to sequencing depth)
- local_lambda.bdg background estimates are appropriate and smaller than or comparable to ChIP pileup signal in non-peak regions
- p/q-value score BEDGRAPH shows expected statistical enrichment pattern (higher scores at true peak regions, lower in background)
- peak calls from bdgpeakcall output align with known or expected CTCF binding sites based on CTCF tutorial dataset documentation
