---
name: smiles-salt-notation-repair
description: Use when metabolomics involves LC-MS or GC-MS untargeted lipidomics to remove dot-separated salt notation from SMILES strings in mass spectral library metadata, extracting the neutral parent compound structure and validating the repaired SMILES against the parent_mass field.
when_to_use_negative:
- Input SMILES already contain only neutral parent structures without salt notation (no salts to remove).
- parent_mass metadata field is missing or unpopulated, preventing validation of the repair outcome.
- The spectrum is intended to represent a salt complex; removing the salt notation would lose scientifically necessary structural information for the application.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0154
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: Provides the repair_smiles_of_salts filter to extract neutral parent compound SMILES from salt-notation notation within spectrum metadata objects
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Parses repaired SMILES strings and computes monoisotopic mass for validation against parent_mass metadata
- name: PubChem
  role: Provides canonical SMILES, InChI and InChIKey lookup for annotation validation and repair workflows
  repo: https://pubchem.ncbi.nlm.nih.gov/
provenance:
  source_task_ids:
  - task_004
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/smiles-salt-notation-repair@sha256:4e5a6e858087537b91c8979223acf7c7c166fd78ac9c3233aefb29ef78bb45f7
---

# SMILES salt-notation repair

## Summary

This skill removes dot-separated salt notation from SMILES strings in mass spectral library metadata, extracting the neutral parent compound structure and validating the repaired SMILES against the parent_mass field. It prevents spectra with salt-notation SMILES from being incorrectly filtered out during library curation.

## When to use

Apply this skill when processing GNPS or similar public mass spectral libraries and you encounter spectra whose SMILES metadata contain dot-separated salt notation (e.g., 'C1=NC2=NC=NC(=C2N1)N.Cl'). This is especially critical during library cleaning pipelines where spectra with mismatched monoisotopic mass and parent_mass metadata would otherwise be removed; the skill rescues such spectra by correcting the SMILES annotation.

## When NOT to use

- Input SMILES already contain only neutral parent structures without salt notation (no salts to remove).
- parent_mass metadata field is missing or unpopulated, preventing validation of the repair outcome.
- The spectrum is intended to represent a salt complex; removing the salt notation would lose scientifically necessary structural information for the application.

## Inputs

- Mass spectral library in matchms format with SMILES metadata containing salt notation
- spectrum objects with parent_mass field populated
- dot-separated SMILES strings (e.g., salt notation like 'compound.counterion')

## Outputs

- Repaired SMILES metadata with salt notation removed
- Validated monoisotopic mass computed from repaired SMILES
- Spectrum objects with corrected SMILES and verified parent_mass alignment
- Summary report of repaired spectra count and validation results

## How to apply

Load mass spectral library data into matchms format and identify spectra with dot-separated SMILES notation. Apply the matchms `repair_smiles_of_salts` filter to extract the neutral parent compound SMILES from the salt-containing notation. Parse the repaired SMILES using RDKit to compute the monoisotopic mass for each corrected structure. Compare the computed monoisotopic mass against the parent_mass metadata field; successful repair is indicated when the computed mass now matches the stored parent_mass, thereby preserving the spectrum in the curated library rather than removing it as a failed validation check.

## Related tools

- **matchms** (Provides the repair_smiles_of_salts filter to extract neutral parent compound SMILES from salt-notation notation within spectrum metadata objects) — https://github.com/matchms/matchms
- **RDKit** (Parses repaired SMILES strings and computes monoisotopic mass for validation against parent_mass metadata)
- **PubChem** (Provides canonical SMILES, InChI and InChIKey lookup for annotation validation and repair workflows) — https://pubchem.ncbi.nlm.nih.gov/

## Evaluation signals

- Monoisotopic mass computed from repaired SMILES matches the parent_mass field in spectrum metadata (successful validation).
- Count of repaired spectra should be >0 when processing libraries with known salt-notation SMILES (e.g., 52,084 spectra in GNPS case).
- Repaired SMILES are single-component structures (no remaining dot-separated notation) and parse successfully with RDKit.
- Mass difference between computed and stored parent_mass is within measurement tolerance (< 1–5 ppm for high-resolution instruments).
- Spectrum is retained in the curated library post-repair, rather than being removed by downstream validation filters.

## Limitations

- The skill assumes that the neutral parent compound is the intended annotation; if the salt form is scientifically required, this repair will lose structural information.
- Repair relies on accurate parent_mass metadata; if the stored parent_mass itself is incorrect or derived from molar mass instead of monoisotopic mass, validation will fail even after correct SMILES repair.
- Multiple salts or complex counter-ions (e.g., polymeric salts) may not be handled correctly if RDKit cannot parse the notation structure.
- The skill only validates mass consistency; wrong chemical annotations that happen to match the measured parent_mass will not be detected and will pass validation.

## Evidence

- [abstract] repair_smiles_of_salts filter: "Repair SMILES of salts"
- [other] salt-notation SMILES with dot-separated counter-ions: "identify spectra whose SMILES metadata contain dot-separated salt notation (e.g., 'C1=NC2=NC=NC(=C2N1)N.Cl')"
- [other] monoisotopic mass validation against parent_mass field: "Parse the repaired SMILES using RDKit to compute the monoisotopic mass for each repaired structure. Compare computed monoisotopic masses against the parent_mass field"
- [abstract] 52,084 spectra successfully repaired and retained: "newly introduced repair functions repaired the metadata of 52,084"
- [other] Rescue of spectra from removal in library curation: "preventing their removal from the library"
