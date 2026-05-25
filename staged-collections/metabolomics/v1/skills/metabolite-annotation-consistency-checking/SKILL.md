---
name: metabolite-annotation-consistency-checking
description: Use when validating metabolite annotations in metabolomics by comparing derived canonical chemical identifiers (SMILES, InChI, InChIKey) against reference data in LC-MS and GC-MS untargeted lipidomics, checking consistency between precursor m/z, adduct assignment, and molecular weight.
when_to_use_negative:
- Input spectra lack compound names, SMILES, or other chemical identifiers that can be mapped to PubChem.
- The dataset contains only unannotated spectra or spectra with de novo annotations not yet validated against reference databases.
- Precursor m/z or adduct information is missing from the spectrum metadata and cannot be inferred from other fields.
edam_operation: http://edamontology.org/operation_3282
edam_topics:
- http://edamontology.org/topic_0599
- http://edamontology.org/topic_3365
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: Python library that implements the repair_adduct_based_on_smiles filter and manages the full spectrum metadata harmonization pipeline
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Derives canonical SMILES, InChI, and InChIKey from compound names and existing SMILES; performs chemical structure validation and mass calculation
- name: PubChem
  role: Reference database queried to obtain canonical chemical identifiers and verify chemical structures linked to compound names
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/metabolite-annotation-consistency-checking@sha256:3cfbc2294ca3aa7f866794ddcaf7aae8ed41ab9274894e0462e1d4a367a2623a
---

# Metabolite annotation consistency checking

## Summary

Validate metabolite annotations in MS/MS library spectra by comparing derived canonical chemical identifiers (SMILES, InChI, InChIKey) against reference data and checking consistency between precursor m/z, adduct assignment, and molecular weight. This skill detects mismatches that indicate incorrect or incomplete annotations before library curation.

## When to use

Apply this skill when you have MS/MS spectra with metabolite annotations (compound name, SMILES, InChI, or InChIKey) and you need to identify inconsistencies between the stated chemical structure and the measured precursor mass or adduct assignment. Specifically, use it during library cleaning workflows when you want to quantify error rates in adduct derivation, detect structural misannotations, or repair metadata before merging spectra into a curated reference library.

## When NOT to use

- Input spectra lack compound names, SMILES, or other chemical identifiers that can be mapped to PubChem.
- The dataset contains only unannotated spectra or spectra with de novo annotations not yet validated against reference databases.
- Precursor m/z or adduct information is missing from the spectrum metadata and cannot be inferred from other fields.

## Inputs

- MS/MS spectrum collection in matchms format with compound name and/or SMILES annotation
- Precursor m/z values
- Adduct ion type (e.g., [M+H]+, [M-H]-)
- Parent mass (molar mass or monoisotopic mass) metadata field

## Outputs

- Annotated spectrum collection with repaired adduct and parent mass fields
- Summary statistics: count and percentage of spectra with no derived adduct
- Count and percentage of spectra with incorrect adduct (mismatch between derived and recorded)
- List of spectra flagged for manual review or removal due to annotation inconsistency

## How to apply

Load spectra with annotations in matchms format. Apply the 'repair_adduct_based_on_smiles' filter, which uses RDKit to derive canonical SMILES and InChI/InChIKey from PubChem reference data for each spectrum's compound name or existing SMILES. Compare the derived adduct and recalculated parent mass against the spectrum's recorded precursor m/z and adduct metadata. Count spectra where (1) no adduct could be derived (failure to map to PubChem or invalid SMILES), (2) derived adduct differs from recorded adduct (indicating a mismatch between metadata and measured mass), or (3) the recalculated parent mass does not match the precursor m/z within the instrument's mass accuracy tolerance. Generate a summary report with failure counts and percentages to establish baseline error rates and identify spectra requiring manual curation or removal.

## Related tools

- **matchms** (Python library that implements the repair_adduct_based_on_smiles filter and manages the full spectrum metadata harmonization pipeline) — https://github.com/matchms/matchms
- **RDKit** (Derives canonical SMILES, InChI, and InChIKey from compound names and existing SMILES; performs chemical structure validation and mass calculation)
- **PubChem** (Reference database queried to obtain canonical chemical identifiers and verify chemical structures linked to compound names)

## Evaluation signals

- Verify that the percentage of spectra with no derived adduct is ≤0.02% (the observed error rate for a well-curated subset of 413,314 GNPS spectra).
- Confirm that among spectra with successfully derived adducts, the percentage with incorrect adduct assignment is ≤0.024%.
- Check that repaired adducts and parent masses now match the precursor m/z within the instrument's mass accuracy tolerance (e.g., 5 ppm or mass defect window).
- Validate that the repair functions recover metadata for spectra that would otherwise be removed due to missing or conflicting annotation fields (target: ~52,084 spectra in the GNPS 500,569-spectrum dataset).
- Confirm schema consistency: all repaired spectra contain non-null values for adduct, precursor_mz, and parent_mass fields after repair.

## Limitations

- The filter cannot detect wrong chemical annotations that are consistent with the measured precursor mass—e.g., isomers or compounds with identical molecular weight that produce different fragmentation patterns.
- Repair success depends on PubChem coverage; compound names not found in PubChem will fail to derive canonical identifiers and will be flagged as unrepaired.
- The pipeline does not validate whether the measured fragment peaks are consistent with the annotated chemical structure; it only checks mass and adduct consistency.
- Parent mass field confusion (molar mass vs. monoisotopic mass) can persist if the original annotation is ambiguous and the compound name does not resolve unambiguously to a single structure.

## Evidence

- [abstract] repair_adduct_based_on_smiles filter error rates: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
- [abstract] canonical identifier derivation and comparison method: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] pipeline recovers annotations that would be lost: "combined the newly introduced repair functions repaired the metadata of 52,084"
- [discussion] limitation: isomeric misannotations cannot be detected: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline"
- [abstract] general scope of metadata and structure validation: "structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
