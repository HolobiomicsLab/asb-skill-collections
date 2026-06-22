---
name: effective-mobility-calibration-single-marker
description: Use when when you have CE-MS data with migration times that vary between runs due to electroosmotic flow drift, but you possess a reliable internal standard with a known effective mobility value.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MobilityTransformR
  - R
  - MSnbase
  - MetaboCoreUtils
  - xcms
  - Spectra
  techniques:
  - CE-MS
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- Description and usage of MobilityTransformR
- compute Procaine's effective mobility using mobilityTransform
- there is no implementation in R that performs effective mobility transformation of CE-MS(/MS) data
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MSnbase")`
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MetaboCoreUtils")`
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("xcms")`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilitytransformr_cq
    doi: 10.1093/bioinformatics/btac441
    title: MobilityTransformR
  dedup_kept_from: coll_mobilitytransformr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac441
  all_source_dois:
  - 10.1093/bioinformatics/btac441
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# effective-mobility-calibration-single-marker

## Summary

Transform capillary electrophoresis–mass spectrometry (CE-MS) migration times to effective mobility values using a single calibration marker with known mobility (typically an EOF marker like Paracetamol with mobility = 0). This produces a reproducible, system-independent mobility scale that corrects for electroosmotic flow fluctuations.

## When to use

When you have CE-MS data with migration times that vary between runs due to electroosmotic flow drift, but you possess a reliable internal standard with a known effective mobility value. Use this skill when you want to establish a single unified mobility scale for a single electrophoretic system without access to a second calibration marker, or when EOF is your primary reference point.

## When NOT to use

- Input data are already in effective mobility scale or have been pre-transformed by another method
- You have access to two or more calibration markers covering a wide mobility range — use two-marker calibration for improved accuracy
- Migration times are missing or the reference marker's rtime is not precisely known or reproducible

## Inputs

- Migration time (rtime) of reference marker (numeric, in minutes)
- Reference marker mobility value (numeric, typically 0 for EOF marker)
- Electrical field ramp time tR (numeric, in minutes)
- Applied voltage U (numeric, in kV, with sign indicating polarity)
- Capillary length L (numeric, in mm)
- Migration times of analyte compounds (numeric vector or data frame column, in minutes)

## Outputs

- Effective mobility values for analytes (numeric vector or data frame column, units: cm²/(V·s) or equivalent)
- Data frame or structured object mapping input migration times to transformed effective mobilities

## How to apply

Load the marker data frame containing the reference compound's migration time (rtime), assigned mobility value (typically 0 for EOF markers like Paracetamol), and experimental parameters: electrical field ramp time (tR = 3/60 min), applied voltage (U = +30 kV), and capillary length (L = 800 mm). Invoke the mobilityTransform function from MobilityTransformR with these calibration parameters and the migration times of your analytes. The function applies equation 1 (single-marker method) to compute effective mobility for each compound relative to the reference marker's mobility scale. The resulting effective mobility values remain stable across runs in the same electrophoretic system, enabling reproducible peak alignment and compound identification.

## Related tools

- **MobilityTransformR** (Implements the mobilityTransform function that performs single-marker effective mobility transformation using equation 1 and specified experimental parameters) — https://github.com/LiesaSalzer/MobilityTransformR
- **R** (Runtime environment in which MobilityTransformR functions are executed)
- **MetaboCoreUtils** (Provides supporting functionality for metabolomics data transformation)
- **MSnbase** (Used to load and represent CE-MS data objects for transformation)

## Examples

```
mobilityTransform(mzml_data, markers_df, tR = 3/60, U = 30, L = 800)
```

## Evaluation signals

- Effective mobility values are stable (invariant) across replicate injections in the same electrophoretic system, whereas the input migration times show variation
- Transformed mobility values cluster reproducibly by compound identity; peaks align across runs on the mobility scale
- Output data frame contains valid numeric effective mobility values with no missing or infinite entries for successfully transformed analytes
- The reference marker's transformed effective mobility equals its assigned input value (e.g., 0 for EOF marker), confirming calibration correctness
- Effective mobility values fall within physically plausible ranges (typically −5 to +5 cm²/(V·s) for small organic molecules in CE-MS)

## Limitations

- Single-marker calibration assumes a linear relationship between migration time and effective mobility; non-linear drift or system instability may reduce accuracy compared to two-marker calibration
- Effective mobility transformation for CE-MS is more complex than for CE-UV and depends on accurate knowledge of experimental parameters (tR, U, L)
- Accuracy relies on the stability and precision of the reference marker's migration time measurement; errors propagate to all derived mobility values

## Evidence

- [intro] Effective mobility remains stable and single-marker method rationale: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] Reproducibility benefit of effective mobility scale: "will result in highly reproducible peaks, which has already been shown in 2001"
- [intro] No prior R implementation and CE-MS specific complexity: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility"
- [other] mobilityTransform function with single-marker workflow: "The mobilityTransform function computes Procaine's effective mobility using equation 1 (single marker method) with the Paracetamol EOF marker as reference, requiring inputs of migration time, marker"
- [other] Single-marker parameter specifications and workflow: "Invoke MobilityTransformR's mobilityTransform function with the calibration parameters: tR (reference time) = 3/60 minutes, U (applied voltage) = +30 kV, and L (capillary length) = 800 cm. 3. Apply"
