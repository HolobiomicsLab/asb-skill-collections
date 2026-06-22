---
name: mass-spectrometry-adduct-nomenclature-and-formula-transformation
description: Use when you have a neutral molecular formula (e.g., C3H8O2) and need to compute the adducted formula that will actually be observed in MS data;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mzapy.isotopes
  - h5py
  - collections.UserDict
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c01653
  title: mzapy
- doi: 10.1021/acs.jproteome.2c00313
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzapy_cq
    doi: 10.1021/acs.analchem.3c01653
    title: mzapy
  dedup_kept_from: coll_mzapy_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c01653
  all_source_dois:
  - 10.1021/acs.analchem.3c01653
  - 10.1021/acs.jproteome.2c00313
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-adduct-nomenclature-and-formula-transformation

## Summary

Transform molecular formulas to their MS adduct equivalents by applying charge-specific composition deltas (e.g., [M+H]+, [M+Na]+, [M-H]-), and validate adduct strings against a curated registry of 21 common ionization modes. This skill bridges molecular composition representation with mass spectrometry acquisition modes, essential for predicting observed m/z values and interpreting fragmentation patterns.

## When to use

You have a neutral molecular formula (e.g., C3H8O2) and need to compute the adducted formula that will actually be observed in MS data; or you have an adduct designation from experimental metadata ([M+H]+, [M+Na]+, [M+2H]2+, [M-H]-, etc.) and must validate it against the supported ionization registry or compute the mass delta it introduces. Use this when reconciling between chemical formulas in compound databases and observed m/z peaks in multidimensional MS workflows (LC–MS, IM–MS, DIA).

## When NOT to use

- Adduct state is unknown or absent from the 21 curated adduct list (e.g., exotic adducts [M+Cl]-, [M+I]- not in the mzapy registry)
- Input is already an adducted formula and you need to back-calculate the neutral composition—use subtraction on MolecularFormula instead
- You are working with multiply charged ions where the charge state is not explicitly specified in the adduct string (ambiguous notation)

## Inputs

- Neutral molecular formula as MolecularFormula object or dict(str:int) mapping element symbols to counts (e.g., {'C': 3, 'H': 8, 'O': 2})
- Adduct designation string (e.g., '[M+H]+', '[M+Na]+', '[M-H]-', '[M+2H]2+', '[M+NH4]+')
- Element monoisotopic mass dictionary (_ELEMENT_MONOISO_MASS: 24 entries)

## Outputs

- Adducted MolecularFormula object with element-count dict updated by charge-specific composition delta
- Monoisotopic mass (float) of the adducted species, used to calculate theoretical m/z
- Composition delta dict (str:int) representing net element additions/subtractions for the adduct
- Boolean validation result (True/False) for adduct string membership in supported registry

## How to apply

First, validate the adduct string against the mzapy isotopes module's list of 21 supported adducts using `valid_ms_adduct()`, which checks both notation and charge state. Next, retrieve the composition delta for that adduct (e.g., [M+H]+ adds one proton: {'H': +1}; [M+Na]+ adds sodium minus one proton: {'Na': +1, 'H': -1}). Apply the delta to the neutral molecular formula by element-wise addition to obtain the adducted formula. Finally, use `ms_adduct_formula()` to compute the net composition delta, and `monoiso_mass()` on the adducted formula to obtain the theoretical monoisotopic m/z for charge determination. This workflow ensures consistency across LC–MS, IM–MS, and DIA data acquisition modes where adduct states vary by ionization polarity and chemical matrix.

## Related tools

- **mzapy.isotopes** (Provides MolecularFormula data structure, adduct registry (21 ionization modes), validation functions (valid_ms_adduct, valid_element), and composition delta computation (ms_adduct_formula, monoiso_mass)) — https://github.com/PNNL-m-q/mzapy
- **h5py** (Reads monoisotopic mass reference data and metadata (including adduct state annotations) from MZA HDF5 files)
- **collections.UserDict** (Base class for MolecularFormula, enabling dict-like operations (element-wise addition/subtraction) used in adduct formula transformation)

## Examples

```
from mzapy.isotopes import MolecularFormula, valid_ms_adduct, ms_adduct_formula, monoiso_mass; neutral = MolecularFormula({'C': 6, 'H': 12, 'O': 6}); adduct = '[M+H]+'; assert valid_ms_adduct(adduct); delta = ms_adduct_formula(neutral, adduct); adducted = neutral + delta; mz_theoretical = monoiso_mass(adducted) / 1.0
```

## Evaluation signals

- Adduct string passes valid_ms_adduct() validation against the 21-entry supported adduct registry without exception
- Adducted formula element counts are non-negative integers after applying the charge-specific delta; negative element counts flag invalid transformations
- Monoisotopic mass of adducted formula is consistent with observed m/z in MS1 spectra (within ±5 ppm tolerance typical for high-resolution MS, or ±0.05 Da for low-res instruments)
- Round-trip consistency: neutral_formula + adduct_delta == adducted_formula; adducted_formula - adduct_delta == neutral_formula
- Charge state extracted from adduct string matches charge used in m/z calculation (observed_mz = (adducted_mass ± delta) / charge), validated across MS1 and precursor metadata columns (PrecursorCharge)

## Limitations

- Only 21 adducts are supported in the mzapy registry; exotic adducts (e.g., [M+Cl]-, [M+I]-, metal complexes) will fail validation and require manual extension of the adduct list.
- Adduct nomenclature is case-sensitive and requires exact bracket/charge notation (e.g., '[M+H]+' not 'M+H+' or '[M+H]1+'); malformed strings will not validate.
- The monoisotopic mass computation assumes natural isotopic abundance; isotope-edited samples (e.g., 13C- or 15N-labeled) require separate handling and are not addressed by this skill alone.
- Multimeric adducts ([2M+H]+, [3M+Na]+) require the input formula to be multiplied beforehand; the skill assumes single-molecule adduct transformation.
- For multiply charged species (e.g., [M+2H]2+, [M+3H]3+), the correct charge must be extracted from the adduct string to compute m/z accurately; charge inference from mass alone is ambiguous.

## Evidence

- [other] Adduct registry definition and supported modes: "Define 21 MS adducts with charge assignments ([M]+, [M+H]+, [M+Na]+, [M+K]+, [M+2K]2+, [M+NH4]+, [M+H-H2O]+, [M-H]-, [M+HCOO]-, [M+CH3COO]-, [M-2H]2-, [M-3H]3-, [M+2Na-H]+, [M+2H]2+, [M+3H]3+ through"
- [other] Utility validation and transformation functions: "valid_element (checking against _ELEMENT_MONOISO_MASS dictionary), valid_ms_adduct (checking against supported adduct list), monoiso_mass (returning exact mass from element dict), ms_adduct_formula"
- [other] MolecularFormula as dict-like data structure: "Design MolecularFormula as a collections.UserDict subclass with four initialization modes (empty, from dict, from MolecularFormula, from kwargs)"
- [other] Element-wise arithmetic operators for formula transformation: "Implement element-wise addition (__add__, __radd__) and subtraction (__sub__) operators supporting both MolecularFormula and dict(str:int) operands, ensuring operations return MolecularFormula"
- [other] Monoisotopic mass reference data: "Populate _ELEMENT_MONOISO_MASS with 24 elements and their monoisotopic masses as documented"
- [readme] MZA format and MS metadata context: "each row in the metadata table represents a spectrum and the columns represent the properties of the spectrum such as scan number (unique to each spectrum), MS level, activation (i.e., ion"
