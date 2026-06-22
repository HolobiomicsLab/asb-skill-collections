---
name: spectral-data-preprocessing-normalization
description: Use when you have raw MS/MS spectral data in MGF format from multiple sources or instruments with inconsistent metadata fields, varying intensity scales, and potential low-quality spectra that need standardization before metadata harmonization or spectral library compilation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3643
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - spectraverse-analysis repository
  - spectraverse-analysis
  - matchms
  - SpectralEntropy
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-data-preprocessing-normalization

## Summary

Standardize and clean raw MS/MS spectral data by normalizing intensity values, filtering low-quality spectra, and converting between spectral formats (MGF, CSV, mzML, mzTab) according to repository-defined quality thresholds. This skill prepares heterogeneous spectral libraries for downstream harmonization and curation.

## When to use

Apply this skill when you have raw MS/MS spectral data in MGF format from multiple sources or instruments with inconsistent metadata fields, varying intensity scales, and potential low-quality spectra that need standardization before metadata harmonization or spectral library compilation. Trigger conditions include: receipt of multi-source MGF files, presence of spectra with incomplete or non-standard metadata annotations, or need to merge spectral libraries into a unified format.

## When NOT to use

- Input is already a single-source, internally consistent spectral library with validated metadata and no known duplicates or quality issues.
- Raw spectra have already undergone format conversion and intensity normalization by another preprocessing pipeline.
- Use case requires real-time or streaming spectral processing rather than batch preprocessing of entire libraries.

## Inputs

- Raw MS/MS spectral data in MGF (Mascot Generic Format) files
- Associated metadata files with compound identifiers, adduct annotations, collision energies, instrument types
- Configuration JSON files (config_step1.json, config_step2.json, config_step3.json) specifying script execution order and data paths
- Matchms filter configuration YAML files (library_cleaning_1.yaml, library_cleaning_2.yaml)

## Outputs

- Preprocessed and harmonized MS/MS spectral library in standardized format (mzML, mzTab, or MGF)
- CSV intermediate files with standardized metadata fields
- Cleaned MGF files with validated spectra and removed duplicates
- Numpy format pairwise cosine similarity scores for duplicate candidate spectra

## How to apply

Execute the preprocessing pipeline in three sequential phases using configuration-driven scripts. Phase 1 (config_step1.json): clean MGF files, standardize metadata fields, convert to CSV format, merge files, and convert back to MGF with manual metadata standardization. Phase 2 (config_step2.json): remove duplicate spectra (identical fragment intensities), standardize SMILES representations, filter by precursor/fragment mass coherence, remove low-resolution spectra, and eliminate high fragment masses exceeding precursor m/z. Phase 3 (config_step3.json): identify and remove duplicate spectra using cosine similarity scoring, remove low-intensity noise fragments, and finalize instrument and collision energy annotations. Each phase is followed by matchms library cleaning using YAML-defined filter specifications to repair metadata annotations.

## Related tools

- **spectraverse-analysis** (Master repository containing preprocessing pipeline scripts, configuration templates, and orchestration logic for MGF cleaning, format conversion, and metadata standardization) — https://github.com/skinniderlab/spectraverse-analysis
- **matchms** (Library used to perform spectral preprocessing and metadata repair with YAML-specified filter chains applied between preprocessing phases) — https://github.com/matchms/matchms
- **SpectralEntropy** (Library used to calculate pairwise cosine similarity scores between duplicate candidate spectra for informed removal decisions) — https://github.com/YuanyueLi/SpectralEntropy.git

## Examples

```
python run_steps.py --config config/config_step1.json && python run_steps.py --config config/config_step2.json && python run_steps.py --config config/config_step3.json
```

## Evaluation signals

- All input MGF spectra successfully parse and convert through intermediate CSV format without data loss or format errors.
- Preprocessed library exhibits zero duplicate spectra when assessed by cosine similarity scoring above the removal threshold.
- Metadata fields (compound identifiers, adducts, collision energies, instrument types) conform to unified schema with no missing required annotations.
- Low-quality spectrum removal (low resolution, high fragment masses exceeding precursor m/z, identical fragment intensities) reduces library size by expected percentage relative to input size.
- Output spectral library validates against schema requirements (e.g., each spectrum has precursor m/z, ≥1 fragment annotation, consistent adduct annotation).

## Limitations

- Pipeline execution order is strict; each phase depends on outputs of the previous phase, making parallelization or selective re-runs difficult.
- Matchms library requires custom modifications (provided as spectraverse/matchms.zip) to correctly handle spectra with [M]+ or [M]− adducts annotated with zero charge; default matchms may produce incorrect neutral mass calculations.
- Cosine similarity-based duplicate detection requires manual tuning of similarity threshold for removal decisions; no single universal threshold is provided for all spectral types.
- No changelog or version history is documented in the repository, limiting reproducibility tracking and rollback capability.

## Evidence

- [intro] code used to preprocess and harmonize MS/MS spectra and their associated metadata: "This repository contains code used to preprocess and harmonize MS/MS spectra and their associated metadata in the compilation of Spectraverse."
- [readme] sequential three-phase pipeline structure with intermediate matchms application: "Step 1: Run the initial preprocessing. Step 2: Run matchms using filters specified in matchms/library_cleaning_1.yaml. Step 3: Run the second preprocessing step. Step 4: Run matchms again using"
- [readme] MGF cleaning, metadata standardization, format conversion, and merging operations: "step1-1_mgf-clean.py: MGF cleaning and metadata standardization; step1-2_mgf2csv.py: MGF to CSV conversion; step1-3_merge-csv.py: Merge CSV files; step1-4_merge-mgf.py: Merge MGF files;"
- [readme] duplicate removal, quality filtering, and adduct standardization: "step2-2_cleaning.py: Cleaning metadata and MGF files by removing spectra with identical fragment intensities; step2-3_standardization.py: Standardize SMILES; step2-5_lowres-check.py: Removal of"
- [readme] final duplicate identification and cosine scoring methodology: "step3-3_uniq-comb.py: Identification of candidate duplicate spectra; step3-4_uniq-cos-calc.py: Calculating pairwise cosine scores for duplicate spectra and saving in numpy format;"
- [readme] matchms customization requirement for charge handling: "this version fixes the function _get_neutral_mass to ignore spectra annotated with [M]+ or [M]− adducts that had a reported charge of zero."
