---
name: conditional-dispatch-workflow-implementation
description: Use when when you have loaded a raw mass spectrum (e.g., ESI_NEG_SRFA.d in Bruker or .raw format) and need to apply one of several noise-threshold strategies based on user preference or spectrum metadata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Conditional-Dispatch Workflow Implementation

## Summary

A pattern for implementing mutually exclusive signal-processing branches in mass spectrometry workflows, where spectrum properties or user parameters trigger selection of one noise-thresholding method (relative_abundance, signal_noise, or log) to filter and retain different peak populations from raw MS data.

## When to use

When you have loaded a raw mass spectrum (e.g., ESI_NEG_SRFA.d in Bruker or .raw format) and need to apply one of several noise-threshold strategies based on user preference or spectrum metadata. Use this skill when you must decide between filtering by minimum relative abundance, signal-to-noise ratio, or standard deviation, and each choice produces materially different peak retention counts that will affect downstream annotation or quantification.

## When NOT to use

- Input spectrum has already been noise-filtered or peak-picked by the instrument firmware or an upstream processing step; re-applying conditional dispatch risks losing peaks or introducing inconsistent thresholds.
- All three noise-threshold methods are expected to yield equivalent results (e.g., a synthetic or heavily pre-processed spectrum with already-separated signal and noise); conditional dispatch adds computational overhead without informing method choice.
- A single fixed noise-threshold strategy is mandated by protocol or regulatory requirement; conditional dispatch implies flexibility that may not be available or desirable.

## Inputs

- Raw mass spectrum file (Bruker .d, Thermo .raw, or CoreMS-exported HDF5)
- MSParameters configuration object specifying noise-threshold mode and parameters
- User selection or programmatic trigger indicating preferred noise-threshold strategy

## Outputs

- Filtered mass spectrum object with peaks retained according to selected noise-threshold method
- Peak count per ionization mode and method identifier
- Structured JSON or CSV record containing method name, peak counts, and metadata

## How to apply

Load mass spectrum data using CoreMS MSParameters factory to instantiate noise-threshold configuration. Implement conditional logic (e.g., if-then or case dispatch) that selects one of three mutually exclusive noise-threshold methods based on spectrum properties or user input: 'relative_abundance' (filtered by minimum relative abundance parameter), 'signal_noise' (filtered by signal-to-noise ratio threshold), or 'log' (filtered by standard deviation parameter). Apply the selected method to the loaded spectrum using CoreMS peak-filtering routines. Capture the resulting peak count per ionization mode and method name, then serialize results (method identifier, peak count per mode) as structured JSON or CSV for downstream analysis or comparison.

## Related tools

- **CoreMS** (Provides MSParameters factory, mass spectrum data structures, and mutually exclusive noise-threshold filtering routines (relative_abundance, signal_noise, log modes)) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Serialization and tabular representation of filtered peak counts and method results)
- **Docker** (Containerized execution environment for reproducible conditional-dispatch workflows)
- **numpy** (Numerical array operations supporting parameter thresholds and peak count aggregation)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; params = MSParameters('tests/tests_data/ftms/ESI_NEG_SRFA.d'); params.ms_peak.noise_threshold_method = 'signal_noise'; spectrum = params.get_spectrum(); filtered_peaks = spectrum.apply_noise_threshold(); print(f'Method: signal_noise, Peaks retained: {len(filtered_peaks)}')
```

## Evaluation signals

- Verify that exactly one of the three noise-threshold methods was applied (no overlapping or duplicate filtering).
- Confirm that peak counts differ between methods for the same input spectrum, validating that the conditional branch was correctly selected and executed.
- Check that serialized JSON/CSV output contains method identifier, peak count per ionization mode, and expected metadata fields.
- Validate that the filtered peak list is a proper subset of the original spectrum (no new peaks introduced).
- Confirm reproducibility: running the same workflow with identical parameters and user selection yields identical method name and peak counts.

## Limitations

- The three noise-threshold methods are mutually exclusive by design; a single spectrum cannot be processed with multiple methods simultaneously within a single workflow execution without repeated dispatch cycles.
- Peak count alone does not validate method correctness; chemical interpretation requires downstream molecular formula assignment or spectral comparison.
- Parameter sensitivity varies by method: relative_abundance depends on minimum abundance cutoff, signal_noise depends on SNR threshold, and log depends on standard deviation multiplier; user must understand and tune parameters appropriate to the ionization mode and analyte class.
- CoreMS noise-threshold methods are optimized for small-molecule analysis; applicability to polymer or macromolecular MS data is not documented.

## Evidence

- [other] CoreMS provides three mutually exclusive noise threshold methods: 'relative_abundance' (filtered by minimum relative abundance parameter), 'signal_noise' (filtered by signal-to-noise ratio threshold), and 'log' (filtered by standard deviation parameter), each producing different peak retention counts for the same input spectrum.: "CoreMS provides three mutually exclusive noise threshold methods: 'relative_abundance' (filtered by minimum relative abundance parameter), 'signal_noise' (filtered by signal-to-noise ratio"
- [other] Load mass spectrum data from ESI_NEG_SRFA.d using CoreMS MSParameters factory to instantiate noise-threshold configuration. Implement conditional dispatch logic that selects one of three mutually exclusive noise-threshold methods based on spectrum properties or user input. Apply the selected noise-threshold method to the loaded spectrum using CoreMS peak-filtering routines. Capture the resulting peak count per ionization mode and method name. Serialize the results (method identifier, peak count per mode) as a structured JSON or CSV record.: "Load mass spectrum data from ESI_NEG_SRFA.d using CoreMS MSParameters factory to instantiate noise-threshold configuration. Implement conditional dispatch logic that selects one of three mutually"
- [readme] CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.: "CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis."
- [readme] from corems.encapsulation.factory.parameters import MSParameters: "from corems.encapsulation.factory.parameters import MSParameters"
- [readme] Manual and automatic noise threshold calculation: "Manual and automatic noise threshold calculation"
