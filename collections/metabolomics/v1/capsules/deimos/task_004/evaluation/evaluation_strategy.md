# Evaluation Strategy

## Direct Checks

- verify file github:pnnl__deimos can be cloned from https://github.com/pnnl/deimos
- verify dataset MSV000091746 is accessible via ftp://massive.ucsd.edu/v01/MSV000091746
- verify Snakemake workflow execution completes without errors using provided YAML configuration
- verify all final HDF5 output artifacts exist (file_exists check on output .h5 files)
- verify output HDF5 files are valid HDF5 format using h5py or similar tool
- verify Snakemake reports successful completion of all workflow rules (script_runs with exit code 0)

## Expert Review

- confirm that HDF5 output structure and content are consistent with DEIMoS workflow specification
- validate that feature detection, alignment, and calibration steps produced chemically plausible results
- assess whether output datasets contain expected dimensional data (m/z, drift_time, retention_time, intensity) without corruption
