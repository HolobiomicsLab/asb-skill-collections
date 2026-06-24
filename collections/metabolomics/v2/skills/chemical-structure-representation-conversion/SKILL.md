---
name: chemical-structure-representation-conversion
description: Use when when you have .msp mass spectrometry metadata containing chemical
  identifiers (e.g., compound names or SMILES strings) and need to compute derived
  chemical properties (e.g., InChI, InChIKey, molecular formula) locally without network
  latency or service availability constraints.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3697
  edam_topics:
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_0154
  tools:
  - MSMetaEnhancer
  - pytest
  - RDKit
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-structure-representation-conversion

## Summary

Convert between different chemical structure representations (e.g., SMILES to InChI) using RDKit as a local compute backend within MSMetaEnhancer. This skill enables offline chemical metadata enrichment of .msp files without relying on external web services.

## When to use

When you have .msp mass spectrometry metadata containing chemical identifiers (e.g., compound names or SMILES strings) and need to compute derived chemical properties (e.g., InChI, InChIKey, molecular formula) locally without network latency or service availability constraints.

## When NOT to use

- When the input .msp file already contains all required chemical metadata (e.g., InChI, formula, InChIKey are already present).
- When the source identifier is ambiguous or contains drawing/image data that RDKit cannot parse into a valid molecular structure.
- When network latency is acceptable and you need access to curated, validated chemical databases (use web service converters like PubChem or IDSM instead).

## Inputs

- SMILES string
- source chemical identifier (name, InChI, CAS number, or other structure format)
- ComputeConverter class template

## Outputs

- InChI string
- InChIKey string
- molecular formula
- canonical SMILES
- chemical metadata dictionary

## How to apply

Create a new ComputeConverter subclass in MSMetaEnhancer/libs/converters/compute/ that inherits from ComputeConverter and defines a conversions list with source and target attributes (e.g., 'smiles' to 'inchi'). Implement conversion methods using RDKit functions (e.g., Chem.MolFromSmiles to parse SMILES, Chem.inchi.MolToInchi to generate InChI) and call create_top_level_conversion_methods with asynch=False to expose those conversions as top-level methods. Return converted data as a dictionary with target attribute keys. Register the converter in MSMetaEnhancer/libs/converters/compute/__init__.py and validate with pytest tests that verify converter instantiation, conversion accuracy against reference SMILES inputs, and output chemical correctness before running the full MSMetaEnhancer annotation pipeline.

## Related tools

- **RDKit** (Local molecular structure parser and converter; implements Chem.MolFromSmiles, Chem.inchi.MolToInchi, and related cheminformatics transformations)
- **MSMetaEnhancer** (Container application that registers and orchestrates converters (both web and compute) to enrich .msp mass spectrometry metadata) — https://github.com/RECETOX/MSMetaEnhancer
- **pytest** (Test framework for validating converter instantiation, conversion accuracy, and chemical correctness before integration)

## Examples

```
from MSMetaEnhancer.libs.converters.compute import RDKit; from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder; ConverterBuilder.register([RDKit]); app.annotate_spectra(services=['RDKit'], jobs=[('name', 'inchi', 'RDKit'), ('inchi', 'inchikey', 'RDKit')])
```

## Evaluation signals

- Converter class instantiates without errors and is successfully imported in MSMetaEnhancer/libs/converters/compute/__init__.py.
- Conversion methods execute without raising exceptions on reference SMILES inputs (e.g., benzene 'c1ccccc1').
- Output dictionary structure matches expected keys (e.g., 'inchi', 'inchikey', 'formula') and values are non-empty strings.
- Chemical correctness: output InChI/InChIKey/formula matches known reference values for test molecules (e.g., benzene InChI='InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H').
- Pytest suite passes: all existing tests still pass and new converter tests execute successfully.

## Limitations

- RDKit conversion accuracy depends on input SMILES validity; malformed or non-standard SMILES strings will fail to parse.
- Local compute approach scales linearly with number of conversions and cannot leverage distributed caching or batch optimization of web services.
- Conversion is synchronous (asynch=False); does not integrate with MSMetaEnhancer's asynchronous annotation pipeline for network-based converters.
- RDKit does not support all chemical formats or edge cases that specialized web services (CIR, CTS, PubChem) may handle (e.g., stereochemistry rendering, rare element support).

## Evidence

- [other] Create a new Python file in MSMetaEnhancer/libs/converters/compute/ that inherits from ComputeConverter: "Create a new Python file in MSMetaEnhancer/libs/converters/compute/ that inherits from ComputeConverter."
- [other] Define the conversions list with source and target attributes (e.g., 'smiles' to 'inchi'): "Define the conversions list with source and target attributes (e.g., 'smiles' to 'inchi') and call create_top_level_conversion_methods with asynch=False."
- [other] Implement conversion methods using RDKit to perform local molecular structure transformations: "Implement conversion methods using RDKit to perform local molecular structure transformations (e.g., parse SMILES strings with RDKit Chem.MolFromSmiles and generate InChI with Chem.inchi.MolToInchi)."
- [other] Return converted data as a dictionary with target attribute keys.: "Return converted data as a dictionary with target attribute keys."
- [other] Register the new converter in MSMetaEnhancer/libs/converters/compute/__init__.py by importing and adding to __all__.: "Register the new converter in MSMetaEnhancer/libs/converters/compute/__init__.py by importing and adding to __all__."
- [other] Create a pytest test file that validates converter instantiation and tests conversion accuracy: "Create a pytest test file that validates converter instantiation and tests conversion accuracy against reference SMILES inputs, verifying output structure and chemical correctness."
- [other] MSMetaEnhancer uses RDKit as a reference implementation for implementing ComputeConverter subclasses: "MSMetaEnhancer uses RDKit as a reference implementation for implementing ComputeConverter subclasses that perform local chemical structure conversions."
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR], [CTS], [PubChem], [IDSM], and [BridgeDb]."
