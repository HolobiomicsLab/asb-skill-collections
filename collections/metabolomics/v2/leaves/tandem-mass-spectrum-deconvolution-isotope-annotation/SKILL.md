---
name: tandem-mass-spectrum-deconvolution-isotope-annotation
description: 'Use when you have aligned features characterized across multiple dimensions
  (m/z, drift time, retention time) and need to: (1) resolve MS/MS spectra that may
  contain fragments from multiple co-eluting or co-mobilizing precursors; (2) identify
  and validate isotopic signatures (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - DEIMoS
  - conda
  - pip
  - Python
  - Snakemake
  - ProteoWizard msconvert
  - HDF5 (h5py / pytables)
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python
  application programming interface and command-line tool
- import deimos
- Use conda to create a virtual environment with required dependencies.
- 'Install DEIMoS using pip: pip install -e .'
- is a Python application programming interface and command-line tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c05017
  all_source_dois:
  - 10.1021/acs.analchem.1c05017
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-mass-spectrum-deconvolution-isotope-annotation

## Summary

This skill resolves convolved tandem mass spectra (MS/MS) into individual component spectra and annotates detected features with their isotopic signatures, enabling accurate molecular characterization in high-dimensional mass spectrometry workflows. It is essential for disambiguating overlapping fragmentation patterns and linking isotopologue patterns to detected features in multidimensional datasets.

## When to use

Apply this skill when you have aligned features characterized across multiple dimensions (m/z, drift time, retention time) and need to: (1) resolve MS/MS spectra that may contain fragments from multiple co-eluting or co-mobilizing precursors; (2) identify and validate isotopic signatures (e.g., ¹²C/¹³C, ¹⁶O/¹⁸O patterns) associated with detected features to confirm molecular identity and improve confidence in feature matching across study samples. The skill is most valuable when dealing with complex, high-dimensional datasets where convolution artifacts in tandem mass spectra are likely.

## When NOT to use

- Input data are already at the compound/metabolite identification level (e.g., library-matched spectra or validated structure assignments) — further isotope deconvolution is redundant.
- MS/MS spectra are from low-resolution instruments or have poor fragmentation coverage; deconvolution and isotope assignment will lack statistical support.
- Dataset contains only MS1 features with no associated tandem mass spectra; isotope detection can proceed, but MS/MS deconvolution cannot.

## Inputs

- Aligned feature table (HDF5 format with 'features' dataset containing detected features across samples)
- MS/MS spectral data (HDF5 'ms2' dataset or mzML.gz format with tandem mass spectra)
- Drift time and retention time dimensions for each feature and spectrum
- Peak-detected MS1 data (threshold-filtered intensity values)

## Outputs

- Deconvolved MS/MS spectra (individual fragment ion spectra resolved from convoluted raw spectra)
- Isotope table (HDF5 'isotopes' dataset with isotopologue assignments, including mass differences and intensity ratios)
- Annotated feature table linking each feature to its isotopic signature and deconvolved MS/MS spectrum
- Quality metrics (e.g., isotopic pattern confidence scores, deconvolution residuals)

## How to apply

Within the DEIMoS workflow, MS/MS spectral deconvolution and isotope detection operate as sequential downstream steps after feature alignment and CCS calibration. (1) Load the aligned feature table and associated MS/MS spectra (typically from HDF5 output of feature detection and alignment stages). (2) Apply DEIMoS deconvolution algorithms to decompose convoluted MS/MS spectra into constituent fragments, leveraging all available dimensions to separate overlapping signals and reduce noise. (3) Extract isotopic patterns from aligned features by examining mass differences and intensity ratios consistent with natural isotope abundance (e.g., at least 3 members for a credible isotopic signature). (4) Annotate each feature with its isotopic composition and link deconvolved MS/MS spectra to the corresponding isotopic signature. (5) Validate by confirming that isotopic patterns follow expected elemental composition rules and that deconvolved spectra have improved signal-to-noise and interpretability compared to raw convoluted spectra. The multidimensional approach is crucial: simultaneous use of m/z, drift time, and retention time dimensions improves feature separation and reduces false positive isotope assignments.

## Related tools

- **DEIMoS** (Core Python API and CLI tool executing MS/MS deconvolution and isotope detection algorithms within the Snakemake workflow; processes multidimensional MS data and outputs HDF5 feature and isotope tables.) — http://github.com/pnnl/deimos
- **Snakemake** (Workflow orchestration engine that chains feature detection, alignment, CCS calibration, MS/MS deconvolution, and isotope detection as sequential Snakemake rules, automatically handling input/output dependencies.)
- **conda** (Environment and dependency manager; creates isolated virtual environment with all required DEIMoS and supporting library versions.)
- **ProteoWizard msconvert** (Format conversion utility for converting proprietary vendor MS data formats (e.g., .raw, .d) to mzML.gz, which DEIMoS accepts as input.)
- **HDF5 (h5py / pytables)** (Underlying file format for storing and retrieving aligned features, MS/MS spectra, and isotope tables; enables efficient access to multidimensional arrays.)

## Examples

```
deimos --config config.yaml --cores 8
```

## Evaluation signals

- Verify that the 'isotopes' dataset in the output HDF5 file is non-empty and contains rows with at least 3 isotopologue members and mass differences matching expected elemental compositions (e.g., 1.003 Da for ¹³C offset).
- Confirm that deconvolved MS/MS spectra show reduced convolution artifacts and improved signal-to-noise compared to raw input spectra by visual inspection or peak count/intensity ratio metrics.
- Check that all detected features in the output have been assigned an isotope group (or explicitly marked as singleton features with no isotope partner), with no missing or null isotope annotations.
- Validate that intensity ratios between isotopologues match natural abundance predictions (e.g., ¹³C/¹²C ratio ~1.1% per carbon atom) within a realistic tolerance, indicating chemically plausible assignments.
- Confirm that MS/MS deconvolution achieves higher alignment/feature matching confidence by re-running feature alignment on deconvolved spectra and comparing match scores or consensus spectrum quality metrics to pre-deconvolution results.

## Limitations

- Isotope detection relies on sufficient intensity and peak resolution; low-abundance features or features with poor m/z or drift-time resolution may fail to identify valid isotopic partners.
- Deconvolution algorithm performance depends on the degree of spectral overlap and the quality of the multidimensional separation (drift time and retention time); highly convoluted spectra from poorly resolved instruments may not deconvolve cleanly.
- The skill requires complete, multi-dimensional data (m/z, drift time, retention time); datasets missing one or more dimensions will lose the separation benefit and may produce lower-confidence results.
- No built-in changelog or versioning documentation is available in the DEIMoS repository, making it difficult to track algorithmic changes or validate reproducibility across software versions.

## Evidence

- [intro] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [intro] mitigate convolution artifacts in tandem mass spectra: "mitigate convolution artifacts in tandem mass spectra"
- [intro] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
- [intro] algorithm implementations simultaneously utilize all dimensions to offer greater separation between features: "algorithm implementations simultaneously utilize all dimensions to offer greater separation between features, thus improving detection sensitivity"
- [results] A good first screening is to only consider those isotopic signatures with at least 3 members: "A good first screening is to only consider those isotopic signatures with at least 3 members."
- [other] detected features aligned across study samples and characterized by mass, CCS, tandem mass spectra, and isotopic signature: "detected features aligned across study samples and characterized by mass, CCS, tandem mass spectra, and isotopic signature"
