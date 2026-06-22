---
name: spectral-output-formatting
description: Use when after generating tandem mass spectrum predictions from a neural model (ICEBERG, SCARF, or baseline), and before attempting retrieval ranking, metric computation, or validation against experimental spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ms-pred
  - ICEBERG WebUI
  - ICEBERG
  - SCARF
  - PubChem
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
evidence_spans:
- github.com__samgoldman97__ms-pred
- You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_fragmentation_graph_generation_cq
    doi: 10.1021/acs.analchem.3c04654
    title: ICEBERG / fragmentation graph generation
  dedup_kept_from: coll_iceberg_fragmentation_graph_generation_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04654
  all_source_dois:
  - 10.1021/acs.analchem.3c04654
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-output-formatting

## Summary

Convert predicted tandem mass spectra (m/z and intensity pairs, or subformula assignments) from neural model outputs into structured, exportable spectrum files (e.g., MGF, TSV, or HDF5 formats) suitable for downstream comparison, retrieval, or archival. This skill bridges model inference and practical spectrometry workflows by ensuring consistent representation of predicted peaks and metadata.

## When to use

After generating tandem mass spectrum predictions from a neural model (ICEBERG, SCARF, or baseline), and before attempting retrieval ranking, metric computation, or validation against experimental spectra. Specifically apply this skill when raw model outputs (logits, intensity scores, fragment nodes) must be decoded into peak lists with m/z values and normalized intensities.

## When NOT to use

- Input is raw experimental spectra already in a standard format (MGF, mzML) — use format conversion tools instead of model output parsing.
- Model inference has not yet completed — defer formatting until all forward passes and intensity predictions are finalized.
- Spectrum predictions are being used only for internal debugging or unit testing, where structured export is not needed.

## Inputs

- Model output logits or intensity tensors (PyTorch tensor or NumPy array)
- Fragment or subformula vocabulary mapping (indexed list or dictionary of m/z values or chemical formulas)
- Precursor m/z and charge state (float, integer)
- Compound identifier and collision energy annotation (string, float)
- Optional: model hyperparameters specifying peak filtering threshold or normalization scheme

## Outputs

- Structured spectrum file in MGF, TSV, or HDF5 format
- Peak list with (m/z, intensity) pairs, sorted by m/z or intensity
- Spectrum metadata table with columns for compound ID, precursor m/z, charge, collision energy, and predicted peaks
- Formatted spectrum ready for retrieval ranking or comparison against experimental spectra

## How to apply

Retrieve the model's raw output tensors or logit arrays representing fragments (in ICEBERG) or subformulae (in SCARF). Decode fragment indices to their corresponding m/z values using a precomputed fragment or subformula vocabulary. Scale intensity predictions to a normalized range (e.g., 0–100 or 0–1 scale), optionally filtering peaks below a noise threshold. Pair each m/z with its intensity to form (m/z, intensity) tuples. Serialize the sorted peak list into the target format—common choices are MGF (mascot generic format for mass spec databases), TSV for tabular import, or HDF5 for efficient batch storage with metadata. Include spectrum annotations (precursor m/z, charge state, compound ID, collision energy if available) as header or table fields to preserve experimental context.

## Related tools

- **ICEBERG** (Fragment-level spectrum prediction model; outputs are decoded into peak lists with m/z and intensity pairs) — https://github.com/coleygroup/ms-pred
- **SCARF** (Subformula-level spectrum prediction model; outputs parsed and formatted as peaks with subformula assignments) — https://github.com/coleygroup/ms-pred
- **ms-pred** (Repository containing all spectrum predictor models and example formatting workflows via Jupyter notebooks) — https://github.com/coleygroup/ms-pred
- **PubChem** (Reference library used to verify formatted spectra during retrieval ranking and structural elucidation campaigns)

## Examples

```
# After model prediction, format ICEBERG output to MGF:
python src/ms_pred/dag_pred/predict_smis.py --config configs/iceberg/iceberg_elucidation.yaml --output-format mgf --output-path predictions.mgf
```

## Evaluation signals

- All predicted peaks have valid m/z values (positive, within expected range for target ionization mode) and intensity values normalized to the specified scale (0–100 or 0–1).
- Peak lists are sorted consistently (either ascending by m/z or descending by intensity) and contain no duplicates.
- Output file conforms to target schema: MGF files have valid [PRECURSOR_MZ] and [PEAKS] blocks; TSV files have required columns (compound_id, precursor_mz, charge, m/z, intensity); HDF5 files have correct dataset hierarchy and metadata attributes.
- Spectrum metadata (precursor m/z, charge state, collision energy, compound ID) is preserved in output headers or columns and matches input annotations.
- Downstream retrieval or comparison metrics (e.g., cosine similarity to experimental spectra, top-k hit rates) are computed without errors, indicating format compatibility.

## Limitations

- Formatting depends on accurate model output decoding; errors in fragment vocabulary indexing or intensity scaling will propagate to the final spectrum representation.
- Peak filtering thresholds are hyperparameter-dependent; too-aggressive filtering may remove low-intensity but biologically relevant fragments, while too-lenient filtering may include noise.
- Format choice (MGF vs. TSV vs. HDF5) affects downstream tool compatibility; not all tools support all formats, and conversion between formats may introduce rounding or metadata loss.
- Collision energy annotation is essential for fair comparison to experimental spectra; predicted spectra generated at a different collision energy may not retrieve the correct candidates even if correct.

## Evidence

- [other] Decode model outputs to construct predicted tandem mass spectrum (m/z and intensity pairs).: "Decode model outputs to construct predicted tandem mass spectrum (m/z and intensity pairs)."
- [other] Format and export predicted spectrum as a structured spectrum file.: "Format and export predicted spectrum as a structured spectrum file."
- [other] Parse and format predicted spectra (peak intensities, m/z values, subformula assignments) into structured output table.: "Parse and format predicted spectra (peak intensities, m/z values, subformula assignments) into structured output table."
- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] spec_files.hdf5 and mgf_files are standard output format directories in the processed dataset structure: "├── mgf_files
    ├── spec_files.hdf5"
