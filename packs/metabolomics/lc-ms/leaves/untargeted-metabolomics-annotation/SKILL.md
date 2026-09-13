---
name: untargeted-metabolomics-annotation
description: Use when you have authentic metabolite standards analyzed by LC-MS in
  both positive and negative ESI modes (converted to .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - metScribeR
  - R
  - Shiny
  - chromatographR
  - mzR
  - MSConvert
  - MassBank of North America (MoNA)
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
  - build: coll_george_cq
    doi: 10.1021/acs.analchem.5b03628
    title: geoRge
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

# Build in-house MS1 & RT metabolite library standards for untargeted metabolomics annotation

## Summary

metScribeR automates the construction of curated metabolite reference libraries from LC-MS/MS data of authentic standards, using MS1 m/z and retention time (RT) values to enable high-confidence compound identification in untargeted metabolomics workflows. This skill is essential when you have authentic reference standards analyzed in positive and negative ESI modes and need to create a searchable library for identifying unknowns in experimental samples.

## When to use

You have authentic metabolite standards analyzed by LC-MS in both positive and negative ESI modes (converted to .mzML format), along with metadata (common name, monoisotopic mass, inchiKey if available) and want to build a validated in-house reference library for matching against untargeted metabolomics data. This is the appropriate workflow when MS2/MS/MS data are unavailable or not required for your identification confidence threshold, and when manual curation of detected peaks is feasible.

## When NOT to use

- Your input is already a validated metabolite reference library or MSMS spectral database (e.g., MassBank, HMDB)—use library search directly instead.
- You only have MS2/MS/MS data without authentic standards data or retention time measurements—this workflow explicitly excludes MS2 data from library building.
- You lack authentic reference standards or cannot provide both positive and negative ESI mode LC-MS data for your target metabolites.

## Inputs

- mzML files (positive and negative ESI LC-MS data of authentic standards)
- standards_df.csv (common_name, monoisotopic_mass, pos_mode_mzML_file_path, neg_mode_mzML_file_path, optional inchiKey and additional_identifiers)
- adduct_df.csv (adduct name, change_from_neutral mass, ionization mode)

## Outputs

- exported_metScribeR_library.csv (curated library with MS1 m/z, RT, adduct identity for 'good' peaks)
- exported_metScribeR_library_with_metrics.csv (all peaks classified and peak quality metrics)
- exported_metScribeR_MoNA_MSMS.csv (optional MS/MS spectra from MassBank of North America)
- Figures directory (PNG chromatograms of each manually reviewed peak)
- storage_object.RDS (checkpoint for resuming curation progress)

## How to apply

Install metScribeR and its dependencies (chromatographR, mzR via BiocManager). Prepare a standards_df.csv with columns: common_name, monoisotopic_mass, pos_mode_mzML_file_path, neg_mode_mzML_file_path (optionally inchiKey, additional_identifiers); and an adduct_df.csv with columns: adduct, change_from_neutral, mode (POS/NEG). Launch the Shiny app via runMetScribeRShinyApp(), upload both CSVs, set noise threshold using the background noise plot, and specify m/z and RT tolerances based on your LC-MS instrument resolution. In the 'Find Peaks' tab, adjust density filtering and data smoothing parameters to optimize peak detection for your method. Move to 'Review Results' tab and manually classify each detected peak as 'Good Peak', 'Bad Peak', or 'Multimodal/Indeterminate' by inspecting the extracted ion chromatogram (EIC) boundaries (blue/red vertical lines mark peak start/end; dashed line marks RT). Optionally search MoNA for MS/MS data to enrich annotations. Export the final library via 'View/Export Library' tab—the exported_metScribeR_library.csv contains 'good' adducts ready for compound identification.

## Related tools

- **metScribeR** (Primary automated workflow engine for processing in-house metabolite library standards data, peak detection, and interactive curation via Shiny app) — https://github.com/ncats/metScribeR
- **Shiny** (Interactive web interface for parameter tuning (noise threshold, m/z tolerance, RT tolerance), peak review and manual classification, and library export)
- **chromatographR** (Dependency for chromatographic data processing and EIC extraction) — https://github.com/ethanbass/chromatographR
- **mzR** (Bioconductor package for reading and parsing mzML mass spectrometry data files)
- **MSConvert** (Upstream tool to convert various mass spectrometry vendor formats to .mzML standard format prior to metScribeR processing)
- **MassBank of North America (MoNA)** (Optional external database lookup to enrich library with MS/MS spectra for curated peaks)

## Examples

```
library(metScribeR); setwd('/path/to/extdata'); runMetScribeRShinyApp()
```

## Evaluation signals

- Schema validation: exported_metScribeR_library.csv contains all required columns (common_name, monoisotopic_mass, m/z, RT, adduct identity) with no missing values in 'good' peak rows.
- Peak quality consistency: manually classified 'Good Peaks' exhibit sharp, unimodal EIC signals with well-defined start (blue) and end (red) boundaries that do not overlap with incidental peaks.
- Adduct assignment accuracy: crossed adducts check (via Shiny button) confirms absence of impossible adduct combinations for each compound's monoisotopic mass.
- Library completeness: number of 'good' peaks exported matches the count expected from your standards_df input, accounting for compounds with detectable signal in at least one ionization mode.
- MoNA enrichment (optional): MS/MS records successfully retrieved for ≥80% of 'good' peaks indicates correct inchiKey mapping and MoNA server responsiveness.

## Limitations

- Requires authentic reference standards; cannot build library from unknown analytes or from literature-only monoisotopic masses without experimental validation.
- Manual peak curation is labor-intensive; review time scales with number of detected peaks (README estimates ~30 min for 12,000 mzML files to complete initial computation before manual review).
- MS2 data are not integrated into library construction, limiting identification specificity if two isomeric compounds co-elute and share identical MS1 m/z and RT.
- MoNA MS/MS lookup depends on external server speed and availability; collection can be slow and is not guaranteed for all compounds, especially for non-metabolite or proprietary standards.
- m/z and RT tolerance parameters must be manually tuned based on instrument capability; incorrect settings may cause missed peaks or false adduct assignments.
- Library performance depends on the quality of the input LC-MS data; poorly resolved peaks, contamination, or suboptimal ionization will propagate into the final library.

## Evidence

- [readme] metScribeR focuses library building on MS1 & RT data, and MS2 data is not used or required for library construction: "metScribeR focuses library building on MS1 & RT data, and MS2 data is not used or required for library construction"
- [readme] The package provides an automated workflow for processing in-house metabolite library standards data for use in untargeted metabolomics identification workflows: "This package provides an automated workflow for processing in-house metabolite library standards data for use in untargeted metabolomics identification workflows"
- [readme] Create standards_df.csv with required columns: common_name, monoisotopic_mass, pos_mode_mzML_file_path, neg_mode_mzML_file_path, optionally inchiKey and additional_identifiers: "Create standards_df.csv (or .tsv) with the following required, identically spelled column names: common_name, with the name of each standard; monoisotopic_mass, the neutral mass of each standard;"
- [readme] Manual peak review workflow: toggle between peaks, classify as 'Good Peak', 'Bad Peak', or 'Multimodal/Indeterminate' based on EIC boundaries: "Toggle between peaks with the drop-down menu and arrow buttons. In each figure, the blue and red vertical lines indicate the beginning and ending boundaries of the peak. The dashed vertical line"
- [readme] m/z and RT tolerance parameters should be set based on LC-MS equipment resolution capability: "choose an m/z and RT tolerance for creating EICs and distinguishing between adducts. These tolerances should be set based on the ability for the LC-MS equipment to confidently separate two signals"
- [readme] Output files include exported_metScribeR_library.csv for identifications, with_metrics variant, and optional MoNA_MSMS data: "The exported_metScribeR_library.csv file is the primary library including all 'good' adducts and information relevant for making identifications with your new library"
