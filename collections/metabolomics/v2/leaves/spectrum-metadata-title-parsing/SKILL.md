---
name: spectrum-metadata-title-parsing
description: Use when when you have PSM files from a search engine (e.g., MaxQuant,
  MSGFPlus, Mascot) and corresponding spectrum files in mzML or MGF format, and the
  spectrum identifiers in both files use different naming conventions or formats.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS²Rescore
  - psm_utils
  techniques:
  - mass-spectrometry
  license_tier: open
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

# spectrum-metadata-title-parsing

## Summary

Extract spectrum identifiers from spectrum file titles (mzML or MGF format) using regex capture groups to enable PSM-to-spectrum matching in MS²Rescore. This skill bridges the gap between search engine PSM outputs and raw mass spectrometry data by reliably linking each peptide identification to its originating spectrum.

## When to use

When you have PSM files from a search engine (e.g., MaxQuant, MSGFPlus, Mascot) and corresponding spectrum files in mzML or MGF format, and the spectrum identifiers in both files use different naming conventions or formats. This is required before PSM rescoring in MS²Rescore, particularly when spectrum titles contain scan numbers, indices, or other metadata that must be extracted and matched to PSM spectrum_id fields.

## When NOT to use

- Spectrum identifiers already match PSM identifiers without transformation—skip regex extraction and use direct string matching instead
- Spectrum files are in unsupported formats (neither mzML nor MGF)—no extraction mechanism is available in MS²Rescore
- Spectrum files lack consistent metadata structure in titles (e.g., scan numbers embedded in inconsistent positions or mixed formats)—regex patterns will fail or require excessive refinement

## Inputs

- spectrum file in mzML format with embedded scan numbers or indices in spectrum titles
- spectrum file in MGF format with embedded scan numbers or indices in spectrum titles
- regex pattern string with at least one capturing group (spectrum_id_pattern parameter)

## Outputs

- spectrum identifier lookup table (mapping from captured identifier to spectrum metadata)
- list of extracted spectrum identifiers ready for matching to PSM identifiers
- list of unmatched or malformed spectrum titles (for error reporting)

## How to apply

Define a regex pattern with at least one capturing group (spectrum_id_pattern) that matches and extracts the identifier portion from spectrum file titles—typically a scan number or index embedded in the title string. Load the spectrum file (mzML or MGF) and apply this pattern to each spectrum title to isolate the identifier. The pattern must match the entire spectrum title string and return a single, unambiguous captured group per spectrum. Store the extracted identifiers in a lookup table indexed by the captured identifier value. When matching PSMs (which have already been processed with psm_id_pattern), compare the PSM-extracted identifier to this spectrum identifier lookup using string equality. Document the regex pattern in the MS²Rescore configuration file under the spectrum_id_pattern parameter. Any spectrum titles that do not match the pattern should be flagged for manual inspection, as they indicate either misconfigured regex patterns or malformed spectrum file metadata.

## Related tools

- **MS²Rescore** (main orchestration platform that performs PSM-to-spectrum linking via spectrum_id_pattern regex) — https://github.com/compomics/ms2rescore
- **psm_utils** (PSM file parser that reads and standardizes PSM inputs before spectrum matching) — https://github.com/compomics/ms2rescore

## Evaluation signals

- Each extracted spectrum identifier appears exactly once in the lookup table (no duplicates within a single spectrum file)
- All spectrum titles matching the regex pattern yield a single, non-empty captured group per title
- String equality comparison of matched PSM identifiers (via psm_id_pattern) to extracted spectrum identifiers produces a 1:1 or N:1 mapping (multiple PSMs per spectrum is allowed; zero or multiple spectra per PSM indicates misconfiguration)
- Unmatched PSMs (those whose identifiers do not appear in the spectrum identifier table) are correctly flagged and reported before rescoring begins
- The number of successful PSM-to-spectrum links is consistent with the total number of unique PSMs in the input file (accounting for multiple ranks per spectrum)

## Limitations

- Regex patterns are brittle: spectrum title formats must be consistent across the entire file, or the pattern will fail silently on malformed titles and produce incomplete mappings
- The regex pattern must match the *entire* spectrum title string; partial matches do not trigger errors but yield incorrect captures if the group is positioned incorrectly
- If spectrum identifiers are non-unique (e.g., multiple spectra with the same scan number in different runs), the lookup table will overwrite earlier entries, causing silent data loss
- MS²Rescore requires access to *all* target and decoy PSMs without FDR-filtering; if the PSM file is pre-filtered, spectrum identifiers for filtered-out PSMs will not be extracted, leading to incomplete spectrum-to-PSM coverage
- mzML and MGF formats store spectrum metadata differently; the same regex pattern may not work for both file types, requiring format-specific patterns or manual pattern refinement

## Evidence

- [other] MS²Rescore uses two regex patterns with single capture groups—``spectrum_id_pattern`` to extract identifiers from spectrum file titles and ``psm_id_pattern`` to extract identifiers from PSM file spectrum_id fields—that must match the entire string and return the same identifier to link PSMs to spectra.: "MS²Rescore uses two regex patterns with single capture groups—``spectrum_id_pattern`` to extract identifiers from spectrum file titles and ``psm_id_pattern`` to extract identifiers from PSM file"
- [other] Load spectrum file (mzML or MGF format) and extract spectrum identifiers from spectrum titles using the spectrum_id_pattern regex with at least one capturing group.: "Load spectrum file (mzML or MGF format) and extract spectrum identifiers from spectrum titles using the spectrum_id_pattern regex with at least one capturing group."
- [intro] Both ``mzML`` and ``mgf`` formats are supported: "Both ``mzML`` and ``mgf`` formats are supported"
- [intro] Essential for MS²Rescore to function correctly is linking the search engine PSMs to the original spectra...two options are available to map PSMs to spectra: ``spectrum_id_pattern`` and: "Essential for MS²Rescore to function correctly is linking the search engine PSMs to the original spectra...two options are available to map PSMs to spectra: ``spectrum_id_pattern`` and"
- [intro] MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
