# Evaluation Strategy

## Direct Checks

- verify file outputs/ERR188044_sparse_anchors.mapping_rates.txt exists and contains numeric mapping rate and NumReads Pearson values; robust to parameter choices in seed representation
- verify file outputs/ERR188044_fixed_k_anchors.mapping_rates.txt exists and contains numeric mapping rate and NumReads Pearson values; robust to parameter choices in seed representation
- verify file outputs/ERR188044_reference_kmers.mapping_rates.txt exists and contains numeric mapping rate and NumReads Pearson values; robust to parameter choices in seed representation
- value of NumReads Pearson field in outputs/ERR188044_sparse_anchors.mapping_rates.txt is >= 0.99999995
- value of NumReads Pearson field in outputs/ERR188044_fixed_k_anchors.mapping_rates.txt is >= 0.99999995
- value of NumReads Pearson field in outputs/ERR188044_reference_kmers.mapping_rates.txt is >= 0.99999995
- verify that mapping rate (percentage of reads mapped) across all three seed variants differs by < 1% absolute; parameter-sensitive to index and read set

## Expert Review

- assess whether the reported NumReads Pearson values (≥0.99999995) across seed variants are statistically consistent with the claim that seed granularity was not the root cause of mapping discrepancy
- evaluate whether the choice of sparse fixed-k anchors, reference k-mer variants, and unitig-constrained MEMs constitutes a sufficiently comprehensive variant space to establish robustness to seed representation
- review the experimental design to confirm that the alternative seed representations were applied to the same ERR188044 reads and GRCh38 cDNA index used in the reported baseline (36.35M 76bp PE)
