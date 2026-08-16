---
name: peak-detection-optimization-free
description: Use when when processing raw untargeted LC/MS data in mzML or mzXML format
  and you need to detect peaks across mass-to-charge (m/z) and retention time (rt)
  dimensions without prior knowledge of optimal signal detection parameters, QC samples,
  or domain expertise in LC/MS preprocessing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mzEmbed
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1101/2025.01.26.634927v3
  title: mzLearn
evidence_spans:
- mzEmbed, a framework for developing pre-trained generative models and fine-tuning
  them for specific tasks for untargeted metabolomics datasets
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzlearn_cq
    doi: 10.1101/2025.01.26.634927v3
    title: mzLearn
  dedup_kept_from: coll_mzlearn_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.01.26.634927v3
  all_source_dois:
  - 10.1101/2025.01.26.634927v3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-detection-optimization-free

## Summary

Automated LC/MS peak detection using mzLearn, a data-driven algorithm that identifies metabolite signals from raw untargeted LC/MS data without requiring manual parameter tuning or quality control samples. The method iteratively learns signal characteristics to correct for retention time and intensity drifts, outputting a feature abundance table suitable for downstream metabolite annotation.

## When to use

When processing raw untargeted LC/MS data in mzML or mzXML format and you need to detect peaks across mass-to-charge (m/z) and retention time (rt) dimensions without prior knowledge of optimal signal detection parameters, QC samples, or domain expertise in LC/MS preprocessing. Use this skill at the very beginning of an untargeted metabolomics workflow before annotation or generative modeling.

## When NOT to use

- Input is already a processed feature table or intensity matrix — mzLearn is a raw-data-to-features detector, not a post-processing step.
- Targeted LC/MS analysis requiring detection of known metabolites with predefined m/z and retention time windows — mzLearn is designed for untargeted discovery.
- Data in non-standard formats (e.g., proprietary vendor formats without mzML/mzXML conversion) — mzLearn requires open mzML format.

## Inputs

- Raw LC/MS data files in mzML or mzXML format
- One or more LC/MS runs (scalable to large batches, e.g., 2,075 files)

## Outputs

- Two-dimensional feature abundance table (CSV or mzTab format) with dimensions [n_samples, n_features]
- Feature annotations: median m/z values, median retention times, normalized intensities across samples

## How to apply

Load raw LC/MS data in mzML format into mzLearn's signal detector. The algorithm autonomously applies iterative learning to refine signal detection across the full dataset, correcting for retention time and intensity drifts caused by batch effects and run order without user-supplied parameters. The algorithm outputs a two-dimensional feature table indexed by median m/z and retention time values with normalized intensities across samples. No hyperparameter optimization, QC sample preparation, or manual threshold adjustment is required. Verify output by checking that the feature table has expected dimensions (n_samples × ~2,736 robust features) and that retention time and m/z distributions are reasonable for the instrument and method used.

## Related tools

- **mzEmbed** (Framework that accepts mzLearn output feature tables and uses them for pre-trained generative model development and fine-tuning in untargeted metabolomics) — https://github.com/ReviveMed/mzEmbed

## Examples

```
# Load raw LC/MS data in mzML format and run mzLearn signal detection
python -c "from mz_embed.signal_detection import mzLearn; detector = mzLearn(); features = detector.detect_peaks('/path/to/raw_data/*.mzML'); features.to_csv('detected_features.csv')"
```

## Evaluation signals

- Output feature table has shape [n_samples, ~2,736 features] matching the robust mzLearn peak set, with no missing values in m/z or retention time columns.
- Retention time values are within the expected chromatography window (e.g., 0–30 minutes for typical LC gradients) and show no artificial clustering or truncation.
- m/z values span the expected mass range for the mass spectrometer (e.g., 100–1,200 m/z for typical metabolomics) and match known metabolite ion masses (spot check against reference standards or public databases).
- Intensity distributions are approximately log-normal and show expected variation across samples; no sample exhibits zero or near-zero total intensity (indicating successful ionization).
- Normalized intensities are in comparable ranges across samples (no extreme run-to-run drift after drift correction), indicating successful batch effect and run-order correction.

## Limitations

- mzLearn requires data in open mzML format; proprietary vendor formats must be converted first, which may introduce data loss or format-specific artifacts.
- The algorithm is tuned for untargeted metabolomics and may not be optimal for highly targeted, hypothesis-driven studies requiring detection of known analytes with strict m/z or retention time windows.
- Output feature set is fixed at ~2,736 robust features; datasets with unusual mass ranges, ionization conditions, or chemical diversity may benefit from custom re-optimization (though mzLearn is designed to minimize this need).
- Large batch processing (e.g., 2,075 files) may require significant computational resources; runtime scales with dataset size and instrument resolution.

## Evidence

- [readme] mzLearn is a data-driven algorithm designed to autonomously detect metabolite signals from raw LC/MS data without requiring input parameters from the user.: "mzLearn is a data-driven algorithm designed to autonomously detect metabolite signals from raw LC/MS data without requiring input parameters from the user."
- [readme] The algorithm processes raw LC/MS data files in the open-source mzML format, iteratively learning signal characteristics to ensure high-quality signal detection.: "The algorithm processes raw LC/MS data files in the open-source mzML format, iteratively learning signal characteristics to ensure high-quality signal detection."
- [readme] Zero-parameter design: No prior knowledge or QC samples are required.: "Zero-parameter design: No prior knowledge or QC samples are required."
- [readme] mzLearn autonomously refines signal detection, correcting for retention time (rt) and intensity drifts caused by batch effects and run order.: "Iterative learning: mzLearn autonomously refines signal detection, correcting for retention time (rt) and intensity drifts caused by batch effects and run order."
- [readme] Output: A two-dimensional table of detected features defined by median rt and m/z values, with normalized intensities across samples.: "Output: A two-dimensional table of detected features defined by median rt and m/z values, with normalized intensities across samples."
- [other] Apply the data-driven signal detection algorithm to identify peaks and features across the mass-to-charge and retention time dimensions without requiring manual parameter optimization.: "Apply the data-driven signal detection algorithm to identify peaks and features across the mass-to-charge and retention time dimensions without requiring manual parameter optimization."
- [readme] Capable of handling large-scale datasets (e.g., 2,075 files in a single run).: "Capable of handling large-scale datasets (e.g., 2,075 files in a single run)."
