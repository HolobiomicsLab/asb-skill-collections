---
name: feature-intensity-thresholding
description: Use when after feature extraction from mzML/mzXML files when you have identified candidate peaks in breath spectrometry data but need to separate true VOC signals from instrument noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - BreathXplorer
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
---

# feature-intensity-thresholding

## Summary

Filter extracted breath spectrometry features by applying signal intensity and prominence thresholds to remove noise and retain only peaks with sufficient signal-to-noise ratio. This quality control step is applied during peak recognition to flag or exclude low-confidence detections in volatile organic compound (VOC) analysis.

## When to use

Apply this skill after feature extraction from mzML/mzXML files when you have identified candidate peaks in breath spectrometry data but need to separate true VOC signals from instrument noise. Use it when your feature set contains peaks with highly variable intensity distributions or when you want to enforce a minimum intensity threshold to ensure downstream analysis uses only high-confidence features.

## When NOT to use

- Input is already a manually curated or pre-filtered feature table with known high confidence.
- Analysis requires exhaustive detection of trace-level VOCs where aggressive thresholding would remove true signals below the noise floor.
- Threshold value is unknown or has not been empirically validated for your instrument and sample matrix.

## Inputs

- Feature extraction output (numerical array or pandas DataFrame)
- Intensity values indexed by m/z or retention time
- Optional: peak prominence or signal-to-noise ratio estimates

## Outputs

- Filtered feature table (CSV or JSON)
- Peak indices with assigned confidence flags or intensity rankings
- Quality-controlled feature set suitable for alignment or statistical analysis

## How to apply

Load the feature extraction output (a numerical array or dataframe containing intensity values across retention time or m/z dimensions). Define intensity and prominence thresholds based on your signal characteristics—the README recommends using relative standard deviation (RSD) quantile filtering as a quality control metric (e.g., `fs.rsd_control(fs.rsd.quantile(0.1))` to filter at the 10th percentile). Apply the threshold to assign confidence scores or peak flags to each detected peak. Retain only features exceeding the threshold and generate a labelled output with peak indices, intensity values, and flags in CSV or JSON format. The choice of threshold should balance sensitivity (retaining true VOCs) against specificity (rejecting noise); higher thresholds are more stringent.

## Related tools

- **BreathXplorer** (Python package providing RSD-based filtering and peak flagging within the peak recognition workflow step) — https://github.com/wykswr/breathXplorer

## Examples

```
from breathXplorer import find_feature
fs = find_feature('sample.mzML', False, .8, 'Topological', 6)
fs = fs.rsd_control(fs.rsd.quantile(0.1))
fs.to_csv('filtered_feature_table.csv')
```

## Evaluation signals

- Filtered feature set has smaller or equal cardinality (fewer or same number of peaks) compared to unfiltered input.
- All retained peaks have intensity or RSD values above the specified threshold; verify no peaks below threshold remain.
- Output CSV/JSON schema matches expected structure: peak indices, m/z values, intensity totals, and confidence flags are all populated.
- Downstream feature alignment step runs without unexpected missing-data artifacts; aligned feature table has non-zero entries for retained peaks across samples.
- RSD distribution of retained features is more homogeneous (lower variance) than the full unfiltered set, indicating noise removal.

## Limitations

- Threshold selection is empirical and data-dependent; no universal threshold suits all breath matrices, instruments, or VOC classes.
- Overly stringent thresholds risk losing true low-abundance VOCs; overly permissive thresholds retain instrument noise and reduce statistical power.
- RSD-based filtering assumes reproducible peak detection across scans; high-variability features may be rejected even if biologically real.
- The README does not provide explicit guidance on threshold validation or sensitivity analysis; users must justify threshold choice post-hoc.

## Evidence

- [other] Assign confidence scores or peak flags to each detected peak based on signal intensity and prominence thresholds.: "Assign confidence scores or peak flags to each detected peak based on signal intensity and prominence thresholds."
- [readme] RSD can filter out noise which doesn't have a consistent intensity with breath peaks.: "the relative standard deviation (RSD) can be used to filter out the noise which doesn't have a consistent intensity with breath peaks"
- [readme] RSD quantile filtering example for quality control.: "fs = fs.rsd_control(fs.rsd.quantile(0.1))  # use the 10% quantile of the RSD"
- [readme] Peak recognition includes peak detection and flagging in the analytical workflow.: "Peak recognition](#peak-recognition)"
