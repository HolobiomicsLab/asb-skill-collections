---
name: peptide-mass-calculation-average
description: Use when you have a list of polypeptide sequences (one per line or CSV format) and need to compute average mass (weighted by natural isotope abundances) to compare against experimental LC-MS or MS/MS data where the full isotopic distribution—not just the most abundant peak—is relevant for peptide.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0399
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pip
  - NumPy
  - Pyteomics
  - pandas
  techniques:
  - LC-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peptide-mass-calculation-average

## Summary

Calculate average molecular mass for polypeptide sequences using Pyteomics, complementing monoisotopic mass to characterize the full isotopic envelope of peptides. This is essential for relating theoretical peptide properties to experimental mass spectrometry observations where natural isotope abundances affect observed m/z.

## When to use

You have a list of polypeptide sequences (one per line or CSV format) and need to compute average mass (weighted by natural isotope abundances) to compare against experimental LC-MS or MS/MS data where the full isotopic distribution—not just the most abundant peak—is relevant for peptide identification or validation.

## When NOT to use

- Input sequences are already annotated with experimentally measured masses — use direct comparison instead of recalculation.
- You require isotopic envelopes or full isotopic patterns; use pyteomics.mass.isotopic_composition_* functions instead.
- Input data are non-standard amino acid codes or heavily modified peptides not covered by standard chemical composition tables.

## Inputs

- polypeptide sequence list (plain text, one sequence per line, or CSV format)
- amino acid sequence strings (standard IUPAC nomenclature, optionally with post-translational modifications)

## Outputs

- pandas DataFrame or CSV table with columns: sequence, monoisotopic_mass, average_mass
- structured mass data suitable for downstream proteomics analysis or MS matching

## How to apply

Install Pyteomics via pip with NumPy as a required dependency. Load polypeptide sequences from an input file and import the pyteomics.mass module. Apply the average mass calculation function to each sequence; Pyteomics computes this by summing element masses weighted by their natural isotope abundances, providing a complementary view to monoisotopic mass. Aggregate the sequence, average mass, and any other properties (e.g., monoisotopic mass, charge, pI) into a structured pandas DataFrame or CSV table. Save the output and verify that average mass values are consistently higher than monoisotopic masses (typically by 1–3 Da for peptides) and fall within expected ranges for the peptide composition.

## Related tools

- **Pyteomics** (Core library for mass and isotopic distribution calculation from peptide sequences) — https://github.com/levitsky/pyteomics
- **NumPy** (Required dependency for numerical array operations underlying mass calculations)
- **pandas** (Optional but recommended for structuring and exporting mass calculation results to CSV or DataFrame)
- **pip** (Package manager for installing Pyteomics and dependencies)

## Examples

```
from pyteomics import mass; import pandas as pd; sequences = ['PEPTIDE', 'MKFLK']; data = {'sequence': sequences, 'monoisotopic': [mass.fast_mass(s) for s in sequences], 'average': [mass.fast_mass(s, mass_type='average') for s in sequences]}; df = pd.DataFrame(data); df.to_csv('peptide_masses.csv', index=False)
```

## Evaluation signals

- Average mass is consistently 1–3 Da higher than monoisotopic mass for typical peptides (due to heavier isotopes).
- Output table schema matches expected columns: sequence, monoisotopic_mass, average_mass, with no missing values.
- Calculated masses are within expected range for peptide MW based on sequence composition (rough check: ~110 Da per amino acid residue plus water ~18 Da).
- Values are numeric, non-negative, and sortable; no NaN or inf values for valid sequences.
- Round-trip consistency: re-running the same sequence list produces identical mass values (reproducibility check).

## Limitations

- Pyteomics uses standard IUPAC atomic weights; custom isotope abundances or non-standard elements are not supported without modification.
- Post-translational modifications must be specified in sequence notation or separately; automatic PTM detection from sequence text is not performed.
- Average mass calculation assumes natural isotope abundances; samples enriched in stable isotopes (e.g., 13C, 15N) will yield different values.
- No changelog documented in the source; version-to-version changes in mass calculation precision or element data are not publicly tracked.

## Evidence

- [readme] Pyteomics provides modules for calculation of basic physico-chemical properties of polypeptides: mass and isotopic distribution: "calculation of basic physico-chemical properties of polypeptides: mass and isotopic distribution"
- [other] Calculate the average mass for each sequence using the mass module: "Calculate the average mass for each sequence using the mass module"
- [other] Aggregate sequence, monoisotopic mass, and average mass into a structured table (CSV or pandas DataFrame) and save to output file: "Aggregate sequence, monoisotopic mass, and average mass into a structured table (CSV or pandas DataFrame)"
- [other] Import the pyteomics.mass module and apply the monoisotopic mass calculation function to each sequence: "Import the pyteomics.mass module and apply the monoisotopic mass calculation function to each sequence"
- [methods] Pyteomics supports recent versions of Python 3: "Pyteomics supports recent versions of Python 3"
