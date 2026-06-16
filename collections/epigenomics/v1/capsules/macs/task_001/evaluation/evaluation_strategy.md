# Evaluation Strategy

## Direct Checks

- verify file CTCF_ChIP_200K.bed.gz exists in github:macs3-project__MACS/test directory
- verify file CTCF_Control_200K.bed.gz exists in github:macs3-project__MACS/test directory
- script_runs: macs3 callpeak command completes without error on the two input files
- file_exists: narrowPeak output file is generated
- file_format_is: narrowPeak output follows ENCODE narrowPeak format specification
- verify filterdup read count reported in callpeak log output is numeric and positive
- verify predicted fragment length d value reported in callpeak log output is numeric and positive
- value_in_range: predicted fragment length d is within biologically plausible range for chromatin (typically 100–300 bp), parameter-sensitive to organism and ChIP target

## Expert Review

- assess whether reported filterdup read count (number of reads after duplicate removal) is reasonable relative to input file size and CTCF ChIP-Seq expectations
- assess whether predicted fragment length d aligns with typical nucleosome-scale or protein-DNA interaction lengths for CTCF binding
- assess whether narrowPeak peak calls show expected genomic distribution and enrichment characteristics for CTCF (known motif-driven regulator)
