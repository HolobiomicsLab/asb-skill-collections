---
name: isotope-pattern-detection
description: Use when you have MS1-format mass spectrometry files and need to determine the isotope count for peptide features without manual inspection or expert parameter tuning.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotope-pattern-detection

## Summary

Predict the number of isotopes in a peptide directly from MS1 mass spectrometry data using a deep learning end-to-end model (IsoFusion). This skill is applied when you need automated, parameter-free isotope enumeration as part of peptide feature detection in proteomics workflows.

## When to use

You have MS1-format mass spectrometry files and need to determine the isotope count for peptide features without manual inspection or expert parameter tuning. This is particularly useful when isotope information is required downstream for charge state assignment, retention time prediction, or peptide identification.

## When NOT to use

- Your input is already a fully processed feature table with annotated isotope patterns — the model is for raw spectrum prediction, not post-processing.
- Your mass spectrometry files are not in MS1 format and you cannot convert them — the pipeline requires MS1 input.
- You have expert knowledge and strict parameter constraints that conflict with the model's automatic, parameter-free design.

## Inputs

- MS1-format mass spectrometry file (raw mass spectrometry data converted to MS1 format)
- Absolute file path to the MS1 input file

## Outputs

- Isotope count predictions per spectrum
- Charge state predictions (from multi-task learning)
- Retention time predictions (from multi-task learning)
- Prediction output file(s) in specified output directory

## How to apply

Convert your raw mass spectrometry files to MS1 format using MSConvert. Prepare the MS1 file with absolute path reference. Load the IsoFusion Docker image (jorhelp/isofusion) and mount the MS1 file directory. Execute the IsoFusion end-to-end deep learning model via the Docker container, specifying the MS1 file path, output directory, number of processes (typically 8), GPU device index (0 if available), and batch size (512 recommended). The model operates without requiring adjustment of complex parameters and directly outputs isotope count predictions from the mass spectrum along with associated charge and retention time predictions.

## Related tools

- **MSConvert** (Converts raw mass spectrometry files to MS1 format for input to IsoFusion)
- **IsoFusion** (End-to-end deep learning model that predicts isotope count, charge state, and retention time directly from MS1 mass spectrum) — https://github.com/xfcui/IsoFusion

## Examples

```
docker run --name isofusion --runtime=nvidia -v /data/ms1:/mnt jorhelp/isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/sample.ms1 --output /mnt/ --process_num 8 --gpu 0 --batch_size 512
```

## Evaluation signals

- Output file is generated in the specified output directory with predictions for all input spectra.
- Predictions include isotope count values that are positive integers and fall within expected biological ranges (typically 2–10 for peptides).
- Multi-task predictions (charge, isotopes, retention time) are all present and consistent across the output.
- Model execution completes without errors on valid MS1 input files.
- Isotope predictions align with the observed isotope patterns visible in the raw mass spectrum when spot-checked against example spectra.

## Limitations

- The model requires input in MS1 format; other mass spectrometry formats must be converted first, introducing potential information loss.
- Performance depends on the quality and preprocessing of the MS1 file; noisy or poorly formatted spectra may yield unreliable isotope counts.
- GPU availability is recommended for efficient batch processing; CPU-only execution may be significantly slower.
- The multi-task learning design couples isotope prediction with charge and retention time prediction; isotope output cannot be isolated or tuned independently.

## Evidence

- [readme] our model is an end-to-end model that can predict charge, number of isotopes and retention time directly from the mass spectrum: "our model is an end-to-end model that can predict charge, number of isotopes and retention time directly from the mass spectrum"
- [readme] This method does not rely on expert knowledge and does not need to adjust complex parameters, which makes it easier to use than traditional methods: "This method does not rely on expert knowledge and does not need to adjust complex parameters, which makes it easier to use than traditional methods"
- [readme] You will need to convert your raw mass spectrometry files to MS1 format. The conversion tool can use MSConvert, which you need to download and install yourself.: "You will need to convert your raw mass spectrometry files to MS1 format. The conversion tool can use MSConvert"
- [readme] Using the multi-task learning to predict charge, number of isotopes and retention time simultaneously, the auxiliary task can help improve the learning performance of the main task: "Using the multi-task learning to predict charge, number of isotopes and retention time simultaneously, the auxiliary task can help improve the learning performance of the main task"
- [readme] docker run --name isofusion --runtime=nvidia  -v PATH_TO_MS1:/mnt isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/MS1_FILE --output /mnt/ --process_num 8 --gpu 0 --batch_size 512: "docker run --name isofusion --runtime=nvidia  -v PATH_TO_MS1:/mnt isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/MS1_FILE --output /mnt/ --process_num 8 --gpu 0 --batch_size 512"
