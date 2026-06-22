---
name: ms-data-format-parsing-and-conversion
description: Use when you have raw breath HRMS data in mzML or mzXML format and need to extract volatile organic compound (VOC) features as a standardized CSV table indexed by m/z value, with columns for scan time or sample identifiers and corresponding intensity measurements.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - BreathXplorer
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-data-format-parsing-and-conversion

## Summary

Parse and convert raw mass-spectrometry data from standard instrument formats (mzML, mzXML) into structured, normalized feature tables (CSV) suitable for downstream bioinformatic analysis. This skill bridges raw HRMS output and feature-centric workflows by handling file I/O, format validation, and schema transformation.

## When to use

You have raw breath HRMS data in mzML or mzXML format and need to extract volatile organic compound (VOC) features as a standardized CSV table indexed by m/z value, with columns for scan time or sample identifiers and corresponding intensity measurements. Apply this skill as the first step before feature alignment or statistical analysis.

## When NOT to use

- Input is already a feature table (CSV or aligned sample matrix) — skip directly to feature alignment or statistical analysis.
- Input file format is not mzML or mzXML — BreathXplorer does not currently support other mass-spectrometry formats.
- Data are from a non-breath or non-HRMS instrument — BreathXplorer is designed specifically for breath mass-spectrometry analysis.

## Inputs

- mzML file (raw HRMS data)
- mzXML file (raw HRMS data)
- file path (string)

## Outputs

- Feature table CSV (rows=m/z features, columns=scan times or samples, values=intensities)
- FeatureSet object (Python; contains mz, scan_time, intensity, rsd attributes)

## How to apply

Load the mzML or mzXML file using BreathXplorer's `find_feature()` function, specifying the file path and algorithm choice ('Topological' or 'Gaussian'). The function returns a FeatureSet object containing extracted m/z values, scan times, and integrated intensities. Optionally apply RSD (relative standard deviation) filtering to remove noise—either at a fixed threshold (e.g., 0.1) or at a quantile (e.g., 10th percentile) to retain only breath peaks with consistent intensity profiles. Export the validated FeatureSet to CSV using `to_csv()`, which produces a table with m/z as row index, total intensity and per-scan-time intensities as columns. Optionally enable adduct and isotope inference during export for enhanced chemical annotation.

## Related tools

- **BreathXplorer** (Python package that implements find_feature() to parse mzML/mzXML and extract FeatureSet objects; also provides to_csv() export and RSD filtering) — https://github.com/wykswr/breathXplorer

## Examples

```
from breathXplorer import find_feature
fs = find_feature("sample.mzML", False, .8, "Topological", 6)
fs = fs.rsd_control(fs.rsd.quantile(0.1))
fs.to_csv("feature_table.csv")
```

## Evaluation signals

- Output CSV file conforms to BreathXplorer feature table schema: row index = m/z values (numeric, ascending), first column = 'intensity' (sum), remaining columns = scan times (numeric) or sample names (string) with non-negative integer values.
- Number of extracted features is non-zero and reasonable for breath VOC analysis (typically hundreds to thousands of m/z peaks).
- RSD values for retained features are either below the specified threshold or at or below the quantile cutoff used for filtering.
- No null or NaN values present in intensity columns (or only where expected for features absent in certain scans/samples).
- Adduct and isotope annotations (if enabled) match known elemental patterns (e.g., [M+H]+, [M+Na]+, isotope mass differences ≈ 1.003 Da for 13C).

## Limitations

- BreathXplorer currently supports only mzML and mzXML formats; other vendor formats (e.g., .raw, .d) require prior conversion.
- Feature extraction quality depends on algorithm choice ('Topological' vs. 'Gaussian') and quality threshold (0–1 range); no guidance provided for algorithm selection in the documentation.
- RSD filtering is heuristic and user-dependent; incorrect thresholds may remove true VOC signals or retain noise.
- Supported Python versions are 3.7–3.10; compatibility with newer Python releases is not guaranteed.
- Peak recognition relies on m/z and retention time clustering; highly overlapping or poorly resolved peaks may be merged or missed.

## Evidence

- [readme] The input file should be in mzML or mzXML format: "The input file should be in mzML or mzXML format (Perhaps more in the future)."
- [readme] Feature extraction produces a FeatureSet object with m/z, scan_time, intensity, and RSD attributes.: "The `fs` is a FeatureSet object, it contains the following information: fs.mz  # m/z values of the extracted features fs.scan_time  # scan time of the experiment fs.intensity  # the total intensity"
- [readme] Feature table CSV has m/z as index and intensity columns indexed by scan time.: "The index of the table is the m/z value of the features, and the 1st column is the total intensity of the feature. The other columns are the intensity of the feature over time, the time is the name"
- [readme] RSD filtering removes noise that doesn't have consistent intensity with breath peaks.: "In practice, the relative standard deviation (RSD) can be used to filter out the noise which doesn't have a consistent intensity with breath peaks"
- [readme] Topological and Gaussian algorithms are available for feature extraction.: "The `"Topological"` indicates the algorithm used for feature extraction, the other option is `"Gaussian"`."
