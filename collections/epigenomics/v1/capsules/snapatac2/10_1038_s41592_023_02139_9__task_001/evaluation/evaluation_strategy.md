# Evaluation Strategy

## Direct Checks

- verify that tl.spectral function exists and is callable in the installed SnapATAC2 package from github:scverse__SnapATAC2
- verify that a dataset with ≥10 million cells can be loaded or constructed (either from public accession, SnapATAC2 built-in datasets, or synthetic data with documented cell count)
- verify wall-clock execution time is logged and reported as a single numeric value in seconds
- verify peak memory usage is logged and reported as a single numeric value in GB or MB
- verify that reported time complexity is O(n) or linear (no canonical answer for exact constant factor; multiple defensible profiling approaches acceptable)
- verify that reported space complexity is O(n) or linear (no canonical answer for exact constant factor; multiple defensible profiling approaches acceptable)

## Expert Review

- assess whether wall-clock time and peak memory measurements are consistent with claimed linear scaling (expert judgment required to evaluate whether empirical results support the theoretical complexity claim given hardware, implementation details, and parameter choices)
- evaluate whether the benchmark dataset (≥10M cells) is representative and sufficiently large to meaningfully demonstrate scalability; assess appropriateness of profiling methodology
