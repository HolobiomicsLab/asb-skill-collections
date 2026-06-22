---
name: molecular-formula-heteroatom-classification
description: Use when after molecular formula assignment has been completed on detected peaks in a processed mass spectrum object.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - CoreMS
  - pandas
  - EnviroMS
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.'
- import pandas as pd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-formula-heteroatom-classification

## Summary

Organizes formula-assigned peaks from a mass spectrum into heteroatom class groups (CHO, CHON, CHOS, CHOP, etc.) for compositional analysis and visualization. This skill enables rapid summary and filtering of complex mass spectrometry datasets by elemental composition.

## When to use

Apply this skill after molecular formula assignment has been completed on detected peaks in a processed mass spectrum object. Use it when you need to aggregate and summarize peaks by their heteroatom class composition, particularly for natural organic matter or environmental samples where compositional heterogeneity is a key analytical dimension.

## When NOT to use

- Input mass spectrum contains no formula assignments — classification requires valid molecular formulas on each peak.
- Peaks lack required metadata fields (e.g., abundance values) — summary statistics cannot be computed without complete peak annotations.
- Analysis goal is to filter or rank peaks by spectral properties (e.g., resolving power, mass error) — use mass calibration or peak quality filters instead.

## Inputs

- processed mass spectrum object (CoreMS MassSpectrum with formula-assigned peaks)
- molecular formula assignment parameter (e.g., selected formula field per peak)

## Outputs

- pandas DataFrame with heteroatom class summary (columns: heteroatom_class, peak_count, total_abundance, percent_abundance)
- heteroatom class assignments for each detected peak
- aggregated abundance and peak count by heteroatom class

## How to apply

Load a processed mass spectrum object containing peaks with assigned molecular formulas (e.g., from CoreMS deserialization or post-assignment state). Instantiate the HeteroatomsClassification factory from CoreMS, passing the mass spectrum object as input. The factory automatically extracts and organizes assigned peaks into heteroatom classes by parsing the elemental composition of each formula. Aggregate peak counts and total abundance (or percent abundance) for each class. Generate a pandas DataFrame summary with columns: heteroatom_class, peak_count, total_abundance, percent_abundance. Validate that all detected peaks are classified into exactly one heteroatom class with no unassigned or duplicate peak entries.

## Related tools

- **CoreMS** (Provides HeteroatomsClassification factory, MassSpectrum object model, and formula assignment infrastructure) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Constructs and manipulates summary DataFrame output with heteroatom class aggregations)
- **EnviroMS** (Higher-level workflow that may consume heteroatom classification output for natural organic matter annotation) — https://github.com/EMSL-Computing/EnviroMS

## Examples

```
from corems.mass_spectra.factory import MassSpectraFactory
ms = MassSpectraFactory.from_bruker_solarix('sample.d')
from corems.mass_spectra.factory import HeteroatomsClassification
heteroatom_summary = HeteroatomsClassification(ms).classification_results_dataframe
```

## Evaluation signals

- All detected peaks appear in exactly one heteroatom class row — no unassigned or duplicate peak entries.
- Sum of peak_count across all classes equals total number of formula-assigned peaks in the input spectrum.
- Sum of percent_abundance across all classes equals 100% (or close, accounting for rounding).
- Heteroatom classes follow valid elemental composition patterns (e.g., CHO, CHON, CHOS, CHOP, CHN); invalid or malformed classes indicate assignment failure.
- Peaks with identical molecular formulas are grouped into the same heteroatom class with consistent abundance reporting.

## Limitations

- Requires prior successful molecular formula assignment on all peaks; unassigned peaks cannot be classified.
- Classification is deterministic once formulas are assigned — no handling for ambiguous or multiple formula candidates per peak (caller must resolve beforehand).
- Does not account for isotopic variants (e.g., 13C) — isotope peaks are classified separately by their assigned formula.
- Heteroatom classes are defined by elemental composition only; no spatial, temporal, or structural discrimination (e.g., isomers with identical formula are grouped together).

## Evidence

- [other] HeteroatomsClassification accepts a formula-assigned mass spectrum object and a molecular formula selection parameter, then organizes the assigned peaks into heteroatom classes (such as CHO, CHON): "HeteroatomsClassification accepts a formula-assigned mass spectrum object and a molecular formula selection parameter, then organizes the assigned peaks into heteroatom classes (such as CHO, CHON)"
- [other] Load a processed mass spectrum object (from CoreMS import or deserialization) containing peaks with assigned molecular formulas. Instantiate the HeteroatomsClassification factory from CoreMS with the mass spectrum object as input. Extract heteroatom class assignments (e.g., CHO, CHON, CHOS, CHOP) for each detected peak. Aggregate peak counts and total abundance by heteroatom class.: "Load a processed mass spectrum object (from CoreMS import or deserialization) containing peaks with assigned molecular formulas. Instantiate the HeteroatomsClassification factory from CoreMS with the"
- [other] Generate a summary table (pandas DataFrame) with columns: heteroatom_class, peak_count, total_abundance, percent_abundance. Validation: confirm all detected peaks are classified into exactly one heteroatom class with no unassigned peaks.: "Generate a summary table (pandas DataFrame) with columns: heteroatom_class, peak_count, total_abundance, percent_abundance. Validation: confirm all detected peaks are classified into exactly one"
- [readme] Heteroatoms classification and visualization: "Heteroatoms classification and visualization"
- [readme] CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.: "CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis."
