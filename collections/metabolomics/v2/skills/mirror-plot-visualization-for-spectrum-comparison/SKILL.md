---
name: mirror-plot-visualization-for-spectrum-comparison
description: Use when after computing compareSpectra similarity scores between an experimental consensus MS2 spectrum and candidate reference spectra (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MsBackendMgf
  - MsFeatures
  - Spectra
  - xcms
  - MetaboCoreUtils
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
---

# mirror-plot-visualization-for-spectrum-comparison

## Summary

Generate side-by-side mirror plots to visually compare experimental MS2 fragmentation spectra against reference spectra, enabling rapid qualitative assessment of spectral similarity and compound annotation confidence. Mirror plots display peak intensities inverted across a horizontal axis, making matching fragment ions immediately recognizable.

## When to use

After computing compareSpectra similarity scores between an experimental consensus MS2 spectrum and candidate reference spectra (e.g., from Metlin), use mirror-plot visualization when you need to visually validate the top-scoring match(es) or investigate why two spectra scored differently than expected. Particularly valuable when scores are borderline or when multiple compounds have similar m/z but distinct fragmentation patterns.

## When NOT to use

- When numerical similarity scores alone are sufficient for your analysis goal (e.g., bulk batch annotation without manual review).
- When comparing more than 2–3 spectra simultaneously; mirror plots become too cluttered for multiplex comparison.
- If reference spectra have substantially different m/z ranges or collision energies than your experimental data, since fragments may not align despite correct compound match.

## Inputs

- Consensus MS2 spectrum (Spectra object)
- Reference MS2 spectrum from spectral database (Spectra object, typically loaded from MGF)

## Outputs

- Mirror plot graphic (publication-ready plot showing overlaid experimental and reference spectra)
- Visual annotation confirming presence/absence of shared fragment peaks

## How to apply

Load experimental consensus MS2 spectrum and reference spectra (e.g., from Metlin MGF files using readMgf() or MsBackendMgf). Call plotSpectraMirror() to generate annotated mirror plots, specifying the experimental spectrum on top and reference spectrum inverted below, with ppm tolerance (typically 20–40 ppm) for peak matching. Visually inspect the plot for coinciding peaks (indicating fragment ion matches) and estimate overlap coverage. Peaks that align vertically across the mirror axis represent shared fragments; widespread vertical alignment combined with high compareSpectra cosine similarity scores (e.g., >0.7) confirms the annotation. Use the plot as supporting evidence alongside numerical scores for compound identification.

## Related tools

- **Spectra** (Core container and manipulation package for MS spectra objects; plotSpectraMirror() method resides here) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMgf** (Backend for reading MGF format spectral libraries (Metlin reference spectra) into Spectra objects) — https://github.com/RforMassSpectrometry/MsBackendMgf
- **xcms** (Provides chromPeakSpectra() and combineSpectra() to extract and consensus-combine experimental MS2 spectra prior to comparison) — https://github.com/sneumann/xcms
- **MetaboCoreUtils** (Provides compareSpectra() function for computing similarity scores (cosine, etc.) that inform which reference to visualize)

## Examples

```
plotSpectraMirror(ex_spectrum, flumanezil[3], main = "Experimental vs. Flumazenil", ppm = 40)
```

## Evaluation signals

- Vertical peak alignment: Experimental and reference peaks that match within ppm tolerance should align vertically across the mirror axis.
- Visual coverage: High-confidence matches typically show ≥50% of the most intense peaks shared between spectra.
- Concordance with numerical scores: Mirror plot visual impression (extent of alignment) should qualitatively match the reported compareSpectra score (e.g., high score ↔ dense vertical alignment).
- Absence of spurious peaks: Experimental peaks not present in the reference spectrum should be clearly distinguishable as unaligned noise or minor fragments.
- Symmetry and completeness: Both experimental and reference spectra should be fully represented in the plot with no clipping of m/z or intensity ranges.

## Limitations

- Mirror plots are subjective and qualitative; they supplement but do not replace numerical similarity metrics (e.g., cosine similarity scores).
- Collisional energy differences between experimental acquisition and reference library spectra can cause missing fragments in one spectrum, leading to incomplete visual alignment even for correct matches.
- Large ppm tolerances (e.g., 40 ppm) may cause false peak alignments if spectra have overlapping but distinct fragments close in m/z.
- Mirror plots become uninterpretable when experimental consensus spectra are very sparse (few detected fragments) or when reference spectra have very high noise floors.
- No automatic quantitative judgment of 'acceptable match' from the plot alone; analyst must combine visual inspection with compareSpectra scores to make annotation decisions.

## Evidence

- [intro] Visualization method establishes visual similarity: "generate annotated mirror plots for visual comparison"
- [intro] Method and tool used in the example task: "plotSpectraMirror(ex_spectrum, flumanezil[3], main = "against Flumanezil", ppm = 40)"
- [intro] Mirror plots used alongside numerical scores for validation: "mirror plot visualization and compareSpectra scores confirming Fenamiphos as the match"
- [intro] Consensus spectrum created for comparison: "combineSpectra(ex_spectra, FUN = combinePeaks, ppm = 20, peaks = 'intersect', minProp = 0.8)"
