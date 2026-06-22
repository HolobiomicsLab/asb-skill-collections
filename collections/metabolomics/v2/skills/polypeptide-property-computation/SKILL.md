---
name: polypeptide-property-computation
description: Use when you have one or more polypeptide sequences (from FASTA, CSV, or direct input) and need to compute monoisotopic mass, average mass, isotopic distribution, charge state, or isoelectric point for downstream proteomics analysis such as MS database matching, retention time prediction, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0392
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pip
  - NumPy
  - Pyteomics
  - conda
  - pandas
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- Pyteomics is a collection of lightweight and handy tools for Python
- Pyteomics supports recent versions of Python 3.
- pip install pyteomics
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

# polypeptide-property-computation

## Summary

Compute physicochemical properties of polypeptides—including monoisotopic mass, average mass, isotopic distribution, charge, and pI—from amino acid sequences using Pyteomics mass modules. This skill enables rapid, reproducible calculation of mass-dependent proteomics features required for peptide identification and quantification workflows.

## When to use

Use this skill when you have one or more polypeptide sequences (from FASTA, CSV, or direct input) and need to compute monoisotopic mass, average mass, isotopic distribution, charge state, or isoelectric point for downstream proteomics analysis such as MS database matching, retention time prediction, or peptide property filtering.

## When NOT to use

- Input is already a feature table or pre-computed mass matrix; use this skill on raw sequences only.
- Polypeptide sequences contain non-standard amino acids not covered by Pyteomics' standard composition tables without explicit custom Composition object setup.
- Task requires real-time, high-throughput mass calculation on >10^7 sequences in a single pass; consider batch processing or compiled alternatives (e.g., C/Rust wrappers).

## Inputs

- polypeptide sequences (plain text, one per line; or CSV format)
- optional: list of post-translational modifications (PTMs) as Pyteomics Composition objects
- optional: desired ion charge state

## Outputs

- CSV table or pandas DataFrame with columns: sequence, monoisotopic_mass, average_mass
- optional: isotopic_composition (distribution of isotopologues)
- optional: isoelectric_point (pI)
- optional: charge_state

## How to apply

Install Pyteomics (via pip or conda with optional dependencies if XML parsing is required). Load polypeptide sequences from input file or in-memory list. Import the pyteomics.mass module and apply the monoisotopic_mass() or average_mass() function to each sequence, optionally specifying modifications or ion charge state. For isotopic distribution calculations, use the isotopic_composition() or isotope_mass_spectrum() functions. Aggregate results (sequence, monoisotopic mass, average mass, isotopic composition) into a structured table (CSV or pandas DataFrame) and validate output by spot-checking calculated masses against known reference peptides or by verifying consistency between monoisotopic and average mass values (average ≥ monoisotopic for the same sequence).

## Related tools

- **Pyteomics** (Core library providing mass calculation, isotopic distribution, and physicochemical property functions for polypeptides) — https://github.com/levitsky/pyteomics
- **pip** (Package installer for Pyteomics and dependencies)
- **conda** (Alternative package manager for Pyteomics via bioconda channel)
- **NumPy** (Core numerical computation dependency for Pyteomics mass calculations)
- **pandas** (Optional data structure for aggregating and outputting sequence properties)

## Examples

```
from pyteomics.mass import calculate_mass; sequences = ['PEPTIDE', 'MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVV']; masses = [{'monoisotopic': calculate_mass(seq, mass_type='monoisotopic'), 'average': calculate_mass(seq, mass_type='average')} for seq in sequences]; import pandas as pd; df = pd.DataFrame({'sequence': sequences, **{k: [m[k] for m in masses] for k in masses[0]}}); df.to_csv('peptide_masses.csv', index=False)
```

## Evaluation signals

- Monoisotopic mass value is strictly less than or equal to average mass for the same sequence (monoisotopic uses lightest isotope, average includes heavier isotopes).
- Output table has no null or NaN values for mass columns; all sequences produce valid numeric outputs.
- Spot-check: known reference peptide (e.g., insulin or trypsin digestion products) yields published monoisotopic mass values within <0.01 Da or <10 ppm tolerance.
- Isotopic distribution sums to approximately 1.0 (or 100%) across all isotopologues.
- Output row count equals input sequence count; no sequences silently dropped or duplicated.

## Limitations

- Pyteomics uses standard isotope composition tables; unusual isotope patterns from non-biological systems or enriched isotope samples may not be accurately represented.
- No built-in support for complex post-translational modifications without explicit Composition object definition; users must manually encode PTM masses.
- Calculation assumes the polypeptide is in a neutral or specified charge state; pH-dependent properties (pI) are computed theoretically and may diverge from experimental measurements in non-standard buffer conditions.
- Performance degrades linearly with sequence count; very large batches (>10^6 sequences) require external parallelization or batch splitting.
- No changelog is available in the repository, limiting ability to track breaking changes between versions.

## Evidence

- [readme] Pyteomics provides modules for calculation of basic physico-chemical properties of polypeptides: mass and isotopic distribution, charge and pI, chromatographic retention time.: "calculation of basic physico-chemical properties of polypeptides: mass and isotopic distribution, charge and pI, chromatographic retention time"
- [other] Install Pyteomics via pip with NumPy as a core dependency. Load the list of polypeptide sequences from an input file (one sequence per line, or CSV format). Import the pyteomics.mass module and apply the monoisotopic mass calculation function to each sequence. Calculate the average mass for each sequence using the mass module. Aggregate sequence, monoisotopic mass, and average mass into a structured table (CSV or pandas DataFrame) and save to output file.: "Import the pyteomics.mass module and apply the monoisotopic mass calculation function to each sequence. Calculate the average mass for each sequence using the mass module. Aggregate sequence,"
- [readme] Pyteomics is a collection of lightweight and handy tools for Python that help to handle various sorts of proteomics data.: "Pyteomics is a collection of lightweight and handy tools for Python that help to handle various sorts of proteomics data"
- [methods] pip install pyteomics and conda install -c bioconda pyteomics are standard installation methods; optional dependencies can be installed via pip install pyteomics[XML].: "pip install pyteomics"
