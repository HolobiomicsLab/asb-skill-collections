# Evaluation Strategy

## Direct Checks

- verify file exists: antiSMASH .gbk output for S. griseus SRR3309439 dataset in github:ablab__npdtools repository
- verify file exists: contigs.fasta for S. griseus SRR3309439 dataset in github:ablab__npdtools repository
- script_runs: MetaMiner execution with antiSMASH .gbk file as input completes without fatal errors
- script_runs: MetaMiner execution with contigs.fasta file as input completes without fatal errors
- file_format_is: MetaMiner output directory structure and log files present after .gbk run
- file_format_is: MetaMiner output directory structure and log files present after .fasta run
- contains_substring: MetaMiner .gbk run output does not contain 'AmfS' in results (no detection), robust to different output format variations

## Expert Review

- Confirm that AmfS absence in .gbk results represents a known/documented failure mode (manual discrepancy between FASTA and antiSMASH input handling)
- Evaluate whether MetaMiner .fasta results correctly detect AmfS and that detection is biologically plausible
- Assess whether the input discrepancy observed is consistent with documented differences in how antiSMASH .gbk and raw .fasta files are parsed by MetaMiner
