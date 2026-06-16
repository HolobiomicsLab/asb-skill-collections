# Evaluation Strategy

## Direct Checks

- verify file exists in github:kopeckylukas__py-mamsi repository containing MamsiStructSearch.flattening or equivalent parameter definition
- verify script_runs: instantiate MamsiStructSearch with flattening='silhouette' (or equivalent API) on sample LC-MS data from kopeckylukas/py-mamsi-tutorials without error
- verify script_runs: instantiate MamsiStructSearch with default flattening method (constant-threshold or equivalent) on identical sample data without error
- file_format_is: cluster assignments output from silhouette-flattened pipeline is a structured record (CSV, JSON, or Python dict-like object) with fields: feature_id, cluster_id, and confidence_score or equivalent
- file_format_is: cluster assignments output from default-flattened pipeline matches same structure
- row_count_equals or value_in_range: number of structural clusters produced by silhouette method is within ±50% of default method (or report exact counts for expert review if outside range)
- value_in_range: silhouette score(s) reported by silhouette method are in range [−1, +1], robust to parameter choices
- field_present: cluster assignment outputs include field indicating flattening method used, allowing byte-for-byte verification of method identity

## Expert Review

- Compare silhouette-method vs. default-method cluster assignments for biological/chemical plausibility: do reassignments of features to different clusters align with expected m/z and RT proximity and known metabolite structure relationships?
- Evaluate whether silhouette-based flattening produces more stable or more interpretable cluster boundaries than constant-threshold method on the same dataset
- Assess whether the silhouette method resolves ambiguous borderline features (low distance to multiple clusters) more defensibly than the default approach, multiple defensible outcomes possible
