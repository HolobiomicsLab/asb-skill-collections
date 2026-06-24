---
name: mass-spectrum-visualization-matplotlib
description: Use when you have an annotated MsmsSpectrum object (with fragment assignments
  via ProForma 2.0) and need to produce a high-resolution, static PNG figure showing
  both the observed spectrum and color-highlighted fragment ion matches for inclusion
  in a manuscript or supplementary materials.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - spectrum_utils
  - Python
  - matplotlib
  - ProForma 2.0
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization
- import matplotlib.pyplot as plt
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils_cq
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-visualization-matplotlib

## Summary

Generate publication-quality static plots of annotated mass spectrometry spectra using spectrum_utils' Matplotlib backend. This skill enables customizable visualization of fragment ion annotations overlaid on observed m/z intensity distributions for peer-reviewed figure production.

## When to use

You have an annotated MsmsSpectrum object (with fragment assignments via ProForma 2.0) and need to produce a high-resolution, static PNG figure showing both the observed spectrum and color-highlighted fragment ion matches for inclusion in a manuscript or supplementary materials.

## When NOT to use

- The spectrum is unannotated or lacks fragment ion assignments — use spectrum.annotate_proforma() first.
- You need interactive, web-based visualization (e.g., zooming, tooltips) — consider Vega-Embed or Altair instead.
- The output must be vector-based (PDF, SVG) rather than raster — use plt.savefig() with format='pdf' or 'svg' and different backend instead.

## Inputs

- MsmsSpectrum object (annotated with fragment assignments)
- ProForma 2.0 peptide string
- Fragment tolerance parameters (mass value, mode: 'Th' or 'ppm')
- Ion type specification (e.g., 'aby' for a, b, y fragments)

## Outputs

- PNG image file (300 dpi, publication-quality)
- Matplotlib Figure object
- Matplotlib Axes object with rendered spectrum

## How to apply

Load or create an MsmsSpectrum object and annotate it using spectrum.annotate_proforma() with a ProForma 2.0 peptide string, specifying fragment_tol_mass, fragment_tol_mode, and ion_types (e.g., 'aby'). Create a matplotlib figure and axes using plt.subplots(). Call spectrum_utils.plot.spectrum() with the annotated spectrum, the axes object, and parameters color_ions=True and grid=False to enable ion-type color coding and remove gridlines. Customize the plot by hiding right and top spines via ax.spines[].set_visible(False) and set a descriptive title with ax.set_title(). Save the figure to PNG using plt.savefig() with dpi=300 for publication resolution, bbox_inches='tight' to eliminate margins, and transparent=True for overlay compatibility.

## Related tools

- **spectrum_utils** (Provides the MsmsSpectrum class, annotate_proforma() method, and spectrum_utils.plot.spectrum() plotting function with Matplotlib backend) — https://github.com/bittremieux/spectrum_utils
- **matplotlib** (Rendering engine for static figure generation; plt.subplots(), ax.spines, ax.set_title(), and plt.savefig() called via spectrum_utils.plot interface)
- **ProForma 2.0** (Specification for encoding peptide sequences with post-translational modifications; used as input string to spectrum.annotate_proforma()) — https://github.com/HUPO-PSI/psi-mod-CV

## Examples

```
import matplotlib.pyplot as plt
from spectrum_utils.spectrum import MsmsSpectrum
from spectrum_utils import plot
spectrum = MsmsSpectrum.from_usi("mzspec:MSV000082283:f07074:scan:5475")
spectrum.annotate_proforma("PEPTIDE", fragment_tol_mass=0.02, fragment_tol_mode="Th", ion_types="aby")
fig, ax = plt.subplots(figsize=(12, 6))
plot.spectrum(spectrum, color_ions=True, grid=False, ax=ax)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_title("Annotated MS/MS Spectrum")
plt.savefig("spectrum.png", dpi=300, bbox_inches="tight", transparent=True)
```

## Evaluation signals

- Output PNG file exists at specified path with dpi=300 and file size > 10 KB (indicating rendered content)
- Image displays annotated peaks in color (ion_types 'a', 'b', 'y' distinguished) against observed intensity spectrum
- Figure title and axis labels are visible and legible when opened in standard image viewer or embedded in manuscript
- Comparing spectrum plot to original MsmsSpectrum object: all annotated fragment ions appear at correct m/z and intensity positions
- PNG is transparent (verified by overlay on colored background without white background bleed)

## Limitations

- Plotting quality depends on prior annotation accuracy — mismatched fragment_tol_mass or fragment_tol_mode values will result in missed or spurious ion highlights.
- Static PNG output loses interactivity; users cannot zoom or inspect specific peak values post-export.
- High-resolution rendering (dpi=300) may be slow for very large spectra (>1000 peaks) or when called in batch workflows.
- Matplotlib rendering is single-threaded; parallel batch visualization requires manual parallelization outside spectrum_utils.

## Evidence

- [other] Publication-quality, fully customizable spectrum plotting capabilities for visualizing annotated spectra: "spectrum_utils provides publication-quality, fully customizable spectrum plotting capabilities for visualizing annotated spectra, with a Matplotlib backend enabling static image generation of"
- [other] Workflow: Create matplotlib figure, call spectrum_utils.plot.spectrum() with color_ions and grid parameters, customize spines and title, save to PNG: "Create a matplotlib figure and axes using plt.subplots(). Call spectrum_utils.plot.spectrum() with the annotated spectrum, passing parameters for color_ions=True, grid=False, and ax=ax. Customize the"
- [other] Annotate using ProForma 2.0 specification and fragment tolerance parameters: "Annotate the spectrum with a ProForma 2.0 peptide string using spectrum.annotate_proforma() with specified fragment tolerance (mass and mode), ion types (e.g., 'aby'), and optionally neutral losses."
- [intro] Publication-quality, fully customizable and interactive spectrum plotting: "Publication-quality, fully customizable spectrum plotting and interactive spectrum plotting."
- [other] Matplotlib backend enabling static image generation: "with a Matplotlib backend enabling static image generation of annotated mass spectrometry data"
