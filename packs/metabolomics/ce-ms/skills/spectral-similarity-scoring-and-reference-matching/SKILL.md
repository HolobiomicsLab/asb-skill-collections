---
name: spectral-similarity-scoring-and-reference-matching
description: Use when when you have extracted MS2 spectra from DDA chromatographic peaks and need to identify the originating compound by comparing against reference MS2 spectra (e.g., from Metlin or GNPS).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - MsBackendMgf
  - MsFeatures
  - Spectra
  - xcms
  - Metlin
  - GNPS
  techniques:
  - CE-MS
  - tandem-MS
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- library(MsBackendMgf)
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package with additional functionality being implemented
- VignetteDepends{xcms,BiocStyle,faahKO,pheatmap,MsFeatures}
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms_cq
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac051437y
  all_source_dois:
  - 10.1021/ac051437y
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-scoring-and-reference-matching

## Summary

Compute similarity scores between experimental MS2 fragmentation spectra and reference library spectra to enable compound annotation. This skill quantifies spectral concordance using cosine similarity or other metrics and produces ranked matches suitable for metabolite identification.

## When to use

When you have extracted MS2 spectra from DDA chromatographic peaks and need to identify the originating compound by comparing against reference MS2 spectra (e.g., from Metlin or GNPS). Use this when MS1 mass accuracy alone is insufficient for reliable annotation and you want to leverage fragmentation pattern information to disambiguate between candidate compounds with similar m/z values.

## When NOT to use

- The experimental MS2 spectrum is of poor quality (low signal-to-noise ratio, few fragments, or low intensity peaks) — spectral comparison will be unreliable.
- No MS2 fragmentation data is available (MS1-only data, e.g., from data-independent acquisition without precursor isolation) — similarity scoring requires fragment ion information.
- The reference library does not cover the compound class of interest — high similarity scores may not be achievable even for correct compounds.

## Inputs

- Experimental MS2 consensus spectrum (Spectra object, msLevel=2)
- Reference MS2 library spectra (MGF format or Spectra object from MsBackendMgf)
- Parameter values: ppm tolerance (typically 20 ppm), similarity metric (cosine, default)

## Outputs

- Numeric similarity scores (compareSpectra output, one score per reference spectrum)
- Ranked list of candidate compounds (sorted by similarity score)
- Annotated mirror plots (visual comparison of experimental vs. reference fragments)
- Compound annotation assignment (matched reference spectrum identifier)

## How to apply

First, prepare a consensus MS2 spectrum from multiple scans of the same precursor using combineSpectra() with FUN=combinePeaks, ppm=20, peaks='intersect', and minProp=0.8 to aggregate fragmentation information. Load reference MS2 spectra from a library (e.g., Metlin MGF files via readMgf() or MsBackendMgf backend). Compute compareSpectra() similarity scores between the experimental consensus spectrum and each reference spectrum using the default cosine similarity metric. Generate annotated mirror plots via plotSpectraMirror() for visual inspection of the top-scoring matches. Report both numerical similarity scores and visual comparisons; higher cosine similarity (typically >0.7) and visually aligned peak positions indicate stronger matches. The rank order and magnitude of similarity scores guide the final compound assignment.

## Related tools

- **Spectra** (R package for storing, manipulating, and comparing mass spectrometry spectra objects; provides compareSpectra() function for similarity computation)
- **MsBackendMgf** (Bioconductor backend for reading and writing MGF (mascot generic format) reference library files)
- **xcms** (Extracts MS2 spectra associated with detected chromatographic peaks via chromPeakSpectra() and combines multiple spectra into consensus via combineSpectra()) — https://github.com/sneumann/xcms
- **Metlin** (Reference MS2 spectral library for metabolite annotation) — https://metlin.scripps.edu
- **GNPS** (Community resource for MS2 spectral matching and feature-based molecular networking) — https://ccms-ucsd.github.io/GNPSDocumentation/featurebasedmolecularnetworking/

## Examples

```
compareSpectra(ex_spectra, consensus_spectrum, ppm = 20); plotSpectraMirror(consensus_spectrum, reference_spectrum, main = 'Experimental vs. Fenamiphos', ppm = 20)
```

## Evaluation signals

- Similarity scores are bounded in [0, 1] range; top-scoring candidate has substantially higher similarity than second-ranked candidate (>0.3 point gap suggests clearer match).
- Mirror plot visualization shows overlapping fragment peaks at consistent m/z values between experimental and reference spectra; misaligned or absent peaks indicate poor correspondence.
- Experimental consensus spectrum shares ≥80% of most intense fragments with the highest-scoring reference spectrum (minProp=0.8 threshold), indicating robust fragmentation pattern agreement.
- The matched compound has plausible elemental composition, retention time, and ionization consistency with the experimental chromatographic peak properties.
- When multiple reference spectra exist for the same compound (different instruments or collision energies), they rank similarly high relative to non-matching compounds, demonstrating specificity.

## Limitations

- Cosine similarity can produce false positives when compounds have structurally similar fragments but different origins; visual inspection of mirror plots is essential for final confirmation.
- Reference library coverage is incomplete for many pesticides, drugs, and metabolites; absent compounds cannot be matched regardless of spectral quality.
- MS2 spectra are sensitive to ionization polarity, collision energy, and instrument type; reference spectra acquired under different conditions may not match well despite structural identity.
- Consensus spectra constructed with minProp=0.8 may discard low-abundance diagnostic fragments present in only some scans, potentially reducing annotation sensitivity.
- DDA acquisition does not guarantee MS2 spectra for all detected features, limiting annotation to the subset of peaks that triggered data-dependent fragmentation.

## Evidence

- [other] The experimental consensus MS2 spectrum from the m/z 304.1131 chromatographic peak showed high similarity to Fenamiphos reference spectra but not to Flumazenil: "The experimental consensus MS2 spectrum from the m/z 304.1131 chromatographic peak showed high similarity to Fenamiphos reference spectra but not to Flumazenil, with mirror plot visualization and"
- [other] Combine multiple MS2 spectra into a single consensus spectrum using combineSpectra() with FUN=combinePeaks, ppm=20, peaks='intersect', and minProp=0.8.: "Combine multiple MS2 spectra into a single consensus spectrum using combineSpectra() with FUN=combinePeaks, ppm=20, peaks='intersect', and minProp=0.8."
- [other] Compute compareSpectra similarity scores between the consensus spectrum and each reference spectrum using default or cosine similarity metric.: "Compute compareSpectra similarity scores between the consensus spectrum and each reference spectrum using default or cosine similarity metric."
- [other] Report similarity scores and generate annotated mirror plots for visual comparison.: "Report similarity scores and generate annotated mirror plots for visual comparison."
- [intro] A search of potential ions with a similar m/z in a reference database (e.g. [Metlin](https://metlin.scripps.edu)): "A search of potential ions with a similar m/z in a reference database (e.g. [Metlin](https://metlin.scripps.edu))"
- [intro] This workflow can be included into the *Feature-Based Molecular Networking* [FBMN](https://ccms-ucsd.github.io/GNPSDocumentation/featurebasedmolecularnetworking/) to match MS2 spectra against: "This workflow can be included into the *Feature-Based Molecular Networking* [FBMN](https://ccms-ucsd.github.io/GNPSDocumentation/featurebasedmolecularnetworking/) to match MS2 spectra against"
- [intro] Extract MS2 spectra associated with chromatographic peaks for annotation: "Extract MS2 spectra associated with chromatographic peaks for annotation"
- [intro] Match experimental MS2 spectrum against reference database spectra using similarity metrics: "Match experimental MS2 spectrum against reference database spectra using similarity metrics"
