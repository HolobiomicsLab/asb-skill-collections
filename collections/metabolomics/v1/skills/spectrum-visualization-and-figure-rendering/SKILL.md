---
name: spectrum-visualization-and-figure-rendering
description: Use when when you have a processed or annotated MsmsSpectrum object (from USI loading or direct instantiation) and need to generate a figure showing observed peaks, their intensities, and assigned fragment ions (e.g., b/y ions) for publication or presentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spectrum_utils
  - Python
  - matplotlib
  - ProForma 2.0
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
- import matplotlib.pyplot as plt
- fig, ax = plt.subplots(figsize=(12, 6))
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils
schema_version: 0.2.0
---

# Spectrum Visualization and Figure Rendering

## Summary

Create publication-quality mass spectrometry spectrum plots annotated with fragment ion assignments using spectrum_utils.plot and Matplotlib. This skill enables interactive and static visualization of tandem mass spectrometry data with customizable peak annotations, intensity scaling, and output formats suitable for peer-reviewed manuscripts.

## When to use

When you have a processed or annotated MsmsSpectrum object (from USI loading or direct instantiation) and need to generate a figure showing observed peaks, their intensities, and assigned fragment ions (e.g., b/y ions) for publication or presentation. Use this skill when you want fine control over grid visibility, spine rendering, resolution (300 dpi), and file format (PNG).

## When NOT to use

- Input spectrum has not been processed (precursor/noise removal and intensity scaling are typically prerequisite steps for clear visualization).
- Fragment annotation is not desired or the peptide sequence is unknown; use spectrum_utils.plot without annotate_proforma() in that case.
- Output must be interactive (e.g., for web embedding); use Vega-Lite or interactive plotting backends instead of static PNG export.

## Inputs

- MsmsSpectrum object (loaded from USI or instantiated from raw m/z and intensity arrays)
- ProForma 2.0 peptide string (optional, for annotation)
- Fragment tolerance parameters (mass value and mode: 'Da' or 'ppm')

## Outputs

- PNG figure file at specified path
- matplotlib Figure and Axes objects (if rendered to notebook or display)

## How to apply

Instantiate or load an MsmsSpectrum object, optionally annotate it using annotate_proforma() with a ProForma 2.0 peptide string and ion_types parameter (e.g., 'by' for b and y ions, 'aby' for a, b, and y) with a specified fragment tolerance (e.g., 10 ppm). Create a matplotlib Figure and Axes, then call spectrum_utils.plot.spectrum() with the annotated spectrum, disabling the grid and adjusting spine visibility for clarity. Save the figure using savefig() with dpi=300 and bbox_inches='tight' to ensure publication-quality output and remove excess whitespace.

## Related tools

- **spectrum_utils** (Core library providing MsmsSpectrum class, annotate_proforma() method, and spectrum_utils.plot.spectrum() plotting function for spectrum rendering.) — https://github.com/bittremieux/spectrum_utils/
- **matplotlib** (Underlying plotting backend; provides Figure, Axes, and savefig() for creating and exporting publication-quality figures.)
- **ProForma 2.0** (Standard specification for encoding modified peptidoforms and fragment ion annotations passed to annotate_proforma().) — https://www.psidev.info/proforma

## Examples

```
import matplotlib.pyplot as plt
from spectrum_utils.spectrum import MsmsSpectrum
from spectrum_utils import plot

spectrum = MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475')
spectrum.annotate_proforma('PEPTIDE', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='by')

fig, ax = plt.subplots(figsize=(10, 6))
plot.spectrum(spectrum, ax=ax, grid=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.savefig('spectrum.png', dpi=300, bbox_inches='tight')
```

## Evaluation signals

- PNG file is created at the specified output path with non-zero file size.
- Figure resolution is 300 dpi (verify via image metadata or matplotlib savefig dpi argument).
- Grid is not visible on the plot (grid removed or set to False in spectrum_utils.plot call).
- Spine visibility is adjusted (e.g., top and right spines hidden for clean appearance).
- If annotation was applied, observed peaks are labeled with their assigned fragment ion types (b, y, a, etc.) and the number of matched peaks is > 0.

## Limitations

- The quality of annotation depends on fragment tolerance (tol_mass and tol_mode); tight tolerances may result in false negatives (unmatched peaks), while loose tolerances may cause false positives.
- Fragment annotation requires a known or inferred peptide sequence in ProForma 2.0 format; unknown modifications or non-standard residues may not be recognized.
- Static PNG export loses interactive features; for interactive exploration, alternative plotting backends (e.g., Plotly or Vega) are more suitable.
- Spectrum processing (precursor removal, intensity filtering, scaling) is assumed to be performed before visualization; raw, unprocessed spectra may be cluttered and difficult to interpret.

## Evidence

- [intro] Publication-quality, fully customizable spectrum plotting and interactive spectrum plotting.: "Publication-quality, fully customizable spectrum plotting and interactive spectrum plotting"
- [other] Annotate the spectrum with a ProForma peptide string using annotate_proforma() method, specifying ion_types='by' to label b and y fragment ions and a fragment tolerance (e.g., 10 ppm).: "Annotate the spectrum with a ProForma peptide string using annotate_proforma() method, specifying ion_types='by' to label b and y fragment ions and a fragment tolerance (e.g., 10 ppm)"
- [other] Create a matplotlib figure and use spectrum_utils.plot.spectrum() to render the annotated spectrum with grid disabled and spine visibility adjusted.: "Create a matplotlib figure and use spectrum_utils.plot.spectrum() to render the annotated spectrum with grid disabled and spine visibility adjusted"
- [other] Save the resulting figure as a PNG file with 300 dpi resolution and tight bounding box.: "Save the resulting figure as a PNG file with 300 dpi resolution and tight bounding box"
- [intro] Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms"
