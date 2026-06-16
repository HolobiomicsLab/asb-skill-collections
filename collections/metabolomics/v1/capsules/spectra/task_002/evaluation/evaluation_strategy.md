# Evaluation Strategy

## Direct Checks

- verify that calling spectraData() on a MsBackendTest instance with only user-supplied spectra variables (msLevel, rtime) returns a DataFrame
- verify that the returned DataFrame contains all core spectra variables as columns
- verify that columns corresponding to missing core spectra variables (e.g., centroided, polarity) contain NA values
- verify that fillCoreSpectraVariables() is invoked during spectraData() execution by inspecting function call stack or code inspection

## Expert Review

- expert review of whether the set of core spectra variables returned matches the documented specification for core variables
- expert review of whether NA-filling behavior is appropriate and consistent with the MsBackend API contract
