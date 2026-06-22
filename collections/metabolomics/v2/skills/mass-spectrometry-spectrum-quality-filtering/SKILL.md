---
name: mass-spectrometry-spectrum-quality-filtering
description: Use when compiling or harmonizing MS/MS spectral libraries from multiple source repositories and you need to identify and remove spectra that fail quality thresholds (low resolution, precursor-fragment mass inconsistency, duplicate fragment patterns, noise-dominated, or missing critical metadata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - spectraverse-analysis repository
  - matchms
  - SpectralEntropy
  - spectraverse-analysis
  techniques:
  - LC-MS
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

# mass-spectrometry-spectrum-quality-filtering

## Summary

Removal and quality control of MS/MS spectra based on spectral integrity, metadata coherence, and mass accuracy criteria. This skill is applied during curation of small molecule spectral libraries to eliminate low-resolution, duplicative, or analytically uninformative spectra before downstream analysis.

## When to use

Apply this skill when compiling or harmonizing MS/MS spectral libraries from multiple source repositories and you need to identify and remove spectra that fail quality thresholds (low resolution, precursor-fragment mass inconsistency, duplicate fragment patterns, noise-dominated, or missing critical metadata annotations). Trigger conditions include: raw MGF/mzML files from heterogeneous instrument platforms, presence of identical fragment intensity patterns across nominally different spectra, or fragments with m/z values exceeding the precursor m/z.

## When NOT to use

- Input is already a manually curated, instrument-specific reference library with no known duplicates or quality issues — re-filtering risks losing valid spectra and introduces redundant computational cost.
- Your workflow requires retention of all spectral variants (e.g., same compound acquired at multiple collision energies, different adducts) for comparative analysis — aggressive duplicate removal may conflate distinct biological or chemical signals.
- Spectra are already in a harmonized, single-vendor format (e.g., direct output from a commercial MS data system with built-in QA) — schema-based filtering may be sufficient without mass accuracy or resolution checks.

## Inputs

- Raw MGF (Mascot Generic Format) spectral files
- CSV metadata tables (compound ID, adduct annotation, collision energy, instrument type, m/z values)
- Preprocessed MS/MS spectra with normalized intensity values

## Outputs

- Filtered and deduplicated MGF library
- Quality-validated CSV metadata table
- Pairwise cosine similarity scores (numpy format) for duplicate candidate pairs
- QC report (removal counts and criteria applied per step)

## How to apply

Execute a multi-stage filtering pipeline: (1) perform low-resolution detection by comparing observed fragment mass spacing against expected instrumental resolution; (2) validate precursor m/z and fragment m/z consistency by checking that fragment masses do not exceed precursor mass and that reported adducts ([M]+, [M]−, etc.) match neutral mass calculations; (3) identify duplicate spectra by calculating pairwise cosine similarity scores and retain only the highest-quality example (based on signal-to-noise or spectral completeness); (4) remove spectra with all fragment m/z > PRECURSOR_MZ, a sign of annotation error or instrumental artifact; (5) filter low-intensity noise fragments and spectra lacking adduct or collision energy annotations; (6) validate the resulting library against the target metadata schema and confirm no orphaned or contradictory annotations remain.

## Related tools

- **matchms** (Spectrum preprocessing, adduct annotation repair, and metadata harmonization prior to and after quality filtering steps) — https://github.com/matchms/matchms
- **SpectralEntropy** (Calculation of cosine similarity scores for duplicate spectrum detection and selection) — https://github.com/YuanyueLi/SpectralEntropy.git
- **spectraverse-analysis** (Orchestration of multi-step filtering pipeline (steps 2 and 3) and MGF/CSV conversion utilities) — https://github.com/skinniderlab/spectraverse-analysis

## Examples

```
python run_steps.py --config config/config_step2.json && python run_steps.py --config config/config_step3.json
```

## Evaluation signals

- Schema validation pass: all remaining spectra contain required metadata fields (compound identifier, adduct annotation, collision energy, instrument type) and conform to Spectraverse target schema.
- No fragments exceed precursor m/z: verify that max(fragment_mz) ≤ precursor_mz for 100% of retained spectra, and count of removed spectra with this violation matches step2-7 output.
- Duplicate removal correctness: confirm that pairs of spectra with cosine similarity > threshold (e.g., 0.8) have been reduced to a single representative, and that the retained spectrum has the higher signal-to-noise or spectral completeness rank.
- Low-resolution artifact removal: spectra with uniform or near-uniform fragment spacing (indicative of instrumental binning or calibration failure) are removed; verify removal count and examples in QC log.
- Metadata coherence: adduct annotation matches reported neutral mass ± mass tolerance (e.g., ±5 ppm for high-resolution instruments); no spectra carry conflicting adduct or charge annotations after filtering.

## Limitations

- Cosine similarity thresholds for duplicate detection are sensitive to spectral preprocessing parameters (intensity normalization, noise floor); artifacts in earlier preprocessing steps (e.g., baseline correction errors) can inflate false-positive duplicates.
- Low-resolution detection relies on hard cutoffs (e.g., minimum fragment spacing) that may not generalize across different MS instrument classes (TOF, Orbitrap, quadrupole); calibration drift or instrument-specific tuning can cause both false positives and negatives.
- Precursor m/z validation assumes that adduct annotations are correct at input; conflicting or ambiguous adduct assignments (e.g., [M]+ or [M]− with charge = 0, as fixed by the modified matchms version) must be detected and corrected upstream.
- Manual standardization of metadata fields (e.g., collision energy normalization, instrument name synonyms) is performed in step 1-5 and requires human curation; no fully automated mapping exists for all vendor-specific annotation conventions.
- Repository does not provide a version-controlled changelog; updates to filtering thresholds, scoring metrics, or removal criteria are not explicitly documented, hampering reproducibility across releases.

## Evidence

- [other] Execute preprocessing pipeline to standardize spectral formats, normalize intensity values, and filter low-quality spectra according to repository-defined quality thresholds.: "Execute preprocessing pipeline to standardize spectral formats, normalize intensity values, and filter low-quality spectra according to repository-defined quality thresholds."
- [readme] step2-2_cleaning.py: Cleaning metadata and MGF files by removing spectra with identical fragment intensities: "step2-2_cleaning.py: Cleaning metadata and MGF files by removing spectra with identical fragment intensities"
- [readme] step2-5_lowres-check.py: Removal of low-resolution spectra: "step2-5_lowres-check.py: Removal of low-resolution spectra"
- [readme] step2-6_prec-check.py: Removal of spectra based on precursor and fragment mass check: "step2-6_prec-check.py: Removal of spectra based on precursor and fragment mass check"
- [readme] step2-7_highfragmass-check.py: Removal of spectra with all fragment mass > PRECURSOR_MZ: "step2-7_highfragmass-check.py: Removal of spectra with all fragment mass > PRECURSOR_MZ"
- [readme] step3-4_uniq-cos-calc.py: Calculating pairwise cosine scores for duplicate spectra: "step3-4_uniq-cos-calc.py: Calculating pairwise cosine scores for duplicate spectra"
- [readme] step3-5_uniq-select.py: Removal of duplicate spectra based on pairwise cosine scores: "step3-5_uniq-select.py: Removal of duplicate spectra based on pairwise cosine scores"
- [readme] step3-6_noise-rem.py: Removal of low-intensity fragment ions and additional structurally uninformative spectra: "step3-6_noise-rem.py: Removal of low-intensity fragment ions and additional structurally uninformative spectra"
- [readme] this version fixes the function _get_neutral_mass to ignore spectra annotated with [M]+ or [M]− adducts that had a reported charge of zero.: "this version fixes the function _get_neutral_mass to ignore spectra annotated with [M]+ or [M]− adducts that had a reported charge of zero."
