# Evaluation Strategy

## Direct Checks

- verify file 'refseq.hg18.bed.txt' exists in package
- verify file 'cpgi.hg18.bed.txt' exists in package
- script_runs: annotateWithGeneParts() executes without error on methylDiff object
- script_runs: annotateWithFeatureFlank() executes without error on methylDiff object
- output_matches_reference: percentage overlap table for promoter/exon/intron categories matches vignette summary statistics (robust to minor floating-point rounding)
- output_matches_reference: percentage overlap table for CpGi/shores categories matches vignette summary statistics (robust to minor floating-point rounding)
- field_present: output table contains columns for promoter, exon, intron categories
- field_present: output table contains columns for CpGi and shores categories

## Expert Review

- Verify that annotateWithGeneParts() and annotateWithFeatureFlank() are called with appropriate parameters for hg18 genome version
- Confirm that annotation results are biologically sensible (e.g., percentage values sum to 100% or fall within expected genomic coverage ranges)
- Assess whether reported percentages align with known properties of differential methylation in promoters vs. introns vs. exons and CpG island vs. shore distributions
