---
name: metadata-completeness-evaluation
description: Systematically assess the completeness and internal consistency of chemical annotation metadata (SMILES, InChI, InChIKey) in mass spectral library records using RDKit validation. This skill identifies incomplete or conflicting annotation fields and quantifies the proportion of spectra affected, enabling targeted repair or removal decisions.
when_to_use_negative:
- Spectra that lack SMILES, InChI, or InChIKey fields entirely and no repair function has been attempted—validation will simply remove them without distinguishing repairable from irreparable gaps.
- When annotation metadata is already curated and repair functions have been exhausted; further filtering may not improve quality.
- Unannotated experimental mass spectral data without chemical structure metadata; this skill is designed for library cleaning, not de novo annotation discovery.
edam_operation: http://edamontology.org/operation_3932
edam_topics:
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_0593
tools:
- name: matchms
  role: Framework that implements the 'require_valid_annotation' filter to load and cross-validate SMILES, InChI, and InChIKey using RDKit; orchestrates repair functions and generates validation reports.
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Chemical informatics library that loads SMILES, InChI, and InChIKey and validates their internal consistency by confirming all three encode the same molecular structure.
  repo: https://github.com/rdkit/rdkit
- name: PubChem
  role: Chemical database used by the 'derive annotation from compound name' filter to look up and assign canonical SMILES, InChI, and InChIKey when missing or inconsistent.
provenance:
  source_task_ids:
  - task_006
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/metadata-completeness-evaluation@sha256:3c3aa460ff58074b6ffac1fbebb6b3121aff88a5122eb90a33c6432ec2d7b430
---

# metadata-completeness-evaluation

## Summary

Systematically assess the completeness and internal consistency of chemical annotation metadata (SMILES, InChI, InChIKey) in mass spectral library records using RDKit validation. This skill identifies incomplete or conflicting annotation fields and quantifies the proportion of spectra affected, enabling targeted repair or removal decisions.

## When to use

When you have loaded a mass spectral library (e.g., GNPS, MoNA, Massbank) into matchms and need to understand how many spectra have missing or internally inconsistent annotation metadata before or after applying repair functions. Use this skill when the library cleaning goal includes measuring the impact of annotation validation on retention rates (e.g., 'what fraction of spectra will be removed by the require_valid_annotation filter?').

## When NOT to use

- Spectra that lack SMILES, InChI, or InChIKey fields entirely and no repair function has been attempted—validation will simply remove them without distinguishing repairable from irreparable gaps.
- When annotation metadata is already curated and repair functions have been exhausted; further filtering may not improve quality.
- Unannotated experimental mass spectral data without chemical structure metadata; this skill is designed for library cleaning, not de novo annotation discovery.

## Inputs

- Mass spectral library in matchms format (spectra with metadata fields: compound_name, smiles, inchi, inchikey, parent_mass, adduct, ionmode, precursor_mz)
- Spectral object collection or library file (e.g., GNPS library with 500,569+ spectra)

## Outputs

- Validation report (CSV or JSON) with counts of spectra processed, removed, and retained per validation criterion
- Breakdown of failure modes: missing annotation fields vs. internally inconsistent field pairs
- Retention rate (fraction of spectra passing all annotation consistency checks)
- Optional: comparative metrics showing impact of repair functions on recovery rate

## How to apply

Load the spectral library into matchms and apply the 'require_valid_annotation' filter, which uses RDKit to load and cross-validate SMILES, InChI, and InChIKey fields for each spectrum. The filter checks for missing fields and validates that the three chemical descriptors are internally consistent (e.g., that SMILES and InChI encode the same 2D structure). Count and categorize spectra that fail validation: those missing one or more fields, and those with conflicting field pairs. Generate a structured report (CSV or JSON) documenting the total number of spectra processed, the counts and fractions failing each validation criterion, and the final retention rate. Optionally, apply repair functions (such as 'derive annotation from compound name' or 'repair not matching annotation') before validation to salvage spectra with repairable inconsistencies, and re-run validation to measure how many spectra were recovered.

## Related tools

- **matchms** (Framework that implements the 'require_valid_annotation' filter to load and cross-validate SMILES, InChI, and InChIKey using RDKit; orchestrates repair functions and generates validation reports.) — https://github.com/matchms/matchms
- **RDKit** (Chemical informatics library that loads SMILES, InChI, and InChIKey and validates their internal consistency by confirming all three encode the same molecular structure.) — https://github.com/rdkit/rdkit
- **PubChem** (Chemical database used by the 'derive annotation from compound name' filter to look up and assign canonical SMILES, InChI, and InChIKey when missing or inconsistent.)

## Evaluation signals

- Validation report shows non-zero counts for both 'missing field' and 'inconsistent field pair' failure categories, indicating the filter correctly distinguished repairable gaps from conflicts.
- Retention rate (spectra passing all checks / spectra processed) is quantifiable and reproducible; re-running on the same library produces identical counts.
- When repair functions are applied before validation, the fraction of spectra removed should decrease; the delta (e.g., 83,843 − 31,758 = 52,084 recovered) quantifies repair effectiveness.
- No spectra with valid, internally consistent SMILES/InChI/InChIKey triplets are removed by the filter; spot-check a sample of retained spectra to confirm RDKit validation passed correctly.
- Validation time scales linearly with library size; for a 500,569-spectrum library the full pipeline completes in <7 hours, confirming filter overhead is acceptable.

## Limitations

- The filter validates internal consistency of SMILES/InChI/InChIKey only; it cannot detect chemical annotations that are chemically plausible (e.g., consistent with the measured precursor m/z) but semantically wrong (e.g., a different isomer or structural isomer of the correct compound).
- Repair functions are limited to metadata harmonization and derivation from other fields (compound name, molar mass, adduct); they cannot invent missing chemical structures.
- Current matchms filters do not validate whether measured MS/MS fragments match the annotated structure; metadata-only validation may retain spectra with inconsistent fragmentation patterns.
- Additional metadata fields such as instrument type, collision energy, and sample preparation are not yet cleaned by the current matchms filter pipeline, limiting the scope of metadata completeness assessment.

## Evidence

- [abstract] The core validation method and tool integration: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] Quantitative impact of validation and repair on library curation: "a total of 83,843 spectra were removed...only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084"
- [abstract] The specific filter and its role in the workflow: "Require valid annotation"
- [discussion] Problem context—limitations of current validation approach: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline."
- [abstract] Performance and scalability metric: "Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min"
