# Evaluation Strategy

## Direct Checks

- verify file exists in asari source repository (github:shuzhao-li-lab/asari) containing COMP_COMPOSITEMAP construction logic
- verify scipy.signal.find_peaks is imported and called exactly once per composite map construction in the peak detection module
- verify function signature of composite map builder accepts summed intensity array as input
- script_runs: execute asari peak detection pipeline on test dataset (github:shuzhao-li/data/tree/main/data) and confirm no errors occur during composite map construction and scipy.signal.find_peaks invocation
- value_in_range: confirm number of find_peaks function calls in execution trace equals 1 (not N where N = number of samples), parameter-sensitive to sample count and batch processing configuration
- file_format_is: verify output composite peak detection result is a structured record (JSON, pickle, or numpy array) containing detected peak indices and properties

## Expert Review

- Confirm that composite map construction (COMP_COMPOSITEMAP) correctly sums intensity values across all samples at each retention time and m/z coordinate before peak detection
- Confirm that single composite-level find_peaks call produces equivalent or superior peak detection sensitivity compared to per-sample peak detection baseline (RESULT_COMPOSITE_EFFICIENCY claim)
- Verify prominence control parameters used in scipy.signal.find_peaks call are appropriate for metabolomics data and documented in code or configuration
