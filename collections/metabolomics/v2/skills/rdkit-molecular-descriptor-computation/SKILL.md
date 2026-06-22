---
name: rdkit-molecular-descriptor-computation
description: Use when when annotating .msp mass spectrometry files with chemical structure metadata and you need fast, offline molecular transformations (SMILES↔InChI, canonical SMILES generation) without network latency or service availability constraints;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3696
  edam_topics:
  - http://edamontology.org/topic_3293
  - http://edamontology.org/topic_0154
  tools:
  - MSMetaEnhancer
  - RDKit
  - pytest
  - Python
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
- Use the RDKit converter as a reference implementation
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.04494
  all_source_dois:
  - 10.21105/joss.04494
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# rdkit-molecular-descriptor-computation

## Summary

Implement a local ComputeConverter subclass using RDKit to perform chemical structure conversions (e.g., SMILES to InChI) on mass spectrometry metadata without relying on external web services. This skill enables offline, deterministic molecular property computation integrated into the MSMetaEnhancer annotation pipeline.

## When to use

When annotating .msp mass spectrometry files with chemical structure metadata and you need fast, offline molecular transformations (SMILES↔InChI, canonical SMILES generation) without network latency or service availability constraints; particularly useful when processing large batches of spectra that require consistent, reproducible structure conversions.

## When NOT to use

- Input structures require validation against external reference services or you need confidence scores for conversions.
- You need stereoisomeric SMILES variants (ISOMERIC_SMILES or CANONICAL_SMILES from PubChem) that require web service lookup.
- The converter must support asynchronous batch processing with dynamic retry logic for failed conversions.

## Inputs

- SMILES strings (or other chemical structure formats supported by RDKit)
- Converter configuration (source and target chemical attribute names)
- Molecular structure objects (RDKit Mol objects from parsed input)

## Outputs

- InChI strings
- InChI keys
- Canonical SMILES
- Molecular formulas
- Converted metadata dictionaries keyed by target attribute names

## How to apply

Create a new Python file inheriting from ComputeConverter in MSMetaEnhancer/libs/converters/compute/ that defines a conversions list with source and target attributes (e.g., 'smiles' to 'inchi') and calls create_top_level_conversion_methods with asynch=False. Implement conversion methods using RDKit's Chem module (e.g., RDKit Chem.MolFromSmiles to parse SMILES strings and Chem.inchi.MolToInchi to generate InChI). Return converted data as a dictionary with target attribute keys. Register the converter in MSMetaEnhancer/libs/converters/compute/__init__.py by importing and adding to __all__. Write pytest tests validating converter instantiation and conversion accuracy against reference SMILES inputs, then run pytest to confirm existing tests pass and new converter executes successfully.

## Related tools

- **RDKit** (Core cheminformatics library for local molecular structure parsing, validation, and conversion (SMILES→InChI, canonical SMILES generation))
- **MSMetaEnhancer** (Parent framework providing ComputeConverter base class, converter registration, and async annotation orchestration for .msp files) — https://github.com/RECETOX/MSMetaEnhancer
- **pytest** (Test framework for validating converter instantiation, conversion accuracy against reference inputs, and regression testing of existing converters)
- **Python** (Implementation language for ComputeConverter subclass and integration with MSMetaEnhancer async pipeline)

## Examples

```
from MSMetaEnhancer.libs.converters.compute import RDKit
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
ConverterBuilder.register([RDKit])
app = Application()
app.load_data('sample.msp', file_format='msp')
jobs = [('smiles', 'inchi', 'RDKit'), ('smiles', 'inchikey', 'RDKit')]
import asyncio
asyncio.run(app.annotate_spectra(['RDKit'], jobs))
```

## Evaluation signals

- Converter instantiates without errors and is registered in __all__ and importable from MSMetaEnhancer.libs.converters.compute
- Conversion methods correctly parse valid SMILES strings and produce chemically valid output (InChI, InChI keys, canonical SMILES) matching RDKit reference implementations
- Pytest test suite passes for instantiation, conversion accuracy against known reference SMILES, and output structure (dictionary keys matching target attributes)
- All existing MSMetaEnhancer tests continue to pass after converter registration (no regression)
- Edge cases (invalid SMILES, None inputs, empty structures) are handled gracefully or raise appropriate exceptions, with behavior documented in test assertions

## Limitations

- RDKit local conversion does not provide alternative stereoisomeric SMILES representations or validate against external reference databases like PubChem.
- Performance depends on RDKit's local computation speed; very large molecular structures or batches may be CPU-bound.
- Conversion accuracy is limited to RDKit's chemical structure canonicalization rules; some specialized or unusual structures may not convert as expected.
- Asynchronous execution (asynch=True) is not supported by ComputeConverter; this skill is inherently synchronous and may block the MSMetaEnhancer async pipeline if not carefully integrated.

## Evidence

- [other] ComputeConverter subclass using RDKit perform local chemical structure conversions (e.g., SMILES to InChI) without relying on web services: "ComputeConverter subclass using RDKit perform local chemical structure conversions (e.g., SMILES to InChI) without relying on web services"
- [other] Create a new Python file in MSMetaEnhancer/libs/converters/compute/ that inherits from ComputeConverter: "Create a new Python file in MSMetaEnhancer/libs/converters/compute/ that inherits from ComputeConverter"
- [other] Implement conversion methods using RDKit to perform local molecular structure transformations (e.g., parse SMILES strings with RDKit Chem.MolFromSmiles and generate InChI with Chem.inchi.MolToInchi): "Implement conversion methods using RDKit to perform local molecular structure transformations (e.g., parse SMILES strings with RDKit Chem.MolFromSmiles and generate InChI with Chem.inchi.MolToInchi)"
- [other] Register the new converter in MSMetaEnhancer/libs/converters/compute/__init__.py by importing and adding to __all__: "Register the new converter in MSMetaEnhancer/libs/converters/compute/__init__.py by importing and adding to __all__"
- [other] Create a pytest test file that validates converter instantiation and tests conversion accuracy against reference SMILES inputs, verifying output structure and chemical correctness: "Create a pytest test file that validates converter instantiation and tests conversion accuracy against reference SMILES inputs, verifying output structure and chemical correctness"
- [readme] MSMetaEnhancer is a tool used for `.msp` files annotation. It adds metadata like SMILES, InChI, and CAS number: "MSMetaEnhancer is a tool used for `.msp` files annotation. It adds metadata like SMILES, InChI, and CAS number"
- [other] Use the RDKit converter as a reference implementation: "Use the RDKit converter as a reference implementation"
