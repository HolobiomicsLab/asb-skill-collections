---
name: lc-hrms-data-processing-evaluation
description: Use when you have processed the same set of untargeted LC/HRMS files (mzXML, mzML, or netCDF format) with two or more peak-picking tools and need to validate which tool produces higher-quality peaklists for organic small molecules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - IDSL.IPA
  - MZmine 2
  - xcms
  - R
  - MS-DIAL
derived_from:
- doi: 10.1021/acs.jproteome.2c00120
  title: IDSL.IPA
evidence_spans:
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight R package'
- IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2
- IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, *xcms
- similar peak picking tools such as MZmine 2, *xcms
- light-weight R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_ipa_cq
    doi: 10.1021/acs.jproteome.2c00120
    title: IDSL.IPA
  dedup_kept_from: coll_idsl_ipa_cq
schema_version: 0.2.0
---

# lc-hrms-data-processing-evaluation

## Summary

Evaluate and benchmark peak-picking performance for untargeted LC/HRMS data by comparing tool outputs on sensitivity, specificity, and runtime metrics. This skill applies structured comparison workflows to assess whether a peak-extraction tool (e.g., IDSL.IPA, MZmine 2, xcms) meets quality thresholds for population-scale metabolomics studies.

## When to use

You have processed the same set of untargeted LC/HRMS files (mzXML, mzML, or netCDF format) with two or more peak-picking tools and need to validate which tool produces higher-quality peaklists for organic small molecules. Typical triggers: planning a new analysis pipeline, validating a tool upgrade, or reproducing published benchmark results comparing peak detection methods.

## When NOT to use

- Input peaklists are from the same tool with different parameter sets—use parameter optimization skill instead.
- You lack a gold-standard or reference peak list and cannot assess true positives/false positives—consider sensitivity analysis or literature comparison instead.
- The LC/HRMS data are from fundamentally different ionization modes or instrument types across tools—results may not be directly comparable without mode/instrument harmonization.

## Inputs

- LC/HRMS raw data files (mzXML, mzML, netCDF)
- Peaklist outputs from ≥2 peak-picking tools (.csv, .Rdata, or .tsv format)
- Tool-specific parameter configurations or method descriptions
- Gold-standard or reference peak list (optional but recommended)

## Outputs

- Structured comparison table with columns: tool name, metric type, measured value, source reference
- Performance metrics (sensitivity, specificity, precision, recall, runtime, peak properties)
- Visualization or summary report of tool ranking by metric
- Documentation of benchmark conditions (instrument, ionization mode, dataset size, parameter values)

## How to apply

Obtain peaklist outputs (in .Rdata or .csv format) from each tool being compared on identical input HRMS data. Extract and tabulate quantitative metrics reported in each tool's publication or derived from outputs: sensitivity (true positives / (true positives + false negatives)), specificity (true negatives / (true negatives + false positives)), precision, recall, runtime, and peak property statistics (e.g., peak area, S/N ratio, peak width, asymmetry factor). Normalize metrics to a common scale and document the source section/figure/table and input dataset characteristics (instrument type, ionization mode, sample count). Compare performance across tools using the same gold-standard reference peaks or benchmark dataset. Document any parameter tuning per tool (e.g., IDSL.IPA's retention time tolerance, MZmine 2's noise threshold) to ensure fair comparison.

## Related tools

- **IDSL.IPA** (Primary peak-picking tool for LC/HRMS; generates peaklists with 19 chromatographic peak properties; outputs in .Rdata and .csv formats) — https://github.com/idslme/IDSL.IPA
- **MZmine 2** (Comparative peak-picking tool for benchmarking; reference implementation for sensitivity/specificity comparison)
- **xcms** (Comparative peak-picking tool for benchmarking; provides alternative S/N ratio calculation method)
- **MS-DIAL** (Comparative peak-picking tool mentioned in IDSL.IPA publication for performance evaluation)
- **R** (Statistical and visualization environment for tabulating, normalizing, and comparing metric outputs across tools)

## Examples

```
library(IDSL.IPA); IPA_workflow("Address of the IPA parameter spreadsheet"); # Compare output peaklists (*.csv) from IDSL.IPA, MZmine 2, xcms on identical input mzXML files and tabulate sensitivity, specificity, runtime metrics.
```

## Evaluation signals

- Sensitivity, specificity, precision, and recall values are computed from identical reference peak sets across all tools; values should sum logically (TP + FN + FP + TN = total peaks evaluated).
- Runtime measurements are recorded under identical computational conditions (thread count, hardware); runtime ratios between tools are consistent with published values.
- Peak property distributions (area, S/N, width, asymmetry) from each tool's output are compared statistically (e.g., median, quartiles, or rank correlation) to detect systematic differences.
- Documentation includes tool parameter values used (e.g., IDSL.IPA retention time tolerance in PARAM0007, MZmine 2 noise threshold); results are reproducible if parameters are identical.
- Benchmark dataset characteristics are reported (instrument type, ionization mode [POS/NEG], number of samples, LC method); comparison is restricted to studies with matching characteristics.

## Limitations

- The IDSL.IPA publication demonstrates outperformance over MZmine 2 and xcms, but specific comparison metrics and results tables are not included in the abstract/intro text—full publication access is required to extract quantitative benchmarks.
- Peak-picking evaluation depends on availability of a validated reference peak list or gold-standard; performance metrics cannot be reliably computed without ground truth.
- Tool parameter sensitivity may dominate benchmark results—default parameters in one tool may not be optimal; fair comparison requires either tool-specific tuning or explicit disclosure of parameter mismatch.
- Comparison is most reliable within the same ionization mode (POS or NEG) and LC method; cross-mode or cross-instrument generalization is not guaranteed.
- Runtime comparisons require identical computational hardware and thread configuration; reported speedup over xcms and MZmine 2 is conditional on these factors.

## Evidence

- [readme] We have shown in our publication that IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, xcms, and MS-DIAL in terms of sensitivity, specificity and speed.: "We have shown in our publication that IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, xcms, and MS-DIAL in terms of sensitivity, specificity and speed."
- [readme] IDSL.IPA generates comprehensive and high-quality datasets from untargeted analysis of organic small molecules for population-size studies: "IDSL.IPA generates comprehensive and high-quality datasets from untargeted analysis of organic small molecules for population-size studies"
- [readme] Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R<13>C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor...: "Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R<sup>13</sup>C, peak width, RPW, number of separation trays, asymmetry factor"
- [intro] extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects: "extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects"
- [readme] Individual peaklists for each HRMS file in *.Rdata* and *.csv* formats in the 'peaklists' directory.: "Individual peaklists for each HRMS file in *.Rdata* and *.csv* formats in the 'peaklists' directory."
