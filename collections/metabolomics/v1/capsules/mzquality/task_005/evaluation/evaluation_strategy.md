# Evaluation Strategy

## Direct Checks

- verify file 'example.tsv' exists in the mzQuality package repository or deposited dataset
- script_runs: execute buildExperiment(example.tsv, primaryAssay='<identified column>', secondaryAssay=NULL) without error in R environment with mzQuality loaded
- field_present: verify 'ratio' assay is present in resulting SummarizedExperiment object
- output_matches_reference: extract all 'ratio' assay values from output and verify they equal corresponding primary assay values (robust to floating-point precision within machine epsilon)

## Expert Review

- verify that the conditional behaviour documented in the article (divisor defaults to 1 when secondaryAssay is omitted) is correctly implemented and produces mathematically sound ratio calculations
- confirm that the ratio assay calculation logic aligns with the stated package design for handling missing secondary assay specifications
