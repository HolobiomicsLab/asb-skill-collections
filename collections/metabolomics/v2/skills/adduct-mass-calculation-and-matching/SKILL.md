---
name: adduct-mass-calculation-and-matching
description: Use when when you have a list of target molecules with known molecular
  formulas and need to extract and validate their peaks from centroided mzML files,
  or when assessing whether detected peaks in a mass spectrometry run correspond to
  expected adducts of known metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - mzRAPP
  - enviPat
  - R
  - MSconvert
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing
  (NPP)
- mzRAPP extracts and validates chromatographic peaks for which boundaries are provided
  for all (enviPat predicted) isotopologues
- library(mzRAPP)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrapp_cq
    doi: 10.1093/bioinformatics/btab231/6214530
    title: mzRAPP
  dedup_kept_from: coll_mzrapp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab231/6214530
  all_source_dois:
  - 10.1093/bioinformatics/btab231/6214530
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# adduct-mass-calculation-and-matching

## Summary

Calculate theoretical m/z values for molecular adducts (M+H, M+NH4, M+Na, M+K, etc.) and match them against observed mass spectrometry peaks within specified mass accuracy tolerance. This skill is essential for validating detected peaks in non-targeted LC-HRMS workflows and for generating reliable benchmark datasets with known adduct composition.

## When to use

When you have a list of target molecules with known molecular formulas and need to extract and validate their peaks from centroided mzML files, or when assessing whether detected peaks in a mass spectrometry run correspond to expected adducts of known metabolites. Specifically apply this when generating benchmark datasets to validate non-targeted data pre-processing tools (XCMS, MZmine, MS-DIAL, etc.).

## When NOT to use

- Input data are not centroided (peak-picked) — first convert via MSconvert or equivalent tool.
- Molecular formula contains trailing zeros (e.g., 'C12H8N0S2') — formulas must be cleaned before submission.
- You lack retention time boundaries (user.rtmin/user.rtmax) for target compounds — this skill requires prior manual curation or external RT database to set boundaries.

## Inputs

- Centroided mzML files (LC-HRMS data)
- Target molecule file (CSV with columns: molecule, SumForm_c, main_adduct, user.rtmin, user.rtmax, and optional adduct_c)
- Instrument resolution specification (e.g., 'OrbitrapXL,Velos,VelosPro_R60000@400' or custom CSV with R and m/z columns)
- List of adducts to match (e.g., M+H, M+NH4, M+Na, M+K)

## Outputs

- Benchmark dataset (CSV) with detected peaks linked to target molecules, including validated adducts and isotopologues
- Peak annotations with calculated m/z, isotopologue ratio metrics, and peak shape quality scores
- Summary statistics: number of molecules detected, number of features (adducts + isotopologues), total peak count

## How to apply

Use enviPat to predict all isotopologues for each target molecule under the specified instrument resolution (e.g., OrbitrapXL/Velos at R=60000 @ 400 m/z). For each adduct specified (main_adduct and additional adducts), calculate the theoretical m/z and isotopic pattern. Extract ion chromatograms (EICs) centered on these m/z values within the mass accuracy window (e.g., ±6 ppm or ±5 ppm as specified). Match observed peaks to theoretical m/z by requiring: (1) detection of the most abundant isotopologue AND at least one additional isotopologue, (2) peak shape correlation ≥0.85 with the most abundant isotopologue, and (3) isotopologue abundance ratios within 30% of predicted values. Reject adducts if fewer than two isotopologues are detected. Apply this iteratively across all target molecules and sample files.

## Related tools

- **mzRAPP** (Orchestrates adduct mass calculation, isotopologue prediction, EIC extraction, and peak matching via the 'Generate Benchmark' tab; handles multi-adduct validation and isotope filtering) — https://github.com/YasinEl/mzRAPP
- **enviPat** (Predicts isotopologue patterns and calculates theoretical m/z values for all adducts under instrument-specific mass resolution; provides isotope abundance ratios for validation)
- **R** (Runtime environment for calling mzRAPP functions programmatically (e.g., library(mzRAPP); callmzRAPP()))
- **MSconvert** (Converts vendor mass spectrometry formats to centroided mzML for input to adduct matching pipeline) — http://proteowizard.sourceforge.net/tools.shtml

## Examples

```
library(mzRAPP); callmzRAPP() # Then navigate to Generate Benchmark tab, select 30 _POS.mzML files, sample-group CSV, target CSV; set instrument to OrbitrapXL,Velos,VelosPro_R60000@400; select adducts M+NH4, M+Na, M+K; set mass accuracy 5 ppm, mass precision 6 ppm; execute and export benchmark CSV.
```

## Evaluation signals

- All main_adducts for target molecules are detected; if a main_adduct is not found, no secondary adducts should be accepted for that molecule.
- Isotopologue abundance ratios fall within ±30% of enviPat predictions; deviations beyond this threshold indicate degraded data quality or mismatched peaks.
- Peak shape correlation coefficient ≥0.85 between low-abundance and most-abundant isotopologue, indicating coherent chromatographic behavior.
- For the MTBLS267 benchmark (30 _POS.mzML files, OrbitrapXL/Velos/VelosPro, M+NH4/M+Na/M+K adducts), expect ~47 molecules, ~157 features, ~2870 total peaks after filtering.
- Number of detected peaks aligns with expectations from prior processing runs (e.g., 83–99% detection rate post-alignment, depending on tool used).

## Limitations

- Adducts will only be added to the benchmark if at least two isotopologues of the respective adduct can be detected; rare or low-abundance adducts may be missed.
- Retention time boundaries (user.rtmin/user.rtmax) must be manually curated or provided externally; mzRAPP can refine them to 5% peak height intersections, but cannot discover them de novo.
- Mass resolution specification must match the actual instrument used; incorrect resolution will cause systematic mismatches between theoretical and observed m/z.
- Isotopologue filtering removes peaks with correlation <0.85 or ratio bias >30%; this may exclude valid low-abundance isotopologues in noisy samples.
- Centroiding is required; profile-mode data will fail or produce unreliable results.

## Evidence

- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files"
- [readme] Isotopologue peaks with area/height >30% off predicted or Pearson correlation <0.85 are removed: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed"
- [readme] Only isotopologues where most abundant and at least one additional isotopologue are found are kept: "Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered for the final benchmark"
- [readme] If main_adduct not detected, other adducts are not accepted; adducts must satisfy isotope criteria: "If the main_adduct is not detected also other adducts wont be accepted. Therefore it makes sense to select the most trusted adduct (generally M+H or M-H) as main adduct"
- [methods] MTBLS267 benchmark generation produced 47 molecules with 157 features and 2870 peaks: "Processing all 30 mzML files generates a benchmark containing 47 different molecules with 157 different features including all adducts and isotopologues, resulting in 2870 peaks in total"
- [methods] Mass accuracy and precision parameters are specified in ppm: "Configure extraction parameters: lowest isotopologue 0.05, minimum 6 scans per peak, 6 ppm mass precision, 5 ppm mass accuracy"
- [readme] Target file must include molecular composition, main adduct, and retention time boundaries: "molecule: names of target molecules (should be unique identifiers) ... SumForm_c: Molecular composition of the neutral molecule ... main_adduct: One main adduct has to be defined for each molecule"
- [readme] Adducts are only added if at least two isotopologues are detected: "adducts will only be added if at least two isotoplogues of the respective adduct can be detected"
