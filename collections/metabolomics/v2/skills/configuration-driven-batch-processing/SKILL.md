---
name: configuration-driven-batch-processing
description: Use when when processing multiple PSM files from search engines (e.g., MaxQuant, MSGFPlus, Mascot) that omit fixed modifications from their output, or when PSM and spectrum files use inconsistent ID schemes, decoy naming conventions, or modification notations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MS²Rescore
  - psm_utils
  - Percolator
  - Mokapot
  - ProForma v2
  techniques:
  - LC-MS
derived_from:
- doi: 10.1002/pmic.202300336
  title: MS2Rescore (immunopeptidome rescoring)
evidence_spans:
- MS²Rescore is a tool for rescoring peptide-spectrum matches
- Accepted ProForma modification labels in :py:mod:`psm_utils`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2rescore_immunopeptidome_rescoring_cq
    doi: 10.1002/pmic.202300336
    title: MS2Rescore (immunopeptidome rescoring)
  dedup_kept_from: coll_ms2rescore_immunopeptidome_rescoring_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/pmic.202300336
  all_source_dois:
  - 10.1002/pmic.202300336
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Configuration-Driven Batch Processing

## Summary

Automate rescoring of multiple PSM files and spectrum datasets by defining fixed modifications, modification label mappings, and decoy/spectrum ID patterns in a declarative configuration file (JSON/TOML), then applying these rules uniformly across all input files. This skill ensures consistent handling of unreported fixed modifications and heterogeneous search engine outputs without manual per-file intervention.

## When to use

When processing multiple PSM files from search engines (e.g., MaxQuant, MSGFPlus, Mascot) that omit fixed modifications from their output, or when PSM and spectrum files use inconsistent ID schemes, decoy naming conventions, or modification notations. Applies when you need to resccore all target and decoy PSMs uniformly while mapping engine-specific modification labels (e.g., 'ox' → 'U:Oxidation', 'CM' → 'U:Carbamidomethyl') to ProForma v2 notation before feature generation and rescoring.

## When NOT to use

- PSM file already contains all fixed modifications in its native notation and you do not need to standardize to ProForma—direct ingest without modification remapping may be simpler.
- Input PSM file is already FDR-filtered or deduplicated, as MS²Rescore requires all target and decoy PSMs without filtering.
- Spectrum files are not available and none of the feature generators (e.g., DeepLC, MS²PIP) require spectrum data—some workflows can skip spectrum linking.

## Inputs

- PSM file(s) in any psm_utils-supported format (MaxQuant msms.txt, MSGFPlus .mzid, Mascot .mzid, Sage .sage.tsv, etc.)
- Spectrum file(s) in mzML or mgf format
- Configuration file (JSON or TOML) defining modification_mapping, fixed_modifications, id_decoy_pattern, and spectrum_id_pattern

## Outputs

- Augmented PSM TSV file (<prefix>.psms.tsv) with ProForma-standardized peptide sequences and applied fixed modifications
- HTML quality control report (<prefix>.report.html) summarizing rescoring metrics and modification application

## How to apply

First, load the PSM file(s) and spectrum file(s) and inspect the modification notation used by the search engine, the decoy PSM naming pattern (e.g., prefix 'DECOY_' or regex rule), and the spectrum ID format (scan number, index, or other identifier). Define a configuration object (JSON or TOML) with three key mappings: (1) `modification_mapping` that associates each search engine label to its ProForma equivalent (e.g., {'ox': 'U:Oxidation', 'TMT': 'U:TMT6plex'}), (2) `fixed_modifications` that lists amino acids and terminal positions ('N-term', 'C-term', 'K', 'C', etc.) and their associated ProForma modification labels, and (3) regex patterns for `id_decoy_pattern` and `spectrum_id_pattern` to extract decoy flags and spectrum identifiers. For each PSM, iterate through the `fixed_modifications` map and insert the specified ProForma labels (e.g., 'U:Carbamidomethyl') at the appropriate residue positions if not already present in the sequence annotation. Finally, pass the configuration file to MS²Rescore (via CLI, GUI, or API) along with the PSM and spectrum file paths; MS²Rescore will apply the rules uniformly, link PSMs to spectra, and output augmented PSM records with standardized ProForma notation ready for downstream feature generation and rescoring.

## Related tools

- **MS²Rescore** (Primary rescoring and configuration orchestration platform that applies the configuration-driven batch workflow to PSM files, links them to spectra, and outputs standardized PSM records) — https://github.com/compomics/ms2rescore
- **psm_utils** (Handles parsing and standardization of PSM files in multiple search engine formats and validates ProForma modification labels) — https://github.com/compomics/psm_utils
- **Percolator** (Optional rescoring engine selected and configured via the batch configuration file to rescore PSMs after fixed modifications are applied) — https://github.com/percolator/percolator
- **Mokapot** (Alternative rescoring engine selectable and configurable via the batch configuration file)
- **ProForma v2** (Standardized notation format for modified peptide sequences; MS²Rescore configuration defines mappings to ProForma labels) — https://github.com/HUPO-PSI/ProForma

## Examples

```
ms2rescore --config rescoring_config.toml --psm_files MaxQuant_msms.txt --spectrum_files spectra.mzML
```

## Evaluation signals

- All PSM sequences in the output file use consistent ProForma notation (e.g., 'U:Carbamidomethyl' brackets around cysteine, 'U:TMT6plex' at N-terminus and lysine residues) matching the fixed_modifications specification.
- Fixed modifications appear at correct residue positions: terminal modifications only at N-term or C-term, amino acid–specific modifications only at matching residues, and no duplicates for modifications already reported by the search engine.
- Decoy PSMs are correctly identified and isolated using the id_decoy_pattern regex; target and decoy counts align with expected proportions from the search engine output.
- Spectrum IDs in the output PSM records match those extracted from spectrum files using the spectrum_id_pattern regex; no PSMs remain unlinked to spectra.
- Output TSV preserves all original PSM fields (score, rank, protein ID, etc.) and adds or updates only the peptide sequence field with ProForma annotations; no data loss or truncation.

## Limitations

- Configuration files must be manually authored for each search engine and modification set; errors in regex patterns (id_decoy_pattern, spectrum_id_pattern) or modification_mapping can cause silent failures or incorrect linking.
- Fixed modifications are applied uniformly to all PSMs; the configuration does not support conditional application based on PSM rank, score, or other contextual metadata.
- Spectrum files must be present and indexed if feature generators require them; mzML and mgf formats are supported, but other formats (e.g., Bruker .d for DDA-PASEF) require specialized handling (TIMS²Rescore).
- ProForma notation mapping is one-way: once mapped to ProForma, reverting to search engine–native notation or exporting to non-ProForma formats may require additional conversion steps.
- The skill assumes modifications are Unimod-based or PSI-MOD–compatible; custom or non-standard modifications may not have defined ProForma labels and will be rejected or ignored.

## Evidence

- [intro] fixed modifications that are not reported in the PSM file must be configured separately: "fixed modifications that are not reported in the PSM file must be configured separately"
- [other] Fixed modifications are configured through a mapping that associates ProForma modification labels (e.g., U:Carbamidomethyl, U:TMT6plex) with lists of residue target positions: "Fixed modifications are configured through a mapping that associates ProForma modification labels (e.g., U:Carbamidomethyl, U:TMT6plex) with lists of residue target positions, including special"
- [intro] MS²Rescore can be configured through the command line interface (CLI), the graphical user interface (GUI), or a JSON/TOML configuration file: "MS²Rescore can be configured through the command line interface (CLI), the graphical user interface (GUI), or a JSON/TOML configuration file"
- [intro] most PSM file types coming from different proteomics search engines use a custom modification notation...Therefore, ``ox`` needs to be mapped to ``U:Oxidation``: "most PSM file types coming from different proteomics search engines use a custom modification notation...Therefore, ``ox`` needs to be mapped to ``U:Oxidation``"
- [intro] MS²Rescore requires mapping of search engine modification labels to ProForma notation: "MS²Rescore requires mapping of search engine modification labels to ProForma notation"
- [intro] MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
- [other] For each PSM, iterate through the fixed_modifications map and insert the specified modifications at the appropriate positions in the sequence using ProForma notation (e.g., 'U:Carbamidomethyl') if not already present.: "For each PSM, iterate through the fixed_modifications map and insert the specified modifications at the appropriate positions in the sequence using ProForma notation (e.g., 'U:Carbamidomethyl') if"
- [intro] Both ``mzML`` and ``mgf`` formats are supported: "Both ``mzML`` and ``mgf`` formats are supported"
