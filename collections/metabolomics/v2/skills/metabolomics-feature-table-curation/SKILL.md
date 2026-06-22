---
name: metabolomics-feature-table-curation
description: Use when you have a raw feature table (TSV/CSV) derived from LC-MS peak detection (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - ThermoRawFileParser
  - Python
  - Asari
  - PCPFM (PythonCentricPipelineForMetabolomics)
  - metDataModel
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
---

# metabolomics-feature-table-curation

## Summary

Curation of LC-MS feature tables through blank masking, normalization, batch correction, and quality control to produce analysis-ready metabolomics datasets. This skill removes contamination, corrects for systematic bias, and prepares feature abundance matrices for downstream statistical analysis.

## When to use

Apply this skill when you have a raw feature table (TSV/CSV) derived from LC-MS peak detection (e.g. from Asari), accompanied by sample metadata indicating blank, QC, or unknown sample types, and your goal is to remove features with low signal-to-noise relative to process blanks, correct for batch effects, normalize across samples, and produce a curated table suitable for univariate or multivariate analysis.

## When NOT to use

- Input is a targeted feature list or a pre-curated, publication-ready table already filtered by domain experts; re-applying blank masking and normalization may remove biologically relevant low-abundance features or introduce artifacts.
- Sample metadata lacks clear blank/unknown designations or batch information; blank masking and batch correction cannot be reliably applied without these critical fields.
- Raw mass spectrometry files have not yet been converted to a feature table; apply peak detection (Asari) first before curation.

## Inputs

- raw feature table (TSV/CSV from Asari or comparable peak detection tool)
- sample metadata CSV file with columns: sample name/ID, file path, sample_type (e.g. 'Blank', 'QC', 'Unknown'), and optional batch/acquisition order information

## Outputs

- curated feature table (TSV) with blank-filtered, normalized, and batch-corrected abundances, ready for downstream analysis
- QA/QC figures (PCA, t-SNE plots) summarizing batch structure and sample relationships
- experiment summary JSON with curation parameters and feature retention statistics

## How to apply

First, load the feature table and sample metadata file into PCPFM, identifying blank samples (e.g. via 'sample_type' column) and unknown/study samples. Apply blank masking by computing median or mean feature intensity across blank samples and study samples (excluding zeros), then calculating the intensity ratio (unknown/blank) and retaining only features where this ratio meets or exceeds the blank_intensity_ratio threshold (default 3). Next, apply data normalization (e.g. median normalization or quantile normalization) to account for run-to-run variation, then perform batch correction if samples were acquired in multiple batches (using parameters specified in the sample metadata). Finally, apply quality control filters (e.g. relative standard deviation thresholds in QC samples) and export the curated feature table in standardized format (.tsv or JSON) with preserved feature annotations and sample metadata.

## Related tools

- **Asari** (performs peak detection and generates the raw feature table (mzML → feature table) prior to curation) — https://github.com/shuzhao-li/asari
- **Python** (execution environment for PCPFM curation pipeline; implements blank masking, normalization, and batch correction algorithms)
- **PCPFM (PythonCentricPipelineForMetabolomics)** (orchestrates full curation workflow including blank masking, normalization, batch correction, QC, and annotation integration) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **metDataModel** (defines standardized data structures for feature tables, metadata, and empirical compound annotations within the curation pipeline) — https://github.com/shuzhao-li-lab/metDataModel

## Examples

```
pcpfm curate --input raw_feature_table.tsv --metadata sequence.csv --blank_intensity_ratio 3.0 --normalization median --batch_correction comBat --output curated_feature_table.tsv
```

## Evaluation signals

- Feature count decreases after blank masking; verify that features removed have intensity ratio (unknown/blank) < blank_intensity_ratio threshold (default 3) by spot-checking a sample of filtered features.
- PCA/t-SNE plots show reduced batch clustering and improved within-group sample cohesion after normalization and batch correction, compared to uncorrected data.
- Relative standard deviation (RSD) of QC samples across all features should decrease (typically < 30%) after normalization; compare RSD before and after.
- Feature table schema validation: verify output TSV contains expected columns (feature ID, m/z, RT, sample abundances) and matches metDataModel structure; no missing or NaN-only columns.
- Sample metadata preservation: confirm that all input samples appear in the output table; no samples are silently dropped during curation.

## Limitations

- Blank masking assumes that blank and unknown samples are correctly designated in the metadata; misclassification (e.g., labeling a low-analyte true sample as 'blank') will remove genuine features.
- Default blank_intensity_ratio threshold (3×) may be too stringent for trace metabolites or too lenient for highly contaminated blanks; threshold should be validated empirically for each dataset or instrument platform.
- Batch correction methods (e.g. ComBat, quantile normalization) can over-correct and mask true biological differences when batch and phenotype are confounded; careful experimental design and metadata annotation are required.
- The pipeline is currently designed for LC-MS data; support for GC-MS and other ionization modes is under development (per README), limiting applicability to non-LC datasets.

## Evidence

- [other] features whose intensity in unknown samples is not at least the specified ratio times more than blank samples are dropped: "features whose intensity in unknown samples is not at least the specified ratio times more than blank samples are dropped."
- [other] For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values: "For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values."
- [intro] data normalization and batch correction: "data normalization and batch correction"
- [readme] designed to take raw LC-MS metabolomics data and ready them for downstream statistical analysis: "designed to take raw LC-MS metabolomics data and ready them for downstream statistical analysis"
- [intro] Asari supports a visual dashboard to explore and inspect individual features: "Asari supports a visual dashboard to explore and inspect individual features"
- [readme] Outputs are intended to be immediately usable for downstream analysis (e.g. MetaboAnalyst or common tools in R, Python etc.): "Outputs are intended to be immediately usable for downstream analysis (e.g. MetaboAnalyst or common tools in R, Python etc.)."
