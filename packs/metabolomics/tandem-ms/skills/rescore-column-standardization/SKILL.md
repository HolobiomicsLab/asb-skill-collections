---
name: rescore-column-standardization
description: Use when after running FIDDLE v2.0.0 inference on MS/MS spectra and obtaining ranked formula candidates with confidence scores, apply this skill when the rescore model outputs columns named Rescore (0), Rescore (1), ...
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - FIDDLE
  - msfiddle
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# rescore-column-standardization

## Summary

Rename and standardize Rescore (k) output columns from FIDDLE v2.0.0's Siamese-architecture rescore model to a uniform format for downstream analysis and CSV export. This ensures consistent column naming across different inference runs and integrations with external tools.

## When to use

After running FIDDLE v2.0.0 inference on MS/MS spectra and obtaining ranked formula candidates with confidence scores, apply this skill when the rescore model outputs columns named Rescore (0), Rescore (1), ..., Rescore (k) and you need to export results to CSV with standardized, machine-readable column headers for integration with other analysis pipelines or comparative studies.

## When NOT to use

- Rescore columns are already standardized or in a non-parenthetical naming format — standardization is unnecessary.
- Output is intended for direct ingestion by a tool that explicitly expects the original parenthetical format (Rescore (k)) — check tool documentation first.
- Inference has not yet been run or rescore model was not included in the FIDDLE pipeline — no columns to rename.

## Inputs

- DataFrame or table with raw FIDDLE v2.0.0 rescore model outputs (Rescore (0), Rescore (1), ..., Rescore (k) columns)
- Top-k ranking parameter (typically 5 for default output)
- Output file path for CSV export

## Outputs

- CSV file with standardized Rescore column names
- Renamed DataFrame ready for downstream analysis or tool integration

## How to apply

After executing the Siamese-architecture rescore model inference via FIDDLE (v2.0.0), extract the raw Rescore (k) output columns where k ranges from 0 to the top-k ranking (typically 0–4 for top-5 candidates). Identify the pattern of numeric suffixes in the column names and apply a consistent renaming rule (e.g., map Rescore (0) → Rescore_0, Rescore (1) → Rescore_1, etc., or adopt a domain convention such as Rescore_rank_0, depending on downstream tool compatibility). Validate that all k columns are present and contain numeric confidence scores in the expected range (typically [0, 1] for neural model outputs). Finally, export the dataframe to CSV ensuring the renamed columns are written with the standardized header row.

## Related tools

- **FIDDLE** (Deep learning framework that performs MS/MS spectral inference using a Siamese-architecture rescore model and produces ranked formula candidates with confidence scores in Rescore (k) columns) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (PyPI package providing CLI and Python API for FIDDLE inference; handles model download, inference execution, and CSV output generation with Rescore columns) — https://github.com/josiehong/msfiddle

## Examples

```
python run_fiddle.py --test_data ./demo/input_msms.mgf --config_path ./config/fiddle_tcn_orbitrap.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt --rescore_resume_path ./check_point/fiddle_rescore_orbitrap.pt --result_path ./demo/output_fiddle.csv --device 0
```

## Evaluation signals

- All Rescore (k) columns are successfully renamed to the standardized format with no missing or duplicate column names.
- Rescore values remain unchanged (numeric, in valid range [0, 1] or expected score range) after renaming.
- CSV header row contains exactly top-k renamed Rescore columns (e.g., Rescore_0 through Rescore_4 for top-5 output).
- Row counts and column order are preserved; no data is dropped or reordered during the renaming operation.
- Downstream tools or comparative workflows accept the renamed CSV without parsing errors or schema mismatches.

## Limitations

- Renaming is a surface-level operation and does not validate or correct underlying score semantics or calibration; scores remain as output by the neural model.
- If the rescore model was not included in the FIDDLE inference pipeline (e.g., TCN-only prediction), no Rescore columns will be present and standardization cannot be applied.
- Different versions or forks of FIDDLE may use variant column naming patterns (e.g., Rescore_k, Rescore[k], Rescore-k); consult the specific tool version documentation to determine the exact input pattern.
- Standardization logic must be adapted if the number of top-k candidates changes or if the output format differs from the documented Rescore (k) template.

## Evidence

- [other] Extract rescore predictions and rename Rescore (k) output columns to standardized format: "Extract rescore predictions and rename Rescore (k) output columns to standardized format."
- [readme] The rescore model has been redesigned with a Siamese architecture in v2.0.0: "The rescore model has been redesigned (Siamese architecture)"
- [readme] Top-5 output columns with confidence scores for refined formula candidates: "Rescore (0..4) | Confidence scores for the default top-5 refined candidates."
- [readme] CSV export workflow with standardized column headers: "Export results to CSV with properly labeled columns."
