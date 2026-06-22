---
name: m-z-alignment-and-mass-grid-assembly
description: Use when when processing multiple centroided mzML LC-MS files from the same study and you need to identify which mass tracks represent the same metabolite across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - pymzml
  - khipu
  - JMS
  - HMDB 4
  - asari
  - mass2chem
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- The default method uses `pymzml` to parse mzML files.
- The preannotaion is done via another package khipu (https://github.com/shuzhao-li-lab/khipu)
- The empirical compounds are searched against known compound database (default HMDB 4) via another package JMS (https://github.com/shuzhao-li/JMS).
- known compound database (default HMDB 4)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# m/z-alignment-and-mass-grid-assembly

## Summary

Aligns mass tracks (extracted ion chromatograms) across multiple LC-MS samples using high-mass-resolution m/z separation and hierarchical clustering to build a unified MassGrid that serves as the foundation for composite peak detection and feature extraction. This skill prioritizes mass resolution over retention time to handle co-eluting isomers and complex mixtures.

## When to use

When processing multiple centroided mzML LC-MS files from the same study and you need to identify which mass tracks represent the same metabolite across samples. Apply this skill after mass track extraction (binning and clustering within individual samples) but before composite peak detection. Essential when sample cohort is ≤10 samples (pairwise anchor-first mode) or larger (centroiding mode), and when mass resolution is ≥5 ppm tolerance or better.

## When NOT to use

- Input is already a feature table (preferred_Feature_table.tsv or full_Feature_table.tsv); alignment has already been performed.
- Single-sample analysis where no cross-sample alignment is needed.
- Raw (profile-mode) mzML data; asari requires centroided input to define discrete m/z bins.

## Inputs

- Multiple centroided mzML files (one per sample)
- Mass tracks per sample (list of (m/z, intensity, retention time) tuples from chromatograms.extract_massTracks_)
- Tolerance ppm parameter (default 5 ppm)
- Sample registry from workflow.register_samples

## Outputs

- MassGrid object (maps m/z → aligned mass tracks across samples)
- _mass_grid_mapping.csv (tabular export of MassGrid alignments)
- Anchor mass tracks (identified 13C/12C and Na/H adduct relationships)
- Per-sample m/z recalibration vectors (when deviation > 1 ppm)

## How to apply

Extract mass tracks from each sample by binning all MS1 m/z values to 0.001 amu granularity using `chromatograms.get_thousandth_bins`, then cluster bins where m/z range exceeds 2× tolerance ppm (default 5 ppm) using `mass_functions.nn_cluster_by_mz_seeds` to isolate anchor mass tracks for 13C/12C isotopes and Na/H adducts. For ≤10 samples, build the MassGrid using `MassGrid.build_grid_sample_wise` with pairwise anchor-first alignment, establishing anchor mass tracks from isotope and adduct mass differences. For larger cohorts, use `MassGrid.build_grid_by_centroiding` to merge mass tracks via consensus m/z positions. Trigger systematic recalibration whenever m/z deviation across samples exceeds 1 ppm. The resulting MassGrid maps each unique m/z value (at ≥0.001 amu resolution) to a list of (sample, intensity) pairs aligned by retention time calibration.

## Related tools

- **asari** (Main Python package implementing MassGrid.build_grid_sample_wise, MassGrid.build_grid_by_centroiding, chromatograms.get_thousandth_bins, and mass_functions.nn_cluster_by_mz_seeds) — https://github.com/shuzhao-li/asari
- **pymzml** (Parses centroided mzML files to extract MS1 spectra as input to mass track binning)
- **mass2chem** (Provides isotope and adduct mass difference libraries for anchor mass track identification) — https://github.com/shuzhao-li/mass2chem

## Examples

```
python3 -m asari.main process -i mydir/projectx_dir --mode pos
```

## Evaluation signals

- MassGrid contains no duplicate m/z values (each m/z bin is unique to ±0.001 amu or the specified tolerance)
- Cross-sample m/z alignment validates: repeat samples show identical or near-identical m/z positions (deviation ≤ 1 ppm after recalibration)
- Anchor mass tracks (13C/12C, Na/H adducts) are correctly identified by m/z difference (13C = 1.003355 Da, Na–H = 21.9819 Da) in the output _mass_grid_mapping.csv
- Composite mass tracks (sums of aligned intensities) show expected intensity ratios for isotope clusters (13C ~1.1% of 12C for natural compounds) and adduct ratios consistent with ionization efficiency
- Sample coverage: each feature in the MassGrid is present in ≥1 sample (no empty alignments)

## Limitations

- Requires centroided mzML input; profile-mode data must be centroided beforehand (e.g. via ProteoWizard msconvert or ThermoRawFileParser).
- Default 5 ppm tolerance assumes modern high-resolution instruments (Orbitrap, QTOF); lower-resolution data may require broader tolerance, risking false merging of distinct metabolites.
- Anchor mass track identification relies on accurate isotope and adduct mass libraries; contamination or unusual ionization modes may produce spurious anchors.
- MassGrid alignment assumes similar chromatographic behavior across samples; severe retention time shifts (>2 min) or missing landmarks (mSelectivity >0.99) can degrade anchor-based recalibration.
- Performance scales with sample count; centroiding mode is recommended for >10 samples to avoid combinatorial pairwise comparisons.

## Evidence

- [other] Alignment of mass tracks across all samples into a MassGrid using MassGrid.build_grid_sample_wise for ≤10 samples (with pairwise anchor-first alignment) or MassGrid.build_grid_by_centroiding for larger studies: "Alignment of mass tracks across all samples into a MassGrid using MassGrid.build_grid_sample_wise for ≤10 samples (with pairwise anchor-first alignment) or MassGrid.build_grid_by_centroiding for"
- [other] Extract mass tracks for each sample by parsing MS1 spectra with pymzml, binning m/z values to 0.001 amu using chromatograms.get_thousandth_bins, clustering with mass_functions.nn_cluster_by_mz_seeds where m/z ranges exceed 2× tolerance ppm: "Extract mass tracks for each sample by parsing MS1 spectra with pymzml, binning m/z values to 0.001 amu using chromatograms.get_thousandth_bins, clustering with mass_functions.nn_cluster_by_mz_seeds"
- [other] Establish anchor mass tracks for 13C/12C isotopes and Na/H adducts: "Establish anchor mass tracks for 13C/12C isotopes and Na/H adducts"
- [other] systematic recalibration when m/z deviation exceeds 1 ppm: "systematic recalibration when m/z deviation exceeds 1 ppm"
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
- [readme] Transparent, JSON centric data structures, easy to chain other tools: "Transparent, JSON centric data structures, easy to chain other tools"
