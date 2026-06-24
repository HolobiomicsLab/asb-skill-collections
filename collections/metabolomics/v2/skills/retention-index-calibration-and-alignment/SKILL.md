---
name: retention-index-calibration-and-alignment
description: Use when processing raw GC-MS data in NetCDF format where peaks have
  been detected but lack standardized retention indices.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3047
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  - ReadAndiNetCDF
  - LowResMassSpectralMatch
  techniques:
  - GC-MS
  license_tier: restricted
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

# Retention-Index Calibration and Alignment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calibrate gas chromatography retention times against reference alkane standards to compute retention indices (RI) for each detected peak, enabling standardized peak identification across different instruments and experimental conditions. This skill is essential for GC-MS compound identification workflows where spectral library matching relies on both mass spectral similarity and retention-index proximity.

## When to use

Apply this skill when processing raw GC-MS data in NetCDF format where peaks have been detected but lack standardized retention indices. Use it as a prerequisite to spectral library matching workflows that score compound matches by both cosine similarity and RI-proximity, especially when working with low-resolution mass spectrometry data against reference libraries like PNNLMetV20191015.MSL that include RI metadata.

## When NOT to use

- Input data is already processed and contains pre-computed, validated retention indices from a certified reference database.
- GC instrument does not include alkane standards or retention time calibrants in the experimental run.
- Analysis does not require spectral library matching or compound identification; RI calibration adds no value for purely structural or quantitative peak profiling.

## Inputs

- Raw GC-MS data in ANDI NetCDF format (.cdf)
- Detected chromatographic peaks with retention times
- Reference alkane standard peak list with known RIs

## Outputs

- Peak table with computed retention indices (RI values)
- RI calibration coefficients (linear or polynomial)
- Calibrated retention time–RI mapping for downstream spectral matching

## How to apply

Load the raw GC-MS NetCDF data and extract retention time data for all detected peaks. Apply the GC_RI_Calibration step to align peak retention times against reference alkane standards (e.g., C8–C40 or equivalent), computing linear or polynomial calibration coefficients. Once calibrated, calculate the retention index for each peak using the formula: RI = 100 × [log(RT_sample) − log(RT_lower_alkane)] / [log(RT_upper_alkane) − log(RT_lower_alkane)], where RT values are from adjacent reference alkanes. Store computed RIs alongside peak m/z and intensity data. These RI values then serve as secondary matching criteria during spectral library matching, improving confidence in compound assignments by penalizing matches with poor RI agreement.

## Related tools

- **CoreMS** (Provides GC_RI_Calibration class and ReadAndiNetCDF data loader for NetCDF GC-MS data ingestion and retention index computation.) — https://github.com/EMSL-Computing/CoreMS
- **ReadAndiNetCDF** (Parses raw GC-MS data in NetCDF format, extracting instrument parameters and chromatographic signals (retention times) for calibration.) — https://github.com/EMSL-Computing/CoreMS
- **LowResMassSpectralMatch** (Consumes computed retention indices as secondary matching criterion during spectral library matching, scoring matches by both cosine similarity and RI-proximity.) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Aggregates calibrated peaks and RIs into structured data frames for downstream analysis and export.)
- **numpy** (Performs numerical calculations for calibration polynomial fitting and RI formula evaluation.)

## Examples

```
from corems.encapsulation.factory.parameters import GCMSParameters; from corems.data_source.andi_netcdf import ReadAndiNetCDF; gcms_run = ReadAndiNetCDF('sample.cdf'); gcms_run.gc_ri_calibration(alkane_list=['C8', 'C10', 'C12']); peaks_df = gcms_run.to_dataframe(include_ri=True)
```

## Evaluation signals

- Computed RI values fall within expected ranges (typically 700–3000 for small organic compounds on standard columns) and show smooth, monotonically increasing progression across the chromatogram.
- Calibration residuals (difference between observed and fitted RIs for reference alkanes) are <2 RI units, indicating good linear or polynomial fit quality.
- Downstream spectral library matches show improved confidence and specificity when RI proximity is factored into the match score; matches with RIs far from the library reference should be down-ranked.
- Peak table output schema includes RI column with no missing values for peaks above the noise threshold, and metadata includes calibration coefficients and alkane standard identifiers used.
- Validation: compare computed RIs for the same compound on different GC runs or instruments; RIs should be reproducible to ±5 RI units if calibration is sound.

## Limitations

- RI calibration assumes the presence and correct identification of alkane reference standards in the experimental run; missing or misidentified standards will introduce systematic calibration error.
- RI values are column-dependent and temperature-dependent; calibration is valid only for the specific column phase and oven temperature program used in the experiment.
- Non-linear retention time drifts over long analytical runs may not be adequately captured by simple linear or polynomial models; high-resolution monitoring of reference standards throughout the run is recommended.
- Spectral library RI metadata must be obtained under comparable GC conditions (same column type and temperature program) to be comparable; published RI values from different sources or instruments may introduce systematic bias.

## Evidence

- [other] Apply GC_RI_Calibration to align retention times against reference alkane standards and compute retention indices for each detected peak.: "Apply GC_RI_Calibration to align retention times against reference alkane standards and compute retention indices for each detected peak."
- [other] Extract low-resolution mass spectra from each peak and perform LowResMassSpectralMatch against the PNNLMetV20191015.MSL spectral library, scoring matches by cosine similarity and retention-index proximity.: "perform LowResMassSpectralMatch against the PNNLMetV20191015.MSL spectral library, scoring matches by cosine similarity and retention-index proximity."
- [other] Load raw GC-MS data in NetCDF format using ReadAndiNetCDF, parsing instrument parameters and chromatographic signals.: "Load raw GC-MS data in NetCDF format using ReadAndiNetCDF, parsing instrument parameters and chromatographic signals."
- [readme] Retention Index Calibration: "Retention Index Calibration"
- [readme] ANDI NetCDF for GC-MS (.cdf): "ANDI NetCDF for GC-MS (.cdf)"
