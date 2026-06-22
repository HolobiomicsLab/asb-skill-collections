---
name: numerical-feature-serialization-and-storage
description: Use when after computing molecular descriptors (RDKit, mordred) or featurizing chromatographic parameters (column metadata, gradient slopes, pH, additives), you have a NumPy array or list of arrays in memory that must be persisted for reproducibility, shared across pipeline stages, or archived.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3429
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - mordred
  - NumPy
  - pandas
  - pickle (Python standard library)
  - RDKit
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
- import mordred from mordred import Calculator, descriptors
- import numpy as np
- import pandas as pd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphormer_rt_cq
    doi: 10.1021/acs.analchem.4c05859
    title: Graphormer-RT
  dedup_kept_from: coll_graphormer_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05859
  all_source_dois:
  - 10.1021/acs.analchem.4c05859
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# numerical-feature-serialization-and-storage

## Summary

Serialize computed molecular descriptor arrays and chromatographic feature matrices into multiple persistent formats (.npz, .npy, .csv, .pkl) to enable efficient storage, version control, and downstream machine learning ingestion. This skill bridges in-memory feature computation and model training by choosing format trade-offs (compression, human-readability, portability).

## When to use

After computing molecular descriptors (RDKit, mordred) or featurizing chromatographic parameters (column metadata, gradient slopes, pH, additives), you have a NumPy array or list of arrays in memory that must be persisted for reproducibility, shared across pipeline stages, or archived. Choose this skill when the feature matrix is ready for storage and you need to decide between compressed binary (.npz), NumPy native (.npy), human-readable tabular (.csv), or Python object (.pkl) formats.

## When NOT to use

- Input is streaming or real-time data that must not be written to disk.
- Feature array is already persisted and you need to reload and transform it (use deserialization, not storage).
- The downstream consumer requires a specific non-standard format (e.g., HDF5, Parquet); adapt the workflow rather than forcing into .npz/.csv.

## Inputs

- NumPy ndarray (1D or 2D numerical features)
- list of NumPy ndarrays (e.g., [rdkit_descriptors, mordred_descriptors])
- pandas DataFrame (tabular features with column headers)

## Outputs

- .npz file (compressed NumPy archive, single or multiple arrays)
- .npy file (NumPy binary single-array format)
- .csv file (comma-separated tabular representation)
- .pkl or .pickle file (Python pickle serialization)

## How to apply

Construct the feature array as a NumPy ndarray (e.g., by concatenating RDKit and mordred descriptors, or stacking column/gradient/solvent/pH features). Use np.savez_compressed() to save as .npz (smallest disk footprint, recommended for large matrices); use np.save() for .npy (fast single-array I/O); use pandas.DataFrame.to_csv() for .csv (human-inspectable, interoperable); use pickle.dump() for .pkl (preserves Python object structure, e.g., lists of arrays). Select .npz as default for descriptor matrices (supports multiple arrays per file), .csv for tabular features with named columns (e.g., column diameter, temperature, pH), and .pkl when the array structure is irregular or accompanies metadata dictionaries. Verify file integrity by reloading and comparing shape and data type.

## Related tools

- **NumPy** (Primary serialization library; np.savez_compressed() for .npz, np.save() for .npy, np.load() for reading) — https://github.com/numpy/numpy
- **pandas** (Tabular I/O; DataFrame.to_csv() and read_csv() for human-readable feature export/import) — https://github.com/pandas-dev/pandas
- **pickle (Python standard library)** (Object serialization for irregular array structures and metadata preservation)
- **RDKit** (Computes molecular descriptors (input to feature matrix); descriptor names/values become rows/columns of serialized array) — https://github.com/rdkit/rdkit
- **mordred** (Computes additional molecular descriptors; output arrays deduplicated and concatenated before serialization)

## Examples

```
import numpy as np; features = [rdkit_descriptors, mordred_descriptors]; np.savez_compressed('descriptors.npz', rdkit=features[0], mordred=features[1])
```

## Evaluation signals

- File exists on disk at the specified path and has non-zero size matching the feature array magnitude (e.g., M features × N samples).
- Reloading the file (np.load(), np.load(..., allow_pickle=True), pd.read_csv(), pickle.load()) reproduces the in-memory array with identical dtype, shape, and values (use np.allclose() for floating-point comparison).
- For .npz files with multiple arrays, verify the key names match the input dictionary keys and all arrays are present.
- .csv files can be opened in a text editor and contain header row (if provided) and numeric/string values in expected columns.
- Compressed .npz file size is ≤60–80% of uncompressed .npy size for typical molecular descriptor matrices (validation via du or os.path.getsize()).

## Limitations

- NumPy binary formats (.npz, .npy) are not human-readable; inspect via Python REPL or convert to .csv for debugging.
- .csv export loses precision in floating-point descriptors if delimiter/quoting is misconfigured; always verify round-trip conversion.
- .pkl files are Python-specific and may not be portable across Python versions or to other languages; use for internal pipelines only.
- Large descriptor matrices (>10 GB) may exceed RAM when fully loaded; use memory-mapping (np.load(..., mmap_mode='r')) or HDF5 for very large datasets.
- The article does not provide explicit guidance on chunking or streaming strategies for multi-gigabyte feature sets; consider external formats (Parquet, HDF5) if storage >1 GB.

## Evidence

- [results] Loading and saving features in multiple formats (.npz compressed, .npy, .csv/.txt, .pkl/.pickle): "Loading and saving features in multiple formats (.npz compressed, .npy, .csv/.txt, .pkl/.pickle)"
- [results] def save_features(path: str, features: List[np.ndarray]): np.savez_compressed(path, features=features): "def save_features(path: str, features: List[np.ndarray]):
    np.savez_compressed(path, features=features)"
- [other] Concatenate RDKit and deduplicated mordred descriptor arrays into a single feature matrix. 7. Save the resulting descriptor matrix in compressed NumPy format (.npz) and optionally in .csv/.npy/.pkl formats.: "Concatenate RDKit and deduplicated mordred descriptor arrays into a single feature matrix. 7. Save the resulting descriptor matrix in compressed NumPy format (.npz) and optionally in .csv/.npy/.pkl"
