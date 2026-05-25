---
name: spectral-metadata-harmonization
description: Use when harmonizing and repairing MS/MS spectral metadata in the metabolomics domain using LC-MS and GC-MS techniques to ensure valid and comparable library entries.
when_to_use_negative:
- Metadata is already manually curated and validated against chemical structures; harmonization may overwrite correct custom annotations or introduce false positives.
- Your goal is to annotate *unknown* experimental spectra against a library; use spectral similarity matching or MS/MS fragmentation prediction instead; metadata harmonization is for library curation, not peak matching.
- Spectral library lacks precursor m/z or ionization mode; repair filters for parent_mass and adduct require these fields, and their absence will cause repairs to fail or be skipped.
edam_operation: http://edamontology.org/operation_3096
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: Primary framework for loading, filtering, and harmonizing MS/MS spectral metadata; implements tiered filter sets (Basic, Default, Library cleaning) and repair functions (parent_mass, adduct, SMILES, annotation validation)
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Derives canonical SMILES, InChI, and InChIKey from compound names; validates SMILES and compares structure representations; used to infer parent_mass and adduct from chemical structure
  repo: https://www.rdkit.org/
- name: PubChem
  role: External reference database queried to retrieve canonical SMILES, InChI, and InChIKey for a given compound name; used by the 'derive annotation from compound name' filter
- name: Python
  role: Host language for matchms and RDKit; used to write and orchestrate metadata harmonization scripts and YAML configuration files
provenance:
  source_task_ids:
  - task_005
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/spectral-metadata-harmonization/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/spectral-metadata-harmonization/skill.md
    merged_at: '2026-05-25T07:33:56.271682+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/spectral-metadata-harmonization@sha256:007ac824dc78b009af17bfbd45404882776d923bfae5f7fb212649d636368329
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# spectral-metadata-harmonization

## Summary

Harmonize and repair MS/MS spectral metadata (parent mass, adducts, SMILES, compound names, ionization modes) against reference chemical structures and consistency rules to produce valid, comparable library entries. This skill detects and corrects systematic errors—such as molar mass vs. monoisotopic mass confusion, missing adduct assignments, and mismatched annotations—across large spectral libraries.

## When to use

Apply this skill when ingesting MS/MS spectra from public libraries (GNPS, MassBank, NIST, MoNA) or experimental datasets where metadata completeness and correctness are uncertain. Trigger conditions include: (1) metadata fields such as parent_mass, adduct, SMILES, or compound_name are missing or suspected to be incorrect; (2) you need to validate that parent_mass and adduct are consistent with the chemical structure; (3) you are preparing spectral libraries for downstream matching or annotation tasks and require plausibility checks that integrate both metadata and measured m/z values; (4) library scale is large enough to benefit from automated repair (e.g., > 1,000 spectra) rather than manual curation.

## When NOT to use

- Metadata is already manually curated and validated against chemical structures; harmonization may overwrite correct custom annotations or introduce false positives.
- Your goal is to annotate *unknown* experimental spectra against a library; use spectral similarity matching or MS/MS fragmentation prediction instead; metadata harmonization is for library curation, not peak matching.
- Spectral library lacks precursor m/z or ionization mode; repair filters for parent_mass and adduct require these fields, and their absence will cause repairs to fail or be skipped.

## Inputs

- Mass spectral library (in formats compatible with matchms: JSON, MGFPLUS, or mzML)
- Spectral metadata table with fields: spectrum_id, compound_name, parent_mass, precursor_mz, adduct, ionmode, SMILES (or InChI/InChIKey)
- Reference chemical structure data (PubChem, NIST, or local database)
- Tolerance parameters for mass comparison (e.g., ppm threshold, ionization mode)

## Outputs

- Harmonized spectral metadata table with repaired and validated entries
- CSV or JSON file with spectrum_id, corrected_parent_mass, original_parent_mass, corrected_adduct, canonical_SMILES, InChIKey, validation_status
- Repair log detailing count and type of corrections (e.g., '52,084 spectra had metadata repaired', '27.6% of spectra could not derive SMILES from compound name')
- Filtered spectral library with invalid or incomplete entries removed or marked

## How to apply

Load the spectral library in matchms and apply a tiered sequence of harmonization filters: (1) **Basic metadata harmonization** — normalize field names, remove invalid characters, and apply basic syntax checks. (2) **Derive missing metadata** — use PubChem lookups and RDKit to derive canonical SMILES, InChI, and InChIKey from compound names; repair SMILES of salts by isolating the parent ion structure. (3) **Repair parent mass and adducts** — detect and correct spectra where parent_mass was calculated from molar mass rather than monoisotopic mass; recalculate parent_mass and adduct assignments from the SMILES structure using RDKit, comparing against the measured precursor m/z with a tolerance appropriate to your instrument (typically ±5 ppm for high-resolution MS). (4) **Validate consistency** — ensure that precursor m/z, parent_mass, and adduct annotation are mutually consistent; flag or repair mismatches. (5) **Require complete annotations** — filter out spectra that lack essential metadata (ionization mode, precursor m/z, validated SMILES) after repairs. The matchms library cleaning filter set automates these steps via YAML configuration; typical runtime for 500,000 spectra is ~6–7 hours. Use the 'Library cleaning' filter tier if you require strict validation; use 'Default filters' if you accept incomplete metadata provided key fields are present.

## Related tools

- **matchms** (Primary framework for loading, filtering, and harmonizing MS/MS spectral metadata; implements tiered filter sets (Basic, Default, Library cleaning) and repair functions (parent_mass, adduct, SMILES, annotation validation)) — https://github.com/matchms/matchms
- **RDKit** (Derives canonical SMILES, InChI, and InChIKey from compound names; validates SMILES and compares structure representations; used to infer parent_mass and adduct from chemical structure) — https://www.rdkit.org/
- **PubChem** (External reference database queried to retrieve canonical SMILES, InChI, and InChIKey for a given compound name; used by the 'derive annotation from compound name' filter)
- **Python** (Host language for matchms and RDKit; used to write and orchestrate metadata harmonization scripts and YAML configuration files)

## Evaluation signals

- Precursor m/z and parent_mass (calculated from SMILES + adduct) agree within instrument tolerance (typically ±5 ppm for high-resolution MS).
- All spectra in the output have non-null and valid entries for: precursor_mz, parent_mass, ionmode, and a SMILES that can be parsed by RDKit.
- Repair log shows expected magnitude of corrections relative to library size (e.g., 'repair_parent_mass_is_molar_mass' should flag a small but meaningful fraction if molar-mass confusion exists in input); large unexpected repair counts may indicate data quality issues or misconfigured thresholds.
- Canonical SMILES derived from compound names should match the original SMILES in a high percentage of cases (>95% agreement in unambiguous cases); mismatches can indicate ambiguous or incorrect compound names.
- Spectra removed during 'Require valid annotation' step should be a small minority (<10%) after repairs; high removal rate suggests input metadata is too fragmented or corrupted for automated repair.

## Limitations

- Wrong chemical annotations that are consistent with measured parent mass will go unnoticed; the pipeline validates structural consistency but does not check whether fragments match the annotation—this requires orthogonal fragmentation prediction or manual inspection.
- Compound names that are ambiguous, proprietary, or absent from PubChem cannot be resolved; typically 25–30% of spectra may fail compound-name-to-SMILES derivation.
- Repair assumes that precursor m/z and ionization mode are correctly recorded; if these fields are systematically misreported, the filter will fail or introduce false repairs.
- Current matchms filters do not harmonize all metadata fields; instrument type, collision energy, and other instrumental parameters remain uncleaned and must be validated separately.
- Performance on very large libraries (>1 million spectra) or with slow network access to PubChem may be limited; typical runtime is 6–7 hours for 500,000 spectra.

## Evidence

- [abstract] metadata cleaning, peak filtering, intensity normalization, and structure annotation validation: "metadata cleaning, peak filtering, intensity normalization, and structure annotation validation"
- [abstract] Before cleaning, the GNPS library contained 500,569 spectra; after cleaning, 448,485 curated mass spectra remained: "Before cleaning, the GNPS library contained 500,569 spectra...The final cleaned GNPS public mass spectral library contains 448.485 curated mass spectra"
- [abstract] Newly introduced repair functions repaired the metadata of 52,084 spectra that would have been removed: "combined the newly introduced repair functions repaired the metadata of 52,084"
- [abstract] A common mistake is that the parent mass is calculated from the molar mass instead of the monoisotopic mass: "A common mistake is that the parent mass is calculated from the molar mass instead of the monoisotopic mass"
- [abstract] For 27.6% of the spectra, the SMILES could not be derived from the compound name: "For 27,6% of the spectra, the SMILES could not be derived from the compound name"
- [discussion] Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments"
- [discussion] Wrong chemical annotations that are consistent with the measured mass will go unnoticed: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline"
- [abstract] Running the matchms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min: "Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min"
