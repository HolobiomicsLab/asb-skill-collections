---
name: smiles-inchi-inchikey-comparison-and-validation
description: Use when working in the metabolomics domain to derive canonical SMILES, InChI, and InChIKey from compound names via PubChem lookup, then compare these chemical structure representations against existing annotations to detect unannotated spectra and structural mismatches.
when_to_use_negative:
- Input spectra lack valid compound name metadata; PubChem lookup requires unambiguous chemical names.
- Chemical structure metadata is already complete, validated, and trusted; this skill is redundant for pre-curated libraries.
- Spectra originate from synthetic or novel compounds not indexed in PubChem; derivation will fail for unknown compounds.
edam_operation: http://edamontology.org/operation_3346
edam_topics:
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3375
tools:
- name: matchms
  role: Framework for executing the 'derive_annotation_from_compound_name' filter to query PubChem and compare chemical structures
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Parses SMILES, InChI, and InChIKey representations and performs structural comparison to identify 2D structure mismatches
- name: PubChem
  role: Remote database queried to retrieve canonical SMILES, InChI, and InChIKey for compound names
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
derived_from:
- doi: 10.1186/s13321-024-00878-1
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/smiles-inchi-inchikey-comparison-and-validation@sha256:6950a04502a7b45a42a767d67a7ab3f7b7e8bb58b46421fb101dd6697d9a1f23
---

# SMILES/InChI/InChIKey Comparison and Validation

## Summary

Derives canonical SMILES, InChI, and InChIKey from compound names via PubChem lookup, then compares these chemical structure representations against existing annotations to detect unannotated spectra and structural mismatches. This skill validates chemical structure metadata consistency and identifies annotation errors in mass spectral libraries.

## When to use

Apply this skill when you have mass spectra with compound name metadata but uncertain or incomplete chemical structure annotation (SMILES/InChI/InChIKey), or when you need to verify that existing structure annotations match the stated compound name. Specifically, use it after basic metadata harmonization when you have valid compound names and need to populate or reconcile structure fields before downstream fragment validation.

## When NOT to use

- Input spectra lack valid compound name metadata; PubChem lookup requires unambiguous chemical names.
- Chemical structure metadata is already complete, validated, and trusted; this skill is redundant for pre-curated libraries.
- Spectra originate from synthetic or novel compounds not indexed in PubChem; derivation will fail for unknown compounds.

## Inputs

- Mass spectral library with valid compound name metadata
- Spectra with existing chemical structure annotations (SMILES/InChI/InChIKey)
- Ion mode and adduct information (to ensure correct ionization context)

## Outputs

- Spectra with canonical SMILES/InChI/InChIKey derived from PubChem
- Comparison table documenting matches and mismatches between derived and original annotations
- Error report quantifying derivation failure rate and structural mismatch rate
- Curated spectrum subset with validated or repaired structure metadata

## How to apply

Load spectra with valid compound names into matchms and apply the 'derive_annotation_from_compound_name' filter, which queries PubChem to retrieve canonical SMILES, InChI, and InChIKey for each compound. Use RDKit to parse and compare the derived structures against existing annotations in the spectrum metadata. Calculate two key metrics: (1) the proportion of spectra from which SMILES could not be derived (expected ~27.6% in GNPS-scale datasets), and (2) among successfully annotated spectra, the percentage assigned a different 2D structure than the original annotation (expected ~1.62%). Flag spectra with structural mismatches as requiring manual review or removal. Document all derivation failures and structural discrepancies in an error report to inform downstream curation decisions.

## Related tools

- **matchms** (Framework for executing the 'derive_annotation_from_compound_name' filter to query PubChem and compare chemical structures) — https://github.com/matchms/matchms
- **RDKit** (Parses SMILES, InChI, and InChIKey representations and performs structural comparison to identify 2D structure mismatches)
- **PubChem** (Remote database queried to retrieve canonical SMILES, InChI, and InChIKey for compound names)

## Evaluation signals

- Derivation success rate matches expected proportions (e.g., ~72.4% derivation success for GNPS-scale datasets); sustained deviation suggests systematic PubChem lookup failures or non-standard compound naming.
- Mismatch rate among successfully annotated spectra aligns with expected error threshold (~1.62% for GNPS); higher rates indicate pre-existing annotation errors or ambiguous compound names mapping to multiple structures.
- All spectra in output have non-null SMILES, InChI, and InChIKey fields (or explicit 'not_found' markers); schema validation confirms no partial structure records.
- Manual spot-check of flagged mismatches confirms they represent genuine structural differences (e.g., regioisomers, salt form omissions) rather than parser artifacts.
- Error report documents the exact count of spectra without derivation and the molecular differences (e.g., InChIKey hash mismatch) for each flagged spectrum.

## Limitations

- PubChem lookup fails for 20–30% of spectra in real datasets, typically due to ambiguous, misspelled, or non-standard compound names; success depends on metadata quality upstream.
- Canonical structures from PubChem may not match the salt form or exact protonation state present in the experimental sample, leading to false-positive mismatches when comparing derived structures to ion-mode-specific annotations.
- The filter detects structure annotations inconsistent with compound name but cannot verify if the annotation is correct when the compound name is wrong; wrong but internally self-consistent annotations will pass undetected.
- Running the full pipeline on 500,569 spectra takes ~6 h 45 min; performance scales linearly with library size and PubChem API latency.

## Evidence

- [methods] This filter derives the canonical SMILES, InChI and InChIKey from PubChem: "This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [methods] SMILES, InChI and InChIKey are loaded by RDKit and compared to each other: "SMILES, InChI and InChIKey are loaded by RDKit and compared to each other"
- [results] For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [discussion] Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments.: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments."
- [discussion] Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline.: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline."
