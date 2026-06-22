---
name: decoy-psm-identification-and-tagging
description: Use when ingesting PSM files from proteomics search engines (MS Amanda, MSGFPlus, MaxQuant, etc.) that contain a mixture of target and decoy PSMs, and you need to ensure accurate FDR calculation during or after rescoring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS²Rescore
  - psm_utils
  - Percolator
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

# decoy-psm-identification-and-tagging

## Summary

Identify and tag decoy peptide-spectrum matches (PSMs) in search engine output using regex patterns or protein name prefixes to enable correct false discovery rate (FDR) control during rescoring. This skill is essential for distinguishing target identifications from decoys before rank filtering and statistical validation.

## When to use

Apply this skill when ingesting PSM files from proteomics search engines (MS Amanda, MSGFPlus, MaxQuant, etc.) that contain a mixture of target and decoy PSMs, and you need to ensure accurate FDR calculation during or after rescoring. Decoy identification is a prerequisite for rank-based filtering (max_psm_rank_output) and FDR-based significance testing in MS²Rescore workflows.

## When NOT to use

- Input PSM file has already been FDR-filtered; MS²Rescore requires all target and decoy PSMs without FDR-filtering applied beforehand.
- Search engine output uses a non-standard or undocumented decoy naming scheme that cannot be reliably parsed by regex or prefix matching.
- PSM file contains only target PSMs or only decoy PSMs (no mix); decoy identification is meaningless without both populations.

## Inputs

- PSM file in psm_utils-supported format (TSV, mzID, CSV, msf, xml)
- Search engine output (MS Amanda, MSGFPlus, MaxQuant, Sage, Mascot, etc.)
- Regex pattern for decoy identification (id_decoy_pattern parameter)
- Protein name prefix convention (e.g., 'DECOY_')

## Outputs

- Annotated PSM table with decoy/target classification
- Parsed PSM objects (via psm_utils) with is_decoy flag set
- Stratified PSM sets ready for rank filtering and FDR calculation

## How to apply

Extract decoy PSM identifiers using one of two strategies: (1) apply a regex pattern (id_decoy_pattern) to match decoy annotations in PSM file fields, or (2) detect a protein name prefix convention (e.g., 'DECOY_') to flag decoy entries. This classification must occur during PSM file parsing before any rank-based filtering, so that downstream FDR calculations can correctly separate target from decoy PSMs. The choice of pattern depends on the search engine output format; for example, Percolator-compatible workflows often use a dedicated decoy label field, while concatenated target-decoy searches may embed 'DECOY_' in protein IDs. Correctly tagged decoys enable MS²Rescore to filter lower-ranking PSMs (controlled by max_psm_rank_output) while preserving FDR validity, since FDR is computed as (number of decoys passing threshold) / (number of targets passing threshold).

## Related tools

- **psm_utils** (Parses PSM files from heterogeneous search engines and provides standardized data structures for decoy tagging and classification)
- **MS²Rescore** (Consumes classified decoy/target PSMs and enforces FDR control during rescoring and output filtering using the decoy population) — https://github.com/compomics/ms2rescore
- **Percolator** (Downstream rescoring engine that relies on correctly identified decoy PSMs to compute q-values and FDR thresholds) — https://github.com/percolator/percolator

## Evaluation signals

- Decoy PSMs are correctly classified: verify by inspecting the parsed PSM objects or output TSV for is_decoy flag agreement with regex pattern or prefix rule.
- No false negatives in decoy detection: spot-check protein names in the input file against the regex pattern to confirm all decoys matching the convention are tagged.
- FDR values in downstream output are consistent with the decoy count: confirm that FDR = (# decoys above threshold) / (# targets above threshold) matches reported q-values.
- Stratification is preserved after rank filtering: verify that both decoy and target PSMs are retained and ranked independently per spectrum before max_psm_rank_output filtering.
- Output PSM table includes decoy/target annotation column: inspect the output TSV for a 'is_decoy' or equivalent column with boolean or binary values.

## Limitations

- Regex pattern must be carefully designed to avoid cross-matching target protein names that coincidentally contain the decoy substring; testing against real search engine output is critical.
- Some search engines (e.g., MaxQuant) may not report decoy annotations in all fields; manual configuration of the decoy pattern is often necessary.
- Concatenated target-decoy searches require the search engine to be run with appropriate flags (e.g., MSGFPlus with -addFeatures 1) to ensure decoys are present in the output file.
- Decoy identification relies on consistent naming conventions; if the search engine output or protein database changes the naming scheme between runs, the regex pattern may fail silently.

## Evidence

- [intro] Identify decoy PSMs using id_decoy_pattern or protein name prefix: "it can usually be derived from the protein name. For example, if the protein name contains the prefix ``DECOY_``, the PSM is a decoy PSM"
- [intro] Decoy identification is a prerequisite for FDR control: "To ensure a correct FDR control after rescoring, MS²Rescore filters out lower-ranking PSMs before final FDR calculation"
- [intro] MS²Rescore requires both target and decoy PSMs: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
- [methods] Decoy identification uses regex pattern parameter: "Regex pattern used to identify the decoy PSMs in identification file"
- [readme] Multiple search engine formats are supported: "MS²Rescore can read peptide identifications in any format supported by [psm_utils][psm_utils] (see [Supported file formats][file-formats]) and has been tested with various search engines output files"
