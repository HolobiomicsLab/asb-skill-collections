# Evaluation Strategy

## Direct Checks

- verify that input file exists and is readable HDF5 format
- verify that deimos.isotopes function executes without error on the peak-picked feature table
- verify that output table file exists and is in expected format (CSV or HDF5)
- verify that output table contains at least one row of annotated isotopologue data
- verify that output table contains required columns for isotope annotation (e.g., isotope_offset, parent_mz, charge_state)
- verify that all detected isotope offsets are consistent with C13 mass difference (~1.003 Da) for singly charged species
- verify that output matches structure described in deimos isotope detection documentation — no canonical answer for exact column names across versions, parameter-sensitive to input peak-picking thresholds

## Expert Review

- assess whether detected C13 isotopologue offsets are chemically reasonable and match expected isotope patterns for biological small molecules
- evaluate whether the isotope annotation quality and false-discovery rate are consistent with published deimos validation results
- review whether singly charged species assumption is appropriately applied and documented in output labelling
