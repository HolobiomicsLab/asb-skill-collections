---
name: chemical-shift-reference-matching
description: Use when when preparing an input spectral peak list for NMRformer or similar Transformer-based peak assignment models, and you have observed peaks whose chemical shifts do not align with known metabolite signatures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - Pandas
  - NumPy
  - SciPy
  - NMRformer
derived_from:
- doi: 10.1021/acs.analchem.4c05632
  title: NMRformer
evidence_spans:
- pip install pandas==1.5.1
- pip install numpy==1.26.4
- pip install scipy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmrformer_cq
    doi: 10.1021/acs.analchem.4c05632
    title: NMRformer
  dedup_kept_from: coll_nmrformer_cq
schema_version: 0.2.0
---

# chemical-shift-reference-matching

## Summary

Cross-reference observed spectral peaks against a chemical shift database or reference library to identify and flag unrecognized peaks before feeding data to a peak-assignment model. This step removes peaks that the model cannot reliably assign, improving prediction accuracy.

## When to use

When preparing an input spectral peak list for NMRformer or similar Transformer-based peak assignment models, and you have observed peaks whose chemical shifts do not align with known metabolite signatures. Specifically, use this skill when you need to distinguish between legitimate spectral features and noise or instrumental artifacts that will degrade model output.

## When NOT to use

- Input peak list has already been manually curated and validated by an expert; re-filtering may introduce false negatives.
- Your goal is to *discover* novel peaks or unexpected metabolites; aggressive filtering will suppress rare or shifted signals.
- No reference spectral library or chemical shift database is available for your sample matrix; filtering criteria cannot be defined.

## Inputs

- CSV or table-format spectral peak list with columns: chemical shift (ppm), peak intensity, and optional metadata
- Reference spectral library or chemical shift database (BMRB, HMDB, or custom)
- SNR threshold (numeric; typical range 3–10 for NMR)

## Outputs

- Filtered spectral peak list (CSV) with unrecognized and low-SNR peaks removed
- Peak flagging log or metadata indicating which peaks were excluded and why (unrecognized vs. low SNR)
- Summary statistics (count of peaks removed, SNR distribution of retained peaks)

## How to apply

Load the input spectral peak list (CSV or table format with chemical shifts and intensities) using Pandas. For each observed peak, compute the absolute chemical shift difference against entries in a reference spectral library or chemical shift database. Flag peaks whose nearest reference match falls outside a tolerance window (e.g., >0.05 ppm for 1H NMR) or whose match confidence is below a threshold. Mark these as unrecognized. Combine unrecognized-peak filtering with signal-to-noise ratio (SNR) filtering: use NumPy and SciPy to exclude peaks below an SNR quality threshold. Remove all flagged peaks and export the cleaned list as CSV compatible with NMRformer input.

## Related tools

- **Pandas** (Load, manipulate, and export spectral peak list tables (CSV/DataFrame operations))
- **NumPy** (Compute chemical shift distances and SNR filtering thresholds)
- **SciPy** (Apply signal-to-noise ratio (SNR) filtering and statistical threshold computation)
- **NMRformer** (Downstream Transformer-based model that receives the filtered peak list for peak assignment and metabolite identification) — github.com/zza1211/NMRformer

## Examples

```
import pandas as pd; import numpy as np; peaks = pd.read_csv('input_peaks.csv', names=['shift', 'intensity']); snr = peaks['intensity'] / peaks['intensity'].std(); filtered = peaks[snr > 5]; filtered.to_csv('filtered_peaks.csv', index=False)
```

## Evaluation signals

- Filtered peak list has no peaks below the specified SNR threshold and all retained peaks have reference matches within the chemical shift tolerance window.
- Comparison of model output (metabolite assignments) on unfiltered vs. filtered peak lists shows improved assignment confidence or reduced spurious metabolite calls when using filtered input.
- Peak flagging log correctly identifies and reports the filtering reason (unrecognized vs. low SNR) for all excluded peaks; no false negatives (legitimate peaks incorrectly removed) are present upon manual review of a sample subset.
- Filtered peak list conforms to NMRformer input schema (CSV columns and format as documented in NMRformer.ipynb).
- Retention rate (filtered peaks / original peaks) is reasonable for the sample type and quality (typically 70–95% for high-quality spectra).

## Limitations

- Filtering efficacy depends on the completeness and accuracy of the reference spectral library; if the library is biased toward common metabolites, novel or rare peaks may be incorrectly flagged as unrecognized.
- Chemical shift tolerance thresholds (e.g., 0.05 ppm) are empirical and may not account for field-dependent shifts or pH/solvent effects; inappropriate thresholds will cause either over-filtering or under-filtering.
- SNR definition and measurement are instrument- and acquisition-dependent; a fixed SNR threshold may not generalize across different NMR spectrometers or pulse sequences.
- The README notes that 'noisy peaks or unrecognized peaks in the input spectral peak list can negatively affect model output' but does not specify quantitative thresholds or benchmark reference libraries, requiring users to define parameters empirically.

## Evidence

- [readme] When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as possible.: "When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as"
- [other] The NMRformer workflow requires manual or automated filtering of the input spectral peak list to exclude unrecognized or noisy peaks, since such peaks degrade model output.: "The NMRformer workflow requires manual or automated filtering of the input spectral peak list to exclude unrecognized or noisy peaks, since such peaks degrade model output"
- [other] Cross-reference remaining peaks against a reference spectral library or chemical shift database to identify and mark unrecognized peaks.: "Cross-reference remaining peaks against a reference spectral library or chemical shift database to identify and mark unrecognized peaks."
- [other] Apply signal-to-noise ratio (SNR) filtering to exclude peaks below a quality threshold using NumPy and SciPy.: "Apply signal-to-noise ratio (SNR) filtering to exclude peaks below a quality threshold using NumPy and SciPy."
- [other] Load the input spectral peak list (CSV or table format containing peak chemical shifts, intensities, and metadata) using Pandas.: "Load the input spectral peak list (CSV or table format containing peak chemical shifts, intensities, and metadata) using Pandas."
