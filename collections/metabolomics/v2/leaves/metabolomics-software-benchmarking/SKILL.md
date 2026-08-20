---
name: metabolomics-software-benchmarking
description: Use when you have completed peak picking with two or more competing tools
  (e.g., IDSL.IPA, MZmine 2, xcms, MS-DIAL) on the same LC/HRMS dataset(s) and need
  to quantify which performs better. Use this skill when tool selection claims require
  validation (e.g., 'IDSL.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
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

# metabolomics-software-benchmarking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantitatively compare peak-picking tools on untargeted LC/HRMS data by extracting and tabulating performance metrics (sensitivity, specificity, precision, recall, runtime, accuracy) across multiple algorithms. This skill enables practitioners to select the most appropriate tool for their population-scale metabolomics workflow based on empirical evidence rather than anecdotal claims.

## When to use

You have completed peak picking with two or more competing tools (e.g., IDSL.IPA, MZmine 2, xcms, MS-DIAL) on the same LC/HRMS dataset(s) and need to quantify which performs better. Use this skill when tool selection claims require validation (e.g., 'IDSL.IPA outperforms xcms') or when you must justify tool choice to collaborators or for publication.

## When NOT to use

- You are comparing tools on fundamentally different data types (e.g., GC/MS vs. LC/HRMS); benchmark metrics are instrument-specific and not transferable.
- The publication does not provide quantitative metrics—only qualitative statements like 'faster' or 'better quality' without measured values or statistical tests.
- You need to benchmark tools on your own local dataset; this skill assumes a published benchmark; use IDSL.IPA or xcms workflow skills instead if you must run your own comparison.

## Inputs

- Peer-reviewed publication describing multi-tool peak-picking benchmark study
- LC/HRMS raw data files (mzXML, mzML, or netCDF) used in the benchmark
- Peak-picking tool outputs (peaklists in CSV or Rdata format from IDSL.IPA, MZmine 2, xcms, or MS-DIAL)

## Outputs

- Structured benchmark comparison table (CSV or data frame) with columns: Tool Name, Metric Type, Measured Value, Dataset/Instrument, Reference
- Summary statistics and rankings (e.g., sensitivity/specificity scores, runtime in seconds, peak detection accuracy %)
- Annotated comparison narrative documenting which tool excels at which task (e.g., 'IDSL.IPA achieved 95% sensitivity vs. xcms 87% on MS1 peaks')

## How to apply

Locate the peer-reviewed publication describing the benchmark study (typically in Methods or Results section). Extract reported performance metrics for each tool, focusing on sensitivity, specificity, speed (runtime), and any domain-specific measures (e.g., peak detection accuracy on reference standards). Cross-reference metrics with the data source (e.g., which LC/HRMS instrument, sample type, or file format was used). Tabulate metrics in a structured format (CSV or table with columns: Tool Name, Metric Type, Measured Value, Instrument/Dataset, Source Reference). Verify that all tools were evaluated on identical or equivalent input data and under comparable parameter configurations. Document which sections/tables/figures provided each metric to ensure reproducibility and traceability.

## Related tools

- **IDSL.IPA** (Reference peak-picking tool; subject of the benchmark comparison for sensitivity, specificity, and speed on LC/HRMS data) — https://github.com/idslme/IDSL.IPA
- **xcms** (Comparative peak-picking tool; performance metrics extracted and compared against IDSL.IPA)
- **MZmine 2** (Comparative peak-picking tool; performance metrics extracted and compared against IDSL.IPA)
- **MS-DIAL** (Comparative peak-picking tool; performance metrics extracted and compared against IDSL.IPA)
- **R** (Statistical and data wrangling environment for extracting, tabulating, and visualizing benchmark metrics)

## Evaluation signals

- All metrics are sourced from a single publication and section is clearly cited (e.g., 'Table 3, Results' or 'Figure 2, Supplementary Materials').
- Metrics span at least 2 dimensions (e.g., sensitivity AND specificity AND runtime, not just runtime alone).
- Tool comparison is performed on identical input data (same LC/HRMS instrument, sample type, file format).
- Sensitivity and specificity values fall within expected ranges (0–100% or 0–1); runtimes are reported in consistent units (seconds, minutes).
- The benchmark publication reports statistical tests (e.g., p-values, confidence intervals) to support tool ranking; effect sizes are non-trivial (e.g., >5% sensitivity gain).

## Limitations

- Benchmark metrics are instrument and sample-type specific; performance on Thermo Orbitrap data may not transfer to Bruker or Waters instruments.
- Published benchmarks may use outdated parameter settings or software versions; tool performance improves with updates, so metric values become stale.
- No changelog is available for IDSL.IPA, making it difficult to track which algorithmic changes drove performance improvements between versions.
- Benchmarks typically test on small curated reference sets (e.g., n=33 in quick example); real population-scale studies (n>500) may exhibit different tool behavior due to computational overhead or drift in retention time across batches.

## Evidence

- [readme] We have shown in our publication that IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, *xcms*, and MS-DIAL in terms of sensitivity, specificity and speed.: "IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, *xcms*, and MS-DIAL in terms of sensitivity, specificity and speed."
- [readme] Fakouri Baygi, S., Kumar, Y. Barupal, D.K. IDSL. IPA characterizes the organic chemical space in untargeted LC/HRMS datasets. *Journal of proteome research*, **2022**, *21(6)*, 1485-1494.: "IDSL. IPA characterizes the organic chemical space in untargeted LC/HRMS datasets. *Journal of proteome research*, **2022**, *21(6)*, 1485-1494."
- [readme] Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R<sup>13</sup>C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor, skewness using derivative method, symmetry using pseudo-moments, skewness using pseudo-moments, gaussianity, S/N using baseline, S/N using the *xcms* method, S/N using the RMS method, and sharpness.: "Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R<sup>13</sup>C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing"
- [readme] extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects: "extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects"
- [readme] Follow these steps for a quick case study (n = 33) [ST002263] which has Thermo Q Exactive HF hybrid Orbitrap data collected in the HILIC-ESI-POS/NEG modes.: "Follow these steps for a quick case study (n = 33) which has Thermo Q Exactive HF hybrid Orbitrap data collected in the HILIC-ESI-POS/NEG modes."
