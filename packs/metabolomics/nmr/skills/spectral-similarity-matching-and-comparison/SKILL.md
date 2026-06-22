---
name: spectral-similarity-matching-and-comparison
description: Use when after extracting and optionally combining MS2 spectra from a chromatographic peak (e.g., at a known m/z value like 304.1131), you need to determine which compound(s) in a reference library match the experimental spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MsFeatures
  - Spectra
  - MsBackendMgf
  - MetaboCoreUtils
  - xcms
  techniques:
  - LC-MS
  - GC-MS
  - CE-MS
  - NMR
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
- library(Spectra)
- library(MsBackendMgf)
- '%\VignetteDepends{xcms,MsDataHub,BiocStyle,pander,Spectra,MsBackendMgf,MetaboCoreUtils}'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac051437y
  all_source_dois:
  - 10.1021/ac051437y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-matching-and-comparison

## Summary

Match experimental MS2 spectra (consensus or single) against reference spectral libraries to identify unknown compounds through normalized dot-product similarity scoring. This skill enables compound identification in LC-MS/MS by quantifying spectral peak overlap and intensity agreement between experimental and reference MS2 data.

## When to use

After extracting and optionally combining MS2 spectra from a chromatographic peak (e.g., at a known m/z value like 304.1131), you need to determine which compound(s) in a reference library best match the experimental spectrum. This is essential when the precursor m/z alone is insufficient for identification, such as when multiple reference compounds have overlapping mass values (e.g., Flumazenil and Fenamiphos both near m/z 304) or when you need to confirm peak identity against known standards in MGF or spectral database format.

## When NOT to use

- When reference spectra for the suspected compounds are not available or differ significantly in acquisition conditions (e.g., different collision energy or MS instrument type) — similarity scores may be artificially low.
- When the experimental MS2 spectrum is of very low intensity or contains few informative peaks — consensus building from multiple spectra is required first.
- When the chromatographic peak is unresolved or contains multiple co-eluting compounds — deconvolution or higher-resolution separation should be performed before spectral matching.

## Inputs

- Experimental MS2 spectrum (Spectra object, single or consensus from chromPeakSpectra)
- Reference MS2 spectra in MGF format (loaded via MsBackendMgf)
- Chromatographic peak metadata (m/z, retention time, isolation window)

## Outputs

- Similarity scores (numeric vector) for each reference spectrum comparison
- Compound identity assignment (best-matching reference compound and ID)
- Mirror-plot visualization comparing experimental and reference spectra

## How to apply

Load reference MS2 spectra from MGF files or spectral libraries (e.g., Metlin IDs 2724 for Flumazenil, 72445 for Fenamiphos) into a Spectra object using the Spectra and MsBackendMgf packages. Prepare the experimental MS2 spectrum by either using a single high-intensity spectrum or combining multiple MS2 spectra from the same chromatographic peak via combineSpectra() with combinePeaks() to increase signal robustness. Call compareSpectra() with the normalized dot-product method, setting the m/z tolerance to 40 ppm (or appropriate for your instrument) to account for mass measurement error. Compare the resulting similarity scores across all reference candidates; a high similarity score (typically >0.7 for reliable matches) to one reference but not others indicates positive compound identification. Generate mirror-plot visualizations to qualitatively inspect peak alignment and confirm that major experimental peaks align with major reference peaks.

## Related tools

- **Spectra** (Core package for loading, manipulating, and storing experimental and reference MS2 spectra objects)
- **MsBackendMgf** (Backend for reading reference MS2 spectra from MGF (mascot generic format) files into Spectra objects)
- **MetaboCoreUtils** (Provides compareSpectra() method and similarity metrics (normalized dot-product) for spectral comparison)
- **xcms** (Upstream tool for chromatographic peak detection (findChromPeaks) and MS2 spectrum extraction (chromPeakSpectra)) — https://github.com/sneumann/xcms
- **MsFeatures** (Provides combineSpectra() and combinePeaks() functions for consensus spectrum generation prior to matching)

## Examples

```
compareSpectra(experimental_spectrum, reference_spectra, method='dot', ppm=40)
```

## Evaluation signals

- Similarity scores for true-positive reference compound are > 0.70 and substantially higher than false-positive candidates (e.g., >0.3 absolute difference).
- Mirror-plot visualization shows major m/z peaks (those with relative intensity >10% in either spectrum) in spatial alignment within the 40 ppm m/z tolerance window.
- Experimental spectrum intensity pattern across top 5–10 peaks correlates with reference spectrum pattern (visual inspection or Pearson r > 0.60 for peak intensities).
- Consensus spectrum from multiple MS2 scans shows improved match score and lower variance in peak position compared to any individual scan (when applicable).
- Matched compound's literature m/z, retention time range, and chemical class are consistent with the chromatographic peak metadata.

## Limitations

- Spectral similarity depends on matching acquisition parameters (collision energy, ionization mode, instrument type); reference spectra acquired under different conditions may yield falsely low similarity scores.
- The 40 ppm m/z tolerance is appropriate for high-resolution Orbitrap or Q-TOF instruments but may need adjustment for lower-resolution instruments; tolerance selection directly impacts false-positive and false-negative rates.
- Compounds with very similar structures (isomers, regioisomers) may produce nearly identical MS2 spectra; additional orthogonal confirmation (e.g., retention time, NMR, or complementary ionization mode) may be necessary.
- Gap-filling and missing signal detection in MS2 spectra are not addressed by this skill; undetected peaks in the experimental or reference spectrum reduce similarity scores even if the compound is correct.
- The normalized dot-product method is sensitive to noise and low-intensity peaks; spectra with poor signal-to-noise ratios or extensive background should be filtered or enhanced before comparison.

## Evidence

- [other] The consensus MS2 spectrum from the chromatographic peak at m/z 304.1131 has high similarity to Fenamiphos but not to Flumazenil when compared using the normalized dot-product method with 40 ppm tolerance, allowing identification of the peak as Fenamiphos.: "The consensus MS2 spectrum from the chromatographic peak at m/z 304.1131 has high similarity to Fenamiphos but not to Flumazenil when compared using the normalized dot-product method with 40 ppm"
- [intro] Spectra for identified chromatographic peaks can be extracted with the `chromPeakSpectra()` method. We next reduce this to a single MS2 spectrum using the `combineSpectra()` method employing the `combinePeaks()` function we can also calculate similarities between them with the `compareSpectra()` method: "Spectra for identified chromatographic peaks can be extracted with the `chromPeakSpectra()` method. We next reduce this to a single MS2 spectrum using the `combineSpectra()` method employing the"
- [other] Match the experimental consensus spectrum against Flumazenil (Metlin ID 2724) and Fenamiphos (Metlin ID 72445) reference spectra in MGF format using compareSpectra().: "Match the experimental consensus spectrum against Flumazenil (Metlin ID 2724) and Fenamiphos (Metlin ID 72445) reference spectra in MGF format using compareSpectra()"
- [readme] The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data"
