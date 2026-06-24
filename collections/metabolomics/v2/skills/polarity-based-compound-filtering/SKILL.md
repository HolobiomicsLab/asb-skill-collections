---
name: polarity-based-compound-filtering
description: Use when you have a multi-polarity compound target list (e.g., a .xlsx
  file with a polarity or ionization mode column indicating positive or negative ESI
  mode) and you are about to perform targeted peak detection in a single LC–MS acquisition
  mode (e.g., positive-ion mode only).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3370
  tools:
  - TARDIS
  - R
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- Targeted peak integration of LC-MS data using TARDIS
- rmarkdown::html_document
- Quick start for targeted peak integration of LC-MS data using TARDIS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis_cq
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00567
  all_source_dois:
  - 10.1021/acs.analchem.5c00567
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# polarity-based-compound-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter a compound target list to retain only compounds matching a specified ionization polarity (positive or negative) before peak detection in LC–MS data. This step ensures that TARDIS peak integration operates only on chemically relevant m/z and retention time windows, avoiding spurious matches from oppositely charged ions.

## When to use

You have a multi-polarity compound target list (e.g., a .xlsx file with a polarity or ionization mode column indicating positive or negative ESI mode) and you are about to perform targeted peak detection in a single LC–MS acquisition mode (e.g., positive-ion mode only). Filter before calling createTargetList() or peak integration to avoid processing compounds incompatible with the acquired mass spectrometry polarity.

## When NOT to use

- Your LC–MS data were acquired in both positive and negative polarity modes in a single run (e.g., alternating scan events). In this case, retain both polarities or post-process results by polarity rather than filtering the target list.
- Your compound target list is already single-polarity or pre-filtered. Applying this filter again wastes computation and introduces no benefit.
- You are using TARDIS in screening mode to visually inspect target visibility across a wide m/z and RT window; polarity filtering at this stage may hide valid compounds from exploratory review.

## Inputs

- data.frame with columns: compound ID, compound name, theoretical or measured m/z, expected RT (minutes), and ionization mode indicator (e.g., 'positive', 'negative', or regex-matchable pattern)

## Outputs

- TARDIS-compatible target list data.frame (or object) containing only compounds matching the specified polarity, with columns retained for ID, name, m/z, RT, and polarity

## How to apply

Within the TARDIS workflow, polarity filtering is performed inside the createTargetList() function using polarity patterns (pos_pattern and neg_pattern parameters) and a polarity selection argument. Extract the ionization mode column from your target data.frame (e.g., a column containing strings like 'positive' or 'negative'), match it against the specified pattern, and retain only rows where the polarity matches your acquisition mode. The function then outputs a TARDIS-compatible target list containing only the filtered compounds. This avoids the need for manual pre-subsetting and integrates polarity filtering with m/z and retention time column selection in a single step.

## Related tools

- **TARDIS** (Performs polarity filtering via createTargetList() function with pos_pattern, neg_pattern, and polarity parameters; integrates filtering with column selection and retention time correction) — https://github.com/pablovgd/TARDIS
- **R** (Environment in which TARDIS and data.frame manipulation functions execute)

## Examples

```
target_list <- createTargetList(file = 'targets.xlsx', pos_pattern = 'positive', neg_pattern = 'negative', polarity = 'positive', ion_column = 'ionization_mode', columns_of_interest = list(id = 'compound_id', name = 'compound_name', mz = 'mz_measured', rt = 'rt_minutes'))
```

## Evaluation signals

- The output target list contains only compounds whose ionization mode matches the specified polarity (e.g., all 'positive' if pos_polarity is selected); inspect the polarity column or count of rows before and after filtering.
- The number of rows in the filtered target list is ≤ the input; no rows should be duplicated.
- Subsequent peak detection (with screening_mode=TRUE or FALSE) produces EICs and quality metrics (AUC, Max. Int., SNR, peak_cor) only for the retained polarity; visually confirm that chromatograms match the selected polarity (e.g., no anomalously high m/z or RT values from opposite-polarity ions).
- If a compound known to be present in the raw LC–MS data is absent from results, verify it was not accidentally filtered due to a mismatch between the ionization mode string in the target list and the pos_pattern / neg_pattern regex; re-inspect the original target .xlsx.
- The TARDIS results tibble listing average metrics per target in QC runs should not contain targets from both polarities; each row should correspond to a compound retained after filtering.

## Limitations

- Polarity filtering relies on exact or regex pattern matching of the ionization mode column; if values in the source .xlsx file are misspelled, inconsistently capitalized, or formatted differently than expected (e.g., 'Pos' vs. 'positive'), the filter may fail to match and incorrectly exclude or retain compounds.
- TARDIS filters polarity within the tool, so no manual pre-subsetting is required; however, if the ionization mode column is missing or malformed in the input data.frame, the filtering step will produce an error or skip filtering silently.
- When LC–MS data contain overlapping m/z scan windows (e.g., in high-resolution or multiplexed methods), empty spectra are filtered within TARDIS, which can produce a sawtooth profile in EICs even after polarity filtering; this is not a failure of polarity filtering but a consequence of window geometry.
- Polarity filtering does not account for in-source adduct formation (e.g., [M+Na]+ in positive mode); if adducts of the target compound appear in the opposite polarity, they will not be detected after filtering and may go unreported.

## Evidence

- [intro] Polarity filtering performed within TARDIS: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] Target data.frame requires ionization mode column for polarity filtering: "Following columns at least need to be present for each compound: A compound ID, a unique identifier, A compound Name, Theoretical or measured *m/z*, Expected RT (in minutes), A column that indicates"
- [other] createTargetList() accepts polarity pattern and polarity selection parameters: "The createTargetList() function accepts parameters including file path, pos_pattern and neg_pattern for ionization modes, polarity selection, ion_column name, and columns_of_interest list (id, name,"
- [intro] Polarity filtering based on ionization mode column: "the patterns for positive and negative ionization, the polarity of interest, the columnn that contains the ionization mode"
- [intro] Filtering empty spectra occurs within TARDIS as part of data processing: "you will notice that peaks will have a sawtooth profile, because of the filtering of empty spectra within TARDIS"
