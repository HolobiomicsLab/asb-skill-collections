---
name: msi-metadata-curation-and-storage
description: Use when after generating a 3D pixel array (shape n+1, y, x) from raw line-scan MSI data via MSIGen's get_image_data() call, curate and validate the accompanying JSON metadata file before visualization or downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MSIGen
  - Python
  - Jupyter Notebook
  - pyBaf2Sql
derived_from:
- doi: 10.1021/jasms.4c00178
  title: MSIGen
evidence_spans:
- MSIGen provides tools for processing mass spectrometry imaging data acquired in line-scan mode into images and figures.
- from MSIGen import msigen
- Using an environment with python version >=3.9 and <=3.11
- If you want to use MSIGen in a Jupyter notebook, you may also need to install jupyter notebook
- MSIGen is most easily used through Jupyter Notebooks or through the GUI.
- If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msigen_cq
    doi: 10.1021/jasms.4c00178
    title: MSIGen
  dedup_kept_from: coll_msigen_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00178
  all_source_dois:
  - 10.1021/jasms.4c00178
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MSI Metadata Curation and Storage

## Summary

Curate and store standardized JSON metadata accompanying mass spectrometry imaging pixel arrays, encoding acquisition geometry, mass list definitions, tolerances, and processing parameters to enable reproducible visualization and analysis downstream. This skill ensures that the pixels.npy output and its corresponding pixels_metadata.json are complete, consistent, and machine-readable.

## When to use

After generating a 3D pixel array (shape n+1, y, x) from raw line-scan MSI data via MSIGen's get_image_data() call, curate and validate the accompanying JSON metadata file before visualization or downstream analysis. Trigger this skill when: (1) you have completed spectral extraction, m/z matching within tolerances, and spatial binning; (2) you are about to visualize ion images or generate derived products (ratio/fractional abundance images); or (3) you need to archive or share processed MSI datasets with full provenance.

## When NOT to use

- Input is raw, unprocessed line-scan MSI data that has not yet been passed through MSIGen's get_image_data() pipeline — extract and bin spectra first.
- You are working with already-processed and archived MSI datasets where metadata has been frozen and requires no updates or re-curation.
- Your workflow uses a non-MSIGen pipeline (e.g., direct MATLAB, Bruker flexAnalysis, or vendor-specific tools) that does not produce pixels.npy and pixels_metadata.json; adapt the metadata schema manually or use vendor documentation.

## Inputs

- raw line-scan MSI data file (Agilent .d, Bruker .tsf/.baf/.baf, Thermo .raw, or .mzML)
- mass list file (Excel .xlsx or CSV with columns: m/z, precursor m/z, fragment m/z, ion mobility)
- MSIGen processing parameters object (file path, mass tolerances, image dimensions, normalization mode)
- pixels.npy array (output from get_image_data(), shape (n+1, y, x))

## Outputs

- pixels_metadata.json file with acquisition geometry, mass definitions, applied tolerances, normalization settings, and processing metadata
- validated metadata dictionary (Python dict) ready for downstream visualization functions

## How to apply

After calling MSIGen's get_image_data(verbose=True), the pixels_metadata.json file is automatically generated with fields encoding: (1) scanned area dimensions (height, width in mm or specified units); (2) image normalization mode (e.g., 'TIC', 'intl_std', or 'none'); (3) mass list entries with m/z, precursor m/z, fragment m/z, and ion mobility values; (4) applied tolerance thresholds (mass_tolerance_MS1 in ppm/mz, mass_tolerance_prec, mass_tolerance_frag, mobility_tolerance in 1/K0 or μs); (5) pixels-per-line normalization strategy (max, min, or mean). Verify that all metadata keys match the pixel array dimensions and that the mass list cardinality matches the first n dimensions of pixels. Store the .json alongside pixels.npy in the specified output directory. This metadata must be loaded and passed to downstream visualization functions (e.g., vis.get_and_display_images(), vis.ratio_images()) to ensure correct image interpretation.

## Related tools

- **MSIGen** (generates pixels.npy and pixels_metadata.json via get_image_data(); defines metadata schema) — https://github.com/LabLaskin/MSIGen
- **Python** (runtime and scripting environment for metadata curation and JSON I/O)
- **Jupyter Notebook** (interactive environment for loading, inspecting, and curating metadata with MSIGen_jupyter.ipynb) — https://github.com/LabLaskin/MSIGen/blob/main/other_files/MSIGen_jupyter.ipynb
- **pyBaf2Sql** (optional dependency for reading and parsing Bruker .baf format data before metadata generation) — https://github.com/gtluu/pyBaf2Sql

## Examples

```
metadata, pixels = MSIGen_generator.get_image_data(verbose=True); import json; with open('pixels_metadata.json') as f: meta = json.load(f); print(f"Masses: {len(meta['mass_list'])}, Dimensions: {meta['img_height']} x {meta['img_width']}, Normalization: {meta.get('normalize')}")
```

## Evaluation signals

- pixels_metadata.json file is written to the specified output directory and is valid JSON parseable by json.load().
- Metadata dictionary keys include: 'img_height', 'img_width', 'pixels_per_line', 'normalize_img_sizes', 'mass_list' (with per-mass entries containing m/z, precursor m/z, fragment m/z, ion mobility as applicable), 'mass_tolerance_MS1', 'mass_tolerance_prec', 'mass_tolerance_frag', 'mobility_tolerance', and their corresponding unit fields.
- The number of mass entries in metadata['mass_list'] equals n (i.e., the first dimension of pixels.npy minus 1, since one channel is TIC).
- Image dimensions in metadata (img_height × img_width) are consistent with the spatial dimensions (y, x) of pixels.npy.
- Applied tolerances (ppm, mz, 1/K0, μs units) and normalization mode are recorded and match the parameters passed to get_image_data(); verified by loading the file and passing to vis.get_and_display_images() without error.
- Metadata persists through checkpoint save/load cycle: pixels, metadata = msigen.load_pixels(output_dir) recovers all fields without loss or corruption.

## Limitations

- MSIGen metadata generation is automatic and non-interactive; users cannot manually edit or validate individual m/z matches or tolerance applicability before metadata is written. Post-hoc JSON editing is possible but not officially supported.
- Ion mobility tolerance and ion mobility values are only populated if the input file format supports ion mobility (e.g., Bruker .tdf); other formats will have null or omitted mobility fields.
- No changelog or version tracking is embedded in pixels_metadata.json; users must manually document which MSIGen version and parameter commit produced a given output.
- Metadata does not encode individual spectrum-level QC metrics (e.g., signal-to-noise, spectral quality flags, or per-pixel abundance statistics); these must be computed and stored separately if needed.
- The 'normalize_img_sizes' field records the normalization strategy but does not store the raw (pre-normalized) pixels-per-line values for each line; reconstruction of the original spatial resolution requires the raw input file.

## Evidence

- [other] Generate both a NumPy pixel array and JSON metadata as intermediate outputs for subsequent visualization: "MSIGen converts raw line-scan MSI data to a visualizable format by processing the data through a pipeline that generates both a NumPy pixel array and JSON metadata as intermediate outputs for"
- [methods] Generate a 3D array with JSON metadata encoding acquisition parameters and mass list: "bin pixels spatially, and generate a 3D array of shape (n+1, y, x) where n is the number of masses plus one TIC image. 5. Verify output files pixels.npy and pixels_metadata.json are written to the"
- [methods] Define and pass tolerance parameters to MSIGen for metadata-driven downstream analysis: "Define processing parameters: specify the input file path (Agilent .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .mzML), mass list file (Excel or CSV with m/z, precursor m/z, fragment m/z, and/or ion"
- [methods] Metadata is passed to visualization and image processing functions: "Visualize and display ion images with normalization options [evidence='vis.get_and_display_images(pixels, metadata, normalize, std_idx, ...)'] Generate fractional abundance images"
- [methods] Load previously saved NumPy array and metadata files for reproducible reanalysis: "Load previously saved NumPy array and metadata files [evidence='pixels, metadata = msigen.load_pixels(load_path)']"
- [readme] MSIGen is designed for converting MSI data from raw line-scan data to visualizable format with metadata: "MSIGen is designed for converting mass spectrometry imaging (MSI) data from the raw line-scan data to a visualizable format and is designed with nano-DESI MSI in mind."
