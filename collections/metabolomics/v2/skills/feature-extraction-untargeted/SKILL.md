---
name: feature-extraction-untargeted
description: Use when when you have raw untargeted LC/MS data in mzML or mzXML format and need to detect and quantify metabolite signals across mass-to-charge and retention time dimensions without prior knowledge of instrument parameters, batch effects, or optimal detection thresholds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - mzEmbed
derived_from:
- doi: 10.1101/2025.01.26.634927v3
  title: mzLearn
evidence_spans:
- mzEmbed, a framework for developing pre-trained generative models and fine-tuning them for specific tasks for untargeted metabolomics datasets
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
---

# feature-extraction-untargeted

## Summary

mzLearn is a data-driven LC/MS signal detection algorithm that autonomously extracts metabolite features (peaks) from raw untargeted LC/MS data without requiring manual parameter tuning or QC samples. It processes raw mass spectrometry files to produce a standardized feature abundance table suitable for downstream metabolomics analysis and model development.

## When to use

When you have raw untargeted LC/MS data in mzML or mzXML format and need to detect and quantify metabolite signals across mass-to-charge and retention time dimensions without prior knowledge of instrument parameters, batch effects, or optimal detection thresholds. Use this skill at the entry point of an untargeted metabolomics workflow, especially for large-scale studies where manual parameter optimization is infeasible.

## When NOT to use

- Input is already a processed feature table or feature matrix — mzLearn is for raw signal detection, not re-processing existing features.
- Data is in targeted mode with known metabolite m/z values and retention times — mzLearn is designed for untargeted discovery.
- Input files are not in mzML or mzXML format and cannot be converted — mzLearn requires open-source mass spectrometry formats.

## Inputs

- Raw LC/MS data files (mzML or mzXML format)
- One or more untargeted LC/MS runs from a cohort or study

## Outputs

- Two-dimensional feature abundance table (CSV or mzTab) with columns: m/z (median), retention time (median), intensity (normalized across samples)
- Feature matrix suitable for metabolite annotation or machine learning (shape [n_samples, 2736])

## How to apply

Load raw LC/MS data files (mzML or mzXML format) into mzLearn. The algorithm iteratively learns signal characteristics autonomously, correcting for retention time and intensity drifts caused by batch effects and run order, without requiring user-specified parameters. The zero-parameter design means no QC samples or prior tuning is needed. mzLearn outputs a two-dimensional feature table with median m/z and retention time values for each detected feature, along with normalized intensity measurements across all samples. The resulting feature abundance table (typically with ~2,736 robust features) is then formatted as CSV or mzTab for downstream metabolite annotation or as standardized input (floats, z-scored, shape [n_samples, 2736]) for pre-trained generative model pipelines like mzEmbed.

## Related tools

- **mzEmbed** (Framework for consuming mzLearn feature tables to develop pre-trained generative models and fine-tune them for metabolomics tasks) — https://github.com/ReviveMed/mzEmbed

## Examples

```
# Load raw LC/MS data and apply mzLearn signal detection via mzEmbed (no parameters needed)
from mz_embed.signal_detection import mzlearn_detect
feature_table = mzlearn_detect(input_files=['sample1.mzML', 'sample2.mzML', ...], output_dir='/path/to/features')
```

## Evaluation signals

- Output feature table has shape [n_samples, expected_feature_count] with no missing values in m/z, retention time, or intensity columns.
- Feature intensity values are normalized and comparable across all samples (e.g., z-scored or log-transformed).
- Detected features span the expected m/z range for the instrument and study (e.g., 50–1200 m/z for typical small-molecule metabolomics).
- Retention time values are monotonically increasing or clustered within expected chromatographic windows, with no implausible negative or >120 min values for typical LC.
- Feature count is stable across large cohorts and consistent with prior literature or internal validation (e.g., ~2,000–3,000 features for robust untargeted metabolomics).

## Limitations

- mzLearn requires raw data in mzML or mzXML format; proprietary vendor formats must be converted first, which may introduce artifacts.
- Iterative learning assumes sufficient sample diversity; very small cohorts (<10 samples) may not allow robust batch-effect correction.
- Output is a standardized 2,736-feature set; features rare or instrument-specific to a single study may be filtered out or merged.
- Signal detection depends on ion abundance and noise levels; very low-abundance metabolites or highly noisy runs may be missed.

## Evidence

- [readme] mzLearn is a data-driven algorithm designed to autonomously detect metabolite signals from raw LC/MS data without requiring input parameters from the user.: "mzLearn is a data-driven algorithm designed to autonomously detect metabolite signals from raw LC/MS data without requiring input parameters from the user."
- [readme] The algorithm processes raw LC/MS data files in the open-source `mzML` format, iteratively learning signal characteristics to ensure high-quality signal detection.: "The algorithm processes raw LC/MS data files in the open-source `mzML` format, iteratively learning signal characteristics to ensure high-quality signal detection."
- [readme] Zero-parameter design: No prior knowledge or QC samples are required. Iterative learning: mzLearn autonomously refines signal detection, correcting for retention time (rt) and intensity drifts caused by batch effects and run order.: "mzLearn autonomously refines signal detection, correcting for retention time (rt) and intensity drifts caused by batch effects and run order."
- [readme] Output: A two-dimensional table of detected features defined by median rt and m/z values, with normalized intensities across samples.: "A two-dimensional table of detected features defined by median rt and m/z values, with normalized intensities across samples."
- [readme] Capable of handling large-scale datasets (e.g., 2,075 files in a single run).: "Capable of handling large-scale datasets (e.g., 2,075 files in a single run)."
- [other] Extract and quantify detected signals, generating a feature abundance table with m/z values, retention times, and intensity measurements.: "Extract and quantify detected signals, generating a feature abundance table with m/z values, retention times, and intensity measurements."
