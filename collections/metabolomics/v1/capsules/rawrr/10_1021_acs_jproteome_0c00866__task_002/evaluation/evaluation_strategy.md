# Evaluation Strategy

## Direct Checks

- file_exists: verify that rawrr::sampleFilePath() returns a valid .raw file path accessible to the R environment
- script_runs: execute rawrr:::.benchmark() with rawrr::readSpectrum on the sample raw file and confirm the function completes without error
- output_matches_reference: extract the 'spectra-per-second' throughput metric from benchmark output and verify it matches the reported figure cited in the article (exact numeric value required; robust to minor floating-point variation ±5%)
- field_present: confirm the benchmark output object contains a named field or column explicitly labeling throughput in 'spectra/second' or 'spectra per second' units
- value_in_range: verify the measured throughput is positive and within a physically plausible range for single-threaded spectrum reading on commodity hardware (candidate range: 100–100,000 spectra/second; expert review required to validate range)

## Expert Review

- Assess whether the reported spectra-per-second throughput is consistent with claimed performance goals and typical Orbitrap data complexity in the sample file
- Evaluate whether the benchmark experimental setup (single sample file, readSpectrum function, hardware environment) faithfully represents the conditions under which the throughput claim was originally measured and reported
- Determine whether any disclosed limitations (e.g., .NET runtime version, Windows vs. non-Windows OS differences, temporary file I/O overhead) materially affect reproducibility or comparability of the result
