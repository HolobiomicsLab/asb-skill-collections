---
name: dna-adduct-characterization
description: Use when when you have a collection of DNA adduct compound structures
  in SDF format that requires validation for structural integrity and completeness,
  and you need to generate predicted fragment spectra at defined ionization levels
  and mass ranges for comparison against experimental mass.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_0593
  tools:
  - CFM-ID
  - RDKit
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.3389/fchem.2022.908572
  title: DNA adduct database
evidence_spans:
- CFM-ID
- the CFM-ID spectra, the Chemdraw files, the mol files and the SDF files of the DNA
  adducts
- compound database in SDF format
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dna_adduct_database_cq
    doi: 10.3389/fchem.2022.908572
    title: DNA adduct database
  dedup_kept_from: coll_dna_adduct_database_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fchem.2022.908572
  all_source_dois:
  - 10.3389/fchem.2022.908572
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# DNA adduct characterization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Computational workflow for validating and predicting fragment spectra from DNA adduct compound structures using structure file parsing and in-silico fragmentation. This skill integrates structural database validation with CFM-ID-based fragment prediction to build a curated, experimentally-aligned spectral resource.

## When to use

When you have a collection of DNA adduct compound structures in SDF format that requires validation for structural integrity and completeness, and you need to generate predicted fragment spectra at defined ionization levels and mass ranges for comparison against experimental mass spectrometry data or deposition into a spectral database.

## When NOT to use

- Input compounds are already in a validated spectral database with experimental mass spectrometry data — direct database lookup is more appropriate
- SDF file is malformed or contains non-chemical records — preprocessing/repair is required before this workflow
- Fragment prediction at unconventional ionization levels or mass ranges not supported by CFM-ID — manual rule-based fragmentation may be needed

## Inputs

- SDF-formatted compound database file containing DNA adduct structures
- Compound structures with defined molecular connectivity and stereochemistry

## Outputs

- Parsed and validated SDF structural records with integrity confirmation
- Predicted fragment spectra database indexed by compound
- Validation report documenting file integrity, record count, and structural verification

## How to apply

First, parse the SDF compound database file using RDKit to validate structural validity and confirm each record represents a single DNA adduct compound, generating a validation report documenting file integrity and record count. Second, execute CFM-ID on each validated compound structure to predict fragment spectra at the appropriate ionization level and mass range. Third, compile predicted fragment spectra into a structured database matching the format of deposited predicted-fragments resources. Fourth, validate output by confirming all input compounds have corresponding predicted spectra entries. The rationale is to ensure structural fidelity before in-silico prediction, reducing downstream errors in spectral matching and metabolite identification pipelines.

## Related tools

- **RDKit** (Parse SDF files to verify structural validity and extract molecular records; confirm each record represents a single DNA adduct compound)
- **CFM-ID** (Execute in-silico fragment prediction on each compound structure to predict fragment spectra at specified ionization level and mass range)

## Examples

```
# Validate SDF and predict fragments
from rdkit import Chem
import subprocess
# Parse and validate SDF
supp = Chem.SDMolSupplier('dna_adducts.sdf')
valid_mols = [m for m in supp if m is not None]
print(f'Validated {len(valid_mols)} compounds')
# Run CFM-ID on each structure
for mol in valid_mols:
    Chem.MolToMolFile(mol, 'tmp.mol')
    subprocess.run(['cfm-id', 'tmp.mol', '-ionization_mode', 'positive'])
```

## Evaluation signals

- All input compounds from the SDF file have corresponding entries in the output predicted fragments database with no missing records
- RDKit validation confirms 100% of SDF records parse without structural errors and represent valid molecular graphs
- Predicted fragment spectra contain mass values within the specified mass range and match expected fragmentation patterns for the compound class (DNA adducts)
- Output predicted-fragments database schema matches the format of deposited online predicted-fragments resources (field names, data types, indexing)
- Comparison of predicted spectra against experimental fragment data (if available) shows reasonable cosine similarity or peak matching rates

## Limitations

- CFM-ID prediction accuracy depends on availability of suitable machine learning models trained on similar compound classes; predictions for novel DNA adduct scaffolds may be less reliable
- SDF file parsing assumes well-formed chemical structure representations; non-standard or corrupted molecular connectivity will cause validation failure
- No changelog or version tracking documented for the DNA adductomics database, making it difficult to track structural or spectral updates over time
- Workflow does not account for isomeric variants or multiple tautomeric forms within a single SDF record; manual curation may be required for such cases

## Evidence

- [other] Parse the SDF file using RDKit to verify structural validity and extract the number of molecular records: "Parse the SDF file using RDKit to verify structural validity and extract the number of molecular records."
- [other] The in-silico fragment prediction stage uses CFM-ID to process SDF compound structures and generate predicted fragment spectra: "The in-silico fragment prediction stage uses CFM-ID to process SDF compound structures and generate predicted fragment spectra, with results deposited in the predicted fragments database."
- [other] Execute CFM-ID on each compound structure to predict fragment spectra at the appropriate ionization level and mass range: "Execute CFM-ID on each compound structure to predict fragment spectra at the appropriate ionization level and mass range."
- [other] Confirm that each record represents a single DNA adduct compound and generate a validation report: "Confirm that each record represents a single DNA adduct compound and generate a validation report documenting file integrity, record count, and parseable structure verification."
- [intro] Multiple formats and access points are available: Excel, Word, online interactive versions, SDF compound files, experimental and predicted fragment databases: "The following files are available: [Excel format, Word format, online, SDF format, experimental fragments online, predicted fragments online, collection of Excel file, online databases, CFM-ID']"
