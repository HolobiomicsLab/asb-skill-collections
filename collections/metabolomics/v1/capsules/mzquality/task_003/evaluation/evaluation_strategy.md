# Evaluation Strategy

## Direct Checks

- verify that batch-corrected experiment object (SummarizedExperiment) exists as input
- verify file_exists for RSDQC values table (tab-delimited or CSV format) computed across all internal standard candidates
- verify that output table contains at least one row per compound with columns for compound identifier, internal standard candidates, and their corresponding RSDQC values
- verify that output table field_present: 'recommended_internal_standard' or equivalent column identifying the internal standard with minimum RSDQC per compound
- verify output_matches_reference against reported recommendation table location in article (if deposited), or verify table structure is consistent with mzQuality export format

## Expert Review

- verify that RSDQC calculation methodology matches article description: relative standard deviation computed over batch-corrected QC sample ratios (compound / internal standard) for each candidate pairing
- verify that the lowest RSDQC selection logic is correctly applied per compound (no ties, handling of missing values, numerical precision)
- assess whether batch-correction step (using pooled SQC samples) was applied before RSDQC computation, as stated in article scope
