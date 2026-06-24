---
name: ms2-spectral-deconvolution-and-annotation
description: Use when you have acquired LC-IMS-MS/MS data (or equivalent multidimensional
  MS/MS acquisition) in mzML or mzML.gz format and need to disambiguate overlapping
  fragmentation spectra arising from co-eluting or co-drifting precursor ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DEIMoS
  - Python
  - conda
  - pip
  - Snakemake
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- Functionality includes feature detection, feature alignment, collision cross section
  (CCS) calibration, isotope detection, and MS/MS spectral deconvolution
- import deimos
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
- Use `conda <https://www.anaconda.com/download/>`_ to create a virtual environment
  with required dependencies.
- 'Install DEIMoS using `pip <https://pypi.org/project/pip/>`_: ``pip install -e .``'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos_cq
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos_cq
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

# MS/MS spectral deconvolution and annotation

## Summary

Separate and characterize individual precursor ion fragmentation spectra from multiplexed tandem mass spectrometry data acquired across multiple separation dimensions (m/z, retention time, drift time). DEIMoS applies N-dimensional algorithmic implementations to mitigate convolution artifacts and assign fragment ions to their parent precursors, enabling confident annotation of tandem spectra characterized by mass, CCS, and isotopic signature.

## When to use

You have acquired LC-IMS-MS/MS data (or equivalent multidimensional MS/MS acquisition) in mzML or mzML.gz format and need to disambiguate overlapping fragmentation spectra arising from co-eluting or co-drifting precursor ions. This is especially critical when precursors share similar m/z values but differ in retention time or collision cross section, where traditional 2D MS/MS assignment would conflate fragments.

## When NOT to use

- Input is already a deconvolved feature table or spectral library (redundant application).
- MS data is 1D or 2D only (e.g., no drift time / IMS dimension); N-dimensional deconvolution adds limited value if separation dimensions are missing.
- Precursor feature detection has not yet been performed on MS1 data; deconvolution requires known precursor coordinates to anchor fragment assignment.

## Inputs

- mzML or mzML.gz files with multidimensional MS/MS data (MS level ≥ 2)
- Parsed accession metadata mapping (retention_time, drift_time, m/z)
- Precursor feature table (output of feature detection on MS1 data)
- Intensity threshold parameter (e.g., 500 counts minimum)

## Outputs

- Deconvolved tandem mass spectra assigned to individual precursor features
- Fragment ion annotations (m/z, intensity, drift_time, retention_time coordinates)
- Feature table enriched with tandem spectral information and fragmentation patterns

## How to apply

Load multidimensional MS/MS data from mzML.gz files by parsing accession fields (e.g., 'MS:1000016' for retention_time, 'MS:1002476' for drift_time) using DEIMoS's load API. Apply threshold filtering (e.g., threshold=500) to remove low-intensity noise, then execute the MS/MS spectral deconvolution workflow as part of the DEIMoS pipeline, which correlates fragment peaks to precursor features detected across all separation dimensions. The deconvolution leverages N-dimensional proximity and intensity patterns to assign fragments to their correct precursor, mitigating convolution artifacts that would arise in 2D-only approaches. Verify deconvolution success by checking that tandem spectra are assigned to precursor features with consistent m/z, retention time, drift time, and CCS values; examine the resulting spectral output for fragment ion clarity and absence of high-intensity contaminant peaks inconsistent with fragmentation chemistry.

## Related tools

- **DEIMoS** (Primary API and CLI for N-dimensional MS/MS spectral deconvolution, feature detection, and alignment) — https://github.com/pnnl/deimos
- **Snakemake** (Workflow orchestration framework to compose and execute DEIMoS deconvolution as part of a multi-step processing DAG)
- **ProteoWizard msconvert** (Utility to convert vendor MS data formats to mzML for input to DEIMoS deconvolution)
- **Python** (Runtime environment and API layer for DEIMoS deconvolution logic and custom filtering)

## Examples

```
data = deimos.load('example_data.mzML.gz', accession={'retention_time': 'MS:1000016', 'drift_time': 'MS:1002476'}); deconvolved = deimos.deconvolute_spectra(data, threshold=500)
```

## Evaluation signals

- Verify that each deconvolved tandem spectrum is assigned to a unique precursor feature with consistent m/z, retention_time, and drift_time coordinates across all dimension space.
- Check that fragment ion peaks in the output spectrum do not violate expected charge states or m/z ranges relative to the assigned precursor m/z.
- Confirm that high-intensity artifact peaks are eliminated from tandem spectra compared to raw MS/MS data, indicating successful demultiplexing of overlapping spectra.
- Validate that the number of deconvolved spectra matches or approaches the number of detected precursor features; missing spectra may indicate missed assignments.
- Inspect r-squared values or other alignment confidence metrics (if output) to confirm that deconvolution parameters yielded acceptable spectral quality (target r² > 0.99).

## Limitations

- Deconvolution accuracy depends critically on prior MS1 feature detection quality; erroneous or missed precursor calls propagate to tandem spectrum assignment.
- N-dimensional deconvolution requires multidimensional data (m/z, retention_time, drift_time); performance degrades on 2D or 1D-only acquisitions.
- Threshold filtering (e.g., threshold=500) may remove genuine low-abundance fragment ions; threshold choice requires instrument-specific calibration.
- Spectral deconvolution is agnostic to fragmentation chemistry; assignment confidence depends on sufficient spatial separation between precursors; highly congested m/z or drift_time regions may still yield ambiguous or mixed spectra.

## Evidence

- [readme] MS/MS spectral deconvolution mitigates convolution artifacts via N-dimensional implementations: "algorithm implementations simultaneously utilize all dimensions to (iii) mitigate convolution artifacts in tandem mass spectra"
- [results] DEIMoS loads mzML data by parsing accession fields for multidimensional coordinates: "data = deimos.load('example_data.mzML.gz', accession={'retention_time': 'MS:1000016', 'drift_time': 'MS:1002476'})"
- [intro] MS/MS spectral deconvolution is a core functionality of DEIMoS: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [other] Threshold filtering applied during feature detection and deconvolution: "applies threshold filtering (threshold=500), index building from factors, and persistent homology-based peak detection to identify local maxima fulfilling signal criteria"
