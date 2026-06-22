---
name: python-collection-subclassing-and-operator-overloading
description: Use when you need to represent structured scientific data (e.g., molecular formulas with element–count mappings) as a dict-like object, but standard dict does not preserve type across arithmetic operations, does not support domain-specific validation, or lacks convenient string representations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3805
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Python collections.UserDict
  - mzapy.isotopes module
  - pytest or unittest
derived_from:
- doi: 10.1021/acs.analchem.3c01653
  title: mzapy
- doi: 10.1021/acs.jproteome.2c00313
  title: ''
evidence_spans:
- A Python package that provides an interface to unprocessed MS data in the MZA format.
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

# Python Collection Subclassing and Operator Overloading

## Summary

Extend Python's collections.UserDict to create domain-specific mutable mapping types with custom string representations and arithmetic operators. This skill enables building lightweight, type-preserving data structures for scientific computing that behave like dictionaries but enforce domain semantics and return instances of the custom class from operations.

## When to use

You need to represent structured scientific data (e.g., molecular formulas with element–count mappings) as a dict-like object, but standard dict does not preserve type across arithmetic operations, does not support domain-specific validation, or lacks convenient string representations. Use this when arithmetic combinations of entities must remain instances of your custom class and when iteration order or element sorting matters for output formatting.

## When NOT to use

- Input data is already a typed Pydantic model or dataclass with immutability requirements; UserDict is mutable by design.
- You need strict immutability or want to forbid element addition/removal after instantiation; UserDict does not prevent modification.
- The domain requires hierarchical or nested structure; UserDict is flat key–value only.

## Inputs

- Empty constructor call or kwargs dict with element–count pairs
- Existing MolecularFormula or compatible dict(str: int) instance
- Operands for __add__, __sub__: MolecularFormula or dict(str: int)

## Outputs

- MolecularFormula instance (dict-like object with element keys, integer count values)
- String representation in dict style: 'MolecularFormula{...}'
- String representation in formula style: 'C3H8O2' or ordered by atomic mass
- Result of arithmetic operations (__add__, __sub__) as new MolecularFormula instance

## How to apply

Inherit from collections.UserDict to gain dict interface without reimplementing __getitem__, __setitem__, and __delitem__. Implement __repr__ to return 'ClassName{}' dict-style notation and __str__ to return domain-specific format (e.g., element symbols with counts ordered by atomic mass). Implement __add__, __radd__, and __sub__ operators accepting both instances of your class and plain dicts, always returning instances of your class to preserve type through chained operations. For ordering requirements, create a subclass (e.g., OrderedMolecularFormula) that overrides __str__ to sort output by a domain property (atomic mass). Support multiple initialization modes in __init__: empty (no args), from dict, from existing instance, and from kwargs. Validate inputs against domain-specific dictionaries (e.g., element symbols against a monoisotopic mass table) in dedicated validation functions. Write unit tests covering all initialization modes, operator combinations with mixed operand types, string representations, and edge cases like empty instances or identity operations.

## Related tools

- **Python collections.UserDict** (Base class for custom MolecularFormula dict subclass; provides __getitem__, __setitem__, __delitem__ and .data attribute to avoid reimplementing dict mechanics) — https://docs.python.org/3/library/collections.html#collections.UserDict
- **mzapy.isotopes module** (Context provider: defines _ELEMENT_MONOISO_MASS dictionary (24 elements with exact masses), MS adduct list (21 adducts), and validation functions (valid_element, valid_ms_adduct, monoiso_mass, ms_adduct_formula) used in MolecularFormula initialization and operator overloading) — https://github.com/PNNL-m-q/mzapy
- **pytest or unittest** (Testing framework for unit tests covering initialization modes, operator combinations, string representations, and edge cases)

## Examples

```
from mzapy.isotopes import MolecularFormula, OrderedMolecularFormula
mf1 = MolecularFormula({'C': 3, 'H': 8, 'O': 2})
mf2 = MolecularFormula(C=2, H=6, O=1)
mf_sum = mf1 + mf2
print(mf_sum)  # Ordered by atomic mass
print(repr(mf_sum))  # MolecularFormula{...} format
```

## Evaluation signals

- All initialization modes (empty, from dict, from instance, from kwargs) produce MolecularFormula instances with correct internal .data state
- Arithmetic operations (__add__, __sub__) with both MolecularFormula and dict operands return MolecularFormula instances (type invariant)
- __str__ output matches expected formula format ('C3H8O2') with elements ordered by atomic mass in OrderedMolecularFormula subclass
- __repr__ output matches 'MolecularFormula{...}' dict-style notation
- Element validation rejects keys not in _ELEMENT_MONOISO_MASS; unit tests verify valid_element() guards initialization
- Chained operations preserve type: (mf1 + mf2) - dict_operand returns MolecularFormula, not dict

## Limitations

- UserDict is mutable; no protection against post-initialization modification of counts. Use immutable alternatives (e.g., types.MappingProxyType) if immutability is required.
- Element validation depends on external _ELEMENT_MONOISO_MASS dictionary; adding new elements requires updating both that dictionary and any hardcoded element lists.
- Operator overloading does not support all arithmetic operators; __mul__ (scaling counts by integer) is not mentioned in the article's workflow and may need separate implementation.
- No built-in support for negative element counts; __sub__ can produce negative values if operands are not carefully ordered. Validation should reject invalid chemical formulas (e.g., 'C-1H2O').

## Evidence

- [other] Design MolecularFormula as a collections.UserDict subclass with four initialization modes (empty, from dict, from MolecularFormula, from kwargs): "Design MolecularFormula as a collections.UserDict subclass with four initialization modes (empty, from dict, from MolecularFormula, from kwargs)"
- [other] Implement __repr__ and __str__ methods to output 'MolecularFormula{}' dict-style and 'C3H8O2' element-count format respectively: "Implement __repr__ and __str__ methods to output 'MolecularFormula{}' dict-style and 'C3H8O2' element-count format respectively"
- [other] Implement element-wise addition (__add__, __radd__) and subtraction (__sub__) operators supporting both MolecularFormula and dict(str:int) operands, ensuring operations return MolecularFormula instances: "Implement element-wise addition (__add__, __radd__) and subtraction (__sub__) operators supporting both MolecularFormula and dict(str:int) operands, ensuring operations return MolecularFormula"
- [other] Create OrderedMolecularFormula subclass that inherits from MolecularFormula and orders elements by increasing atomic mass in __str__ output: "Create OrderedMolecularFormula subclass that inherits from MolecularFormula and orders elements by increasing atomic mass in __str__ output"
- [other] Implement utility validation functions: valid_element (checking against _ELEMENT_MONOISO_MASS dictionary), valid_ms_adduct (checking against supported adduct list), monoiso_mass (returning exact mass from element dict): "Implement utility validation functions: valid_element (checking against _ELEMENT_MONOISO_MASS dictionary), valid_ms_adduct (checking against supported adduct list), monoiso_mass (returning exact mass"
- [intro] A Python package that provides an interface to unprocessed MS data in the MZA format.: "A Python package that provides an interface to unprocessed MS data in the MZA format."
