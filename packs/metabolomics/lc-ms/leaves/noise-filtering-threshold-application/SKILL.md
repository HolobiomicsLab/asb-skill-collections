---
name: noise-filtering-threshold-application
description: Use when when you have raw or centroid-mode LC-MS All-ion fragmentation (AIF) spectra and need to generate or match against ion fragment databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- To install this package, start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03032
  all_source_dois:
  - 10.1021/acs.analchem.1c03032
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# noise-filtering-threshold-application

## Summary

Apply intensity-based noise thresholds to LC-MS/MS spectra to remove low-intensity signals and retain only biologically or analytically relevant fragment peaks. This preprocessing step is essential before library entry generation or metabolite annotation to improve signal-to-noise ratio and reduce false positive peak matches.

## When to use

When you have raw or centroid-mode LC-MS All-ion fragmentation (AIF) spectra and need to generate or match against ion fragment databases. Apply this skill if your peak list contains low-intensity noise that would inflate false-positive annotations or if you are constructing a metabolite library entry and must distinguish marker peaks from instrumental artifacts.

## When NOT to use

- Input is already a high-confidence feature table or a consensus spectrum that has been pre-filtered by the instrument vendor or a prior processing pipeline (e.g., xcms output). Re-filtering may remove genuine low-abundance fragments.
- Your analysis requires detection of low-intensity metabolite markers or biomarkers where signal is inherently weak; aggressive noise filtering may discard clinically relevant peaks.
- You are annotating spectra from targeted MS/MS methods with high S/N (e.g., selected-reaction monitoring, SRM) where noise is already negligible and thresholds should be much lower than defaults.

## Inputs

- Raw LC-MS/MS spectrum in centroid mode (mzML, NetCDF, or MassBank record format)
- Peak list with m/z and intensity values
- Noise threshold parameter (intensity units; default 0.005)
- Marker peak threshold parameter (intensity units; default 0.1)

## Outputs

- Filtered peak list containing only peaks above noise and marker thresholds
- Annotated spectrum with retained peaks ranked by intensity and occurrence score
- CSV-formatted library entry with mass, intensity, and match scores (when used with genFragEntry)

## How to apply

Load the experimental MS/MS spectrum (e.g. from MassBank or raw instrument output in centroid mode). Apply a two-stage filtering pipeline: first, remove all peaks below the noise intensity threshold (default: 0.005 relative intensity units) to suppress baseline artifacts and instrumental noise; second, apply a marker peak threshold (default: 0.1 relative intensity units) to identify significant fragment ions that represent true fragmentation products. The rationale is that peaks below the noise threshold are indistinguishable from background, while peaks between noise and marker thresholds represent minor fragments that may introduce spurious matches. Execute these filters before passing the cleaned spectrum to annotation or library-building functions (e.g. genFragEntry with mpeaksScore=0.9 and mzTol=0.01). Verify that the retained peak count and intensity distribution are consistent with expected fragmentation patterns for your metabolite class.

## Related tools

- **MetaboAnnotatoR** (Applies noise-filtering thresholds and executes genFragEntry to generate library entries from filtered spectra; accepts noise=0.005 and mpeaksThres=0.1 parameters.) — https://github.com/gggraca/MetaboAnnotatoR
- **xcms** (Upstream peak-picking and centroid-mode data transformation; produces peak-picked data that is then passed to noise filtering before annotation.)
- **RamClustR** (Co-processes LC-MS AIF chromatograms alongside xcms to generate pseudo-MS/MS spectra that undergo noise filtering prior to annotation.)

## Examples

```
genFragEntry(spectrum_data, metabolite_name='D-Pantothenic Acid', adduct='[M+H]+', mz_adduct=220.1175, noise=0.005, mpeaksThres=0.1, mpeaksScore=0.9, mzTol=0.01, output_file='pantothenic_acid_entry.csv')
```

## Evaluation signals

- Verify that all retained peaks have intensity ≥ noise threshold (0.005) and marker threshold (0.1) in the filtered spectrum.
- Check that the number of retained peaks is realistic for the metabolite class (e.g., D-Pantothenic Acid typically yields 5–20 major fragments); anomalously small or large counts may indicate threshold misconfiguration.
- Confirm that match scores (mpeaksScore) are above 0.9 for annotated fragments and that m/z matching tolerances (mzTol) are ≤ 0.01 Da.
- Visually inspect the filtered spectrum plot to ensure that marker peaks correspond to known fragmentation ions (e.g., loss of water, CO₂, or characteristic neutral losses for the compound class).
- Validate the output CSV library entry structure: it should contain columns for m/z, intensity, and match score, with no null or negative intensity values.

## Limitations

- Default thresholds (noise=0.005, mpeaksThres=0.1) are calibrated for relative intensity units in centroid-mode spectra and may not be appropriate for absolute intensity counts or profile-mode data. Users must validate thresholds empirically for their instrument and acquisition method.
- Noise thresholds do not account for mass-dependent signal suppression in LC-MS, where low m/z ions may have inherently lower intensity. A fixed intensity threshold may over-filter high m/z regions or under-filter low m/z regions.
- No changelog or version history is documented for MetaboAnnotatoR, so threshold behavior across releases is not tracked; reproducibility across tool versions is not guaranteed.
- The skill assumes centroid-mode input; application to profile-mode or raw binary data requires prior transformation, which is not covered by this skill.
- Filtering may discard weak but genuine signals from low-abundance metabolites or minor isotopologues, potentially missing biologically relevant compounds in complex mixtures.

## Evidence

- [intro] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode"
- [other] Peak-picking filtering at noise threshold of 0.005 to remove low-intensity signals: "Apply peak-picking filtering at noise threshold of 0.005 to remove low-intensity signals"
- [other] Apply marker peak filtering at threshold of 0.1 to identify significant fragment peaks: "Apply marker peak filtering at threshold of 0.1 to identify significant fragment peaks"
- [other] genFragEntry converts an MS/MS spectrum into a library entry by identifying marker peaks above the mpeaksThres threshold (0.1 default) and noise level (0.005 default): "genFragEntry converts an MS/MS spectrum into a library entry by identifying marker peaks above the mpeaksThres threshold (0.1 default) and noise level (0.005 default)"
- [intro] noise=0.005 and mpeaksThres=0.1 parameters documented in the article: "Peak-picking above noise level threshold (default: 0.005) [section=intro; evidence='noise=0.005'] Peak-picking above marker peak threshold (default: 0.1) [section=intro; evidence='mpeaksThres=0.1']"
- [other] Output results as a CSV-formatted library entry containing annotated fragments with mass, intensity, and match scores: "Output results as a CSV-formatted library entry containing annotated fragments with mass, intensity, and match scores"
