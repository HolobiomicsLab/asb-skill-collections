---
name: docker-containerized-pipeline-execution
description: Use when you have raw mass spectrometry data converted to MS1 format and need to predict peptide features (charge, isotope count, retention time) without installing complex dependencies or configuring GPU/Python environments locally.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - IsoFusion
  - MSConvert
  - Docker
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.26599/bdma.2024.9020059
  title: IsoFusion
evidence_spans:
- github.com__xfcui__IsoFusion
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isofusion_cq
    doi: 10.26599/bdma.2024.9020059
    title: IsoFusion
  dedup_kept_from: coll_isofusion_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26599/bdma.2024.9020059
  all_source_dois:
  - 10.26599/bdma.2024.9020059
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# docker-containerized-pipeline-execution

## Summary

Execute a pre-built deep learning pipeline for peptide feature detection using Docker, eliminating the need for manual environment setup. This skill applies the IsoFusion model to MS1 mass spectrometry files to predict charge state, isotope count, and retention time in a containerized, reproducible manner.

## When to use

You have raw mass spectrometry data converted to MS1 format and need to predict peptide features (charge, isotope count, retention time) without installing complex dependencies or configuring GPU/Python environments locally. Use this when you want reproducible, parameter-minimal execution on a system with Docker and NVIDIA GPU runtime available.

## When NOT to use

- Your mass spectrometry data is already in a processed feature table or has pre-extracted peptide features; this skill is for raw or lightly processed MS1 data only.
- You do not have Docker installed or NVIDIA GPU runtime configured; the containerized execution requires these dependencies.
- Your raw files are not yet converted to MS1 format and you cannot run MSConvert separately beforehand.

## Inputs

- MS1-formatted mass spectrometry file (absolute path)
- GPU device index (integer, e.g., 0)

## Outputs

- Peptide feature predictions (charge state, number of isotopes, retention time)
- Results saved to specified output directory

## How to apply

First, convert your raw mass spectrometry files to MS1 format using MSConvert if not already in that format. Pull the IsoFusion Docker image (jorhelp/isofusion or the Aliyun mirror for mainland China users). Mount your MS1 file directory to the container at /mnt, specify the MS1 file path, output directory, and processing parameters (process_num for multiprocessing, gpu for GPU selection, batch_size for inference batching). Run the container with NVIDIA GPU runtime enabled to execute the end-to-end deep learning model. The model outputs predictions for charge, isotope count, and retention time directly from the mass spectrum without requiring expert parameter tuning.

## Related tools

- **IsoFusion** (End-to-end deep learning model for predicting charge, isotope count, and retention time from MS1 spectra; runs within the Docker container) — https://github.com/xfcui/IsoFusion
- **MSConvert** (Pre-processing tool to convert raw mass spectrometry files to MS1 format before Docker pipeline execution)
- **Docker** (Containerization runtime for executing IsoFusion with isolated environment and reproducible dependencies)

## Examples

```
docker run --name isofusion --runtime=nvidia -v /path/to/ms1/files:/mnt jorhelp/isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/sample.ms1 --output /mnt/ --process_num 8 --gpu 0 --batch_size 512
```

## Evaluation signals

- Verify output files are written to the specified output directory with predictions for charge, isotope count, and retention time.
- Check that the Docker container exits with status code 0 (successful execution) and logs contain no errors or GPU initialization failures.
- Confirm batch processing completed as expected by verifying the number of spectra processed matches the MS1 input file size.
- Validate that output predictions fall within reasonable ranges (charge states typically 1–5+, isotope counts 2–10, retention time in minutes matching the MS1 acquisition window).
- Ensure the same MS1 input file produces identical predictions across multiple runs (reproducibility check).

## Limitations

- Requires NVIDIA GPU and Docker runtime; CPU-only execution is not supported by the containerized version.
- Input must be in MS1 format; other mass spectrometry formats (mzML, mzXML, raw) require pre-conversion using MSConvert.
- Model performance depends on mass spectrometry data quality and instrument type; performance on novel instruments or very low-quality spectra is not characterized in the article.
- No changelog or versioning information is provided for the Docker image, making it difficult to track breaking changes across updates.

## Evidence

- [readme] our model is an end-to-end model that can predict charge, number of isotopes and retention time directly from the mass spectrum: "our model is an end-to-end model that can predict charge, number of isotopes and retention time directly from the mass spectrum"
- [readme] This method does not rely on expert knowledge and does not need to adjust complex parameters, which makes it easier to use than traditional methods: "This method does not rely on expert knowledge and does not need to adjust complex parameters, which makes it easier to use than traditional methods"
- [readme] You will need to convert your raw mass spectrometry files to MS1 format. The conversion tool can use MSConvert, which you need to download and install yourself.: "You will need to convert your raw mass spectrometry files to MS1 format. The conversion tool can use MSConvert, which you need to download and install yourself."
- [readme] Pull the docker image: `docker pull jorhelp/isofusion`, for users in Mainland China: `docker pull registry.cn-hangzhou.aliyuncs.com/sdu-bioinfo/isofusion`: "Pull the docker image: `docker pull jorhelp/isofusion`, for users in Mainland China"
- [readme] docker run --name isofusion --runtime=nvidia  -v PATH_TO_MS1:/mnt isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/MS1_FILE --output /mnt/ --process_num 8 --gpu 0 --batch_size 512: "docker run --name isofusion --runtime=nvidia  -v PATH_TO_MS1:/mnt isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/MS1_FILE --output /mnt/ --process_num 8 --gpu 0 --batch_size 512"
