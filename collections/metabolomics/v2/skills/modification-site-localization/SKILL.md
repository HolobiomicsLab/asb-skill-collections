---
name: modification-site-localization
description: Use when you have a pair of MS/MS spectra—one from a known compound and one from a structurally related modified (unknown) compound—and need to identify which atom(s) in the structure carry the modification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - ModiFinder
  - Python
  - RDKit
  - matplotlib
  - GNPS
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

# modification-site-localization

## Summary

Localize structural modification sites on unknown compounds by aligning tandem mass spectra and fragmentation patterns between a known reference compound and its modified counterpart. ModiFinder computes per-atom modification site probabilities through cosine spectral alignment and fragment annotation, enabling investigators to pinpoint which atoms bear the chemical modification.

## When to use

You have a pair of MS/MS spectra—one from a known compound and one from a structurally related modified (unknown) compound—and need to identify which atom(s) in the structure carry the modification. Use this skill when chemical derivatization, post-translational modification, or in-source fragmentation has altered a known metabolite but you lack independent structural confirmation.

## When NOT to use

- The spectra are from unrelated compounds or lack sufficient spectral overlap; cosine alignment requires substantial shared fragmentations to generate meaningful probabilities.
- The modification is unknown and multiple atoms are plausible candidates, but no MS/MS spectrum from the modified compound is available.
- Precursor m/z values are missing or spectra are severely noisy (signal-to-noise ratio < 3); ModiFinder relies on reliable peak detection and mass accuracy.

## Inputs

- known_compound_spectrum (list of [mz, intensity] pairs)
- known_compound_precursor_mz (float)
- known_compound_precursor_charge (int)
- known_compound_adduct (string, e.g. '[M+H]+', '[M-H]-')
- known_compound_smiles (string)
- modified_compound_spectrum (list of [mz, intensity] pairs)
- modified_compound_precursor_mz (float)
- modified_compound_precursor_charge (int)
- modified_compound_adduct (string)
- modified_compound_smiles (string, optional)

## Outputs

- per_atom_modification_probabilities (numpy array or list with atom indices and probability values)
- matched_peaks_dictionary (mapping of aligned peaks between known and modified spectra)
- fragment_annotation_object (fragmentation assignments for known compound)

## How to apply

Instantiate Compound objects for both the known and modified compounds by supplying their MS/MS peak lists (formatted as [[mz, intensity], ...]), precursor m/z, charge state, adduct type, and SMILES strings (SMILES optional for the modified compound). Pass both Compound objects to a ModiFinder instance configured with a CosineAlignmentEngine (default: mz_tolerance=0.01, ppm_tolerance=40, normalize_peaks=True, ratio_to_base_peak=0.01) and MAGMaAnnotationEngine to align the spectra and annotate fragments. Call generate_probabilities() to compute per-atom modification site scores; the output is a numpy array or list mapping atom indices to probability values, which should be serialized to JSON or CSV for interpretation. Higher probability values indicate atoms more consistent with fragmentation differences between the known and modified compounds.

## Related tools

- **ModiFinder** (Computes per-atom modification site probabilities by tandem mass spectral alignment and MAGMa fragment annotation) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **RDKit** (Enables structural manipulation, SMILES parsing, and molecular visualization for annotation of identified modification sites) — http://www.rdkit.org/
- **matplotlib** (Visualizes per-atom probability heatmaps and spectral alignment results) — http://matplotlib.org/
- **GNPS** (Public repository from which known compound spectra and metadata are retrieved via accession identifiers)

## Examples

```
main_compound = Compound(spectrum=s1_peaks, precursor_mz=s1_prec_mz, precursor_charge=s1_charge, adduct='[M+H]+', smiles=s1_smiles); mod_compound = Compound(spectrum=s2_peaks, precursor_mz=s2_prec_mz, precursor_charge=s2_charge, adduct='[M+H]+', smiles=s2_smiles); siteLocator = ModiFinder(main_compound, mod_compound); peaksObj, fragmentsObj = siteLocator.get_result()
```

## Evaluation signals

- Per-atom probability array contains values in the range [0, 1] with no NaNs; the sum of probabilities is distributed across structurally plausible modification sites (e.g., hydroxyl, amine, or carboxylic acid groups).
- Matched peaks count is > 10% of the smaller spectrum's peak count, indicating sufficient spectral overlap for reliable alignment (cosine similarity typically > 0.5).
- Fragmentation annotations (MAGMa) correctly assign molecular formulas to the top N peaks, validating that fragment m/z values are chemically consistent with the proposed structure.
- Manual visual inspection of the molecule image overlaid with probability colors confirms that high-probability atoms are chemically reasonable (e.g., on functional groups known to undergo the suspected modification).
- Reproducibility: re-running the same Compound pair and ModiFinder parameters yields identical probability arrays (numpy reproducibility controlled via random seed if stochasticity is present).

## Limitations

- ModiFinder requires both a known reference spectrum and a modified compound spectrum; it cannot predict modification sites de novo from an MS/MS alone.
- Probabilities are relative and reflect alignment confidence, not absolute likelihood; chemical validation (NMR, MS/MS fragmentation interpretation) remains necessary.
- Performance degrades when the known and modified compounds share few or very weak peaks, or when multiple structural isomers are plausible; ambiguous results should be cross-validated against orthogonal data.
- The method assumes the modification is a single event; multiply-modified compounds may yield confounded probabilities if fragmentation patterns overlap.
- SMILES string quality and chemical validity are critical; incorrect SMILES will propagate through RDKit visualization and fragment annotation, leading to misleading probability assignments.

## Evidence

- [other] ModiFinder generates per-atom modification site probabilities through tandem mass spectral alignment, enabling structural modification site localization.: "ModiFinder generates per-atom modification site probabilities through tandem mass spectral alignment, enabling structural modification site localization."
- [other] Instantiate a ModiFinder object with the known compound, modified compound, and default CosineAlignmentEngine and MAGMaAnnotationEngine. Call generate_probabilities() on the ModiFinder instance to compute per-atom modification site scores based on spectral alignment and fragmentation annotation.: "Instantiate a ModiFinder object with the known compound, modified compound, and default CosineAlignmentEngine and MAGMaAnnotationEngine. Call generate_probabilities() on the ModiFinder instance to"
- [other] Retrieve the known and modified compounds from GNPS using their accession identifiers via the Compound class constructor, applying default preprocessing (mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True).: "Retrieve the known and modified compounds from GNPS using their accession identifiers via the Compound class constructor, applying default preprocessing (mz_tolerance=0.01, ppm_tolerance=40,"
- [other] Serialize the probability array (numpy array or list) to a JSON or CSV file with atom indices and corresponding probability values.: "Serialize the probability array (numpy array or list) to a JSON or CSV file with atom indices and corresponding probability values."
- [intro] ModiFinder is a tool for site localization of structural modifications using MS/MS data.: "ModiFinder is a tool for site localization of structural modifications using MS/MS data."
- [readme] Pass these to a ModiFinder Object... Collect dictionary results: peaksObj, fragmentsObj = siteLocator.get_result(): "Pass these to a ModiFinder Object... Collect dictionary results: peaksObj, fragmentsObj = siteLocator.get_result()"
