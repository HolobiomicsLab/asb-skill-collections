---
name: compound-identifier-mapping-curation
description: Use when when integrating MS/MS spectra from multiple source repositories
  or instruments into a unified library, and the compound identifiers, adduct annotations,
  collision energies, and instrument types differ in format, terminology, or completeness
  across sources.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - spectraverse-analysis repository
  - matchms
  - SpectralEntropy
  - spectraverse-analysis
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

# compound-identifier-mapping-curation

## Summary

Standardize and harmonize compound identifiers and metadata annotations across heterogeneous MS/MS spectral libraries by mapping source-specific identifiers to a common schema, removing duplicates, and validating consistency. This skill ensures that spectral data from multiple repositories can be reliably merged and searched using unified chemical nomenclature.

## When to use

When integrating MS/MS spectra from multiple source repositories or instruments into a unified library, and the compound identifiers, adduct annotations, collision energies, and instrument types differ in format, terminology, or completeness across sources. Apply this skill before spectral matching or when duplicate spectra must be detected and consolidated.

## When NOT to use

- Input spectra are already fully standardized to a single schema and have been deduplicated (re-harmonization is redundant).
- Spectral library is from a single, well-curated source with consistent annotation practices (mapping adds no value).
- Goal is spectral similarity matching only, without the need for unified metadata or cross-repository integration.

## Inputs

- raw MS/MS spectra in MGF format
- heterogeneous metadata files (CSV, JSON, or MGF headers) containing compound identifiers, adduct types, collision energies, and instrument annotations from multiple sources

## Outputs

- harmonized and deduplicated MS/MS spectral library in MGF format
- validated metadata conforming to unified schema (standardized compound identifiers, adduct annotations, collision energies, instrument types)
- duplicate candidate report with pairwise cosine scores

## How to apply

Load raw MS/MS spectral data and associated metadata files from source repositories. Execute repository mapping functions to standardize metadata fields including compound identifiers (e.g., InChI, SMILES), adduct annotations ([M+H]+, [M-H]−, etc.), collision energies, and instrument types to a common schema. Standardize SMILES strings using chemical canonicalization libraries, remove unwanted or malformed adducts, and correct incoherent annotations. Validate harmonized metadata against schema requirements to flag missing or conflicting values. Finally, identify and remove duplicate spectra by calculating pairwise cosine similarity scores and selecting representative spectra based on quality thresholds, with final metadata standardization of instrument and collision energy fields before export.

## Related tools

- **matchms** (Preprocessing and metadata repair of MS/MS spectra; applies library cleaning filters and corrects adduct and mass annotations) — https://github.com/matchms/matchms
- **SpectralEntropy** (Calculates cosine similarity scores for duplicate detection between harmonized spectra) — https://github.com/YuanyueLi/SpectralEntropy.git
- **spectraverse-analysis** (Orchestrates the complete preprocessing, harmonization, and deduplication pipeline via config-driven scripts (step1–step3)) — https://github.com/skinniderlab/spectraverse-analysis

## Examples

```
python run_steps.py --config config/config_step1.json && python run_steps.py --config config/config_step2.json && python run_steps.py --config config/config_step3.json
```

## Evaluation signals

- All compound identifiers conform to the unified schema (e.g., valid SMILES and InChI strings for all entries; no mixed formats within a single metadata field).
- Adduct annotations are standardized and non-redundant (e.g., [M+H]+ appears only once per unique compound and collision energy; zero-charge adducts like [M]+ or [M]− are correctly handled).
- Duplicate spectra are correctly identified by pairwise cosine similarity ≥ threshold (as specified in config) and only one representative per duplicate set remains in the final library.
- Metadata validation reports zero schema violations after harmonization (all required fields populated, no conflicting values for the same spectrum).
- Precursor and fragment mass consistency checks pass: fragment masses do not exceed precursor mass, and neutral mass calculations account for corrected adduct charges.

## Limitations

- Mapping functions depend on accurate and complete source metadata; missing or severely malformed identifiers may cause records to fail harmonization and be excluded.
- SMILES canonicalization and adduct correction rely on external chemistry libraries; errors in standardization propagate downstream and can introduce false duplicates or missed matches.
- Cosine similarity thresholds for duplicate detection must be tuned per library; overly aggressive thresholds may remove legitimate high-quality variants, while permissive thresholds retain near-duplicates.
- The changelog is not documented; version tracking of harmonization rules and schema updates is absent, making reproducibility and rollback difficult across library releases.

## Evidence

- [other] Harmonize metadata fields (compound identifiers, adduct annotations, collision energies, instrument types) to common schema using repository mapping functions.: "Harmonize metadata fields (compound identifiers, adduct annotations, collision energies, instrument types) to common schema using repository mapping functions."
- [intro] Code is used to preprocess and harmonize MS/MS spectra and their associated metadata in the compilation of Spectraverse.: "This repository contains code used to preprocess and harmonize MS/MS spectra and their associated metadata in the compilation of Spectraverse."
- [readme] Standardize SMILES; Removal and correction of unwanted adducts; Standardization of instrument and collision energy fields, and finalizing the metadata.: "step2-3_standardization.py: Standardize SMILES
step3-2_adduct-rem.py: Removal and correction of unwanted adducts
step3-7_metadata.py: Standardization of instrument and collision energy fields, and"
- [readme] Identification of candidate duplicate spectra; Calculating pairwise cosine scores for duplicate spectra; Removal of duplicate spectra based on pairwise cosine scores.: "step3-3_uniq-comb.py: Identification of candidate duplicate spectra
step3-4_uniq-cos-calc.py: Calculating pairwise cosine scores for duplicate spectra and saving in numpy"
- [other] Validate harmonized spectra and metadata against schema requirements and remove duplicates.: "Validate harmonized spectra and metadata against schema requirements and remove duplicates."
