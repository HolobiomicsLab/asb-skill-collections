# Evaluation Strategy

## Direct Checks

- verify that inputs include a bias-corrected bigWig file (format: .bw or .bigWig) and a BED file defining accessible genomic regions
- verify that the expected output file exists and is in bigWig format (.bw or .bigWig)
- verify that the output bigWig contains footprint score values (numeric, typically float or integer) across the input regions
- verify that the output bigWig has the same genomic coordinate system and chromosome naming as the input files
- verify that all genomic regions from the input BED file are represented in the output (no regions dropped or silently filtered)
- script_runs: confirm that the ScoreBigwig command or equivalent TOBIAS scoring function executes without errors on the provided inputs

## Expert Review

- assess whether computed footprint scores are biologically plausible in magnitude and distribution (e.g., negative or near-zero scores over bound regions, reflecting characteristic Tn5 insertion depletion)
- confirm that the scoring method correctly implements the intended footprint-scoring algorithm (e.g., whether it computes depletion of insertions as described in the TOBIAS methodology)
- evaluate whether the output tracks show expected patterns: depleted signal at known transcription factor binding sites and elevated signal in flanking nucleosome-free regions
