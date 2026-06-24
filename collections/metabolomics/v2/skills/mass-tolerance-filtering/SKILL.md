---
name: mass-tolerance-filtering
description: Use when when you have observed fragment peak m/z values from tandem
  mass spectra and need to assign chemical subformulae to them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
  tools:
  - SIRIUS
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS
  fragmentation trees)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf_cq
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-tolerance-filtering

## Summary

Filter candidate chemical subformulae for fragment peaks by accepting only those whose theoretical m/z values fall within a specified mass tolerance window of the observed peak m/z. This is a data-preprocessing step that constrains the chemical formula space before applying validity filters and scoring.

## When to use

When you have observed fragment peak m/z values from tandem mass spectra and need to assign chemical subformulae to them. Apply this skill as the first filtering stage to enumerate all candidate formulas whose theoretical masses match the observed peak mass within instrument accuracy bounds, before applying chemical validity constraints or machine-learning scoring.

## When NOT to use

- Input fragment peaks have already been pre-filtered by mass tolerance (redundant application).
- You are working with low-resolution MS data (e.g., <1 Da accuracy) where mass tolerance filtering may be too permissive to meaningfully constrain the formula space.
- You do not have a reliable estimate of instrument mass accuracy; in this case, validate tolerance via a calibration set before applying it systematically.

## Inputs

- observed fragment peak list with m/z values and intensities
- enumerated chemical subformula candidates (with theoretical m/z)
- mass tolerance threshold (in ppm or Da)

## Outputs

- filtered candidate chemical subformulae per peak (those within mass tolerance)
- peak-to-formula mapping table (pre-scoring)

## How to apply

For each observed fragment peak (m/z value and intensity), compute the theoretical m/z for all possible chemical subformulae in a predefined chemical space (typically generated via dynamic programming enumeration). Retain only those candidate subformulae whose theoretical m/z lies within a specified ppm or Da tolerance window centered on the observed peak m/z. The tolerance window should reflect the mass accuracy of the measurement instrument; typical values range from 5–10 ppm for high-resolution data. This filtered candidate list becomes the input to downstream chemical validity and energy-based scoring stages. Mass tolerance filtering dramatically reduces the computational burden of subsequent ranking steps while maintaining high recall of correct formulas.

## Related tools

- **SIRIUS** (Provides dynamic programming algorithm (SIRIUS decomp) for enumerating all valid chemical subformulae for a given neutral mass; those enumerated candidates are then filtered by mass tolerance) — https://bio.informatik.uni-jena.de/software/sirius/

## Evaluation signals

- Verify that all retained candidates have theoretical m/z within the specified tolerance of the observed peak m/z (no false positives).
- Confirm that the correct chemical formula (from reference library or manual annotation) is retained in the filtered candidate list (recall = 1.0 for ground truth).
- Check that the number of candidate formulas per peak is reduced by a factor of 10–100× compared to the unfiltered enumeration, demonstrating computational filtering efficacy.
- Validate that downstream scoring/ranking steps show improved precision and reduced runtime when operating on mass-tolerance-filtered candidates vs. unfiltered.
- Compare mass tolerance window size (ppm or Da) against instrument calibration accuracy; tolerance should be 2–3× the typical calibration error to avoid false negatives.

## Limitations

- Mass tolerance filtering assumes accurate m/z calibration of the mass spectrometer; miscalibration can lead to systematic exclusion of correct formulas or spurious inclusion of false candidates.
- Performance degrades on low-resolution or low mass-accuracy data (e.g., quadrupole instruments or unit-resolution ToF), where a single m/z value may correspond to many valid formulas even after tolerance filtering.
- The choice of tolerance threshold (ppm vs. Da) affects filtering stringency; ppm-based tolerances are more conservative at low m/z, while Da-based tolerances are uniform across the mass range. No single threshold is optimal for all mass ranges.
- For very small molecules or fragment peaks at very low m/z (<100), tolerance windows may become too narrow, increasing the risk of excluding correct formulas due to rounding or calibration drift.

## Evidence

- [other] For each fragment peak, enumerate all valid chemical subformulae within the mass tolerance window.: "For each fragment peak, enumerate all valid chemical subformulae within the mass tolerance window."
- [other] Apply chemical validity constraints (valence rules, atom count limits) to filter candidates.: "Apply chemical validity constraints (valence rules, atom count limits) to filter candidates."
- [readme] To list out all potential formulae for an observed MS1 mass, we utilize the dynamic programming algorithm implemented by SIRIUS, `SIRIUS decomp`: "To list out all potential formulae for an observed MS1 mass, we utilize the dynamic programming algorithm implemented by SIRIUS, `SIRIUS decomp`"
