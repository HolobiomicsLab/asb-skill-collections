---
name: mass-tolerance-parameter-calibration
description: Use when when converting raw line-scan mass spectrometry imaging data (Agilent .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .mzML formats) and must decide which m/z values from a reference mass list correspond to peaks in the raw spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MSIGen
  - Python
  - Jupyter Notebook
  - pyBaf2Sql
  techniques:
  - MS-imaging
  - ion-mobility-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-tolerance-parameter-calibration

## Summary

Calibrate mass-to-charge (m/z) and ion mobility tolerance windows for matching observed spectra against a reference mass list during line-scan MSI data processing. Correct tolerance settings are critical for accurate feature extraction and prevent false positive or false negative ion assignments.

## When to use

When converting raw line-scan mass spectrometry imaging data (Agilent .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .mzML formats) and must decide which m/z values from a reference mass list correspond to peaks in the raw spectra. Tolerances are required separately for MS1 precursor ions, MS2 fragment ions, and ion mobility dimensions when applicable.

## When NOT to use

- Input is already a pre-processed feature table or image matrix — tolerance calibration applies only to raw spectrum–to–mass list matching.
- Mass list file is absent or malformed — tolerance parameters cannot be applied without a reference list to match against.
- Ion mobility dimension is not present in the raw data — mobility_tolerance and mobility_tolerance_units should not be specified.

## Inputs

- Input file path (raw MSI data: Agilent .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .mzML)
- Mass list file (Excel or CSV with m/z, precursor m/z, fragment m/z, and/or ion mobility columns)
- Instrument mass accuracy specification (ppm or m/z error)

## Outputs

- Matched m/z–intensity pairs within tolerance windows for each spatial pixel
- 3D pixel array of shape (n+1, y, x) where n is the number of matched masses (plus one TIC image)
- JSON metadata file recording tolerance parameter values used for reproducibility

## How to apply

Define three independent mass tolerance parameters before calling get_image_data(): (1) mass_tolerance_MS1 and mass_tolerance_MS1_units for matching m/z values in MS1 spectra (typically ppm or mz); (2) mass_tolerance_prec and mass_tolerance_prec_units for precursor ions in MS2 spectra; (3) mass_tolerance_frag and mass_tolerance_frag_units for fragment ions in MS2 spectra. If ion mobility data is present (e.g., TIMS), also set mobility_tolerance and mobility_tolerance_units (1/K0 or μs). These tolerances act as match windows: a peak in the raw spectrum is assigned to a mass list entry only if its observed m/z (or mobility value) falls within the tolerance window of the reference value. Tighter tolerances reduce false positives but risk missing true signals; looser tolerances increase sensitivity but risk spurious assignments. Choose tolerances based on your instrument's mass accuracy specification and the expected resolution of your MSI acquisition.

## Related tools

- **MSIGen** (Calls get_image_data(verbose=True) with mass tolerance parameters to extract and match spectra against mass list within the specified windows) — https://github.com/LabLaskin/MSIGen
- **pyBaf2Sql** (Decodes Bruker .baf files to extract raw spectra for tolerance-based matching) — https://github.com/gtluu/pyBaf2Sql
- **Python** (Runtime environment (≥3.9 and ≤3.11) for defining and passing tolerance parameters to MSIGen)

## Examples

```
MSIGen_generator = msigen(example_file='sample.d', mass_list_dir='masses.csv', mass_tolerance_MS1=5, mass_tolerance_MS1_units='ppm', mass_tolerance_prec=10, mass_tolerance_prec_units='ppm', mass_tolerance_frag=20, mass_tolerance_frag_units='ppm', img_height=10, img_width=10); metadata, pixels = MSIGen_generator.get_image_data(verbose=True)
```

## Evaluation signals

- Verify that the output 3D pixel array has shape (n+1, y, x) where n equals the number of masses in the reference list successfully matched within tolerance windows; dimension mismatch indicates tolerance miscalibration or mass list parsing failure.
- Check that pixels_metadata.json contains recorded values for all tolerance parameters (mass_tolerance_MS1, mass_tolerance_prec, mass_tolerance_frag, mobility_tolerance if applicable) for reproducibility.
- Visually inspect ion images for expected signal distribution and absence of obvious artifacts; excessively sparse images suggest tolerances too tight; noisy or chemically implausible images suggest tolerances too loose.
- Cross-validate by re-running with tighter and looser tolerance bounds (e.g., ±50% adjustment) and comparing output TIC and ion image intensities; large changes indicate parameter sensitivity.
- If external reference imaging data or known spatial annotations exist, compare the spatial patterns in tolerance-matched images to the ground truth; correlation or AUC should remain high across reasonable tolerance ranges.

## Limitations

- Tolerance values are fixed across all spectra in the dataset; dynamic, spectrum-dependent calibration is not supported by MSIGen.
- No automated tolerance optimization is provided; users must select values a priori based on instrument specifications or manual calibration experiments.
- Separate tolerances for MS1, precursor, and fragment ions require prior knowledge of whether the raw data contains MS2 spectra; inapplicable tolerances are silently ignored.
- Ion mobility tolerance relies on accurate mobility calibration in the raw file; uncalibrated or poorly calibrated mobility axes will yield spurious or missed matches even with correct tolerance windows.

## Evidence

- [other] Define processing parameters: specify the input file path (Agilent .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .mzML), mass list file (Excel or CSV with m/z, precursor m/z, fragment m/z, and/or ion mobility columns), and MS1 mass tolerance (ppm or mz), precursor ion tolerance, fragment ion tolerance, and mobility tolerance (1/K0 or μs).: "mass list file (Excel or CSV with m/z, precursor m/z, fragment m/z, and/or ion mobility columns), and MS1 mass tolerance (ppm or mz), precursor ion tolerance, fragment ion tolerance, and mobility"
- [other] match m/z values and mobility values within tolerances, bin pixels spatially, and generate a 3D array of shape (n+1, y, x) where n is the number of masses plus one TIC image.: "match m/z values and mobility values within tolerances, bin pixels spatially, and generate a 3D array of shape (n+1, y, x) where n is the number of masses plus one TIC image"
- [methods] Mass tolerance filtering for MS1 spectra  [section=methods; evidence='mass_tolerance_MS1, mass_tolerance_MS1_units for matching m/z values in MS1 spectra']; Precursor ion mass tolerance filtering  [section=methods; evidence='mass_tolerance_prec, mass_tolerance_prec_units for precursor ions in MS2 spectra']; Fragment ion mass tolerance filtering  [section=methods; evidence='mass_tolerance_frag, mass_tolerance_frag_units for fragment ions in MS2 spectra']; Ion mobility tolerance filtering  [section=methods; evidence='mobility_tolerance, mobility_tolerance_units for matching ion mobility values']: "mass_tolerance_MS1, mass_tolerance_MS1_units for matching m/z values in MS1 spectra; mass_tolerance_prec, mass_tolerance_prec_units for precursor ions in MS2 spectra; mass_tolerance_frag,"
- [other] Initialize the msigen object with all parameters and call get_image_data(verbose=True) to extract spectra, match m/z values and mobility values within tolerances: "Initialize the msigen object with all parameters and call get_image_data(verbose=True) to extract spectra, match m/z values and mobility values within tolerances"
