---
name: ms-ms-spectrum-peak-annotation
description: Use when you have an experimental MS/MS spectrum (e.g., from MassBank or local data) and need to identify significant fragment ions above noise, assign occurrence scores to peaks, and generate a CSV-formatted library entry for use in metabolite feature annotation pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
  techniques:
  - LC-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS/MS Spectrum Peak Annotation

## Summary

Annotate fragment peaks in an MS/MS spectrum by applying noise and marker peak thresholds, then scoring matched ions against a metabolite library using occurrence-based scoring. This skill converts experimental spectra into library entries with scored fragment annotations suitable for downstream feature annotation in untargeted metabolomics workflows.

## When to use

You have an experimental MS/MS spectrum (e.g., from MassBank or local data) and need to identify significant fragment ions above noise, assign occurrence scores to peaks, and generate a CSV-formatted library entry for use in metabolite feature annotation pipelines. Apply this skill when building custom fragment libraries or validating fragment picks for a known metabolite with accurate m/z and adduct notation.

## When NOT to use

- Input is already a feature table or annotated library; use this skill only on raw or lightly processed MS/MS spectra.
- Spectrum is in profile (non-centroided) mode; genFragEntry requires centroid data.
- Metabolite identity, adduct type, or accurate precursor m/z are unknown or uncertain; the function requires explicit, accurate definitions to assign correct fragment annotations.

## Inputs

- Centroid-mode MS/MS spectrum (numeric intensity array indexed by m/z)
- Metabolite name (string identifier)
- Adduct notation (string, e.g., '[M+H]+')
- Accurate adduct m/z (float, monoisotopic mass)
- Output filename (string, .csv format)

## Outputs

- CSV-formatted metabolite library entry
- Annotated fragment table with columns: fragment m/z, intensity, occurrence score, match metric

## How to apply

Load the centroid-mode MS/MS spectrum and apply two cascading peak-picking filters: (1) remove signals below the noise threshold (default 0.005 relative intensity) to eliminate background noise; (2) retain only marker peaks above the mpeaksThres threshold (default 0.1) to identify significant fragments. Execute the genFragEntry function with parameters mpeaksScore=0.9 and mzTol=0.01 m/z tolerance to annotate fragment ions, compute occurrence-based match scores, and associate each peak with its mass, intensity, and scoring metric. Output the result as a CSV-formatted library entry containing the metabolite name, adduct notation (e.g., [M+H]+), accurate adduct m/z, and all scored fragments. The rationale is that dual thresholding reduces false-positive fragments (noise/minor isotopes) while preserving biologically relevant marker ions, and occurrence scoring weights peaks by their prevalence across reference spectra.

## Related tools

- **MetaboAnnotatoR** (Provides the genFragEntry function for MS/MS spectrum peak annotation and occurrence scoring; part of the broader annotation workflow for AIF LC–MS data) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment (version 4.5.0 or higher) required to execute genFragEntry and related functions)
- **xcms** (Upstream tool for peak-picking and feature detection from raw LC-MS chromatograms in centroid mode prior to spectrum assembly)
- **RamClustR** (Companion tool for pseudo-MS/MS spectrum generation from AIF data; produces the spectral input for genFragEntry)

## Examples

```
genFragEntry(spectrum = ms2_spectrum, metabolite = 'D-Pantothenic Acid', adduct = '[M+H]+', mz_adduct = 220.1168, mpeaksThres = 0.1, mpeaksScore = 0.9, mzTol = 0.01, outfile = 'dpantothenic_acid_lib.csv')
```

## Evaluation signals

- Output CSV file is well-formed and contains columns for m/z, intensity, and occurrence score with no missing values for retained peaks.
- All retained peaks have intensity ≥ mpeaksThres (0.1) and pass the noise threshold (≥ 0.005); verify by inspecting the intensity distribution.
- Match scores are in the expected range (0–1 or 0–0.9 depending on mpeaksScore) and reflect peak occurrence frequency in reference spectra.
- Fragment annotations are chemically reasonable for the specified adduct (e.g., neutral losses, common rearrangements) and do not include peaks below noise level.
- Library entry metadata (metabolite name, adduct notation, accurate m/z) are correctly preserved and match the input specification.

## Limitations

- No changelog or version history is documented, limiting reproducibility across MetaboAnnotatoR releases.
- Threshold defaults (noise=0.005, mpeaksThres=0.1) may require optimization for different MS platforms, ionization modes, or metabolite classes; the article does not provide guidance on threshold tuning.
- Occurrence scoring depends on availability of reference spectra in the underlying database; novel metabolites or those underrepresented in public databases may receive poor scores.
- The function requires explicit, accurate metabolite name and adduct notation; errors in these inputs will propagate into library entries and cause downstream annotation failures.

## Evidence

- [intro] noise=0.005 and mpeaksThres=0.1: "Peak-picking above noise level threshold (default: 0.005) ... Peak-picking above marker peak threshold (default: 0.1)"
- [other] genFragEntry parameters and output format: "genFragEntry converts an MS/MS spectrum into a library entry by identifying marker peaks above the mpeaksThres threshold (0.1 default) and noise level (0.005 default), attributing occurrence scores"
- [intro] Centroid mode requirement: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode"
- [other] CSV output format: "Output results as a CSV-formatted library entry containing annotated fragments with mass, intensity, and match scores."
- [readme] MetaboAnnotatoR purpose: "This R package is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases."
