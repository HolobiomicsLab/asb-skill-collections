---
name: mass-spectrum-simulation
description: Use when when you have one or more peptide sequences (as strings) and need to predict their theoretical isotopic distribution patterns to compare against experimental MS data, validate peak assignments, or generate synthetic spectra for method development.
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
  - pip / conda
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

# mass-spectrum-simulation

## Summary

Compute isotopic distribution envelopes for peptide sequences to predict mass spectrometry peak patterns. This skill generates m/z and relative intensity pairs for theoretical peptide ions, enabling validation of experimental spectra and rapid software prototyping in proteomics workflows.

## When to use

When you have one or more peptide sequences (as strings) and need to predict their theoretical isotopic distribution patterns to compare against experimental MS data, validate peak assignments, or generate synthetic spectra for method development. Apply this skill before matching experimental peaks to theoretical masses or when designing targeted proteomics assays.

## When NOT to use

- Input is already experimental centroided or profile MS data — use deconvolution or peak-picking instead.
- You need to analyze intact proteins (>~50 kDa) where isotopic resolution is lost — consider average-mass approximation.
- Peptide modifications are unknown or highly variable — isotopic distribution will be inaccurate without correct composition.

## Inputs

- Peptide sequence strings (e.g., 'PEPTIDE', 'MVHLTPEEKS')
- Peptide composition objects (from pyteomics.mass.Composition)

## Outputs

- Isotopic distribution pairs (m/z, intensity)
- CSV or JSON files with m/z and relative abundance columns
- Matplotlib visualizations of isotopic envelopes

## How to apply

Install Pyteomics via pip or conda, ensuring NumPy is available as a core dependency. Import the pyteomics.mass module and define peptide sequences as input strings. Call the isotopic distribution calculation function on each peptide composition to compute relative abundances of isotopic peaks at different m/z values. The function returns pairs of (m/z, intensity) that characterize the isotopic envelope. Format and export results to CSV or JSON; optionally visualize the envelope using matplotlib to inspect peak spacing, height ratios, and overall pattern shape. The isotopic pattern reflects the natural abundance of heavy isotopes (13C, 15N, 18O, 34S, 37Cl) in the peptide composition and serves as a fingerprint for ion identification.

## Related tools

- **Pyteomics** (Core library providing pyteomics.mass module for isotopic distribution calculation) — https://github.com/levitsky/pyteomics
- **NumPy** (Dependency for numerical computation of isotopic abundance arrays)
- **matplotlib** (Optional visualization of isotopic envelope peaks and intensities)
- **pip / conda** (Package managers for installing Pyteomics and dependencies)

## Examples

```
from pyteomics import mass; peptide = 'PEPTIDE'; iso_dist = mass.isotopic_composition_from_string(peptide); print([(m, intensity) for m, intensity in sorted(iso_dist.items())])
```

## Evaluation signals

- Isotopic pattern monoisotopic peak m/z matches theoretical mass of peptide composition (within <5 ppm).
- Relative intensities of adjacent isotopic peaks follow expected 13C/15N abundance ratios (first peak ~100%, second ~30–50% for typical peptides).
- Peak spacing between consecutive isotopes matches 1/z (charge state) — e.g., ~1 m/z for z=1, ~0.5 m/z for z=2.
- Output CSV/JSON structure contains non-empty m/z and intensity columns with matching row counts.
- Visualized envelope shape exhibits smooth, bell-curve-like profile consistent with natural isotope abundances; no spurious or inverted peaks.

## Limitations

- Accuracy depends on correct peptide sequence and knowledge of post-translational modifications; incorrect composition will yield incorrect isotopic distribution.
- For very large peptides or proteins (>50 kDa), isotopic resolution diminishes and isotopic peaks merge, reducing utility of fine-structure simulation.
- Pyteomics does not natively account for charge-state-dependent isotopic fine structure or conformational effects; it assumes ideal gas-phase ions.
- No changelog available in repository documentation, limiting visibility of bug fixes or method updates.

## Evidence

- [other] Research question: What is the mechanism by which Pyteomics computes isotopic distribution for peptides?: "Pyteomics provides a mass module that calculates isotopic distribution as part of its suite of basic physico-chemical property calculations for polypeptides."
- [other] Workflow from task card: "Call the isotopic distribution calculation function on each peptide composition to compute relative abundances of isotopic peaks."
- [readme] README introduction: "calculation of basic physico-chemical properties of polypeptides: mass and isotopic distribution, charge and pI, chromatographic retention time"
- [methods] Installation instructions from article enrichment: "Install Pyteomics with pip or conda, ensuring NumPy is available as a core dependency."
