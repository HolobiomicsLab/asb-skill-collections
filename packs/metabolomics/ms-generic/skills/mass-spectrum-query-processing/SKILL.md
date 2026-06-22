---
name: mass-spectrum-query-processing
description: Use when you have an unknown mass spectrum (as m/z and intensity arrays) and need to identify candidate compounds by matching against a mass spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MSEntropy
  - Python
  - EntropySearch
  - FlashEntropySearch
  techniques:
  - mass-spectrometry
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-query-processing

## Summary

Query mass spectral libraries using entropy-based similarity scoring via the Flash Entropy Search algorithm, which accelerates real-time matching of unknown spectra against large library collections. This skill enables rapid compound identification by computing entropy similarity scores between a query spectrum and indexed library entries.

## When to use

Apply this skill when you have an unknown mass spectrum (as m/z and intensity arrays) and need to identify candidate compounds by matching against a mass spectral library. Use it specifically when you require rapid, real-time similarity ranking across multiple spectral libraries without pre-filtering by precursor m/z alone, or when dot product similarity has insufficient discriminative power for your compound identification task.

## When NOT to use

- Your query spectra are already confidently assigned to compounds via orthogonal methods (e.g., retention time, reference standards); use this skill for de novo or confirmatory identification, not post-hoc validation.
- Your spectral library is very small (<100 spectra) or your turnaround-time budget does not constrain classical dot product similarity; classical methods may suffice and avoid added dependencies.
- Your library spectra lack consistent precursor_mz annotation or contain predominantly low-quality (low S/N) fragments; Flash Entropy Search assumes well-formed library data.

## Inputs

- Query spectrum object with precursor_mz (float) and peaks (2D array of [m/z, intensity] pairs)
- Spectral library (list of dictionaries with required keys: precursor_mz, peaks; optional: id, metadata)
- Precursor m/z tolerance or mass range (implicit in indexing step)

## Outputs

- Ranked list of library spectrum matches with entropy similarity scores
- Similarity score arrays for hybrid_search, identity_search, neutral_loss_search, and open_search modes
- Library spectrum identifiers and metadata associated with top-ranked matches

## How to apply

First, format your query spectrum with precursor_mz and peaks (as [m/z, intensity] pairs) and load or build an index from library spectra using the FlashEntropySearch class in MSEntropy. Call the search() method with your query precursor_mz and peaks to compute entropy-based similarity scores across all indexed library spectra. The algorithm returns similarity scores for hybrid_search, identity_search, neutral_loss_search, and open_search modes—rank results by the relevant similarity metric in descending order. Select the hybrid_search or open_search score for general-purpose identification; use identity_search for exact mass matching or neutral_loss_search for fragmentation pathway analysis. Validate matches by examining the ranked library spectrum identifiers and metadata returned.

## Related tools

- **MSEntropy** (Python package implementing Flash Entropy Search algorithm and spectral entropy calculation for library querying) — https://github.com/YuanyueLi/MSEntropy
- **EntropySearch** (Standalone GUI application for searching spectral files (.mgf, .msp, .mzML, .lbm2) against spectral libraries using entropy similarity) — https://github.com/YuanyueLi/EntropySearch
- **FlashEntropySearch** (Repository containing original algorithm source code, benchmark data, and implementation reference for the Flash Entropy Search manuscript) — https://github.com/YuanyueLi/FlashEntropySearch

## Examples

```
from ms_entropy import FlashEntropySearch
import numpy as np
entropy_search = FlashEntropySearch()
spectral_library = entropy_search.build_index([{"id": "lib_1", "precursor_mz": 150.0, "peaks": [[100.0, 1.0], [101.0, 1.0]]}, {"id": "lib_2", "precursor_mz": 200.0, "peaks": np.array([[100.0, 1.0], [102.0, 1.0]], dtype=np.float32)}])
similarity = entropy_search.search(precursor_mz=150.0, peaks=np.array([[100.0, 1.0], [101.0, 1.0], [102.0, 1.0]], dtype=np.float32))
```

## Evaluation signals

- Returned entropy similarity scores fall within the valid range [0, 1] for all four search modes (hybrid, identity, neutral_loss, open).
- Top-ranked library matches have higher entropy similarity scores than lower-ranked entries; score ranks are monotonically ordered.
- Query spectrum precursor_mz is within tolerance of matched library spectra precursor_mz (tolerance depends on instrument calibration; typically <0.01 Da for high-resolution MS).
- Returned library spectrum identifiers and metadata correspond to valid entries in the indexed spectral library (no orphaned or corrupted references).
- Computational runtime for a single query on a large library (>100,000 spectra) completes in seconds, demonstrating algorithmic acceleration vs. classical similarity computation.

## Limitations

- The algorithm requires spectra to be formatted consistently with precursor_mz and peaks keys; malformed or missing precursor_mz values will cause indexing or search failures.
- Entropy similarity assumes sufficient spectral complexity; low-mass or low-intensity query spectra with few significant peaks may produce ambiguous or low-confidence matches.
- No changelog is available in the FlashEntropySearch repository, limiting visibility into version-to-version algorithmic or API changes.
- The Flash Entropy Search algorithm is currently implemented in Python only; C/C++, R, and JavaScript implementations of classical entropy/entropy similarity are available, but real-time library search acceleration is Python-exclusive.

## Evidence

- [intro] Algorithm accelerates entropy similarity computation for library querying: "Flash entropy search to query all mass spectral libraries in real time"
- [intro] Entropy similarity outperforms dot product for compound identification: "Entropy similarity, which measured spectral similarity based on spectral entropy, has been shown to outperform dot product similarity in compound identification"
- [readme] Query workflow: load query spectrum, build index from library, search and rank results: "Step 1: Build the index from the library spectra
entropy_search.build_index(spectral_library)

# Step 2: Search the library
entropy_similarity = entropy_search.search(
    precursor_mz ="
- [readme] Output structure includes four similarity score modes: "{'hybrid_search': array([0.6666666 , 0.99999994, 0.99999994, 0.99999994], dtype=float32),
 'identity_search': array([0.6666667, 0.       , 0.       , 0.       ], dtype=float32),"
- [readme] Library spectrum input format and required keys: "Note that the `precursor_mz` and `peaks` keys are required, the reset of the keys are optional"
- [readme] GUI supports standard spectral file formats: "To search one spectral file against another spectral file or a spectral library, use the Entropy Search GUI. The GUI supports `.mgf`, `.msp`, `.mzML`, and `.lbm2` file formats"
