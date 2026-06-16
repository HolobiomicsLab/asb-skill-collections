# Evaluation Strategy

## Direct Checks

- verify that a pre-processed xcms result object for faahKO dataset is available as input (file_exists or accessible via standard xcms workflow)
- verify that groupFeatures() function executes without error when called with SimilarRtimeParam(window=20s) on the xcms result object (script_runs)
- verify that the output object contains a featureDefinitions table with a grouping column (field_present)
- verify that the reported feature group count matches the unique group identifiers in the output object (output_matches_reference or value_in_range if a reference value is provided in the article)
- verify that a table of group sizes (frequency distribution of features per group) can be extracted from the output and matches any reported table in the article (output_matches_reference, robust to formatting variations)
- verify that all features in the input object are assigned to exactly one group (no missing or duplicate assignments)

## Expert Review

- assess whether the grouping result is biologically sensible: features assigned to the same group should show plausible co-elution patterns consistent with a 20-second retention time window
- assess whether the group size distribution is consistent with expected chromatographic behavior for the faahKO dataset (e.g., whether singleton and small-group frequencies are reasonable)
