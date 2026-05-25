---
name: metadata-harmonization-cleaning
description: Use when working in the metabolomics domain to systematically clean and harmonize metadata in mass spectral libraries using a tiered filter pipeline that validates chemical annotations and repairs structural identifiers for LC-MS and GC-MS untargeted lipidomics.
when_to_use_negative:
- Input library is already fully annotated and has been validated against fragment ion composition (i.e., fragments already verified to match the given chemical structure); additional repair will not improve reliability.
- Annotated spectra contain wrong chemical structures that are consistent with measured parent mass (e.g., isomers); the current pipeline cannot detect these and will pass them through.
- Library lacks sufficient metadata (e.g., no ion mode, no precursor m/z fields at all) to enable even basic harmonization; preprocessing to recover or impute these fields is required first.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3520
tools:
- name: matchms
  role: Core framework for executing the metadata cleaning and repair filter pipeline, including basic, default, and library cleaning tiers; orchestrates RDKit and PubChem calls.
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Validates and repairs SMILES strings; identifies salt components; derives canonical SMILES, InChI, and InChIKey; compares chemical structures to detect inconsistencies.
- name: PubChem
  role: Supplies canonical chemical identifiers (SMILES, InChI, InChIKey) when compound name is provided; used by the 'derive annotation from compound name' filter.
- name: Python
  role: Runtime environment for matchms and integration of filter logic, logging, and statistics reporting.
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/metadata-harmonization-cleaning/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/metadata-harmonization-cleaning/skill.md
    merged_at: '2026-05-25T07:15:30.852857+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/metadata-harmonization-cleaning@sha256:a53214b50a28c5d7c90d11d5c69c0067f422c1a78147aba44aa09ceacf55256d
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# metadata-harmonization-cleaning

## Summary

Systematically clean and harmonize metadata in mass spectral libraries by applying a tiered filter pipeline (basic, default, library cleaning) that validates chemical annotations, repairs structural identifiers (SMILES, InChI, InChIKey), reconciles precursor m/z and adduct assignments with structure, and removes or repairs spectra with incomplete or inconsistent metadata. This skill is essential for preparing public MS/MS libraries (e.g., GNPS, MoNA, MassBank) for reliable downstream analysis and sharing.

## When to use

Apply this skill when ingesting public mass spectral libraries with known metadata quality issues (incomplete ion mode, missing precursor m/z, unvalidated chemical structures, inconsistent adduct assignments), and you require a reproducible, auditable record of which spectra were retained, removed, and repaired. Specific triggers: input library contains >10% spectra with incomplete annotations, or stakeholders require evidence that chemical structures match measured precursor masses and fragment patterns.

## When NOT to use

- Input library is already fully annotated and has been validated against fragment ion composition (i.e., fragments already verified to match the given chemical structure); additional repair will not improve reliability.
- Annotated spectra contain wrong chemical structures that are consistent with measured parent mass (e.g., isomers); the current pipeline cannot detect these and will pass them through.
- Library lacks sufficient metadata (e.g., no ion mode, no precursor m/z fields at all) to enable even basic harmonization; preprocessing to recover or impute these fields is required first.

## Inputs

- MGF-format mass spectral library file (e.g., GNPS no-propagated snapshot, MoNA, MassBank export)
- YAML configuration file specifying filter chain, parameters, and repair settings
- PubChem API access (for 'derive annotation from compound name' filter)
- RDKit chemical toolkit (for SMILES validation and structure comparison)

## Outputs

- Cleaned and harmonized MS/MS library (MGF or equivalent)
- Summary statistics: input spectrum count, retained count, removed count, repaired count
- Per-spectrum repair log indicating which filters modified metadata
- Filtering report with filter-by-filter pass/fail rates and reason codes

## How to apply

Load the MS/MS library in MGF or equivalent format using matchms 0.26.4 (or compatible version) and apply the filter pipeline in order: (1) Basic filters to harmonize metadata field names and case; (2) Default filters to derive missing ion mode, precursor m/z, and normalize peak intensities; (3) Library cleaning filters to repair SMILES of salts using RDKit, repair parent mass (correcting molar mass vs. monoisotopic mass confusion), derive canonical SMILES/InChI/InChIKey from PubChem for compound names, repair adduct assignments based on SMILES structure, remove spectra with mismatches between annotation and precursor m/z, and require valid annotations post-repair. Configure all steps in a YAML file specifying thresholds and repair logic, execute the pipeline, and log counts of input, retained, removed, and repaired spectra. Performance: expect ~6–7 hours for 500,000 spectra on standard hardware.

## Related tools

- **matchms** (Core framework for executing the metadata cleaning and repair filter pipeline, including basic, default, and library cleaning tiers; orchestrates RDKit and PubChem calls.) — https://github.com/matchms/matchms
- **RDKit** (Validates and repairs SMILES strings; identifies salt components; derives canonical SMILES, InChI, and InChIKey; compares chemical structures to detect inconsistencies.)
- **PubChem** (Supplies canonical chemical identifiers (SMILES, InChI, InChIKey) when compound name is provided; used by the 'derive annotation from compound name' filter.)
- **Python** (Runtime environment for matchms and integration of filter logic, logging, and statistics reporting.)

## Evaluation signals

- Spectrum count audit: compare input count, retained count, removed count, and repaired count to expected values (e.g., for GNPS no-propagated: 500,569 input, 448,485 retained, 31,758 removed, 52,084 repaired).
- Metadata completeness: verify that all retained spectra have non-null ion mode, precursor m/z, and (after repair) valid chemical structure identifiers (SMILES, InChI, InChIKey).
- Structure–precursor consistency: randomly sample repaired spectra and confirm that the repaired adduct assignment and parent mass match the structure via monoisotopic mass calculation (not molar mass).
- Repair transparency: confirm that the per-spectrum repair log identifies which filter(s) modified each spectrum and records the old and new values.
- PubChem derivation rate: for spectra annotated by compound name lookup, verify that the fraction of successful derivations (e.g., 72.4% for GNPS) matches the reported filter statistics, and spot-check that derived structures are chemically reasonable.

## Limitations

- The pipeline cannot detect wrong chemical annotations that are consistent with the measured parent m/z; isomers and regioisomers with identical masses will pass through undetected.
- Repair of parent mass confuses molar mass with monoisotopic mass in the input; the filter corrects this only if the molar mass field is present and populated, but if the field is entirely missing, the repair cannot proceed.
- PubChem lookups fail for ~27.6% of compound names (in GNPS case), either because the compound is not indexed or the name is non-standard; these spectra are not repaired by the derive-from-name filter.
- Fragment ion composition is not checked against the annotated structure; spectra with fragments that are inconsistent with the given chemical structure are not flagged or removed.
- Additional metadata fields (instrument type, collision energy) are not yet harmonized or validated by the current filter set; users requiring these fields must implement custom repair logic.

## Evidence

- [abstract] metadata harmonization, peak filtering, intensity normalization, and structure annotation validation: "metadata cleaning, peak filtering, intensity normalization, and structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
- [abstract] Basic, Default, and Library cleaning filter tiers: "Basic filters. Runs basic metadata harmonization. Default filters. Runs basic metadata harmonization, but also derives missing metadata from other fields, requiring metadata about ionmode and"
- [abstract] Repair SMILES of salts using RDKit; derive canonical SMILES/InChI/InChIKey from PubChem: "Repair SMILES of salts. This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [abstract] GNPS library: 500,569 input spectra, 448,485 retained, 31,758 removed, 52,084 repaired by new repair functions: "Before cleaning, the GNPS library contained 500,569 spectra...The final cleaned GNPS public mass spectral library contains 448.485 curated mass spectra"
- [abstract] Repair parent mass corrects molar mass confusion: common mistake is calculating parent mass from molar mass instead of monoisotopic mass: "Repair parent mass is molar mass field. A common mistake is that the parent mass is calculated from the molar mass instead of the monoisotopic mass"
- [discussion] Current libraries lack plausibility checks considering both metadata and measured fragments; wrong annotations consistent with measured mass go unnoticed: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments."
- [abstract] PubChem derivation success rate and structural discrepancy detection: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [abstract] Adduct repair accuracy: 0.02% had no derived adduct; of 99.98%, 0.024% had incorrect adduct: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
- [abstract] Runtime performance: 6 h 45 min for GNPS library of 500,569 spectra: "Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min"
- [abstract] Configuration and reproducibility: YAML files specify filters and settings; scripts and cleaned library deposited on Zenodo: "Examples of these YAML files can be found on Zenodo [5]. The cleaned library, the scripts and YAML file with the filters and settings can be found on Zenodo [5]"
