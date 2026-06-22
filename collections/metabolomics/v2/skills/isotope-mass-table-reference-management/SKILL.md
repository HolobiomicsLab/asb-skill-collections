---
name: isotope-mass-table-reference-management
description: 'Use when when building a mass spectrometry analysis pipeline that requires exact mass lookups, molecular formula validation, or isotope abundance predictions. Specifically: (1) you are constructing a MolecularFormula class that needs to validate element symbols against known isotopes;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mzapy.isotopes
  - h5py
  - numpy
derived_from:
- doi: 10.1021/acs.analchem.3c01653
  title: mzapy
- doi: 10.1021/acs.jproteome.2c00313
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzapy_cq
    doi: 10.1021/acs.analchem.3c01653
    title: mzapy
  dedup_kept_from: coll_mzapy_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c01653
  all_source_dois:
  - 10.1021/acs.analchem.3c01653
  - 10.1021/acs.jproteome.2c00313
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotope-mass-table-reference-management

## Summary

Maintain and reference a dictionary of monoisotopic masses for chemical elements to enable accurate mass calculations in MS workflows. This skill underpins molecular formula validation, exact mass computation, and isotope-pattern prediction for multidimensional mass spectrometry data.

## When to use

When building a mass spectrometry analysis pipeline that requires exact mass lookups, molecular formula validation, or isotope abundance predictions. Specifically: (1) you are constructing a MolecularFormula class that needs to validate element symbols against known isotopes; (2) you must compute monoisotopic masses from element composition; (3) you are predicting MS adduct masses or isotope patterns ([M]+, [M+H]+, etc.); (4) your input data includes element symbols or molecular formulas that must be cross-checked against reference standards.

## When NOT to use

- Input contains only experimental m/z values with no element composition information—use a spectral database or peak-matching algorithm instead.
- Isotope abundances or fine isotope patterns are required—this skill provides monoisotopic masses only; use a full isotope-distribution model for isotopologue prediction.
- Element symbols are already verified and you only need fast mass lookup without validation—a simple dict lookup suffices without wrapper functions.

## Inputs

- Element symbol (string, e.g. 'C', 'H', 'N')
- MolecularFormula object or dict of {element: count} pairs
- MS adduct string (e.g. '[M+H]+', '[M-H]-')

## Outputs

- Monoisotopic mass (float, in Da)
- Validation status (boolean or error message)
- Adjusted molecular formula for adduct (dict or MolecularFormula)

## How to apply

Populate a _ELEMENT_MONOISO_MASS dictionary with at least 24 commonly detected elements (C, H, N, O, S, P, F, Cl, Br, I, Si, etc.) and their exact monoisotopic masses, following IUPAC or NIST reference standards. When a MolecularFormula object is instantiated or validated, iterate through its element keys and check each against this dictionary using a valid_element() function; raise an error if an unknown symbol is encountered. To compute the monoisotopic mass of a formula, sum the stored masses weighted by each element's count. Use this lookup table as the authoritative reference for all downstream mass calculations (adduct prediction, isotope pattern simulation, exact-mass filtering). Document the source and version of the reference data (e.g., NIST, IUPAC 2021) to enable reproducibility and future updates.

## Related tools

- **mzapy.isotopes** (Provides the MolecularFormula class and utility functions (valid_element, monoiso_mass, ms_adduct_formula, predict_m_m1_m2) that depend on the monoisotopic mass table for validation and mass calculation.) — https://github.com/PNNL-m-q/mzapy
- **h5py** (Used to store and retrieve MZA metadata and mass reference data from HDF5 files if isotope tables are persisted alongside experimental spectra.)
- **numpy** (Supports vectorized lookups and mass computations across arrays of formulas or m/z values.)

## Examples

```
from mzapy.isotopes import valid_element, monoiso_mass; assert valid_element('C'); mass = monoiso_mass({'C': 3, 'H': 8, 'O': 2}); print(f'Monoisotopic mass: {mass:.4f} Da')
```

## Evaluation signals

- All 24 (or more) documented elements are present in _ELEMENT_MONOISO_MASS with monoisotopic masses matching NIST/IUPAC references (e.g., C = 12.0, H ≈ 1.0078, O ≈ 15.9949).
- valid_element() returns True for valid symbols and raises ValueError for unknowns; unit tests pass for edge cases (lowercase, typos, non-existent elements).
- monoiso_mass({'C': 3, 'H': 8, 'O': 2}) returns the sum 3×12.0 + 8×1.0078 + 2×15.9949 ≈ 92.047, verifiable against standard chemistry databases.
- ms_adduct_formula('C3H8O2', '[M+H]+') correctly adjusts the element count and returns the modified formula; predicted m/z matches expected values within 5 ppm.
- All example code snippets from mzapy documentation execute without KeyError or ValueError when looking up element masses.

## Limitations

- Only monoisotopic masses are provided; full isotope-abundance distributions (for prediction of M+1, M+2 peaks) require a separate isotope-model lookup.
- The table covers 24 common elements but may not include rare or exotic isotopes; users must extend _ELEMENT_MONOISO_MASS if analyzing uncommon elements.
- Mass values are static and tied to a specific reference year/version (e.g., IUPAC 2021); updates to atomic mass standards require manual table maintenance.
- Validation occurs at instantiation time; if a reference table is corrupted or loaded incorrectly, errors may propagate silently to downstream mass calculations until validation is explicitly invoked.

## Evidence

- [other] _ELEMENT_MONOISO_MASS dictionary and supporting validation functions: "Populate _ELEMENT_MONOISO_MASS with 24 elements and their monoisotopic masses as documented."
- [other] Element validation routine in isotopes module: "Implement utility validation functions: valid_element (checking against _ELEMENT_MONOISO_MASS dictionary)"
- [other] Monoisotopic mass calculation from formula: "monoiso_mass (returning exact mass from element dict)"
- [other] Adduct-adjusted mass and isotope prediction: "ms_adduct_formula (computing formula delta), and predict_m_m1_m2 (isotope prediction)"
- [other] MolecularFormula class integration: "The mzapy package provides an interface to unprocessed MS data in the MZA format, which includes data structure implementations for molecular formula representation within the isotopes module."
