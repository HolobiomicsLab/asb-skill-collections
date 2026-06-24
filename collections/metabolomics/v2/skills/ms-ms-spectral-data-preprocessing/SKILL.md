---
name: ms-ms-spectral-data-preprocessing
description: Use when when you have MS/MS spectral data (raw or intermediate format)
  that must be fed into the Mass2SMILES Docker container or similar deep learning
  models for MS/MS-to-structure inference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Mass2SMILES Docker container
  - GNPS (Global Natural Products Social Molecular Networking)
  - Docker
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2023.07.06.547963v1
  title: Mass2SMILES
- doi: 10.5281/zenodo.14778327
  title: ''
evidence_spans:
- open-source Python based deep learning approach
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2smiles_cq
    doi: 10.1101/2023.07.06.547963v1
    title: Mass2SMILES
  dedup_kept_from: coll_mass2smiles_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2023.07.06.547963v1
  all_source_dois:
  - 10.1101/2023.07.06.547963v1
  - 10.5281/zenodo.14778327
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-ms-spectral-data-preprocessing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Prepare and format tandem mass spectrometry (MS/MS) spectral data as GNPS-style MGF files for downstream deep learning-based structure prediction. This skill bridges raw or intermediate spectral formats into the standardized input required by Mass2SMILES and similar inference pipelines.

## When to use

When you have MS/MS spectral data (raw or intermediate format) that must be fed into the Mass2SMILES Docker container or similar deep learning models for MS/MS-to-structure inference. Use this skill when your input is NOT already in GNPS-style MGF format, or when you need to validate and organize spectral files before launching containerized inference.

## When NOT to use

- Input is already a validated GNPS-style MGF file and ready for inference — skip directly to containerized inference.
- Your downstream tool does not require MGF format or has its own preferred spectral input format (e.g., vendor-specific peak lists or proprietary databases).
- You are performing untargeted feature detection or spectral clustering — use dedicated MS/MS preprocessing pipelines (e.g., XCMS, MzMine) instead.

## Inputs

- MS/MS spectral data in raw instrument format (e.g., .raw, .mzML, .mzXML, or vendor-specific binary)
- GNPS-style MGF files (partially prepared or requiring validation)
- Spectral metadata (precursor m/z, fragment peaks, intensity values, retention time)

## Outputs

- GNPS-style MGF file(s) organized in input directory
- Validated spectral records ready for Mass2SMILES Docker container inference

## How to apply

Convert or validate your MS/MS spectral data into GNPS-style MGF file format, ensuring each spectrum includes precursor m/z, fragment ion peaks, and associated metadata (retention time, intensity, scan number if available). Organize MGF files into a designated input directory that will be mounted into the Mass2SMILES Docker container. Verify MGF syntax and completeness before invoking the container, as malformed spectra will fail or produce unreliable structure predictions. The MGF format is preferred by GNPS and Mass2SMILES because it is human-readable, widely supported, and preserves both precursor and fragmentation information needed for the deep learning model to generate predicted SMILES structures.

## Related tools

- **Mass2SMILES Docker container** (Containerized deep learning inference engine that accepts GNPS-style MGF files as input and outputs predicted SMILES structures) — https://hub.docker.com/r/delser292/mass2smiles
- **GNPS (Global Natural Products Social Molecular Networking)** (Community platform that defines and standardizes MGF spectral file format for MS/MS data sharing and analysis)
- **Python** (Primary language for reading, validating, and converting spectral data into MGF format) — https://github.com/volvox292/mass2smiles
- **Docker** (Containerization platform used to run Mass2SMILES with mounted input/output directories for spectral processing)

## Examples

```
docker run -v /path/to/your/mgf_files:/app mass2smiles:transformer_v1 conda run -n tf python app/mass2smiles_transformer.py your_sample.mgf /app
```

## Evaluation signals

- MGF file syntax is valid: each spectrum block contains BEGIN IONS and END IONS delimiters; precursor m/z and charge are specified; fragment peaks are listed as 'mz intensity' pairs.
- All spectra include mandatory GNPS-style metadata: PRECURSORMZ, PRECURSORTYPE or CHARGE, and TITLE fields.
- MGF files mount successfully into the Mass2SMILES Docker container via `-v` volume binding without I/O errors.
- The Mass2SMILES inference completes without reporting missing or malformed spectral records; output SMILES predictions are generated for all input spectra.
- Spectral intensity values and m/z ranges are within realistic ranges for the instrument and ionization method used (e.g., no negative intensities, m/z > 0, fragment m/z ≤ precursor m/z).

## Limitations

- MGF format does not preserve all vendor-specific metadata or raw signal-to-noise ratios; conversion may lose instrument-specific calibration or acquisition parameters.
- GNPS-style MGF preparation requires knowledge of precursor charge state and ionization mode; ambiguity or missing metadata can degrade downstream model predictions.
- No built-in changelog or versioning in the Mass2SMILES repository; MGF format compliance may shift across container versions (see Zenodo 10.5281/zenodo.14778327 for recent updates).
- GPU vs. CPU inference trade-off: the provided container uses TensorFlow CPU because CUDA driver compatibility issues; preprocessing must account for inference latency when choosing to preprocess speculatively.

## Evidence

- [intro] Spectral data can be provided as MGF files (GNPS-syle): "Spectral data can be provided as MGF files (GNPS-syle)"
- [readme] mass2smiles is an open-source Python based deep learning approach for structure and functional group prediction from mass spectrometry data (MS/MS): "Mass2SMILES is an open-source Python based deep learning approach for structure and functional group prediction from mass spectrometry data (MS/MS)"
- [readme] model inference is most effciently performed via the provided docker container: "model inference is most effciently performed via the provided docker container"
- [readme] You need to point to your input and output dir: "You need to point to your input and output dir, now the mass2smiles model is built into the container"
- [readme] the container is available as tarball in supplementary or via docker pull delser292/mass2smiles:final: "the container is available as tarball in supplementary or via docker pull delser292/mass2smiles:final"
