# Evaluation Strategy

## Direct Checks

- verify file exists: trained motifset artifact (ARTIFACT-MOTIFSET) in input package or referenced deposit
- verify file exists: Spec2Vec model checkpoint from https://zenodo.org/records/15688609
- verify script runs: load Spec2Vec model from DATASET-ZENODO without errors
- verify script runs: load trained motifset and instantiate annotation lookup module without errors
- verify format_is: per-motif annotation output as structured record (JSON, CSV, or table) containing fields: motif_id, label, similarity_score
- verify field_present: each annotation record includes at least motif_id, label, and similarity_score fields
- verify value_in_range: all similarity scores are numeric and fall within [0.0, 1.0] or model's native range
- verify row_count_equals or robust_to_dataset_size: number of output annotation records matches or is traceable to input motifset cardinality
- verify output_matches_reference: annotation output structure and Spec2Vec scoring logic align with method description (no canonical answer—multiple valid annotation formats acceptable if fields are present)

## Expert Review

- assess semantic correctness: do assigned labels and similarity scores reflect genuine spectral/structural similarity as inferred by Spec2Vec, or are they arbitrary/nonsensical?
- assess completeness: does the annotation output cover all motifs in the input motifset, or are some unexpectedly missing?
- assess methodological alignment: verify that the Spec2Vec-based scoring mechanism matches the published MAG algorithm description for automated annotation
