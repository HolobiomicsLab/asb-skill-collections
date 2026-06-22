---
name: mass-spectral-data-formatting
description: Use when when you have raw mass spectral data in .mgf, .msp, .mzML, or .lbm2 file formats and need to search against a spectral library using entropy similarity or Flash Entropy Search. Also apply this skill before building spectral library indices or computing entropy-based compound identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MSEntropy
  - Python
  - Entropy Search GUI
  - MSEntropy (Python package)
  - MS Viewer web app
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41592-023-02012-9
  title: Flash entropy search
evidence_spans:
- we provide a Python implementation of the algorithm in the `MSEntropy` repository
- Python implementation of the algorithm
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_flash_entropy_search_cq
    doi: 10.1038/s41592-023-02012-9
    title: Flash entropy search
  dedup_kept_from: coll_flash_entropy_search_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-023-02012-9
  all_source_dois:
  - 10.1038/s41592-023-02012-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectral-data-formatting

## Summary

Prepare mass spectral data (peaks, precursor m/z, and optional metadata) into standardized dictionary structures required by entropy-based spectral search algorithms. This skill ensures compatibility with Flash Entropy Search and other entropy similarity computations across diverse input file formats.

## When to use

When you have raw mass spectral data in .mgf, .msp, .mzML, or .lbm2 file formats and need to search against a spectral library using entropy similarity or Flash Entropy Search. Also apply this skill before building spectral library indices or computing entropy-based compound identification.

## When NOT to use

- Input is already a validated list of spectrum dictionaries with 'precursor_mz' and 'peaks' keys—proceed directly to search or index building.
- Working with data formats that do not encode m/z or intensity information (e.g., aggregated feature tables, quantitation matrices without spectral detail).
- Spectral data that lacks precursor m/z annotation (required for Flash Entropy Search's precursor-based filtering).

## Inputs

- Mass spectral data file (.mgf, .msp, .mzML, .lbm2 format)
- Raw m/z and intensity arrays (lists or numpy arrays)
- Precursor m/z value (float)

## Outputs

- Formatted spectral library (list of dictionaries with 'id', 'precursor_mz', 'peaks', and optional metadata)
- Query spectrum dictionary (with 'precursor_mz' and 'peaks' keys)
- Validated peak arrays (numpy float32 or list of [m/z, intensity] pairs)

## How to apply

Parse the input spectral file (using the Entropy Search GUI or manual parsing in Python/R/C++) to extract peaks as [m/z, intensity] pairs and the precursor m/z value. Construct a dictionary for each spectrum with required keys 'precursor_mz' and 'peaks', plus optional 'id' and arbitrary metadata keys. Store peaks as a list of lists or numpy array (dtype=float32 preferred for performance). Validate that all precursor_mz values are positive floats and peaks are non-negative intensity pairs. This formatting step is mandatory before calling FlashEntropySearch.build_index() or entropy_search.search().

## Related tools

- **Entropy Search GUI** (User-friendly interface to load, parse, and format .mgf, .msp, .mzML, and .lbm2 spectral files for entropy-based library searching) — https://github.com/YuanyueLi/EntropySearch/releases
- **MSEntropy (Python package)** (Provides programmatic API (FlashEntropySearch class) that accepts pre-formatted spectral dictionaries and builds indices from formatted spectral libraries) — https://github.com/YuanyueLi/MSEntropy
- **MS Viewer web app** (Real-time visualization and formatting of two MS/MS spectra prior to entropy similarity calculation)

## Examples

```
```python
import numpy as np
from ms_entropy import FlashEntropySearch

spectral_library = [{
    "id": "Spectrum_1",
    "precursor_mz": 150.0,
    "peaks": np.array([[100.0, 1.0], [101.0, 1.0], [103.0, 1.0]], dtype=np.float32)
}]

query_spectrum = {"precursor_mz": 150.0, "peaks": np.array([[100.0, 1.0], [101.0, 1.0], [102.0, 1.0]], dtype=np.float32)}

entropy_search = FlashEntropySearch()
entropy_search.build_index(spectral_library)
results = entropy_search.search(precursor_mz=query_spectrum['precursor_mz'], peaks=query_spectrum['peaks'])
```
```

## Evaluation signals

- Each spectrum dictionary contains exactly the keys 'precursor_mz' and 'peaks', plus optional metadata keys; absence of either required key raises an error on build_index() or search().
- Peaks are stored as a 2D array or list of [m/z, intensity] pairs with m/z in ascending order or within expected mass range (e.g., 50–2000 m/z for small molecules).
- Precursor m/z values are positive floats matching the mass of the queried compound; out-of-range or null values should trigger validation warnings.
- When passed to FlashEntropySearch.build_index(), the formatted library is successfully indexed without parsing errors or type mismatches.
- Search results are returned as a dict with keys 'hybrid_search', 'identity_search', 'neutral_loss_search', 'open_search', each containing an array of similarity scores matching the number of spectra in the library.

## Limitations

- The 'precursor_mz' and 'peaks' keys are required; other keys are optional but may affect downstream filtering or metadata propagation. Missing 'precursor_mz' will cause Flash Entropy Search to fail.
- Peak intensity normalization and m/z tolerance are not handled by the formatting step itself; these preprocessing steps must be performed upstream or by the search algorithm.
- File format support (.mgf, .msp, .mzML, .lbm2) is limited to formats recognized by the Entropy Search GUI or custom parsers; non-standard or legacy formats require custom parsing code.
- Large spectral libraries (>100k spectra) may require significant memory when loaded as Python lists of dictionaries; consider streaming or batching for very large datasets.

## Evidence

- [readme] Suppose you have a spectral library, you need to format it like this: [{"id": "Demo spectrum 1", "precursor_mz": 150.0, "peaks": [[100.0, 1.0], [101.0, 1.0], [103.0, 1.0]]} ...]: "Suppose you have a spectral library, you need to format it like this: [{"id": "Demo spectrum 1", "precursor_mz": 150.0, "peaks": [[100.0, 1.0], [101.0, 1.0], [103.0, 1.0]]}]"
- [readme] Note that the `precursor_mz` and `peaks` keys are required, the reset of the keys are optional.: "Note that the `precursor_mz` and `peaks` keys are required, the reset of the keys are optional."
- [readme] To search one spectral file against another spectral file or a spectral library, use the Entropy Search GUI. The GUI supports `.mgf`, `.msp`, `.mzML`, and `.lbm2` file formats.: "The GUI supports `.mgf`, `.msp`, `.mzML`, and `.lbm2` file formats."
- [readme] query_spectrum = {"precursor_mz": 150.0, "peaks": np.array([[100.0, 1.0], [101.0, 1.0], [102.0, 1.0]], dtype=np.float32)}: "query_spectrum = {"precursor_mz": 150.0, "peaks": np.array([[100.0, 1.0], [101.0, 1.0], [102.0, 1.0]], dtype=np.float32)}"
- [other] Load the query spectrum (m/z and intensity arrays) and specify the target mass spectral library using MSEntropy.: "Load the query spectrum (m/z and intensity arrays) and specify the target mass spectral library using MSEntropy."
