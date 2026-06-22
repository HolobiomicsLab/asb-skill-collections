---
name: spectral-library-entry-generation
description: Use when you have an experimental or public MS/MS spectrum (e.g., from MassBank in msp format, or a raw centroid-mode chromatogram) and need to create a reusable library entry for a known metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3636
  edam_topics:
  - http://edamontology.org/topic_0091
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-entry-generation

## Summary

Convert an experimental MS/MS spectrum into a scored metabolite library entry by applying peak-picking thresholds, identifying marker fragments, and annotating fragment ions with match scores. This skill is essential for building custom fragment databases from experimental or public spectral data to support downstream metabolite annotation in untargeted LC–MS metabolomics workflows.

## When to use

You have an experimental or public MS/MS spectrum (e.g., from MassBank in msp format, or a raw centroid-mode chromatogram) and need to create a reusable library entry for a known metabolite. Apply this skill when you want to build or augment a fragment database with scored, annotated fragments that will later be matched against features in untargeted all-ion fragmentation (AIF) LC–MS datasets.

## When NOT to use

- Your spectrum is already in a curated, published library (e.g., MassBank, GNPS); import directly instead of regenerating.
- You are annotating a feature table against an existing library; use annotateRC or spectral matching instead.
- Your input is profile-mode (non-centroid) data; preprocess to centroid mode using xcms or vendor software first.

## Inputs

- MS/MS spectrum in centroid mode (raw mzML/netCDF or MassBank .msp format)
- Metabolite identifier (name, standard InChI or SMILES)
- Adduct notation (e.g., [M+H]+, [M-H]−)
- Accurate adduct m/z value
- Output filename for library entry

## Outputs

- CSV-formatted library entry with columns: fragment m/z, intensity, match score
- Annotated MS/MS spectrum object (RAMClustR-compatible format)
- Metabolite metadata record (name, adduct, precursor m/z)

## How to apply

Load the MS/MS spectrum in centroid mode and apply a two-stage peak-picking filter: first, remove low-intensity noise below the noise threshold (default 0.005 relative intensity); second, identify marker peaks above the mpeaksThres threshold (default 0.1) that represent significant fragment ions. Execute the genFragEntry function with parameters mpeaksScore=0.9 and mzTol=0.01 (m/z tolerance in Da) to annotate fragment peaks and assign occurrence-based match scores. Provide explicit metadata including the metabolite name, adduct notation (e.g., [M+H]+), accurate adduct m/z value, and desired output filename. The function outputs a CSV-formatted library entry with columns for fragment mass, intensity, and match scores, suitable for use in annotateRC or other fragment-matching workflows.

## Related tools

- **MetaboAnnotatoR** (R package providing genFragEntry function to generate and score library entries from MS/MS spectra) — https://github.com/gggraca/MetaboAnnotatoR
- **xcms** (LC-MS data processing and peak-picking; converts raw chromatograms to centroid mode)
- **RamClustR** (Generates pseudo-MS/MS spectra from AIF chromatograms; output format compatible with library entry generation)

## Examples

```
genFragEntry(MS2spectrum = spectrum_obj, metaboliteName = 'D-Pantothenic Acid', adduct = '[M+H]+', adductMz = 220.1179, mpeaksThres = 0.1, mpeaksScore = 0.9, mzTol = 0.01, outputFile = 'DPantothenic_MH_library.csv')
```

## Evaluation signals

- Output CSV contains non-empty columns for fragment m/z (numeric, sorted ascending), intensity (0–1 range), and match score (0–1 range).
- Marker peak count is consistent with expected fragmentation pattern for the metabolite (typically 3–20 significant fragments for small-molecule metabolites).
- No peaks below noise threshold (0.005) or marker threshold (0.1) are included in the output.
- Metadata fields (metabolite name, adduct notation, precursor m/z) are correctly populated and match input specifications.
- Library entry can be successfully imported into annotateRC without schema or parsing errors.

## Limitations

- Requires centroid-mode input; profile-mode spectra must be centroided first, introducing potential peak distortion or loss of low-intensity signals.
- Peak-picking thresholds (noise=0.005, mpeaksThres=0.1) are fixed defaults; user cannot easily optimize per spectrum or metabolite class without modifying the package code.
- Occurrence scoring relies on peak intensity alone; does not incorporate retention time, isotope patterns, or adduct-specific fragmentation rules.
- No built-in conflict resolution for isobaric fragments or spectral artifacts (e.g., solvent peaks, contamination).
- No changelog or version history documented; reproducibility across tool updates is not guaranteed.

## Evidence

- [other] genFragEntry converts MS/MS spectrum into library entry by identifying marker peaks: "genFragEntry converts an MS/MS spectrum into a library entry by identifying marker peaks above the mpeaksThres threshold (0.1 default) and noise level (0.005 default), attributing occurrence scores"
- [intro] Two-stage peak-picking filter workflow: "Apply peak-picking filtering at noise threshold of 0.005 to remove low-intensity signals. Apply marker peak filtering at threshold of 0.1 to identify significant fragment peaks."
- [readme] Centroid mode requirement: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
- [other] Output format and parameters: "Output results as a CSV-formatted library entry containing annotated fragments with mass, intensity, and match scores."
- [other] Function parameters and metadata inputs: "Execute genFragEntry function with mpeaksScore=0.9 and mzTol=0.01 to annotate fragment ions and generate scored matches. ... requires explicit definition of metabolite name, adduct notation, accurate"
- [readme] Library generation from public databases: "Generation of Metabolite fragment database entry from MS/MS spectra from public databases (in .msp format)."
