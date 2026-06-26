---
name: spatial-pixel-coordinate-alignment
description: Use when you have mzML files from a mass spectrometry imaging (MSI) experiment
  and need to convert them to imzML format with correctly positioned pixel coordinates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - imzML Writer
  - imzML Scout
  - msconvert
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c06520
  title: imzML Writer
evidence_spans:
- import os import imzml_writer.utils as iw_utils
- iw_utils.mzML_to_imzML_convert(PATH=mzML_path)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_imzml_writer_cq
    doi: 10.1021/acs.analchem.4c06520
    title: imzML Writer
  dedup_kept_from: coll_imzml_writer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06520
  all_source_dois:
  - 10.1021/acs.analchem.4c06520
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spatial-pixel-coordinate-alignment

## Summary

Align mass spectrometry imaging pixels to their spatial coordinates by converting mzML acquisition metadata into imzML pixel position arrays using X scan speed and Y step size parameters. This skill ensures that each pixel in the resulting ion image corresponds to its true location on the tissue sample.

## When to use

Apply this skill when you have mzML files from a mass spectrometry imaging (MSI) experiment and need to convert them to imzML format with correctly positioned pixel coordinates. The skill is necessary when raw vendor files have been converted to mzML but lack explicit 2D spatial indexing, and you have experimental parameters (X scan speed in µm/s and Y step size in µm) available from the imaging acquisition metadata.

## When NOT to use

- Input is already an imzML file with validated spatial coordinates — use metadata annotation instead.
- Experimental parameters (X scan speed, Y step size) are unavailable or unknown — alignment cannot be computed without these inputs.
- The mzML file lacks scan-level metadata (e.g., scan count per line) needed to reconstruct the 2D acquisition grid.

## Inputs

- mzML file(s) from mass spectrometry imaging experiment
- X scan speed parameter (µm/s)
- Y step size parameter (µm)

## Outputs

- imzML file with barebones structure and aligned pixel coordinates
- 2D spatial pixel array indexed by (x, y) position in micrometers

## How to apply

Call iw_utils.mzML_to_imzML_convert(PATH=mzML_path) to write the barebones imzML structure and compute pixel positions by multiplying the X scan speed (µm/s) and Y step size (µm) against the spectral acquisition indices. The function reads mzML scan metadata to extract the number of scans per line and total lines acquired, then maps each spectrum to a (x, y) coordinate in micrometers. Verify alignment by visually inspecting the ion image in imzML Scout to confirm that the pixel grid matches the expected tissue dimensions and that adjacent spectra are spatially adjacent in the output image. If pixels appear discontinuous or the image dimensions are incorrect, check that X scan speed and Y step size values match the instrument acquisition parameters.

## Related tools

- **imzML Writer** (Provides the iw_utils module and mzML_to_imzML_convert function that performs coordinate alignment and imzML structure generation.) — https://github.com/VIU-Metabolomics/imzML_Writer
- **imzML Scout** (Visualization and validation tool to inspect aligned pixel coordinates and verify spatial correctness of the ion image.) — https://github.com/VIU-Metabolomics/imzML_Writer
- **msconvert** (Upstream tool that converts raw vendor files to mzML format containing the acquisition metadata required for pixel alignment.) — https://proteowizard.sourceforge.io/download.html

## Examples

```
from imzml_writer import iw_utils; iw_utils.mzML_to_imzML_convert(PATH='/path/to/file.mzML')
```

## Evaluation signals

- Output imzML file contains valid pixel coordinate arrays with no NaN or infinite values.
- Pixel spacing in micrometers matches expected values computed from X scan speed and Y step size.
- Visual inspection in imzML Scout shows continuous, rectangular ion image with no gaps or overlaps between adjacent pixels.
- Ion image dimensions (in pixels) equal the number of scans per line × number of lines in the mzML acquisition.
- Clicking on adjacent pixels in Scout shows adjacent spectra (e.g., consecutive scan indices in the mzML) and red pixel highlight indicates correct spatial position.

## Limitations

- Requires accurate X scan speed and Y step size parameters from the instrument acquisition; incorrect values produce spatially misaligned images.
- Assumes linear, rectangular raster scanning pattern; non-standard or spiral acquisition patterns may not be correctly represented.
- The mzML file must contain sufficient scan metadata (scan count, filter strings); truncated or malformed mzML files may fail alignment.
- Pixel alignment alone does not correct for mass accuracy errors or peak picking artifacts; downstream metadata annotation is required for full imzML compliance.

## Evidence

- [other] Call iw_utils.mzML_to_imzML_convert(PATH=mzML_path) to write barebones imzML structure and align pixels according to X scan speed (µm/s) and Y step size (µm) parameters.: "Call iw_utils.mzML_to_imzML_convert(PATH=mzML_path) to write barebones imzML structure and align pixels according to X scan speed (µm/s) and Y step size (µm) parameters."
- [methods] Type in the experimental parameters (i.e., X scan speed, Y step, Lock mass) and choose the MS data mode of interest (i.e., Centroid or Profile): "Type in the experimental parameters (i.e., X scan speed, Y step, Lock mass) and choose the MS data mode of interest (i.e., Centroid or Profile)"
- [methods] Click on any pixel on the ion image, the pixel will turn red and the corresponding mass spectrum will be shown on the right.: "Click on any pixel on the ion image, the pixel will turn red and the corresponding mass spectrum will be shown on the right."
- [methods] imzML Writer relies on MS convert to convert raw instrument data into the open format mzML, requiring a working install.: "imzML Writer relies on MS convert to convert raw instrument data into the open format mzML, requiring a working install."
