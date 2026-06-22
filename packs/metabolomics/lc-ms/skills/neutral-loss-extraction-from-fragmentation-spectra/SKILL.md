---
name: neutral-loss-extraction-from-fragmentation-spectra
description: Use when preparing MS/MS spectra for bag-of-fragments conversion and LDA-based motif discovery. You have raw spectra in supported formats (.mgf, .mzML, or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2LDA
  - Python
  - Conda
  techniques:
  - LC-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- Invoke the main script `ms2lda_runfull.py` with your arguments
- configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- Configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- These steps assume you have [Conda](http://conda.io/) installed.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda_cq
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neutral-loss-extraction-from-fragmentation-spectra

## Summary

Extract neutral loss values from tandem mass spectrometry spectra by computing mass differences between precursor ions and observed fragment ions. This is a critical preprocessing step in MS2LDA that converts raw fragmentation patterns into discrete structural tokens for downstream topic modeling.

## When to use

Apply this skill when preparing MS/MS spectra for bag-of-fragments conversion and LDA-based motif discovery. You have raw spectra in supported formats (.mgf, .mzML, or .msp) with both precursor mass and fragment ion m/z values, and you need to extract the neutral mass losses that characterize fragmentation pathways before aggregating into a corpus for topic modeling.

## When NOT to use

- Input spectra lack precursor m/z information or are already in processed/centroided formats where fragment assignments are ambiguous.
- Analysis goal is to preserve raw m/z fingerprints for library matching; neutral loss extraction is appropriate only for unsupervised motif discovery, not for spectral similarity scoring.
- Spectra are from instruments with poor mass accuracy (>100 ppm) where neutral loss computation becomes unreliable.

## Inputs

- MS/MS spectra in .mgf, .mzML, or .msp format
- Precursor m/z values
- Fragment ion m/z values and intensities
- Ionization mode (positive or negative)

## Outputs

- Neutral loss values paired with intensities
- Neutral loss tokens for bag-of-fragments representation
- Processed spectrum objects with neutral losses embedded

## How to apply

For each spectrum, compute the mass difference between the precursor m/z and each observed fragment ion m/z, accounting for ionization mode (positive or negative). These differences represent neutral losses—molecules shed during fragmentation—and encode structural information about the parent compound. Store neutral loss values alongside their corresponding intensities as discrete tokens. The rationale is that recurring neutral losses across many spectra reveal common functional groups or structural motifs; by extracting them explicitly rather than using raw m/z values, the subsequent LDA step can identify which fragmentation patterns co-occur and thus infer the latent substructures driving the observed spectral dataset.

## Related tools

- **MS2LDA** (Container framework; the Preprocessing.load_and_clean module ingests spectra and the extract neutral loss operation feeds into generate_corpus for LDA modeling) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Scripting language for implementing neutral loss computation logic)
- **Conda** (Environment manager for installing MS2LDA and Python dependencies)

## Examples

```
from ms2lda.Preprocessing import load_and_clean; spectra = load_and_clean('sample.mgf', ionization_mode='positive'); neutral_losses = [precursor_mz - frag_mz for frag_mz in spectrum.fragment_ions for spectrum in spectra]
```

## Evaluation signals

- Neutral loss values are consistent with known fragmentation chemistry (e.g., 18.0106 for H₂O, 44.0262 for CO₂, 28.0106 for CO) and fall within expected mass ranges for common losses.
- Neutral loss intensities are non-negative and scale with the corresponding fragment ion intensities; no negative or NaN values present.
- Neutral loss distribution is ionization-mode-specific: positive ion mode spectra show characteristic losses (e.g., H₂O from alcohols, NH₃ from amines); negative mode spectra show corresponding but distinct patterns.
- Downstream bag-of-fragments corpus contains neutral loss tokens alongside fragment ion m/z tokens; vocabulary size and token counts match expected input cardinality for LDA model.
- Mass error (difference between computed neutral loss and theoretical loss) is within instrument calibration tolerance (typically ±5 ppm or ±0.01 Da for high-resolution MS).

## Limitations

- Neutral loss extraction assumes accurate precursor m/z assignment; if precursor mass is misassigned, all neutral losses for that spectrum become incorrect.
- Low-intensity fragments or noise peaks may be incorrectly interpreted as real fragment ions, leading to spurious neutral losses; preprocessing filtering (noise removal) must precede or accompany neutral loss extraction.
- Multiple fragmentation pathways from the same precursor can produce identical neutral loss values, conflating distinct structural features; the bag-of-fragments representation inherently loses the ordered sequence of fragmentations.
- Protonated [M+H]⁺ or deprotonated [M−H]⁻ species must be correctly identified; wrong ionization mode assignment propagates errors through all neutral loss calculations.

## Evidence

- [other] Extract neutral loss values from each spectrum by computing differences between precursor mass and observed fragment ions.: "Extract neutral loss values from each spectrum by computing differences between precursor mass and observed fragment ions."
- [other] Convert filtered spectra into bag-of-fragments format, aggregating fragment ions and neutral losses as discrete tokens with their intensities.: "Convert filtered spectra into bag-of-fragments format, aggregating fragment ions and neutral losses as discrete tokens with their intensities."
- [other] Apply ionization-mode-specific filtering to handle positive and negative ion mode data separately, removing low-intensity noise peaks and m/z artifacts.: "Apply ionization-mode-specific filtering to handle positive and negative ion mode data separately, removing low-intensity noise peaks and m/z artifacts."
- [readme] MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data.: "MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data."
- [other] Extract neutral losses: "Extract neutral losses"
