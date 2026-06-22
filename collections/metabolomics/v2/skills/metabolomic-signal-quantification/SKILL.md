---
name: metabolomic-signal-quantification
description: Use when you have raw untargeted LC/MS data in open mzML or mzXML format and need to extract a quantified feature matrix (m/z and retention time coordinates with sample intensities) without prior knowledge of optimal signal detection parameters, batch effects, or quality control samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - mzEmbed
  - mzLearn
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.01.26.634927v3
  all_source_dois:
  - 10.1101/2025.01.26.634927v3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-signal-quantification

## Summary

Autonomously detect and quantify metabolite signals from raw LC/MS data (mzML/mzXML format) without manual parameter tuning, producing a feature abundance table with m/z, retention time, and normalized intensity measurements across samples. This is the foundational preprocessing step that enables downstream metabolite annotation and model-based analysis in untargeted metabolomics workflows.

## When to use

You have raw untargeted LC/MS data in open mzML or mzXML format and need to extract a quantified feature matrix (m/z and retention time coordinates with sample intensities) without prior knowledge of optimal signal detection parameters, batch effects, or quality control samples. Use this skill when manual parameter optimization is infeasible (e.g., large cohorts, run-order drift, or unknown instrument calibration) and you require a zero-parameter, data-driven alternative.

## When NOT to use

- Input is already a processed feature abundance table or feature matrix — re-running signal detection would introduce redundant noise and lose sample alignment.
- Targeted LC/MS data with known analyte parameters — use targeted peak extraction or MRM-specific tools instead.
- Data already aligned and quantified by another pipeline (e.g., XCMS, MS-DIAL) — mzLearn's iterative learning requires raw spectral data for drift correction.

## Inputs

- Raw LC/MS data files (mzML or mzXML format)
- Single or batch of LC/MS runs (tested at scale: 2,075+ files)

## Outputs

- Feature abundance table (CSV or mzTab format)
- Two-dimensional feature matrix [n_samples × m_features]
- Feature metadata: m/z values, retention times, normalized intensities
- Z-scored feature matrix suitable for model input

## How to apply

Load raw LC/MS data files in mzML or mzXML format into the mzLearn signal detector within the mzEmbed framework. The algorithm iteratively learns signal characteristics from the data itself, autonomously correcting for retention time and intensity drifts caused by batch effects and run order. No user-provided parameters are required; the algorithm outputs a two-dimensional feature table indexed by median m/z and retention time, with normalized intensities across all samples. The resulting feature matrix is z-scored and formatted (typically 2,736 robust features) for downstream metabolite annotation, model pretraining, or statistical analysis.

## Related tools

- **mzEmbed** (Framework hosting mzLearn signal detection and downstream pre-trained generative model development for untargeted metabolomics) — github.com/ReviveMed/mzEmbed
- **mzLearn** (Data-driven signal detection engine that autonomously detects metabolite peaks and features from raw LC/MS spectra without parameter tuning) — http://mzlearn.com/

## Examples

```
# Load raw LC/MS data and apply mzLearn signal detection
from mz_embed.pretrain import signal_detection
detector = signal_detection.mzLearnDetector()
feature_table = detector.detect('path/to/raw_lcms_data/*.mzML', output_format='csv')
```

## Evaluation signals

- Feature table shape matches expected sample count and reported feature dimension (e.g., [n_samples, 2736] for the standard robust peak set).
- m/z values and retention times are within expected instrument range (typically m/z 50–1200, rt 0–60 min for typical LC/MS methods) with no NaN or infinite values.
- Intensity values are positive (or zero) and normalized across samples; z-scoring applied correctly (mean ≈ 0, std ≈ 1 across features).
- Feature table can be loaded by pandas.read_csv with index_col=0 (row index in first column) and contains numeric entries only.
- Retention time and m/z values show expected correlation structure (features from same metabolite cluster near identical m/z, within ±5 ppm; retention time spread reflects chromatographic resolution).

## Limitations

- Algorithm requires sufficiently large sample cohorts to reliably learn signal characteristics; very small studies (< 20 samples) may not benefit from iterative drift correction.
- Assumes open mzML/mzXML formats; proprietary vendor formats (e.g., .d, .raw) require prior conversion.
- Output assumes z-scored input; non-metabolomic data or extreme batch effects may degrade the iterative learning process.
- Fixed output feature set (e.g., 2,736 robust features) may not capture rare metabolites or instrument-specific low-intensity peaks.
- Retention time alignment is relative; absolute retention time reproducibility depends on LC method consistency across the cohort.

## Evidence

- [readme] mzLearn is a data-driven algorithm designed to autonomously detect metabolite signals from raw LC/MS data without requiring input parameters from the user.: "mzLearn is a data-driven algorithm designed to autonomously detect metabolite signals from raw LC/MS data without requiring input parameters from the user."
- [readme] The algorithm processes raw LC/MS data files in the open-source mzML format, iteratively learning signal characteristics to ensure high-quality signal detection.: "The algorithm processes raw LC/MS data files in the open-source `mzML` format, iteratively learning signal characteristics to ensure high-quality signal detection."
- [readme] mzLearn autonomously refines signal detection, correcting for retention time (rt) and intensity drifts caused by batch effects and run order.: "mzLearn autonomously refines signal detection, correcting for retention time (rt) and intensity drifts caused by batch effects and run order."
- [readme] A two-dimensional table of detected features defined by median rt and m/z values, with normalized intensities across samples.: "A two-dimensional table of detected features defined by median rt and m/z values, with normalized intensities across samples."
- [other] Extract and quantify detected signals, generating a feature abundance table with m/z values, retention times, and intensity measurements.: "Extract and quantify detected signals, generating a feature abundance table with m/z values, retention times, and intensity measurements."
- [readme] Capable of handling large-scale datasets (e.g., 2,075 files in a single run).: "Capable of handling large-scale datasets (e.g., 2,075 files in a single run)."
