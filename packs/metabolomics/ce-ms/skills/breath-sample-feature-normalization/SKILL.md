---
name: breath-sample-feature-normalization
description: Use when after peak recognition has identified significant m/z signals in individual breath samples and you need to aggregate features by sample identifier before aligning features across multiple samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - BreathXplorer
  techniques:
  - CE-MS
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

# breath-sample-feature-normalization

## Summary

Normalize intensity values of detected mass-spectrometry features across breath samples to enable cross-sample comparison and alignment. This step standardizes feature intensities after peak recognition, preparing data for downstream feature alignment and statistical analysis.

## When to use

Apply this skill after peak recognition has identified significant m/z signals in individual breath samples and you need to aggregate features by sample identifier before aligning features across multiple samples. Normalization is essential when comparing volatile organic compound (VOC) intensities across different breath samples or subjects.

## When NOT to use

- Input is already an aligned feature table CSV with per-sample aggregated intensities—use directly for downstream analysis instead.
- Raw mass-spectrometry data has not yet been processed through peak recognition; first apply feature extraction using `find_feature`.
- Analysis requires preservation of temporal or scan-time-resolved intensity profiles; normalization aggregates to total intensity and may lose chromatographic detail.

## Inputs

- FeatureSet object (extracted from individual mzML or mzXML file)
- List of FeatureSet objects (one per sample)
- Sample identifiers/names (customizable labels for each sample)

## Outputs

- Normalized feature table CSV (single sample: rows = features, columns = m/z and intensity over time)
- Aligned feature table CSV (multiple samples: rows = features, columns = sample names with aggregated intensities)
- Filtered FeatureSet object (after RSD quality control)

## How to apply

After extracting features from individual mzML/mzXML files using the `find_feature` function, aggregate detected peaks by sample identifier and normalize their intensity values. BreathXplorer calculates total feature intensity by integrating intensity over scan time, then applies relative standard deviation (RSD) filtering to remove noise—typically using the 10th percentile quantile of RSD or a specific threshold (e.g., 0.1)—to retain only features with consistent intensity across breath peaks. The normalized feature table is then exported as CSV with rows indexed by m/z value, columns representing samples or time points, and cells containing normalized intensity values, enabling consistent input to the feature alignment step.

## Related tools

- **BreathXplorer** (Python package providing `find_feature()` for initial feature extraction, RSD-based filtering with `rsd_control()`, and `merge_result()` for feature alignment and normalization across samples) — https://github.com/wykswr/breathXplorer
- **Python** (Runtime environment for BreathXplorer; supported versions 3.7–3.10)

## Examples

```
from breathXplorer import find_feature, merge_result
fss = [find_feature(f, False, .8, "Topological", 6) for f in ["sample1.mzML", "sample2.mzML"]]
fss = [fs.rsd_control(fs.rsd.quantile(0.1)) for fs in fss]
sample = merge_result(fss, ["sample1", "sample2"])
sample.to_csv("aligned_table.csv")
```

## Evaluation signals

- Output CSV conforms to BreathXplorer feature table schema: index = m/z value, first column = total intensity, subsequent columns = intensity per sample or time point
- All features in filtered FeatureSet pass quality control threshold: RSD ≤ specified quantile (e.g., 0.1 or 10th percentile)
- Total intensity for each feature represents integration over the full scan time range with no missing or NaN values for retained features
- Sample names in aligned feature table exactly match provided identifiers; row count equals number of unique m/z features detected across all samples
- Normalized intensities are numeric, non-negative, and dimensionally consistent (e.g., all in same intensity units from the source MS instrument)

## Limitations

- RSD filtering is data-dependent; choice of quantile threshold (e.g., 0.1 vs. fixed 0.1 value) affects feature retention and may require pilot optimization.
- Relative standard deviation calculation assumes consistent peak shape and signal stability across scan time; highly variable or drifting baselines may inflate RSD and cause feature loss.
- Normalization aggregates intensity over scan time; temporal or chromatographic resolution is lost in the single-value-per-feature output.
- Features present in only a subset of samples will have zero (or missing) intensity in other samples; downstream alignment must handle sparsity.
- Input data must be in mzML or mzXML format; other MS data formats are not supported.

## Evidence

- [other] Aggregate features by sample identifier and normalize intensity values.: "Aggregate features by sample identifier and normalize intensity values."
- [readme] Feature extraction is performed using the `find_feature` function. The function takes the path to an mzMl/mzXML file as input, and returns an object containing the extracted feature table: "Feature extraction is performed using the `find_feature` function. The function takes the path to an mzMl/mzXML file as input, and returns an object containing the extracted feature table"
- [readme] the total intensity of each feature (calculated by integrating the intensity over scan time): "the total intensity of each feature (calculated by integrating the intensity over scan time)"
- [readme] In practice, the relative standard deviation (RSD) can be used to filter out the noise which doesn't have a consistent intensity with breath peaks: "In practice, the relative standard deviation (RSD) can be used to filter out the noise which doesn't have a consistent intensity with breath peaks"
- [readme] FeatureSet object can be exported as csv file using the `to_csv` method: "FeatureSet object can be exported as csv file using the `to_csv` method"
- [readme] The `merge_feature` function takes as input a list of FeatureSet objects, and returns a Sample object. It aligns the features with the similar m/z value from different samples, and calculate the total intensity of each feature in each sample.: "The `merge_feature` function takes as input a list of FeatureSet objects, and returns a Sample object. It aligns the features with the similar m/z value from different samples, and calculate the"
- [readme] The index of the table is the m/z value of the features, and each column is the total intensity of the feature in a sample (experiment of a subject).: "The index of the table is the m/z value of the features, and each column is the total intensity of the feature in a sample (experiment of a subject)."
