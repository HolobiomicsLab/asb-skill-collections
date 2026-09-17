---
name: feature-table-construction-for-multivariate-analysis
description: Use when when you have high-resolution mass-spectrometry (HRMS) breath
  data in mzML or mzXML format from multiple subjects or conditions and need to prepare
  a sample-by-feature intensity matrix for downstream statistical comparison, biomarker
  discovery, or classification tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - BreathXplorer
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.4c00152
  title: BreathXplorer
evidence_spans:
- '[![PyPI](https://img.shields.io/pypi/pyversions/breathXplorer)]'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_breathxplorer_cq
    doi: 10.1021/jasms.4c00152
    title: BreathXplorer
  dedup_kept_from: coll_breathxplorer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00152
  all_source_dois:
  - 10.1021/jasms.4c00152
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-table-construction-for-multivariate-analysis

## Summary

Construct aligned feature tables from mass-spectrometry breath data by extracting volatile organic compound (VOC) features from individual samples, filtering by quality metrics (RSD), and merging across samples to produce a matrix suitable for multivariate statistical analysis. This skill bridges raw MS data through feature extraction and alignment to a standardized CSV format where rows are samples and columns are m/z features with intensity values.

## When to use

When you have high-resolution mass-spectrometry (HRMS) breath data in mzML or mzXML format from multiple subjects or conditions and need to prepare a sample-by-feature intensity matrix for downstream statistical comparison, biomarker discovery, or classification tasks. Use this skill when raw peak data must be harmonized across samples to account for retention-time drift and instrument variation.

## When NOT to use

- Input is already an aligned feature table or pre-processed CSV—skip directly to statistical analysis.
- Data is from non-breath or non-HRMS instruments (e.g., GC-FID, targeted assays) where peak detection workflows differ.
- Sample sizes are so small (<3 samples) that alignment becomes unreliable or pooling across replicates is impossible.

## Inputs

- mzML or mzXML files (raw HRMS breath data)
- List of file paths (one per sample)
- Sample name identifiers (strings)

## Outputs

- Aligned feature table CSV (rows: m/z features; columns: sample identifiers; values: total intensities)
- FeatureSet objects (intermediate; for quality control inspection)

## How to apply

First, call find_feature() on each mzML/mzXML file with appropriate algorithm choice (Topological or Gaussian) and quality threshold (typically 0.8) to extract a FeatureSet object containing m/z values, scan times, and integrated intensities. Apply RSD (relative standard deviation) filtering—either at a fixed threshold or using a quantile (e.g., 0.1 quantile)—to remove noise features with inconsistent breath-peak intensity patterns. Next, invoke merge_result() on the list of filtered FeatureSets with custom sample names to align features across samples by m/z value and calculate per-sample intensity totals. Finally, export the resulting Sample object to CSV using to_csv(), which produces a table with m/z as the index, sample names as columns, and total intensity per feature per sample as cell values. Optional: annotate adducts and isotopes by passing adduct=True and isotope=True to to_csv().

## Related tools

- **BreathXplorer** (Python package providing find_feature(), merge_result(), and to_csv() functions for feature extraction, alignment, and table export) — https://github.com/wykswr/breathXplorer

## Examples

```
from breathXplorer import find_feature, merge_result
fss = [find_feature(f, False, .8, "Topological", 6) for f in ["sample1.mzML", "sample2.mzML", "sample3.mzML"]]
fss = [fs.rsd_control(fs.rsd.quantile(0.1)) for fs in fss]
sample = merge_result(fss, ["sample1", "sample2", "sample3"])
sample.to_csv("aligned_feature_table.csv")
```

## Evaluation signals

- Output CSV has consistent dimensions: number of rows equals number of unique m/z features, number of columns equals number of input samples plus 2 (ID and m/z columns).
- All intensity values are non-negative and within the expected dynamic range for the instrument (no negative or implausibly large values).
- No m/z duplicates in the output; each feature is represented exactly once (merge_result aligns by m/z and aggregates intensities).
- RSD-filtered FeatureSets have demonstrably lower noise: median RSD of retained features is below the applied threshold (e.g., median RSD < 0.1 if threshold = 0.1 quantile).
- Cross-sample alignment produces expected feature presence/absence patterns; features detected in multiple samples show consistent m/z values (within typical MS tolerance, ~5 ppm for HRMS).

## Limitations

- Peak recognition sensitivity depends on user-selected quality threshold (0.8 default); lower thresholds may introduce noise, higher thresholds may miss weak but real VOCs.
- RSD-based filtering assumes breath peaks have consistent intensity across the breath cycle; metabolically variable or transient features may be incorrectly removed.
- Feature alignment relies on m/z matching without chromatographic retention-time information in the final output; co-eluting isomers with identical m/z cannot be distinguished.
- The Gaussian algorithm requires prior knowledge (number of breaths in experiment) which may not always be available; Topological algorithm is more general but may perform differently on certain breath profiles.
- Supported input formats are limited to mzML and mzXML; other vendor formats (e.g., .raw) require conversion before processing.

## Evidence

- [readme] BreathXplorer is a bioinformatic solution to process breath data generated from HRMS analysis. It contains a suite of functions, including feature extraction, feature alignment, and breath recognition.: "BreathXplorer is a bioinformatic solution to process breath data generated from HRMS analysis. It contains a suite of functions, including feature extraction, feature alignment, and breath"
- [readme] The input file should be in mzML or mzXML format (Perhaps more in the future). For the output, the single or aligned feature table can be exported as csv file.: "The input file should be in mzML or mzXML format (Perhaps more in the future). For the output, the single or aligned feature table can be exported as csv file."
- [readme] The index of the table is the m/z value of the features, and each column is the total intensity of the feature in a sample (experiment of a subject). The name of the column is the sample name.: "The index of the table is the m/z value of the features, and each column is the total intensity of the feature in a sample (experiment of a subject). The name of the column is the sample name."
- [readme] Feature extraction is used to find the volatile organic compound (VOC) in the breath sample. The feature extraction is performed using the `find_feature` function.: "Feature extraction is used to find the volatile organic compound (VOC) in the breath sample. The feature extraction is performed using the `find_feature` function."
- [readme] In practice, the relative standard deviation (RSD) can be used to filter out the noise which doesn't have a consistent intensity with breath peaks.: "In practice, the relative standard deviation (RSD) can be used to filter out the noise which doesn't have a consistent intensity with breath peaks."
- [readme] The `merge_result` function takes as input a list of FeatureSet objects, and returns a Sample object. It aligns the features with the similar m/z value from different samples, and calculate the total intensity of each feature in each sample.: "The `merge_result` function takes as input a list of FeatureSet objects, and returns a Sample object. It aligns the features with the similar m/z value from different samples, and calculate the total"
- [other] BreathXplorer implements feature extraction as a workflow step that processes mass-spectrometry input data and produces a feature table CSV output in a standardized format.: "BreathXplorer implements feature extraction as a workflow step that processes mass-spectrometry input data and produces a feature table CSV output in a standardized format."
