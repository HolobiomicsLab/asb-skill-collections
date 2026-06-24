---
name: feature-intensity-ratio-calculation
description: Use when after generating a feature table from LC-MS/MS data when your
  experiment includes blank control samples and you need to remove features driven
  by background ions or instrumental contamination.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Asari
  - PCPFM (Python-Centric Pipeline for Metabolomics)
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

# feature-intensity-ratio-calculation

## Summary

Blank masking uses intensity ratios between study and blank samples to identify and remove features likely arising from background contamination rather than true biological signal. Features are retained only when their median intensity in unknown samples exceeds a user-specified multiple (typically 3×) of their median intensity in blank samples.

## When to use

Apply this skill after generating a feature table from LC-MS/MS data when your experiment includes blank control samples and you need to remove features driven by background ions or instrumental contamination. This is especially critical when blank samples are run in the same batch as study samples, as blank masking helps distinguish true analytes from carry-over or environmental background.

## When NOT to use

- Your experiment has no blank control samples or blanks were not analyzed in the same batch as study samples.
- Your features are already log-transformed or normalized in a way that makes intensity ratios meaningless.
- You require retention of all detected features for exploratory analysis (blank masking is destructive and cannot be reversed).

## Inputs

- Feature table (TSV/CSV with features as rows, samples as columns, intensity values)
- Experiment metadata (CSV with sample identifiers and type field designating blanks vs. unknowns)
- query_field name (metadata column used to categorize samples)
- blank_value and sample_value (strings matching blank and study sample designations in query_field)

## Outputs

- Filtered feature table (same format as input, with low-intensity features removed)
- Experiment metadata reference (updated in experiment.json)

## How to apply

Load the feature table and experiment metadata, then identify samples designated as blanks (blank_value) versus study samples (sample_value) using a query_field in the metadata. For each feature, compute the median intensity excluding zero values separately for blanks and for unknowns. Retain only features where the study-sample median intensity is at least blank_intensity_ratio times the blank-sample median (default ratio = 3). Features failing this threshold are dropped from the output table. The rationale is that true biological features should be substantially enriched in study samples relative to procedural blanks, while contaminants show comparable intensities across both.

## Related tools

- **Asari** (Upstream tool that generates the initial feature table from mzML data; blank masking is a QC filter applied post-Asari) — https://github.com/shuzhao-li/asari
- **PCPFM (Python-Centric Pipeline for Metabolomics)** (Pipeline framework that orchestrates blank masking as an optional QC step alongside normalization and batch correction) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Python** (Implementation language for calculating median intensities and applying the intensity ratio filter)

## Evaluation signals

- Verify that the output feature table has fewer rows than the input (features with low blank ratios are removed).
- Check that all retained features have study-sample intensity ≥ blank_intensity_ratio × blank-sample intensity; spot-check 5–10 features via manual calculation.
- Confirm that the number and identity of samples (columns) remain unchanged; only features (rows) are filtered.
- Validate that zero-intensity values were excluded from ratio calculations (i.e., the median is computed only over non-zero intensities in each group).
- Cross-reference the experiment.json to ensure the new_moniker points to the filtered table and the filtering parameters (blank_intensity_ratio, query_field, blank_value, sample_value) are logged.

## Limitations

- The default ratio threshold (3×) is user-configurable but not data-adaptive; no method is provided to estimate an optimal ratio from the data itself.
- Blank masking assumes blanks and study samples are comparable in volume and processing; if blank samples were prepared differently (e.g., lower input mass), the ratio may be biased.
- Features with zero intensity in all blank samples will have undefined or infinite ratios; the implementation must handle this explicitly to avoid NaN/Inf artifacts.
- The skill is destructive: features below the threshold cannot be recovered; exploratory workflows may prefer flagging low-ratio features instead of removing them.

## Evidence

- [other] Blank masking compares feature intensity between study samples and blank samples using a user-specified ratio threshold (blank_intensity_ratio); features are retained only if their intensity in unknown samples is at least N times higher than in blanks, with a default ratio of 3, and the operation excludes zero-intensity values from the ratio calculation.: "features are retained only if their intensity in unknown samples is at least N times higher than in blanks, with a default ratio of 3, and the operation excludes zero-intensity values from the ratio"
- [other] For each feature, calculate the median intensity (excluding zeros) in blank samples and in study samples. Retain only features where study-sample intensity ≥ blank_intensity_ratio × blank-sample intensity.: "For each feature, calculate the median intensity (excluding zeros) in blank samples and in study samples. Retain only features where study-sample intensity ≥ blank_intensity_ratio × blank-sample"
- [readme] feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM: "feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated"
- [other] How does the blank masking step identify and remove features that are likely due to background contamination rather than true biological signal?: "identify and remove features that are likely due to background contamination rather than true biological signal"
- [other] Blank masking to remove features likely due to background ions and contaminants: "Blank masking to remove features likely due to background ions and contaminants"
