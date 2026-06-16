# Evaluation Strategy

## Direct Checks

- verify that loosolab/TOBIAS repository contains an ATACorrect module or command
- verify that ATACorrect module accepts a BAM file as input
- verify that ATACorrect module produces a bigWig output file
- script_runs: ATACorrect executes without fatal errors on a valid ATAC-seq BAM input
- file_format_is: output file has .bw or .bigwig extension
- file_exists: output bigWig file is non-empty and readable by standard bigWig tools (e.g., bigWigInfo)
- verify output bigWig contains numerical signal values (robust to parameter choices in bias correction algorithm)

## Expert Review

- evaluate whether bias-corrected signal track shows expected depletion patterns (footprints) consistent with transcription factor binding sites
- assess whether the bias correction meaningfully reduces Tn5 insertion sequence bias (e.g., AT-richness artifacts) compared to raw signal
- confirm that the bigWig signal values are in a reasonable dynamic range for ATAC-seq accessibility quantification
