---
name: ion-mobility-filtering-and-tolerance-tuning
description: Use when your raw MSI dataset is acquired on an ion-mobility-enabled instrument (e.g., Bruker .baf, .tsf, or .tdf formats) and your analyte of interest has a known or experimentally determined ion mobility value (1/K0 or drift time μs).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
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

# ion-mobility-filtering-and-tolerance-tuning

## Summary

Apply ion mobility (1/K0 or μs units) tolerance windows during mass spectrometry imaging data processing to selectively extract and bin spectra by collisional cross-section, improving spatial specificity and reducing chemical noise in line-scan MSI workflows. This skill is essential when processing ion-mobility-resolved MSI data from instruments like Bruker timsTOF or when distinguishing isomers and isobars that co-elute in m/z space but separate in mobility space.

## When to use

Use this skill when your raw MSI dataset is acquired on an ion-mobility-enabled instrument (e.g., Bruker .baf, .tsf, or .tdf formats) and your analyte of interest has a known or experimentally determined ion mobility value (1/K0 or drift time μs). Apply it to reduce false positives from isobars, isomers, or background ions that share the same nominal m/z but have distinct mobility signatures, or when you need to extract mobility-resolved spatial images for a multi-pass analysis.

## When NOT to use

- Your raw data is from a non-mobility-resolved instrument (e.g., standard Orbitrap, Q-TOF without ion mobility encoding) — mobility filtering requires multi-dimensional raw data.
- Your mass list file lacks a mobility column or reference mobility values are unavailable — filtering requires a target mobility to define the tolerance window.
- You are processing already-centroided or pre-filtered data where mobility information has been discarded — mobility filtering must occur at the raw spectral extraction stage.

## Inputs

- raw MSI data file in ion-mobility format (.baf, .tsf, .tdf, .raw, or .mzML from an ion-mobility instrument)
- mass list file (Excel .xlsx or .csv) with at least m/z column and ion mobility column (1/K0 or μs)
- numeric mobility tolerance value (e.g., 0.02 1/K0)
- mobility tolerance units string ('1/K0' or 'μs')

## Outputs

- pixels.npy: 3D NumPy array of shape (n+1, y, x) with spatial bins filtered and summed only over spectra within the mobility tolerance window
- pixels_metadata.json: JSON metadata file documenting applied mobility tolerance, units, and per-mass ion mobility range statistics

## How to apply

During MSIGen initialization, define the `mobility_tolerance` parameter (numeric value) and `mobility_tolerance_units` parameter ('1/K0' or 'μs', depending on your instrument and calibration). These tolerances act as a ±window around the target mobility value: only spectra with ion mobility within [target_mobility − tolerance, target_mobility + tolerance] are retained and binned into the output pixel array. Set tolerance conservatively (typically 0.01–0.05 1/K0 or 1–5 μs) based on your instrument resolution and the reference mobility values in your mass list file (which should include a mobility column). Pass these parameters to the `msigen()` object, then call `get_image_data(verbose=True)` to apply the filter during spectral extraction and spatial binning; inspect the resulting pixels.npy array dimensions and metadata to confirm that the number of spatial voxels and intensity distributions reflect successful mobility filtering.

## Related tools

- **MSIGen** (primary tool for applying ion mobility tolerance filtering during spectral extraction and spatial binning in line-scan MSI workflows) — https://github.com/LabLaskin/MSIGen
- **pyBaf2Sql** (underlying library for reading Bruker .baf files with ion mobility data access when processing Bruker instruments) — https://github.com/gtluu/pyBaf2Sql
- **Python** (runtime environment (version ≥3.9 and ≤3.11) for MSIGen and mobility tolerance parameter definition)

## Examples

```
metadata, pixels = MSIGen_generator.get_image_data(verbose=True) where MSIGen_generator = msigen(example_file='sample.baf', mass_list_dir='masses.xlsx', mobility_tolerance=0.02, mobility_tolerance_units='1/K0', ...)
```

## Evaluation signals

- Verify that pixels.npy has expected shape (n+1, y, x) where n is the number of masses in the mass list; mismatched dimensions indicate filtering errors.
- Check pixels_metadata.json for a 'mobility_tolerance' and 'mobility_tolerance_units' field matching your input parameters.
- Qualitatively inspect ion images (via vis.get_and_display_images) for spatial localization consistent with known sample structure; diffuse or absent signal suggests tolerance is too stringent or mobility value is incorrect.
- Compare per-pixel intensity distributions and TIC between a mobility-filtered run and a non-filtered run; mobility filtering should reduce background noise and increase contrast for the target analyte.
- Confirm that all output metadata records the actual mobility range (min/max observed 1/K0 or μs) for each extracted mass, falling within the specified tolerance window.

## Limitations

- Ion mobility tolerance tuning is instrument and ion-specific; 1/K0 or μs values must be obtained experimentally or from reference databases, and calibration drift or unknown analyte structures can render pre-defined tolerances incorrect.
- MSIGen is designed with nano-DESI MSI in mind; applicability to other ion sources (MALDI, ESI-imaging) with different mobility characteristics is not explicitly validated in the source material.
- Very tight mobility tolerances (e.g., <0.005 1/K0) may result in no spectra passing the filter if instrument resolution or analyte heterogeneity is underestimated; conversely, loose tolerances defeat the specificity benefit.
- The mobility tolerance filter is applied uniformly across all line-scan positions; spatial or temporal variations in instrument calibration are not accounted for within a single MSIGen run.

## Evidence

- [other] Set image acquisition parameters: scanned area height and width in specified units (e.g., mm), and whether to normalize all images to the same size using max, min, or mean pixels per line.: "Define processing parameters: specify the input file path (Agilent .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .mzML), mass list file (Excel or CSV with m/z, precursor m/z, fragment m/z, and/or ion"
- [methods] Ion mobility tolerance filtering during spectral extraction and binning is a core MSIGen parameter.: "Ion mobility tolerance filtering  [section=methods; evidence='mobility_tolerance, mobility_tolerance_units for matching ion mobility values']"
- [other] MSIGen processes data by matching m/z and mobility values within tolerances and binning pixels spatially.: "Initialize the msigen object with all parameters and call get_image_data(verbose=True) to extract spectra, match m/z values and mobility values within tolerances, bin pixels spatially, and generate a"
- [intro] MSIGen is designed for nano-DESI MSI, a specific ion source context.: "is designed with nano-DESI MSI in mind"
- [readme] README example initialization shows how parameters are passed to MSIGen.: "An example can be found in the other_files folder. Run the following in Anaconda Prompt: conda activate MSIGen; python "C:/Path/to/MSIGen_CLI.py" "C:/path/to/config_file1.json""
