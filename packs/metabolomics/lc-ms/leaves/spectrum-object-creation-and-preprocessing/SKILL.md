---
name: spectrum-object-creation-and-preprocessing
description: Use when when you have raw tandem mass spectrometry peak data (m/z and intensity pairs), precursor m/z, charge state, and adduct annotation for one or more compounds, and need to construct normalized spectrum objects suitable for downstream spectral alignment, modification site prediction, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ModiFinder
  - Python
  - RDKit
  - matplotlib
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00061
  all_source_dois:
  - 10.1021/jasms.4c00061
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-object-creation-and-preprocessing

## Summary

Create and preprocess mass spectrometry spectrum objects from raw peak data and metadata, applying standardized normalization and filtering to prepare inputs for comparative structural analysis. This skill is essential for building reproducible, comparable spectra objects required by alignment and annotation engines like ModiFinder.

## When to use

When you have raw tandem mass spectrometry peak data (m/z and intensity pairs), precursor m/z, charge state, and adduct annotation for one or more compounds, and need to construct normalized spectrum objects suitable for downstream spectral alignment, modification site prediction, or fragmentation annotation. Specifically, apply this skill before invoking ModiFinder's comparative analysis or when building reproducible datasets from GNPS accessions.

## When NOT to use

- Input is already a Compound or Spectrum object from a prior workflow step — reuse directly without re-instantiation.
- Peak data lack accurate precursor m/z or charge state annotation — ModiFinder requires these for fragmentation annotation.
- SMILES or chemical structure is unavailable and structure-aware fragmentation mapping is required downstream.

## Inputs

- Peak list (array of [m/z, intensity] pairs)
- Precursor m/z (float)
- Precursor charge (integer)
- Adduct annotation (string, e.g., '[M+H]+', '[M-H]-')
- SMILES string (optional for modified compound)

## Outputs

- Compound object (Python object encapsulating spectrum and structure)
- Normalized spectrum with intensity normalized to base peak
- Filtered peak list (low-intensity peaks removed if filtering applied)

## How to apply

Instantiate a Compound object by supplying peak data (formatted as [[mz, intensity], ...]), precursor m/z, charge state, adduct string, and SMILES structure. Apply ModiFinder's default preprocessing parameters during construction: mz_tolerance=0.01 Da, ppm_tolerance=40 ppm for mass accuracy, ratio_to_base_peak=0.01 to filter weak peaks, and normalize_peaks=True to scale intensities to the base peak. If working with multiple spectra or real-world data, call normalize() and optionally remove_small_peaks() or keep_top_k() filter steps to reduce noise and standardize intensity distributions. The resulting Compound object encapsulates both the spectral data and chemical structure, enabling comparison and annotation in downstream ModiFinder workflows.

## Related tools

- **ModiFinder** (Provides Compound class constructor and default preprocessing parameters (mz_tolerance, ppm_tolerance, ratio_to_base_peak, normalize_peaks) for standardized spectrum object creation) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **RDKit** (Parses and validates SMILES strings during Compound instantiation for structure representation) — http://www.rdkit.org/
- **Python** (Required runtime environment for Compound class instantiation and preprocessing operations)

## Examples

```
main_compound = Compound(spectrum=[[100.0, 50], [200.5, 100], [300.3, 45]], precursor_mz=450.2, precursor_charge=1, adduct='[M+H]+', smiles='CC(=O)Nc1ccccc1'); mod_compound = Compound(spectrum=[[100.0, 48], [200.5, 102], [315.4, 90]], precursor_mz=480.1, precursor_charge=1, adduct='[M+H]+')
```

## Evaluation signals

- Compound object successfully instantiated with no parsing or validation errors for peak list, precursor m/z, charge, and SMILES.
- Intensity values after normalize_peaks=True application are in range [0, 1.0] with maximum intensity equal to 1.0 (base peak normalization).
- Peak count after filtering (if applied) is ≤ peak count before filtering; no negative or zero intensities remain.
- Precursor m/z and charge state are consistent with input metadata and do not trigger mass accuracy warnings (within ±40 ppm tolerance).
- SMILES parses without error and RDKit generates a valid molecular graph with expected atom and bond counts.

## Limitations

- SMILES structure is optional for the modified compound; without it, atom-level fragmentation annotation cannot be performed in downstream ModiFinder steps.
- Default preprocessing parameters (mz_tolerance=0.01, ratio_to_base_peak=0.01) are optimized for small molecules with single precursor species; high-mass or multiply charged ions may require parameter tuning.
- Peak data must be pre-sorted or will be sorted internally; unsorted input may yield unpredictable behavior in alignment algorithms.
- Adduct annotation must match GNPS or standard notation (e.g., '[M+H]+') for proper charge and mass calculations; non-standard formats may be silently ignored or misinterpreted.

## Evidence

- [other] Retrieve the known and modified compounds from GNPS using their accession identifiers via the Compound class constructor, applying default preprocessing (mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True).: "Compound class constructor, applying default preprocessing (mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True)"
- [readme] ModiFinder requires two spectrum objects with specific formatting: Compound(spectrum=[[mz, int], ...], precursor_mz=Float, precursor_charge=Int, adduct=Str, smiles=Str): "spectrum=s1_peaks, # Formatted as [[mz, int], ...]; precursor_mz=s1_prec_mz, # Float; precursor_charge=s1_charge, # Int; adduct=s1_adduct, # Str; smiles=s1_smiles"
- [readme] ModiFinder includes several useful utility functions for normalization and filtering of spectral data.: "ModiFinder includes several useful utility functions for mass spectrometry data analysis and visualization"
- [other] Normalize peaks to standardize intensity distributions across spectra.: "spectrum.normalize(); Spectrum.normalize_peaks()"
- [other] Filter spectra by precursor mass range to isolate compounds of interest.: "filtered = df[(df['precursor_mz'] >= 200) & (df['precursor_mz'] <= 500)]"
