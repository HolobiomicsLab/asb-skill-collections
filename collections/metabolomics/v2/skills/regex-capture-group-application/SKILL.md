---
name: regex-capture-group-application
description: Use when when you have PSM files (output from search engines like MaxQuant, MSGFPlus, or Sage) and spectrum files in mzML or MGF format with non-trivial or inconsistent naming schemes, and you need to establish which PSMs correspond to which spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS²Rescore
  - psm_utils
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# regex-capture-group-application

## Summary

Apply regex capture groups to extract spectrum identifiers from both PSM file spectrum_id fields and spectrum file titles, then match the extracted identifiers to establish PSM-to-spectrum linkage. This is essential for MS²Rescore to correctly associate peptide-spectrum matches with their corresponding mass spectrometry data.

## When to use

When you have PSM files (output from search engines like MaxQuant, MSGFPlus, or Sage) and spectrum files in mzML or MGF format with non-trivial or inconsistent naming schemes, and you need to establish which PSMs correspond to which spectra. Specifically, when the spectrum identifier in the PSM file does not exactly match the spectrum title in the spectrum file, requiring pattern-based extraction and normalization to create the mapping.

## When NOT to use

- Spectrum identifiers in the PSM file and spectrum file already match exactly without transformation — use direct string matching instead.
- Spectrum files are not available or not required for your analysis (e.g., if you are only performing rescoring with predicted spectra that do not depend on raw spectrum identifiers).
- The spectrum identifier format is fundamentally ambiguous or non-deterministic (e.g., multiple spectra with identical extracted identifiers after regex application), as this will lead to incorrect or duplicate mappings.

## Inputs

- PSM file (TSV, CSV, mzID, or other format supported by psm_utils) with spectrum_id field
- Spectrum file in mzML or MGF format with spectrum title/identifier metadata
- regex pattern string for spectrum_id_pattern (with at least one capturing group)
- regex pattern string for psm_id_pattern (with at least one capturing group)

## Outputs

- PSM-to-spectrum mapping table or data structure (e.g., dictionary keyed by PSM identifier with spectrum reference)
- List or report of unmatched PSMs (PSMs with no corresponding spectrum in the spectrum file)
- Validation summary indicating the number of successful matches and any mapping failures

## How to apply

Design two regex patterns, each with at least one capturing group: `spectrum_id_pattern` to extract identifiers from spectrum file titles (mzML or MGF), and `psm_id_pattern` to extract identifiers from PSM file spectrum_id fields. Both patterns must match the entire string and isolate the same identifier type (scan number, index, or filename component). Load the PSM file and apply `psm_id_pattern` to each spectrum_id field to extract the normalized identifier; load the spectrum file and apply `spectrum_id_pattern` to each spectrum title to extract the normalized identifier. Match extracted PSM identifiers to spectrum identifiers using string equality, building a mapping table that links each PSM row to its corresponding spectrum. Flag any PSMs without a matched spectrum for error reporting, as unmatched PSMs cannot be rescored.

## Related tools

- **MS²Rescore** (Orchestrates PSM-to-spectrum mapping via spectrum_id_pattern and psm_id_pattern configuration; requires correct mapping to enable feature generation and rescoring) — https://github.com/compomics/ms2rescore
- **psm_utils** (Parses PSM files in multiple formats (mzID, TSV, CSV, etc.) and exposes spectrum_id fields for regex-based extraction)

## Evaluation signals

- 100% of PSMs in the input file are matched to a spectrum (no unmatched PSM report, or unmatched count is zero and documented).
- Spot-check: manually verify 5–10 regex-extracted identifiers from both PSM and spectrum files match exactly and correspond to the correct experimental scan or spectrum.
- Verify that the regex patterns match the entire spectrum identifier string (not partial matches) and do not collide (i.e., two different spectra do not extract to the same identifier).
- Output mapping table is consistent with input PSM count and spectrum file content (e.g., one row per PSM, referencing valid spectrum identifiers).
- Downstream rescoring or feature generation succeeds without 'spectrum not found' errors, indicating mapping was correct.

## Limitations

- Regex patterns must be carefully designed and validated; incorrect patterns will silently produce incomplete or incorrect mappings, leading to loss of PSMs or false associations.
- If multiple spectra extract to the same identifier (ambiguous mapping), the regex approach cannot resolve the ambiguity; manual intervention or data curation is required.
- Spectrum file format variations (e.g., different mzML namespaces or MGF header formats) may require multiple regex patterns or format-specific preprocessing.
- Performance may degrade with very large spectrum files (millions of spectra) if regex matching is not optimized; batch processing or indexing may be needed.

## Evidence

- [other] MS²Rescore uses two regex patterns with single capture groups—`spectrum_id_pattern` to extract identifiers from spectrum file titles and `psm_id_pattern` to extract identifiers from PSM file spectrum_id fields—that must match the entire string and return the same identifier to link PSMs to spectra.: "two regex patterns with single capture groups—``spectrum_id_pattern`` to extract identifiers from spectrum file titles and ``psm_id_pattern`` to extract identifiers from PSM file spectrum_id"
- [intro] Essential for MS²Rescore to function correctly is linking the search engine PSMs to the original spectra using spectrum_id_pattern and psm_id_pattern.: "Essential for MS²Rescore to function correctly is linking the search engine PSMs to the original spectra...two options are available to map PSMs to spectra: ``spectrum_id_pattern`` and"
- [other] Load PSM file and extract spectrum identifiers using the psm_id_pattern regex with at least one capturing group to isolate the scan number or index.: "Load PSM file and extract spectrum identifiers using the psm_id_pattern regex with at least one capturing group to isolate the scan number or index."
- [other] Load spectrum file (mzML or MGF format) and extract spectrum identifiers from spectrum titles using the spectrum_id_pattern regex with at least one capturing group.: "Load spectrum file (mzML or MGF format) and extract spectrum identifiers from spectrum titles using the spectrum_id_pattern regex with at least one capturing group."
- [other] Match extracted PSM identifiers to spectrum identifiers using string equality to establish the PSM-to-spectrum mapping.: "Match extracted PSM identifiers to spectrum identifiers using string equality to establish the PSM-to-spectrum mapping."
- [intro] Both mzML and mgf formats are supported by MS²Rescore for spectrum input.: "Both ``mzML`` and ``mgf`` formats are supported"
