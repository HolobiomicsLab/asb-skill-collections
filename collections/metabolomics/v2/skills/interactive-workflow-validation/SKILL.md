---
name: interactive-workflow-validation
description: 'Use when after automated peak detection has identified candidate peaks from LC-MS mzML files, but before exporting the final metabolite library. Use this skill when you need to: (1) optimize noise and peak-detection parameters by visualizing their effect on a representative subset of peaks;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - metScribeR
  - R
  - chromatographR
  - mzR
  - Shiny
  - MoNA (MassBank of North America)
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
---

# interactive-workflow-validation

## Summary

Use a Shiny-based interactive application to manually inspect, filter, and validate peaks detected in LC-MS metabolite standards data before finalizing a curated library. This skill bridges automated peak detection with expert judgment, allowing real-time parameter tuning and peak-by-peak curation decisions.

## When to use

After automated peak detection has identified candidate peaks from LC-MS mzML files, but before exporting the final metabolite library. Use this skill when you need to: (1) optimize noise and peak-detection parameters by visualizing their effect on a representative subset of peaks; (2) manually review and classify peaks as 'Good', 'Bad', or 'Multimodal/Indeterminate' to ensure library quality; (3) inspect extracted ion chromatograms (EICs) to distinguish true adducts from artefacts.

## When NOT to use

- Input mzML files are not in standard LC-MS format or have not been converted from vendor formats (use MSConvert first if necessary).
- You do not have authentic chemical standards corresponding to the rows in standards_df—interactive validation requires visual confirmation of known peaks.
- MS1 and RT data are insufficient to distinguish your analytes; if MS2 fragmentation is required for confident identification, this workflow will not resolve ambiguities that require spectral matching.

## Inputs

- standards_df.csv or .tsv with columns: common_name, monoisotopic_mass, pos_mode_mzML_file_path, neg_mode_mzML_file_path, and optional inchiKey and additional_identifiers
- adduct_df.csv or .tsv with columns: adduct, change_from_neutral, mode (POS or NEG)
- LC-MS mzML files (positive and negative ESI mode) referenced in standards_df
- Initial metScribeR storage object (after noise and tolerance parameters submitted)

## Outputs

- exported_metScribeR_library.csv containing all 'Good' adducts and identification-relevant metadata
- exported_metScribeR_library_with_metrics.csv including all 'Good', 'Bad', and 'Multimodal/Indeterminate' adducts plus peak quality metrics
- exported_metScribeR_MoNA_MSMS.csv with matched MS/MS spectra from MoNA (optional)
- Figures directory with .png images of each manually reviewed peak
- storage_object.RDS with current analysis state for resuming progress

## How to apply

Launch the metScribeR Shiny app after uploading standards and adduct CSV files and completing the initial noise and tolerance submission. In the 'Find Peaks' tab, iteratively adjust density filtering and data smoothing settings while toggling through a subset of 50 representative peaks; use the displayed chromatograms (with blue and red boundary lines) and boxplots to assess which parameter values best separate signal from noise for your LC-MS method. Then move to the 'Review Results' tab and manually evaluate each peak that passed filtering by examining its EIC boundaries (blue/red lines), retention time marker (dashed line), and any co-eluting incidental peaks (black lines); assign each peak a confidence label (Good/Bad/Multimodal). Finally, update the library and optionally check for crossed adducts and query MoNA for MS/MS validation before exporting the final CSV library.

## Related tools

- **metScribeR** (Shiny application that implements the interactive peak validation and library curation interface; launches via runMetScribeRShinyApp()) — https://github.com/ncats/metScribeR
- **chromatographR** (Upstream R package dependency for chromatographic data processing and EIC extraction)
- **mzR** (Bioconductor package for reading and parsing mzML mass spectrometry data files)
- **Shiny** (R framework providing the interactive user interface for parameter tuning, peak visualization, and manual classification)
- **MoNA (MassBank of North America)** (Optional external spectral database queried by metScribeR to retrieve and validate MS/MS data for detected peaks)

## Examples

```
library(metScribeR); setwd('C:/Users/user123/Downloads/metScribeR_extdata_folder'); runMetScribeRShinyApp()
```

## Evaluation signals

- Peak boundary lines (blue/red vertical lines in EICs) align visually with chromatographic peak shoulders; dashed retention-time marker is centered within peak boundaries.
- Incidental peaks (marked with black lines) in the same EIC are correctly distinguished from the peak under review, indicating proper peak deconvolution.
- Peaks classified as 'Good' have consistent MS1 m/z and RT across replicate standards (within specified m/z and RT tolerances); 'Bad' peaks show anomalous boundaries, low signal-to-noise, or ambiguous RT.
- Final exported library CSV contains non-empty rows only for peaks marked 'Good'; row count and adduct composition reflect user's manual classifications.
- When MoNA cross-check is applied, peaks with high crossed-adduct probability or unambiguous MS/MS matches are flagged for secondary review.

## Limitations

- Manual review is labor-intensive and subjective; consistency depends on operator expertise and fatigue, especially for large submissions (e.g., ~12,000 mzML files may take ~30 min for initial computation alone).
- Peak detection and boundary assignment rely on noise level, m/z tolerance, and RT tolerance set in the initial submission; poor initial parameters may require restarting from the noise-plot step.
- MS/MS validation via MoNA query is dependent on MoNA server availability and speed; collection can be slow or fail if the server is under heavy load.
- Density filtering and data smoothing are heuristic; no automated criteria exist to determine optimal settings for all LC-MS methods—visual inspection of a 50-peak subset may not capture rare edge cases in the full dataset.

## Evidence

- [readme] metScribeR focuses library building on MS1 & RT data, and MS2 data is not used or required for library construction: "metScribeR focuses library building on MS1 & RT data, and MS2 data is not used or required for library construction"
- [readme] The Shiny app allows interactive parameter tuning and peak-by-peak manual review: "Use the noise plot figure on the right side of the screen to find and input the level of the background noise"
- [readme] Peaks are visualized with boundary markers and retention-time indicators: "In each figure, the blue and red vertical lines indicate the beginning and ending boundaries of the peak. The dashed vertical line indicates the RT of the peak."
- [readme] Manual classification occurs in the Review Results tab: "Click Good Peak, Bad Peak, and Multimodal/Indeterminate to indicate your confidence in the quality of the peak for inclusion in the final library."
- [readme] Output exports support downstream identification workflows: "Use the Export Library csv button to save progress and export .csv library results for use identifying experimental compounds."
- [readme] Computational cost of initial submission: "For large submissions, this computation will take some time (~30 min for 12000 mzML files)."
