---
name: configuration-file-interpretation
description: Use when when you have PSM files from proteomics search engines (MaxQuant, MSGFPlus, Sage, etc.) that use non-standard modification notation (e.g., 'ox', '+57.02146', or mass-shift labels) and need to resccore peptide identifications with MS²Rescore.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - psm_utils
  - MS²Rescore
  - Percolator
  - Mokapot
  - DeepLC
derived_from:
- doi: 10.1002/pmic.202300336
  title: MS2Rescore (immunopeptidome rescoring)
evidence_spans:
- Accepted ProForma modification labels in :py:mod:`psm_utils`
- MS²Rescore is a tool for rescoring peptide-spectrum matches
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
---

# configuration-file-interpretation

## Summary

Parse and apply JSON/TOML configuration files to map search-engine-specific modification labels to standardized ProForma notation, enabling MS²Rescore to correctly link PSMs to spectra and configure rescoring parameters. This skill is essential for translating heterogeneous search engine outputs into a unified proteomics rescoring workflow.

## When to use

When you have PSM files from proteomics search engines (MaxQuant, MSGFPlus, Sage, etc.) that use non-standard modification notation (e.g., 'ox', '+57.02146', or mass-shift labels) and need to resccore peptide identifications with MS²Rescore. The configuration file bridges the gap between search engine output and the ProForma v2 standard required by rescoring engines and feature generators like DeepLC.

## When NOT to use

- PSM files already contain ProForma-compliant modification notation (e.g., from a previous MS²Rescore run) — no remapping is needed.
- You have pre-filtered PSM files (FDR-filtered results) — MS²Rescore requires access to ALL target and decoy PSMs without FDR filtering.
- Spectrum files are unavailable or unlinked — some feature generators (e.g., DeepLC) require spectrum data and cannot proceed with configuration alone.

## Inputs

- JSON or TOML configuration file with modification_mapping, fixed_modifications, spectrum_id_pattern, id_decoy_pattern, and rescoring engine settings
- PSM files from search engines (MaxQuant msms.txt, MSGFPlus .mzid, Sage .sage.tsv, etc.) in formats supported by psm_utils
- Spectrum files in mzML or mgf format linked via spectrum_id_pattern

## Outputs

- Parsed configuration object with validated modification mappings conforming to ProForma v2
- PSM objects with remapped peptide sequences using ProForma notation
- Intermediate or final PSM file with standardized modification labels ready for feature generation and rescoring
- Decoy/target PSM sets correctly partitioned using id_decoy_pattern

## How to apply

Load the JSON or TOML configuration file that contains three key mappings: (1) modification_mapping, which translates each search-engine-specific modification label to ProForma notation using PSI-MOD accession, PSI-MOD name, Unimod accession, Unimod name, or chemical formula (e.g., 'Formula:HO3P'); (2) fixed_modifications, mapping amino acids to modification names for modifications not reported in the PSM file; and (3) spectrum_id_pattern and id_decoy_pattern regex patterns to extract scan numbers and identify decoy PSMs. For each PSM, iterate through its peptide sequence and replace each search-engine modification label with its corresponding ProForma label from the mapping dictionary. Validate that all mapped labels conform to HUPO-PSI ProForma v2 notation using psm_utils validation. The configuration also specifies decoy identification strategy (e.g., 'DECOY_' protein name prefix) and rescoring engine parameters (Mokapot or Percolator). Apply the configuration via CLI (ms2rescore --config config.toml), GUI, or Python API before feature generation and rescoring.

## Related tools

- **MS²Rescore** (Primary rescoring platform that reads and applies the configuration file to map modifications, link PSMs to spectra, and orchestrate rescoring) — https://github.com/compomics/ms2rescore
- **psm_utils** (Validates that mapped modification labels conform to HUPO-PSI ProForma v2 notation and parses PSM files from multiple search engines)
- **Percolator** (Rescoring engine configured and invoked by MS²Rescore after modification mapping is applied) — https://github.com/percolator/percolator/releases/latest
- **Mokapot** (Alternative rescoring engine that can be selected and configured via the configuration file)
- **DeepLC** (Feature generator that requires modification formula notation; configuration determines which modification format is preferred)

## Examples

```
ms2rescore --config config.toml input_psms.mzid --spectrum_files spectra.mzML
```

## Evaluation signals

- All search-engine-specific modification labels (e.g., 'ox', 'gl', '+57.02146') are successfully mapped to ProForma labels (e.g., 'U:Oxidation', 'U:Gln->pyro-Glu') and validate against psm_utils ProForma v2 schema without errors.
- PSM-to-spectrum linkage succeeds for ≥95% of PSMs using the spectrum_id_pattern regex; failed linkages are logged and investigated.
- Decoy PSMs are correctly identified using id_decoy_pattern (e.g., protein name prefix 'DECOY_' or custom regex); decoy rate in output matches input before rescoring.
- Fixed modifications not reported in the PSM file are correctly added to the peptide sequences for all affected amino acids (e.g., carbamidomethyl on all C residues).
- Feature generators (DeepLC, MS²PIP) and rescoring engines (Percolator, Mokapot) execute without modification-related errors after configuration is applied; rescoring improves PSM confidence scores and increases identifications at constant FDR threshold.

## Limitations

- Some search engines (e.g., MaxQuant) do not report fixed modifications in the PSM file; these must be configured separately in fixed_modifications or rescoring will not account for them.
- Mass-shift notation (e.g., '+57.02146') is ambiguous and may map to multiple modifications; formula notation (e.g., 'Formula:HO3P') is preferred for modifications not in PSI-MOD or Unimod controlled vocabularies.
- Regex patterns for spectrum_id_pattern, id_decoy_pattern, and PSM_id extraction (psm_id_pattern) are search-engine-specific and error-prone; incorrect patterns cause silent PSM-spectrum mismatches or incorrect decoy identification.
- Configuration file format (JSON vs. TOML) and parameter naming differ across MS²Rescore versions; version compatibility must be verified.

## Evidence

- [intro] MS²Rescore requires mapping of search engine modification labels to ProForma notation: "most PSM file types coming from different proteomics search engines use a custom modification notation...Therefore, ``ox`` needs to be mapped to ``U:Oxidation``"
- [intro] Configuration via JSON/TOML file is a primary usage mode: "MS²Rescore can be configured through the command line interface (CLI), the graphical user interface (GUI), or a JSON/TOML configuration file"
- [methods] Modification mapping accepts five standardized formats from controlled vocabularies: "modification_mapping as a configuration object that maps search-engine-specific modification labels to ProForma labels in five accepted formats: PSI-MOD accession, PSI-MOD name, Unimod accession,"
- [intro] Fixed modifications must be configured separately for search engines that do not report them: "fixed modifications that are not reported in the PSM file must be configured separately"
- [intro] Decoy identification is configured via regex pattern: "it can usually be derived from the protein name. For example, if the protein name contains the prefix ``DECOY_``, the PSM is a decoy PSM"
- [intro] Spectrum linkage requires configurable ID extraction patterns: "Essential for MS²Rescore to function correctly is linking the search engine PSMs to the original spectra...two options are available to map PSMs to spectra: ``spectrum_id_pattern`` and"
- [intro] Input requires all target and decoy PSMs unfiltered: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
- [intro] ProForma v2 is the standardized notation required: "MS²Rescore uses the `HUPO-PSI standardized ProForma v2 notation` to represent modified peptides"
