---
name: metadata-harmonization-standardization
description: Use when when you have preprocessed MS/MS spectra from multiple source
  repositories or instruments with inconsistent metadata field naming, formats, or
  values (e.g., mixed adduct notations like '[M+H]+' vs '[M+H]⁺', variable instrument
  type strings, or non-standard collision energy units).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - spectraverse-analysis repository
  - matchms
  - SpectralEntropy
  - spectraverse-analysis pipeline scripts
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.5c06256
  title: Spectraverse
evidence_spans:
- github.com/skinniderlab/spectraverse-analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectraverse_cq
    doi: 10.1021/acs.analchem.5c06256
    title: Spectraverse
  dedup_kept_from: coll_spectraverse_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c06256
  all_source_dois:
  - 10.1021/acs.analchem.5c06256
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metadata-harmonization-standardization

## Summary

Harmonize and standardize MS/MS spectral metadata fields (compound identifiers, adduct annotations, collision energies, instrument types) to a common schema after preprocessing. This ensures consistency across heterogeneous spectral library sources and enables reliable downstream analysis and cross-library comparisons.

## When to use

When you have preprocessed MS/MS spectra from multiple source repositories or instruments with inconsistent metadata field naming, formats, or values (e.g., mixed adduct notations like '[M+H]+' vs '[M+H]⁺', variable instrument type strings, or non-standard collision energy units). Apply this skill after spectral format standardization and quality filtering but before duplicate detection and final library export.

## When NOT to use

- Input spectra are already part of a single, internally consistent spectral library (e.g., a single instrument's native format with uniform metadata conventions); harmonization will add unnecessary processing overhead.
- Metadata fields are already in a validated, standardized schema and preprocessing/filtering has not introduced new inconsistencies or duplicates.
- The analysis goal requires preservation of source-specific metadata variations (e.g., historical instrument-specific collision energy notation) rather than normalization to a common standard.

## Inputs

- Preprocessed MS/MS spectra in MGF format with source metadata fields
- Metadata CSV files extracted from MGF headers
- Repository mapping configuration files defining standard schema (adduct list, instrument name mappings, collision energy unit conversions)
- matchms filter YAML configuration files (library_cleaning_1.yaml, library_cleaning_2.yaml)

## Outputs

- Harmonized metadata CSV files with standardized field values
- Harmonized MGF files with corrected and unified metadata annotations
- Duplicate candidate list with pairwise cosine similarity scores (numpy format)
- Final curated spectral library in standardized output format (mzML, mzTab, or MGF)

## How to apply

Execute the Spectraverse harmonization pipeline in stages: (1) Load preprocessed MGF files and associated metadata via mgf2csv conversion; (2) Apply standardization scripts (step2-3_standardization.py for SMILES, step3-2_adduct-rem.py for adduct correction, step3-7_metadata.py for instrument and collision energy fields) that map non-standard values to a repository-defined common schema; (3) Run matchms library cleaning filters (library_cleaning_1.yaml and library_cleaning_2.yaml) to repair metadata coherence after each stage; (4) Validate harmonized metadata against schema requirements (e.g., adduct field contains only approved adduct strings, collision energy values are numeric and within expected ranges); (5) Identify and flag or remove duplicate spectra based on harmonized metadata combinations using cosine similarity thresholds (pairwise cosine scores calculated in step3-4); (6) Export final harmonized library in standardized format (mzML, mzTab, or MGF with corrected metadata).

## Related tools

- **matchms** (Repairs and validates metadata consistency; applies standardized cleaning filters after each harmonization stage to correct incoherent annotations and remove metadata errors) — https://github.com/matchms/matchms
- **SpectralEntropy** (Calculates cosine similarity scores for duplicate spectrum detection based on harmonized spectra) — https://github.com/YuanyueLi/SpectralEntropy.git
- **spectraverse-analysis pipeline scripts** (Orchestrates multi-stage harmonization: mgf2csv, step2-3_standardization.py (SMILES), step3-2_adduct-rem.py (adduct correction), step3-7_metadata.py (instrument/collision energy standardization), step3-5_uniq-select.py (duplicate removal)) — https://github.com/skinniderlab/spectraverse-analysis

## Examples

```
python run_steps.py --config config/config_step3.json
```

## Evaluation signals

- All adduct annotations conform to a predefined controlled vocabulary (e.g., no malformed or undeclared adduct strings; step3-2 reports count of corrections applied).
- Instrument type field contains only standardized instrument identifiers; no remaining free-text variants or abbreviations outside the approved schema.
- Collision energy values are numeric, fall within expected ranges for the instrument type, and use consistent units (e.g., all eV, all normalized 0–100 scale).
- Pairwise cosine similarity scores are computed for all candidate duplicate spectra pairs; duplicates identified by score threshold (implicit in step3-5_uniq-select.py) are removed, reducing redundancy.
- Final library export validates against schema: no null/missing required metadata fields, no spectra with identical fragment m/z intensity patterns (removed in step2-2), no spectra with all fragment m/z > precursor m/z (removed in step2-7).

## Limitations

- Harmonization depends on the completeness and accuracy of the predefined schema mappings; metadata fields not covered by the mapping rules may remain non-standard or be lost.
- matchms repair functions may fail or produce incorrect mappings for highly corrupted or non-standard metadata entries; manual curation may be required for outliers.
- Duplicate detection via cosine similarity is heuristic-dependent; setting the cosine threshold too high may retain duplicates, while too low may remove genuine spectral variants.
- No changelog is available in the repository to track schema evolution or previous harmonization decisions, limiting reproducibility and version control of metadata changes.

## Evidence

- [other] Harmonize metadata fields (compound identifiers, adduct annotations, collision energies, instrument types) to common schema using repository mapping functions.: "Harmonize metadata fields (compound identifiers, adduct annotations, collision energies, instrument types) to common schema using repository mapping functions."
- [intro] code used to preprocess and harmonize MS/MS spectra and their associated metadata in the compilation of Spectraverse.: "code used to preprocess and harmonize MS/MS spectra and their associated metadata in the compilation of Spectraverse."
- [readme] step3-7_metadata.py: Standardization of instrument and collision energy fields, and finalizing the metadata: "step3-7_metadata.py: Standardization of instrument and collision energy fields, and finalizing the metadata"
- [readme] step3-2_adduct-rem.py: Removal and correction of unwanted adducts: "step3-2_adduct-rem.py: Removal and correction of unwanted adducts"
- [readme] At this point, matchms is run to repair the metadata associated with each spectrum.: "At this point, matchms is run to repair the metadata associated with each spectrum."
- [readme] step3-5_uniq-select.py: Removal of duplicate spectra based on pairwise cosine scores: "step3-5_uniq-select.py: Removal of duplicate spectra based on pairwise cosine scores"
