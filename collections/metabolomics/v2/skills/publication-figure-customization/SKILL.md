---
name: publication-figure-customization
description: Use when after annotating a mass spectrometry spectrum with fragment ions (e.g., via ProForma 2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - spectrum_utils
  - matplotlib
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization
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
---

# publication-figure-customization

## Summary

Customize static mass spectrometry spectrum plots for publication quality using matplotlib backends, including spine removal, title formatting, and high-resolution PNG export with transparency. This skill transforms annotated spectra into camera-ready figures suitable for peer-reviewed journals.

## When to use

After annotating a mass spectrometry spectrum with fragment ions (e.g., via ProForma 2.0 peptide strings), when you need to generate publication-quality static figures with customized aesthetics—specifically when default plotting is insufficient and you require fine-grained control over axes, labels, resolution, and background transparency for inclusion in manuscripts.

## When NOT to use

- Input spectrum is not yet annotated with fragment ions—perform annotation (e.g., via annotate_proforma()) before customization.
- Interactive visualization is required; this skill produces static plots only. Use interactive backends (e.g., Plotly) for web-based exploration.
- Figure will be printed in grayscale; color_ions=True may not provide sufficient contrast without additional adjustment.

## Inputs

- annotated MsmsSpectrum object (from spectrum_utils.spectrum.MsmsSpectrum)
- matplotlib figure and axes objects

## Outputs

- high-resolution PNG image file (300 dpi, transparent background)
- customized matplotlib figure with publication-quality aesthetics

## How to apply

Create a matplotlib figure and axes using plt.subplots(). Call spectrum_utils.plot.spectrum() with the annotated MsmsSpectrum object, setting parameters color_ions=True for colored ion annotations and grid=False to remove visual clutter. Customize the figure by hiding the right and top spines using ax.spines[].set_visible(False) to follow publication guidelines for minimal ink. Add a descriptive title using ax.set_title(). Finally, save the figure to PNG format using plt.savefig() with dpi=300 for publication resolution, bbox_inches='tight' to eliminate excess whitespace, and transparent=True to enable composite figures or non-white backgrounds. These choices produce camera-ready output compliant with journal submission requirements.

## Related tools

- **spectrum_utils** (provides spectrum_utils.plot.spectrum() function for rendering annotated spectra and MsmsSpectrum class for holding annotated fragment data) — https://github.com/bittremieux/spectrum_utils
- **matplotlib** (backend for figure creation (plt.subplots()), axes customization (ax.spines, ax.set_title()), and PNG export (plt.savefig()))
- **Python** (runtime environment for spectrum_utils and matplotlib integration)

## Examples

```
import matplotlib.pyplot as plt; from spectrum_utils.spectrum import MsmsSpectrum; spectrum = MsmsSpectrum.from_usi("mzspec:MSV000082283:f07074:scan:5475"); spectrum.annotate_proforma("PEPTIDE", fragment_tol_mass=0.02, fragment_tol_mode='Da', ion_types='aby'); fig, ax = plt.subplots(); from spectrum_utils.plot import spectrum as plot_spectrum; plot_spectrum(spectrum, color_ions=True, grid=False, ax=ax); ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False); ax.set_title('MS/MS Spectrum'); plt.savefig('spectrum.png', dpi=300, bbox_inches='tight', transparent=True)
```

## Evaluation signals

- Output PNG file exists and is non-empty; file size > 10 KB typical for 300 dpi annotated spectrum
- Image dimensions and resolution metadata: `identify output.png` or `PIL.Image.open()` shows DPI = 300
- Visual inspection: right and top spines are absent; left and bottom spines are visible; title text is present and readable
- Background is transparent: opening PNG in transparent-aware viewer (e.g., GIMP) shows checkerboard pattern behind spectrum, not white
- Ion peaks are rendered in distinct colors when color_ions=True (e.g., different hues for a, b, y fragments); grid lines are absent (grid=False verified)

## Limitations

- Static PNG output only; no interactive tooltips or zoom capability. For interactive exploration, use alternative backends.
- Customization is limited to matplotlib-accessible properties (spines, titles, labels). Complex layouts (multi-panel figures) require additional matplotlib composition.
- Color scheme and ion annotation types are determined upstream during spectrum.annotate_proforma(); this skill does not alter ion assignments, only their visual presentation.
- Transparent backgrounds may cause rendering issues in older PDF viewers or when embedded in certain document formats; verify compatibility with target publication workflow.

## Evidence

- [other] spectrum_utils provides publication-quality, fully customizable spectrum plotting capabilities for visualizing annotated spectra, with a Matplotlib backend enabling static image generation of annotated mass spectrometry data.: "spectrum_utils provides publication-quality, fully customizable spectrum plotting capabilities for visualizing annotated spectra, with a Matplotlib backend enabling static image generation"
- [other] Create a matplotlib figure and axes using plt.subplots(). Call spectrum_utils.plot.spectrum() with the annotated spectrum, passing parameters for color_ions=True, grid=False, and ax=ax. Customize the plot by hiding right and top spines using ax.spines[].set_visible(False) and set the title using ax.set_title(). Save the figure to PNG using plt.savefig() with dpi=300, bbox_inches='tight', and transparent=True.: "Create a matplotlib figure and axes using plt.subplots(). Call spectrum_utils.plot.spectrum() with the annotated spectrum, passing parameters for color_ions=True, grid=False, and ax=ax. Customize the"
- [intro] spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.: "spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization."
- [other] import matplotlib.pyplot as plt: "import matplotlib.pyplot as plt"
