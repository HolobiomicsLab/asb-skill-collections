---
name: physicochemical-property-computation
description: Use when you have one or more peptide or protein sequences in string
  format and need to calculate their mass, isotopic envelope (m/z and intensity pairs),
  charge state behavior, isoelectric point, or predicted chromatographic retention.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0400
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0601
  tools:
  - Python
  - pip
  - conda
  - NumPy
  - matplotlib
  - Pyteomics
  - pandas
  - SQLAlchemy
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
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

# physicochemical-property-computation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute fundamental physico-chemical properties of polypeptides—including mass, isotopic distribution, charge, pI, and chromatographic retention time—using the Pyteomics mass module. This skill enables rapid characterization of peptide and protein sequences as a foundation for downstream proteomics data analysis.

## When to use

Apply this skill when you have one or more peptide or protein sequences in string format and need to calculate their mass, isotopic envelope (m/z and intensity pairs), charge state behavior, isoelectric point, or predicted chromatographic retention. Common triggers include validation of experimental MS peaks against theoretical isotopic patterns, quality control of synthetic peptides, or feature engineering for machine learning on proteomics datasets.

## When NOT to use

- Input is already a pre-computed feature table or mass spectrum — use this skill to generate features, not to process them.
- You need real-time deconvolution of experimental MS data — Pyteomics computes theoretical properties; use dedicated deconvolution tools (e.g., Decon2LS) for observed spectra.
- Sequences contain non-standard amino acids or modifications not supported by Pyteomics' composition database — verify modification coverage in Unimod first.

## Inputs

- peptide sequence strings (e.g., 'PEPTIDE', 'MKVLWAALLVTFLAGCAKAKSIS')
- optional: modified peptide sequences with position-specific modifications

## Outputs

- isotopic distribution (m/z, intensity pairs)
- mass value (monoisotopic and average)
- charge state predictions
- isoelectric point (pI)
- chromatographic retention time (predicted)
- formatted output (CSV, JSON, or matplotlib figure)

## How to apply

Install Pyteomics via pip or conda, ensuring NumPy is available as a core dependency. Import the pyteomics.mass module and define peptide sequences as input strings. Call the isotopic distribution calculation function on each peptide composition to compute relative abundances of isotopic peaks across the m/z range. The function returns pairs of (m/z, intensity) values representing the theoretical isotopic envelope. Format and export results to CSV or JSON; optionally visualize the envelope using matplotlib to inspect peak spacing, abundance ratios, and overall pattern fidelity against observed mass spectra.

## Related tools

- **Pyteomics** (Primary library for isotopic distribution and physico-chemical property calculation via the mass module) — https://github.com/levitsky/pyteomics
- **NumPy** (Core numerical computation dependency for isotopic abundance calculations)
- **matplotlib** (Visualization of isotopic distribution envelopes and m/z intensity patterns)
- **pandas** (Optional: tabular export and manipulation of isotopic distribution results)
- **SQLAlchemy** (Optional: backend for Unimod database access and modification lookup)

## Examples

```
from pyteomics.mass import isotopic_composition; peptide = 'PEPTIDE'; iso_dist = isotopic_composition(peptide); print(iso_dist)
```

## Evaluation signals

- Isotopic peak spacing matches theoretical m/z differences for the element composition (e.g., ~1.0 Da between ¹²C and ¹³C isotopes).
- Intensity ratios of isotopic peaks align with predicted natural abundances (e.g., M+1 peak ~1% of M for typical peptides).
- Exported m/z and intensity values can be imported and compared against experimental MS spectra with known resolution; cosine similarity or spectral matching score > 0.8 indicates good fit.
- Calculated mass agrees with independent tools (e.g., online ProteomicsTools calculators) to ±0.01 Da.
- pI and retention time predictions lie within expected ranges for the peptide length and composition (pI typically 3–11; retention varies by HPLC column and solvent).

## Limitations

- Isotopic distribution calculation assumes natural isotope abundances and does not account for metabolic labeling (e.g., ¹⁵N, ¹³C) — use labeled composition data if available.
- Modification support depends on Unimod database coverage; non-standard or newly discovered post-translational modifications may not be recognized.
- Chromatographic retention time prediction is empirical and method-specific; predictions are most accurate when trained on the same column, solvent system, and peptide characteristics as the article's calibration set.
- The module does not model charge-state-dependent fragmentation patterns or ion mobility; use complementary tools for those predictions.
- Large-scale batch processing of many sequences may require memory management for NumPy arrays if working with very large peptide libraries.

## Evidence

- [readme] Pyteomics provides modules for calculation of basic physico-chemical properties of polypeptides: mass and isotopic distribution, charge and pI, chromatographic retention time: "calculation of basic physico-chemical properties of polypeptides: mass and isotopic distribution, charge and pI, chromatographic retention time"
- [intro] Pyteomics provides a mass module that calculates isotopic distribution as part of its suite of basic physico-chemical property calculations for polypeptides.: "Pyteomics provides a mass module that calculates isotopic distribution as part of its suite of basic physico-chemical property calculations"
- [methods] Import the pyteomics.mass module and define one or more peptide sequences as input strings. Call the isotopic distribution calculation function on each peptide composition to compute relative abundances of isotopic peaks.: "Import the pyteomics.mass module and define one or more peptide sequences as input strings. Call the isotopic distribution calculation function on each peptide composition to compute relative"
- [methods] Format and export the isotopic distribution results (m/z, intensity pairs) to a CSV or JSON file; optionally visualize the envelope using matplotlib.: "Format and export the isotopic distribution results (m/z, intensity pairs) to a CSV or JSON file; optionally visualize the envelope using matplotlib"
- [readme] pip install pyteomics: "pip install pyteomics"
- [readme] Pyteomics is a collection of lightweight and handy tools for Python that help to handle various sorts of proteomics data.: "Pyteomics is a collection of lightweight and handy tools for Python that help to handle various sorts of proteomics data"
