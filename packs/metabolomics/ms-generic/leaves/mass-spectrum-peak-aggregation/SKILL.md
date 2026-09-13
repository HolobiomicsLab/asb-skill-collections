---
name: mass-spectrum-peak-aggregation
description: Use when you have a processed mass spectrum object with assigned molecular
  formulas for individual peaks and need to summarize peaks by their heteroatom composition—e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - CoreMS
  - pandas
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development
  and data analysis of small molecules analysis.'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-peak-aggregation

## Summary

Organize formula-assigned mass spectrum peaks into heteroatom classes (CHO, CHON, CHOS, CHOP, etc.) and aggregate their counts and abundances for classification-based analysis and visualization. This skill transforms a peak-resolved mass spectrum into a summary table stratified by elemental composition.

## When to use

Apply this skill when you have a processed mass spectrum object with assigned molecular formulas for individual peaks and need to summarize peaks by their heteroatom composition—e.g., to characterize the elemental diversity of natural organic matter (NOM) or to group peaks for downstream classification, statistical comparison, or visualization by chemical class.

## When NOT to use

- Input mass spectrum has no assigned molecular formulas—formula assignment must precede aggregation.
- Input is a raw or centroid mass spectrum without peak-level formula assignments.
- Analysis goal is to retain individual peak-level resolution rather than summarize by class (e.g., fine structure studies or single-peak tracking).

## Inputs

- formula-assigned mass spectrum object (CoreMS MassSpectrum or CoreMS.MassSpectra with assigned molecular formulas)
- molecular formula selection parameter (string or enum specifying which formula candidate to use per peak)

## Outputs

- pandas DataFrame with columns: heteroatom_class, peak_count, total_abundance, percent_abundance
- heteroatom class assignments for each peak (e.g., CHO, CHON, CHOS, CHOP)

## How to apply

Instantiate the HeteroatomsClassification factory from CoreMS, passing the formula-assigned mass spectrum object and a molecular formula selection parameter. The factory iterates over all detected peaks, extracts the heteroatom class assignment from each peak's formula (e.g., 'CHO' for peaks containing only C, H, O), and aggregates peak counts and total abundance (m/z-weighted intensity) by class. Group results into a pandas DataFrame with columns: heteroatom_class, peak_count, total_abundance, and percent_abundance. Validate that all peaks are classified into exactly one heteroatom class with no unassigned peaks remaining.

## Related tools

- **CoreMS** (Framework providing HeteroatomsClassification factory, mass spectrum data structures, and peak metadata access) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Data frame construction and aggregation for heteroatom class summary table)

## Examples

```
from corems.mass_spectrum import MassSpectrum; hc = MassSpectrum.HeteroatomsClassification(mass_spectrum_object); summary_df = hc.get_class_summary()
```

## Evaluation signals

- All detected peaks in the input spectrum are classified into exactly one heteroatom class with no unassigned peaks.
- Sum of peak_count across all heteroatom classes equals the total number of peaks in the input spectrum.
- Sum of percent_abundance across all heteroatom classes equals 100% (or close, within floating-point tolerance).
- Each heteroatom class string conforms to elemental symbol order (e.g., CHO, CHON, CHOS, CHOP) with no duplicates or malformed entries.
- Heteroatom class assignments are reproducible when applied to the same input spectrum with the same formula selection parameter.

## Limitations

- Requires that molecular formula assignment has already been performed on all peaks; unassigned or ambiguous peaks may fail or be excluded.
- Heteroatom classes are defined by the discrete elemental combinations present in assigned formulas; does not interpolate or predict missing classes.
- Abundance aggregation assumes peaks are independent; may obscure isotopic structure or overlapping species if not pre-resolved.
- Classification outcome depends on the molecular formula selection strategy (e.g., most abundant candidate, lowest m/z error); different selection rules may yield different class distributions.

## Evidence

- [other] HeteroatomsClassification factory transforms a formula-assigned mass spectrum into a heteroatom class summary: "HeteroatomsClassification factory transform a formula-assigned mass spectrum into a heteroatom class summary?"
- [other] Instantiate HeteroatomsClassification with mass spectrum object and extract heteroatom class assignments: "Instantiate the HeteroatomsClassification factory from CoreMS with the mass spectrum object as input. 3. Extract heteroatom class assignments (e.g., CHO, CHON, CHOS, CHOP) for each detected peak."
- [other] Aggregate peak counts and total abundance by heteroatom class into a summary DataFrame: "Aggregate peak counts and total abundance by heteroatom class. 5. Generate a summary table (pandas DataFrame) with columns: heteroatom_class, peak_count, total_abundance, percent_abundance."
- [other] Validation requires all detected peaks classified into exactly one heteroatom class with no unassigned peaks: "Validation: confirm all detected peaks are classified into exactly one heteroatom class with no unassigned peaks."
- [readme] Heteroatom classification and visualization listed as available feature in CoreMS: "Heteroatoms classification and visualization"
