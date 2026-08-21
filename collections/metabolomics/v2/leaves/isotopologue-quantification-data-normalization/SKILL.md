---
name: isotopologue-quantification-data-normalization
description: Use when after autoQ has extracted and integrated peak areas for all
  isotopologues of your targeted compounds.
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
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c02998
  title: isoSCAN
evidence_spans:
- install_github("jcapelladesto/isoSCAN") library(isoSCAN)
- install_github("jcapelladesto/isoSCAN")
- To Install from R console
- 'To Install from R console: ```` install.packages("devtools", dependencies=TRUE)
  library(devtools)'
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

# isotopologue-quantification-data-normalization

## Summary

Transform raw isotopologue peak area measurements from autoQ output into percentage-normalized format suitable for downstream visualization and statistical analysis. This normalization step converts absolute integration values into relative abundances, enabling direct comparison across samples and compounds.

## When to use

Apply this skill after autoQ has extracted and integrated peak areas for all isotopologues of your targeted compounds. Use it when you need to prepare quantified isotopologue data for metBarPlot visualization or when absolute area values must be converted to percentage-normalized abundances for comparative analysis across replicates or conditions.

## When NOT to use

- Input is already in percentage or normalized format (applying QTransform twice will corrupt the data)
- You need to retain absolute quantitation or peak area values for external calibration or comparison to reference standards
- Raw peak intensity or signal-to-noise ratio values are required for quality control rather than relative abundance

## Inputs

- integrations data frame from autoQ function output
- peak area measurements for isotopologues

## Outputs

- percentage-normalized isotopologue abundance data frame
- format compatible with metBarPlot visualization

## How to apply

Load the integrations data frame output by autoQ (containing peak area measurements for all detected isotopologues). Apply the QTransform function with parameters val.to.use='area' to select area-based integration values and val.trans='P' to apply quantile normalization, converting raw areas into percentage format. The resulting transformed data frame can be directly passed to metBarPlot for barplot visualization with error bars or used for downstream statistical comparisons. The quantile normalization ensures that all isotopologues for a given compound sum to 100%, enabling meaningful relative abundance comparisons.

## Related tools

- **autoQ** (Extracts and integrates isotopologue peak areas; produces the input integrations data frame for normalization) — github.com/jcapelladesto/isoSCAN
- **QTransform** (Applies quantile normalization and converts area values to percentage format) — github.com/jcapelladesto/isoSCAN
- **metBarPlot** (Visualizes the normalized isotopologue abundances as barplots with standard deviation error bars) — github.com/jcapelladesto/isoSCAN
- **R** (Execution environment for QTransform and data frame operations)

## Examples

```
# Load integrations from autoQ output and apply QTransform normalization
integrations_normalized <- QTransform(integrations, val.to.use='area', val.trans='P')
# Pass normalized data to metBarPlot for visualization
metBarPlot(integrations_normalized)
```

## Evaluation signals

- All isotopologue percentages for each compound sum to 100% (or very close, accounting for floating-point precision)
- Output data frame retains the same row and sample structure as input, with area column replaced by normalized percentage values
- Visualization via metBarPlot displays stacked or grouped bars where individual isotopologue heights represent their relative abundance as percentages
- No negative values or values >100% appear in the normalized output
- Relative ranking and trends between isotopologues are preserved compared to raw area values (higher area → higher percentage)

## Limitations

- Quantile normalization (val.trans='P') assumes that isotopologue abundances are comparable across samples; extreme outliers or saturated peaks can skew percentages
- The method converts to relative abundance only; absolute quantitation information is lost and cannot be recovered from percentage values alone
- If autoQ fails to detect or integrate minor isotopologues (e.g., very low abundance or below SNR threshold), those isotopologues will be absent from the integrations data frame and their percentages will be zero, potentially underestimating true abundance
- Profile format data for low-resolution or centroided data for high-resolution GC-CI-MS is required upstream; incorrect data format will compromise peak integration and subsequent normalization

## Evidence

- [other] QTransform accepts the autoQ integrations data frame with parameters val.to.use='area' and val.trans='P', transforming raw area values into percentage-normalized format: "QTransform accepts the autoQ integrations data frame with parameters val.to.use='area' and val.trans='P', transforming raw area values into percentage-normalized format that can be directly passed to"
- [intro] autoQ function produces integrations data containing peak area measurements for isotopologues: "Now we can call `autoQ` function that will process the files and look for the isotopologues for each compound found in the `formulaTable`."
- [intro] metBarPlot function consumes the normalized data for visualization: "The `metBarPlot` function is designed to plot values in a barplot including standard deviation error bars."
- [intro] The package extracts abundances of isotopologues of targeted compounds: "The package is designed to automatically extract the abundances of isotopologues of a targeted list of compounds."
