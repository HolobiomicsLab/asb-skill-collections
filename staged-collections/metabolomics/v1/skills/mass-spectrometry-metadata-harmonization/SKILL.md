---
name: mass-spectrometry-metadata-harmonization
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to systematically repair and validate MS/MS spectral metadata, including adducts, precursor m/z, SMILES, and compound annotations, through chemical structure validation against reference databases and cross-field consistency checks.
when_to_use_negative:
- Input spectra already have complete, manually curated, and structurally validated metadata (e.g., NIST or internal curated standards); harmonization would be redundant.
- The analysis goal requires preservation of original (even if incorrect) metadata for historical comparison or error auditing; repair operations are destructive.
- Spectra lack compound name, SMILES, or InChI fields entirely and no reference database is available to derive them; the pipeline will reject these as 'incomplete annotation'.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3071
- http://edamontology.org/topic_3520
tools:
- name: matchms
  role: Core library cleaning and metadata harmonization framework; provides filter classes (Basic, Default, Library Cleaning) and repair functions (repair_adduct_based_on_smiles, repair_parent_mass, repair_smiles_of_salts, derive_annotation_from_compound_name)
- name: RDKit
  role: Canonicalizes SMILES, InChI, and InChIKey; compares chemical structures for validation; used within repair_adduct_based_on_smiles to derive canonical forms and detect structural discrepancies
- name: PubChem
  role: Reference chemical structure database; provides canonical SMILES, InChI, and InChIKey lookups; used to validate and derive missing compound metadata and expected adduct masses
- name: Python
  role: Scripting and automation language for orchestrating matchms filter pipelines and generating batch processing workflows
- name: Git
  role: Version control for matchms codebase and reproducibility; ensures filter code and pipeline configuration are tracked and retrievable
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/mass-spectrometry-metadata-harmonization/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/mass-spectrometry-metadata-harmonization/skill.md
    merged_at: '2026-05-25T06:57:01.462004+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/mass-spectrometry-metadata-harmonization@sha256:60a99a82f5ca79ce8d0d0e1e72ed281bf2643fb036d6a6127c45159c2c231137
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# mass-spectrometry-metadata-harmonization

## Summary

Systematically repair and validate MS/MS spectral metadata—including adducts, precursor m/z, SMILES, and compound annotations—using chemical structure validation against reference databases and cross-field consistency checks. This skill ensures that library spectra meet plausibility thresholds before downstream analysis or publication.

## When to use

When ingesting MS/MS spectra from public or private libraries (GNPS, NIST, MoNA, MassBank) with incomplete, inconsistent, or potentially incorrect metadata fields (compound name, SMILES, InChI, adduct, precursor m/z, parent mass). Apply this skill before using spectra for similarity matching, structure dereplication, or molecular identification, or when preparing spectra for curation and publication.

## When NOT to use

- Input spectra already have complete, manually curated, and structurally validated metadata (e.g., NIST or internal curated standards); harmonization would be redundant.
- The analysis goal requires preservation of original (even if incorrect) metadata for historical comparison or error auditing; repair operations are destructive.
- Spectra lack compound name, SMILES, or InChI fields entirely and no reference database is available to derive them; the pipeline will reject these as 'incomplete annotation'.

## Inputs

- MS/MS spectrum collection in matchms format (mzML, mzXML, or matchms-native serialization)
- Spectrum metadata fields: compound_name, SMILES, InChI, InChIKey, precursor_mz, parent_mass, adduct, ionmode, spectrum_id
- Reference chemical structure database (PubChem for SMILES/InChIKey lookup)
- YAML configuration file specifying filter chain and parameters (e.g., ionmode whitelist, intensity norm method)

## Outputs

- Harmonized MS/MS spectrum collection with repaired and validated metadata
- Summary statistics: counts of spectra repaired, rejected, or retained per filter; error rates for adduct derivation and structure mismatch
- Log of metadata corrections applied (e.g., 'adduct repaired: [M+H]+ → [M+Na]+ for spectrum_id=X')
- Cleaned library ready for similarity matching, dereplication, or publication

## How to apply

Load MS/MS spectra in matchms format and apply a tiered filter pipeline: (1) run 'Basic filters' for elementary metadata harmonization (e.g., field validation, whitespace normalization); (2) run 'Default filters' to derive missing metadata from existing fields (e.g., SMILES/InChIKey from compound name via PubChem, infer ionmode from precursor m/z), require ionmode and precursor m/z, and normalize intensities; (3) for library curation, run 'Library cleaning' filters which additionally repair annotation errors via SMILES canonicalization (RDKit), salt removal, parent mass correction (monoisotopic vs. molar mass), and adduct repair by comparing precursor m/z against chemistry-derived masses. Use the 'repair_adduct_based_on_smiles' filter to validate adduct assignments: this filter derives canonical SMILES and InChIKey from PubChem, calculates expected precursor m/z for each common adduct, and flags/corrects mismatches. Accept spectra only if all repairs complete and metadata is consistent post-repair. This approach reduced a 500,569-spectrum GNPS library to 448,485 curated spectra while rescuing 52,084 that would have been discarded.

## Related tools

- **matchms** (Core library cleaning and metadata harmonization framework; provides filter classes (Basic, Default, Library Cleaning) and repair functions (repair_adduct_based_on_smiles, repair_parent_mass, repair_smiles_of_salts, derive_annotation_from_compound_name))
- **RDKit** (Canonicalizes SMILES, InChI, and InChIKey; compares chemical structures for validation; used within repair_adduct_based_on_smiles to derive canonical forms and detect structural discrepancies)
- **PubChem** (Reference chemical structure database; provides canonical SMILES, InChI, and InChIKey lookups; used to validate and derive missing compound metadata and expected adduct masses)
- **Python** (Scripting and automation language for orchestrating matchms filter pipelines and generating batch processing workflows)
- **Git** (Version control for matchms codebase and reproducibility; ensures filter code and pipeline configuration are tracked and retrievable)

## Evaluation signals

- Adduct repair completeness: ≥99.98% of spectra with valid SMILES must have a derived adduct (target from article: 0.02% failure rate acceptable); adduct correctness: ≤0.024% of repaired spectra should have an incorrect adduct assignment.
- SMILES derivation from compound name: ≥72.4% of spectra should yield a SMILES; among successful derivations, ≤1.62% should have a different 2D structure than expected.
- Metadata consistency: precursor m/z matches expected mass for detected adduct within stated tolerance; parent mass uses monoisotopic mass, not molar mass.
- Require-valid-annotation filter: all retained spectra must have ionmode, precursor_mz, and either SMILES/InChI or InChIKey present and internally consistent.
- Library size and yield: track spectra removed vs. repaired; a successful cleaning run should repair >10% of the spectra that would have been discarded (article example: repaired 52,084 of 83,843 that would have been removed).

## Limitations

- The pipeline does not validate whether MS/MS fragment peaks actually match the chemical structure in the annotation; wrong chemical annotations consistent with measured precursor m/z will pass through undetected.
- Metadata fields not yet supported by matchms filters (instrument type, collision energy, resolving power) are not cleaned or validated; future expansions needed.
- SMILES derivation from compound name requires a PubChem lookup; if PubChem lacks the compound or the name is ambiguous/misspelled, derivation fails (27.6% failure rate in article example).
- The repair_adduct_based_on_smiles filter requires valid SMILES as input; if SMILES are absent or malformed, no adduct can be derived and the spectrum may be rejected.
- Runtime scales with library size; processing 500,569 GNPS spectra took 6 hours 45 minutes; very large libraries or resource-constrained environments may face performance constraints.

## Evidence

- [abstract] Metadata harmonization and repair in matchms pipeline: "we here introduce a comprehensive pipeline for library cleaning within the matchms framework"
- [abstract] Filter tiers and core workflow steps: "metadata cleaning, peak filtering, intensity normalization, and structure annotation validation"
- [abstract] Adduct repair via SMILES canonicalization and PubChem reference: "This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [abstract] Adduct repair error metrics: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
- [abstract] SMILES derivation and structure validation outcomes: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [abstract] Impact of repair functions on library yield: "a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084"
- [discussion] Existing limitations in current publicly available libraries: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments."
- [discussion] Gap in fragment-annotation validation: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline."
