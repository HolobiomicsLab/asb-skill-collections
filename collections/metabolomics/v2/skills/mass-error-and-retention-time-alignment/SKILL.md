---
name: mass-error-and-retention-time-alignment
description: Use when when processing low- or high-resolution mass spectrometry data
  (mzML profile or centroided format) for isotopologue quantification and you need
  to match detected peaks to a targeted formulaTable of compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - R
  - isoSCAN
  - mzR
  - enviPat
  - Proteowizard MSconvert
  techniques:
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c02998
  title: isoSCAN
evidence_spans:
- To Install from R console
- 'To Install from R console: ```` install.packages("devtools", dependencies=TRUE)
  library(devtools)'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c02998
  all_source_dois:
  - 10.1021/acs.analchem.0c02998
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-error-and-retention-time-alignment

## Summary

Align detected isotopologue peaks to targeted compounds by constraining mass accuracy (m/z error tolerance) and retention time windows during automated quantification. This skill ensures that peaks corresponding to the correct isotopologues are selected rather than confounding ions or off-target compounds.

## When to use

When processing low- or high-resolution mass spectrometry data (mzML profile or centroided format) for isotopologue quantification and you need to match detected peaks to a targeted formulaTable of compounds. Use this skill whenever the raw data contains multiple potential peaks near the expected m/z and retention time of your compounds and you must disambiguate the correct isotopologue signal from background noise or co-eluting ions.

## When NOT to use

- Input mzML files are already centroided and you are processing low-resolution data (profile format is essential for low-resolution peak quantification).
- formulaTable lacks validated RT values or RT drift across the batch exceeds the specified RTwin by a large margin (alignment will fail or select wrong peaks).
- Mass error tolerance is set wider than the spacing between candidate m/z peaks of different compounds (risk of cross-contamination between isotopologues or related compounds).

## Inputs

- formulaTable data frame (R) with columns: CompoundName, mz (monoisotopic m/z), RT (retention time in seconds), Formula, NumAtoms
- mzML files in profile format (low-resolution) or centroided format (high-resolution)
- mass error tolerance parameter (mzerror in Da or maxppm)
- retention time window parameter (RTwin in seconds)
- signal-to-noise ratio threshold (SNR)
- peak width bounds (minwidth, maxwidth in scans)

## Outputs

- Per-compound isotopologue area values (when peak shape permits quantification)
- Per-compound isotopologue maxo (maximum intensity) values
- Aligned peak table indexed by CompoundName and isotopologue identity

## How to apply

During autoQ processing, specify two complementary tolerance parameters: (1) a mass error tolerance (mzerror in Da or maxppm in parts-per-million) to define the acceptable m/z window around the monoisotopic ion listed in formulaTable, and (2) a retention time window (RTwin in seconds) to define the expected elution time range. These parameters work together to constrain the peak-finding algorithm to a narrow region of mass–time space, reducing false positives. The choice of tolerance depends on instrument resolution: low-resolution data typically uses looser tolerances (e.g., mzerror=0.1 Da), while high-resolution data can support tighter windows. Retention time tolerance should reflect the chromatographic peak width and any expected RT drift across the sample batch. The algorithm then extracts area and maxo (maximum intensity) values only for peaks falling within both windows, rejecting out-of-window candidates.

## Related tools

- **isoSCAN** (R package that wraps autoQ function to perform mass–time alignment and isotopologue quantification on mzML files) — https://github.com/jcapelladesto/isoSCAN
- **mzR** (R package used by isoSCAN to read and parse mzML format mass spectrometry files)
- **enviPat** (R package used by isoSCAN to calculate isotopologue patterns and masses for high-resolution data disambiguation)
- **Proteowizard MSconvert** (External tool to convert vendor raw MS formats into mzML; controls profile/centroid format choice)

## Examples

```
autoQ(formulaTable=quadrupole_ft, mzMLfiles=list.files(pattern='.mzML'), minscans=6, SNR=3, mzerror=0.1, RTwin=5, maxwidth=4, minwidth=1)
```

## Evaluation signals

- Area and maxo values are returned for all isotopologues of target compounds listed in formulaTable (no missing compounds unless genuinely absent from the sample).
- Extracted peaks fall within the specified mzerror (or maxppm) and RTwin bounds; spot-check 5–10 peaks by overlay against raw chromatogram and spectrum.
- No cross-contamination: peaks from different compounds (with distinct m/z or RT) are not collapsed into a single quantification.
- Reproducibility: rerunning autoQ on the same files with identical parameters yields identical area/maxo tables.
- Quality control plots (rawPlot, meanRawPlot) show unimodal, symmetric peak shapes without saturation or movement artifacts for quantified isotopologues.

## Limitations

- Requires a high-quality, validated formulaTable with accurate RT values; if RT values are missing or drift significantly across the batch, alignment fails or selects incorrect peaks.
- Low-resolution data must be in profile (not centroided) format; centroided data cannot be reliably quantified because peak area cannot be reconstructed.
- For high-resolution data, Formula column must match the derivatized formula (e.g., with trimethylsilyl groups for GC-MS), otherwise m/z mismatch causes alignment failure.
- Co-eluting isotopologues or isobars within the mass error window cannot be resolved; the algorithm will sum their signals or misassign peaks.
- Peak width parameters (minwidth, maxwidth) must be appropriate for the chromatographic method; mismatched values may reject valid peaks or accept noise.

## Evidence

- [intro] formulaTable must contain columns: CompoundName, mz, RT, Formula, NumAtoms: "_formulaTable_ __must__ contain the following column names in no specific order: * __CompoundName__ * __mz__ * __RT__ * __Formula__ * __NumAtoms__"
- [intro] autoQ uses mass error (mzerror or maxppm) and retention time window (RTwin) as alignment parameters: "autoQ function with the formulaTable, specifying parameters: minscans, SNR (signal-to-noise ratio threshold), mzerror or maxppm (mass error tolerance), RTwin (retention time window in seconds), and"
- [intro] Low-resolution data requires profile format for peak quantification: "In the case of Low-resolution. Transform the data mantaining __profile format__. This is essential for peak quantification."
- [intro] High-resolution data requires centroiding: "In the case of High-resolution, __please use centroiding__ (e.g. _peakPicking= True_ in MSconvert)"
- [other] Example parameters for low-resolution Quadrupole data processing: "minscans=6, SNR=3, mzerror=0.1, RTwin=5, maxwidth=4, minwidth=1 yields both area and maxo values for isotopologues of compounds like ILeu"
