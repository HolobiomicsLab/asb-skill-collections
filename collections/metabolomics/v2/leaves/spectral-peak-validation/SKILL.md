---
name: spectral-peak-validation
description: Use when before feeding a peak list into the NMRformer model or other
  transformer-based spectral assignment frameworks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3050
  tools:
  - Pandas
  - NumPy
  - SciPy
  - NMRformer
  techniques:
  - NMR
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-validation

## Summary

Filter unrecognized and noisy peaks from input spectral peak lists prior to model inference, using signal-to-noise ratio thresholds and reference spectral library cross-referencing. This preprocessing step is critical for NMRformer and similar peak-assignment models, as unfiltered noisy or unrecognized peaks degrade metabolite identification accuracy.

## When to use

Before feeding a peak list into the NMRformer model or other transformer-based spectral assignment frameworks. Apply this skill when you have a raw or minimally curated input peak list (CSV or table format with chemical shifts, intensities, and metadata) derived from 1D ¹H NMR spectral processing, and you need to improve model output quality by removing peaks that either fall below signal quality thresholds or do not map to known metabolite chemical shift ranges.

## When NOT to use

- Input is already manually curated or pre-filtered by an expert annotator; re-filtering may remove valid but unusual peaks.
- You are working with a peak list that has already undergone vendor-specific spectral deconvolution and quality filtering; additional filtering may over-reduce the peak set.
- The reference spectral library or chemical shift database is absent or unreliable; cross-referencing will produce high false-positive removal rates.

## Inputs

- spectral peak list in CSV or table format (columns: chemical shift, intensity, metadata)
- reference spectral library or chemical shift database
- SNR threshold or peak quality criterion (numeric)

## Outputs

- filtered spectral peak list in CSV format compatible with NMRformer input
- summary of removed peaks (optional log or report)

## How to apply

Load the input spectral peak list (CSV or table format) using Pandas, preserving columns for chemical shift, intensity, and any metadata. Apply signal-to-noise ratio (SNR) filtering using NumPy and SciPy to exclude peaks below a quality threshold (specific SNR cutoff should be determined empirically or from instrument specifications). Cross-reference remaining peaks against a reference spectral library or chemical shift database to identify peaks that cannot be assigned to known metabolites or fall outside expected chemical shift ranges for the target metabolite class. Remove or flag unrecognized and low-SNR peaks, then export the filtered peak list as a CSV file compatible with NMRformer's input requirements (first column: chemical shift; second column: intensity or spectrum values). The rationale is that noisy peaks introduce spurious model predictions, while unrecognized peaks provide no signal for the model to learn from; removing them concentrates the model's attention on high-confidence, metabolite-relevant peaks.

## Related tools

- **Pandas** (Load, manipulate, and export the spectral peak list in CSV/table format)
- **NumPy** (Compute signal-to-noise ratios and apply numeric filtering thresholds)
- **SciPy** (Provide statistical filtering and signal processing utilities (e.g., for SNR calculation))
- **NMRformer** (Downstream transformer-based model that consumes the filtered peak list for peak assignment and metabolite identification) — github.com/zza1211/NMRformer

## Examples

```
import pandas as pd; import numpy as np; from scipy import signal; peaks_df = pd.read_csv('input_peaks.csv', header=None, names=['chemical_shift', 'intensity']); snr = peaks_df['intensity'] / peaks_df['intensity'].std(); filtered_df = peaks_df[snr > 3.0]; filtered_df.to_csv('filtered_peaks.csv', index=False, header=False)
```

## Evaluation signals

- Output CSV contains only peaks with SNR above the specified threshold; verify by comparing input and output peak counts and spot-checking SNR values.
- All peaks in the output are present in the reference spectral library or fall within known metabolite chemical shift ranges; verify by cross-reference against the library.
- The downstream NMRformer model produces metabolite assignments with higher confidence scores and lower spurious metabolite predictions when fed the filtered peak list versus the unfiltered list (measurable via output.csv probability columns).
- Output CSV adheres to NMRformer input schema: first column is chemical shift (ppm), second column is intensity or spectrum value; verify via schema validation or file inspection.
- Removed peaks are logged with their SNR values and reason for removal (e.g., 'SNR < threshold', 'unrecognized chemical shift'); spot-check that removal decisions are consistent with the filtering parameters.

## Limitations

- The specific SNR threshold and reference library cutoff values are not detailed in the NMRformer documentation; practitioners must determine these empirically or from instrument/protocol specifications.
- Cross-referencing against a chemical shift database assumes the database is comprehensive and accurate for the target metabolite class; incomplete or biased reference libraries will introduce false removals or false acceptances.
- The skill does not address systematic noise patterns (e.g., solvent residual peaks, instrumental artifacts) that may require domain-specific masking or suppression techniques beyond SNR filtering.
- Manual curation or validation of the filtered peak list may still be necessary for edge cases (e.g., metabolites with overlapping or atypical chemical shifts).

## Evidence

- [readme] When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as possible.: "When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as"
- [other] Apply signal-to-noise ratio (SNR) filtering to exclude peaks below a quality threshold using NumPy and SciPy. Cross-reference remaining peaks against a reference spectral library or chemical shift database to identify and mark unrecognized peaks.: "Apply signal-to-noise ratio (SNR) filtering to exclude peaks below a quality threshold using NumPy and SciPy. Cross-reference remaining peaks against a reference spectral library or chemical shift"
- [other] Load the input spectral peak list (CSV or table format containing peak chemical shifts, intensities, and metadata) using Pandas.: "Load the input spectral peak list (CSV or table format containing peak chemical shifts, intensities, and metadata) using Pandas."
- [other] The NMRformer workflow requires manual or automated filtering of the input spectral peak list to exclude unrecognized or noisy peaks, since such peaks degrade model output: "The NMRformer workflow requires manual or automated filtering of the input spectral peak list to exclude unrecognized or noisy peaks, since such peaks degrade model output"
