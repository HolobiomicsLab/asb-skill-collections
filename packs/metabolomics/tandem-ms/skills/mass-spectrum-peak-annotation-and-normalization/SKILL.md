---
name: mass-spectrum-peak-annotation-and-normalization
description: Use when you have raw MS/MS spectra in MSP format or as numpy arrays and need to standardize them for comparison or library matching. Specifically, use it before performing electronic or chemical denoising, or before computing entropy-similarity metrics between query and reference spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - Python
  - pandas
  - RDkit
  - spectral_denoising
  - ms_entropy
  - numpy
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41592-025-02646-x
  title: Spectral Denoising
- doi: 10.1038/s41592-023-02012-9
  title: ''
evidence_spans:
- Spectral denoising requires ``Python >= 3.8`` installed on your system
- import spectral_denoising as sd
- pandas==2.2.3
- '- ``pandas==2.2.3``'
- rdkit==2024.3.5
- smiles = 'O=c1nc[nH]c2nc[nH]c12'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectral_denoising_cq
    doi: 10.1038/s41592-025-02646-x
    title: Spectral Denoising
  dedup_kept_from: coll_spectral_denoising_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02646-x
  all_source_dois:
  - 10.1038/s41592-025-02646-x
  - 10.1038/s41592-023-02012-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-peak-annotation-and-normalization

## Summary

Prepare and standardize MS/MS spectra by reading raw peak data, removing malformed or zero-intensity ions, sorting by mass, and optionally computing spectral entropy metrics to enable reliable downstream spectral matching and denoising. This skill handles the foundational data hygiene and normalization required before comparative analysis of noisy versus denoised spectra.

## When to use

Apply this skill when you have raw MS/MS spectra in MSP format or as numpy arrays and need to standardize them for comparison or library matching. Specifically, use it before performing electronic or chemical denoising, or before computing entropy-similarity metrics between query and reference spectra. Trigger this step if input spectra contain zero-intensity peaks, unsorted m/z values, or lack normalized intensity distributions.

## When NOT to use

- Input spectra are already in a normalized feature table or processed matrix format — skip to spectral comparison directly.
- Precursor m/z value is missing or known to be unreliable — entropy_similarity() requires pmz for precursor region masking; consider handling missing values before this step.
- Peak data is in a format other than MSP or numpy array (e.g., mzML, mzXML) — convert to MSP or array first using an appropriate parser outside this workflow.

## Inputs

- MSP file (mass spectrometry peak format) with peaks, precursor_mz, SMILES or formula, and adduct columns
- numpy array of shape (n_peaks, 2) with m/z and intensity pairs (dtype=float32)
- SMILES string or molecular formula for reference compound
- adduct string (e.g., '[M+H]+', '[M+Na]+')
- precursor m/z value (float)

## Outputs

- Sanitized peak array (sorted by m/z, zero-intensity ions removed)
- Spectral entropy value (float, range 0–1 after normalization)
- Normalized entropy value (float, range 0–1)
- Pandas DataFrame with columns: peaks, precursor_mz, SMILES/formula, adduct (for batch)
- Head-to-tail visualization (Jupyter notebook output)

## How to apply

Load spectra from MSP files using sd.read_msp() to extract peak arrays (m/z and intensity pairs) along with precursor m/z, SMILES or formula, and adduct metadata. Remove zero-intensity ions and sort peaks by increasing m/z using sanitize_spectrum() (which wraps remove_zero_ions() and sort_spectrum()); this ensures consistent peak ordering across all downstream operations. Compute baseline spectral entropy and normalized entropy on the cleaned spectrum using spectral_entropy() and normalized_entropy() to quantify signal complexity before denoising. For batch operations on multiple spectra, wrap processing in a main() function to avoid multiprocessing conflicts. These operations establish a canonical spectrum representation required for reliable entropy_similarity() comparisons.

## Related tools

- **spectral_denoising** (Primary package providing sd.read_msp(), sanitize_spectrum(), spectral_entropy(), normalized_entropy(), and entropy_similarity() functions) — https://github.com/FanzhouKong/spectral_denoising
- **ms_entropy** (Dependency for computing entropy and entropy_similarity metrics on normalized spectra) — https://pypi.org/project/ms_entropy/
- **RDkit** (Dependency for SMILES parsing and molecular formula manipulation during peak annotation)
- **numpy** (Array operations and spectral data structure manipulation)
- **pandas** (DataFrame creation and batch metadata handling for multiple spectra)

## Examples

```
import spectral_denoising as sd; import numpy as np
query_data = sd.read_msp('sample_data/query_spectra.msp')
peak_clean = sd.spectral_operations.sanitize_spectrum(query_data.iloc[0]['peaks'])
entropy_val = sd.spectral_entropy(peak_clean)
print(f'Normalized entropy: {sd.normalized_entropy(peak_clean):.2f}')
```

## Evaluation signals

- Output peak array has no zero-intensity ions: all intensity values > 0.
- Output peak array is sorted in ascending m/z order: m/z values form a monotonically increasing sequence.
- Spectral entropy value is in the range [0, 1] after normalization; baseline entropy on clean reference spectra typically ranges 0.6–0.95 depending on complexity.
- Precursor ion region correctly excluded from entropy_similarity() when pmz is provided: peaks within ±10 Da of pmz are masked before similarity computation.
- Batch processing completes without multiprocessing errors: when wrapped in main(), parallel processing on multiple spectra runs without deadlock or orphaned processes.

## Limitations

- Requires Python ≥3.8 and <3.13 due to RDkit compatibility constraints; Python 3.13 is not supported.
- MSP file must include all required columns (peaks, precursor_mz, SMILES or formula, adduct); missing or malformed entries will cause read_msp() to fail or produce incomplete DataFrames.
- Spectral entropy computation assumes non-empty peak arrays; empty spectra will produce undefined or NaN values.
- Batch mode requires explicit main() function wrapper in scripts; direct calls to batch functions outside main() will cause multiprocessing issues on some platforms.
- Head-to-tail visualization (head_to_tail_plot) only works in Jupyter notebooks; does not output to file or CLI.

## Evidence

- [readme] Read spectra from MSP file and extract metadata: "Load sample noisy spectra and reference data from MSP files using sd.read_msp(). Extract a single spectrum with peaks and precursor m/z from the query data."
- [readme] Remove malformed peaks and sort by mass: "``spectral_operations.remove_zero_ions`` will remove ions with zero intensity from the query spectrum. ``spectral_operations.sort_spectrum`` sort the query spectrum by mass."
- [readme] Compute spectral entropy metrics on normalized peaks: "the spectrum entropy of raw spectrum is {spectral_entropy(peak):.2f}, the normalized entropy of raw spectrum is {normalized_entropy(peak):.2f}"
- [readme] Python version and library compatibility requirements: "Please use Python version between 3.8 to 3.12 for this package to work. RDkit currently does not have a distribution compitable to python 3.13!!!!!"
- [readme] Batch processing requires main() wrapper: "Note: if you try to use the batch mode in script and compile it in terminal, please wrap the code in main() function since they are implemented in parallal with multiprocessing and directly calling"
- [readme] Entropy similarity computation with precursor masking: "the entropy similarity of contaminated spectrum and the raw spectrum is {entropy_similairty(peak_with_noise,peak,  pmz = pmz):.2f}"
