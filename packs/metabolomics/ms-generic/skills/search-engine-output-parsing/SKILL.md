---
name: search-engine-output-parsing
description: Use when you have PSM output files from one or more search engines (e.g., MaxQuant msms.txt, MSGFPlus .mzid, Sage .sage.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - psm_utils
  - MS²Rescore
  techniques:
  - mass-spectrometry
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

# search-engine-output-parsing

## Summary

Parse and standardize peptide-spectrum match (PSM) files from multiple proteomics search engines (MaxQuant, MSGFPlus, Sage, etc.) into a unified format with mapped modification notation and linked spectrum identifiers. This skill is essential for downstream rescoring pipelines that require canonical, cross-engine-compatible PSM representations.

## When to use

You have PSM output files from one or more search engines (e.g., MaxQuant msms.txt, MSGFPlus .mzid, Sage .sage.tsv) and need to (1) extract all putative identifications without FDR filtering, (2) convert search-engine-specific modification labels to HUPO-PSI ProForma v2 notation, and (3) link PSMs to their corresponding spectrum files using regex-based spectrum ID matching before rescoring or feature generation.

## When NOT to use

- PSM file has already been FDR-filtered or contains only high-confidence identifications — MS²Rescore requires all target and decoy PSMs without FDR filtering.
- Spectrum files are unavailable and spectrum_id_pattern / psm_id_pattern cannot be reliably matched — PSM-to-spectrum linking will fail.
- modification_mapping configuration is incomplete or unmaintained for your search engine — unmapped modification labels will cause ProForma validation errors or be silently dropped.

## Inputs

- PSM file (any format supported by psm_utils: MaxQuant msms.txt, MSGFPlus .mzid, Sage .sage.tsv, PeptideShaker .mzid, ProteomeDiscoverer .msf, Mascot .mzid, MS Amanda .csv, X!Tandem .xml, PEAKS .mzid)
- Spectrum file (mzML or mgf format)
- modification_mapping configuration (JSON/TOML object mapping search-engine labels to ProForma labels)
- spectrum_id_pattern regex (with ≥1 capturing group)
- psm_id_pattern regex (with ≥1 capturing group)
- fixed_modifications configuration (optional; maps amino acids to modification names for modifications not in PSM file)

## Outputs

- Standardized PSM records with ProForma-formatted modification notation
- PSM-to-spectrum mapping table (linking each PSM to matched spectrum by identifier)
- Unified PSM data structure (e.g., pandas DataFrame or psm_utils PSMList) compatible with downstream rescoring
- Validation report flagging unmatched PSMs or invalid ProForma conversions

## How to apply

Load the PSM file using psm_utils, which abstracts format differences across search engines. Extract spectrum identifiers from PSM records using the psm_id_pattern regex (with at least one capturing group to isolate scan number or index), and extract matching identifiers from spectrum file titles using spectrum_id_pattern. Apply the modification_mapping configuration to replace each search-engine-specific modification label (e.g., 'ox', '+57.02146', or mass-shift notation) with its ProForma-compatible equivalent (e.g., 'U:Oxidation'), selecting from five accepted formats: PSI-MOD accession, PSI-MOD name, Unimod accession, Unimod name, or chemical formula (e.g., 'Formula:HO3P'). Validate that all mapped labels conform to ProForma v2 and are recognized by psm_utils. Link each PSM to its spectrum by string equality of extracted identifiers, flagging unmatched PSMs for error reporting. Retain all target and decoy PSMs without FDR filtering, and separately configure any fixed modifications not reported in the PSM file itself.

## Related tools

- **psm_utils** (Abstracts PSM file format parsing across multiple search engines; validates and converts modification labels to ProForma notation)
- **MS²Rescore** (Orchestrates the end-to-end workflow; applies modification_mapping and spectrum_id_pattern configuration to standardize PSM input before rescoring) — https://github.com/compomics/ms2rescore

## Evaluation signals

- All PSM records contain valid ProForma-formatted modification notation with no unmapped modification labels present.
- String equality check: extracted psm_id_pattern identifiers match extracted spectrum_id_pattern identifiers for all PSMs; unmatched PSMs are flagged and reported.
- Modification mapping is bidirectional-traceable: each search-engine label in modification_mapping has a corresponding ProForma label in one of five accepted formats (PSI-MOD accession/name, Unimod accession/name, or chemical formula).
- Retained PSM count = input PSM count; all target and decoy PSMs are present (no FDR filtering applied during parsing).
- Output PSM data structure is accepted by downstream feature generators (e.g., MS²PIP, DeepLC) and rescoring engines (Percolator, Mokapot) without format errors.

## Limitations

- Some search engines (e.g., MaxQuant) do not report fixed modifications in the PSM file; these must be configured separately via fixed_modifications to avoid loss of modification information in ProForma output.
- regex patterns (spectrum_id_pattern, psm_id_pattern) must match the entire spectrum title or PSM spectrum_id field; complex or non-standard identifier formats may require custom regex patterns that are error-prone and user-dependent.
- ProForma notation depends on availability of modifications in controlled vocabularies (Unimod, PSI-MOD); novel or undocumented modifications may only be representable as chemical formulas, which carry higher ambiguity.
- Decoy PSM identification relies on regex pattern (id_decoy_pattern) or protein name prefix (e.g., 'DECOY_'); misconfigurations result in incorrect FDR control downstream.

## Evidence

- [intro] most PSM file types coming from different proteomics search engines use a custom modification notation...Therefore, ``ox`` needs to be mapped to ``U:Oxidation``: "most PSM file types coming from different proteomics search engines use a custom modification notation...Therefore, ``ox`` needs to be mapped to ``U:Oxidation``"
- [intro] MS²Rescore uses the `HUPO-PSI standardized ProForma v2 notation` to represent modified peptides...requires a configuration :py:obj:`modification_mapping` which maps each specific search engine: "MS²Rescore uses the `HUPO-PSI standardized ProForma v2 notation` to represent modified peptides...requires a configuration :py:obj:`modification_mapping` which maps each specific search engine"
- [intro] MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
- [other] modification_mapping as a configuration object that maps search-engine-specific modification labels to ProForma labels in five accepted formats: PSI-MOD accession, PSI-MOD name, Unimod accession, Unimod name, or chemical formula (e.g., 'Formula:HO3P'): "modification_mapping as a configuration object that maps search-engine-specific modification labels to ProForma labels in five accepted formats: PSI-MOD accession, PSI-MOD name, Unimod accession,"
- [other] two regex patterns with single capture groups—``spectrum_id_pattern`` to extract identifiers from spectrum file titles and ``psm_id_pattern`` to extract identifiers from PSM file spectrum_id fields—that must match the entire string and return the same identifier to link PSMs to spectra: "two regex patterns with single capture groups—``spectrum_id_pattern`` to extract identifiers from spectrum file titles and ``psm_id_pattern`` to extract identifiers from PSM file spectrum_id"
- [intro] fixed modifications that are not reported in the PSM file must be configured separately: "fixed modifications that are not reported in the PSM file must be configured separately"
- [intro] Both ``mzML`` and ``mgf`` formats are supported: "Both ``mzML`` and ``mgf`` formats are supported"
- [readme] MS²Rescore can read peptide identifications in any format supported by [psm_utils] (see [Supported file formats]) and has been tested with various search engines output files: [MS Amanda, Sage, PeptideShaker, ProteomeDiscoverer, MSGFPlus, Mascot, MaxQuant, X!Tandem, PEAKS]: "MS²Rescore can read peptide identifications in any format supported by [psm_utils] and has been tested with various search engines output files: MS Amanda .csv, Sage .sage.tsv, PeptideShaker .mzid,"
