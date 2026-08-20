---
name: spectrum-peak-counting-and-reporting
description: Use when when you need to quantify and compare the filtering efficacy
  of mutually exclusive noise-threshold methods on the same input mass spectrum, or
  when validating that a selected noise-filtering strategy retains an expected number
  of peaks for downstream molecular formula assignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  techniques:
  - LC-MS
  - GC-MS
  - MS-imaging
  license_tier: open
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters
  import MSParameters']
- import pandas as pd
- pandas [section=results; evidence='import pandas as pd']
- import numpy as np
- numpy [section=results; evidence='import numpy as np']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems
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

# spectrum-peak-counting-and-reporting

## Summary

Count and report the number of peaks retained in a mass spectrum after applying a selected noise-threshold method (relative_abundance, signal_noise, or log mode), producing structured records of method identifier and peak counts per ionization mode for comparative evaluation.

## When to use

When you need to quantify and compare the filtering efficacy of mutually exclusive noise-threshold methods on the same input mass spectrum, or when validating that a selected noise-filtering strategy retains an expected number of peaks for downstream molecular formula assignment.

## When NOT to use

- Input is a mass list that has already been noise-filtered or centroided by the instrument vendor; peak counting is post-hoc reporting, not applicable to data that lacks the raw signal intensity distribution needed to re-apply threshold criteria.
- Analysis goal requires identification of isotopic clusters or fine structure; peak counting reports total peaks but does not distinguish monoisotopic, isotopic, or artifact peaks.
- Spectrum has already been processed through multiple conflicting noise-threshold steps; multiple successive applications of different methods will compound filtering artifacts.

## Inputs

- Raw mass spectrum file (Bruker .d, ThermoFisher .raw, or CoreMS HDF5 format)
- MSParameters configuration object with noise-threshold method selection
- Noise-threshold parameters: relative_abundance minimum threshold, signal_noise ratio threshold, or log standard deviation cutoff

## Outputs

- Peak count (integer) per noise-threshold method
- Method identifier (string: 'relative_abundance', 'signal_noise', or 'log')
- Ionization mode label (e.g., 'ESI_NEG')
- Structured JSON or CSV record with method name, peak count, and mode

## How to apply

Load a raw mass spectrum (e.g., ESI_NEG_SRFA.d in Bruker or .raw format) using CoreMS MSParameters factory. Select one of three mutually exclusive noise-threshold methods: 'relative_abundance' (filtered by minimum relative abundance parameter), 'signal_noise' (filtered by signal-to-noise ratio threshold), or 'log' (filtered by standard deviation parameter). Apply the selected method to the loaded spectrum using CoreMS peak-filtering routines. Capture and serialize the resulting peak count, method name, and ionization mode identifier as a structured JSON or CSV record. Compare peak counts across methods to evaluate which filtering strategy best balances noise suppression and analyte retention for your analysis goal.

## Related tools

- **CoreMS** (Provides MSParameters factory to instantiate noise-threshold configuration, implements conditional dispatch logic for three mutually exclusive threshold methods, and applies peak-filtering routines to compute final peak counts.) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Serializes peak count results and method metadata into structured DataFrames; enables export to CSV or Excel for downstream comparison.)
- **Docker** (Provides containerized execution environment to ensure reproducible CoreMS-based peak counting workflows across systems.)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters
from corems.data_source.data_source_factory import run_from_file
import json

ms_obj = run_from_file('tests/tests_data/ftms/ESI_NEG_SRFA.d', MSParameters)
for spectrum in ms_obj:
    spectrum.apply_noise_threshold(SNR_threshold=10, noise_method='signal_noise')
    result = {'method': 'signal_noise', 'peak_count': len(spectrum.peaks), 'ionization_mode': 'ESI_NEG'}
    print(json.dumps(result))
```

## Evaluation signals

- Peak count is a non-negative integer; verify it is ≥ 0 and ≤ total m/z centroids detected in the raw spectrum.
- Method identifier matches exactly one of: 'relative_abundance', 'signal_noise', or 'log'; no other mode is reported.
- Peak counts differ across the three mutually exclusive methods applied to the same input spectrum (different methods should produce different retention counts unless the spectrum is trivial).
- Ionization mode label is correctly inherited from input spectrum metadata (e.g., 'ESI_NEG' for negative-ion ESI data).
- JSON or CSV output conforms to expected schema: columns for method name, peak_count, ionization_mode, and optional timestamp; no missing or malformed entries.

## Limitations

- Peak count is a global statistic; it does not distinguish peak quality, confidence, or role in molecular formula assignment.
- The three noise-threshold methods are mutually exclusive; a single spectrum can be processed under only one method at a time, preventing simultaneous multi-method evaluation within a single call.
- Peak counting does not account for m/z calibration accuracy; miscalibrated spectra may produce artificially high or low peak counts if threshold criteria are m/z-dependent.
- CoreMS peak-filtering routines are designed for small-molecule analysis (ESI and FT-MS); applicability to GC-MS, LC-MS, or high-resolution imaging mass spectrometry workflows is not documented in the provided evidence.

## Evidence

- [other] CoreMS provides three mutually exclusive noise threshold methods: 'relative_abundance' (filtered by minimum relative abundance parameter), 'signal_noise' (filtered by signal-to-noise ratio threshold), and 'log' (filtered by standard deviation parameter), each producing different peak retention counts for the same input spectrum.: "CoreMS provides three mutually exclusive noise threshold methods: 'relative_abundance' (filtered by minimum relative abundance parameter), 'signal_noise' (filtered by signal-to-noise ratio"
- [other] Load mass spectrum data from ESI_NEG_SRFA.d using CoreMS MSParameters factory to instantiate noise-threshold configuration. Implement conditional dispatch logic that selects one of three mutually exclusive noise-threshold methods (COND-001, COND-002, COND-003) based on spectrum properties or user input. Apply the selected noise-threshold method to the loaded spectrum using CoreMS peak-filtering routines. Capture the resulting peak count per ionization mode and method name. Serialize the results (method identifier, peak count per mode) as a structured JSON or CSV record.: "Load mass spectrum data from ESI_NEG_SRFA.d using CoreMS MSParameters factory to instantiate noise-threshold configuration...Apply the selected noise-threshold method to the loaded spectrum using"
- [readme] CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.: "CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis"
- [other] from corems.encapsulation.factory.parameters import MSParameters: "from corems.encapsulation.factory.parameters import MSParameters"
- [readme] Bruker Solarix (CompassXtract), Bruker Solarix transients, ser and fid (FT magnitude mode only), ThermoFisher (.raw), Spectroswiss signal booster data-acquisition station (.hdf5): "Bruker Solarix (CompassXtract), Bruker Solarix transients, ser and fid (FT magnitude mode only), ThermoFisher (.raw)"
