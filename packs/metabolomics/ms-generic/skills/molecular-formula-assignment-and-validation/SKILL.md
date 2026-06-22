---
name: molecular-formula-assignment-and-validation
description: Use when you have a calibrated FT-ICR transient (ESI_NEG or similar ionization mode) and need to annotate each detected m/z peak with its most likely elemental composition.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  - matplotlib
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Molecular Formula Assignment and Validation

## Summary

This skill applies CoreMS SearchMolecularFormulas with elemental constraints (CHO) to assign molecular formulas to calibrated FT-ICR mass spectra, then validates assignments through mass error metrics and score distributions. It is essential for annotating natural organic matter and complex mixtures where multiple formula candidates exist per m/z.

## When to use

Apply this skill when you have a calibrated FT-ICR transient (ESI_NEG or similar ionization mode) and need to annotate each detected m/z peak with its most likely elemental composition. Use it when you want to compare assignment behavior under different search strategies (first-hit vs. all-hits) or when you need quantified mass error and formula score metrics for downstream filtering or reporting.

## When NOT to use

- Input mass spectrum has not been calibrated or has unresolved mass error > 5 ppm (assignment confidence depends on prior calibration quality).
- Peak intensity or signal-to-noise is too low to distinguish true peaks from noise after threshold filtering.
- Sample contains only known, simple molecules where a priori formula knowledge or vendor libraries are more appropriate than formula search.

## Inputs

- Calibrated FT-ICR mass spectrum (CoreMS Spectrum object post-MzDomainCalibration)
- Reference file (SRFA.ref or equivalent) for calibration verification
- Elemental constraint definition (e.g., CHO, CHON, CHOS)

## Outputs

- Assigned molecular formula table (CSV) with m/z, calibrated m/z, calculated m/z, molecular formula, mass error (ppm), and formula score
- Assignment count summary (first-hit vs. all-hits comparison)
- Formula score distribution statistics (mean, median, std, min, max) per assignment mode

## How to apply

Load the calibrated mass spectrum (after Hanning apodization, zero-fill, noise thresholding, and MzDomainCalibration against a reference file such as SRFA.ref) into CoreMS. Execute SearchMolecularFormulas with elemental constraints limited to C, H, O atoms and configure the first_hit parameter (True for single best match per peak, False for all candidates). Extract assignment counts, mass error (ppm), and formula score statistics from the output. Tabulate and compare assignment distributions across parameter modes to judge whether stricter (first-hit=True) or permissive (first-hit=False) assignment is appropriate for your sample composition and downstream analysis goals.

## Related tools

- **CoreMS** (Provides SearchMolecularFormulas class, MzDomainCalibration, and Spectrum data structure for formula assignment and metric calculation) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Tabulates and exports assignment results and statistics to CSV and comparison summaries)
- **numpy** (Computes distribution statistics (mean, median, std) for formula scores and mass errors)
- **Docker** (Containerizes CoreMS environment to ensure reproducible formula assignment workflow)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; spectrum.SearchMolecularFormulas(first_hit=False); results_df = spectrum.to_dataframe(); results_df.to_csv('molecular_formulas.csv')
```

## Evaluation signals

- All detected peaks above noise threshold receive at least one formula assignment (assignment coverage); no unassigned peaks in output table.
- Mass error (ppm) for assigned formulas falls within expected calibration tolerance (typically ≤ 1–2 ppm for FT-ICR after reference calibration).
- Comparison of first_hit=True vs. first_hit=False assignment counts shows expected behavior: first_hit produces fewer or equal assignments per peak, while all_hits produces multiple candidates per peak; score distribution is consistent with formula diversity in sample.
- Export to CSV completes without truncation and retains all numeric precision for mass error and score metrics; metadata (ionization mode, elemental constraints) is preserved as JSON.
- Formula assignments are chemically plausible for the sample type (e.g., ESI_NEG_SRFA should yield highly oxidized CHO formulas consistent with natural organic matter).

## Limitations

- SearchMolecularFormulas performance depends critically on prior calibration quality; uncalibrated or poorly calibrated spectra will produce high mass errors and ambiguous or spurious formula assignments.
- Elemental constraint specification (e.g., CHO vs. CHON) directly controls the search space; overly permissive constraints increase assignment candidates and ambiguity, while overly restrictive constraints may exclude valid formulas.
- First-hit mode may miss valid alternative formulas if the scoring function does not rank them correctly; all-hits mode can produce hundreds of candidates per peak for complex samples, requiring downstream filtering by mass error or chemical plausibility.
- CoreMS relies on a precomputed or dynamically generated molecular formula database (SQLite or PostgreSQL); database generation time and memory usage scale with search space size.
- The skill does not account for isotope patterns, in-source fragmentation, or isobaric interferences; use isotope and charge-state filtering in prior or subsequent steps if needed.

## Evidence

- [other] Apply Hanning apodization with one zero-fill to the time-domain spectrum. 3. Apply noise thresholding to remove low-intensity peaks. 4. Perform mass-domain calibration using MzDomainCalibration against SRFA.ref reference data. 5. Execute SearchMolecularFormulas with elemental constraints limited to C, H, O atoms.: "Execute SearchMolecularFormulas with elemental constraints limited to C, H, O atoms. 6. Export assigned molecular formulas with calculated mass error and formula score metrics to CSV format."
- [other] SearchMolecularFormulas can be run with first_hit parameter set to True or False, enabling comparison of assignment behavior under different prioritization modes.: "SearchMolecularFormulas can be run with first_hit parameter set to True or False, enabling comparison of assignment behavior under different prioritization modes."
- [other] Extract and tabulate assignment counts and score distribution statistics (mean, median, std, min, max) for each mode.: "Extract and tabulate assignment counts and score distribution statistics (mean, median, std, min, max) for each mode."
- [other] The pipeline executes complete molecular formula assignment by applying Hanning apodization with zero-fill, noise thresholding, MzDomainCalibration against SRFA.ref reference data, and SearchMolecularFormulas with CHO constraints, producing assigned peaks with mass error and abundance metrics exportable to CSV.: "producing assigned peaks with mass error and abundance metrics exportable to CSV."
- [readme] modern molecular formulae assignment algorithms: "modern molecular formulae assignment algorithms"
