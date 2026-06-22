---
name: ionization-mode-classification
description: Use when when converting raw MS/MS spectral records (e.g. from .msp format) into metabolite fragment database entries for MetaboAnnotatoR, and the output filenames or library index must distinguish between positive and negative ionization modes to ensure correct library selection during annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3172
  tools:
  - MetaboAnnotatoR
  - R
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator_cq
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator_cq
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

# ionization-mode-classification

## Summary

Classify MS/MS spectra by ionization mode (positive or negative) based on adduct type metadata to assign appropriate ionization mode suffixes to spectral library entries. This is essential for downstream metabolite annotation, as fragment libraries are mode-specific and misclassification leads to incorrect candidate ranking.

## When to use

When converting raw MS/MS spectral records (e.g. from .msp format) into metabolite fragment database entries for MetaboAnnotatoR, and the output filenames or library index must distinguish between positive and negative ionization modes to ensure correct library selection during annotation.

## When NOT to use

- Spectra already pre-sorted into separate positive and negative mode library files or directories — classification has already occurred.
- Raw LC-MS feature tables without MS/MS fragmentation data — ionization mode is assigned at acquisition, not inferred from fragments.
- Datasets lacking adduct type metadata in spectral records — classification cannot be performed without this annotation.

## Inputs

- .msp spectral library file (MS/MS spectra with adduct metadata)
- spectrum metadata including adduct type annotation

## Outputs

- .csv library entry files with ionization mode suffix appended to filename
- ionization mode classification label (positive or negative)

## How to apply

Extract the adduct type from spectrum metadata (e.g. '[M+H]+' for positive mode, '[M-H]-' for negative mode). Use this adduct annotation to infer the ionization polarity. Append the appropriate ionization mode suffix ('+' for positive, '-' for negative) to the output .csv filename. This classification gates library routing: positive-mode spectra must be queried against positive-mode libraries (e.g. LipidPos) and negative-mode spectra against their negative counterparts. The mspToLib function automates this step during batch conversion of .msp records.

## Related tools

- **MetaboAnnotatoR** (Executes mspToLib function to read .msp files, detect adduct type from spectrum metadata, and assign ionization mode suffixes to output .csv library entries) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment (version 4.5.0 or higher) for executing mspToLib and ionization mode classification logic)

## Examples

```
library(MetaboAnnotatoR); mspToLib(msp_file='MassBank_example.msp', output_dir='./lib_entries')
```

## Evaluation signals

- Output .csv filenames contain correct ionization mode suffix: '+' appended for positive-mode spectra, '-' for negative-mode spectra
- Adduct type extracted from spectrum metadata matches the assigned ionization mode (e.g. '[M+H]+' → positive, '[M-H]-' → negative)
- All spectra with [M+H]+, [M+Na]+, or similar cationic adducts are classified as positive mode; all with [M-H]-, [M+Cl]-, or anionic adducts are classified as negative mode
- Downstream annotation using classified libraries produces expected candidate rankings (e.g. lipid feature annotates to LipidPos library when classified as positive mode)
- No output files lack ionization mode suffix or contain ambiguous/unmapped mode labels

## Limitations

- Classification depends on adduct type being correctly annotated in source .msp metadata; missing or corrupted adduct fields will cause misclassification.
- Ambiguous adducts (e.g. neutral loss adducts or multiply-charged ions) may not map unambiguously to a single ionization mode and require manual review.
- The mspToLib function applies peak-picking filters (configurable noise and marker peak thresholds) during conversion; spectra filtered out during this step will not be classified or output.

## Evidence

- [other] mspToLib function applies peak-picking and assigns mode suffix: "The mspToLib function reads MS/MS spectra from .msp files, applies peak-picking with configurable noise and marker peak thresholds, assigns occurrence scores to detected peaks, and outputs library"
- [other] Adduct type inferred from spectrum metadata gates mode assignment: "Assign positive and negative ionization mode suffixes to output filenames based on adduct type detected in spectrum metadata."
- [intro] Mode-specific libraries required for annotation: "annotation can be performed using the default Lipid Positive mode libraries "*LipidPos*""
- [readme] MetaboAnnotatoR operates on centroid mode MS/MS data: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
