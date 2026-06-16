# Evaluation Strategy

## Direct Checks

- verify that github:kbseah__mass2adduct repository contains cardinal2msimat() function with callable signature
- verify that cardinal2msimat() function accepts MSProcessedImagingExperiment or MSContinuousImagingExperiment objects as input
- verify that cardinal2msimat() returns an object of class msimat
- verify that the returned msimat object can be passed directly to massdiff() without preprocessing errors
- verify that massdiff() output can be passed directly to adductMatch() without preprocessing errors
- script_runs: execute cardinal2msimat() → massdiff() → adductMatch() pipeline end-to-end on a test MSProcessedImagingExperiment or MSContinuousImagingExperiment object from Cardinal package; robust to dataset size up to 10,000 peaks
- verify output_matches_reference: pipeline produces a named list or data.frame with columns including mass difference values and adduct annotations, matching the structure documented in methods section

## Expert Review

- assess whether Cardinal object conversion preserves spatial metadata required for downstream corrPairsMSI() correlation analysis
- assess whether mass accuracy is maintained through the cardinal2msimat() conversion step and does not introduce systematic bias
- evaluate whether the interoperability path correctly handles both continuous and discrete imaging experiment formats without data loss
