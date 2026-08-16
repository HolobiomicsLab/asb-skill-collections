---
name: entropy-search-algorithm-implementation
description: Use when you need to search one or more query MS/MS spectra against large
  spectral libraries (hundreds of thousands to millions of spectra) and require real-time
  or near-real-time compound identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Entropy Search
  - MSEntropy
  - Python
  - Entropy Search (GUI)
  - MSEntropy (Python package)
  - FlashEntropySearch (source repository)
  - MS Viewer web app
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41592-023-02012-9
  title: Flash entropy search
evidence_spans:
- a standalone software with a Graphical User Interface (GUI) named Entropy Search
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

# entropy-search-algorithm-implementation

## Summary

Implement the Flash Entropy Search algorithm to accelerate real-time querying of mass spectral libraries by building an indexed entropy-based search structure and computing entropy similarity scores. This skill enables searching large spectral databases with throughput orders of magnitude faster than classical dot-product methods.

## When to use

Apply this skill when you need to search one or more query MS/MS spectra against large spectral libraries (hundreds of thousands to millions of spectra) and require real-time or near-real-time compound identification. Use it specifically when you want to replace slower dot-product similarity with entropy similarity, which has been shown to outperform dot product for small-molecule compound identification.

## When NOT to use

- Input spectra are already pre-filtered or you only have a very small library (< 1000 spectra); classical dot-product similarity is adequate and simpler.
- You need to compute all pairwise similarities in a spectral library without a query spectrum (use batch entropy similarity instead).
- Your data is in formats other than mass spectra (e.g., chromatograms, imaging data, nucleotide sequences).

## Inputs

- spectral_library: list of dictionaries, each with required keys 'precursor_mz' (float) and 'peaks' (array-like of [m/z, intensity] pairs); optional metadata keys allowed
- query_spectrum: dictionary with 'precursor_mz' (float) and 'peaks' (array-like of [m/z, intensity] pairs)
- spectral file formats supported: .mgf, .msp, .mzML, .lbm2

## Outputs

- entropy_similarity: dictionary with four keys ('hybrid_search', 'identity_search', 'neutral_loss_search', 'open_search'), each mapping to a numpy array of float32 similarity scores (range 0–1) for each library spectrum
- ranked candidate list (implicit): sorted by similarity score for compound identification

## How to apply

First, prepare your spectral library in the required format: each spectrum must have at minimum a 'precursor_mz' field and a 'peaks' field containing m/z and intensity pairs (as 2D arrays or lists). Build an index from the library using the FlashEntropySearch.build_index() method, which pre-computes entropy-based data structures to accelerate subsequent searches. For each query spectrum (with its own precursor_mz and peaks), call the search() method to compute entropy similarity scores across all library spectra. The algorithm returns four similarity arrays: hybrid_search (combined filters), identity_search (exact mass matches), neutral_loss_search (mass difference patterns), and open_search (unrestricted mass matching). The rationale is that Flash Entropy Search accelerates entropy similarity computation through indexed filtering, reducing the need to compute full similarities for every spectrum pair.

## Related tools

- **Entropy Search (GUI)** (Standalone graphical interface for interactive real-time visualization and entropy similarity calculation between two MS/MS spectra or searching spectral files against libraries) — https://github.com/YuanyueLi/EntropySearch/releases
- **MSEntropy (Python package)** (Python implementation of spectral entropy, entropy similarity, and the Flash Entropy Search algorithm for programmatic integration) — https://github.com/YuanyueLi/MSEntropy
- **FlashEntropySearch (source repository)** (Original source code, benchmark data, and figures for the Flash Entropy Search manuscript) — https://github.com/YuanyueLi/FlashEntropySearch
- **MS Viewer web app** (Web-based tool for straightforward real-time visualization and entropy similarity calculation for two MS/MS spectra) — https://yuanyueli.github.io/MSViewer

## Examples

```
from ms_entropy import FlashEntropySearch
import numpy as np
entropy_search = FlashEntropySearch()
spectral_library = [{'id': 'spec1', 'precursor_mz': 150.0, 'peaks': [[100.0, 1.0], [101.0, 1.0]]}, {'id': 'spec2', 'precursor_mz': 200.0, 'peaks': np.array([[100.0, 1.0], [102.0, 1.0]], dtype=np.float32)}]
entropy_search.build_index(spectral_library)
query_spectrum = {'precursor_mz': 150.0, 'peaks': np.array([[100.0, 1.0], [101.0, 1.0]], dtype=np.float32)}
entropy_similarity = entropy_search.search(precursor_mz=query_spectrum['precursor_mz'], peaks=query_spectrum['peaks'])
```

## Evaluation signals

- Verify schema compliance: output dictionary contains exactly four keys (hybrid_search, identity_search, neutral_loss_search, open_search), each with a numpy float32 array matching the length of the spectral library.
- Check similarity score bounds: all values in the output arrays fall in the range [0.0, 1.0].
- Validate reproducibility: query results match reported benchmark metrics from the manuscript when run on the same library and query spectra.
- Confirm preprocessing: query and library spectra have been normalized and formatted with m/z and intensity peaks before indexing and search.
- Benchmark throughput: measure queries per second (QPS) to confirm search latency is improved over classical dot-product methods for large libraries.

## Limitations

- Flash Entropy Search algorithm is currently only available in Python; C/C++ and JavaScript implementations exist for entropy calculation but not for the full indexed search.
- The algorithm requires sufficient memory to build and store the index structure; very large libraries (multi-million spectra) may require distributed or incremental indexing strategies not yet documented.
- Search quality depends on spectral quality and peak filtering; low-quality or heavily noise-contaminated spectra may produce uninformative similarity scores.
- Precursor m/z filtering is applied in hybrid and identity search modes; searches with large mass tolerance or open mass mode may incur higher computational cost.

## Evidence

- [other] Flash entropy search to query all mass spectral libraries in real time: "Flash entropy search to query all mass spectral libraries in real time"
- [readme] Flash Entropy Search algorithm significantly accelerates the computation of entropy similarity: "The `Flash Entropy Search` algorithm significantly accelerates the computation of entropy similarity"
- [readme] Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification: "Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification"
- [readme] Step 1: Build the index from the library spectra; Step 2: Search the library: "Step 1: Build the index from the library spectra
entropy_search.build_index(spectral_library)
Step 2: Search the library
entropy_search.search(precursor_mz = query_spectrum_precursor_mz, peaks ="
- [readme] precursor_mz and peaks keys are required: "Note that the `precursor_mz` and `peaks` keys are required, the reset of the keys are optional."
- [readme] The result will look like this: hybrid_search, identity_search, neutral_loss_search, open_search: "{'hybrid_search': array([0.6666666 , 0.99999994, 0.99999994, 0.99999994], dtype=float32),
 'identity_search': array([0.6666667, 0.       , 0.       , 0.       ], dtype=float32),"
- [readme] To search one spectral file against another spectral file or a spectral library, use the Entropy Search GUI. The GUI supports .mgf, .msp, .mzML, and .lbm2 file formats.: "To search one spectral file against another spectral file or a spectral library, use the [Entropy Search GUI](https://github.com/YuanyueLi/EntropySearch). The GUI supports `.mgf`, `.msp`, `.mzML`,"
- [readme] Currently, the Flash entropy search algorithm is only available in Python: "Currently, the Flash entropy search algorithm is only available in **Python**. Use the [`ms-entropy` package`"
