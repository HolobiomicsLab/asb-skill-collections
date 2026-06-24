---
name: peak-picking-algorithm-comparison
description: Use when you have claims in a paper or tool documentation that one peak
  picking method outperforms others (e.g., 'IDSL.IPA outperforms MZmine 2 and xcms'),
  but the specific comparison metrics, numerical results, and source tables are not
  provided in the abstract or introduction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - IDSL.IPA
  - MZmine 2
  - xcms
  - R
  - MS-DIAL
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.2c00120
  title: IDSL.IPA
evidence_spans:
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory
  for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight
  R package'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00120
  all_source_dois:
  - 10.1021/acs.jproteome.2c00120
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-picking-algorithm-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically benchmark and compare peak picking algorithms (e.g., IDSL.IPA, MZmine 2, xcms, MS-DIAL) on LC/HRMS data using quantitative performance metrics such as sensitivity, specificity, precision, recall, runtime, and accuracy to validate superiority claims and inform tool selection for untargeted metabolomics studies.

## When to use

You have claims in a paper or tool documentation that one peak picking method outperforms others (e.g., 'IDSL.IPA outperforms MZmine 2 and xcms'), but the specific comparison metrics, numerical results, and source tables are not provided in the abstract or introduction. You need to retrieve the full publication, locate the results section, extract the quantitative metrics, and tabulate them to validate or reproduce the benchmark.

## When NOT to use

- The full publication with quantitative results is not accessible or does not exist—avoid guessing or inferring metric values.
- Benchmark data was collected on a different instrument type, ionization mode, or data format (e.g., shotgun proteomics or GC/MS) than your target use case, making direct applicability unclear.
- Peak picking comparison is based only on qualitative statements or visual inspection without numerical metrics for sensitivity, specificity, or runtime—such claims alone are insufficient for reproducible benchmarking.

## Inputs

- Tool documentation or paper abstract claiming peak picking superiority
- GitHub repository URL or citation link to the full publication
- LC/HRMS raw data files (mzXML, mzML, or netCDF format) used in the benchmark study
- Published results section with performance comparison tables or figures

## Outputs

- Structured comparison table (CSV or JSON) with columns: tool name, metric type (sensitivity, specificity, precision, recall, runtime, accuracy, S/N, peak property), measured value, units, and publication reference (figure/table)
- Reproduced or extracted benchmark metrics for IDSL.IPA, MZmine 2, xcms, MS-DIAL, and other tools
- Validated claims of outperformance with numerical evidence

## How to apply

First, identify the full citation or GitHub repository link from the abstract/intro (e.g., github.com/idslme/IDSL.IPA#citation). Locate the peer-reviewed publication via the citation link or repository README. In the results section, search for comparison tables or figures that report performance metrics (sensitivity, specificity, precision, recall, runtime, accuracy, S/N ratios, peak property calculations) for each tool tested on the same LC/HRMS dataset(s). Extract the reported values for each metric and tool, noting the sample size, instrument type (e.g., Thermo Q Exactive HF), and ionization mode (ESI-POS/NEG, HILIC). Tabulate the results in a structured format (CSV or table) with columns for tool name, metric type, measured value, and units, and cross-reference each metric to the publication's figure/table number and section. Use this tabulation to verify that claims of outperformance are supported by statistically meaningful differences in the reported metrics.

## Related tools

- **IDSL.IPA** (Peak picking algorithm under evaluation; extracts peaks for organic small molecules from untargeted LC/HRMS data and calculates 19 chromatographic peak properties) — https://github.com/idslme/IDSL.IPA
- **MZmine 2** (Reference peak picking tool for comparative benchmarking against IDSL.IPA)
- **xcms** (Reference peak picking tool for comparative benchmarking against IDSL.IPA; also used as one of the S/N calculation methods within IDSL.IPA)
- **MS-DIAL** (Reference peak picking tool for comparative benchmarking against IDSL.IPA)
- **R** (Statistical and computational environment for extracting, tabulating, and analyzing benchmark metrics)

## Evaluation signals

- Extracted metrics table contains at least 3 quantitative performance measures (e.g., sensitivity, specificity, precision, recall, runtime) for ≥2 tools tested on the same LC/HRMS dataset.
- Each metric value is accompanied by a publication reference (figure/table number and section) so that results are traceable and reproducible.
- Reported performance differences (e.g., IDSL.IPA sensitivity vs. MZmine 2 sensitivity) are numerically meaningful and not due to rounding or measurement noise.
- All tools were evaluated on the same instrument type (e.g., Thermo Q Exactive HF Orbitrap), ionization mode (ESI-POS or ESI-NEG), and data format (mzXML, mzML, or netCDF) to ensure fair comparison.
- Sample size (number of MS files, number of detected peaks, or number of validated compounds) is documented for each benchmark trial.

## Limitations

- Benchmark studies may use different LC/HRMS instruments, ionization modes, or sample types, limiting direct generalizability across all workflows; results are specific to the published dataset.
- Peak picking performance is highly dependent on parameter tuning (e.g., mass tolerance, retention time window, S/N threshold) for each tool; default parameters may not reflect optimal configuration.
- Publication may report aggregate metrics (e.g., average sensitivity across multiple files) without per-sample or per-peak-class breakdowns, obscuring performance on rare or difficult-to-detect metabolites.
- Runtime comparisons may not account for differences in hardware, parallelization strategy, or preprocessing overhead, limiting reproducibility across environments.
- Specific comparison metrics beyond sensitivity, specificity and speed (e.g., false discovery rate, isotope pairing accuracy, retention time correction drift) may not be consistently reported across all tools in the same publication.

## Evidence

- [readme] IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, *xcms*, and MS-DIAL in terms of sensitivity, specificity and speed.: "IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, *xcms*, and MS-DIAL in terms of sensitivity, specificity and speed."
- [readme] We have shown in our publication that IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, *xcms*: "We have shown in our publication that IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, *xcms*"
- [readme] Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R<sup>13</sup>C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor, skewness using derivative method, symmetry using pseudo-moments, skewness using pseudo-moments, gaussianity, S/N using baseline, S/N using the *xcms* method, S/N using the RMS method, and sharpness.: "Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R13C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor,"
- [readme] extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects: "extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects"
- [readme] Fakouri Baygi, S., Kumar, Y. Barupal, D.K. IDSL. IPA characterizes the organic chemical space in untargeted LC/HRMS datasets. Journal of proteome research, 2022, 21(6), 1485-1494.: "Fakouri Baygi, S., Kumar, Y. Barupal, D.K. IDSL. IPA characterizes the organic chemical space in untargeted LC/HRMS datasets. Journal of proteome research, 2022, 21(6), 1485-1494."
