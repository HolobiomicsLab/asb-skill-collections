---
name: molecular-formula-representation-and-manipulation
description: Use when you need to represent, validate, and manipulate molecular compositions
  in MS analysis—specifically when annotating precursor or product ions with elemental
  formulas, computing monoisotopic masses for formula-to-charge assignments, predicting
  isotope patterns ([M]+, [M+H]+, [M+Na]+, etc.).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - mzapy
  - h5py
  - numpy
  - MZA converter
  techniques:
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Molecular Formula Representation and Manipulation

## Summary

Design and implement a MolecularFormula data structure as a collections.UserDict subclass with element-wise arithmetic operations and mass calculations to support isotope annotation and MS adduct prediction in multidimensional mass spectrometry workflows. This skill enables programmatic representation of molecular compositions, validation against known elements, and systematic formula transformations required for ion identification.

## When to use

Apply this skill when you need to represent, validate, and manipulate molecular compositions in MS analysis—specifically when annotating precursor or product ions with elemental formulas, computing monoisotopic masses for formula-to-charge assignments, predicting isotope patterns ([M]+, [M+H]+, [M+Na]+, etc.), or performing formula arithmetic (adding/subtracting H, Na, K, NH4, HCOO, CH3COO groups during adduction). Required when MS metadata includes PrecursorMonoisotopicMz or PrecursorCharge fields and you must resolve which molecular formula and adduct combination explains the observed m/z.

## When NOT to use

- Input is already a validated, read-only isotope pattern table or feature matrix; use direct lookup instead.
- You only need to store or display formulas without performing arithmetic or adduct transformations; a simple string field suffices.
- Molecular formula cannot be unambiguously resolved from m/z and charge alone (e.g., degenerate isomers); prioritize orthogonal separation data (LC retention, ion mobility drift time) before formula assignment.

## Inputs

- elemental composition as dict(str: int) mapping element symbols to atom counts
- MolecularFormula instance
- MS adduct string (e.g., '[M+H]+', '[M-H]-')
- monoisotopic mass (float, in Da)

## Outputs

- MolecularFormula instance with validated element–count pairs
- OrderedMolecularFormula instance with elements ordered by increasing atomic mass
- string representation in Hill or other notation (e.g., 'C3H8O2')
- monoisotopic mass (float, in Da) computed from formula
- formula delta (dict) for a given MS adduct
- predicted isotope pattern ([M], [M+1], [M+2] relative intensities)

## How to apply

First, design MolecularFormula as a collections.UserDict subclass supporting four initialization modes (empty, from dict {element: count}, from another MolecularFormula, or from kwargs). Implement __str__ to output Hill system notation (e.g., 'C3H8O2') and __repr__ for dict-like display. Implement element-wise __add__, __radd__, and __sub__ operators accepting both MolecularFormula and dict(str: int) operands, ensuring all operations return MolecularFormula instances to enable chaining. Populate a module-level _ELEMENT_MONOISO_MASS dictionary with exactly 24 elements and their monoisotopic masses, then create validation functions: valid_element (checks element against the dictionary), monoiso_mass (sums monoisotopic masses from a formula dict), and ms_adduct_formula (computes the formula delta for each of 21 standard MS adducts: [M]+, [M+H]+, [M+Na]+, [M+K]+, [M+2K]2+, [M+NH4]+, [M+H-H2O]+, [M-H]−, [M+HCOO]−, [M+CH3COO]−, [M-2H]2−, [M-3H]3−, [M+2Na-H]+, [M+2H]2+, [M+3H]3+, and [M+4H]4+ through [M+20H]20+). Finally, create an OrderedMolecularFormula subclass that sorts elements by increasing atomic mass in its __str__ output. Validate by running comprehensive unit tests on initialization, arithmetic, repr/str formatting, and adduct formula lookups; verify that example code snippets from mzapy documentation execute without error.

## Related tools

- **mzapy** (Python package providing the isotopes module in which MolecularFormula is implemented; exposes mass spectrometry data structures and utilities for MS analysis workflows) — https://github.com/PNNL-m-q/mzapy
- **h5py** (Dependency for reading/writing HDF5 files in which MZA format MS metadata (including PrecursorMonoisotopicMz, PrecursorCharge) is stored)
- **numpy** (Dependency for efficient numeric operations on monoisotopic masses and isotope intensity predictions)
- **MZA converter** (Upstream tool that converts vendor MS formats (Agilent, Bruker, Thermo, mzML) to HDF5-based MZA files; produces metadata tables with PrecursorMonoisotopicMz and PrecursorCharge to which molecular formula and adduct assignments apply) — https://github.com/PNNL-m-q/mza

## Examples

```
from mzapy.isotopes import MolecularFormula, valid_element, monoiso_mass, ms_adduct_formula
mf = MolecularFormula({'C': 3, 'H': 8, 'O': 2})
print(mf)  # 'C3H8O2'
mass = monoiso_mass(mf)
adduct_delta = ms_adduct_formula('[M+H]+')
mf_protonated = mf + adduct_delta
```

## Evaluation signals

- All unit tests pass: empty initialization, dict copy, kwarg initialization, __add__/__sub__ with MolecularFormula and dict operands, __repr__ and __str__ formatting, OrderedMolecularFormula atomic mass sorting.
- Monoisotopic mass computed from a formula matches literature exact mass within 0.001 Da (e.g., C3H8O2 = 76.0393 Da).
- ms_adduct_formula returns correct formula deltas for all 21 supported adducts; e.g., [M+H]+ returns {H: 1}, [M+Na]+ returns {Na: 1}, [M-H]− returns {H: -1}.
- MolecularFormula arithmetic preserves type and commutativity where defined (e.g., MolecularFormula({'C': 1}) + {'H': 4} == {'C': 1, 'H': 4}); negative element counts raise ValueError.
- valid_element rejects strings not in _ELEMENT_MONOISO_MASS; valid_ms_adduct rejects adduct strings not in the 21-member supported list.

## Limitations

- Monoisotopic mass calculation uses only the most abundant isotope of each element; does not account for naturally occurring isotope distributions or rare isotopes beyond the 24 elements in _ELEMENT_MONOISO_MASS.
- MS adduct list is fixed at 21 common adducts; user-defined or exotic adducts (e.g., metal complexes, custom labels) require manual dictionary extension.
- Molecular formula alone cannot distinguish isomers or regioisomers; use orthogonal separation (LC, ion mobility drift time) or fragmentation patterns to disambiguate.
- Formula arithmetic does not validate chemical feasibility (e.g., H_{−10} is computationally allowed but chemically impossible); post-hoc validation or domain constraints are required.

## Evidence

- [other] Design MolecularFormula as a collections.UserDict subclass with four initialization modes (empty, from dict, from MolecularFormula, from kwargs): "Design MolecularFormula as a collections.UserDict subclass with four initialization modes (empty, from dict, from MolecularFormula, from kwargs) following the documented interface."
- [other] Implement __repr__ and __str__ methods to output 'MolecularFormula{}' dict-style and 'C3H8O2' element-count format: "Implement __repr__ and __str__ methods to output 'MolecularFormula{}' dict-style and 'C3H8O2' element-count format respectively."
- [other] Implement element-wise addition (__add__, __radd__) and subtraction (__sub__) operators supporting both MolecularFormula and dict operands: "Implement element-wise addition (__add__, __radd__) and subtraction (__sub__) operators supporting both MolecularFormula and dict(str:int) operands, ensuring operations return MolecularFormula"
- [other] Create OrderedMolecularFormula subclass that inherits from MolecularFormula and orders elements by increasing atomic mass: "Create OrderedMolecularFormula subclass that inherits from MolecularFormula and orders elements by increasing atomic mass in __str__ output."
- [other] Define 21 MS adducts with charge assignments including [M]+, [M+H]+, [M+Na]+, [M+K]+, [M+2K]2+, [M+NH4]+, [M+H-H2O]+, [M-H]-, [M+HCOO]-, [M+CH3COO]-, [M-2H]2-, [M-3H]3-, [M+2Na-H]+, [M+2H]2+, [M+3H]3+ through [M+20H]20+: "Define 21 MS adducts with charge assignments ([M]+, [M+H]+, [M+Na]+, [M+K]+, [M+2K]2+, [M+NH4]+, [M+H-H2O]+, [M-H]-, [M+HCOO]-, [M+CH3COO]-, [M-2H]2-, [M-3H]3-, [M+2Na-H]+, [M+2H]2+, [M+3H]3+ through"
- [readme] mzapy provides an interface to unprocessed MS data in the MZA format: "A Python package that provides an interface to unprocessed MS data in the MZA format."
- [other] Implement utility validation functions: valid_element, valid_ms_adduct, monoiso_mass, ms_adduct_formula: "Implement utility validation functions: valid_element (checking against _ELEMENT_MONOISO_MASS dictionary), valid_ms_adduct (checking against supported adduct list), monoiso_mass (returning exact mass"
- [other] Populate _ELEMENT_MONOISO_MASS with 24 elements and their monoisotopic masses: "Populate _ELEMENT_MONOISO_MASS with 24 elements and their monoisotopic masses as documented."
