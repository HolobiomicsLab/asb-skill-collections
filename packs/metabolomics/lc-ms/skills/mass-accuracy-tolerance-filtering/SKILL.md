---
name: mass-accuracy-tolerance-filtering
description: Use when when you have a peaklist from IDSL.IPA or similar peak-picking tools (containing observed m/z and intensity values) and need to assign molecular formulas from a prioritized chemical space.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - IDSL.UFA
  - IDSL.IPA
  - R
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.2c00563
  title: IDSL.UFA
evidence_spans:
- '**United Formula Annotation (UFA)** by the [**Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me/) is a light-weight R package'
- annotate peaklists from the IDSL.IPA package with molecular formula
- light-weight R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_ufa_cq
    doi: 10.1021/acs.analchem.2c00563
    title: IDSL.UFA
  dedup_kept_from: coll_idsl_ufa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c00563
  all_source_dois:
  - 10.1021/acs.analchem.2c00563
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-accuracy-tolerance-filtering

## Summary

Filter or rank candidate molecular formulas for MS1 peaks by comparing observed m/z values against theoretical m/z predictions within a specified mass accuracy window. This isotopic profile matching approach validates formula assignments using only high-resolution MS1 data.

## When to use

When you have a peaklist from IDSL.IPA or similar peak-picking tools (containing observed m/z and intensity values) and need to assign molecular formulas from a prioritized chemical space. The skill applies when you want to leverage the isotopic patterns present in MS1 spectra to rank and validate candidate formulas without requiring MS2 fragmentation data.

## When NOT to use

- When MS1 data has poor mass resolution or low signal-to-noise ratio, preventing reliable isotopic pattern observation.
- When only MS2 fragmentation spectra are available and MS1 isotopic patterns are not recorded or cannot be resolved.
- When the chemical space of interest is not represented in your IPDB — the annotation depends on having theoretical isotopic profiles pre-computed for candidate formulas.

## Inputs

- peaklist from IDSL.IPA (m/z, intensity, retention time)
- Isotopic Profile DataBase (IPDB) in .Rdata format
- MS1-level HRMS data (mzXML, mzML, or netCDF format)
- parameter spreadsheet (UFA_parameters.xlsx) specifying mass tolerance and ranking criteria

## Outputs

- annotated peaklist table with assigned molecular formulas
- isotopic profile match scores for each peak-formula assignment
- batch untargeted isotopic profile match figures
- aggregated annotated formulas on aligned peak table

## How to apply

For each detected peak in the peaklist, retrieve the observed m/z and intensity values. Query a pre-calculated Isotopic Profile DataBase (IPDB) containing theoretical isotopic patterns for candidate molecular formulas in your chemical space. Compare the observed MS1 isotopic pattern against predicted patterns by checking if the m/z differences and relative intensities fall within your mass accuracy tolerance (typically specified in IDSL.UFA parameters). Rank candidate formulas by isotopic profile similarity score, with matching criteria evaluating how closely the observed pattern matches the predicted pattern. Assign the top-ranked formula to each peak if similarity exceeds your threshold. This process is applied at scale across all peaks in population-size studies (n > 500 samples) using parallel processing.

## Related tools

- **IDSL.UFA** (Primary R package that implements isotopic profile matching and molecular formula annotation using MS1 data and IPDB databases) — https://github.com/idslme/IDSL.UFA
- **IDSL.IPA** (Prerequisite peak-picking and chromatographic annotation tool that generates peaklists (m/z-RT) as input to IDSL.UFA) — https://github.com/idslme/IDSL.IPA
- **R** (Programming environment in which IDSL.UFA isotopic profile matching is executed)

## Examples

```
library(IDSL.UFA)
UFA_workflow("Address of the UFA parameter spreadsheet")
```

## Evaluation signals

- Verify that assigned molecular formulas have isotopic profile match scores above the configured threshold (check PARAM0007 and related ranking parameters in UFA_parameters.xlsx).
- Compare the number of peaks with assigned formulas before and after filtering — expect a subset of input peaks to receive valid assignments.
- Inspect generated batch untargeted isotopic profile match figures to visually confirm that observed MS1 patterns align with theoretical predictions for top-ranked formulas.
- Validate that aggregated molecular formulas on the aligned peak table show consistent formula assignments across replicates in the study.
- Cross-check that formula assignments respect the elemental composition rules and ionization mode (positive/negative ESI) used in the IPDB.

## Limitations

- Annotation accuracy depends entirely on the completeness and accuracy of the pre-computed IPDB — formulas not in the database cannot be assigned.
- Poor performance on peaks with overlapping or unresolved isotopic patterns due to low mass resolution or high background noise.
- MS1-only annotation cannot distinguish isomeric compounds with identical molecular formulas; additional MS2 data or orthogonal techniques are needed for structural identity.
- Requires prior chromatographic annotation (m/z-RT) from IDSL.IPA or similar peak-picking tool; cannot be applied to raw spectral data directly.

## Evidence

- [other] For each detected peak, perform isotopic profile matching by comparing the observed MS1 isotopic pattern against predicted patterns for candidate molecular formulas in the chemical space.: "For each detected peak, perform isotopic profile matching by comparing the observed MS1 isotopic pattern against predicted patterns for candidate molecular formulas"
- [other] IDSL.UFA is an R package that annotates peaklists from IDSL.IPA with molecular formulas from a prioritized chemical space using an isotopic profile matching approach, requiring only MS1 data.: "annotate peaklists from the IDSL.IPA package with molecular formula of a prioritized chemical space using an isotopic profile matching approach. The IDSL.UFA pipeline only requires MS1"
- [other] Rank candidate formulas by isotopic profile similarity and assign the top-ranked formula to each peak.: "Rank candidate formulas by isotopic profile similarity and assign the top-ranked formula to each peak."
- [readme] Generating comprehensive in-silico theoretical libraries (known as IPDB) using natural isotopic distribution profiles: "Generating comprehensive *in-silico* theoretical libraries (known as [IPDB](https://github.com/idslme/IDSL.UFA/wiki/Isotopic-Profile-DataBase-(IPDB))) using natural isotopic distribution profiles"
- [readme] Aggregating annotated molecular formulas on the aligned peak table. This is a very unique feature that is only presented by IDSL.UFA.: "Aggregating annotated molecular formulas on the aligned peak table. This is a very unique feature that is only presented by IDSL.UFA."
