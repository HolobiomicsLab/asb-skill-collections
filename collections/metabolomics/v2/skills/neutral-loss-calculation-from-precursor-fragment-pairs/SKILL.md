---
name: neutral-loss-calculation-from-precursor-fragment-pairs
description: Use when during MS/MS spectral preprocessing when converting raw spectra from .mgf, .msp, or .mzML formats into a bag-of-fragments corpus for LDA modeling. Use it after fragment ion masses have been extracted and normalized within each spectrum, and before noise filtering and corpus generation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
  - Python
  - Conda
  - MS2LDA.Preprocessing.generate_corpus
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
- from MS2LDA.Preprocessing import load_and_clean
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
- These steps assume you have Conda installed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
---

# neutral-loss-calculation-from-precursor-fragment-pairs

## Summary

Calculate neutral loss values for all observed fragment ion pairs in a tandem mass spectrum by subtracting fragment masses from the precursor mass. This transforms raw spectral peaks into a richer bag-of-fragments representation that captures both observed ions and the neutral species lost during fragmentation.

## When to use

Apply this skill during MS/MS spectral preprocessing when converting raw spectra from .mgf, .msp, or .mzML formats into a bag-of-fragments corpus for LDA modeling. Use it after fragment ion masses have been extracted and normalized within each spectrum, and before noise filtering and corpus generation.

## When NOT to use

- Spectra without reliable precursor mass annotation or from instruments with poor m/z calibration.
- Data already preprocessed into a document-term matrix or other compacted representation where individual fragments and losses are no longer resolvable.
- Very low-resolution spectra where fragment masses cannot be distinguished from noise with sufficient confidence.

## Inputs

- MS/MS spectra with extracted fragment ion masses (normalized peak intensities)
- precursor mass values (M) for each spectrum
- intensity threshold or statistical significance cutoff for filtering

## Outputs

- neutral loss values (mass differences) for fragment pairs
- filtered neutral loss set (after noise removal)
- bag-of-fragments corpus incorporating both fragments and losses

## How to apply

For each spectrum with a known precursor mass (M), iterate over all observed fragment ion masses and compute neutral loss as the difference M − fragment_mass. Retain neutral loss values that exceed a minimum intensity threshold or statistical significance cutoff (as configured in the filtering step); this prevents spurious losses from noise. Bin the computed losses into discrete mass tokens alongside the original fragments to create the final bag-of-fragments representation. The rationale is that neutral losses encode structural fragmentation logic—recurring loss patterns across spectra indicate common substructures—making them essential features for motif discovery via LDA.

## Related tools

- **MS2LDA.Preprocessing.load_and_clean** (Loads MS/MS spectra from input files and extracts normalized fragment ion masses required as input for neutral loss calculation) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA.Preprocessing.generate_corpus** (Converts calculated neutral losses and fragments into a bag-of-fragments corpus representation suitable for LDA) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Downstream topic modeling framework that uses neutral losses and fragments as input features for Mass2Motif inference) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Programming language for implementing neutral loss calculations within preprocessing workflows)

## Examples

```
from MS2LDA.Preprocessing import load_and_clean, generate_corpus; spectra = load_and_clean('data.mgf'); neutral_losses = [precursor_mass - frag_mass for frag_mass in spectrum.fragment_masses]; corpus = generate_corpus(spectra_with_losses, min_intensity_threshold=10)
```

## Evaluation signals

- All computed neutral loss values are positive and lie within the valid range [0, M] where M is the precursor mass.
- No neutral loss is larger than the precursor mass; if any loss exceeds M, fragment-to-precursor mapping is incorrect.
- The number of retained losses (after filtering) is proportional to spectral complexity; highly fragmented spectra produce more losses than simple spectra, consistent with chemistry.
- Neutral losses align with known fragmentation pathways (e.g., 18 Da for water loss, 44 Da for CO₂ loss) when cross-checked against reference compounds.
- The bag-of-fragments output contains expected cardinality: fragment count + loss count should be reasonable relative to the original peak count and complexity.

## Limitations

- Neutral loss calculation is sensitive to precursor mass accuracy; miscalibration by >5 ppm can introduce systematic errors in loss values, particularly for small fragments.
- Filtering decisions (intensity threshold, statistical cutoff) are user-defined; inappropriate thresholds may discard true losses or retain noise-derived spurious losses.
- High-mass fragments may produce very small neutral losses (<1 Da), which can be indistinguishable from measurement noise and difficult to bin discretely.
- Neutral losses alone do not distinguish isomeric fragments; two different fragmentation pathways yielding the same loss mass will be conflated in the bag-of-fragments representation.

## Evidence

- [methods] Calculate neutral loss values for all observed fragment pairs.: "Calculate neutral loss values for all observed fragment pairs."
- [methods] Extract fragment ion masses and normalize peak intensities within each spectrum. 3. Calculate neutral loss values for all observed fragment pairs.: "Extract fragment ion masses and normalize peak intensities within each spectrum. 3. Calculate neutral loss values for all observed fragment pairs."
- [methods] Filter noise by removing fragments and losses below a minimum intensity threshold or statistical significance cutoff.: "Filter noise by removing fragments and losses below a minimum intensity threshold or statistical significance cutoff."
- [other] The preprocessing module converts MS/MS spectra into a bag-of-fragments format, extracts neutral losses, and filters out noise to prepare data for LDA modeling.: "The preprocessing module converts MS/MS spectra into a bag-of-fragments format, extracts neutral losses, and filters out noise to prepare data for LDA modeling."
- [methods] Extract neutral losses: "Extract neutral losses"
