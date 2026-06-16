# Evaluation Strategy

## Direct Checks

- verify that asari can be installed from github:shuzhao-li-lab/asari and runs without errors on Python 3.8+
- verify that mzML test files are available from github:shuzhao-li/data/tree/main/data or a public metabolomics repository (MetaboLights/MassIVE)
- file_exists: performance_log.csv or equivalent structured output containing wall-clock execution time and peak memory usage
- value_in_range: wall-clock time increases monotonically or sub-linearly as sample count increases from 10 to 50 to 100+ samples (no canonical answer for exact scaling exponent; parameter-sensitive to hardware and file sizes)
- value_in_range: peak memory usage remains below laptop physical RAM limit (typically 8–16 GB) at 100+ sample threshold, robust to typical consumer hardware configurations
- output_matches_reference: reported scalability metric (samples processed per unit time, or memory per sample) is consistent with claim '>1000 samples on a laptop' stated in article abstract or results section

## Expert Review

- assess whether wall-clock time and memory measurements were collected under controlled, reproducible conditions (fixed hardware specs, single-threaded vs. multi-threaded configuration, consistent input file sizes)
- evaluate whether the tested mzML files are representative of real metabolomics datasets in terms of complexity, spectral density, and retention-time resolution
- determine whether measured scalability trajectory (time/memory vs. sample count) is extrapolatable to the claimed >1000-sample threshold or whether the tested range (10–100) is insufficient to validate the claim
- assess sensitivity of performance measurements to parameter choices (e.g., mass tolerance ppm, peak prominence thresholds, smoothing window size) that may affect per-sample processing cost
