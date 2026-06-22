---
name: compound-structure-comparison-metrics
description: Use when you have two MS/MS spectra from related compounds (e.g., a reference compound and a suspected modified version) and need to quantify where and how their structures differ.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  tools:
  - ModiFinder
  - Python
  - BasicEvaluationEngine
  - RDKit
  techniques:
  - ion-mobility-MS
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

# compound-structure-comparison-metrics

## Summary

Quantitatively compare two related chemical structures (a known compound and a modified analog) by aligning their tandem MS/MS spectra and computing difference metrics to localize structural modification sites. This skill enables systematic evaluation of how spectral fragmentation patterns diverge between compounds, grounding modification hypotheses in observed mass shifts and peak intensity changes.

## When to use

You have two MS/MS spectra from related compounds (e.g., a reference compound and a suspected modified version) and need to quantify where and how their structures differ. Apply this skill when you want to move beyond visual inspection to produce reproducible, numerical evidence of modification site(s) — for instance, to validate hypotheses about post-translational modifications, biotransformations, or synthetic analogs before running site-localization algorithms.

## When NOT to use

- Spectra have not been normalized or are missing key metadata (precursor m/z, charge, adduct); use spectrum.normalize() and validate metadata first.
- Comparing unrelated compounds or compounds differing by more than one modification site; comparison metrics assume localized structural change.
- Input spectra are in raw or unfiltered form with very low-intensity noise; apply peak filtering (remove_small_peaks, keep_top_k) before comparison.

## Inputs

- Compound object for known/reference structure (with spectrum as [[mz, int], ...], precursor_mz, precursor_charge, adduct, smiles)
- Compound object for modified/analog structure (with same spectrum format and metadata)
- Precomputed probability array from ModiFinder.generate_probabilities()
- MS parameters: ppm_tolerance (float), mz_tolerance (float), ratio_to_base_peak (float), normalize_peaks (bool)

## Outputs

- Numerical evaluation score (float, range 0–1) quantifying structural similarity
- Aligned peak correspondence between known and modified spectra
- Fragment attribution map indicating which peaks correspond to which molecular bonds/sites

## How to apply

Load both compounds (known and modified) into ModiFinder Compound objects with normalized peaks (normalize_peaks=True) and consistent MS parameters (ppm_tolerance=40, mz_tolerance=0.01, ratio_to_base_peak=0.01). Instantiate an evaluation engine (e.g., BasicEvaluationEngine) with a distance metric such as average_distance. Call evaluate_single() passing the reference structure, target structure, and precomputed probabilities to obtain a numerical alignment score (e.g., 0.514 for full match). Scores closer to 1.0 indicate stronger structural similarity; scores diverge when modifications introduce new fragmentations or eliminate expected peaks. Document the returned score and compare it against reference values to confirm the magnitude and location of structural divergence.

## Related tools

- **ModiFinder** (Primary tool for spectrum alignment, compound loading, and evaluation engine instantiation; provides utilities for normalized spectrum comparison and fragment mapping.) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **BasicEvaluationEngine** (Computes distance-based structural similarity metrics (e.g., average_distance) between aligned spectra; returns numerical score for structural divergence quantification.) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **Python** (Required runtime environment (≥3.9) for executing ModiFinder API and evaluation workflows.)
- **RDKit** (Underlying chemistry and molecular structure representation; used by ModiFinder for SMILES parsing and molecular visualization.) — http://www.rdkit.org/

## Examples

```
```python
from modifinder import Compound, ModiFinder, BasicEvaluationEngine

main_compound = Compound(spectrum=s1_peaks, precursor_mz=500.1, precursor_charge=1, adduct='[M+H]+', smiles='CCO')
mod_compound = Compound(spectrum=s2_peaks, precursor_mz=516.1, precursor_charge=1, adduct='[M+H]+', smiles='CCO')

siteLocator = ModiFinder(main_compound, mod_compound, ppm_tolerance=40, mz_tolerance=0.01, ratio_to_base_peak=0.01, normalize_peaks=True)
probs = siteLocator.generate_probabilities()

evaluator = BasicEvaluationEngine(default_method='average_distance')
score = evaluator.evaluate_single(main_compound.structure, mod_compound.structure, probs)
print(f'Structural similarity score: {score}')
```
```

## Evaluation signals

- Returned evaluation score falls within expected range (0–1) and is reproducible across repeated runs with identical input compounds and parameters.
- Score value aligns with visual inspection: higher scores (>0.7) for structurally similar compounds, lower scores (<0.4) when modifications introduce large m/z shifts or eliminate major fragment peaks.
- Fragment alignment table shows one-to-one correspondence for unmodified regions and divergence (missing or shifted peaks) at the modification site(s).
- Score matches or closely approximates reference benchmark values (e.g., 0.514) reported in literature or validation datasets when using identical SMILES, spectra, and parameters.
- Difference in fragment abundance matches predicted changes in molecular weight at the modification site (e.g., +15 Da for methylation, +16 Da for oxidation).

## Limitations

- Evaluation assumes the two compounds differ by a single, localized structural modification; multiple sites or large rearrangements may produce ambiguous scores.
- Metric sensitivity depends on normalized peak intensity thresholds (ratio_to_base_peak=0.01) and m/z tolerance windows (ppm_tolerance=40, mz_tolerance=0.01); suboptimal choices can mask or artificially amplify apparent differences.
- SMILES string accuracy is critical; incorrect or missing SMILES for either compound will propagate into fragment assignment and alignment scoring.
- Evaluation does not distinguish between isomeric modifications that produce identical m/z fragmentation patterns; additional orthogonal data (e.g., retention time, ion mobility) may be needed.
- Tool is designed for MS/MS (tandem) data; single-stage MS or low-resolution spectra may not provide sufficient fragment information for reliable comparison.

## Evidence

- [other] ModiFinder provides six categories of utilities—network, spectrum, file I/O, formula, molecule, and comparison utilities—that work seamlessly with core functionality and can be used independently for various MS data processing tasks.: "ModiFinder provides six categories of utilities—network, spectrum, file I/O, formula, molecule, and comparison utilities—that work seamlessly with core functionality"
- [other] Initialize ModiFinder with the loaded compounds and generate probabilities via mf.generate_probabilities(). Instantiate BasicEvaluationEngine with default_method='average_distance'. Call evaluate_single() with the analog structure, target structure, and predicted probabilities to obtain the evaluation score.: "Instantiate BasicEvaluationEngine with default_method='average_distance'. Call evaluate_single() with the analog structure, target structure, and predicted probabilities to obtain the evaluation"
- [other] Compare the returned score against the reference value of 0.514 and document the result.: "Compare the returned score against the reference value of 0.514 and document the result."
- [intro] ModiFinder is a tool for site localization of structural modifications using MS/MS data.: "ModiFinder is a tool for site localization of structural modifications using MS/MS data."
- [readme] ModiFinder requires two spectrum objects: main_compound and mod_compound, each initialized with formatted spectrum peaks, precursor_mz, precursor_charge, adduct, and smiles.: "ModiFinder requires two spectrum objects: main_compound = Compound( spectrum=s1_peaks, precursor_mz=s1_prec_mz, precursor_charge=s1_charge, adduct=s1_adduct, smiles=s1_smiles )"
- [readme] Pass compounds to a ModiFinder object and collect dictionary results including matched_peaks, main_compound_peaks, mod_compound_peaks, and precursor m/z values.: "peaksObj = { 'main_compound_peaks': main_compound_peaks, 'mod_compound_peaks': mod_compound_peaks, 'matched_peaks': matched_peaks, 'main_precursor_mz': knownCompound.spectrum.precursor_mz,"
