---
name: structure-prediction-from-mass-spectra
description: Use when you have GNPS-style MGF spectral files from MS/MS experiments and need to predict the molecular structure (as SMILES) of unknown compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - Mass2SMILES Docker container
  - TensorFlow
  - Docker
  techniques:
  - LC-MS
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

# structure-prediction-from-mass-spectra

## Summary

Predict molecular structures and functional groups from tandem mass spectrometry (MS/MS) data using a deep learning transformer model trained on spectral fragmentation patterns. This skill enables automated SMILES generation from GNPS-style MGF spectral files, bridging high-resolution MS data to chemical structure inference.

## When to use

You have GNPS-style MGF spectral files from MS/MS experiments and need to predict the molecular structure (as SMILES) of unknown compounds. This is appropriate when you lack reference spectra or chemical standards but have high-quality precursor m/z and fragment ion data, and when you want to augment or validate structure annotations computationally rather than through manual spectral interpretation or database matching alone.

## When NOT to use

- Your spectral data is in a non-MGF format (e.g., mzML, mzXML) and cannot be converted to GNPS-style MGF without loss of critical metadata.
- You have low-resolution or low signal-to-noise MS/MS spectra with sparse fragmentation patterns; the model relies on informative fragment ion distributions.
- You require deterministic, rule-based structure elucidation or exact mass matching to a reference library is available; this skill is best suited for exploratory or de novo annotation tasks.

## Inputs

- GNPS-style MGF spectral files (containing precursor m/z, charge, and fragment ion m/z–intensity pairs)

## Outputs

- SMILES strings (predicted molecular structures)
- Functional group annotations (derived from model predictions)

## How to apply

Organize your MS/MS spectral data into GNPS-style MGF files, ensuring each spectrum contains precursor m/z, charge state, and fragment ions with intensities. Pull or load the Mass2SMILES Docker container (delser292/mass2smiles:final), which bundles a pre-trained transformer model and TensorFlow-based inference engine. Mount your input directory (containing MGF files) and output directory into the container, then invoke the inference script with the MGF file path as the argument. The model processes fragmentation patterns through a deep learning encoder–decoder architecture to generate predicted SMILES strings. GPU-based inference significantly accelerates predictions; if GPU is unavailable, CPU inference can be accelerated by increasing thread count (e.g., cpu_threads=128). Collect predicted SMILES from the output directory and assess confidence by cross-referencing against chemical databases or experimental validation.

## Related tools

- **Mass2SMILES Docker container** (Executes the pre-trained deep learning model for MS/MS-to-SMILES inference with optimized GPU or CPU-based TensorFlow runtime) — https://github.com/volvox292/mass2smiles
- **Python** (Underlying language for model inference script (mass2smiles_transformer.py) and spectral data preprocessing)
- **TensorFlow** (Deep learning framework for model inference; CPU-based build used to avoid compatibility issues with newer CUDA drivers)
- **Docker** (Containerization platform enabling reproducible, isolated model deployment with mounted input/output directories)

## Examples

```
docker run -v /path/to/mass2smiles/:/app delser292/mass2smiles:final conda run -n tf python app/mass2smiles_transformer.py input_spectra.mgf /app
```

## Evaluation signals

- Output SMILES strings are syntactically valid (parseable by chemistry libraries such as RDKit) and represent chemically plausible structures.
- Predicted structures have precursor mass (calculated from SMILES) within expected tolerance (typically <5 ppm) of the input precursor m/z.
- Predicted functional groups are consistent with known fragmentation pathways observed in the input MS/MS spectrum (e.g., neutral losses match expected moieties).
- Inference completes without errors and produces one output record per input spectrum; missing predictions indicate model failure or malformed MGF input.
- GPU-accelerated inference is measurably faster than CPU inference for the same MGF file, confirming hardware utilization when available.

## Limitations

- Model predictions are probabilistic; confidence scores and alternative structure hypotheses are not explicitly returned in the baseline workflow.
- Performance depends on training data composition; spectra from novel compound classes or ionization modes not well-represented in training may yield poor predictions.
- The transformer architecture requires well-formatted, complete MGF input; sparse or corrupted spectral records will fail or be skipped silently.
- Inference speed on CPU is significantly slower than GPU; large-scale spectral libraries may require GPU resources or batch processing to be practical.
- No changelog or version history is provided; reproducibility across container versions cannot be guaranteed without explicit version pinning (e.g., delser292/mass2smiles:final tag stability).
- NIST library licensing is required to access supplementary data and pre-trained model weights in the primary Zenodo deposit; alternative routes (GitHub, secondary Zenodo) may have different licensing terms.

## Evidence

- [readme] structure and functional group prediction from mass spectrometry data (MS/MS): "Mass2SMILES is an open-source Python based deep learning approach for structure and functional group prediction from mass spectrometry data (MS/MS)."
- [readme] MGF files as input format: "Spectral data can be provided as MGF files (GNPS-syle)"
- [readme] Docker container for efficient inference: "model inference is most effciently performed via the provided docker container"
- [readme] GPU vs CPU inference performance: "inference speed is highly improved"
- [readme] TensorFlow CPU build rationale: "the cddd does not seem to work on newer cuda drivers, therefore it is build using tensorflow cpu"
- [readme] Directory mounting and MGF file argument: "docker run -v c:/your_path/to_the_folder/mass2smiles/:/app  mass2smiles:transformer_v1 conda run -n tf python app/mass2smiles_transformer.py your_mgf_file.mgf /app"
- [readme] CPU thread optimization: "can be speed up by changing the number of cores: e.g. InferenceModel(cpu_threads=128)"
- [intro] Deep learning architecture for MS/MS data: "deep learning approach for structure and functional group prediction from mass spectrometry data (MS/MS)"
