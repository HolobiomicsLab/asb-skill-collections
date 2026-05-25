---
name: spectral-annotation-validation
description: "Validate the internal consistency of chemical annotation fields (SMILES, InChI, InChIKey) in mass spectral library records using RDKit cross-validation. This skill detects and quantifies annotation errors and inconsistencies that compromise spectral library quality and downstream analysis."
when_to_use_negative: |
  - "Spectra that have not yet undergone repair functions (e.g., 'derive annotation from compound name', 'repair adduct and parent mass based on SMILES'). Run repair filters first to reduce false negatives; 52,084 spectra in the GNPS library had repairable inconsistencies."
  - "Annotated spectra where chemical structure annotation is intentionally incomplete or absent (e.g., unannotated experimental data or library fragments). This filter requires all three SMILES, InChI, and InChIKey fields to be present."
  - "Data where the rationale for annotation inconsistency is external to the annotations themselves (e.g., correct SMILES but wrong measured mass due to instrument error). This skill validates annotation internal consistency only; it does not check whether annotated structures match measured fragment ions."
edam_operation: "http://edamontology.org/operation_3802"
edam_topics: |
  - "http://edamontology.org/topic_3172"
  - "http://edamontology.org/topic_0602"
tools: |
  - name: "matchms"
  role: "Core framework for loading, filtering, and validating mass spectral libraries; implements the 'require_valid_annotation' filter that performs RDKit cross-validation of SMILES, InChI, and InChIKey fields"
  repo: "https://github.com/matchms/matchms"
  - name: "RDKit"
  role: "Parses and validates SMILES, InChI, and InChIKey strings; detects internal inconsistencies and confirms mutual chemical structure equivalence across annotation formats"
  repo: "https://www.rdkit.org"
  - name: "PubChem"
  role: "Source for canonical SMILES, InChI, and InChIKey used in repair and validation workflows; used by the 'derive annotation from compound name' filter to retrieve reference annotations"
  repo: "https://pubchem.ncbi.nlm.nih.gov"
provenance: |
  source_task_ids:
  - task_006
  source_papers:
  - doi: "10.1186/s13321-024-00878-1"
  title: "Reproducible MS/MS library cleaning pipeline in matchms"
schema_version: "0.2.0"
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/spectral-annotation-validation@sha256:788a5d5649019eb465461533e6e3dc44c72bf058d29def5f3aa517da0615869d
---

# Spectral Annotation Validation

## Summary

Validate the internal consistency of chemical annotation fields (SMILES, InChI, InChIKey) in mass spectral library records using RDKit cross-validation. This skill detects and quantifies annotation errors and inconsistencies that compromise spectral library quality and downstream analysis.

## When to use

Apply this skill when you have a collection of annotated mass spectra (e.g., from GNPS, MoNA, or MassBank) and need to assess the quality of their chemical structure annotations before library publication, reuse, or downstream analysis. Use it after repair functions (e.g., deriving SMILES from compound names, repairing adducts) have been applied, to identify residual annotation problems and quantify how many spectra pass validation.

## When NOT to use

- Spectra that have not yet undergone repair functions (e.g., 'derive annotation from compound name', 'repair adduct and parent mass based on SMILES'). Run repair filters first to reduce false negatives; 52,084 spectra in the GNPS library had repairable inconsistencies.
- Annotated spectra where chemical structure annotation is intentionally incomplete or absent (e.g., unannotated experimental data or library fragments). This filter requires all three SMILES, InChI, and InChIKey fields to be present.
- Data where the rationale for annotation inconsistency is external to the annotations themselves (e.g., correct SMILES but wrong measured mass due to instrument error). This skill validates annotation internal consistency only; it does not check whether annotated structures match measured fragment ions.

## Inputs

- Annotated mass spectral library in matchms-compatible format (loaded as Spectrum objects with 'smiles', 'inchi', 'inchikey' fields)
- Chemical structure annotation fields: SMILES string, InChI string, InChIKey string

## Outputs

- Filtered mass spectral library with spectra passing validation (SMILES, InChI, InChIKey all present and mutually consistent)
- Structured report (CSV or JSON) containing: total spectra processed, count and fraction of spectra removed by validation criterion (missing field vs. inconsistent field pairs), final retention rate

## How to apply

Load the annotated mass spectral library into matchms (version ≥0.26.4) and apply the 'require_valid_annotation' filter, which uses RDKit to parse SMILES, InChI, and InChIKey fields and cross-validate their internal consistency and mutual compatibility. The filter checks each annotation record for missing fields (e.g., missing SMILES or InChIKey) and for inconsistencies between field pairs (e.g., SMILES and InChI representing different 2D structures). Count and report the number and fraction of spectra removed at each validation checkpoint (e.g., missing fields vs. field pair mismatches). Generate a structured report (CSV or JSON) documenting total spectra processed, counts and fractions failing each validation criterion, and final retention rate. The validation succeeds when all three annotation fields are present and RDKit confirms they encode the same chemical structure.

## Related tools

- **matchms** (Core framework for loading, filtering, and validating mass spectral libraries; implements the 'require_valid_annotation' filter that performs RDKit cross-validation of SMILES, InChI, and InChIKey fields) — https://github.com/matchms/matchms
- **RDKit** (Parses and validates SMILES, InChI, and InChIKey strings; detects internal inconsistencies and confirms mutual chemical structure equivalence across annotation formats) — https://www.rdkit.org
- **PubChem** (Source for canonical SMILES, InChI, and InChIKey used in repair and validation workflows; used by the 'derive annotation from compound name' filter to retrieve reference annotations) — https://pubchem.ncbi.nlm.nih.gov

## Evaluation signals

- All retained spectra have non-null SMILES, InChI, and InChIKey fields with no parsing errors by RDKit
- Removal counts match documented validation checkpoints: missing fields vs. field pair inconsistencies (e.g., SMILES and InChI encoding different structures)
- Retention rate and removal rate sum to 100% of input spectra; counts are non-negative integers
- Structured report accurately documents the number and fraction of spectra removed by each validation criterion; spot-check a sample of removed spectra to confirm field inconsistency (e.g., SMILES A and InChI B do not encode the same structure according to RDKit)
- Output library contains only spectra passing validation; no spectra with incomplete or inconsistent annotations remain

## Limitations

- The filter validates chemical structure annotation internal consistency only; it does not check whether the annotated structure is correct or matches the measured fragment ions. Wrong chemical annotations consistent with the measured mass will go unnoticed.
- The filter requires all three annotation fields (SMILES, InChI, InChIKey) to be present; spectra with only partial annotation information (e.g., SMILES without InChI) are removed even if the present fields are valid.
- RDKit-based validation depends on correct SMILES syntax; unusual or non-standard SMILES representations may fail parsing and cause false-positive removal.
- The filter does not clean metadata fields beyond chemical structure annotations (e.g., instrument type, collision energy) that may affect spectral interpretation.
- Runtime scales with library size (e.g., 6 hours 45 minutes for 500,569 spectra on GNPS); large libraries may require distributed processing.

## Evidence

- [abstract] SMILES, InChI and InChIKey are loaded by RDKit and compared to each other: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] require_valid_annotation filter removed 83,843 spectra but only 31,758 when repair functions applied first: "a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084"
- [methods] Filter validates SMILES, InChI and InChIKey internal consistency and mutual compatibility: "structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
- [discussion] Current libraries lack plausibility checks considering both metadata and measured fragments: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments."
- [discussion] Wrong chemical annotations consistent with measured mass will go unnoticed: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline."
