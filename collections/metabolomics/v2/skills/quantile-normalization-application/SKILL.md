---
name: quantile-normalization-application
description: Use when after autoQ has extracted peak area measurements for isotopologues from GC-CI-MS data and you need to prepare these integrations for barplot visualization with metBarPlot.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - isoSCAN
  - R
  - autoQ
  - QTransform
  - metBarPlot
derived_from:
- doi: 10.1021/acs.analchem.0c02998
  title: isoSCAN
evidence_spans:
- install_github("jcapelladesto/isoSCAN") library(isoSCAN)
- install_github("jcapelladesto/isoSCAN")
- To Install from R console
- 'To Install from R console: ```` install.packages("devtools", dependencies=TRUE) library(devtools)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isoscan_cq
    doi: 10.1021/acs.analchem.0c02998
    title: isoSCAN
  dedup_kept_from: coll_isoscan_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c02998
  all_source_dois:
  - 10.1021/acs.analchem.0c02998
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# quantile-normalization-application

## Summary

Apply quantile normalization to isotopologue area values from autoQ output to convert raw peak integrations into percentage-normalized format suitable for downstream visualization. This transformation enables direct comparison of isotopologue abundances across samples by removing scale differences while preserving relative distribution patterns.

## When to use

After autoQ has extracted peak area measurements for isotopologues from GC-CI-MS data and you need to prepare these integrations for barplot visualization with metBarPlot. Specifically, when raw area values must be converted to percentage-normalized format to enable visual comparison of isotopologue distributions across multiple samples or conditions.

## When NOT to use

- Input is not in autoQ integrations format (missing isotopologue area columns)
- Data has already been normalized or converted to percentages by another method
- You need to preserve absolute area values for downstream quantitative analysis requiring unconverted measurements

## Inputs

- integrations data frame from autoQ output containing peak area measurements for isotopologues

## Outputs

- percentage-normalized data frame suitable for metBarPlot visualization

## How to apply

Load the integrations data frame output from autoQ containing raw area measurements for each isotopologue. Call the QTransform function with parameters val.to.use='area' to select area-based integration values and val.trans='P' to apply quantile (percentage) normalization. This transforms each isotopologue's area into its percentage contribution relative to the total isotopologue pool for that compound-sample pair. The resulting normalized data frame can be directly passed to metBarPlot for barplot visualization with standard deviation error bars. Quantile normalization ensures that the sum of all isotopologue percentages for each compound equals 100%, enabling fair visual comparison regardless of absolute peak intensity differences between samples.

## Related tools

- **autoQ** (Extracts peak area measurements for isotopologues from processed GC-CI-MS files; produces the integrations data frame that serves as input to QTransform) — github.com/jcapelladesto/isoSCAN
- **QTransform** (Applies quantile normalization to convert raw area values to percentage-normalized format using val.to.use and val.trans parameters) — github.com/jcapelladesto/isoSCAN
- **metBarPlot** (Accepts normalized data frame output from QTransform to generate barplot visualization with standard deviation error bars) — github.com/jcapelladesto/isoSCAN
- **R** (Programming environment in which QTransform function is executed)

## Examples

```
transformed_df <- QTransform(integrations, val.to.use='area', val.trans='P'); metBarPlot(transformed_df)
```

## Evaluation signals

- Output data frame has same number of rows and isotopologue columns as input, with only values transformed
- For each compound-sample pair, sum of all isotopologue percentages equals or is very close to 100%
- Relative ranking of isotopologue abundances within each sample is preserved compared to input (no reordering)
- All percentage values fall within valid range [0, 100]
- When passed to metBarPlot, barplots display proportional isotopologue distributions without negative or out-of-range values

## Limitations

- QTransform assumes all isotopologue peaks in the autoQ output represent the same targeted compound; mixing data from different compounds will produce meaningless percentages
- Requires clean autoQ integrations data; spurious or missing peaks will skew percentage calculations
- Percentage normalization eliminates information about absolute abundance differences; if absolute quantification is needed, original area values must be retained separately
- Sensitive to presence of contaminant or background isotope signals included in autoQ output; filtering prior to QTransform may be necessary

## Evidence

- [other] QTransform accepts the autoQ integrations data frame with parameters val.to.use='area' and val.trans='P', transforming raw area values into percentage-normalized format: "QTransform accepts the autoQ integrations data frame with parameters val.to.use='area' and val.trans='P', transforming raw area values into percentage-normalized format that can be directly passed to"
- [intro] autoQ function processes files and extracts isotopologue abundances as area measurements: "Now we can call `autoQ` function that will process the files and look for the isotopologues for each compound found in the `formulaTable`."
- [intro] metBarPlot uses transformed values to create barplot visualization: "The `metBarPlot` function is designed to plot values in a barplot including standard deviation error bars."
- [intro] Package is designed to extract abundances of isotopologues of targeted compounds: "The package is designed to automatically extract the abundances of isotopologues of a targeted list of compounds."
