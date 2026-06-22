---
name: compound-structure-representation
description: Use when when you have experimental MS/MS data (peak lists, precursor m/z, charge state, adduct type) paired with a chemical structure (SMILES or structural identifier), and need to create a unified Compound object for spectral alignment, modification-site prediction, or comparative fragmentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - ModiFinder
  - Python
  - RDKit
  - matplotlib
  - GNPS Compound class
derived_from:
- doi: 10.1021/jasms.4c00061
  title: ModiFinder
evidence_spans:
- mf = ModiFinder(known_compound, modified_compound, mz_tolerance=0.01, ppm_tolerance=40)
- mf = ModiFinder(known_compound, modified_compound, helpers=helpers_array, **args)
- ModiFinder requires Python 3.9 or above.
- ModiFinder requires Python 3.9 or above
- 'rdkit: http://www.rdkit.org/'
- ModiFinder includes powerful visualization tools built on RDKit and matplotlib for creating publication-quality figures.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_modifinder_cq
    doi: 10.1021/jasms.4c00061
    title: ModiFinder
  dedup_kept_from: coll_modifinder_cq
schema_version: 0.2.0
---

# compound-structure-representation

## Summary

Encode chemical structures as SMILES strings and spectroscopic metadata (precursor m/z, charge, adduct) into Compound objects for downstream mass spectrometry analysis. This skill is essential for initializing structured chemical representations that link molecular topology to experimental ionization and fragmentation data.

## When to use

When you have experimental MS/MS data (peak lists, precursor m/z, charge state, adduct type) paired with a chemical structure (SMILES or structural identifier), and need to create a unified Compound object for spectral alignment, modification-site prediction, or comparative fragmentation analysis. Use this skill as the first step before running ModiFinder or any tool that requires both molecular identity and tandem mass spectra.

## When NOT to use

- Peak list is already aggregated into a feature table or consensus spectrum without individual precursor information.
- SMILES or structural annotation is unavailable and only spectral similarity (not structure-aware alignment) is needed.
- Input spectra require custom preprocessing parameters (e.g., different mz_tolerance or peak-filtering thresholds) not compatible with ModiFinder defaults.

## Inputs

- Peak list (list of [m/z, intensity] pairs)
- Precursor m/z (float)
- Precursor charge state (integer)
- Adduct annotation (string, e.g., '[M+H]+', '[M-H]-')
- SMILES string (str)

## Outputs

- Compound object with normalized spectrum and structural metadata
- Preprocessed peak array with applied tolerance and intensity filtering
- RDKit molecule object for visualization and atom indexing

## How to apply

Instantiate a Compound object by providing: (1) a peak list formatted as [[m/z, intensity], ...]; (2) precursor_mz (float); (3) precursor_charge (integer); (4) adduct string (e.g., '[M+H]+', '[M-H]-'); and (5) SMILES string (required for known compounds, optional for modified compounds). Apply default preprocessing during construction with mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, and normalize_peaks=True to standardize peak representation. The SMILES encoding ensures that structural features (atoms, bonds, functional groups) can be mapped to fragment ions during spectral alignment and enable per-atom modification-site probability calculation.

## Related tools

- **ModiFinder** (Consumes Compound objects to perform tandem mass spectral alignment and modification-site probability prediction.) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **RDKit** (Parses SMILES strings into molecule objects and enables structure visualization and atom indexing.) — http://www.rdkit.org/
- **GNPS Compound class** (Alternative constructor to fetch pre-annotated compounds from GNPS using accession identifiers.) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base

## Examples

```
main_compound = Compound(spectrum=[[101.02, 999], [119.03, 500]], precursor_mz=200.05, precursor_charge=1, adduct='[M+H]+', smiles='CC(=O)O'); mod_compound = Compound(spectrum=[[101.02, 450], [135.04, 999]], precursor_mz=216.04, precursor_charge=1, adduct='[M+H]+', smiles=None)
```

## Evaluation signals

- Compound object is instantiated without error and contains all required attributes: spectrum (normalized peak list), precursor_mz, precursor_charge, adduct, SMILES.
- Peak intensities are normalized (maximum intensity = 1.0 or equivalent); small peaks below ratio_to_base_peak=0.01 threshold are removed.
- RDKit molecule object is valid: SMILES parses without errors, atom count and connectivity match chemical formula.
- Precursor m/z and charge state satisfy chemical plausibility checks (e.g., charge consistent with adduct type, precursor m/z > 0).
- Compound pair (known + modified) can be passed to ModiFinder without type errors; generate_probabilities() executes successfully.

## Limitations

- SMILES parsing requires valid SMILES syntax; invalid or non-standard SMILES will raise RDKit exceptions.
- Default preprocessing (mz_tolerance=0.01, ppm_tolerance=40) may be too strict for low-resolution or high-noise spectra, potentially removing valid fragments.
- Precursor m/z and charge state must be experimentally accurate; misassignment will propagate incorrect neutral mass and fragment hypotheses to downstream ModiFinder calculations.
- Adduct annotation must match the ion type present in the MS/MS data; incorrect adduct specification will misalign theoretical fragments to observed peaks.

## Evidence

- [other] Instantiate a ModiFinder object with the known compound, modified compound, and default CosineAlignmentEngine and MAGMaAnnotationEngine.: "Retrieve the known and modified compounds from GNPS using their accession identifiers via the Compound class constructor, applying default preprocessing (mz_tolerance=0.01, ppm_tolerance=40,"
- [readme] ModiFinder requires two spectrum objects: main_compound with SMILES, precursor_mz, precursor_charge, adduct; mod_compound with same metadata.: "ModiFinder requires two spectrum objects:
```
main_compound = Compound(
    spectrum=s1_peaks,
    precursor_mz=s1_prec_mz,
    precursor_charge=s1_charge,
    adduct=s1_adduct,"
- [intro] Compound objects link spectral data to molecular structure for modification-site localization.: "ModiFinder is a tool for site localization of structural modifications using MS/MS data."
