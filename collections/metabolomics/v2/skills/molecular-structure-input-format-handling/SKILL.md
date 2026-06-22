---
name: molecular-structure-input-format-handling
description: Use when you are receiving molecular structures from external sources (COCONUT database, ZINC database, user-provided chemical data) in varying formats (SMILES strings, InChI identifiers, SDF files), and you need to unify them into a single canonical representation before computing biosynfoni.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3837
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - biosynfoni
  - pip
  - RDKit
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- biosynfoni
- a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research
- pip install -e .[dev]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni
schema_version: 0.2.0
---

# molecular-structure-input-format-handling

## Summary

Accept molecular structures in multiple standardized input formats (SMILES, InChI, SDF files) and convert them to a common internal representation (RDKit Mol objects) for downstream fingerprint computation or analysis. This skill is essential when working with natural product databases or diverse chemical datasets where structures arrive in heterogeneous formats.

## When to use

You are receiving molecular structures from external sources (COCONUT database, ZINC database, user-provided chemical data) in varying formats (SMILES strings, InChI identifiers, SDF files), and you need to unify them into a single canonical representation before computing biosynfoni fingerprints or performing downstream structure-based analysis.

## When NOT to use

- Molecules are already loaded as RDKit Mol objects in memory.
- Input is a pre-computed fingerprint or feature vector (not a structure).
- The molecular structure format is proprietary or non-standard and RDKit cannot parse it.

## Inputs

- SMILES string
- InChI string
- SDF file (multi-molecule structure file)

## Outputs

- RDKit Mol object
- list of RDKit Mol objects (from SDF supplier)

## How to apply

Use RDKit's Chem.MolFromSmiles(), Chem.MolFromInChI(), or Chem.SDMolSupplier() functions to parse input structures according to their format. For command-line workflows, the biosynfoni tool accepts SMILES, InChI, and SDF file paths directly; internally it delegates to RDKit for parsing. For bulk processing, iterate over a molecular supplier (e.g., from an SDF file) and parse each molecule in sequence. Validate that parsing succeeded (i.e., the returned Mol object is not None) before passing to fingerprinting; failed parses should be logged and skipped. The rationale is that RDKit is the de facto standard for cheminformatics in Python and handles all major molecular representation standards.

## Related tools

- **biosynfoni** (Command-line interface for parsing SMILES, InChI, and SDF inputs and converting them to internal molecular representation) — https://github.com/lucinamay/biosynfoni
- **RDKit** (Underlying chemistry toolkit used by biosynfoni to parse SMILES, InChI, and SDF formats into Mol objects)

## Examples

```
from biosynfoni import Biosynfoni
from rdkit import Chem
mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')
fp = Biosynfoni(mol).fingerprint
```

## Evaluation signals

- All input molecules are successfully parsed to non-None RDKit Mol objects.
- Number of parsed molecules equals expected count (or total records in SDF if known).
- Fingerprints can be computed from parsed Mol objects without errors.
- Molecular properties (atom count, formula, SMILES representation) can be retrieved from parsed objects, confirming valid structure.
- Parsing failures are explicitly logged with molecule ID and reason (invalid SMILES, missing InChI, corrupted SDF record).

## Limitations

- RDKit parsing may silently fail or produce chemically invalid Mol objects for malformed SMILES or InChI strings; validation of chemical validity requires additional checks (e.g., Chem.SanitizeMol).
- SDF files with non-standard or proprietary field encodings may not parse correctly.
- Very large SDF files (millions of molecules) may be memory-intensive when loading as a complete list; streaming or chunking strategies may be necessary.
- No changelog documented for the biosynfoni package limits visibility into parsing behavior changes across versions.

## Evidence

- [readme] Convert a SMILES string to a fingerprint: from biosynfoni import Biosynfoni; from rdkit import Chem; smi = <SMILES>; mol = Chem.MolFromSmiles(smi); fp = Biosynfoni(mol).fingerprint: "from biosynfoni import Biosynfoni
from rdkit import Chem

smi = <SMILES>
mol = Chem.MolFromSmiles(smi)
fp = Biosynfoni(mol).fingerprint"
- [readme] Create a fingerprint from an InChI string: biosynfoni <InChI>; Write the fingerprints of all molecules in an SDF file to a CSV file: biosynfoni <molecule_supplier.sdf>: "Create a fingerprint from an InChI string:

```bash
biosynfoni <InChI>
```

Write the fingerprints of all molecules in an SDF file to a CSV file:

```bash
biosynfoni <molecule_supplier.sdf>
```"
- [readme] We have used data from the COCONUT natural product database and ZINC compound database: "We have used data from the [COCONUT](https://coconut.naturalproducts.net) natural product database and [ZINC](https://zinc.docking.org) compound database"
- [other] Load molecular structures from the sample dataset (format and path to be specified by user). Compute biosynfoni fingerprints for each molecule using the biosynfoni package API.: "Load molecular structures from the sample dataset (format and path to be specified by user). Compute biosynfoni fingerprints for each molecule using the biosynfoni package API."
