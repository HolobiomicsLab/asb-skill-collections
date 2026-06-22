---
name: mass-spectrometry-spectral-alignment
description: Use when you have a pair of MS/MS spectra—one from a known compound and one from a structurally modified variant of that compound—and you need to identify which atoms in the structure likely bear the modification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ModiFinder
  - Python
  - RDKit
  - matplotlib
  - GNPS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-spectral-alignment

## Summary

Align tandem mass spectra from known and structurally modified compound pairs using cosine similarity and fragmentation annotation to localize per-atom modification sites. This skill enables direct comparison of MS/MS peaks and fragments to generate modification site probability scores.

## When to use

You have a pair of MS/MS spectra—one from a known compound and one from a structurally modified variant of that compound—and you need to identify which atoms in the structure likely bear the modification. Use this skill when you seek site-specific localization rather than bulk modification detection, and when both the known and modified spectra are available for direct comparison.

## When NOT to use

- Input spectra come from unrelated compounds or compound classes; spectral alignment requires structural similarity for meaningful fragment correspondence.
- Only a single spectrum is available (either known or modified compound missing); the skill requires both spectra for comparative alignment.
- The modification site is already known and confirmed by orthogonal methods; this skill is for hypothesis generation and localization, not validation of known sites.

## Inputs

- Known compound: Compound object with MS/MS spectrum (m/z, intensity pairs), precursor m/z, precursor charge, adduct string, SMILES string
- Modified compound: Compound object with MS/MS spectrum (m/z, intensity pairs), precursor m/z, precursor charge, adduct string, optional SMILES string
- Mass spectrometry parameters: mz_tolerance (float, Da), ppm_tolerance (float), ratio_to_base_peak (float, 0–1)

## Outputs

- Per-atom modification site probability array: numpy array or list with atom indices and corresponding probability scores (0–1 range)
- Matched peaks dictionary: pairs of m/z values from known and modified spectra aligned by cosine similarity
- Fragment annotation dictionary: fragmentation map and structural annotations from MAGMa for both compounds

## How to apply

Instantiate Compound objects for both the known and modified structures, supplying their MS/MS peaks (formatted as [mz, intensity] pairs), precursor m/z, charge, adduct, and SMILES strings. Set preprocessing parameters: mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, and normalize_peaks=True. Create a ModiFinder instance with both compounds and default CosineAlignmentEngine and MAGMaAnnotationEngine. Call generate_probabilities() to compute per-atom modification site scores by matching fragments across the two spectra. The alignment identifies fragment ions that differ between the known and modified compounds; fragments containing the modification will show mass shifts. Serialize the resulting probability array (numpy array or list) to JSON or CSV with atom indices and corresponding probability values for downstream interpretation.

## Related tools

- **ModiFinder** (Core library for tandem MS spectral alignment and per-atom modification site probability computation via Modified Cosine engine and MAGMa annotation) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **RDKit** (Molecular structure parsing, SMILES handling, and fragment annotation for alignment) — http://www.rdkit.org/
- **Python** (Runtime environment and scripting language (requires ≥3.9))
- **GNPS** (Data source for retrieving known compound spectra and metadata by accession identifier)

## Examples

```
from modifinder import Compound, ModiFinder
main = Compound(spectrum=known_peaks, precursor_mz=500.1, precursor_charge=1, adduct='[M+H]+', smiles=known_smiles)
mod = Compound(spectrum=mod_peaks, precursor_mz=516.1, precursor_charge=1, adduct='[M+H]+', smiles=mod_smiles)
siteLocator = ModiFinder(main, mod)
peaksObj, fragmentsObj = siteLocator.get_result()
```

## Evaluation signals

- Probability values are in valid range [0, 1] and atom indices correspond to the known compound's molecular graph.
- Matched peaks dictionary contains symmetric pairs of m/z values with mass differences consistent with the expected modification mass (e.g., +15.9949 for oxidation, +79.9663 for sulfonation).
- High-probability atoms cluster on chemically plausible functional groups (e.g., hydroxyl oxygens for oxidation, aliphatic carbons for methylation).
- Serialized output (JSON/CSV) is parseable and preserves all atom indices and probability values without information loss.
- Fragment annotations from MAGMa correctly map theoretical fragments to observed m/z peaks with mass error < specified ppm_tolerance.

## Limitations

- Spectral alignment relies on sufficient fragment redundancy; low-abundance spectra or heavily fragmented compounds may yield ambiguous or low-confidence site predictions.
- The skill assumes the known and modified compounds differ by a single, localized structural modification; multiple independent modifications or rearrangements will produce misleading alignment scores.
- SMILES input for the modified compound is optional but recommended; without it, annotation and structure validation are reduced.
- ModiFinder is under active development; API and output formats may change in future releases.

## Evidence

- [other] ModiFinder generates per-atom modification site probabilities through tandem mass spectral alignment, enabling structural modification site localization.: "ModiFinder generates per-atom modification site probabilities through tandem mass spectral alignment, enabling structural modification site localization."
- [other] Retrieve the known and modified compounds from GNPS using their accession identifiers via the Compound class constructor, applying default preprocessing (mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True).: "Retrieve the known and modified compounds from GNPS using their accession identifiers via the Compound class constructor, applying default preprocessing (mz_tolerance=0.01, ppm_tolerance=40,"
- [other] Instantiate a ModiFinder object with the known compound, modified compound, and default CosineAlignmentEngine and MAGMaAnnotationEngine.: "Instantiate a ModiFinder object with the known compound, modified compound, and default CosineAlignmentEngine and MAGMaAnnotationEngine."
- [other] Call generate_probabilities() on the ModiFinder instance to compute per-atom modification site scores based on spectral alignment and fragmentation annotation.: "Call generate_probabilities() on the ModiFinder instance to compute per-atom modification site scores based on spectral alignment and fragmentation annotation."
- [readme] Pass these to a ModiFinder Object helper_compounds = None siteLocator = ModiFinder(main_compound, mod_compound, helpers=helper_compounds, **args): "Pass these to a ModiFinder Object helper_compounds = None siteLocator = ModiFinder(main_compound, mod_compound, helpers=helper_compounds, **args)"
- [readme] Collect dictionary results: peaksObj, fragmentsObj = siteLocator.get_result(): "Collect dictionary results: peaksObj, fragmentsObj = siteLocator.get_result()"
