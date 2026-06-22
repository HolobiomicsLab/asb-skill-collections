---
name: retention-time-prediction
description: Use when you have MS1-formatted mass spectrometry files from a liquid chromatography–mass spectrometry (LC-MS) experiment and need to predict the retention time of peptide ions without relying on spectral libraries, empirical models, or manual feature engineering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - IsoFusion
  - MSConvert
  - Docker
  - Scannotation
  techniques:
  - LC-MS
derived_from:
- doi: 10.26599/bdma.2024.9020059
  title: IsoFusion
- doi: 10.1021/acs.est.3c04764
  title: ''
evidence_spans:
- github.com__xfcui__IsoFusion
- Scannotation is an automated and user-friendly suspect screening tool for the rapid pre-annotation of LC-HRMS datasets.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  - build: coll_isofusion_cq
    doi: 10.26599/bdma.2024.9020059
    title: IsoFusion
  - build: coll_scannotation_cq
    doi: 10.1021/acs.est.3c04764
    title: Scannotation
  dedup_kept_from: coll_isofusion_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26599/bdma.2024.9020059
  all_source_dois:
  - 10.26599/bdma.2024.9020059
  - 10.1021/acs.est.3c04764
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-prediction

## Summary

Predict peptide retention time directly from mass spectrometry data using IsoFusion, a multitask deep learning model that jointly learns charge state, isotope count, and retention time from MS1 spectra. This skill eliminates the need for expert parameter tuning and external databases.

## When to use

You have MS1-formatted mass spectrometry files from a liquid chromatography–mass spectrometry (LC-MS) experiment and need to predict the retention time of peptide ions without relying on spectral libraries, empirical models, or manual feature engineering. Apply this skill when you want end-to-end prediction from raw mass spectrum directly.

## When NOT to use

- Your input is in a different mass spectrometry format (e.g., mzML, mzXML) without prior conversion to MS1 — convert first using MSConvert.
- You require retention time predictions calibrated to a specific chromatographic gradient or column — IsoFusion learns gradient-agnostic patterns from training data but may not generalize to novel LC conditions without retraining.
- Your sample contains non-peptide molecules or highly unusual ion chemistries not represented in IsoFusion's training data.

## Inputs

- MS1-formatted mass spectrometry file (from raw MS data converted via MSConvert)
- Mounted directory path containing MS1 file accessible to Docker container

## Outputs

- Retention time predictions (per spectrum or per precursor)
- Charge state predictions (auxiliary output)
- Isotope count predictions (auxiliary output)
- Predictions file in output directory specified at runtime

## How to apply

First, convert your raw mass spectrometry files to MS1 format using MSConvert if they are not already in that format. Load the IsoFusion Docker image (jorhelp/isofusion or the Aliyun mirror for mainland China users). Mount your MS1 file to the container and invoke the run_IsoFusion.py script with the MS1 file path, specifying output directory, number of processes, GPU ID, and batch size (e.g., batch_size=512 for typical datasets). The model processes the mass spectrum end-to-end through multitask learning: the primary task predicts retention time while auxiliary tasks (charge state and isotope count prediction) improve main task performance through shared representation learning. Collect predictions from the output directory and validate that retention time values fall within the expected chromatographic range for your experimental conditions.

## Related tools

- **MSConvert** (Convert raw mass spectrometry vendor formats to MS1 format prior to IsoFusion input)
- **IsoFusion** (End-to-end deep learning model for predicting charge, isotope count, and retention time from MS1 spectra via multitask learning) — https://github.com/xfcui/IsoFusion
- **Docker** (Container runtime to execute IsoFusion with GPU support and isolated environment)

## Examples

```
docker run --name isofusion --runtime=nvidia -v /data/ms1:/mnt jorhelp/isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/sample.ms1 --output /mnt/ --process_num 8 --gpu 0 --batch_size 512
```

## Evaluation signals

- Predicted retention time values are within the expected range for the chromatographic gradient used in the experiment (e.g., 0–120 minutes for typical reversed-phase methods).
- Output file is generated in the specified output directory with retention time predictions for all input spectra.
- Charge state and isotope count predictions (auxiliary outputs) are consistent with known peptide ion properties and improve over baseline when validated against ground truth.
- No crashes or GPU memory errors when running with specified batch_size and process_num; successful completion logged in container output.
- Retention time predictions show lower variance or higher correlation with observed retention times compared to predictions from models that do not leverage multitask learning.

## Limitations

- IsoFusion requires conversion of raw mass spectrometry files to MS1 format; not all vendors' formats may convert losslessly.
- Model performance depends on training data distribution; generalization to LC gradients, columns, or peptide populations substantially different from training data is not guaranteed.
- GPU support (NVIDIA) is configured via Docker but CPU-only execution may be significantly slower; batch_size and process_num should be tuned to available hardware.
- No changelog or versioning information provided in the repository, limiting reproducibility across software updates.

## Evidence

- [readme] our model is an end-to-end model that can predict charge, number of isotopes and retention time directly from the mass spectrum: "our model is an end-to-end model that can predict charge, number of isotopes and retention time directly from the mass spectrum"
- [readme] This method does not rely on expert knowledge and does not need to adjust complex parameters, which makes it easier to use than traditional methods: "This method does not rely on expert knowledge and does not need to adjust complex parameters, which makes it easier to use than traditional methods"
- [readme] Using the multi-task learning to predict charge, number of isotopes and retention time simultaneously, the auxiliary task can help improve the learning performance of the main task: "Using the multi-task learning to predict charge, number of isotopes and retention time simultaneously, the auxiliary task can help improve the learning performance of the main task"
- [readme] You will need to convert your raw mass spectrometry files to MS1 format. The conversion tool can use MSConvert, which you need to download and install yourself.: "You will need to convert your raw mass spectrometry files to MS1 format. The conversion tool can use MSConvert, which you need to download and install yourself."
- [readme] docker run --name isofusion --runtime=nvidia  -v PATH_TO_MS1:/mnt isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/MS1_FILE --output /mnt/ --process_num 8 --gpu 0 --batch_size 512: "docker run --name isofusion --runtime=nvidia  -v PATH_TO_MS1:/mnt isofusion python3 -Bu IsoFusion/run_IsoFusion.py --file /mnt/MS1_FILE --output /mnt/ --process_num 8 --gpu 0 --batch_size 512"
