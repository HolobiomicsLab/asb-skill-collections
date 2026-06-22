---
name: nmr-peak-quality-filtering
description: Use when you have a CSV or table-formatted input spectral peak list (chemical shifts, intensities, metadata) destined for NMRformer metabolite identification, and you observe or suspect that the list contains noisy peaks or peaks with chemical shifts that do not match known reference standards.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
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

# nmr-peak-quality-filtering

## Summary

Filter unrecognized and noisy peaks from input 1D 1H NMR spectral peak lists before feeding them to the NMRformer Transformer model. This preprocessing step removes peaks with low signal-to-noise ratio and unmatched chemical shifts, preventing degradation of metabolite identification output.

## When to use

You have a CSV or table-formatted input spectral peak list (chemical shifts, intensities, metadata) destined for NMRformer metabolite identification, and you observe or suspect that the list contains noisy peaks or peaks with chemical shifts that do not match known reference standards. Apply this skill to improve model accuracy and reduce false or spurious metabolite assignments.

## When NOT to use

- Input peak list is already pre-filtered by your NMR acquisition software or has been validated against a curated database.
- Your analysis goal is to detect and quantify *all* signals including artifacts (e.g., for diagnostic purposes or method development); removing peaks will bias results.
- You lack a reference spectral library or SNR baseline for your instrument and sample type, making unrecognized peak detection unreliable.

## Inputs

- CSV file: chemical shift (ppm) and 1H NMR intensity values
- Table or DataFrame: peak metadata including chemical shift, intensity, and optional quality indicators
- Reference spectral library or chemical shift database for validation

## Outputs

- Filtered CSV file: chemical shift and intensity columns, noisy and unrecognized peaks removed
- Peak quality report: count of peaks removed, SNR threshold applied, unrecognized peaks flagged

## How to apply

Load the input spectral peak list using Pandas as a DataFrame, with chemical shift and intensity columns. Apply signal-to-noise ratio (SNR) filtering using NumPy and SciPy to exclude peaks below a quality threshold (specific SNR cutoff to be determined from your instrument's noise floor and expected peak heights). Cross-reference remaining peaks against a reference spectral library or chemical shift database (e.g., HMDB, literature standards) to identify peaks whose chemical shifts fall outside expected tolerance ranges (typical tolerance ~0.1 ppm for 1H NMR). Mark and remove flagged low-SNR and unrecognized peaks. Export the filtered peak list as a CSV file with the same structure as the input, ensuring compatibility with NMRformer's input requirements (chemical shift in first column, intensity in second column).

## Related tools

- **Pandas** (Load and manipulate input spectral peak list CSV/table; filter and export results)
- **NumPy** (Compute signal-to-noise ratios and apply SNR-based filtering thresholds)
- **SciPy** (Statistical functions for SNR calculation and noise floor estimation)
- **NMRformer** (Downstream Transformer model that receives the filtered peak list for metabolite identification) — github.com/zza1211/NMRformer

## Examples

```
import pandas as pd; import numpy as np; from scipy import signal; peaks = pd.read_csv('input_peaks.csv', header=None); snr = peaks.iloc[:, 1] / np.std(peaks.iloc[:, 1]); filtered = peaks[snr >= 3.0]; filtered.to_csv('filtered_peaks.csv', header=False, index=False)
```

## Evaluation signals

- Verify that the output CSV has the same column structure as the input (chemical shift, intensity) and contains fewer or equal rows.
- Check that all retained peaks have SNR values ≥ the applied threshold and chemical shifts match known reference standards within tolerance.
- Confirm that NMRformer model performance (accuracy, confidence scores in output.csv) improves or does not degrade when run on the filtered peak list compared to unfiltered input.
- Inspect removed peaks: low-SNR peaks should cluster near the noise floor; unrecognized peaks should have chemical shifts outside known metabolite ranges.
- Run the filtered peak list through the NMRformer.ipynb notebook and verify that the resulting output.csv contains metabolite assignments with expected probability distributions (no anomalous high-confidence matches to artifacts).

## Limitations

- The specific SNR threshold and chemical shift tolerance are not detailed in the NMRformer documentation; users must determine these parameters empirically based on their instrument, sample preparation, and reference library.
- Reference spectral library quality and coverage directly affect unrecognized peak detection; incomplete or biased libraries may incorrectly flag legitimate peaks.
- Filtering may remove low-abundance metabolite peaks if their SNR is near the noise floor, potentially missing trace metabolites.
- No automated changelog or validation report is provided; manual inspection of removed peaks is recommended to detect over-filtering.

## Evidence

- [readme] When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as possible.: "When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as"
- [intro] The NMRformer workflow requires manual or automated filtering of the input spectral peak list to exclude unrecognized or noisy peaks, since such peaks degrade model output; however, the specific filtering criteria and implementation method are not detailed in the available documentation.: "The NMRformer workflow requires manual or automated filtering of the input spectral peak list to exclude unrecognized or noisy peaks, since such peaks degrade model output"
- [intro] Apply signal-to-noise ratio (SNR) filtering to exclude peaks below a quality threshold using NumPy and SciPy. Cross-reference remaining peaks against a reference spectral library or chemical shift database to identify and mark unrecognized peaks.: "Apply signal-to-noise ratio (SNR) filtering to exclude peaks below a quality threshold using NumPy and SciPy. Cross-reference remaining peaks against a reference spectral library or chemical shift"
- [intro] Load the input spectral peak list (CSV or table format containing peak chemical shifts, intensities, and metadata) using Pandas.: "Load the input spectral peak list (CSV or table format containing peak chemical shifts, intensities, and metadata) using Pandas."
- [readme] the first column is the chemical shift, and the second column is the 1H NMR spectrum: "the first column is the chemical shift, and the second column is the 1H NMR spectrum"
