---
name: ms-dial-export-format-handling
description: Use when you have performed lipid identification in MS-DIAL and need
  to pass the results to LipoCLEAN or another downstream quality-filtering tool. The
  skill is required whenever you are preparing MS-DIAL output for consumption by external
  analysis pipelines that expect standardized export formats.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - LipoCLEAN
  - MS-DIAL
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.4c04040
  title: lipoclean
evidence_spans:
- LipoCLEAN is a command line tool
- quality filter for lipid identifications from MS-DIAL
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipoclean
    doi: 10.1021/acs.analchem.4c04040
    title: lipoclean
  dedup_kept_from: coll_lipoclean
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c04040
  all_source_dois:
  - 10.1021/acs.analchem.4c04040
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-dial-export-format-handling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure MS-DIAL to export lipid identifications in the correct format (m/z matrix, msp export format, with blank filtering disabled) so that downstream tools like LipoCLEAN can correctly parse and filter the results. This skill ensures MS-DIAL output is compatible with machine learning-based quality filtering pipelines.

## When to use

You have performed lipid identification in MS-DIAL and need to pass the results to LipoCLEAN or another downstream quality-filtering tool. The skill is required whenever you are preparing MS-DIAL output for consumption by external analysis pipelines that expect standardized export formats.

## When NOT to use

- Input data is already in a non-MS-DIAL format (e.g., already exported from another tool or vendor software).
- You need raw MS-DIAL project files (.msp, .ms2) rather than the alignment export; use the native export options instead.
- Blank filtering has already been applied upstream and you need to preserve all identifications without any background subtraction.

## Inputs

- MS-DIAL alignment result (in-memory or saved project)
- Output directory path for export

## Outputs

- Tab-delimited .txt file with 'm/z matrix' export (filename starts with 'Mz')
- File contains MS/MS spectrum column and right-aligned m/z matrix columns

## How to apply

Within MS-DIAL, navigate to the Export menu and select 'Alignment result' from the dropdown. Use the Browse button to navigate to your target output directory, confirm the correct alignment result is selected, and then select 'm/z matrix' as the export type (deselecting any other export formats). Ensure that blank filtering is NOT selected in the export dialog, and verify that the export format is set to 'msp'. The resulting .txt file (with filename starting with 'Mz') will contain the tab-delimited m/z matrix data required for downstream processing. This format is required because downstream tools like LipoCLEAN depend on the specific column structure and m/z numerical data layout that MS-DIAL produces under these settings.

## Related tools

- **MS-DIAL** (Source software that produces the alignment result export; configured with specific export parameters (m/z matrix format, msp format, no blank filtering))
- **LipoCLEAN** (Downstream consumer of MS-DIAL exports; applies machine learning-based quality filtering to the exported lipid identifications) — https://github.com/stavis1/LipoCLEAN

## Evaluation signals

- Output file exists in the specified directory with filename starting with 'Mz' and .txt extension.
- File is tab-delimited text readable in a text editor or spreadsheet application.
- File contains an 'MS/MS spectrum' column followed by numeric m/z columns (m/z values increase monotonically from left to right).
- Downstream tool (LipoCLEAN) successfully reads the file without parsing errors or complaints about missing or malformed columns.
- Row count matches the number of lipid identifications in the MS-DIAL alignment result (no identifications dropped during export).

## Limitations

- The export format is version-specific: MS-DIAL 4 and MS-DIAL 5 produce output with different column names and scaling, requiring separate downstream models and configuration files.
- Blank filtering cannot be selectively re-applied after export; if blank filtering was disabled during export and is later needed, the raw data must be re-exported.
- The m/z matrix export can produce large files for high-resolution datasets with many m/z bins; disk space and memory requirements scale with number of identifications and spectral resolution.
- Export settings are not automatically validated; incorrect menu selections (e.g., selecting a different export format) will produce incompatible output without user-facing warning.

## Evidence

- [readme] All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file.: "All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file."
- [readme] The export format is version-specific and affects downstream model compatibility.: "However, some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other."
- [readme] Specific MS-DIAL export procedure for inference data.: "1. Click "Export" along the top bar
2. Select "Alignment result" in the dropdown menu
3. Navigate to the directory (folder) to which you want to save the export using the "Browse" button
4. The last"
- [readme] Output file naming convention.: "A .txt will now be generated in the chosen directory with the information required for LipoCLEAN. The file name will start with "Mz""
- [readme] Training data preparation requires the same export settings.: "Start with MS-DIAL exports using the same settings as described above for inference."
