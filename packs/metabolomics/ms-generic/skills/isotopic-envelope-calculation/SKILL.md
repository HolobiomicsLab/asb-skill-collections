---
name: isotopic-envelope-calculation
description: Use when when you have one or more peptide sequences (as strings) and need to predict their theoretical isotopic distribution for comparison against experimental MS peaks, validation of mass calibration, or simulation of expected peptide signals in a mass spectrometry assay.
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
  - pandas
  techniques:
  - mass-spectrometry
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

# isotopic-envelope-calculation

## Summary

Compute the relative abundance distribution of isotopic peaks (m/z and intensity pairs) for a given polypeptide sequence using Pyteomics' mass module. This enables prediction of the mass spectrum envelope expected from a peptide, which is essential for matching experimental MS data to theoretical values in proteomics.

## When to use

When you have one or more peptide sequences (as strings) and need to predict their theoretical isotopic distribution for comparison against experimental MS peaks, validation of mass calibration, or simulation of expected peptide signals in a mass spectrometry assay.

## When NOT to use

- You have already-measured experimental mass spectrum peaks and need to perform peak picking or deconvolution—use MS-specific peak detection instead.
- Your input is a protein or genomic sequence; first digest or translate to peptide sequences.
- You need to account for instrument resolution, adducts, or modifications not yet defined in Pyteomics—consider enriching your input or post-processing results.

## Inputs

- peptide sequence string(s)
- optionally: peptide composition object from pyteomics.mass

## Outputs

- isotopic distribution envelope (m/z, intensity pairs)
- CSV or JSON file of m/z and intensity values
- optional: matplotlib visualization of isotopic envelope

## How to apply

Install Pyteomics (via pip or conda) with NumPy as a core dependency. Import the pyteomics.mass module and define your peptide sequences as input strings. Call the isotopic distribution calculation function on each peptide composition to compute the relative abundances of isotopic peaks. The function returns m/z and intensity pairs that describe the expected peak envelope. Format and optionally visualize the results using matplotlib or export to a structured format (CSV or JSON) for downstream analysis or comparison with experimental spectra.

## Related tools

- **Pyteomics** (Provides the mass module for isotopic distribution calculation and core physico-chemical property computations for polypeptides) — https://github.com/levitsky/pyteomics
- **NumPy** (Core numerical dependency for efficient array-based computation of isotopic abundances)
- **matplotlib** (Optional visualization of isotopic peak envelopes as line plots or bar charts)
- **pandas** (Optional export and tabulation of isotopic distribution results to CSV or structured formats)

## Examples

```
from pyteomics.mass import Composition; comp = Composition(sequence='PEPTIDE'); dist = comp.isotopic_composition_abundance(); print([(mz, intensity) for mz, intensity in sorted(dist.items())])
```

## Evaluation signals

- Output m/z values are in ascending order and span the expected mass range for the peptide and its isotopologues.
- Sum of all intensity values equals 1.0 (or 100% if normalized to the most abundant peak).
- The most intense peak corresponds to the monoisotopic composition (all atoms at lowest mass isotope).
- Peak spacing in m/z reflects the expected 1 Da difference between consecutive isotopologues (for singly charged ions).
- Results are reproducible across multiple runs with identical input sequences and Pyteomics version.

## Limitations

- Computation assumes neutral polypeptides; does not inherently account for charge states or common adducts (e.g., [M+H]⁺, [M+Na]⁺) without manual adjustment of m/z values post-calculation.
- Isotopic distribution depends on accurate elemental composition; modifications (e.g., phosphorylation, glycosylation) must be explicitly represented in the input or composition object.
- High-resolution envelopes for large peptides (>20 kDa) may include many peaks; filtering by intensity threshold may be necessary for practical visualization or matching.
- No built-in isotope pattern deconvolution; the output is theoretical and assumes no instrument noise or overlapping peptide signals.

## Evidence

- [readme] Pyteomics provides modules for calculation of basic physico-chemical properties of polypeptides including mass and isotopic distribution: "calculation of basic physico-chemical properties of polypeptides: mass and isotopic distribution"
- [methods] The workflow involves calling isotopic distribution calculation function on each peptide composition to compute relative abundances of isotopic peaks: "Call the isotopic distribution calculation function on each peptide composition to compute relative abundances of isotopic peaks"
- [methods] Results should be formatted and exported to a structured file format and optionally visualized: "Format and export the isotopic distribution results (m/z, intensity pairs) to a CSV or JSON file; optionally visualize the envelope using matplotlib"
- [methods] Pyteomics requires NumPy as a core dependency: "Install Pyteomics with pip or conda, ensuring NumPy is available as a core dependency"
