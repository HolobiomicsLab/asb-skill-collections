---
name: metabolite-library-curation-ms1-rt
description: Use when when you have processed authentic standards with LC-MS in positive
  and negative ESI modes, converted results to .mzML format, and need to build a validated
  in-house reference library with MS1 m/z and RT measurements for use in untargeted
  metabolomics compound identification workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - metScribeR
  - R
  - chromatographR
  - mzR
  - Shiny
  - MSConvert
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.5c00548
  title: metScribeR
evidence_spans:
- This package provides an automated workflow for processing in-house metabolite library
  standards data
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-library-curation-ms1-rt

## Summary

Automated curation of in-house metabolite reference libraries using MS1 m/z and retention time (RT) data from LC-MS standards via the metScribeR package and interactive Shiny interface. This skill enables construction of curated metabolite libraries for untargeted metabolomics without requiring MS2 data.

## When to use

When you have processed authentic standards with LC-MS in positive and negative ESI modes, converted results to .mzML format, and need to build a validated in-house reference library with MS1 m/z and RT measurements for use in untargeted metabolomics compound identification workflows.

## When NOT to use

- If you lack mzML files or monoisotopic mass values for your standards.
- If your goal is to annotate experimental samples without first validating authentic standard peaks; library curation must precede experimental compound identification.
- If you have only MS2 fragmentation data without MS1 m/z or RT measurements; metScribeR explicitly does not use MS2 for library building.

## Inputs

- mzML files (positive and negative ESI mode LC-MS analyses of authentic standards)
- standards_df.csv or .tsv (common_name, monoisotopic_mass, pos_mode_mzML_file_path, neg_mode_mzML_file_path, optional: inchiKey, additional_identifiers)
- adduct_df.csv or .tsv (adduct, change_from_neutral, mode)

## Outputs

- exported_metScribeR_library.csv (primary library with all 'good' adducts and MS1/RT data)
- exported_metScribeR_library_with_metrics.csv (all peak classifications and RT assignment metrics)
- exported_metScribeR_MoNA_MSMS.csv (optional MS/MS spectra from MoNA)
- storage_object.RDS (saved workflow state for resumption)
- Figures directory (PNG visualizations of each manually reviewed peak)

## How to apply

Prepare a standards_df.csv file with required columns (common_name, monoisotopic_mass, pos_mode_mzML_file_path, neg_mode_mzML_file_path) and an adduct_df.csv file (adduct, change_from_neutral, mode). Launch metScribeR Shiny app, upload both CSV files, set noise level threshold from the noise plot, and configure m/z and RT tolerances based on your LC-MS equipment resolution. Execute initial peak finding, then manually review each peak in the 'Review Results' tab to classify as 'Good Peak', 'Bad Peak', or 'Multimodal/Indeterminate'. Update the library and optionally check for crossed adducts and query MassBank of North America (MoNA) for MS/MS enrichment. Export the final library as .csv for downstream identification workflows.

## Related tools

- **metScribeR** (Primary package providing automated workflow for MS1/RT library curation and interactive Shiny interface for peak review and library export) — https://github.com/ncats/metScribeR
- **chromatographR** (Dependency for chromatographic data processing in metScribeR) — https://github.com/ethanbass/chromatographR
- **mzR** (Bioconductor package for reading mzML mass spectrometry files)
- **Shiny** (Interactive R web interface for visual inspection, peak filtering, manual review, and library export)
- **MSConvert** (External tool to convert various mass spectrometry data formats to .mzML)

## Examples

```
library(metScribeR); setwd('path/to/example_data'); runMetScribeRShinyApp()
```

## Evaluation signals

- Exported library .csv contains entries only for peaks manually classified as 'Good Peak', with non-missing values for common_name, monoisotopic_mass, MS1 m/z, and RT.
- Peak boundaries (blue and red vertical lines in Review Results tab figures) align with visually distinct chromatographic signals without spillover into adjacent peaks.
- Noise level threshold is set below background signal, as verified by the noise plot figure; all MS observations below this threshold are excluded.
- m/z and RT tolerances used for EIC extraction and adduct discrimination match the specified resolution of the LC-MS instrument and are consistent across all peaks.
- Optional MoNA MS/MS enrichment and crossed adduct checks complete without errors and add valid MS/MS spectra or confidence flags to the exported library.

## Limitations

- Workflow requires authentic chemical standards processed in both positive and negative ESI modes; unavailable or missing mzML files will cause errors.
- Manual peak review step is labor-intensive; computation time for large submissions (e.g., 12,000 mzML files) may exceed 30 minutes.
- MS/MS enrichment from MoNA is dependent on MoNA server speed and may be slow; inchiKey must be provided in standards_df.csv for this feature.
- Library building does not use MS2 data, so structural confirmation is limited; MS/MS is optional and sourced only from external MoNA database.
- Peak filtering and classification decisions (noise threshold, m/z/RT tolerance, peak quality assessment) are user-dependent and require domain knowledge of the LC-MS method.

## Evidence

- [readme] Core workflow purpose: "This package provides an automated workflow for processing in-house metabolite library standards data for use in untargeted metabolomics identification workflows."
- [readme] MS1/RT focus, MS2 exclusion: "metScribeR focuses library building on MS1 & RT data, and MS2 data is not used or required for library construction."
- [readme] Required input files and columns: "Create standards_df.csv (or .tsv) with the following required, identically spelled column names: common_name, with the name of each standard; monoisotopic_mass, the neutral mass of each standard;"
- [readme] Adduct configuration file specification: "Create adduct_df.csv (or .tsv) with the following columns: adduct, with the name of each adduct; change_from_neutral, with the difference between the adduct and its neutral mass; and mode, with"
- [readme] Parameter tuning rationale: "choose an m/z and RT tolerance for creating EICs and distinguishing between adducts. These tolerances should be set based on the ability for the LC-MS equipment to confidently separate two signals."
- [readme] Manual review classification: "Click Good Peak, Bad Peak, and Multimodal/Indeterminate to indicate your confidence in the quality of the peak for inclusion in the final library."
- [readme] Optional MS/MS enrichment: "If desired, use the check for crossed adducts and search MoNA for MS/MS data buttons to add internal identification probability and MS/MS data to the exported results."
- [readme] Output library format and content: "The exported_metScribeR_library.csv file is the primary library including all 'good' adducts and information relevant for making identifications with your new library."
