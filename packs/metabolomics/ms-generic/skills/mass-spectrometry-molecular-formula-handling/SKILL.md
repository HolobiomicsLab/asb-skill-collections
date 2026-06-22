---
name: mass-spectrometry-molecular-formula-handling
description: 'Use when you have raw or processed FT-ICR MS spectra with detected peaks (m/z values) and need to: (1) assign elemental compositions to each peak, (2) filter assignments by mass error tolerance and isotopic presence, or (3) prepare a peak table with molecular formula annotations for chemodiversity.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MetaboDirect
  - Formularity
  - CoreMS
  - KEGG database
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-molecular-formula-handling

## Summary

Assign molecular formulas to detected m/z peaks in high-resolution FT-ICR MS data and filter results by mass accuracy and isotopic consistency. This is a foundational preprocessing step that converts raw peak lists into chemically interpretable, annotated peak tables suitable for downstream analysis.

## When to use

You have raw or processed FT-ICR MS spectra with detected peaks (m/z values) and need to: (1) assign elemental compositions to each peak, (2) filter assignments by mass error tolerance and isotopic presence, or (3) prepare a peak table with molecular formula annotations for chemodiversity analysis, transformation network generation, or multivariate statistics. This skill is essential before any biochemical interpretation of the data.

## When NOT to use

- Input already contains pre-assigned, validated molecular formulas from a peer-reviewed database (e.g., HMDB); use direct lookup instead.
- Data is low-resolution MS (e.g., TOF or Orbitrap without sub-ppm accuracy); mass error tolerance cannot reliably differentiate isomers.
- Peak list includes already-normalized relative abundances without raw intensity values; isotopic filtering and compound class assignment may be unreliable.
- Samples are from a biological matrix where signal suppression or ion-pairing effects are uncharacterized; formula assignment error may be non-random.

## Inputs

- CSV file with detected m/z values and peak abundances per sample
- Raw FT-ICR MS spectra (optional; formula assignment may require full spectral data)
- User-defined filtering parameters: mass error threshold (ppm), minimum sample presence count

## Outputs

- Peak abundance matrix with assigned molecular formulas and compound classes
- Filtered peak list (CSV) containing m/z, molecular formula, compound class, and normalized abundance per sample
- Filtering summary report (number of peaks retained/removed at each filter step)
- Elemental composition table (H, C, N, O, S, P counts per peak)

## How to apply

Load the detected peak list (CSV with m/z values) into a formula assignment tool (e.g., Formularity, CoreMS, or MetaboDirect's integrated assignment module). Apply mass error filtering at ≤0.5 ppm against theoretical formula masses to retain only high-confidence assignments. Remove isotopic peaks (e.g., 13C peaks) to avoid redundant counting. Filter peaks based on a user-defined minimum presence threshold (number of samples in which the peak must appear) to exclude noise. Classify each formula-assigned peak into a molecular compound class (e.g., lipid, carbohydrate, aromatic, aliphatic) based on elemental composition ratios (H/C, O/C, N/C). Output a normalized, filtered peak abundance matrix (rows = peaks with formula and compound class; columns = samples) suitable for downstream analysis.

## Related tools

- **MetaboDirect** (Integrated pipeline for molecular formula assignment, filtering, and output of normalized peak tables with compound class annotations) — https://github.com/Coayala/MetaboDirect
- **Formularity** (Open-source software for molecular formula assignment to high-resolution MS peaks)
- **CoreMS** (Comprehensive software framework providing formula assignment and spectral processing for FT-ICR MS data)
- **KEGG database** (Optional reference database for validation and mapping of assigned formulas to known metabolites)

## Examples

```
metabodirect --input peaks_abundance.csv --formula-error 0.5 --min-presence 2 --output-dir ./results
```

## Evaluation signals

- All assigned formulas have mass error ≤0.5 ppm against theoretical m/z values; verify by calculating |theoretical m/z − observed m/z| / theoretical m/z × 1e6.
- Isotopic peaks (13C, 18O, 34S) are identified and removed; check that 1.003 Da mass shifts and expected intensity ratios are absent in filtered peak list.
- Elemental composition ratios (H/C, O/C, N/C) fall within biologically plausible ranges (e.g., H/C 0.3–2.5, O/C 0–1.5 for natural organic matter); plot Van Krevelen diagram to verify distribution.
- Peak retention rate after filtering aligns with article benchmarks: e.g., bacterium-phage model system retained ~495 assigned formulas from ~1025 detected peaks (~48%).
- Output CSV contains no missing values in formula or compound class columns; row count matches expected sample size and presence threshold.

## Limitations

- Mass error filtering at 0.5 ppm assumes instrument calibration is stable and accurately mass-calibrated; drift or poor calibration will increase false-negative formula assignments.
- Formula assignment is non-unique at high m/z; multiple distinct molecular formulas may match the same observed m/z within error tolerance. Rank by chemical likelihood (e.g., nitrogen rule, hydrogen deficiency index) but acknowledge ambiguity.
- Isotopic filtering assumes natural isotope abundances; enriched samples (e.g., 13C-labeled, 15N-labeled) will be incorrectly removed as noise.
- Signal suppression and ion-pairing in direct injection (DI) MS can produce non-stoichiometric peak intensities and false formula assignments; the article notes DI MS 'drawbacks include … signal suppression or enhancement that can confound downstream data analysis'.
- Compound class assignment is coarse and based on bulk H/C, O/C ratios; isomers and structurally distinct molecules with identical elemental composition cannot be resolved.

## Evidence

- [intro] MetaboDirect pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique.: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique"
- [methods] Peaks are filtered by m/z values, isotopic presence, formula assignment error, and sample presence count; compound classes are then determined.: "detected peaks are filtered by their m/z values, isotopic presence (13C peaks), error in formula assignment (0.5 ppm), and based on the number of samples that they are present in (threshold"
- [intro] Signal processing and molecular formula assignment steps produce large data matrices with elemental composition and measured abundance of peaks in each sample.: "Signal processing and molecular formula assignment steps will ultimately produce large data matrices containing the elemental composition and measured abundance of the peaks present in each sample"
- [results] Bacterium-phage dataset example: average of 1025 peaks detected, average of 495 peaks assigned molecular formula (~48% retention).: "The data set had an average of 1025 peaks detected across the whole data set (n = 36 samples) and an average of 495 peaks that got assigned a molecular formula"
- [intro] Direct injection MS drawbacks include inability to separate isomers, lack of fine resolving power, and signal suppression that can confound downstream analysis.: "drawbacks are its inability to separate chemical isomers, lack of fine resolving power, and most importantly signal suppression or enhancement that can confound downstream data analysis"
- [methods] MetaboDirect does not provide raw spectra data preprocessing; it assumes molecular formula assignment has been completed prior to input.: "MetaboDirect does not provide raw spectra data preprocessing"
