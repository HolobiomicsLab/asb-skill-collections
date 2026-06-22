---
name: peptide-charge-state-prediction
description: Use when you have raw mass spectrometry data in MS1 format and need to assign charge states to peptide ions without manual curation or rule-based heuristics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - IsoFusion
  - MSConvert
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peptide-charge-state-prediction

## Summary

Predict peptide charge state directly from MS1 mass spectrometry data using IsoFusion, an end-to-end deep learning model that operates without requiring expert knowledge or complex parameter tuning. This skill integrates charge state prediction with auxiliary predictions of isotope count and retention time to improve overall model performance.

## When to use

Apply this skill when you have raw mass spectrometry data in MS1 format and need to assign charge states to peptide ions without manual curation or rule-based heuristics. Use it as a preprocessing step before downstream peptide identification or quantification workflows where charge state is required but unavailable or unreliable.

## When NOT to use

- Input is already annotated with reliable charge states from the mass spectrometer or a validated upstream tool
- Raw mass spectrometry files are not available or cannot be converted to MS1 format
- You require interpretability of charge state assignment rules (IsoFusion is a black-box deep learning model)

## Inputs

- MS1 mass spectrometry file (converted from raw instrument format via MSConvert)
- path to MS1 file (absolute path)
- output directory path

## Outputs

- charge state predictions (per spectrum)
- isotope count predictions (per spectrum)
- retention time predictions (per spectrum)
- structured prediction output file

## How to apply

Convert raw mass spectrometry files to MS1 format using MSConvert if needed. Load the IsoFusion Docker image and mount your MS1 input directory and output directory as volumes. Execute the IsoFusion end-to-end model via the provided Python script, specifying the MS1 file path, output directory, and computational parameters (process_num, gpu device, batch_size). The model processes the mass spectrum directly to predict charge state as one of three simultaneous tasks (charge, isotope count, retention time); multi-task learning allows auxiliary tasks to improve charge prediction accuracy. Collect predictions in the model's output format and validate that charge state values are within expected ionization ranges.

## Related tools

- **IsoFusion** (end-to-end deep learning model for charge state prediction from mass spectrum) — https://github.com/xfcui/IsoFusion
- **MSConvert** (conversion tool to transform raw mass spectrometry files to MS1 format)

## Examples

```
docker run --name isofusion --runtime=nvidia -v /path/to/ms1:/mnt jorhelp/isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/sample.ms1 --output /mnt/ --process_num 8 --gpu 0 --batch_size 512
```

## Evaluation signals

- Output charge state values are integer scalars and fall within typical peptide ionization ranges (z ≥ 1, commonly 1–6)
- All input spectra receive charge predictions (no missing or NaN values in output)
- Multi-task predictions (charge, isotope count, retention time) are present and have reasonable distributions
- Batch processing completes without GPU or memory errors on specified batch_size and process_num settings
- Predictions can be matched back to input spectra in order and quantity

## Limitations

- IsoFusion requires GPU acceleration (NVIDIA runtime) for practical throughput; CPU-only execution is not documented
- Model is not interpretable; no per-spectrum confidence scores or feature importance are provided
- Performance depends on model pre-training; the article does not report cross-instrument or cross-protocol generalization
- Multi-task learning couples charge state to isotope count and retention time; decoupling one task is not straightforward

## Evidence

- [readme] our model is an end-to-end model that can predict charge, number of isotopes and retention time directly from the mass spectrum: "our model is an end-to-end model that can predict charge, number of isotopes and retention time directly from the mass spectrum"
- [readme] This method does not rely on expert knowledge and does not need to adjust complex parameters, which makes it easier to use than traditional methods: "This method does not rely on expert knowledge and does not need to adjust complex parameters, which makes it easier to use than traditional methods"
- [readme] Using the multi-task learning to predict charge, number of isotopes and retention time simultaneously, the auxiliary task can help improve the learning performance of the main task: "Using the multi-task learning to predict charge, number of isotopes and retention time simultaneously, the auxiliary task can help improve the learning performance of the main task"
- [readme] You will need to convert your raw mass spectrometry files to MS1 format. The conversion tool can use MSConvert, which you need to download and install yourself.: "You will need to convert your raw mass spectrometry files to MS1 format. The conversion tool can use MSConvert"
- [readme] docker run --name isofusion --runtime=nvidia  -v PATH_TO_MS1:/mnt isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/MS1_FILE --output /mnt/ --process_num 8 --gpu 0 --batch_size 512: "docker run --name isofusion --runtime=nvidia  -v PATH_TO_MS1:/mnt isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/MS1_FILE --output /mnt/ --process_num 8 --gpu 0 --batch_size 512"
