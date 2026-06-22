---
name: precursor-ion-isolation-windowing
description: Use when processing SWATH-MS (Sequential Windowed Acquisition of all Theoretical Mass-spectra) raw data files (mzML or vendor format) for untargeted metabolomics, specifically before attempting to deconvolute overlapping MS/MS spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DecoMetDIA
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.9b02655
  title: DecoMetDIA
evidence_spans:
- DecoMetDIA was developed to process SWATH-MS based data for metabolomics.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_decometdia_cq
    doi: 10.1021/acs.analchem.9b02655
    title: DecoMetDIA
  dedup_kept_from: coll_decometdia_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b02655
  all_source_dois:
  - 10.1021/acs.analchem.9b02655
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# precursor-ion-isolation-windowing

## Summary

Grouping co-eluting fragment spectra from SWATH-MS data by precursor m/z and retention time windows to enable downstream spectral deconvolution. This step isolates multiplexed MS/MS spectra into manageable subsets for accurate component spectrum separation.

## When to use

Apply this skill when processing SWATH-MS (Sequential Windowed Acquisition of all Theoretical Mass-spectra) raw data files (mzML or vendor format) for untargeted metabolomics, specifically before attempting to deconvolute overlapping MS/MS spectra. Use it when your acquisition strategy has multiplexed many precursor ions into single isolation windows, resulting in mixed fragment spectra that require separation.

## When NOT to use

- Input is already targeted MS/MS data (single precursor per isolation) rather than multiplexed SWATH acquisition.
- Fragment spectra are already deconvoluted or pre-processed by vendor software; re-windowing may introduce artifacts.
- Data is from untargeted methods other than SWATH-MS (e.g., full-scan DIA without defined precursor windows) where precursor-window metadata may not be available or applicable.

## Inputs

- SWATH-MS raw data files (mzML format or vendor format)
- Instrument acquisition method metadata (precursor m/z window definitions, retention time windows)

## Outputs

- Grouped fragment spectra sets binned by precursor m/z and retention time window
- Intermediate spectral dataset ready for multiplexed spectrum decomposition

## How to apply

Load SWATH-MS raw data into DecoMetDIA and define precursor ion isolation windows based on the instrument's acquisition method (typically 25 Da or instrument-specific widths). Apply retention time windowing to group fragment spectra that co-elute within a defined time window (typically 0.5–2 min depending on chromatographic resolution). This pre-processing step reduces spectral complexity and focuses the subsequent deconvolution algorithm on a coherent set of fragments expected to arise from precursors within that m/z and retention time frame. The rationale is that precursor ions in a narrow m/z window with overlapping retention times are more likely to produce overlapping fragments; grouping them separately ensures the deconvolution algorithm can effectively separate individual component spectra without interference from distant precursors.

## Related tools

- **DecoMetDIA** (R package that implements precursor ion isolation and retention time windowing as a preprocessing step before spectral deconvolution of SWATH-MS data) — https://github.com/ZhuMSLab/DecoMetDIA

## Examples

```
devtools::install_github("ZhuMSLab/DecoMetDIA"); library(DecoMetDIA); # Then apply windowing via DecoMetDIA's preprocessing pipeline with m/z isolation and RT grouping before deconvolution
```

## Evaluation signals

- Verify that fragment spectra within each window have precursor m/z values within ±tolerance (e.g., 25 Da) of the window center.
- Check that retention times of grouped spectra cluster within the defined time window (e.g., all within 0.5–2 min).
- Confirm that the windowed groupings preserve co-eluting ions (similar retention times) while excluding distant precursors, reducing spectral overlap complexity.
- Validate post-deconvolution that component spectra within each window have consistent and interpretable mass differences and intensity distributions.
- Compare deconvolution quality metrics (peak counts, mass accuracy, signal-to-noise) before and after windowing to ensure windowing improves separation without loss of information.

## Limitations

- Windowing parameters (m/z width, retention time width) must match the SWATH-MS instrument configuration; mismatched parameters may either lose precursors or retain too much spectral noise.
- Compounds with very similar retention times but distant m/z values may be incorrectly grouped or separated depending on window size, potentially missing or creating false deconvoluted spectra.
- Retention time resolution depends on chromatographic method; high-resolution separations permit tighter time windows, while low-resolution methods require wider windows and may introduce more spectral mixing.

## Evidence

- [other] Apply precursor ion isolation and retention time windowing to group co-eluting fragment spectra: "Apply precursor ion isolation and retention time windowing to group co-eluting fragment spectra."
- [readme] DecoMetDIA was developed to process SWATH-MS based data for metabolomics: "DecoMetDIA was developed to process SWATH-MS based data for metabolomics."
- [other] Load SWATH-MS raw data files (mzML or vendor format) into DecoMetDIA: "Load SWATH-MS raw data files (mzML or vendor format) into DecoMetDIA."
