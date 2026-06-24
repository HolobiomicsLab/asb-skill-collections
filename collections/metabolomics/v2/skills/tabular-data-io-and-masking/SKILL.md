---
name: tabular-data-io-and-masking
description: Use when after generating a preliminary feature table from LC-MS data
  (e.g., via Asari), when experimental design includes blank samples or negative controls
  and you need to filter out features that are likely instrumental or chemical background
  rather than true biological signal.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Asari
  - metDataModel
  techniques:
  - LC-MS
  license_tier: open
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

# Tabular Data I/O and Blank Masking

## Summary

Load feature tables and experiment metadata, then apply intensity-ratio filtering to remove features dominated by background contamination. Blank masking compares feature intensities between study samples and blank controls using a configurable ratio threshold, retaining only features where true sample signal substantially exceeds blank signal.

## When to use

After generating a preliminary feature table from LC-MS data (e.g., via Asari), when experimental design includes blank samples or negative controls and you need to filter out features that are likely instrumental or chemical background rather than true biological signal. Apply this when blank samples are explicitly labeled in the experiment metadata and before downstream statistical analysis or annotation.

## When NOT to use

- Experiment design lacks blank or negative control samples; blank masking requires explicit blank-sample labels in metadata.
- Feature table has already been blank-masked by an upstream tool (Asari or other preprocessor); applying twice risks over-filtering.
- All features have zero intensity in blanks; the ratio calculation will exclude these and leave the table unchanged, rendering the operation redundant.

## Inputs

- Feature table (TSV/CSV format with features as rows, samples as columns, intensity values)
- Experiment metadata (CSV with sample identifiers, file paths, and sample type annotations)

## Outputs

- Filtered feature table (TSV/CSV, same schema as input but with contamination-driven features removed)
- Updated experiment.json tracking the blank-masking operation and new table moniker

## How to apply

Load the input feature table and experiment metadata, identifying samples via a query_field (e.g., 'Sample Type') that distinguishes blank_value designations (e.g., 'BLANK') from sample_value designations (e.g., 'Unknown'). For each feature, calculate the median intensity, excluding zeros, in blank samples and in study samples separately. Retain only features where the median study-sample intensity is at least N times the median blank-sample intensity, where N defaults to 3 but is user-configurable via blank_intensity_ratio. This thresholding removes low-abundance features that are equally present in blanks and samples, indicating contamination. Write the filtered table to a new output file and record the transformation in experiment.json.

## Related tools

- **Python** (Language for implementing the blank-masking filter logic, loading and comparing feature intensities, and writing outputs)
- **Asari** (Upstream tool that generates the initial feature table from mzML files; blank masking is an optional post-processing step in the PCPFM pipeline) — https://github.com/shuzhao-li/asari
- **metDataModel** (Defines the common data model (feature table schema, experiment metadata structure) that blank masking conforms to) — https://github.com/shuzhao-li-lab/metDataModel

## Evaluation signals

- Feature count after masking is lower than before; verify that dropped features had intensity in blanks ≥ (study_intensity / blank_intensity_ratio).
- No features are dropped if all study samples have intensity ≤ blank_intensity_ratio × blank intensity for every feature (conservative filtering).
- Output table schema is identical to input (same row and column structure), confirming no unintended structural changes.
- Experiment.json is updated with a new table moniker and a log entry documenting blank_intensity_ratio, blank_value, and sample_value parameters used.
- Zero-intensity values in blanks and study samples do not contribute to ratio calculation (verified by checking that features with zero in blanks are always retained).

## Limitations

- Assumes median intensity is a robust summary statistic; skewed or multi-modal distributions in blank or study samples may yield unintuitive thresholds. Outliers in blanks can inflate the threshold and reduce filtering stringency.
- The blank_intensity_ratio threshold (default 3) is empirically chosen and may not be optimal for all instrument platforms, metabolite classes, or contamination profiles. No adaptive or data-driven threshold selection is provided.
- Relies on accurate sample-type metadata; mislabeled blank or study samples will propagate errors into the ratio calculation.
- Does not account for batch effects or instrument drift; features that are elevated uniformly across all study samples due to batch contamination will not be detected by ratio masking alone.

## Evidence

- [other] features are retained only if their intensity in unknown samples is at least N times higher than in blanks, with a default ratio of 3, and the operation excludes zero-intensity values from the ratio calculation: "features are retained only if their intensity in unknown samples is at least N times higher than in blanks, with a default ratio of 3, and the operation excludes zero-intensity values"
- [other] For each feature, calculate the median intensity (excluding zeros) in blank samples and in study samples. Retain only features where study-sample intensity ≥ blank_intensity_ratio × blank-sample intensity.: "calculate the median intensity (excluding zeros) in blank samples and in study samples. Retain only features where study-sample intensity ≥ blank_intensity_ratio × blank-sample intensity"
- [intro] optionally blank masked, normalized, batch corrected, annotated or otherwise curated: "optionally blank masked, normalized, batch corrected, annotated or otherwise curated"
- [readme] This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM and empirical compounds as a JSON file representing putative metabolites: "feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM"
- [other] Parse the query_field and identify samples matching blank_value and sample_value designations.: "Parse the query_field and identify samples matching blank_value and sample_value designations"
