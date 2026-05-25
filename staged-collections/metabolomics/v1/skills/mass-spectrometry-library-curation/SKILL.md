---
name: mass-spectrometry-library-curation
description: Systematic cleaning and validation of mass spectrometry spectral library metadata and annotations using the matchms framework, including repair of structural notations (salts, adducts), harmonization of precursor masses, and removal of spectra with unrecoverable or inconsistent annotations.
when_to_use_negative:
- Input library is already manually curated and has passed institutional QC (e.g., NIST private library); re-curation may introduce unnecessary changes.
- Analysis requires retention of all spectral observations regardless of metadata quality (e.g., exploratory analysis of instrument artifacts or rare ionization modes not yet documented in standards).
- Metadata fields critical to your analysis (e.g., collision energy, instrument type) are not yet supported by matchms filters, as the current pipeline does not harmonize these fields.
edam_operation: http://edamontology.org/operation_3435
edam_topics:
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_0601
- http://edamontology.org/topic_3391
tools:
- name: matchms
  role: Core framework for applying tiered filter pipelines (basic, default, library cleaning) to harmonize metadata, repair structural annotations, and validate spectral libraries
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Parses SMILES strings (including repaired salt-notation SMILES), computes monoisotopic masses, and derives canonical SMILES/InChI/InChIKey for structure validation
  repo: https://www.rdkit.org
- name: PubChem
  role: External chemical database queried by 'derive_annotation_from_compound_name' filter to fetch canonical SMILES, InChI, and InChIKey when compound names are available
  repo: https://pubchem.ncbi.nlm.nih.gov
- name: Python
  role: Scripting language for automation, orchestration of filter chains, and custom post-processing or validation logic
provenance:
  source_task_ids:
  - task_004
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/mass-spectrometry-library-curation@sha256:3eb33fd865ac9e5fef24216bca1dd2311406e438d1ed2c5eddcc42571a4c9f38
---

# mass-spectrometry-library-curation

## Summary

Systematic cleaning and validation of mass spectrometry spectral library metadata and annotations using the matchms framework, including repair of structural notations (salts, adducts), harmonization of precursor masses, and removal of spectra with unrecoverable or inconsistent annotations.

## When to use

When ingesting publicly available or private MS/MS spectral libraries (e.g., GNPS, NIST, MoNA, MassBank) that contain incomplete, incorrect, or inconsistent metadata — such as salt-notation SMILES, mismatched adduct assignments, computed molar mass instead of monoisotopic mass, or missing structure annotations — and you need to produce a curated, reproducible library suitable for downstream metabolomics analysis or spectral matching.

## When NOT to use

- Input library is already manually curated and has passed institutional QC (e.g., NIST private library); re-curation may introduce unnecessary changes.
- Analysis requires retention of all spectral observations regardless of metadata quality (e.g., exploratory analysis of instrument artifacts or rare ionization modes not yet documented in standards).
- Metadata fields critical to your analysis (e.g., collision energy, instrument type) are not yet supported by matchms filters, as the current pipeline does not harmonize these fields.

## Inputs

- Raw spectral library in matchms format (mzML, mzXML, or equivalent)
- Spectral metadata including: parent_mass, precursor_mz, ionmode, compound_name, SMILES (possibly salt-notation), InChI, InChIKey, adduct
- YAML configuration file defining filter chain and parameters

## Outputs

- Cleaned and curated spectral library (matchms format)
- Cleaned spectral metadata with repaired SMILES, adduct, parent_mass, and derived structure annotations
- Summary report of filter statistics: counts of spectra removed, repaired, and retained per filter step
- Log file documenting validation failures and repair decisions

## How to apply

Load raw spectral data (in matchms format) and apply a tiered filter strategy: (1) Basic filters for metadata harmonization (ionmode, precursor m/z validation); (2) Default filters to derive missing metadata from existing fields and normalize peak intensities; (3) Library cleaning filters to repair structural annotations (e.g., extract neutral parent SMILES from salt notation using salt-splitting, recompute adduct and parent_mass from repaired SMILES using RDKit, derive canonical SMILES/InChI/InChIKey from PubChem when compound name is available), and flag or remove spectra that fail validation thresholds (e.g., missing ionmode or precursor m/z after repairs, >1.62% structural mismatches when derive_annotation_from_compound_name is applied). Compute monoisotopic masses from repaired SMILES and compare against parent_mass metadata; discard only spectra whose annotations remain unrecoverable. Generate a summary report of counts of spectra removed, repaired, and retained.

## Related tools

- **matchms** (Core framework for applying tiered filter pipelines (basic, default, library cleaning) to harmonize metadata, repair structural annotations, and validate spectral libraries) — https://github.com/matchms/matchms
- **RDKit** (Parses SMILES strings (including repaired salt-notation SMILES), computes monoisotopic masses, and derives canonical SMILES/InChI/InChIKey for structure validation) — https://www.rdkit.org
- **PubChem** (External chemical database queried by 'derive_annotation_from_compound_name' filter to fetch canonical SMILES, InChI, and InChIKey when compound names are available) — https://pubchem.ncbi.nlm.nih.gov
- **Python** (Scripting language for automation, orchestration of filter chains, and custom post-processing or validation logic)

## Evaluation signals

- Spectra count before and after cleaning matches expected reduction (e.g., GNPS library: 500,569 → 448,485 spectra after removing 31,758 unrecoverable spectra, with 52,084 repaired by new repair functions)
- For 'derive_annotation_from_compound_name' filter: check that ≤1.62% of successfully annotated spectra are flagged as having different 2D structure (i.e., SMILES mismatch); if >1.62%, investigate outliers
- For 'repair_smiles_of_salts' filter: verify that computed monoisotopic masses from repaired SMILES match the parent_mass metadata field within instrument-calibration tolerance (typically <5 ppm); flag any mismatches or missing parent_mass values
- For 'repair_adduct_and_parent_mass_based_on_SMILES' filter: confirm that ≥99.976% of spectra receive a derived adduct and that of those, ≥99.976% have correct adduct assignment (i.e., <0.024% incorrect)
- All spectra in the final library have non-null and non-conflicting values for ionmode, precursor_mz, parent_mass, and structure annotation (SMILES or InChI); spot-check a random sample against original metadata to confirm repairs were plausible

## Limitations

- Current pipeline does not validate whether fragment peaks are consistent with the annotated structure; wrong chemical annotations that match the measured parent mass will go unnoticed.
- Metadata fields not yet supported by matchms filters (e.g., instrument type, collision energy) are not cleaned; curation is incomplete if these fields are critical to downstream use.
- Processing large libraries (e.g., 500,569 spectra) requires substantial compute time (~6 hours 45 minutes for GNPS); scalability to much larger datasets or real-time curation is not demonstrated.
- The skill relies on external data sources (PubChem) for compound name resolution; failures or delays in network access or third-party service availability can impede curation.

## Evidence

- [abstract] metadata cleaning, peak filtering, intensity normalization, and structure annotation validation: "metadata cleaning, peak filtering, intensity normalization, and structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
- [abstract] Before cleaning, the GNPS library contained 500,569 spectra...The final cleaned GNPS public mass spectral library contains 448.485 curated mass spectra: "Before cleaning, the GNPS library contained 500,569 spectra...The final cleaned GNPS public mass spectral library contains 448.485 curated mass spectra"
- [abstract] combined the newly introduced repair functions repaired the metadata of 52,084: "combined the newly introduced repair functions repaired the metadata of 52,084 spectra that would have been removed"
- [abstract] For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [abstract] The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
- [abstract] Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min: "Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min"
- [discussion] Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments"
- [discussion] Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline"
