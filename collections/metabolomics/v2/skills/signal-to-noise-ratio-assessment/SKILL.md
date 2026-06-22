---
name: signal-to-noise-ratio-assessment
description: Use when when preparing a 1D 1H NMR spectral peak list for input to the NMRformer metabolite identification model, and you have access to peak intensity measurements and noise level estimates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  tools:
  - Pandas
  - NumPy
  - SciPy
  - NMRformer
  techniques:
  - NMR
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05632
  all_source_dois:
  - 10.1021/acs.analchem.4c05632
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# signal-to-noise-ratio-assessment

## Summary

Assessment and filtering of spectral peaks based on signal-to-noise ratio (SNR) to exclude low-quality peaks before metabolite identification in NMR spectroscopy. This skill removes peaks below a quality threshold to prevent degradation of downstream model output in Transformer-based peak assignment workflows.

## When to use

When preparing a 1D 1H NMR spectral peak list for input to the NMRformer metabolite identification model, and you have access to peak intensity measurements and noise level estimates. Use this skill if your input peak list contains peaks of varying quality and you want to exclude low-SNR peaks that would degrade model output accuracy.

## When NOT to use

- If your input peaks have already been manually curated or pre-filtered by your NMR acquisition software — SNR filtering may be redundant
- If you lack intensity or noise level information in your peak list — SNR cannot be calculated
- If your downstream analysis step explicitly requires all detected peaks regardless of quality (e.g., comparative intensity studies where weak peaks carry biological meaning)

## Inputs

- CSV or table file containing chemical shift values (ppm), peak intensities, and optional noise level estimates
- SNR quality threshold value (numeric, user-defined or empirical)
- Optional: reference spectral library or chemical shift database for cross-validation

## Outputs

- Filtered CSV peak list containing only peaks with SNR ≥ threshold
- Peak metadata indicating which peaks passed/failed SNR filtering (optional quality report)

## How to apply

Load the input spectral peak list (CSV or table format containing peak chemical shifts, intensities, and optionally noise estimates) using Pandas. Calculate or retrieve SNR for each peak by dividing peak intensity by local noise level using NumPy. Define a SNR quality threshold (specific threshold value should be determined empirically or from domain expertise). Use NumPy/SciPy boolean indexing to exclude peaks falling below the threshold. Retain peaks meeting or exceeding the SNR cutoff and export the filtered peak list as a CSV file compatible with NMRformer input requirements. The rationale is that noisy peaks with low SNR are unrecognized by the model and degrade metabolite assignment accuracy.

## Related tools

- **Pandas** (Load and manipulate peak list CSV/table format; filter rows based on SNR criteria) — https://pandas.pydata.org
- **NumPy** (Perform SNR calculations (intensity / noise ratio); vectorized boolean indexing for filtering) — https://numpy.org
- **SciPy** (Optional: compute local noise estimates from spectrum; statistical filtering utilities) — https://scipy.org
- **NMRformer** (Downstream metabolite identification model that receives the filtered peak list as input) — https://github.com/zza1211/NMRformer

## Examples

```
import pandas as pd; import numpy as np; peaks = pd.read_csv('input_peaks.csv'); snr_threshold = 3.0; filtered_peaks = peaks[peaks['intensity'] / peaks['noise'] >= snr_threshold]; filtered_peaks.to_csv('filtered_peaks.csv', index=False)
```

## Evaluation signals

- Output peak list contains only peaks with SNR ≥ specified threshold; all peaks below threshold are absent
- Number of filtered peaks is reduced compared to input (unless all peaks already exceeded threshold); retention rate is reasonable (typically 50–95% depending on spectrum quality and threshold stringency)
- Filtered peak list is in valid CSV format with same column structure as input, compatible with NMRformer.ipynb loader
- Spot-check: visually confirm that removed peaks correspond to low-intensity or high-noise regions in the original spectrum
- Downstream NMRformer metabolite assignments show improved confidence scores or reduced false identifications compared to unfiltered peak list

## Limitations

- SNR filtering effectiveness depends critically on accurate noise level estimation or availability of noise metadata; underestimated noise may over-retain weak peaks; overestimated noise may over-filter true weak signals
- The optimal SNR threshold is not provided in NMRformer documentation and must be determined empirically for each instrument, experiment type, and sample matrix; no universal cutoff is recommended
- Cross-reference filtering against a reference spectral library or chemical shift database (mentioned in the source workflow) is not detailed in the NMRformer README; implementation requires external database access
- SNR assessment alone does not detect all forms of artifact or noise (e.g., satellite peaks, solvent contaminants); supplementary manual inspection may be needed for high-stakes applications

## Evidence

- [readme] When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as possible.: "When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as"
- [other] Apply signal-to-noise ratio (SNR) filtering to exclude peaks below a quality threshold using NumPy and SciPy.: "Apply signal-to-noise ratio (SNR) filtering to exclude peaks below a quality threshold using NumPy and SciPy."
- [other] Load the input spectral peak list (CSV or table format containing peak chemical shifts, intensities, and metadata) using Pandas.: "Load the input spectral peak list (CSV or table format containing peak chemical shifts, intensities, and metadata) using Pandas."
- [intro] Noisy peaks or unrecognized peaks in the input spectral peak list can negatively affect model output: "Noisy peaks or unrecognized peaks in the input spectral peak list can negatively affect model output"
