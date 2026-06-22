---
name: spectral-data-input-handling-mgf-format
description: Use when when you have raw MS/MS mass spectrometry data and need to submit it to the Mass2SMILES Docker inference container for structure and functional group prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Docker
  - mass2smiles_transformer.py
  - delser292/mass2smiles:final
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
---

# spectral-data-input-handling-mgf-format

## Summary

Prepare and validate MS/MS spectral data in GNPS-style MGF format for input to the Mass2SMILES deep learning model. This skill ensures that raw mass spectrometry data is correctly formatted and accessible to the inference pipeline before structure prediction begins.

## When to use

When you have raw MS/MS mass spectrometry data and need to submit it to the Mass2SMILES Docker inference container for structure and functional group prediction. Use this skill if your spectra are currently in MGF (mascot generic format) adhering to GNPS conventions, or if you need to convert or validate existing spectral data into that format.

## When NOT to use

- Input is already in a non-MGF proprietary vendor format (e.g., raw Thermo .raw, Agilent .d) without conversion to MGF first.
- Spectral data is already processed as a feature matrix or embedding and does not need to be re-parsed from raw MGF.
- You need only to retrieve metadata about spectra without performing inference; MGF parsing is unnecessary overhead in that case.

## Inputs

- MGF file (GNPS-style format) containing MS/MS spectral data with precursor m/z and fragment ion peaks

## Outputs

- Parsed spectral data tensor ready for model inference
- Validated MGF metadata and peak lists

## How to apply

Obtain or prepare your MS/MS spectral data as a GNPS-style MGF file, which is the native input format accepted by Mass2SMILES. Mount the directory containing your MGF file to the Mass2SMILES Docker container at runtime (using `-v` flag) so the container can access it. Verify that the MGF file is properly formatted by checking for required GNPS-style headers and m/z–intensity pairs. Pass the MGF filename as an argument to the `mass2smiles_transformer.py` script running inside the container, along with the output directory path. The container will parse the spectral data, prepare it as input tensors for the transformer model, and generate SMILES predictions.

## Related tools

- **Docker** (Container runtime that isolates and executes the Mass2SMILES inference pipeline with mounted volume access to MGF input files)
- **mass2smiles_transformer.py** (Python script that accepts MGF filename as argument and orchestrates parsing, tensor conversion, and model inference) — https://github.com/volvox292/mass2smiles
- **delser292/mass2smiles:final** (Pre-built Docker image containing the Mass2SMILES model, dependencies, and inference scripts; accepts MGF input via mounted volume) — https://hub.docker.com/r/delser292/mass2smiles

## Examples

```
docker run -v /path/to/mass2smiles:/app delser292/mass2smiles:final conda run -n tf python app/mass2smiles_transformer.py sample_spectra.mgf /app
```

## Evaluation signals

- MGF file is successfully mounted to the container and readable at the specified mount path.
- The mass2smiles_transformer.py script completes without file-not-found or format parsing errors.
- The container's standard output or log file confirms that spectral peaks and precursor m/z values were extracted and parsed from the MGF.
- Output SMILES predictions are generated in the specified output directory, confirming that the input spectral tensors were successfully created and passed through the model.
- No warnings or exceptions related to malformed MGF headers, missing required fields, or corrupted peak lists appear in the container logs.

## Limitations

- Only GNPS-style MGF format is supported; other spectral file formats (e.g., mzML, mzXML, vendor raw formats) must be converted to MGF externally before use with Mass2SMILES.
- The inference container requires Docker to be installed and the user must have permission to mount volumes and run containers; local file access depends on correct `-v` flag syntax for the user's operating system.
- Large MGF files or files with very high-resolution spectra may require substantial memory or CPU resources during tensor conversion, depending on the `cpu_threads` parameter configured in the InferenceModel.

## Evidence

- [intro] Spectral data input as MGF files (GNPS-style): "Spectral data can be provided as MGF files (GNPS-syle)"
- [intro] Model inference via Docker container with volume mounting: "model inference is most effciently performed via the provided docker container"
- [readme] Docker run command with volume mount for MGF input and output directory: "docker run -v c:/your_path/to_the_folder/mass2smiles/:/app  mass2smiles:transformer_v1 conda run -n tf python app/mass2smiles_transformer.py your_mgf_file.mgf /app"
- [readme] Mass2SMILES is an open-source Python based deep learning approach for structure and functional group prediction from mass spectrometry data (MS/MS): "Mass2SMILES is an open-source Python based deep learning approach for structure and functional group prediction from mass spectrometry data (MS/MS)"
