---
name: proforma-notation-parsing
description: Use when when peptide identifications from a search engine (MaxQuant, MSGFPlus, Sage, etc.) contain custom or engine-specific modification notation that must be converted to a standardized format before rescoring, or when different search engines use incompatible modification label schemes that.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS²Rescore
  - psm_utils
  - Unimod
  - PSI-MOD
  - HUPO-PSI/ProForma
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

# proforma-notation-parsing

## Summary

Parsing and standardization of modified peptide sequences into HUPO-PSI ProForma v2 notation, which unifies search-engine-specific modification labels (e.g., MaxQuant 'ox', mass shifts) into controlled-vocabulary identifiers (Unimod, PSI-MOD, or chemical formulas) for downstream MS²Rescore rescoring and feature generation.

## When to use

When peptide identifications from a search engine (MaxQuant, MSGFPlus, Sage, etc.) contain custom or engine-specific modification notation that must be converted to a standardized format before rescoring, or when different search engines use incompatible modification label schemes that need unification for joint analysis or cross-tool compatibility.

## When NOT to use

- PSM files already encoded in standardized ProForma notation (no remapping needed)
- Modifications that are absent from all five controlled vocabularies and cannot be expressed as chemical formulas (unless custom formula mapping is explicitly documented)
- Search engines that do not report any modifications in the PSM file (use fixed_modifications configuration instead)

## Inputs

- PSM file from search engine (MaxQuant msms.txt, MSGFPlus .mzid, Sage .sage.tsv, or other format supported by psm_utils)
- Modification mapping configuration (TOML or JSON file with search-engine label → ProForma label mappings)
- Peptide sequences with search-engine-specific modification notation

## Outputs

- PSM records with peptide sequences remapped to ProForma v2 notation
- Annotated PSM object or intermediate file with standardized modification labels
- Validation report confirming all labels conform to HUPO-PSI ProForma v2

## How to apply

Load the PSM file and extract modification labels as they appear in the search engine output (e.g., 'ox', '+15.9949', or mass-shift notation). Read the modification_mapping configuration from a TOML/JSON file, where each search-engine label is explicitly mapped to a ProForma-compatible label in one of five accepted formats: PSI-MOD accession, PSI-MOD name, Unimod accession, Unimod name, or chemical formula (e.g., 'Formula:HO3P'). For each PSM, iterate through its peptide sequence and replace each search-engine modification label with its corresponding ProForma label using the mapping dictionary. Validate that all mapped labels conform to HUPO-PSI ProForma v2 notation and are recognized by psm_utils. Write or update the PSM record with the remapped peptide sequences, preserving all other PSM fields and metadata.

## Related tools

- **psm_utils** (Parsing and validation of PSM files in multiple formats; acceptance and validation of ProForma-compliant modification labels)
- **MS²Rescore** (Rescoring engine that consumes ProForma-normalized PSM records; uses standardized modification notation for feature generation and rescoring) — https://github.com/compomics/ms2rescore
- **Unimod** (Controlled vocabulary for UniMod accessions and names used in ProForma label mapping (e.g., 'U:Oxidation'))
- **PSI-MOD** (Controlled vocabulary for PSI-MOD accessions and names used in ProForma label mapping)
- **HUPO-PSI/ProForma** (Standard notation specification defining syntax and validation rules for ProForma v2 modification labels) — https://github.com/HUPO-PSI/ProForma

## Evaluation signals

- All search-engine modification labels in the input PSM file are successfully matched against the modification_mapping dictionary with zero unmapped labels reported
- Output PSM records conform to HUPO-PSI ProForma v2 syntax when parsed by psm_utils (no validation errors)
- Each mapped ProForma label is expressed in one of the five accepted formats: PSI-MOD accession (e.g., MOD:00696), PSI-MOD name (e.g., Oxidation), Unimod accession (e.g., U:1), Unimod name (e.g., U:Oxidation), or chemical formula (e.g., Formula:HO3P)
- Spot-check: a sample of 10+ PSMs shows correct 1:1 mapping of input labels to output ProForma labels (e.g., MaxQuant 'ox' → 'U:Oxidation', 'gl' → 'U:Gln->pyro-Glu')
- All non-modification fields in the PSM record (scan number, spectrum ID, peptide sequence backbone, charge, m/z, RT) are preserved unchanged in the output

## Limitations

- Modification mapping is search-engine-specific and must be manually curated per search engine; no automatic detection of unmapped labels across engines
- Chemical formula notation is recommended only for modifications absent from Unimod and PSI-MOD controlled vocabularies; mass-shift-only modifications may not be fully portable across tools
- ProForma notation supports a fixed set of syntax rules (e.g., square brackets for position-specific modifications); non-standard or proprietary search-engine notation (e.g., Mascot-specific mass deltas) may require custom pre-processing before mapping
- Fixed modifications not reported in the PSM file must be added via a separate fixed_modifications configuration; this skill only remaps labels already present in the input

## Evidence

- [other] MS²Rescore implements modification_mapping as a configuration object that maps search-engine-specific modification labels to ProForma labels in five accepted formats: PSI-MOD accession, PSI-MOD name, Unimod accession, Unimod name, or chemical formula (e.g., 'Formula:HO3P').: "MS²Rescore implements modification_mapping as a configuration object that maps search-engine-specific modification labels to ProForma labels in five accepted formats: PSI-MOD accession, PSI-MOD name,"
- [intro] MS²Rescore requires mapping of search engine modification labels to ProForma notation; most PSM file types coming from different proteomics search engines use a custom modification notation...Therefore, 'ox' needs to be mapped to 'U:Oxidation': "most PSM file types coming from different proteomics search engines use a custom modification notation...Therefore, ``ox`` needs to be mapped to ``U:Oxidation``"
- [other] 1. Load the PSM file and extract modification labels as they appear in the search engine output (e.g., 'ox', '+57.02146', or mass-shift notation). 2. Read the modification_mapping configuration from the TOML/JSON file, where each search-engine label is mapped to a ProForma-compatible label. 3. For each PSM, iterate through its peptide sequence and replace each search-engine modification label with its corresponding ProForma label using the mapping dictionary. 4. Validate that all mapped labels conform to HUPO-PSI ProForma v2 notation and are recognized by psm_utils.: "Load the PSM file and extract modification labels as they appear in the search engine output (e.g., 'ox', '+57.02146', or mass-shift notation). 2. Read the modification_mapping configuration from the"
- [intro] MS²Rescore uses the `HUPO-PSI standardized ProForma v2 notation` to represent modified peptides...requires a configuration :py:obj:`modification_mapping` which maps each specific search engine: "MS²Rescore uses the `HUPO-PSI standardized ProForma v2 notation` to represent modified peptides...requires a configuration :py:obj:`modification_mapping` which maps each specific search engine"
- [readme] Protein and peptide sequences are usually represented using a string of amino acids using a well-known one letter code endorsed by the IUPAC. However, there is still no clear consensus about how to represent 'proteoforms' and 'peptidoforms'... A standard notation for proteoforms and peptidoforms is then required for the community: "A standard notation for proteoforms and peptidoforms is then required for the community, so that it can be embedded in many relevant PSI (and potentially other) file formats."
