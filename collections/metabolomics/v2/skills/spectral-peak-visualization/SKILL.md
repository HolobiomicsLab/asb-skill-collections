---
name: spectral-peak-visualization
description: Use when you have a resolved mass spectrum (m/z values, intensities, and metadata) from a supported USI source (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA, or MassIVE) and need to create a publication-ready image that retains a link back to an interactive spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - GNPS Molecular Networking
  - GNPS Spectral Libraries
  - MassBank
  - MetaboLights
  - Metabolomics Workbench
  - ProteoXchange Repository
  - MS2LDA
  - MetabolomicsSpectrumResolver
derived_from:
- doi: 10.1101/2020.05.09.086066
  title: Metabolomics Spectrum Resolver
evidence_spans:
- GNPS Molecular Networking Clustered Spectra
- GNPS Spectral Libraries
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
---

# spectral-peak-visualization

## Summary

Generate embeddable static spectrum plots (PNG/SVG) from resolved mass spectrometry data, with optional peak annotations, filtering, and embedded hyperlinks or QR codes for publication integration and interactive spectrum viewer linking.

## When to use

You have a resolved mass spectrum (m/z values, intensities, and metadata) from a supported USI source (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA, or MassIVE) and need to create a publication-ready image that retains a link back to an interactive spectrum visualization platform. Use this skill when publishing figures that must remain static in PDF/print but should provide readers a pathway to explore the raw spectrum interactively.

## When NOT to use

- Input spectrum is already rasterized or lossy-compressed (PNG/JPG); you cannot recover precise m/z and intensity values for re-rendering.
- Target publication or platform does not support hyperlinks, QR codes, or external URL references (e.g., some legacy print-only workflows).
- You need to perform spectral comparison, alignment, or clustering; use mirror matching or network analysis skills instead.

## Inputs

- Resolved USI identifier (string, e.g., 'mzspec:GNPS:TASK-xxx:scan:1943')
- m/z array (numeric vector)
- Intensity array (numeric vector)
- Spectrum metadata (scan number, file name, accession, optional annotations)

## Outputs

- Static spectrum plot image (PNG or SVG file)
- Embeddable image with embedded or adjacent hyperlink/QR code
- Image file metadata or sidecar file containing interactive spectrum viewer URL

## How to apply

Load the resolved spectrum data (m/z array and intensity array) from the USI resolver output or directly from a supported repository endpoint. Render a raster or vector plot of peaks and baseline intensity using a visualization library (matplotlib, plotly, or similar), specifying customizable parameters such as m/z range (mz_min, mz_max), maximum intensity scaling (max_intensity), peak annotation threshold (annotate_threshold), annotation precision (annotate_precision), and optional grid/label rotation. Generate or embed a unique URL pointing to the interactive spectrum viewer endpoint (e.g., metabolomics-usi.ucsd.edu/spectrum/?usi=...) or encode this URL into a QR code. Embed the URL or QR code into the image metadata or as a visible element (e.g., corner badge). Save the output as PNG (raster) or SVG (vector) with the embedded link intact so that downstream tools and readers can extract and follow the reference.

## Related tools

- **GNPS Molecular Networking** (Source of resolved clustered spectra accessible via USI) — https://gnps.ucsd.edu
- **GNPS Spectral Libraries** (Source of reference library spectra accessible via USI accession) — https://gnps.ucsd.edu
- **MassBank** (Source of curated reference spectra accessible via USI) — https://massbank.eu
- **MetaboLights** (Source of metabolomics dataset spectra accessible via USI) — https://www.ebi.ac.uk/metabolights
- **Metabolomics Workbench** (Source of metabolomics dataset spectra accessible via USI) — https://www.metabolomicsworkbench.org
- **ProteoXchange Repository** (Source of proteomics spectra accessible via USI identifiers) — http://www.psidev.info/proteomexchange
- **MS2LDA** (Source of reference motifs accessible via USI)
- **MetabolomicsSpectrumResolver** (Core tool that resolves USI identifiers, renders spectrum plots (SVG/PNG), and generates embeddable images with linked viewers) — https://github.com/mwang87/MetabolomicsSpectrumResolver

## Examples

```
![](https://metabolomics-usi.ucsd.edu/svg/?usi=mzspec:GNPS:TASK-c95481f0c53d42e78a61bf899e9f9adb-spectra/specs_ms.mgf:scan:1943&mz_min=550&mz_max=800&annotate_peaks=[[463.297,708.463,816.474]])
```

## Evaluation signals

- Output image file exists and is valid PNG/SVG format (can be opened in standard image viewers).
- Embedded or sidecar URL points to a live, resolvable interactive spectrum viewer endpoint that displays the same m/z and intensity data.
- Peak annotations (if requested) match the specified m/z values and respect the annotate_threshold; precision matches annotate_precision parameter.
- Rendered m/z and intensity ranges match the input data after applying mz_min, mz_max, and max_intensity filters.
- QR code (if present) is scannable and resolves to the interactive spectrum viewer URL.

## Limitations

- USI identifiers are based on draft standards ('mzdraft' prefix) and are subject to change; forward compatibility is not guaranteed.
- Supported repositories are fixed (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA, MassIVE); spectra from other sources require pre-conversion to USI or custom resolver extension.
- Embeddable images retain hyperlinks only if the publication platform, PDF reader, or downstream tool supports URL extraction and dereferencing; some legacy or restricted environments may strip or ignore embedded URLs.
- Mirror matching visualization requires two USI identifiers; single-spectrum rendering does not support direct spectral comparison overlays within the image.

## Evidence

- [readme] Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots.: "Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots."
- [other] The tool achieves embeddable image creation by resolving USI identifiers from supported sources and generating linked visual outputs for publication integration.: "The tool achieves embeddable image creation by resolving USI identifiers from supported sources (GNPS Molecular Networking, GNPS Spectral Libraries, ProteoXchange, MS2LDA, MassBank, MetaboLights, and"
- [other] Render a static spectrum plot (peaks and baseline) as a raster image (PNG or SVG) using a plotting library.: "Render a static spectrum plot (peaks and baseline) as a raster image (PNG or SVG) using a plotting library."
- [other] Generate or embed a unique URL or QR code that points to the interactive spectrum viewer endpoint.: "Generate or embed a unique URL or QR code that points to the interactive spectrum viewer endpoint."
- [readme] 3rd party embedding for visualization of spectra that exist in repositories (e.g. MassIVE, PRIDE, PeptideAtlas).: "3rd party embedding for visualization of spectra that exist in repositories (e.g. MassIVE, PRIDE, PeptideAtlas)."
- [readme] annotate_peaks: Defines which peaks in which spectrum (top or bottom) will be annotated. The parameters is a list of lists of m/z values of the peaks to be annotated.: "annotate_peaks: Defines which peaks in which spectrum (top or bottom) will be annotated. The parameters is a list of lists of m/z values of the peaks to be annotated."
- [readme] These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec`"
