---
name: sequence-to-feature-mapping
description: Use when when you have a list of polypeptide sequences (plain text, CSV,
  or FASTA format) and need to compute their monoisotopic mass and average mass for
  downstream mass spectrometry interpretation, database matching, or physico-chemical
  property annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0399
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0078
  tools:
  - Python
  - pip
  - NumPy
  - Pyteomics
  - pandas
  - SQLAlchemy
  techniques:
  - mass-spectrometry
  license_tier: restricted
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

# Reconstruct peptide monoisotopic mass calculation from sequence using pyteomics.mass

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calculate monoisotopic and average mass values for polypeptide sequences using Pyteomics' mass module, enabling conversion of raw peptide sequence strings into quantitative physico-chemical properties suitable for proteomics workflows.

## When to use

When you have a list of polypeptide sequences (plain text, CSV, or FASTA format) and need to compute their monoisotopic mass and average mass for downstream mass spectrometry interpretation, database matching, or physico-chemical property annotation.

## When NOT to use

- Input is already an annotated mass spectrometry feature table (mzML, mzXML, or mzJSON) — use direct MS data parsing instead.
- You need isotopic distribution profiles beyond monoisotopic and average mass — use pyteomics.mass.isotopic_composition_support for full isotope envelopes.
- Sequences contain non-standard or highly modified amino acids not registered in Unimod — manual validation or custom mass lookup tables required.

## Inputs

- list of polypeptide sequences (plain text, one per line)
- CSV file with peptide sequences
- FASTA file with protein or peptide sequences

## Outputs

- CSV table with columns: sequence, monoisotopic_mass, average_mass
- pandas DataFrame with physico-chemical properties
- structured proteomics feature table suitable for MS data matching

## How to apply

Install Pyteomics via pip (with NumPy as a core dependency). Load polypeptide sequences from an input file (one sequence per line or CSV format). Import the pyteomics.mass module and apply the monoisotopic mass calculation function to each sequence. Calculate the average mass for each sequence using the same module. Aggregate the sequence, monoisotopic mass, and average mass into a structured table (CSV or pandas DataFrame) and save to output file. The module handles standard amino acid alphabets and modified peptides according to Unimod conventions.

## Related tools

- **Pyteomics** (Core library for monoisotopic and average mass calculation from peptide sequences via pyteomics.mass module) — https://github.com/levitsky/pyteomics
- **NumPy** (Core numerical computing dependency required by Pyteomics for array operations)
- **pandas** (Optional: structure and export calculated mass values into DataFrames or CSV tables)
- **SQLAlchemy** (Optional: access Unimod database for modified amino acid mass definitions)

## Examples

```
from pyteomics import mass; import pandas as pd; seqs = ['PEPTIDE', 'SEQUENCE']; df = pd.DataFrame({'sequence': seqs, 'mono_mass': [mass.calculate_mass(s) for s in seqs], 'avg_mass': [mass.calculate_mass(s, average=True) for s in seqs]}); df.to_csv('peptide_masses.csv', index=False)
```

## Evaluation signals

- All input sequences are present in the output table with no rows dropped or duplicated.
- Monoisotopic mass values fall within expected range for peptides (typically 300–5000 Da for oligopeptides, higher for proteins).
- Average mass is consistently and slightly higher than monoisotopic mass (difference reflects natural isotope abundance).
- Modified amino acids (e.g., phosphoserines, acetylated lysines) produce mass shifts consistent with their chemical composition.
- Output table can be parsed back into a pandas DataFrame with numeric dtypes for mass columns without casting errors.

## Limitations

- Pyteomics uses Unimod registry for modified amino acids; sequences with non-registered or custom modifications will require manual mass adjustment or a custom lookup table.
- No built-in validation of sequence format or amino acid alphabet; invalid characters or malformed sequences may silently produce NaN or raise exceptions depending on the input.
- Monoisotopic mass calculation assumes standard peptide chemistry (C, H, N, O, S, P); non-standard isotope tracers (e.g., heavy labeled amino acids) require explicit mass offset addition.
- No changelog found in repository documentation; version compatibility and bug fixes must be verified through GitHub releases or issue tracker.

## Evidence

- [readme] Pyteomics provides modules for calculation of basic physico-chemical properties of polypeptides: "calculation of basic physico-chemical properties of polypeptides: mass and isotopic distribution, charge and pI, chromatographic retention time"
- [other] Workflow: Load sequences, import mass module, apply functions, aggregate results: "Load the list of polypeptide sequences from an input file (one sequence per line, or CSV format). 3. Import the pyteomics.mass module and apply the monoisotopic mass calculation function to each"
- [methods] NumPy is a core dependency of Pyteomics: "Pyteomics supports recent versions of Python 3."
- [methods] Installation methods via pip and conda: "pip install pyteomics"
- [readme] Pyteomics is a collection of lightweight and handy tools for Python: "Pyteomics is a collection of lightweight and handy tools for Python that help to handle various sorts of proteomics data"
