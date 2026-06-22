---
name: duplicate-spectrum-detection-removal
description: Use when you have a large collection of MS/MS spectra with harmonized metadata and suspect that spectra for the same compound or adduct acquired under similar conditions may be duplicated or near-identical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# duplicate-spectrum-detection-removal

## Summary

Identify and remove redundant MS/MS spectra from a harmonized spectral library by calculating pairwise cosine similarity scores and filtering based on a coherence threshold. This skill ensures the final library contains only unique, high-quality spectra for metabolomics applications.

## When to use

Apply this skill when you have a large collection of MS/MS spectra with harmonized metadata and suspect that spectra for the same compound or adduct acquired under similar conditions may be duplicated or near-identical. This typically occurs after metadata standardization and before final library export, as a quality control step to remove redundancy that inflates library size without improving annotation coverage.

## When NOT to use

- Input spectra lack standardized metadata fields (compound ID, adduct); duplicate detection relies on consistent annotations and will produce false positives or false negatives if metadata is incomplete or non-standard.
- You need to retain all raw spectra for independent validation or method comparison studies; deduplication is irreversible and removes records that might be scientifically valuable despite redundancy.
- Cosine similarity threshold has not been validated for your specific instrument platform or ionization mode; applying a generic threshold without prior calibration may over-deduplicate or under-deduplicate.

## Inputs

- MGF files with standardized metadata (compound identifier, adduct annotation)
- CSV files containing spectrum-level metadata and quality metrics

## Outputs

- Deduplicated MGF file with candidate duplicates removed
- Numpy arrays of pairwise cosine similarity scores
- Log file documenting which spectra were retained and which were merged or discarded

## How to apply

First, identify candidate duplicate spectra by grouping on compound identifiers and adduct annotations using step 3-3 (uniq-comb.py). Second, calculate pairwise cosine similarity scores for all candidate pairs and store results in numpy format (step 3-4, uniq-cos-calc.py), using the SpectralEntropy library's cosine score implementation. Third, apply a cosine similarity threshold—spectra with scores above this threshold are marked as duplicates—and retain only the highest-quality spectrum from each duplicate group based on user-defined criteria such as spectral completeness or signal-to-noise ratio (step 3-5, uniq-select.py). The rationale is that spectra sharing identical or near-identical fragment patterns and metadata indicate redundant measurements, and keeping only one representative per group reduces library bloat while preserving annotation diversity.

## Related tools

- **matchms** (Preprocessing and scoring of MS/MS spectra; used before and after deduplication to repair and validate metadata coherence) — https://github.com/matchms/matchms
- **SpectralEntropy** (Calculation of cosine similarity scores between pairs of spectra to quantify redundancy) — https://github.com/YuanyueLi/SpectralEntropy.git
- **spectraverse-analysis** (Repository containing the complete deduplication pipeline (steps 3-3 through 3-5) and configuration) — https://github.com/skinniderlab/spectraverse-analysis

## Examples

```
python run_steps.py --config config/config_step3.json
```

## Evaluation signals

- Pairwise cosine similarity matrix is square and symmetric with diagonal values equal to 1.0, confirming that spectra are only compared against other spectra, not against themselves
- No spectra are retained from a duplicate group if all members score below the cosine threshold; all spectra in a group above the threshold belong to the same deduplicated record
- The output MGF file has fewer total spectra than the input, and the reduction count matches the number of spectra flagged as duplicates in the log file
- Compound identifiers and adduct annotations remain unchanged in the deduplicated output; only redundant spectra are removed, not metadata fields
- Visual inspection of a sample of retained spectra shows visually distinct fragmentation patterns, while removed spectra show near-identical peak lists and intensities to their retained counterparts

## Limitations

- Cosine similarity is sensitive to mass accuracy and intensity normalization; spectra with poor mass calibration or non-standard intensity scaling may be incorrectly classified as duplicates or singletons
- Deduplication is performed only within compound–adduct groups; spectra of the same compound in different adduct states (e.g., [M+H]+ vs. [M+Na]+) are not compared and will not be deduplicated, which is correct for annotation purposes but may not reduce library redundancy if the same ion was measured in multiple adduct forms
- No changelog is available in the repository, making it difficult to track changes to the cosine similarity calculation or deduplication thresholds across versions
- The threshold for cosine similarity must be manually set; the README provides no guidance on calibration, and an inappropriate threshold can lead to over-aggressive or insufficient deduplication

## Evidence

- [readme] Identification of candidate duplicate spectra: "step3-3_uniq-comb.py: Identification of candidate duplicate spectra"
- [readme] Cosine score calculation for deduplication: "step3-4_uniq-cos-calc.py: Calculating pairwise cosine scores for duplicate spectra and saving in numpy format"
- [readme] Removal of duplicates based on cosine threshold: "step3-5_uniq-select.py: Removal of duplicate spectra based on pairwise cosine scores"
- [readme] SpectralEntropy for cosine calculation: "# Code used to calculate cosine score
   git clone https://github.com/YuanyueLi/SpectralEntropy.git"
- [intro] Purpose of deduplication in pipeline: "code used to preprocess and harmonize MS/MS spectra and their associated metadata in the compilation of Spectraverse"
