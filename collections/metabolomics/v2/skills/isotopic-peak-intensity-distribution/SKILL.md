---
name: isotopic-peak-intensity-distribution
description: Use when when you have one or more peptide sequences (as strings) and need to predict their isotopic distribution pattern for MS instrument simulation, peak deconvolution, or validation of observed isotopic envelopes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pip
  - conda
  - NumPy
  - matplotlib
  - Pyteomics
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
---

# isotopic-peak-intensity-distribution

## Summary

Compute and visualize the relative abundances of isotopic peaks (m/z and intensity pairs) for polypeptide sequences using Pyteomics' mass module. This skill enables quantitative prediction of how peptide ions will appear in mass spectrometry experiments across their natural isotopic envelope.

## When to use

When you have one or more peptide sequences (as strings) and need to predict their isotopic distribution pattern for MS instrument simulation, peak deconvolution, or validation of observed isotopic envelopes. Apply this when designing targeted proteomics experiments or interpreting high-resolution MS data where isotopic fine structure matters.

## When NOT to use

- Input is already an observed mass spectrum from MS data — use deconvolution or peak-picking instead to extract real isotopic patterns.
- You need to account for post-translational modifications not explicitly encoded in the peptide string — modify the sequence or composition object first.
- Target molecule is not a polypeptide (e.g., a small metabolite or lipid) — Pyteomics is specialized for proteomics and may lack pre-configured isotope tables for non-peptides.

## Inputs

- peptide sequence string(s)
- peptide composition object (from pyteomics.mass)
- charge state (optional; for m/z calculation)

## Outputs

- isotopic distribution table (m/z, intensity pairs)
- CSV or JSON export of isotopic peaks
- matplotlib visualization of isotopic envelope

## How to apply

Install Pyteomics (via pip or conda with NumPy as a core dependency), then import the pyteomics.mass module and call its isotopic distribution calculation function on each peptide composition. The function computes relative abundances for each isotopic peak by accounting for the natural abundance of heavy isotopes (13C, 15N, 18O, etc.) in the amino acid composition. Format the output (m/z and intensity pairs) as CSV or JSON; optionally visualize the isotopic envelope using matplotlib to confirm the predicted peak pattern matches expected charge states and mass offsets.

## Related tools

- **Pyteomics** (Core library providing the mass module with isotopic distribution calculation function for polypeptides) — https://github.com/levitsky/pyteomics
- **NumPy** (Core dependency required by Pyteomics for numerical computation of isotope abundances)
- **matplotlib** (Visualization library for rendering isotopic envelope plots)
- **pip** (Package manager for installing Pyteomics and dependencies)
- **conda** (Alternative package manager for installing Pyteomics from bioconda channel)

## Examples

```
from pyteomics import mass; peptide = 'PEPTIDE'; iso_dist = mass.isotopic_distribution(mass.calculate_mass(sequence=peptide), charge=1); import csv; csv.writer(open('isotopic_peaks.csv','w')).writerows(iso_dist.items())
```

## Evaluation signals

- Isotopic peak m/z values are in increasing order and separated by expected intervals (1 Da for singly charged, 0.5 Da for doubly charged, etc.)
- Peak intensities sum to 1.0 or normalized to 100%, confirming valid probability distribution
- Highest intensity peak (monoisotopic or M+1) aligns with manual calculation or reference data for the given peptide composition
- Visualization shows correct peak count and envelope shape for the peptide's elemental composition (e.g., longer peptides show broader envelopes)
- CSV/JSON export can be parsed without errors and contains no NaN or negative intensity values

## Limitations

- Calculation assumes natural isotope abundances; does not account for isotopic labeling (e.g., SILAC, 15N labeling) unless composition is manually adjusted.
- Pyteomics does not include post-translational modifications by default; PTM masses must be added to the peptide composition before calculation.
- Isotopic distribution is computed in silico from elemental composition; it does not predict ion suppression, fragmentation patterns, or ionization efficiency observed in real MS experiments.
- Performance may degrade for very large polypeptides (>100 kDa) due to combinatorial complexity of isotope calculations, though typical peptides (< 10 kDa) are unaffected.

## Evidence

- [other] Pyteomics provides a mass module that calculates isotopic distribution as part of its suite of basic physico-chemical property calculations for polypeptides.: "Pyteomics provides a mass module that calculates isotopic distribution as part of its suite of basic physico-chemical property calculations for polypeptides."
- [other] Workflow steps from task card showing the method.: "Call the isotopic distribution calculation function on each peptide composition to compute relative abundances of isotopic peaks."
- [readme] Installation and dependencies confirmed in README.: "calculation of basic physico-chemical properties of polypeptides: mass and isotopic distribution, charge and pI, chromatographic retention time"
- [other] Export and visualization guidance from workflow.: "Format and export the isotopic distribution results (m/z, intensity pairs) to a CSV or JSON file; optionally visualize the envelope using matplotlib."
- [methods] Installation via pip from article extraction.: "pip install pyteomics"
