---
name: peptide-sequence-composition-parsing
description: Use when you have peptide or protein sequences (as FASTA strings or text
  identifiers) and need to compute their mass, isotopic envelope, charge state, isoelectric
  point, or chromatographic retention time for MS matching, peak annotation, or property
  prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0399
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0157
  tools:
  - Python
  - pip
  - conda
  - NumPy
  - matplotlib
  - Pyteomics
  - Unimod (integrated via SQLAlchemy)
  - pandas
  - pip / conda
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- Pyteomics is a collection of lightweight and handy tools for Python
- Pyteomics supports recent versions of Python 3.
- pip install pyteomics
- conda install -c bioconda pyteomics
- numpy
- numpy <https://numpy.org/>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyteomics_cq
    doi: 10.1021/acs.jproteome.8b00717
    title: pyteomics
  dedup_kept_from: coll_pyteomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00717
  all_source_dois:
  - 10.1021/acs.jproteome.8b00717
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peptide-sequence-composition-parsing

## Summary

Parse peptide sequence strings into molecular compositions and calculate physico-chemical properties (mass, isotopic distribution, charge, pI) using Pyteomics. This skill enables rapid conversion of sequence data into quantitative molecular descriptors needed for proteomics analysis.

## When to use

Apply this skill when you have peptide or protein sequences (as FASTA strings or text identifiers) and need to compute their mass, isotopic envelope, charge state, isoelectric point, or chromatographic retention time for MS matching, peak annotation, or property prediction. Trigger conditions include: incoming LC-MS data requiring m/z assignment, FASTA database sequences needing indexed physico-chemical properties, or modified peptide sequences requiring composition-aware calculations.

## When NOT to use

- Input is already a high-resolution mass spectrum or detected peak list (use spectrum interpretation/matching skills instead).
- Sequences contain non-standard amino acids or modifications not supported by the Pyteomics modification dictionary (Unimod).
- You need real-time, online isotopic pattern matching against an instrument stream (batch composition calculation is not suitable for live MS data acquisition).

## Inputs

- peptide sequence strings (unmodified or with modification annotations)
- FASTA format sequences
- list or file of polypeptide identifiers

## Outputs

- isotopic distribution data (m/z, intensity pairs)
- monoisotopic mass
- charge state assignments
- isoelectric point (pI)
- chromatographic retention time predictions
- CSV or JSON export of composition and properties
- matplotlib visualization of isotopic envelope

## How to apply

Install Pyteomics via pip or conda, ensuring NumPy is available as a core dependency. Import the pyteomics.mass module and define peptide sequences as input strings (plain sequences or with modification annotations). Call the isotopic distribution calculation function on each peptide composition to compute relative abundances of isotopic peaks, yielding m/z and intensity pairs. Optionally compute additional properties (mass, charge, pI) using dedicated Pyteomics functions. Format and export results (m/z, intensity pairs, and auxiliary properties) to CSV or JSON; visualize the isotopic envelope using matplotlib for QC. Rationale: Pyteomics abstracts element composition and natural isotope frequencies into a single unified interface, reducing error and enabling reproducible, documented workflows.

## Related tools

- **Pyteomics** (Core library providing mass module for peptide composition parsing, isotopic distribution calculation, and physico-chemical property computation) — https://github.com/levitsky/pyteomics
- **NumPy** (Required numerical computation backend for isotopic distribution array operations)
- **matplotlib** (Optional visualization of computed isotopic envelopes and m/z intensity distributions)
- **Unimod (integrated via SQLAlchemy)** (Provides standardized modification dictionary for parsing modified peptide sequences)
- **pandas** (Optional data frame export and filtering of composition results)
- **pip / conda** (Package managers for installing Pyteomics and dependencies)

## Examples

```
from pyteomics import mass
composition = mass.calculate_mass(sequence='PEPTIDE', average=False)
isotopes = mass.isotopic_composition(sequence='PEPTIDE')
print(composition, isotopes)
```

## Evaluation signals

- Verify output isotopic distribution sums to 1.0 (relative abundances normalized)
- Check that m/z values match expected monoisotopic and isotopic peak positions within instrumental mass accuracy (typically <5 ppm for high-resolution MS)
- Confirm charge-state-dependent m/z calculations are consistent with input charge assumptions
- Validate that isotopic envelope peak heights follow theoretical abundance ratios from natural isotope frequencies
- Ensure CSV/JSON exports contain all peptides with no missing or NaN composition values

## Limitations

- Pyteomics does not account for post-translational modifications beyond those explicitly defined in the input sequence string or Unimod database; custom modifications require manual composition entry.
- Isotopic distribution calculation assumes natural isotope abundances and does not model isotope labeling (e.g., 13C-SILAC, 15N) without additional parameterization.
- No built-in support for retention time prediction without explicit chromatographic calibration data; only generic predictive models are provided.
- Charge calculation and pI estimation rely on simplified pKa models and may deviate significantly from experimental values for highly modified or non-standard sequences.

## Evidence

- [other] Pyteomics provides a mass module that calculates isotopic distribution as part of its suite of basic physico-chemical property calculations for polypeptides.: "Pyteomics provides modules for calculation of basic physico-chemical properties of polypeptides including mass, isotopic distribution, charge and pI, chromatographic retention time"
- [other] The workflow involves defining peptide sequences as input strings and calling isotopic distribution calculation on each peptide composition.: "Import the pyteomics.mass module and define one or more peptide sequences as input strings. Call the isotopic distribution calculation function on each peptide composition to compute relative"
- [other] Results are formatted and exported to CSV or JSON with optional matplotlib visualization.: "Format and export the isotopic distribution results (m/z, intensity pairs) to a CSV or JSON file; optionally visualize the envelope using matplotlib."
- [readme] Pyteomics supports installation via pip and conda with NumPy as a core dependency.: "pip install pyteomics"
- [methods] NumPy is a required core dependency for Pyteomics calculations.: "Pyteomics supports recent versions of Python 3."
