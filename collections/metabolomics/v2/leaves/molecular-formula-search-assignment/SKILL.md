---
name: molecular-formula-search-assignment
description: Use when you have a recalibrated FT-ICR mass spectrum (Bruker .d format
  or equivalent) with detected, noise-thresholded peaks and need to assign chemical
  formulas to each peak. This is particularly relevant when analyzing samples with
  unknown composition (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - CoreMS
  - pandas
  - numpy
  - Bruker Solarix reader (ReadBrukerSolarix)
  - EnviroMS
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development
  and data analysis of small molecules analysis.'
- import pandas as pd
- import numpy as np
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-formula-search-assignment

## Summary

Assigns molecular formulas to detected m/z peaks in high-resolution mass spectra by matching observed mass-to-charge ratios against a constrained search space of possible elemental compositions. This skill is essential for converting raw peak lists into chemically interpretable molecular annotations, especially for natural organic matter and complex mixture analysis on FT-ICR instruments.

## When to use

You have a recalibrated FT-ICR mass spectrum (Bruker .d format or equivalent) with detected, noise-thresholded peaks and need to assign chemical formulas to each peak. This is particularly relevant when analyzing samples with unknown composition (e.g., environmental extracts, fulvic acids) or when exploring molecular diversity across a wide m/z range. The skill applies after peak picking and mass calibration are complete.

## When NOT to use

- Input peak list is uncalibrated or has mass accuracy worse than your ppm tolerance window (typical limit ~5–10 ppm for FT-ICR); recalibrate first.
- Peaks are not yet noise-thresholded or picked; apply noise filtering and apex detection before formula assignment.
- Element space is unconstrained or unreasonably wide (e.g., allowing arbitrary atom counts); this will produce false positives and slow computation; use domain knowledge (e.g., molecular weight plausibility, DBE limits) to bound the search.

## Inputs

- Recalibrated FT-ICR mass spectrum object (CoreMS MassSpectrum class or equivalent)
- Detected peak list with m/z, abundance, and baseline-subtracted intensities
- Element atom ranges (min/max counts for C, H, O, N, S)
- Mass error tolerance in ppm (min and max)
- Ionization mode specification (protonated, radical, or adduct type)
- Noise threshold parameters (method and cutoff value)

## Outputs

- Molecular formula assignments (one or more per peak)
- Assigned m/z values (calculated from formula)
- Mass error (observed m/z minus calculated m/z, in ppm or mDa)
- Molecular formula table (peak index, m/z, formula, mass error, abundance)
- Heteroatom classification (DBE, O/C, H/C ratios for each formula)
- Structured export (pandas DataFrame, Excel .xlsx, or CSV)

## How to apply

Initialize SearchMolecularFormulas with element atom constraints (C, H, O, N, S ranges), ionization mode (protonated [M+H]+, radical cation [M•]+, or adducts), and mass error tolerance (typically min/max ppm error bounds appropriate to your instrument field strength, e.g., ±5 ppm for 12 T). Configure the calibration signal-to-noise threshold and noise thresholding method (e.g., relative_abundance or log). Execute the molecular formula assignment algorithm (run_worker_mass_spectrum() in CoreMS) to match each detected m/z value against all possible formulas within your search space. The rationale is that modern FT-ICR instruments achieve mass accuracy sufficient to constrain the solution space to one or a few candidate formulas per peak; the search exhausts all valid combinations within your elemental and mass-error bounds, then ranks or filters by abundance and mass defect patterns.

## Related tools

- **CoreMS** (Provides SearchMolecularFormulas class, MassSpectrum data structure, calibration utilities, and run_worker_mass_spectrum() execution engine for formula assignment on FT-ICR data.) — https://github.com/EMSL-Computing/CoreMS
- **Bruker Solarix reader (ReadBrukerSolarix)** (Imports raw Bruker .d format transient data and applies initial calibration for 12 T and other field-strength instruments.) — https://github.com/EMSL-Computing/CoreMS
- **EnviroMS** (Wrapper workflow for natural organic matter formula assignment; automates element constraints, database search, and molecular formula table generation.) — https://github.com/EMSL-Computing/EnviroMS
- **pandas** (Organizes and exports molecular formula assignments and metadata to tabular formats (DataFrame, Excel, CSV).)
- **numpy** (Supports numerical calculations for mass error, DBE, and heteroatom ratio computations.)

## Examples

```
from corems.mass_spectrum.factory import MSParameters; from corems.transient.input.brukerSolarix import ReadBrukerSolarix; ms = ReadBrukerSolarix('data.d'); MSParameters.mass_spectrum.noise_threshold_method = 'relative_abundance'; MSParameters.molecular_search.url_database = 'sqlite:///molecular_formulas.db'; ms.molecular_search_settings.configure(min_ppm_error=-5, max_ppm_error=5, usedAtoms={'C': (1, 100), 'H': (0, 200), 'O': (0, 20), 'N': (0, 4), 'S': (0, 2)}); ms.run_worker_mass_spectrum()
```

## Evaluation signals

- All detected peaks above noise threshold receive at least one assigned formula (no orphaned peaks unless mass error exceeds tolerance).
- Assigned formulas satisfy elemental constraints (C, H, O, N, S within specified ranges).
- Mass error (observed − calculated m/z) for all assignments falls within the specified ppm tolerance window (e.g., ±5 ppm for 12 T).
- Assigned formulas pass chemical validity checks (e.g., even electron rule for ESI mode; DBE non-negative; H count ≤ 2C + 2 + N − X for typical organic compounds).
- Abundance rank of assigned formulas correlates with spectral prominence (dominant peaks receive unambiguous single-formula assignment; minor peaks may have multiple candidates).

## Limitations

- Mass accuracy degrades over the transient acquisition window; recalibration using known reference masses (e.g., Bruker lock masses or user-supplied calibrants) is essential. Without calibration, formula assignment fails or produces spurious matches.
- The search space grows combinatorially with element ranges; overly broad constraints (e.g., C 0–100, H 0–200) cause false positives and long computation. Domain-specific priors (e.g., natural organic matter typically has DBE < 30, O/C < 1) are needed.
- Isobaric interference: multiple valid formulas may match a single m/z within ppm tolerance, especially at high m/z or for low-resolution data; high-resolution MS (resolving power > 100 000) mitigates this but does not eliminate it.
- Ion adducts and charge states must be specified a priori; misspecification (e.g., assuming [M+H]+ when sample is [M+Na]+) leads to systematic formula offset errors.
- Natural organic matter and environmental samples often contain unknown or unstable functional groups; assigned formulas represent the most plausible candidates given elemental constraints, not necessarily the true structure.

## Evidence

- [other] SearchMolecularFormulas operates by configuring molecular search settings including mass error tolerance (min/max ppm error), element atom constraints (C, H, O, N, S), ionization mode (protonated, radical, adduct), and calibration signal-to-noise threshold, then executing run_worker_mass_spectrum() to match detected m/z values against possible molecular formulas.: "SearchMolecularFormulas operates by configuring molecular search settings including mass error tolerance (min/max ppm error), element atom constraints (C, H, O, N, S), ionization mode (protonated,"
- [readme] CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.: "**CoreMS** is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis."
- [other] Apply noise thresholding and peak picking to detected peaks.: "Apply noise thresholding and peak picking to detected peaks."
- [readme] Automatic molecular formulae assignments algorithm for ESI(-) MS for natural organic matter analysis: "Automatic molecular formulae assignments algorithm for ESI(-) MS for natural organic matter analysis"
- [readme] modern molecular formulae assignment algorithms: "modern molecular formulae assignment algorithms"
- [readme] We'll use a Bruker FTICR-MS dataset of Suwannee River Fulvic Acid (SRFA) acquired on a 15 Tesla instrument: "We'll use a Bruker FTICR-MS dataset of Suwannee River Fulvic Acid (SRFA) acquired on a 15 Tesla instrument"
- [other] Load the recalibrated FT-ICR mass spectrum data file (Bruker .d format) using CoreMS ReadBrukerSolarix.: "Load the recalibrated FT-ICR mass spectrum data file (Bruker .d format) using CoreMS ReadBrukerSolarix."
