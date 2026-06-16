# Evaluation Strategy

## Direct Checks

- verify file exists in github:rformassspectrometry__Spectra repository containing backendParallelFactor() method definition for MsBackendMzR class
- verify backendParallelFactor() method returns a factor object (R class 'factor')
- verify backendParallelFactor() method implementation extracts factor levels from dataStorage file names of spectra
- script_runs: execute chunk-wise splitting operation on MsBackendMzR instance with parallel factor applied to Spectra object, no errors
- script_runs: execute operation loading all spectra into memory without chunking on same MsBackendMzR instance, no errors
- memory usage metric from chunk-wise operation is lower than memory usage metric from non-chunked operation (robust to measurement tool, parameter-sensitive to data size and chunk boundaries)

## Expert Review

- peak-data memory demand reduction is substantive and not artifactual (accounts for memory allocation overhead, garbage collection timing, measurement precision)
- chunk-wise splitting implementation is correct and complete (no silent data loss, correct reassembly of results across chunks, consistent with Spectra API semantics)
