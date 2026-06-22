---
name: retention-time-calibration-integration
description: Use when you have LC-MS data from authentic standards run in positive and negative ESI modes, converted to .mzML format, and you need to build an in-house metabolite reference library for untargeted identification workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0189
  - http://edamontology.org/topic_3370
  tools:
  - metScribeR
  - R
  - Shiny
  - mzR
  - chromatographR
  - MSConvert
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jproteome.5c00548
  title: metScribeR
evidence_spans:
- This package provides an automated workflow for processing in-house metabolite library standards data
- This package... can be launched using a function exported by this package
- can be launched using a function exported by this package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metscriber_cq
    doi: 10.1021/acs.jproteome.5c00548
    title: metScribeR
  dedup_kept_from: coll_metscriber_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.5c00548
  all_source_dois:
  - 10.1021/acs.jproteome.5c00548
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-calibration-integration

## Summary

Integrate retention time (RT) measurements from LC-MS analysis of authentic standards into a curated metabolite library for use in untargeted metabolomics compound identification. This skill combines RT data with MS1 m/z values to establish library entries without requiring MS2 spectra.

## When to use

You have LC-MS data from authentic standards run in positive and negative ESI modes, converted to .mzML format, and you need to build an in-house metabolite reference library for untargeted identification workflows. RT calibration is necessary when your LC-MS equipment has established reproducibility in retention time across runs and you want to leverage RT as a discriminating feature alongside m/z.

## When NOT to use

- Your LC-MS data is already in a proprietary binary format and cannot be converted to .mzML
- You lack authentic standards for the metabolites you wish to identify—RT calibration requires reference compounds run in your instrument
- Your LC method exhibits significant RT drift or poor reproducibility across runs, making RT an unreliable discriminator

## Inputs

- LC-MS data files in .mzML format (positive and negative ESI modes)
- standards_df.csv with columns: common_name, monoisotopic_mass, pos_mode_mzML_file_path, neg_mode_mzML_file_path
- adduct_df.csv with columns: adduct, change_from_neutral, mode (POS/NEG)
- Monoisotopic mass values for each standard

## Outputs

- exported_metScribeR_library.csv containing 'good' adducts with RT and m/z values
- exported_metScribeR_library_with_metrics.csv including all adduct classifications and peak metrics
- Figures directory with .png images of each manually reviewed peak
- storage_object.RDS for workflow state persistence

## How to apply

Prepare a standards_df.csv file containing common_name, monoisotopic_mass, and paths to pos_mode_mzML_file_path and neg_mode_mzML_file_path for each authentic standard. Load this into metScribeR along with an adduct_df.csv defining expected adducts and their mass shifts. Set m/z and RT tolerances based on your LC-MS instrument's resolution and peak separation capability. Launch the metScribeR Shiny app, adjust noise thresholds using the noise plot, and apply density filtering and smoothing in the 'Find Peaks' tab to identify peaks. Manually review each peak in the 'Review Results' tab, marking peaks as 'Good', 'Bad', or 'Multimodal/Indeterminate' based on peak shape and RT consistency. Export the curated library as exported_metScribeR_library.csv, which contains RT assignments for each validated standard adduct pair.

## Related tools

- **metScribeR** (Automated workflow engine for processing in-house metabolite standards data, executing peak detection, RT extraction, and library curation via Shiny interactive interface) — https://github.com/ncats/metScribeR
- **Shiny** (Interactive R application framework hosting the metScribeR user interface for noise threshold setting, peak review, and manual curation)
- **mzR** (R package for reading and parsing .mzML mass spectrometry data files to extract MS1 m/z and RT information)
- **chromatographR** (R package providing chromatographic data processing and peak detection utilities required by metScribeR) — https://github.com/ethanbass/chromatographR
- **MSConvert** (External utility for converting vendor-specific mass spectrometry data formats to open .mzML standard format)

## Examples

```
library(metScribeR); setwd('path/to/extdata'); runMetScribeRShinyApp()
```

## Evaluation signals

- Exported library CSV contains no null RT or m/z values for 'good' peaks, and all common_names match input standards_df
- Peak boundaries (blue and red vertical lines in review figures) are consistent and reproducible across replicate standards
- RT values for the same standard across positive and negative ESI modes fall within the specified RT tolerance threshold
- Manual peak review decisions ('Good', 'Bad', 'Multimodal') correlate with peak shape quality and signal-to-noise ratio visible in the Figures directory
- Adduct masses computed from monoisotopic_mass + change_from_neutral match observed m/z values within the specified m/z tolerance

## Limitations

- Computation time for large submission sets (~30 min for 12,000 mzML files) may be prohibitive for exploratory analysis
- MS2 data is not used or required, limiting structural confirmation; library identifications rely on MS1 m/z and RT alone
- Manual review step scales linearly with number of peaks, creating a bottleneck for high-complexity metabolite mixtures
- RT assignments are instrument- and method-specific; libraries built on one LC system may not transfer directly to another without revalidation
- Crossed adduct detection (checking for potential m/z overlap between different adducts) requires explicit user action on the View/Export Library tab

## Evidence

- [readme] MS1 and RT data are the basis for library construction: "metScribeR focuses library building on MS1 & RT data, and MS2 data is not used or required for library construction"
- [readme] Workflow accepts mzML files with RT and m/z from LC-MS standards: "In the wet lab, process authentic standards with LC-MS in positive and negative ESI modes and convert the results to .mzML format"
- [readme] Standards table structure requires RT file paths and monoisotopic mass: "Create standards_df.csv (or .tsv) with the following required, identically spelled column names: common_name, with the name of each standard; monoisotopic_mass, the neutral mass of each standard;"
- [readme] User sets m/z and RT tolerances based on instrument resolution: "choose an m/z and RT tolerance for creating EICs and distinguishing between adducts. These tolerances should be set based on the ability for the LC-MS equipment to confidently separate two signals"
- [readme] Manual peak review produces final library with RT assignments: "Here, each peak that passed filtering must be manually reviewed for inclusion in the final library. Toggle between peaks with the drop-down menu and arrow buttons"
- [readme] Primary output is a library CSV with RT values for good peaks: "The exported_metScribeR_library.csv file is the primary library including all 'good' adducts and information relevant for making identifications with your new library"
