---
name: performance-metric-extraction-from-publications
description: Use when you have identified a claim that one tool outperforms another (e.g., 'IDSL.IPA outperforms MZmine 2 and xcms') in a research article's abstract or introduction, but the specific metrics and results table are not included in the introductory text.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
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

# performance-metric-extraction-from-publications

## Summary

Extract quantitative performance metrics (sensitivity, specificity, precision, recall, runtime, accuracy) from published research comparing bioinformatics tools on a common benchmark dataset. This skill enables reproducible validation of tool claims by locating, tabulating, and source-documenting comparative results.

## When to use

You have identified a claim that one tool outperforms another (e.g., 'IDSL.IPA outperforms MZmine 2 and xcms') in a research article's abstract or introduction, but the specific metrics and results table are not included in the introductory text. You need to retrieve the actual quantitative evidence to reproduce the comparison or validate the claim for a downstream analysis.

## When NOT to use

- The publication does not include a quantitative results section or provides only qualitative statements without numeric values.
- The performance comparison is between different data types or experimental conditions that are not directly comparable (e.g., one tool tested on LC/HRMS, another on GC/MS).
- You have access only to the abstract and introduction, and the repository does not provide a link to the full publication or supplementary materials.

## Inputs

- Publication DOI or full-text PDF containing tool performance comparison
- Research article abstract or introduction claiming tool superiority
- GitHub repository README with citation link

## Outputs

- Structured performance metrics table (CSV or markdown) with columns: tool_name, metric_type, measured_value, unit, source_figure_table
- Source documentation index mapping each metric to publication section/figure/table
- Comparative summary (e.g., sensitivity/specificity/runtime differences between tools)

## How to apply

First, locate the full publication via the repository's citation link or GitHub README (e.g., https://github.com/idslme/IDSL.IPA#citation). Second, navigate to the results section and identify tables or figures presenting side-by-side metric comparisons between the tools. Third, extract the reported metrics (sensitivity, specificity, precision, recall, runtime, accuracy, signal-to-noise ratio, or domain-specific measures like peak picking accuracy for LC/HRMS) along with their measured values for each tool. Fourth, tabulate these metrics in a structured format (CSV or markdown table) with columns for tool name, metric type, measured value, and data type (e.g., percentage, seconds, dimensionless score). Fifth, document the source section, figure number, or table number from the publication for each metric to enable auditing and citation.

## Related tools

- **IDSL.IPA** (Reference tool whose performance metrics are to be extracted from publication; peak picking method for LC/HRMS data) — https://github.com/idslme/IDSL.IPA
- **MZmine 2** (Comparative peak picking tool; performance benchmarked against IDSL.IPA)
- **xcms** (Comparative peak picking tool; performance benchmarked against IDSL.IPA)
- **MS-DIAL** (Comparative peak picking tool; performance benchmarked against IDSL.IPA)

## Examples

```
# Retrieve full publication from GitHub citation; extract metrics from results section
curl -s 'https://github.com/idslme/IDSL.IPA#citation' | grep 'pubs.acs.org' | xargs curl -s > publication.pdf
# Extract and tabulate: tool_name, metric_type, value, unit, source_table
echo 'tool_name,metric_type,value,unit,source_reference\nIDSL.IPA,sensitivity,0.92,fraction,Table 2\nMZmine 2,sensitivity,0.78,fraction,Table 2' > metrics.csv
```

## Evaluation signals

- All extracted metrics have corresponding unit labels (%, seconds, ppm, score range) and are numeric or readily quantifiable.
- Each metric in the output table includes a source reference (section, figure, table number) that can be traced back to the publication.
- At least three performance dimensions are captured (e.g., sensitivity, specificity, and runtime or accuracy) across all tools for fair comparison.
- No metrics are missing or marked 'not reported' for the primary tool (IDSL.IPA) if the publication claims superiority.
- Tool names and metric definitions match the terminology used in the publication results section exactly.

## Limitations

- Publication may claim superiority only in qualitative terms ('outperforms') without providing detailed numeric results in the main text; supplementary materials or linked repositories may be required.
- Performance metrics are dataset- and parameter-specific; benchmarks tested on one LC/HRMS platform or sample type may not generalize to other experimental conditions.
- Runtime and memory metrics depend on hardware (CPU cores, RAM) and software versions; reproducibility requires documentation of the computational environment used in the original study.
- Published comparisons may not include all competing tools or may use outdated versions; the extracted metrics reflect the publication date and may not represent current tool performance.

## Evidence

- [readme] IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, *xcms*, and MS-DIAL in terms of sensitivity, specificity and speed.: "IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, *xcms*, and MS-DIAL in terms of sensitivity, specificity and speed."
- [intro] We have shown in our publication that IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2 and xcms: "We have shown in our publication that IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2 and xcms"
- [other] Extract reported metrics (e.g., sensitivity, specificity, precision, recall, runtime, accuracy) and comparative scores for each tool. Tabulate the extracted metrics in a structured format (CSV or table) with columns for tool name, metric type, and measured value.: "Extract reported metrics (e.g., sensitivity, specificity, precision, recall, runtime, accuracy) and comparative scores for each tool. Tabulate the extracted metrics in a structured format (CSV or"
- [other] Document the source section/figure/table reference from the publication for each metric.: "Document the source section/figure/table reference from the publication for each metric."
- [readme] Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R<sup>13</sup>C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor: "Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R13C, peak width, RPW, number of separation trays, asymmetry factor"
