---
name: unit-test-design-for-data-structure-classes
description: Use when when implementing a new data structure class that extends standard
  Python collections (e.g., collections.UserDict) and must support multiple initialization
  modes, operator overloading (__add__, __sub__), custom string formatting (__str__,
  __repr__), and validation logic.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Python unittest
  - Python collections.UserDict
  - mzapy.isotopes
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

# unit-test-design-for-data-structure-classes

## Summary

Design and implement comprehensive unit tests for custom data structure classes (e.g., dict-like or UserDict subclasses) to verify correct initialization modes, operator overloading, string representations, and edge cases. This skill ensures that molecular formula representations and other domain-specific containers behave correctly across all usage patterns.

## When to use

When implementing a new data structure class that extends standard Python collections (e.g., collections.UserDict) and must support multiple initialization modes, operator overloading (__add__, __sub__), custom string formatting (__str__, __repr__), and validation logic. Use this skill immediately after designing the class interface to catch initialization, arithmetic, and representation bugs before integration into downstream workflows.

## When NOT to use

- The class being tested is a simple wrapper around a built-in type with no custom logic or operators.
- No specification of expected output formats or validation rules has been provided.
- Testing will be deferred to integration testing phases (unit tests must precede integration).

## Inputs

- Python source code defining a UserDict subclass with multiple initialization signatures
- Reference dictionaries (e.g., element monoisotopic mass, supported MS adducts)
- Specification of __str__ and __repr__ output formats
- Specification of arithmetic operators (__add__, __sub__, __radd__) and their operand type signatures

## Outputs

- Comprehensive unit test module with test cases covering initialization, operators, string representations, and validation
- Test execution report with pass/fail status for each test case
- List of verified invariants (e.g., all arithmetic operations return the correct class type, no mutation of operands)

## How to apply

Begin by testing all supported initialization paths: empty constructor, dict unpacking, copy from same class type, and keyword arguments. Verify that __repr__ outputs dict-style notation (e.g., 'MolecularFormula{}') and __str__ outputs domain-formatted notation (e.g., 'C3H8O2' for molecular formulas ordered by atomic mass). Test both homogeneous and heterogeneous operator overloading—verify that __add__ and __sub__ work with both instances of the data structure and plain dict operands (str:int pairs), and that all operations return instances of the correct class type. Include validation tests for element/adduct lookup against reference dictionaries and test edge cases such as empty operands, negative counts, and operations that cancel to zero. Execute all test cases and verify 100% pass rate before declaring the class interface stable.

## Related tools

- **Python unittest** (Standard framework for organizing and executing unit test cases with assertions and test fixtures)
- **Python collections.UserDict** (Base class for implementing custom dict-like data structures with overridable methods)
- **mzapy.isotopes** (Target module containing MolecularFormula and OrderedMolecularFormula classes and validation functions) — https://github.com/PNNL-m-q/mzapy

## Examples

```
import unittest
from mzapy.isotopes import MolecularFormula, OrderedMolecularFormula

class TestMolecularFormula(unittest.TestCase):
    def test_empty_init(self):
        mf = MolecularFormula()
        self.assertEqual(len(mf), 0)
    def test_dict_init(self):
        mf = MolecularFormula({'C': 3, 'H': 8, 'O': 2})
        self.assertEqual(str(mf), 'C3H8O2')
    def test_addition(self):
        mf1 = MolecularFormula({'C': 1})
        mf2 = MolecularFormula({'C': 2})
        result = mf1 + mf2
        self.assertIsInstance(result, MolecularFormula)
        self.assertEqual(result['C'], 3)
    def test_ordered_str(self):
        omf = OrderedMolecularFormula({'O': 2, 'C': 3, 'H': 8})
        output = str(omf)
        self.assertTrue(output.index('C') < output.index('H') < output.index('O'))

if __name__ == '__main__':
    unittest.main()
```

## Evaluation signals

- All initialization modes (empty, dict, copy, kwargs) produce valid instances matching the documented interface.
- String representations conform to expected formats: __repr__ outputs 'MolecularFormula{...}' dict-style, __str__ outputs element-count notation (e.g., 'C3H8O2').
- Arithmetic operations (__add__, __sub__, __radd__) with both homogeneous (MolecularFormula) and heterogeneous (dict) operands return instances of the correct class type.
- Validation functions (valid_element, valid_ms_adduct) correctly reject invalid inputs and accept valid references from _ELEMENT_MONOISO_MASS and supported adduct lists.
- Edge cases (empty operands, canceling operations, negative counts) are handled without exceptions or silent data loss; all test cases pass with no failures or errors.

## Limitations

- Tests assume reference dictionaries (_ELEMENT_MONOISO_MASS, MS adduct list) are populated with 24 elements and 21 adducts respectively; tests must be updated if the reference data changes.
- OrderedMolecularFormula __str__ ordering by increasing atomic mass depends on correct population of element mass values; test coverage cannot detect missing or incorrect mass values without a separate validation step.
- Operator overloading tests assume binary operations (two operands); chained operations (e.g., A + B + C) are not explicitly covered and may require separate integration testing.

## Evidence

- [other] Initialization and operator specification: "Design MolecularFormula as a collections.UserDict subclass with four initialization modes (empty, from dict, from MolecularFormula, from kwargs) following the documented interface."
- [other] String representation specification: "Implement __repr__ and __str__ methods to output 'MolecularFormula{}' dict-style and 'C3H8O2' element-count format respectively."
- [other] Operator overloading design: "Implement element-wise addition (__add__, __radd__) and subtraction (__sub__) operators supporting both MolecularFormula and dict(str:int) operands, ensuring operations return MolecularFormula"
- [other] Validation function requirements: "Implement utility validation functions: valid_element (checking against _ELEMENT_MONOISO_MASS dictionary), valid_ms_adduct (checking against supported adduct list), monoiso_mass (returning exact mass"
- [other] Test coverage scope: "Write comprehensive unit tests covering empty/dict/copy/kwarg initialization, addition/subtraction with both operand types, repr/str formatting, and edge cases."
- [other] Success criterion: "Validation: all unit tests pass and example code snippets from documentation execute without error."
