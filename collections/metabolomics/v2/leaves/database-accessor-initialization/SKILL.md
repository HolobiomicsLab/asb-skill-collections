---
name: database-accessor-initialization
description: Use when a Python module declares optional/conditional dependencies (e.g.,
  sqlalchemy for database access) and you need to confirm that the module can be imported
  and instantiated without exceptions when those dependencies are present in the environment.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - pip
  - sqlalchemy
  - Python
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# database-accessor-initialization

## Summary

Verify that a module depending on conditional dependencies successfully initializes its database accessor when those dependencies are installed. This skill ensures optional dependencies are correctly resolved and do not cause import failures.

## When to use

Use this skill when a Python module declares optional/conditional dependencies (e.g., sqlalchemy for database access) and you need to confirm that the module can be imported and instantiated without exceptions when those dependencies are present in the environment.

## When NOT to use

- When the conditional dependency is already installed as a hard requirement rather than optional.
- When testing behavior when the dependency is intentionally absent (use import-failure testing instead).
- When the module has no database accessor or does not declare conditional dependencies.

## Inputs

- Python package with conditional/optional dependencies declared
- Package dependency specification (e.g., setup.py, pyproject.toml, or requirements file)
- Python interpreter or script environment

## Outputs

- Initialized database accessor instance
- Confirmation of successful module import
- Absence of dependency resolution errors

## How to apply

Install the conditional dependency using pip (e.g., `pip install sqlalchemy`). Then import the target module in a Python interpreter or script and attempt to instantiate the database accessor class (e.g., Unimod class). Verify that no ImportError, AttributeError, or initialization exceptions are raised. Success is confirmed when the accessor object is created and ready for use.

## Related tools

- **pip** (Install sqlalchemy and other optional dependencies for the pyteomics module) — https://github.com/levitsky/pyteomics
- **Python** (Execute import and instantiation of the pyteomics.mass.unimod module and Unimod database accessor) — https://github.com/levitsky/pyteomics
- **sqlalchemy** (Provide conditional database access functionality for the Unimod module) — https://www.sqlalchemy.org/

## Examples

```
pip install sqlalchemy && python -c "from pyteomics.mass import unimod; db = unimod.Unimod(); print('Initialization successful')"
```

## Evaluation signals

- No ImportError or ModuleNotFoundError raised during module import
- Unimod database accessor class can be instantiated without exceptions
- Accessor instance is created and responds to expected method calls or property access
- No AttributeError or configuration errors during initialization
- Module initialization succeeds with sqlalchemy present in sys.modules

## Limitations

- This skill only tests initialization; it does not verify functional correctness of database queries or data retrieval.
- Test depends on sqlalchemy being correctly installed and compatible with the installed Python version.
- Does not test behavior when the conditional dependency is absent (a separate scenario).

## Evidence

- [other] research_question: "Does the pyteomics.mass.unimod module successfully initialize when sqlalchemy is installed as a conditional dependency?"
- [other] workflow: "1. Install sqlalchemy dependency using pip install sqlalchemy. 2. Import the pyteomics.mass.unimod module in a Python interpreter or script. 3. Instantiate the Unimod database accessor class and"
- [other] finding: "The pyteomics.mass.unimod module depends on sqlalchemy as a conditional dependency for accessing the Unimod database."
- [readme] tool_evidence: "- `sqlalchemy <https://www.sqlalchemy.org/>`_ (used by :py:mod:`pyteomics.mass.unimod`);"
