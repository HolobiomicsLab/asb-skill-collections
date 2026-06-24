---
name: gnps-mgf-format-handling
description: Use when you have mass spectrometry MS/MS spectral data in GNPS-style
  MGF format and need to feed it into the Mass2SMILES deep learning model for structure
  and functional group prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Mass2SMILES Docker container
  - Docker
  - Python (TensorFlow-based inference script)
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2023.07.06.547963v1
  title: Mass2SMILES
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# GNPS-style MGF format handling for mass spectrometry spectral input

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Accept and prepare GNPS-style MGF (mascot generic format) spectral files as standardized input for deep learning–based MS/MS structure prediction workflows. This skill bridges public spectral repositories (GNPS) and containerized inference pipelines by ensuring spectral data is in the correct format and accessible to the processing container.

## When to use

You have mass spectrometry MS/MS spectral data in GNPS-style MGF format and need to feed it into the Mass2SMILES deep learning model for structure and functional group prediction. Use this skill when you are preparing spectral files for containerized inference, or when you have downloaded public spectra from GNPS that require reformatting or validation before Docker-based processing.

## When NOT to use

- Input spectral data is already in a non-MGF format (e.g., mzML, mzXML, or vendor-specific formats) — convert to MGF first using appropriate tools (e.g., MSConvert) before using this skill.
- You intend to perform spectral matching or library search — this skill is for structure prediction from MS/MS fragmentation patterns, not spectral similarity matching.
- The MGF file lacks required metadata fields (precursor m/z, charge) or contains only MS1 data without fragment ion peaks — Mass2SMILES requires full MS/MS spectra.

## Inputs

- GNPS-style MGF files (text format containing precursor m/z, charge state, and fragment ion peaks)
- Input directory path (mounted into container)
- MGF filename or file path (passed as argument to the inference script)

## Outputs

- Predicted SMILES structures (written to output directory by the container)
- Inference results (format determined by Mass2SMILES output writer)

## How to apply

Place GNPS-style MGF files into a designated input directory that will be mounted as a volume into the Mass2SMILES Docker container. The MGF format contains precursor m/z, charge, and fragment ion intensities in a text-based structure that Mass2SMILES expects. Specify the input directory path and MGF filename when invoking the container (e.g., via the `docker run` command with `-v` volume mount and the MGF file argument). The container will parse the spectral data, pass it through the transformer-based model, and write predicted SMILES structures to the mounted output directory. Validation occurs implicitly: the container will fail to parse malformed MGF files or ones missing required fields (precursor m/z, MS/MS fragment peaks).

## Related tools

- **Mass2SMILES Docker container** (Performs inference on MGF spectral input; requires MGF files mounted in input directory and writes predictions to output directory) — https://github.com/volvox292/mass2smiles
- **Docker** (Container runtime that mounts input/output directories and executes the Mass2SMILES inference pipeline with volume bindings for MGF input and SMILES output)
- **Python (TensorFlow-based inference script)** (Parses MGF format and orchestrates deep learning model inference within the container) — https://github.com/volvox292/mass2smiles

## Examples

```
docker run -v /local/path/to/mass2smiles:/app delser292/mass2smiles:final conda run -n tf python app/mass2smiles_transformer.py input_spectra.mgf /app
```

## Evaluation signals

- MGF file is accepted by the Docker container without parse errors; container initializes without 'malformed MGF' or 'missing fields' exceptions.
- Output directory contains SMILES predictions corresponding to the number of spectra in the input MGF file (one prediction per spectrum).
- Predicted SMILES are valid chemical notations (parseable by RDKit or other cheminformatics libraries); functional group annotations align with expected fragmentation patterns from the input m/z peaks.
- Container execution completes without I/O errors on the mounted input and output directories; file permissions and volume mount paths are correctly configured.
- Inference latency is acceptable; if GPU is available, speed is noticeably improved; CPU inference can be tuned via the `cpu_threads` parameter in the InferenceModel call.

## Limitations

- GNPS-style MGF files must contain complete MS/MS spectra (precursor m/z, charge state, and fragment peaks); files with only MS1 or incomplete metadata will cause parse failures.
- The Mass2SMILES model inference is built into the container; older versions (Zenodo 7883491) required separate model file setup, which is error-prone — use the recent update container (Zenodo 14778327) to avoid manual model path configuration.
- CDDD component does not work reliably on newer CUDA drivers; the container uses TensorFlow CPU as a fallback, which reduces inference speed — GPU speedup is available but requires driver compatibility validation.
- No changelog is available for the Mass2SMILES model; incremental updates or model retraining events are not publicly documented, making it difficult to assess whether predictions from different container versions are directly comparable.
- MGF format is text-based and can be large for high-resolution MS/MS datasets; very large files may encounter memory or I/O bottlenecks depending on container resource limits and disk mount performance.

## Evidence

- [intro] Spectral data input format specification: "Spectral data can be provided as MGF files (GNPS-syle)"
- [readme] Container-based inference requirement: "model inference is most effciently performed via the provided docker container"
- [intro] Deep learning capability for structure prediction: "deep learning approach for structure and functional group prediction from mass spectrometry data (MS/MS)"
- [readme] Container deployment method: "the container is available as tarball in supplementary or via docker pull delser292/mass2smiles:final"
- [readme] Volume mount and file path specification: "You need to point to your input and output dir, now the mass2smiles model is built into the container"
- [readme] Example Docker invocation with MGF argument: "docker run -v c:/your_path/to_the_folder/mass2smiles/:/app  mass2smiles:transformer_v1 conda run -n tf python app/mass2smiles_transformer.py your_mgf_file.mgf /app"
- [readme] CUDA/TensorFlow compatibility note: "cddd does not seem to work on newer cuda drivers, therefore it is build using tensorflow cpu"
