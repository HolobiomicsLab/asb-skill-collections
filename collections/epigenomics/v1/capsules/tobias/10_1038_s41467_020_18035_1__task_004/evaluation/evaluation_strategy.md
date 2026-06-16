# Evaluation Strategy

## Direct Checks

- verify that a publicly deposited ATAC-seq dataset (GEO or SRA accession) is retrievable and contains aligned reads in standard format (BAM/bedGraph)
- verify that a reference set of TF motif coordinates is provided as a structured file (BED or tabular format) with chromosome, start, end, and motif identity fields
- verify that the computed positional distribution table exists as a named artifact (TSV, CSV, or structured data frame)
- verify that the table contains at least two distinct categories (bound vs. unbound motif sites) and position-indexed Tn5 insertion count columns
- verify that insertion counts are numeric, non-negative, and row_count_equals the number of distinct position windows analyzed
- verify that script or pipeline used to compute positional distributions runs without fatal errors on the specified inputs
- verify output matches reference footprint signal: depletion of insertions at bound motif sites should be visually or statistically distinguishable from unbound sites (no canonical answer for exact magnitude; expert review required for biological interpretation)

## Expert Review

- confirm that the positional distribution pattern (insertion depletion at bound sites) is consistent with the ATAC-seq footprinting phenomenon described in the article and literature
- assess whether the magnitude and width of the observed footprint signal is biologically plausible for the TF(s) and cell type(s) under study
- evaluate whether the bound versus unbound site comparison is appropriately controlled (e.g., background chromatin accessibility, motif quality thresholds, statistical significance)
- judge whether the tabulation method and window definitions are methodologically sound and clearly documented
