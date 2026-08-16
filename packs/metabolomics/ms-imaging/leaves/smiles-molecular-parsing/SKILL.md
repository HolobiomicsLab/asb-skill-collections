---
name: smiles-molecular-parsing
description: Use when when you have a list of candidate metabolite identifiers in SMILES or mol format and need to programmatically apply chemical transformations (e.g., derivatization reactions), compute molecular weights, or enumerate adduct ions for mass spectrometry matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.5c00633
  title: metid
evidence_spans:
- Powered by RDKit
- '[![Powered by RDKit]'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metid_cq
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  dedup_kept_from: coll_metid_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00633
  all_source_dois:
  - 10.1021/acs.analchem.5c00633
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMILES molecular parsing

## Summary

Parse input metabolite structures from SMILES notation or mol format into computational molecular objects using RDKit, enabling downstream chemical transformations and property calculations. This is essential for automating metabolite identification workflows where manual expert annotation is infeasible.

## When to use

When you have a list of candidate metabolite identifiers in SMILES or mol format and need to programmatically apply chemical transformations (e.g., derivatization reactions), compute molecular weights, or enumerate adduct ions for mass spectrometry matching. Use this as the first step in Met-ID's metabolite identification pipeline before derivatization chemistry rules are applied.

## When NOT to use

- Input is already an in-memory RDKit Mol object; proceed directly to derivatization or property calculation steps.
- Metabolite identity is unknown or structure is not yet elucidated; this skill cannot create structures from spectroscopic data alone.
- SMILES strings are malformed or chemically invalid; parsing will fail silently and require manual curation before this skill can proceed.

## Inputs

- SMILES strings (plain text or tab/comma-delimited)
- mol files (.mol or multi-mol .sdf format)
- metabolite structure identifiers or lists

## Outputs

- RDKit Mol objects (in-memory molecule representations)
- Validated molecule list (with parse status)
- Molecules indexed for downstream derivatization or property lookup

## How to apply

Load metabolite structures as SMILES strings or mol files using RDKit's molecule parsing functions (e.g., `Chem.MolFromSmiles()` or `Chem.MolFromMolFile()`). Validate that parsing succeeded by checking the returned molecule object is not None; failed parses indicate malformed SMILES or corrupted mol files and should be logged for manual review. Once parsed, the RDKit molecule object becomes the canonical representation for all downstream steps: identification of derivatization sites, application of reaction SMARTS patterns, molecular weight calculation, and adduct ion enumeration. The rationale is that RDKit's standardized internal representation allows reproducible chemistry operations across diverse metabolite structures.

## Related tools

- **RDKit** (Parse SMILES and mol files into molecule objects; enable chemical transformations and molecular property calculations) — https://www.rdkit.org/

## Examples

```
from rdkit import Chem; mol = Chem.MolFromSmiles('CC(C)Cc1ccc(cc1)C(C)C(O)=O'); print(mol.GetNumAtoms())
```

## Evaluation signals

- All input SMILES/mol files parse without None returns; validate by checking molecule object count matches input count.
- Parsed molecules have non-zero atom and bond counts; molecules with 0 atoms indicate parsing failure.
- Molecular weights calculated from parsed structures are chemically plausible (typically 50–2000 Da for small-to-medium metabolites).
- Subsequent derivatization reactions execute without RDKit errors; failed reactions indicate upstream parsing issues (e.g., incorrect atom types or valence).
- Round-trip validation: convert parsed Mol back to SMILES and re-parse to confirm structure is preserved.

## Limitations

- RDKit parsing is strict about SMILES syntax; non-canonical or incorrectly formatted SMILES will fail to parse and must be curated manually or standardized with external tools.
- Some complex derivatization chemistries (e.g., multi-step or cyclic transformations) may require explicit reaction SMARTS encoding; RDKit's default parsing alone cannot infer reaction mechanisms.
- Stereochemistry in SMILES (e.g., @, @@ chiral markers) is preserved during parsing but is not validated against chemical standards; incorrect stereochemistry encoding can lead to false matches downstream.
- Very large molecules (>1000 atoms) may incur computational overhead during subsequent RDKit operations (reaction application, property calculation).

## Evidence

- [other] Parse input metabolite structures (SMILES or mol format) using RDKit: "Parse input metabolite structures (SMILES or mol format) using RDKit."
- [readme] Met-ID has been developed to automate metabolite identification in Mass Spectrometry Imaging, at the moment most of this is done manually by experts which in the world of high throughput studies is not feasable.: "Met-ID has been developed to automate metabolite identification in Mass Spectrometry Imaging, at the moment most of this is done manually by experts which in the world of high throughput studies is"
