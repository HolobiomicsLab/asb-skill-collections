---
name: metabolomic-feature-table-filtering
description: Use when after feature detection (e.g., Asari processing of mzML files
  to feature tables) but before normalization, batch correction, or annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Python/pandas
  - Asari
  - metDataModel
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm_cq
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-feature-table-filtering

## Summary

Remove unreliable metabolomic features from LC-MS feature tables using intensity-based filtering criteria (blank masking and feature prevalence thresholds). This skill prepares high-quality feature tables for downstream statistical analysis by eliminating background contamination and low-frequency features.

## When to use

Apply this skill after feature detection (e.g., Asari processing of mzML files to feature tables) but before normalization, batch correction, or annotation. Use it when you have a feature table with samples that include blanks or QC controls, or when you need to remove features present in fewer than a specified percentile of study samples to focus on robust, reproducible signals.

## When NOT to use

- Input is already a normalized or batch-corrected feature table; re-filtering may introduce bias.
- Study design lacks blank or QC samples; blank masking cannot be meaningfully applied.
- Features are already curated (e.g., annotated metabolites with known biological relevance); indiscriminate prevalence filtering may discard rare but important compounds.

## Inputs

- Feature table (TSV or CSV format with features as rows, samples as columns, intensity values)
- Experiment metadata (JSON or CSV with sample identifiers, sample type designations, optional batch information)
- Query field string specifying metadata column names for blank_value and sample_value classifications

## Outputs

- Filtered feature table (TSV format, saved to feature_tables subdirectory with new_moniker)
- Updated experiment.json metadata referencing the new filtered table
- Optional: per-sample normalization factors if TIC-based normalization is applied

## How to apply

Execute two sequential filtering operations on the feature table. First, apply blank masking by loading the feature table and experiment metadata, identifying blank and study samples via query_field designations, then calculating median intensity (excluding zeros) for each feature in blank versus study samples. Retain only features where study-sample median intensity is at least N times (default N=3) the blank-sample median intensity. Second, apply feature prevalence filtering by identifying features present across at least the specified percentile threshold (e.g., 90%) of samples, excluding zero-intensity values from presence counts. Calculate per-sample TIC from the filtered feature set and optionally compute normalization factors (median or mean TIC). The rationale is that blank masking removes contamination by comparing signal strength to background, while prevalence filtering prioritizes common, reproducible features that are more likely to be true biological signals rather than rare artifacts.

## Related tools

- **Python/pandas** (Execute feature table loading, filtering logic, intensity calculations, and TSV output) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Asari** (Upstream tool that generates the initial feature table from mzML files that is then filtered by this skill) — https://github.com/shuzhao-li/asari
- **metDataModel** (Defines the data schema and moniker-based reference structure for feature tables and experiment.json) — https://github.com/shuzhao-li-lab/metDataModel

## Evaluation signals

- Blank masking: verify that all retained features have study-sample intensity ≥ blank_intensity_ratio × blank-sample intensity; count and report number of features removed.
- Feature prevalence: confirm that all retained features appear in at least the specified percentile of samples; zero-intensity entries are correctly excluded from presence calculations.
- Output schema: new filtered table is valid TSV with same feature identifiers (rows) as input, subset of samples (columns) if samples were dropped, and all intensity values are non-negative.
- Metadata consistency: experiment.json correctly references new_moniker and links to the filtered table path in feature_tables subdirectory.
- Sanity check: row count decreased (features removed), column count unchanged or decreased (samples optionally removed), no NaN or negative intensities introduced.

## Limitations

- Blank masking assumes zero-intensity values represent true absence, not instrumental noise below detection limit; this may bias median calculations if many features have sporadic zeros.
- Default blank_intensity_ratio of 3 is heuristic; optimal threshold varies by instrument, ionization mode, and sample type and should be tuned or validated per study.
- Feature prevalence filtering (e.g., 90th percentile) is arbitrary and removes rare metabolites that may be biologically important; no guidance is provided on choosing the percentile.
- Batch-aware normalization is mentioned as an option but implementation details and batch effect correction algorithm are not fully specified in the README.
- The pipeline does not yet support GC-MS or other ionization modes; applicability is limited to LC-MS/MS datasets.

## Evidence

- [other] features are retained only if their intensity in unknown samples is at least N times higher than in blanks, with a default ratio of 3, and the operation excludes zero-intensity values from the ratio calculation: "features are retained only if their intensity in unknown samples is at least N times higher than in blanks, with a default ratio of 3, and the operation excludes zero-intensity values from the ratio"
- [other] Filter features to retain only those present in at least the specified percentile of samples (e.g., 90%), excluding zeros from presence calculations: "Filter features to retain only those present in at least the specified percentile of samples (e.g., 90%), excluding zeros from presence calculations"
- [intro] features present in fewer than this percent of samples are dropped: "features present in fewer than this percent of samples are dropped"
- [intro] optionally blank masked, normalized, batch corrected, annotated or otherwise curated: "optionally blank masked, normalized, batch corrected, annotated or otherwise curated"
- [readme] This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM: "This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM"
