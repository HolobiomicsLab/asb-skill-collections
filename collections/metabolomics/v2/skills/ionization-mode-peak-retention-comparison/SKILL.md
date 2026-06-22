---
name: ionization-mode-peak-retention-comparison
description: Use when when you have loaded a raw mass spectrum (e.g. ESI_NEG_SRFA.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters import MSParameters']
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

# ionization-mode-peak-retention-comparison

## Summary

Compare peak retention counts across three mutually exclusive noise-threshold methods (relative_abundance, signal_noise, log) applied to the same mass spectrum, stratified by ionization mode. This skill reveals how method selection affects spectral feature yield and enables data-driven choice of noise filtering strategy.

## When to use

When you have loaded a raw mass spectrum (e.g. ESI_NEG_SRFA.d or similar Bruker/Thermo instrument file) and need to evaluate which noise-threshold method—relative_abundance (minimum relative abundance parameter), signal_noise (signal-to-noise ratio threshold), or log (standard deviation parameter)—will preserve the most interpretable peaks for downstream molecular formula assignment or spectral analysis. Use this skill before committing to a single noise-filtering approach.

## When NOT to use

- Input spectrum has already been filtered by a single noise-threshold method; this skill requires access to the raw, unfiltered peak list.
- Analysis goal does not include noise-method selection or downstream feature validation (e.g., you have already committed to one filtering approach and need only to apply it).
- Spectrum is already preprocessed into a curated feature table or molecular formula table; peak-count comparison is only meaningful on raw or minimally processed spectra.

## Inputs

- Raw mass spectrum data file (Bruker .d, Thermo .raw, or CoreMS-compatible format)
- MSParameters configuration object with noise-threshold settings instantiated

## Outputs

- Peak count per noise-threshold method (integer)
- Method identifier / name (string: 'relative_abundance', 'signal_noise', or 'log')
- Ionization mode label (string: ESI_NEG, ESI_POS, etc.)
- Structured comparison record (JSON or CSV row with method, mode, peak count)

## How to apply

Load the raw spectrum using CoreMS MSParameters factory to instantiate noise-threshold configuration. Implement conditional dispatch logic that sequentially applies each of the three mutually exclusive noise-threshold methods to the same spectrum object. For each method, capture the resulting peak count and method identifier. Rationale: because each method uses a different filtering criterion (relative abundance threshold, signal-to-noise ratio, or standard deviation), they produce different numbers of retained peaks. Comparing counts across modes reveals which method retains features most aggressively or conservatively, informing choice of filtering strategy. Serialize results (method name, peak count per ionization mode, spectrum identifier) as structured JSON or CSV to enable aggregation and statistical comparison across multiple spectra.

## Related tools

- **CoreMS** (Python framework for instantiating MSParameters, loading raw spectra, and applying mutually exclusive noise-threshold dispatch logic (COND-001, COND-002, COND-003) to measure peak retention per method) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Data serialization and aggregation of method comparison results (peak counts per ionization mode and method) into structured CSV or DataFrame for statistical summary)
- **numpy** (Numerical operations on peak count arrays and aggregation statistics across multiple spectra or ionization modes)
- **Docker** (Containerized reproducible environment for CoreMS execution and noise-threshold parameter configuration across different systems)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters
from corems.mass_spectrum.factory import MassSpectrumFactory

ms_params = MSParameters()
spectrum = MassSpectrumFactory.load_from_bruker('tests/tests_data/ftms/ESI_NEG_SRFA.d')

results = []
for method in ['relative_abundance', 'signal_noise', 'log']:
  ms_params.noise_threshold.method = method
  spectrum.apply_noise_threshold()
  results.append({'method': method, 'peak_count': len(spectrum.peaks), 'ionization_mode': 'ESI_NEG'})

import pandas as pd
pd.DataFrame(results).to_csv('noise_method_comparison.csv', index=False)
```

## Evaluation signals

- Three distinct peak counts returned (one per noise-threshold method) for the same input spectrum, with no method count equal to another (unless spectrum properties are pathological).
- Peak counts are integers ≥ 0 and typically decrease monotonically from least to most aggressive filtering (relative_abundance > signal_noise > log, or similar ordering depending on parameter settings).
- Ionization mode label matches the input spectrum metadata (e.g., ESI_NEG for negative-mode ESI data).
- Serialized output record includes all four fields (method name, peak count, ionization mode, spectrum ID) with no null or missing values.
- Peak counts remain stable when the same spectrum is reprocessed with identical MSParameters, confirming reproducibility of noise-threshold dispatch logic.

## Limitations

- Comparison is valid only for the same spectrum; peak counts are not directly comparable across different spectra with different baseline intensities or m/z ranges without normalization.
- Each noise-threshold method requires careful tuning of its specific parameter (relative_abundance threshold, signal_noise ratio, log standard deviation) to be meaningful; default or arbitrary parameter values may not reflect realistic trade-offs.
- The skill does not automate parameter optimization; practitioners must manually set these thresholds or use external validation (e.g., comparison to reference standards) to judge which method is most appropriate for their analytical goal.
- CoreMS peak-filtering routines apply the selected method to the entire spectrum; no per-region or adaptive thresholding is implemented by this skill.

## Evidence

- [other] CoreMS provides three mutually exclusive noise threshold methods: 'relative_abundance' (filtered by minimum relative abundance parameter), 'signal_noise' (filtered by signal-to-noise ratio threshold), and 'log' (filtered by standard deviation parameter), each producing different peak retention counts for the same input spectrum.: "CoreMS provides three mutually exclusive noise threshold methods: 'relative_abundance' (filtered by minimum relative abundance parameter), 'signal_noise' (filtered by signal-to-noise ratio"
- [other] Load mass spectrum data from ESI_NEG_SRFA.d using CoreMS MSParameters factory to instantiate noise-threshold configuration. Implement conditional dispatch logic that selects one of three mutually exclusive noise-threshold methods (COND-001, COND-002, COND-003) based on spectrum properties or user input. Apply the selected noise-threshold method to the loaded spectrum using CoreMS peak-filtering routines. Capture the resulting peak count per ionization mode and method name. Serialize the results (method identifier, peak count per mode) as a structured JSON or CSV record.: "Load mass spectrum data from ESI_NEG_SRFA.d using CoreMS MSParameters factory to instantiate noise-threshold configuration. Implement conditional dispatch logic that selects one of three mutually"
- [readme] from corems.encapsulation.factory.parameters import MSParameters: "from corems.encapsulation.factory.parameters import MSParameters"
- [readme] Automatic local (SQLite) or external (PostgreSQL) database check, generation, and search: "Automatic local (SQLite) or external (PostgreSQL) database check, generation, and search"
