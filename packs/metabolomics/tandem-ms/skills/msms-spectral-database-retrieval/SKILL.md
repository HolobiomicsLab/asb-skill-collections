---
name: msms-spectral-database-retrieval
description: Use when when you have a target compound (modified or unmodified) and need to obtain its experimental MS/MS spectrum and metadata to serve as a known reference for ModiFinder analysis, or when benchmarking evaluation methods like average_distance scoring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ModiFinder
  - Python
  - BasicEvaluationEngine
  - GNPS
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/jasms.4c00061
  title: ModiFinder
evidence_spans:
- mf = ModiFinder(known_compound, modified_compound, mz_tolerance=0.01, ppm_tolerance=40)
- mf = ModiFinder(known_compound, modified_compound, helpers=helpers_array, **args)
- ModiFinder requires Python 3.9 or above.
- ModiFinder requires Python 3.9 or above
- eval_engine = BasicEvaluationEngine(default_method="is_max")
- eval_engine = BasicEvaluationEngine(default_method="average_distance")
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msms-spectral-database-retrieval

## Summary

Retrieve experimental tandem mass spectra and metadata for known compounds from public MS/MS databases (e.g., GNPS-LIBRARY) to establish reference spectra for structural modification site localization and comparative spectral analysis.

## When to use

When you have a target compound (modified or unmodified) and need to obtain its experimental MS/MS spectrum and metadata to serve as a known reference for ModiFinder analysis, or when benchmarking evaluation methods like average_distance scoring. This is the first step in comparative spectral workflows where you require authentic spectral data rather than in silico predictions.

## When NOT to use

- The compound is not in any public MS/MS database and you must use in silico prediction or custom experimental data instead.
- You require MS/MS spectra for rare isotopologues, unusual adducts, or non-standard ionization modes not covered by GNPS-LIBRARY.
- Your analysis workflow uses only high-resolution intact mass without fragmentation data (MS1-only comparison).

## Inputs

- compound accession identifier (string, e.g., CCMSLIB00010113829)
- MS/MS database URI (GNPS or compatible repository endpoint)

## Outputs

- Compound object (precursor_mz, precursor_charge, adduct, spectrum peaks [[mz, int], ...], SMILES)
- spectrum metadata dict (normalized/raw peak intensities, acquisition parameters)

## How to apply

Query the GNPS-LIBRARY database using compound accession identifiers (e.g., CCMSLIB00010113829) to fetch Compound objects containing spectrum peaks (formatted as [[mz, intensity], ...]), precursor m/z, precursor charge, adduct information, and SMILES notation. Load retrieved spectra into ModiFinder-compatible Compound objects with parameters normalized to your analytical context (e.g., ppm_tolerance=40, mz_tolerance=0.01, ratio_to_base_peak=0.01). Configure normalize_peaks=True during loading to ensure consistent peak intensities across database and experimental spectra. Validate retrieved spectra by confirming precursor mass matches expected molecular weight and that peak counts are consistent with the molecular ion fragmentation profile.

## Related tools

- **GNPS** (public MS/MS spectral library repository from which compound spectra are fetched by accession) — https://gnps.ucsd.edu
- **ModiFinder** (loads retrieved Compound objects and integrates spectral data into site localization workflow) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **Python** (runtime environment for executing ModiFinder API calls to instantiate and load Compound objects)

## Examples

```
from modifinder import Compound; c = Compound.from_gnps('CCMSLIB00010113829', ppm_tolerance=40, mz_tolerance=0.01, normalize_peaks=True)
```

## Evaluation signals

- Retrieved Compound object contains non-empty spectrum peaks list with at least 5 fragments (m/z, intensity pairs).
- Precursor m/z value matches or is within 0.01 Da (or 40 ppm, whichever is stricter) of the expected molecular weight for the compound SMILES.
- Spectrum peaks are in ascending m/z order and intensities are normalized to 0–1 or 0–100 range after normalize_peaks=True.
- SMILES string is valid (parses without error in RDKit) and fragment peaks do not exceed the precursor m/z.
- Metadata fields (precursor_charge, adduct) are non-null and match expected ionization mode for the compound class (e.g., [M+H]+ for protonated lipids).

## Limitations

- GNPS-LIBRARY coverage is incomplete; rare, recently synthesized, or proprietary compounds may not be indexed.
- Spectral data reflect specific analytical conditions (solvent, collision energy, instrument model); transfer to different instrumentation may introduce systematic bias.
- Network connectivity or database maintenance outages will block accession-based retrieval; no offline fallback to cached spectra is provided in the core API.
- SMILES notation in GNPS is optional and may be missing or stereochemically ambiguous; validation against experimental fragmentation is recommended.

## Evidence

- [other] Get compound from GNPS; Draw the molecule: "Fetch and Visualize a Compound workflow step"
- [other] Load the known and modified compounds (CCMSLIB00010113829 and CCMSLIB00010125628) with ModiFinder using ppm_tolerance=40, mz_tolerance=0.01, ratio_to_base_peak=0.01, and normalize_peaks=True.: "Load the known and modified compounds (CCMSLIB00010113829 and CCMSLIB00010125628) with ModiFinder using ppm_tolerance=40, mz_tolerance=0.01, ratio_to_base_peak=0.01, and normalize_peaks=True."
- [abstract] mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00010113829: "Extract Data from GNPS: Fetch data from GNPS accession"
- [readme] ModiFinder requires two spectrum objects: main_compound = Compound(spectrum=s1_peaks, precursor_mz=s1_prec_mz, precursor_charge=s1_charge, adduct=s1_adduct, smiles=s1_smiles): "ModiFinder requires two spectrum objects: main_compound = Compound(spectrum=s1_peaks, precursor_mz=s1_prec_mz, precursor_charge=s1_charge, adduct=s1_adduct, smiles=s1_smiles)"
- [readme] ModiFinder includes several useful utility functions for mass spectrometry data analysis and visualization: "ModiFinder includes several useful utility functions for mass spectrometry data analysis and visualization, exposed under"
