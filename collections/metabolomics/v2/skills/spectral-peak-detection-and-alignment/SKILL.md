---
name: spectral-peak-detection-and-alignment
description: Use when after noise filtering and baseline correction have been applied to mass spectrometry data (DI-MS, ASAP-MS, LDI-MS, or other high-throughput MS formats in mzML, mzXML, or vendor formats).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RapidMass
  - DI-MS
  - ASAP-MS
  techniques:
  - direct-infusion-MS
derived_from:
- doi: 10.1021/acs.analchem.4c05062
  title: RapidMass
evidence_spans:
- We have developed a versatile software platform, RapidMass.
- We have developed a versatile software platform, RapidMass
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapidmass_cq
    doi: 10.1021/acs.analchem.4c05062
    title: RapidMass
  dedup_kept_from: coll_rapidmass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05062
  all_source_dois:
  - 10.1021/acs.analchem.4c05062
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Peak Detection and Alignment

## Summary

Automated identification and localization of mass spectrometry peaks across preprocessed spectra, followed by alignment to enable consistent feature comparison across samples. This skill is essential for converting raw spectral noise into discrete, reproducible ion signals suitable for species discrimination and database matching.

## When to use

Apply this skill after noise filtering and baseline correction have been applied to mass spectrometry data (DI-MS, ASAP-MS, LDI-MS, or other high-throughput MS formats in mzML, mzXML, or vendor formats). Use it when you need to extract discrete m/z peaks for database search, when comparing multiple samples and require consistent peak identification across the cohort, or when preparing data for unknown sample scoring and species authentication.

## When NOT to use

- Input spectra have not yet been preprocessed (noise-filtered and baseline-corrected); apply preprocessing first.
- You require only raw spectral visualization without quantitative peak assignment; direct spectral plotting is sufficient.
- Peak alignment has already been performed and you are working with a pre-aligned feature matrix; skip to database search or statistical analysis.

## Inputs

- Preprocessed mass spectra (noise-filtered, baseline-corrected) in mzML, mzXML, or native vendor formats
- Mass spectrometry data from DI-MS, ASAP-MS, LDI-MS, or other ambient ionization MS methodologies
- Sample batch metadata (optional: ground-truth species labels for validation)

## Outputs

- Aligned peak list: m/z values and intensities per sample, with consistent peak identities across the cohort
- Peak detection report: number of peaks detected per sample, signal-to-noise ratios
- Visual outputs: annotated spectra showing detected peaks overlaid on raw data

## How to apply

RapidMass applies automatic peak detection to preprocessed spectra using its integrated peak detection algorithm, which identifies interested MS peaks by their signal intensity and m/z position above noise thresholds established during baseline correction. The algorithm produces a list of detected peaks (m/z values and intensities) for each sample spectrum. Peak alignment is then performed to ensure that the same chemical species (same m/z value) is consistently represented across all spectra in a batch, accounting for small m/z shifts due to instrument calibration variation. The aligned peak list serves as the input to subsequent database search algorithms for unknown sample scoring. Evaluate correctness by confirming that detected peaks correspond to known adducts or fragment ions in reference spectra, that alignment does not merge distinct peaks separated by >0.05 Da (typical MS resolution), and that peak intensities remain reproducible across technical replicates.

## Related tools

- **RapidMass** (Integrates peak detection algorithm and provides automatic identification of interested MS peaks, with support for multiple instrument formats and user-friendly visual interface for review and refinement) — github.com/Katherine00689/RapidMass
- **DI-MS** (Source instrument for direct infusion mass spectrometry data; peak detection and alignment validated on DI-MS spectra)
- **ASAP-MS** (Source instrument for atmospheric solid analysis probe mass spectrometry; peak detection and alignment validated on ASAP-MS spectra)

## Evaluation signals

- Detected peaks correspond to known molecular ions or adducts in reference spectra; verify by cross-reference with compound mass databases (e.g., m/z matches within instrument tolerance ±0.01 Da or ±5 ppm for high-resolution MS).
- Peak alignment accuracy: identical m/z peaks across replicates align to the same feature identity; measure by checking that technical replicates show peak intensity reproducibility (coefficient of variation <15% for major peaks).
- No spurious peak merging: distinct peaks separated by ≥0.05 Da (within instrument resolution) remain separate in the aligned peak list.
- Species discrimination performance: when applied to validation datasets of easily confused plant materials, authenticated species correctly via database matching against known-species peak fingerprints (accuracy metric reported in manuscript).
- Visual outputs show detected peaks consistently positioned and annotated across all sample spectra; no missed peaks in regions of high signal-to-noise ratio.

## Limitations

- Peak detection performance depends on prior noise filtering and baseline correction quality; poor preprocessing leads to false positives (noise peaks) or false negatives (weak signal peaks below threshold).
- Peak alignment assumes that the same m/z value corresponds to the same chemical species across all samples; this assumption fails for isobaric compounds (different species with identical m/z), requiring additional structural confirmation.
- Algorithm performance was validated primarily on plant material samples; applicability to other biological matrices (animal tissues, microbes, synthetic compounds) or MS methodologies not explicitly evaluated in the article remains to be confirmed.
- No changelog or version history documented; reproducibility across software updates is not addressed.

## Evidence

- [readme] Automatic identification of interested MS peaks: "the software provides automatic identification of interested MS peaks"
- [other] Peak detection is part of RapidMass's standard preprocessing pipeline: "Pre-process LDI-MS spectra through RapidMass's standard data pre-processing pipeline (noise filtering, baseline correction, peak detection)"
- [other] Peak detection algorithm execution for unknown sample scoring: "Perform automatic identification of interested MS peaks in LDI-MS spectra using RapidMass's peak detection algorithm"
- [readme] Support for multiple high-throughput MS formats: "supports data from multiple instruments, including DI-MS and ASAP-MS. Other high-throughput mass spectrometry such as ambient ionization mass spectrometry (AI-MS), laser desorption/ionization mass"
- [readme] Validation on plant materials for species discrimination: "The performance of RapidMass was validated using easily confused plant materials, with satisfactory results"
