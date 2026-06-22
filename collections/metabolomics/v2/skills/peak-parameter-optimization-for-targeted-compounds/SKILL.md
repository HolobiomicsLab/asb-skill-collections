---
name: peak-parameter-optimization-for-targeted-compounds
description: Use when you have centroided high-resolution Orbitrap or GC-CI-MS mzML files and a formulaTable of target compounds with known m/z, retention time, and molecular formula, and you need to extract isotopologue abundances and quantification metrics (area, maxo intensity, ppm error) for each labeled.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - R
  - isoSCAN
  - mzR
  - enviPat
  - Proteowizard MSconvert
derived_from:
- doi: 10.1021/acs.analchem.0c02998
  title: isoSCAN
evidence_spans:
- To Install from R console
- 'To Install from R console: ```` install.packages("devtools", dependencies=TRUE) library(devtools)'
- install_github("jcapelladesto/isoSCAN") library(isoSCAN)
- install_github("jcapelladesto/isoSCAN")
- isoSCAN uses `mzR` package in order to read MS files
- isoSCAN makes use of __enviPat__ package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isoscan_cq
    doi: 10.1021/acs.analchem.0c02998
    title: isoSCAN
  dedup_kept_from: coll_isoscan_cq
schema_version: 0.2.0
---

# peak-parameter-optimization-for-targeted-compounds

## Summary

Optimize mass spectrometry peak detection parameters (retention time window, signal-to-noise ratio, peak width bounds, mass error tolerance, and minimum scan count) to reliably extract isotopologue quantification data from centroided high-resolution mzML files. This skill ensures reproducible extraction of abundance, ppm mass error, and peak area values for stable isotope labeling experiments.

## When to use

You have centroided high-resolution Orbitrap or GC-CI-MS mzML files and a formulaTable of target compounds with known m/z, retention time, and molecular formula, and you need to extract isotopologue abundances and quantification metrics (area, maxo intensity, ppm error) for each labeled form (M+0, M+1, M+2, etc.). Use this skill when peak detection is failing to capture expected isotopic forms or when you need to balance sensitivity (signal-to-noise ratio) against specificity (mass error tolerance and peak width constraints).

## When NOT to use

- Input files are in profile format or uncenroided; use profile format for low-resolution data instead, and apply different peak-width constraints.
- formulaTable is missing required columns (CompoundName, mz, RT, Formula, NumAtoms) or Formula does not match the derivatized molecular formula used in high-resolution analysis.
- You have already extracted and validated a quantification table and only need to visualize or post-process the results — use metBarPlot or downstream statistical functions instead.

## Inputs

- Centroided high-resolution mzML files (produced by Proteowizard MSconvert with peakPicking=True)
- formulaTable data frame with columns: CompoundName, mz (monoisotopic m/z), RT (retention time in seconds), Formula (must match derivatized formula for high-resolution), NumAtoms
- enviPat isotopes object for isotope pattern calculation
- Label atom specification (e.g., '13C' for 13C labeling experiments)

## Outputs

- Quantification table with columns: CompoundName, m/z, abundance, Isotopologue designation (M+0, M+1, M+2, etc.), ppm mass error, maxo (maximum intensity), area (peak area) for each isotopic form per sample condition
- Peak detection quality-control plots (rawPlot, meanRawPlot) showing peak shape, intensity, and retention time stability across replicates

## How to apply

Define or tune six interdependent parameters passed to the autoQ function: (1) RTwin (retention time window in seconds around the expected RT) — start with ±10–30 s and narrow if off-target peaks appear; (2) SNR (signal-to-noise ratio threshold) — set to 3–5 to exclude noise; (3) mzerror or maxppm (mass error in ppm) — use 5–10 ppm for high-resolution Orbitrap data to differentiate isotopologues from off-target ions; (4) minwidth and maxwidth (peak width bounds in scans) — constrain based on your chromatographic resolution and MS acquisition rate; (5) minscans (minimum number of scans to define a peak) — typically 3–5 to avoid single-scan noise artifacts. Test parameters on a small subset of files, then validate using rawPlot and meanRawPlot quality-control functions to identify moving peaks, noisy spots, or saturated peaks before running the full batch.

## Related tools

- **isoSCAN** (R package that implements the autoQ function to process centroided mzML files and extract isotopologue abundances and quantification metrics with optimized peak parameters) — https://github.com/jcapelladesto/isoSCAN
- **mzR** (Reads mzML/mzXML files into R for downstream peak detection and quantification by autoQ)
- **enviPat** (Calculates isotope patterns and abundances to aid differentiation of targeted isotopologues from off-target ions at high resolution)
- **Proteowizard MSconvert** (Converts raw vendor MS data into centroided mzML format (with peakPicking=True) required for high-resolution peak parameter optimization)

## Examples

```
autoQ(files=mzML_paths, formulaTable=formula_df, labelatom='13C', maxppm=5, RTwin=20, SNR=3, minscans=3, minwidth=5, maxwidth=25)
```

## Evaluation signals

- The resulting quantification table contains non-null values for all five metrics (abundance, ppm, maxo, area, Isotopologue designation) for each expected labeled isotopomer (M+0, M+1, M+2) across all sample conditions.
- Mass error (ppm column) for each isotopologue falls within the specified maxppm tolerance (e.g., all values < 5 ppm for high-resolution Orbitrap), confirming isotopologues were correctly differentiated from off-target ions.
- rawPlot and meanRawPlot quality-control plots show stable peak shapes and retention times across replicates, with no evidence of moving peaks, saturation, or excessive noise.
- Peak area and maxo intensity values are reproducible across replicate sample conditions (e.g., coefficient of variation < 20% within a condition), indicating robust parameter choice.
- No expected labeled isotopologues are missing from the output table; if M+1 or M+2 are absent despite known labeling, RTwin or SNR parameters may need adjustment.

## Limitations

- High-resolution data requires centroiding and derivatized Formula specification in formulaTable; low-resolution profile-format data requires different parameter tuning and peak-width constraints.
- Parameter optimization is data- and instrument-dependent; settings tuned on Orbitrap data may not transfer directly to other high-resolution instruments or GC-CI-MS platforms without validation.
- Peak parameter tuning is empirical and time-consuming; there is no algorithmic method described to automatically select optimal values — manual iteration with quality-control plots is required.
- Saturated peaks, moving peaks, and noisy background cannot be automatically corrected; these issues must be identified via rawPlot/meanRawPlot and addressed by adjusting SNR, RTwin, or minwidth/maxwidth, or by re-acquiring data with different instrument settings.

## Evidence

- [intro] Before starting with file processing, we need to load the _targeted compounds_ as a _formulaTable_ data frame. This can be done either with `read.table` or `read.csv` functions.: "Before starting with file processing, we need to load the _targeted compounds_ as a _formulaTable_ data frame. This can be done either with `read.table` or `read.csv` functions."
- [intro] _formulaTable_ __must__ contain the following column names in no specific order: * __CompoundName__ * __mz__ * __RT__ * __Formula__ * __NumAtoms__: "_formulaTable_ __must__ contain the following column names in no specific order: * __CompoundName__ * __mz__ * __RT__ * __Formula__ * __NumAtoms__"
- [intro] In the case of High-resolution, __please use centroiding__ (e.g. _peakPicking= True_ in MSconvert): "In the case of High-resolution, __please use centroiding__ (e.g. _peakPicking= True_ in MSconvert)"
- [intro] This parameters refer to peak width and number of scans recorded, together with signal-to-noise ratio and mass error.: "This parameters refer to peak width and number of scans recorded, together with signal-to-noise ratio and mass error."
- [intro] autoQ uses parameters: minscans, SNR (signal-to-noise ratio), mzerror or maxppm (mass error), RTwin (retention time window), maxwidth and minwidth (peak width parameters): "autoQ uses parameters: minscans, SNR (signal-to-noise ratio), mzerror or maxppm (mass error), RTwin (retention time window), maxwidth and minwidth (peak width parameters)"
- [intro] Now we can call `autoQ` function that will process the files and look for the isotopologues for each compound found in the `formulaTable`.: "Now we can call `autoQ` function that will process the files and look for the isotopologues for each compound found in the `formulaTable`."
- [intro] `rawPlot` and `meanRawPlot` functions should be used for quality control purposes. They are useful to check for moving peaks, noisy spots or saturated peaks.: "`rawPlot` and `meanRawPlot` functions should be used for quality control purposes. They are useful to check for moving peaks, noisy spots or saturated peaks."
- [other] The autoQ function returns for high-resolution Orbitrap data a table with columns for CompoundName, m.z, abundance, Isotopologue designation (M+0, M+1, M+2), ppm mass error, and paired maxo and area values for each isotopic form per sample condition.: "The autoQ function returns for high-resolution Orbitrap data a table with columns for CompoundName, m.z, abundance, Isotopologue designation (M+0, M+1, M+2), ppm mass error, and paired maxo and area"
