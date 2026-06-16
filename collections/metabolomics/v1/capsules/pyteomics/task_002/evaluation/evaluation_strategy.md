# Evaluation Strategy

## Direct Checks

- verify file exists: h5py package installable via pip (check pip index or test installation in clean environment)
- verify file exists: hdf5plugin package installable via pip (check pip index or test installation in clean environment)
- script_runs: Python script that executes 'import pyteomics.mzmlb' without ImportError or ModuleNotFoundError
- script_runs: Python script that executes 'from pyteomics import mzmlb' without ImportError or ModuleNotFoundError
- script_runs: Python script that imports h5py, hdf5plugin, and pyteomics.mzmlb in sequence without error
- contains_substring: output of 'python -c "import pyteomics.mzmlb; print(dir(pyteomics.mzmlb))"' contains at least one function or class name (e.g. 'read', 'MzMLb', 'IndexedMzMLb') indicating module is loaded — no canonical answer for specific exported names

## Expert Review

- confirm that h5py and hdf5plugin together provide the HDF5 and mzMLb codec support needed for pyteomics.mzmlb to function
- verify that the installed versions of h5py and hdf5plugin are compatible with the pyteomics version being tested
