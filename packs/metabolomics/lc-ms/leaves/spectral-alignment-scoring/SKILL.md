---
name: spectral-alignment-scoring
description: Use when you have paired MS/MS spectra (known compound and its structural
  analog) with assigned precursor m/z, charge, and SMILES; you want to quantify which
  parts of the molecular structure could have undergone modification by scoring peak
  alignment quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
  tools:
  - ModiFinder
  - BasicEvaluationEngine
  - Python
  - RDKit
  - matplotlib
  - Pillow
  - GNPS
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.4c00061
  title: ModiFinder
evidence_spans:
- mf = ModiFinder(known_compound, modified_compound, mz_tolerance=0.01, ppm_tolerance=40)
- mf = ModiFinder(known_compound, modified_compound, helpers=helpers_array, **args)
- eval_engine = BasicEvaluationEngine(default_method="is_max")
- eval_engine = BasicEvaluationEngine(default_method="average_distance")
- ModiFinder requires Python 3.9 or above.
- ModiFinder requires Python 3.9 or above
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

# spectral-alignment-scoring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute alignment similarity scores between known and modified compound MS/MS spectra using cosine-based metrics and fragment annotation engines. This skill quantifies how well peak-to-fragment mappings align across spectra, enabling probabilistic localization of structural modification sites.

## When to use

You have paired MS/MS spectra (known compound and its structural analog) with assigned precursor m/z, charge, and SMILES; you want to quantify which parts of the molecular structure could have undergone modification by scoring peak alignment quality. Use this when you need to prioritize or evaluate candidate modification sites before or after annotation refinement.

## When NOT to use

- Input spectrum has not been normalized or has not been filtered for low-intensity noise (ratio_to_base_peak threshold); use remove_small_peaks() or normalize_peaks() first.
- Modified compound structure is completely unknown and oracle-mode refinement is not an option; fall back to de novo annotation or orthogonal fragmentation prediction.
- Precursor m/z or charge assignment is uncertain or known to be incorrect; alignment scores will be meaningless.

## Inputs

- Compound object (known structure): spectrum (peak list as [[mz, intensity], ...]), precursor_mz, precursor_charge, adduct, SMILES
- Compound object (modified analog): spectrum, precursor_mz, precursor_charge, adduct, SMILES (optional at input; can be added later)
- Alignment engine configuration: method (e.g., 'Modified Cosine'), tolerances (mz_tolerance, ppm_tolerance, ratio_to_base_peak)
- Annotation engine configuration: engine type (e.g., MAGMaAnnotationEngine), parameters (e.g., breaks=3)

## Outputs

- Modification site probability vector: float array of per-atom or per-bond modification likelihood scores
- Alignment score (is_max): binary indicator (0 or 1) whether the highest-probability site matches ground truth
- Alignment score (average_distance): float in [0, 1] measuring mean distance from predicted to known modification sites
- Refined peak-to-fragment mappings: updated dictionary mapping m/z peaks to fragment identities after annotation refinement
- Visualization: annotated molecule diagram highlighting predicted modification site(s) and confidence scores

## How to apply

Load both compounds from GNPS (or local spectra) using standardized tolerances (mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True). Instantiate a ModiFinder object with a CosineAlignmentEngine (or alternative alignment method) and an annotation engine such as MAGMaAnnotationEngine (breaks=3). Call generate_probabilities() to compute modification site probability scores by aligning peaks and propagating fragment annotations. If structure is available for the modified compound, set is_known=True and call re_annotate() to refine annotations using oracle-mode structural constraints before re-generating probabilities. Output probability vectors and alignment scores capture which bonds or atoms are most likely modified.

## Related tools

- **ModiFinder** (Core package providing CosineAlignmentEngine, MAGMaAnnotationEngine, and Compound/spectrum data structures to compute alignment scores and modification site probabilities) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **BasicEvaluationEngine** (Evaluation framework for scoring alignment results using metrics (is_max, average_distance) against known modification sites) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **RDKit** (Molecular structure parsing, SMILES canonicalization, bond/atom enumeration for mapping probabilities to chemical features) — http://www.rdkit.org/
- **Python** (Programming language for scripting ModiFinder workflows and data I/O)
- **GNPS** (Data source for fetching known compound spectra and metadata via accession identifiers) — https://gnps.ucsd.edu/

## Examples

```
siteLocator = ModiFinder(main_compound, mod_compound); peaksObj, fragmentsObj = siteLocator.get_result(); engine = BasicEvaluationEngine(default_method='average_distance'); is_max_score = engine.evaluate_single(fragmentsObj['structure'], target_structure, probabilities, evaluation_method='is_max'); avg_dist = engine.evaluate_single(fragmentsObj['structure'], target_structure, probabilities, evaluation_method='average_distance')
```

## Evaluation signals

- Probability vector is_max score equals 1.0 for known modification sites (perfect localization); average_distance ≤ 0.5 indicates good site proximity (ModiFinder reports is_max=1.0, average_distance=0.514 under standard conditions).
- Alignment score improves (is_max increases, average_distance decreases) after oracle-mode re_annotate() using refined structural constraints.
- Probability values sum to 1.0 (or follow expected normalization) across all candidate sites; no NaN or infinite values in output vector.
- Visualization diagram correctly highlights modification site atoms/bonds with numeric confidence scores; layout and atom labels match input SMILES.
- Peak-to-fragment mapping remains consistent between baseline and refined runs; matched peak counts should increase or remain stable after refinement.

## Limitations

- Alignment scores assume precursor mass and charge are correct; misassignment cascades to all downstream predictions.
- Performance depends on annotation engine quality (e.g., MAGMa may fail to identify rare or non-standard fragments); incomplete fragmentation libraries reduce site localization precision.
- Oracle-mode refinement (re_annotate()) requires the modified compound structure to be known; unavailable for truly unknown analogs.
- Tolerance parameters (mz_tolerance=0.01, ppm_tolerance=40) are fixed defaults; suboptimal for very low-resolution or high-mass spectra.
- Score interpretation assumes one dominant modification site; multiple simultaneous modifications may produce ambiguous probability distributions.

## Evidence

- [other] ModiFinder achieves BasicEvaluationEngine scores of is_max = 1.0 and average_distance = 0.514 under the default Modified Cosine + MAGMa condition.: "ModiFinder achieves BasicEvaluationEngine scores of is_max = 1.0 and average_distance = 0.514 under the default Modified Cosine + MAGMa condition."
- [other] Load known and modified compounds with specified tolerances and create ModiFinder instance with CosineAlignmentEngine and MAGMaAnnotationEngine; generate modification site probabilities via mf.generate_probabilities().: "Load known compound and modified compound from GNPS with mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True. Create ModiFinder instance with CosineAlignmentEngine and"
- [other] Instantiate BasicEvaluationEngine with default_method and call evaluate_single to compute scores.: "Instantiate BasicEvaluationEngine with default_method='average_distance'. Call evaluate_single(analog_structure, target_structure, probabilities) to compute average_distance score; call again with"
- [other] ModiFinder provides spectrum utilities and molecule utilities that work seamlessly with core functionality to process MS data.: "ModiFinder provides spectrum utilities (Create consensus spectra, refine spectra, handle adducts) and molecule utilities (Calculate edit distances, find modification sites, analyze transitions) that"
- [other] Set is_known flag on modified compound and call re_annotate() to propagate structural constraints; re-generate modification probability scores using generate_probabilities() on the updated network.: "Set the is_known flag on the modified compound to True to signal that its structure is now available for annotation refinement. Call the re_annotate() method on the ModiFinder network using the"
