# Evaluation Strategy

## Direct Checks

- verify file exists: methylKit R package available from github:al2na__methylKit
- script_runs: R script instantiates methylBase object using dataSim() with parameters (replicates=6, sites=1000)
- script_runs: calculateDiffMeth() executes on simulated methylBase with overdispersion='MN' and test='Chisq'
- output_matches_reference: returned object is of class methylDiff (verify class attribute)
- file_format_is: output object serializable and loadable as R methylDiff object, robust to R version within supported range

## Expert Review

- expert_review: Compare q-value distributions (histogram, median, mean) from overdispersion='MN' run versus uncorrected baseline run (overdispersion='none' or default); verify that 'MN'-corrected run produces higher q-values on average (more stringent), consistent with vignette claim that overdispersion correction increases test stringency
- expert_review: Assess whether observed q-value shift magnitude and direction align with known behavior of Möbius-Nobrega overdispersion correction in differential methylation testing
