---
name: rdkit-molecular-property-extraction
description: Use when when you have a set of compounds represented as SMILES strings and need to compute their molecular properties (neutral mass, adduct-adjusted masses, mordred descriptors) for comparison against experimental peaks, retention time predictions, or similarity-based filtering thresholds during.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - RDKit
  - mordred
  - MINE-Database Filter base class
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans:
- MINE-Database requires the use of rdkit, which currently is unavailable to install on pip
- Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pickaxe_cq
    doi: 10.1186/s12859-023-05149-8
    title: Pickaxe
  dedup_kept_from: coll_pickaxe_cq
schema_version: 0.2.0
---

# rdkit-molecular-property-extraction

## Summary

Extract molecular properties (neutral mass, molecular weight, descriptors) from SMILES strings using RDKit to enable compound filtering and matching in reaction network expansion. This skill is essential for comparing generated compounds against experimental data (e.g., metabolomics peaks) or applying structure-based filtering criteria.

## When to use

When you have a set of compounds represented as SMILES strings and need to compute their molecular properties (neutral mass, adduct-adjusted masses, mordred descriptors) for comparison against experimental peaks, retention time predictions, or similarity-based filtering thresholds during Pickaxe reaction network expansion.

## When NOT to use

- Input compounds are already represented as pre-computed molecular weight vectors or feature matrices — use direct comparison instead
- SMILES strings are malformed or RDKit cannot parse them — validate SMILES syntax before invoking this skill
- Mass tolerance is very large (> 1 Da) relative to adduct spacing — collision/ambiguity risk may make matching unreliable

## Inputs

- SMILES string representation of compound structure
- List of possible adducts (e.g., [M+H]+, [M+Na]+, [M+K]+) with their mass offsets in Da
- Optional: trained mordred descriptor model for retention time prediction
- Optional: reference compounds with known masses for validation

## Outputs

- Neutral molecular weight (in Da) computed from SMILES
- Set of adduct-adjusted m/z values for each compound
- Mordred descriptor vector (when retention time prediction is enabled)
- Predicted retention time (when descriptor model is available)

## How to apply

Load each compound's SMILES string into RDKit and compute its molecular weight using RDKit's built-in molecular weight function. For mass-based filtering, calculate adduct-adjusted masses by adding specified adduct masses (e.g., [M+H]+, [M+Na]+) to the neutral mass. For retention time prediction, compute mordred descriptors from the RDKit molecule object and pass them to a trained retention time model. Store computed properties as instance attributes in your filter subclass so they can be queried during each generation iteration. Validate that molecular weight calculations match known reference compounds before deployment.

## Related tools

- **RDKit** (Parses SMILES strings and computes molecular weight and descriptor properties for mass matching and retention time prediction) — https://rdkit.org/docs/api-docs.html
- **mordred** (Computes molecular descriptors from RDKit molecule objects for input into retention time prediction models)
- **MINE-Database Filter base class** (Provides abstract interface in which RDKit property extraction is embedded within _choose_cpds_to_filter method) — https://github.com/tyo-nu/MINE-Database

## Examples

```
from rdkit import Chem; from rdkit.Chem import Descriptors; mol = Chem.MolFromSmiles('CC(C)Cc1ccc(cc1)C(C)C(O)=O'); mw = Descriptors.MolWt(mol); mz_plus_h = mw + 1.007825
```

## Evaluation signals

- Verify that neutral molecular weights computed by RDKit for test SMILES strings match known reference masses within ±0.001 Da
- Confirm that adduct-adjusted m/z values for each compound are correctly offset by the specified adduct mass (e.g., [M+H]+ = neutral_mass + 1.007825 Da)
- Check that compounds with masses within the specified mass_tolerance window (in Da) are retained and those outside are filtered out
- Validate that mordred descriptor computation succeeds for all parsed SMILES without raising exceptions or returning NaN values
- Ensure that the set of filtered compound IDs returned by _choose_cpds_to_filter is a proper subset of input compound IDs

## Limitations

- RDKit may fail to parse malformed SMILES strings, requiring input validation and error handling before property extraction
- Computed neutral masses assume correct SMILES valence and atom types; stereochemistry information in SMILES is not used for mass calculation
- Retention time predictions using mordred descriptors require a pre-trained model; descriptor computation alone does not yield retention times
- Mass tolerance thresholds must be calibrated to the experimental instrument and ionization method; overly tight tolerances may filter valid compounds, overly loose tolerances may cause false positives
- Adduct lists must be tailored to the ionization technique (ESI+, ESI−, APCI, etc.); missing or incorrect adducts will reduce filtering accuracy

## Evidence

- [other] Compute adduct-adjusted neutral masses using RDKit molecular weight from SMILES: "compute adduct-adjusted neutral masses (using RDKit molecular weight from SMILES)"
- [intro] Mordred descriptors are used as input for retention time prediction models: "rt_important_features specifies which mordred descriptors to use as input into the model"
- [other] RDKit is the library providing cheminformatic tools for default filters: "Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools."
- [intro] SMILES strings represent compound structures in the database: "structure field consists of SMILES representation of compounds"
- [intro] The metabolomics filter matches compound masses to peaks within a mass tolerance window: "It will force pickaxe to only keep compounds with masses (and, optionally, retention time (RT)) within a set tolerance of a list of peaks"
