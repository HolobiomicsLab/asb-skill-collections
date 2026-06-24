---
name: interactive-plot-embedding
description: Use when you have resolved USI (Unified Spectrum Identifier) spectrum
  data from a supported repository (GNPS, MassBank, MetaboLights, Metabolomics Workbench,
  ProteoXchange, or MS2LDA) and need to create a figure suitable for journal publication
  or supplementary materials that retains a link to the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - GNPS Molecular Networking
  - MassBank
  - MetaboLights
  - Metabolomics Workbench
  - MetabolomicsSpectrumResolver
  - ProteoXchange Repository
  - MS2LDA
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1101/2020.05.09.086066
  title: Metabolomics Spectrum Resolver
evidence_spans:
- GNPS Molecular Networking Clustered Spectra
- MassBank Library Spectra
- MetaboLights Dataset Spectra
- Metabolomics Workbench Dataset Spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabolomics_spectrum_resolver_cq
    doi: 10.1101/2020.05.09.086066
    title: Metabolomics Spectrum Resolver
  dedup_kept_from: coll_metabolomics_spectrum_resolver_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.05.09.086066
  all_source_dois:
  - 10.1101/2020.05.09.086066
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# interactive-plot-embedding

## Summary

Generate embeddable static spectrum plot images (PNG/SVG) with embedded URLs or QR codes that link to interactive spectrum visualization endpoints, enabling publication-ready figures with clickable access to full spectral data. This skill bridges publication media (static images) with web-based interactivity for metabolomics and proteomics data.

## When to use

You have resolved USI (Unified Spectrum Identifier) spectrum data from a supported repository (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, or MS2LDA) and need to create a figure suitable for journal publication or supplementary materials that retains a link to the full, explorable spectrum in a web browser. Use this when your goal is to enable readers to click or scan a figure in a PDF or HTML article to access interactive peak annotation, m/z filtering, and intensity scaling tools.

## When NOT to use

- The spectrum source is not in a supported repository or cannot be resolved to a valid USI (e.g., proprietary local format without a public accession).
- The use case requires real-time, live spectrum data updates; static images capture a snapshot and do not auto-refresh.
- Your publication or distribution channel does not support hyperlinks or QR code scanning (e.g., some print-only journals); in this case, consider caption text with manual URL entry instead.

## Inputs

- Resolved USI (Unified Spectrum Identifier) in the format mzspec:<source>:<identifier path>:<scan|accession>:<value>
- Spectrum source type (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA)
- Optional rendering parameters: m/z range, intensity scaling, peak annotation list, plot title, grid/annotation toggles

## Outputs

- Static spectrum plot image (PNG or SVG) with embedded URL or QR code
- Embeddable image file suitable for PDF, HTML, or journal manuscript
- Interactive spectrum viewer URL or QR code artifact

## How to apply

Resolve the USI identifier using the MetabolomicsSpectrumResolver to retrieve the spectrum's m/z values, intensities, and metadata. Render a static spectrum plot (bar/stick plot with baseline) as a raster or vector image using the resolver's `/svg/` or `/png/` endpoint, specifying optional parameters such as m/z range (mz_min, mz_max), intensity ceiling (max_intensity), peak annotations (annotate_peaks), grid display, and title. Generate a corresponding URL to the interactive viewer endpoint (e.g., `https://metabolomics-usi.ucsd.edu/spectrum/?usi=<USI>`) or QR code pointing to that URL. Embed this link as metadata within the image file or as a visible QR code overlaid on or adjacent to the static plot. Save the final embeddable image; verify that clicking or scanning the embedded link resolves to the interactive spectrum viewer for the same USI.

## Related tools

- **MetabolomicsSpectrumResolver** (Resolves USI identifiers and generates static plot images (/svg/, /png/ endpoints) and interactive spectrum URLs; core engine for this skill) — https://github.com/mwang87/MetabolomicsSpectrumResolver
- **GNPS Molecular Networking** (Spectrum data source for clustered spectra USI resolution)
- **MassBank** (Library spectrum data source for USI resolution)
- **MetaboLights** (Dataset repository spectrum data source for USI resolution)
- **Metabolomics Workbench** (Dataset repository spectrum data source for USI resolution)
- **ProteoXchange Repository** (Proteomics repository spectrum data source for USI resolution)
- **MS2LDA** (Reference motif and spectrum data source for USI resolution)

## Examples

```
https://metabolomics-usi.ucsd.edu/svg/?usi=mzspec:GNPS:TASK-c95481f0c53d42e78a61bf899e9f9adb-spectra/specs_ms.mgf:scan:1943&mz_min=550&mz_max=800&annotate_peaks=[[463.297,708.463,816.474]]
```

## Evaluation signals

- The generated image file is a valid PNG or SVG raster/vector image and can be opened in standard image viewers and PDF readers.
- The embedded URL or QR code, when clicked or scanned, resolves to an interactive spectrum viewer endpoint displaying the same USI and spectrum data as the static plot.
- The static plot accurately represents the resolved spectrum's peak positions (m/z values) and relative intensities from the source repository.
- Optional parameters (m/z range, peak annotations, intensity ceiling, title) are correctly applied to the rendered image; e.g., peaks outside mz_min/mz_max are not displayed.
- The image can be embedded in a PDF, HTML article, or supplementary material without corruption and retains its hyperlink or QR code functionality.

## Limitations

- USI identifiers are based on draft specifications (currently using 'mzdraft' instead of 'mzspec' prefix) and are subject to change; identifiers may break or require migration in future versions.
- The skill depends on the stability and availability of the underlying spectrum repository APIs (GNPS, MassBank, MetaboLights, etc.); if a repository is offline or removes a spectrum, the embedded link will fail.
- Static images do not auto-update if the underlying spectrum metadata or annotations in the source repository are revised after the image is generated.
- QR code embedding adds visual complexity and may not be suitable for high-resolution or print-heavy figure layouts; URL embedding as metadata may be preferable for some publication formats.
- Mirror-match plots (comparing two spectra) are supported but require two valid USI identifiers; single-spectrum and dual-spectrum rendering paths have separate parameter schemas.

## Evidence

- [readme] Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots.: "Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots."
- [readme] 3rd party embedding for visualization of spectra that exist in repositories (e.g. MassIVE, PRIDE, PeptideAtlas). 3rd party embedding of QR code.: "3rd party embedding for visualization of spectra that exist in repositories (e.g. MassIVE, PRIDE, PeptideAtlas). 3rd party embedding of QR code."
- [other] Load resolved spectrum data; render static spectrum plot; generate/embed URL or QR code pointing to interactive viewer; save embeddable image.: "1. Load the resolved spectrum data (m/z values, intensities, metadata) from the USI resolver output. 2. Render a static spectrum plot (peaks and baseline) as a raster image (PNG or SVG) using a"
- [readme] Supported sources include GNPS Molecular Networking, GNPS Spectral Libraries, ProteoXchange, MS2LDA, MassBank, MetaboLights, and Metabolomics Workbench.: "Supported USI Types: 1. GNPS Molecular Networking Clustered Spectra 2. GNPS Spectral Libraries 3. ProteoXchange Repository Data 4. MS2LDA Reference Motifs 5. MassBank Library Spectra 6. MetaboLights"
- [readme] The resolver provides /svg/ and /png/ endpoints with optional rendering parameters including mz_min, mz_max, annotate_peaks, plot_title, and grid display.: "1. /png/ 1. /svg/ ... ## Plotting Parameters - `mz_min`: Minimum m/z value. - `mz_max`: Maximum m/z value. - `annotate_peaks`: ... - `plot_title`: Custom plot title, omit to use default"
- [readme] USI identifiers are currently in draft status and may be subject to change.: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec`"
