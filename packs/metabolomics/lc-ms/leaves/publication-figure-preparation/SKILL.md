---
name: publication-figure-preparation
description: Use when you have a mass spectrometry spectrum from a supported repository (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA, or MassIVE) and need to include it in a publication or supplementary material.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - GNPS Molecular Networking
  - MassBank
  - MetaboLights
  - Metabolomics Workbench
  - GNPS Spectral Libraries
  - MetabolomicsSpectrumResolver
  techniques:
  - LC-MS
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

# publication-figure-preparation

## Summary

Transform resolved mass spectrometry USI identifiers into embeddable publication figures—static spectrum plots (PNG/SVG) with embedded hyperlinks or QR codes that allow readers to interactively explore spectra in online repositories. This skill bridges reproducibility and reader engagement by linking publication figures directly to viewable, interactive spectrum data.

## When to use

You have a mass spectrometry spectrum from a supported repository (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA, or MassIVE) and need to include it in a publication or supplementary material. You want readers to click through or scan a QR code to access the interactive spectrum viewer without breaking the figure's static embedding in a PDF or HTML article.

## When NOT to use

- Your spectrum does not originate from a supported repository (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA, MassIVE); the USI resolver cannot retrieve it.
- You require real-time, interactive peak picking or annotation during figure preparation; use the web viewer directly instead.
- Your publication platform does not support embedded hyperlinks or QR codes (e.g., print-only formats without digital companions).

## Inputs

- Unified Spectrum Identifier (USI) string (e.g., mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077)
- Resolved spectrum data (m/z values, intensities, metadata from USI resolver output)
- Plotting parameters (optional: mz_min, mz_max, annotate_peaks, plot_title, width, height, grid, annotation_rotation, annotate_threshold, annotate_precision, max_intensity)

## Outputs

- Embeddable spectrum plot image (PNG or SVG format)
- Embedded or annotated hyperlink or QR code pointing to interactive spectrum viewer
- Publication-ready figure file with linked reference metadata

## How to apply

First, obtain or construct a valid USI (Unified Spectrum Identifier) for your spectrum—e.g., `mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077` for a GNPS library spectrum. Resolve the USI using the MetabolomicsSpectrumResolver to retrieve the underlying spectrum data (m/z values, intensities, and metadata). Generate a static raster or vector plot (PNG or SVG) by rendering the peak list and baseline, optionally customizing parameters such as m/z range, intensity scaling, peak annotations, and grid visibility via URL query parameters (e.g., `mz_min`, `mz_max`, `annotate_peaks`, `plot_title`). Embed a clickable URL or QR code that references the interactive spectrum endpoint `/spectrum/?usi=<YOUR_USI>` into or alongside the static image—either as metadata (PDF annotation or hyperlinked image) or as a visual element (e.g., a QR code positioned near the figure caption). Save the final embeddable image to a file format compatible with your publication workflow. Verification: the figure displays correctly when embedded in a PDF or HTML article; the embedded URL or QR code resolves to the correct spectrum in the interactive viewer when clicked or scanned.

## Related tools

- **GNPS Molecular Networking** (Spectrum source and clustering platform; resolves USI for networked spectra.) — https://gnps.ucsd.edu
- **GNPS Spectral Libraries** (Reference spectrum repository; supplies library spectra for USI resolution and rendering.) — https://gnps.ucsd.edu
- **MassBank** (Mass spectrometry reference library; provides searchable, embeddable library spectra via USI.) — https://massbank.eu
- **MetaboLights** (Metabolomics data repository; hosts dataset spectra accessible via USI.) — https://www.ebi.ac.uk/metabolights/
- **Metabolomics Workbench** (Metabolomics data repository; provides dataset spectra for USI-based embedding.) — https://www.metabolomicsworkbench.org
- **MetabolomicsSpectrumResolver** (Core resolver and renderer; converts USI to embeddable images and interactive links.) — https://github.com/mwang87/MetabolomicsSpectrumResolver

## Examples

```
![Spectrum](https://metabolomics-usi.ucsd.edu/svg/?usi=mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077&mz_min=0&mz_max=1000&plot_title=MyCompound)
```

## Evaluation signals

- The generated spectrum plot visually matches the raw peak list from the resolved USI (m/z, intensity pairs are correctly rendered as peaks and baseline).
- The embedded hyperlink or QR code resolves to the correct interactive spectrum viewer endpoint when clicked or scanned.
- The static image embeds cleanly into the publication format (PDF, HTML, or preprint) without corruption or link breakage.
- Peak annotations (if requested) match the specified m/z values and precision settings; custom titles appear if supplied.
- Mass range filters (mz_min, mz_max) and intensity scaling parameters correctly restrict or rescale the visible plot area.

## Limitations

- USI identifiers are based on draft standards (mzdraft prefix) and subject to future changes; long-term stability of embedded links cannot be guaranteed.
- Only 7 specific spectrum repositories are supported; spectra from other sources cannot be resolved.
- Interactive spectrum viewer availability depends on the online deployment of the MetabolomicsSpectrumResolver endpoint; figures may become unclickable if the service is unavailable or migrated.
- QR code embedding requires additional processing and may not be supported by all publication or PDF generation workflows.
- No changelog documented; breaking changes to API or USI format may occur without advance notice.

## Evidence

- [intro] Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots.: "Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots."
- [intro] 3rd party embedding for visualization of spectra that exist in repositories (e.g. MassIVE, PRIDE, PeptideAtlas).: "3rd party embedding for visualization of spectra that exist in repositories (e.g. MassIVE, PRIDE, PeptideAtlas)."
- [intro] 3rd party embedding of QR code.: "3rd party embedding of QR code."
- [other] The tool achieves embeddable image creation by resolving USI identifiers from supported sources (GNPS Molecular Networking, GNPS Spectral Libraries, ProteoXchange, MS2LDA, MassBank, MetaboLights, and Metabolomics Workbench) and generating linked visual outputs for publication integration.: "resolving USI identifiers from supported sources (GNPS Molecular Networking, GNPS Spectral Libraries, ProteoXchange, MS2LDA, MassBank, MetaboLights, and Metabolomics Workbench) and generating linked"
- [other] Render a static spectrum plot (peaks and baseline) as a raster image (PNG or SVG) using a plotting library. Generate or embed a unique URL or QR code that points to the interactive spectrum viewer endpoint. Embed the URL or QR code into or alongside the static image as metadata or as a visual element.: "Render a static spectrum plot (peaks and baseline) as a raster image (PNG or SVG) using a plotting library. Generate or embed a unique URL or QR code that points to the interactive spectrum viewer"
- [readme] These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec` in the first block.: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec`"
- [readme] Plotting Parameters: mz_min, mz_max, annotate_peaks, plot_title, and parameters controlling intensity scaling, grid display, label rotation, and annotation threshold.: "mz_min: Minimum m/z value. mz_max: Maximum m/z value. annotate_peaks: Defines which peaks in which spectrum (top or bottom) will be annotated. plot_title: Custom plot title, omit to use default"
