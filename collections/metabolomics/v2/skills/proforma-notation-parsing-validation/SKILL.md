---
name: proforma-notation-parsing-validation
description: Use when you have peptide sequences with chemical modifications encoded in ProForma notation (e.g., '[Phospho]-PEPTIDE[Carbamidomethyl]-C') and need to validate their syntax, extract modification positions, or prepare them for downstream physico-chemical property calculations (mass, charge, pI).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0235
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pip
  - psims
  - pyteomics.proforma
  - Python
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- The main way to obtain Pyteomics is via `pip Python package manager
- '- `psims <https://mobiusklein.github.io/psims/docs/build/html/>`_ (used py :py:mod:`pyteomics.proforma`)'
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

# proforma-notation-parsing-validation

## Summary

Parse and validate ProForma notation strings representing modified peptide sequences using the pyteomics.proforma module. This skill enables robust handling of standardized proteomics sequence representations with chemical modifications.

## When to use

You have peptide sequences with chemical modifications encoded in ProForma notation (e.g., '[Phospho]-PEPTIDE[Carbamidomethyl]-C') and need to validate their syntax, extract modification positions, or prepare them for downstream physico-chemical property calculations (mass, charge, pI). Use this when working with search engine outputs or manually curated modified peptide lists that follow the ProForma standard.

## When NOT to use

- Input sequences use non-standard modification notation (e.g., single-letter codes without ProForma structure) — use a notation converter first.
- You need to query modification masses from external databases not integrated into pyteomics — use Unimod or manual lookup instead.
- Sequences are already pre-parsed into structured objects — skip to property calculation.

## Inputs

- ProForma notation strings (e.g., '[Phospho]-PEPTIDE[Carbamidomethyl]-C')
- Sequence files containing ProForma-encoded peptides
- Search engine output with modified peptide representations

## Outputs

- Parsed peptide objects with modification positions and identities
- Validation report (syntax errors, unrecognized modifications)
- Extracted modification lists and their chemical properties
- Physico-chemical property calculations (mass, isotopic distribution, charge, pI)

## How to apply

Install the psims conditional dependency using pip (pip install psims), which makes the pyteomics.proforma module available. Import the proforma module in a Python environment and load ProForma-encoded peptide strings. Call the appropriate ProForma parsing functions to parse the notation, validate syntax, and extract modification information. The parser will confirm that all modifications are recognized and that bracket notation is correctly balanced. Use the parsed output to query masses, charges, or other physico-chemical properties from the resulting peptide object.

## Related tools

- **pyteomics.proforma** (Core module for ProForma parsing, validation, and modification extraction) — https://github.com/levitsky/pyteomics
- **psims** (Optional dependency that conditionally enables pyteomics.proforma module availability)
- **Python** (Runtime environment for importing and executing pyteomics modules)
- **pip** (Package manager to install psims and resolve pyteomics.proforma dependency)

## Examples

```
from pyteomics import proforma; pep = proforma.to_proforma('[Phospho]-PEPTIDES[Carbamidomethyl]'); print(pep.mass)
```

## Evaluation signals

- Module imports without errors: `from pyteomics import proforma` executes successfully after psims installation.
- ProForma parsing functions are accessible and callable (e.g., proforma.to_proforma() methods exist).
- Valid ProForma strings parse without raising exceptions; invalid syntax raises informative parse errors.
- Extracted modification positions and identities match the input notation.
- Downstream physico-chemical calculations (mass, isotopic distribution, charge, pI) execute on parsed peptides without type errors.

## Limitations

- ProForma support depends on psims being installed; without it, pyteomics.proforma is unavailable.
- Only modifications recognized by pyteomics' internal or integrated Unimod database will parse; novel or proprietary modifications may fail validation.
- ProForma notation requires strict adherence to bracket and hyphen syntax; malformed input will raise parse exceptions.
- No changelog is available to track changes to ProForma parsing behavior across pyteomics versions.

## Evidence

- [other] Reconstruct optional-dependency resolution for pyteomics.proforma using psims: "task_id=task_004 | title=Reconstruct optional-dependency resolution for pyteomics.proforma using psims"
- [other] Module availability via conditional dependency: "What is the mechanism by which the pyteomics.proforma module becomes available after installing the psims conditional dependency?"
- [intro] Physico-chemical properties calculation: "Pyteomics provides a growing set of modules to facilitate the most common tasks in proteomics data analysis, including calculation of basic physico-chemical properties of polypeptides"
- [readme] Installation via pip: "The main way to obtain Pyteomics is via `pip Python package manager"
- [readme] ProForma as part of sequence manipulation capability: "easy manipulation of sequences of modified peptides and proteins"
