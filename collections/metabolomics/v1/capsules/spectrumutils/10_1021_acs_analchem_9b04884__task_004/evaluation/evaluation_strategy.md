# Evaluation Strategy

## Direct Checks

- verify file exists: mzspec:PXD004732:01650b_BC2-TUM_first_pool_53_01_01-3xHCD-1h-R2:scan:41840 is retrievable via USI mechanism
- script_runs: Python script instantiates spectrum_utils.fragment_annotation with neutral_loss parameter set to False
- script_runs: Python script instantiates spectrum_utils.fragment_annotation with neutral_loss parameter set to True
- output_matches_reference: fraction of peaks receiving interpretation (neutral_loss=False) computed and recorded as a single numeric value
- output_matches_reference: fraction of peaks receiving interpretation (neutral_loss=True) computed and recorded as a single numeric value
- value_in_range: difference between fractions (neutral_loss=True minus neutral_loss=False) is a non-negative number, robust to minor numerical precision differences

## Expert Review

- reported result for neutral loss annotation effect on peak interpretation fraction matches the article text or supplementary materials — requires domain knowledge to locate the specific claimed improvement and verify computation matches article methodology
