---
name: psm-to-spectrum-linking-validation
description: Use when when you have PSM files from a proteomics search engine (e.g.,
  MaxQuant, MSGFPlus, Mascot) and corresponding spectrum files (mzML or MGF format)
  that need to be linked before rescoring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS²Rescore
  - psm_utils
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# PSM-to-spectrum linking validation

## Summary

Validate that peptide-spectrum matches (PSMs) from search engine output are correctly linked to their corresponding mass spectra by extracting and matching spectrum identifiers using regex capture groups. This is a prerequisite for accurate feature generation and rescoring in MS²Rescore workflows.

## When to use

When you have PSM files from a proteomics search engine (e.g., MaxQuant, MSGFPlus, Mascot) and corresponding spectrum files (mzML or MGF format) that need to be linked before rescoring. Use this skill when the PSM file contains a spectrum_id field that must be matched to spectrum file titles, and the identifier extraction method is not obvious from file inspection alone.

## When NOT to use

- PSM file already contains merged or pre-validated spectrum data with explicit spectrum indices or full spectrum objects embedded
- Spectrum files are in proprietary binary formats not supported by spectrum file loaders (use format conversion first)
- PSM file has already undergone FDR filtering; MS²Rescore requires all target and decoy PSMs without FDR pre-filtering

## Inputs

- PSM file from proteomics search engine (CSV, TSV, mzID, MSF, XML, or other psm_utils-supported format) containing spectrum_id field
- Spectrum file in mzML or MGF format with spectrum titles/identifiers
- Regex pattern string for PSM spectrum identifier extraction (psm_id_pattern)
- Regex pattern string for spectrum file identifier extraction (spectrum_id_pattern)

## Outputs

- PSM-to-spectrum mapping table or data structure linking each PSM to matched spectrum
- List or report of unmatched PSMs (flagged for error investigation)
- Validation summary: count of linked PSMs, unlinked PSMs, and any identifier collisions

## How to apply

First, design two regex patterns with at least one capturing group each: one (spectrum_id_pattern) to extract identifiers from spectrum file titles, and one (psm_id_pattern) to extract identifiers from the PSM file's spectrum_id field. Load the PSM file and apply psm_id_pattern to isolate the scan number or index from each PSM record. Load the spectrum file (mzML or MGF) and apply spectrum_id_pattern to extract identifiers from spectrum titles. Match extracted PSM identifiers to spectrum identifiers using string equality to establish the linking. Generate a mapping table or data structure linking each PSM to its matched spectrum, and flag any unmatched PSMs for error reporting. Validate that the number of linked PSMs is consistent with expectations and that no identifiers are duplicated or lost during extraction.

## Related tools

- **MS²Rescore** (Orchestrates PSM-to-spectrum linking validation as a prerequisite step before feature generation and rescoring) — https://github.com/compomics/ms2rescore
- **psm_utils** (Provides parsers for multiple PSM file formats and abstractions for uniform spectrum_id extraction) — https://github.com/compomics/ms2rescore

## Evaluation signals

- All PSMs in the input file have a match in the spectrum file (0% unlinked PSMs, or unlinked count is explicitly documented and justified)
- No duplicate mappings exist: each PSM maps to exactly one spectrum, and each spectrum is matched by the correct PSM records
- Regex capture groups correctly isolate scan numbers or indices; spot-check extracted identifiers from 5–10 random PSM and spectrum records
- Mapping table schema is consistent: columns/fields for PSM_id, spectrum_id, and optional confidence/score are present and non-null
- String equality validation passes: extracted PSM identifiers and extracted spectrum identifiers match character-for-character for all linked pairs

## Limitations

- Regex patterns must be manually designed and validated for each search engine and spectrum format combination; no universal pattern exists
- If spectrum files are in proprietary Bruker .d format, use TIMS²Rescore with timsrust library; standard mzML/MGF parsers will not work
- Unmatched PSMs are not automatically recovered; if a regex pattern is too strict or too loose, manual inspection and pattern refinement is required
- MS²Rescore requires all target and decoy PSMs without FDR pre-filtering; if input PSM file is already FDR-filtered, rescoring results may be biased

## Evidence

- [intro] Essential for MS²Rescore to function correctly is linking the search engine PSMs to the original spectra...two options are available to map PSMs to spectra: ``spectrum_id_pattern`` and: "Essential for MS²Rescore to function correctly is linking the search engine PSMs to the original spectra...two options are available to map PSMs to spectra: ``spectrum_id_pattern`` and"
- [other] MS²Rescore uses two regex patterns with single capture groups—``spectrum_id_pattern`` to extract identifiers from spectrum file titles and ``psm_id_pattern`` to extract identifiers from PSM file spectrum_id fields—that must match the entire string and return the same identifier to link PSMs to spectra.: "MS²Rescore uses two regex patterns with single capture groups—``spectrum_id_pattern`` to extract identifiers from spectrum file titles and ``psm_id_pattern`` to extract identifiers from PSM file"
- [other] Load PSM file and extract spectrum identifiers using the psm_id_pattern regex with at least one capturing group to isolate the scan number or index. 2. Load spectrum file (mzML or MGF format) and extract spectrum identifiers from spectrum titles using the spectrum_id_pattern regex with at least one capturing group. 3. Match extracted PSM identifiers to spectrum identifiers using string equality to establish the PSM-to-spectrum mapping.: "Load PSM file and extract spectrum identifiers using the psm_id_pattern regex with at least one capturing group to isolate the scan number or index. 2. Load spectrum file (mzML or MGF format) and"
- [intro] Both ``mzML`` and ``mgf`` formats are supported: "Both ``mzML`` and ``mgf`` formats are supported"
- [readme] MS²Rescore can read peptide identifications in any format supported by [psm_utils] (see [Supported file formats]) and has been tested with various search engines output files: "MS²Rescore can read peptide identifications in any format supported by [psm_utils] (see [Supported file formats]) and has been tested with various search engines output files"
