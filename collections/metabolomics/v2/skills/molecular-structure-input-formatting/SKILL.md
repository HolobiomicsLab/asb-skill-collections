---
name: molecular-structure-input-formatting
description: Use when when you have a molecular structure in any representation (drawn
  structure, PDB file, common name) and need to input it into mass spectrum prediction
  tools like ICEBERG or SCARF, or when screening candidates from chemical databases
  like PubChem.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0176
  - http://edamontology.org/topic_3172
  tools:
  - ms-pred ICEBERG
  - ICEBERG WebUI
  - PubChem
  - ms-pred (ICEBERG and SCARF)
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans:
- github.com__samgoldman97__ms-pred
- You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/
- By inputting the chemical formula and your experimental spectrum, the WebUI will
  rank it against all candidates from PubChem.
- the WebUI will rank it against all candidates from PubChem
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biotransformer_3_0_cq
    doi: 10.1093/nar/gkac408
    title: BioTransformer 3.0
  - build: coll_iceberg_cq
    doi: 10.1038/s42256-024-00816-8
    title: ICEBERG
  dedup_kept_from: coll_iceberg_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-024-00816-8
  all_source_dois:
  - 10.1038/s42256-024-00816-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-input-formatting

## Summary

Convert molecular structures into standardized input formats (SMILES, InChI, or chemical formula) required by tandem mass spectrum prediction models. This skill bridges chemical structure representation and computational prediction pipelines by ensuring molecules are encoded in formats compatible with downstream ML models.

## When to use

When you have a molecular structure in any representation (drawn structure, PDB file, common name) and need to input it into mass spectrum prediction tools like ICEBERG or SCARF, or when screening candidates from chemical databases like PubChem. The skill is essential before invoking spectrum prediction or structural elucidation workflows.

## When NOT to use

- Input is already a SMILES, InChI, or chemical formula in valid format — skip to model prediction.
- The molecule contains features not expressible in SMILES or InChI (e.g., isotopic labeling beyond standard notation), requiring custom representation or model-specific encoding.
- Structural ambiguity exists (e.g., multiple stereoisomers or tautomers map to the same formula) and your task requires unambiguous stereochemical assignment — consult domain expertise or literature first.

## Inputs

- Molecular structure (drawn structure, SMILES string, InChI string, chemical formula, or PubChem CID)
- Molecule identifier (common name, IUPAC name, or registry number)

## Outputs

- SMILES string
- InChI string
- Chemical formula
- Standardized molecular representation tuple (SMILES, InChI, formula)

## How to apply

Convert the input molecular structure into one of three standardized formats: SMILES (simplified molecular input line entry specification), InChI (International Chemical Identifier), or chemical formula. ICEBERG and SCARF both accept these formats via their WebUI or programmatic APIs. For WebUI use, input the molecular structure identifier directly; for programmatic use, pass the converted string as a parameter to the model. Validate that the conversion preserves chirality (for SMILES) and chemical connectivity. The choice of format depends on the downstream task: SMILES or InChI are preferred for fragment-level prediction (ICEBERG) because they retain structural information; chemical formula alone suffices for formula-level retrieval but loses stereochemical detail. For high-throughput screening against PubChem, pre-convert the candidate library to SMILES–InChI–formula triples and index by formula to enable efficient ranking.

## Related tools

- **ICEBERG WebUI** (Accepts SMILES, InChI, or chemical formula input; displays fragment-level spectrum predictions and retrieval results) — http://iceberg-ms.mit.edu/
- **ms-pred (ICEBERG and SCARF)** (Programmatic spectrum prediction models that consume standardized molecular formats (SMILES/InChI/formula) and generate tandem mass spectrum predictions) — https://github.com/coleygroup/ms-pred
- **PubChem** (Chemical structure database and retrieval resource; source of candidate molecules (SMILES, InChI, formula) for structural elucidation campaigns)

## Examples

```
python data_scripts/pubchem/02_make_formula_subsets.py
```

## Evaluation signals

- Verify SMILES validity: test against a SMILES parser (e.g., RDKit) for round-trip conversion without error or information loss.
- Check InChI uniqueness: confirm that the standardized InChI matches the expected chemical structure and resolves consistently across multiple tools.
- Validate chemical formula matches molecular weight: calculate exact mass from the formula and verify it aligns with observed parent mass ± instrument tolerance.
- Confirm input acceptance: submit the formatted structure to the ICEBERG or SCARF model without parsing errors; log returned spectrum predictions.
- Test against known standards: input a reference compound with published tandem MS spectrum and verify that the formatted structure produces consistent predictions.

## Limitations

- SMILES can represent the same molecule in multiple forms (canonical vs. non-canonical); always canonicalize for reproducibility (use RDKit or equivalent).
- Chemical formula alone discards stereochemical information and cannot distinguish between structural isomers; use SMILES or InChI when isomeric precision is required.
- Molecules with unusual bonding or features (radicals, hypervalent atoms, exotic coordination geometries) may not be expressible in standard SMILES/InChI and require custom handling or model-specific workarounds.
- Large-scale conversions of PubChem (millions of molecules) require parallelization and sufficient memory; the README notes this can take 'on the order of several hours, even parallelized'.

## Evidence

- [intro] Input formats accepted by ICEBERG and workflow entry point: "Input a molecular structure (SMILES, InChI, or chemical formula) into the ICEBERG model via the WebUI at http://iceberg-ms.mit.edu/"
- [intro] Format conversion for SCARF spectrum prediction: "Load or define the input molecule (SMILES string or molecular structure). 2. Invoke the SCARF model from the ms-pred repository to generate spectrum predictions"
- [readme] Retrieval workflow requiring standardized molecular formats: "each chemical formula is mapped to (smiles, inchikey) pairs. Subsets are selected for evaluation"
- [readme] PubChem library integration for candidate retrieval: "Making formula subsets takes longer (on the order of several hours, even parallelized) as it requires converting each molecule in PubChem to a mol / InChI"
- [readme] WebUI input interface for formula and spectrum matching: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem"
