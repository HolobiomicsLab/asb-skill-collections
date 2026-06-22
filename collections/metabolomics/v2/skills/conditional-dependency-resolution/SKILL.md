---
name: conditional-dependency-resolution
description: Use when a Python library exposes functionality that depends on external packages (like sqlalchemy, pandas, or lxml) that are not required for core operations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - pip
  - sqlalchemy
  - Python
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- The main way to obtain Pyteomics is via `pip Python package manager
- '- `sqlalchemy <https://www.sqlalchemy.org/>`_ (used by :py:mod:`pyteomics.mass.unimod`);'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyteomics
    doi: 10.1021/acs.jproteome.8b00717
    title: pyteomics
  dedup_kept_from: coll_pyteomics
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00717
  all_source_dois:
  - 10.1021/acs.jproteome.8b00717
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# conditional-dependency-resolution

## Summary

Verify that a Python module correctly initializes and functions when its optional (conditional) dependencies are installed, ensuring the module gracefully handles both presence and absence of those dependencies. This skill is essential for validating library architecture in projects that support modular functionality.

## When to use

Apply this skill when a Python library exposes functionality that depends on external packages (like sqlalchemy, pandas, or lxml) that are not required for core operations. Use it specifically when you need to confirm that a module can be imported and instantiated successfully when the optional dependency is present, and that the conditional import mechanism works as designed.

## When NOT to use

- When testing the module WITHOUT the optional dependency installed (that requires a separate 'graceful absence' test, not this skill).
- When the optional dependency is declared but the module never actually uses it (requires code inspection, not runtime verification).
- When the module is already known to work; this is a validation/regression test, not a discovery technique.

## Inputs

- Python environment with base package installed
- Optional dependency package (e.g., sqlalchemy, pandas, lxml)
- Module or submodule name that declares conditional dependency

## Outputs

- Confirmation that module imports without exception
- Instantiated accessor/database object (e.g., Unimod object)
- Absence of ImportError or ModuleNotFoundError during initialization

## How to apply

First, install the optional dependency using pip (e.g., `pip install sqlalchemy`). Then, in a Python interpreter or script, attempt to import the module that declares a conditional dependency on that package. Instantiate any accessor or database classes provided by that module (e.g., the Unimod database accessor in pyteomics.mass.unimod). Verify that no ImportError or ModuleNotFoundError exceptions are raised during initialization. The rationale is that conditional dependencies are advertised to users as optional enhancements; verification proves the feature is actually usable when the dependency is satisfied.

## Related tools

- **Python** (Execution environment for importing and instantiating the module)
- **pip** (Package manager for installing the optional dependency)
- **sqlalchemy** (Example optional dependency used by pyteomics.mass.unimod for Unimod database access) — https://www.sqlalchemy.org/

## Examples

```
pip install sqlalchemy && python -c "from pyteomics.mass.unimod import Unimod; u = Unimod(); print('Unimod initialized successfully')"
```

## Evaluation signals

- Module import succeeds without ImportError or AttributeError
- Accessor class (e.g., Unimod) instantiates with no exceptions raised
- No silent failures or fallback-to-stub behavior when the dependency is present
- Object state is populated correctly (e.g., database connection is active, not mocked)
- Subsequent method calls on the instantiated object succeed (e.g., querying the Unimod database)

## Limitations

- This skill validates only the presence case; a separate test is needed to confirm graceful degradation when the dependency is absent.
- Does not verify the quality or correctness of results returned by the module's functionality—only that it initializes.
- Assumes the optional dependency itself is installed correctly; installation errors are out of scope.
- Does not test versioning constraints (e.g., minimum/maximum sqlalchemy version compatibility).

## Evidence

- [other] The pyteomics.mass.unimod module depends on sqlalchemy as a conditional dependency for accessing the Unimod database.: "The pyteomics.mass.unimod module depends on sqlalchemy as a conditional dependency for accessing the Unimod database."
- [other] Install sqlalchemy dependency using pip install sqlalchemy. 2. Import the pyteomics.mass.unimod module in a Python interpreter or script. 3. Instantiate the Unimod database accessor class and confirm initialization succeeds with no exceptions raised.: "Install sqlalchemy dependency using pip install sqlalchemy. 2. Import the pyteomics.mass.unimod module in a Python interpreter or script. 3. Instantiate the Unimod database accessor class and confirm"
- [other] sqlalchemy (used by :py:mod:`pyteomics.mass.unimod`);: "sqlalchemy (used by :py:mod:`pyteomics.mass.unimod`);"
- [readme] Pyteomics is a collection of lightweight and handy tools for Python that help to handle various sorts of proteomics data.: "Pyteomics is a collection of lightweight and handy tools for Python that help to handle various sorts of proteomics data."
