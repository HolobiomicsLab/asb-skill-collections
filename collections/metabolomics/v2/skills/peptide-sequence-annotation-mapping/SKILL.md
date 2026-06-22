---
name: peptide-sequence-annotation-mapping
description: 'Use when you have PSM files from a proteomics search engine (e.g., MaxQuant, MSGFPlus, MS Amanda) and need to convert their native modification notation into HUPO-PSI ProForma v2 format before rescoring. Specifically, use it when: (1) search engines report modifications with custom labels (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - psm_utils
  - MS²Rescore
  - DeepLC
  - Percolator
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

# Peptide Sequence Annotation Mapping

## Summary

Maps search-engine-specific modification labels and fixed modifications onto peptide sequences using standardized ProForma notation. This skill ensures that all peptide modifications—whether variable modifications from search results or unreported fixed modifications—are represented in a common format compatible with downstream rescoring and feature generation tools.

## When to use

Apply this skill when you have PSM files from a proteomics search engine (e.g., MaxQuant, MSGFPlus, MS Amanda) and need to convert their native modification notation into HUPO-PSI ProForma v2 format before rescoring. Specifically, use it when: (1) search engines report modifications with custom labels (e.g., 'ox', 'gl', '+57.02146') that must map to standardized ProForma labels (e.g., 'U:Oxidation', 'U:Gln->pyro-Glu'), and/or (2) fixed modifications configured in the search engine (e.g., carbamidomethylation on cysteines, TMT labeling on lysines and N-terminus) are not explicitly recorded in the PSM file and must be injected before rescoring.

## When NOT to use

- PSM file already contains all modifications in valid ProForma notation and no fixed modifications are missing—skip mapping and proceed directly to rescoring.
- Search engine output does not include modification information or spectrum matching details (e.g., raw spectrum file only)—you must first run a proteomics search engine.
- Input is a pre-processed feature table or a rescored PSM file already in final format—re-mapping would redundantly process already-normalized data.

## Inputs

- PSM file(s) from search engine (supported formats: MaxQuant msms.txt, MSGFPlus .mzid, MS Amanda .csv, Sage .sage.tsv, X!Tandem .xml, etc.)
- modification_mapping configuration (TOML or JSON file mapping search-engine labels to ProForma labels)
- fixed_modifications configuration (TOML or JSON file mapping amino acids and terminal positions to ProForma modification names)

## Outputs

- Annotated PSM file with ProForma-formatted peptide sequences
- PSM records with both variable and fixed modifications represented in standardized notation
- Intermediate or final PSM file suitable for downstream feature generation and rescoring

## How to apply

Load the PSM file and extract modification labels exactly as they appear in search engine output. Read the modification_mapping configuration (from TOML or JSON file) where each search-engine label is mapped to a ProForma-compatible label in one of five formats: PSI-MOD accession, PSI-MOD name, Unimod accession, Unimod name, or chemical formula (e.g., 'Formula:HO3P'). For each PSM, iterate through its peptide sequence and replace search-engine labels with their corresponding ProForma labels using the mapping dictionary. Simultaneously, apply fixed_modifications by inserting ProForma modification labels at specified residue positions (including terminal positions N-term and C-term) if not already present. Validate that all mapped labels conform to ProForma v2 notation and are recognized by psm_utils. Write the annotated PSM records with remapped peptide sequences back to output, preserving all other PSM fields.

## Related tools

- **MS²Rescore** (Main rescoring platform that consumes modification-mapped PSM files and uses ProForma notation throughout the rescoring pipeline) — https://github.com/compomics/ms2rescore
- **psm_utils** (Library for parsing and validating PSM files and ensuring ProForma modification labels conform to HUPO-PSI ProForma v2 specification)
- **DeepLC** (Feature generator that requires modification formula notation; benefits from accurate ProForma mapping to extract chemical composition)
- **Percolator** (Downstream rescoring engine that accepts PSMs with ProForma-formatted sequences as input for machine-learning-driven rescoring) — https://github.com/percolator/percolator

## Evaluation signals

- All search-engine modification labels in input PSM file are successfully mapped to corresponding ProForma labels in output; verify by spot-checking PSM records before and after mapping.
- Fixed modifications are present at all expected residue positions (all cysteines have 'U:Carbamidomethyl' if configured, all lysines and N-terminus have 'U:TMT6plex' if configured, etc.) without duplication of already-reported modifications.
- Output PSM records validate without error when parsed by psm_utils ProForma validator; conformance check can be performed via psm_utils library or command-line tools.
- No loss or corruption of other PSM fields (spectrum ID, peptide sequence, scan number, search engine score, protein accession) during the mapping process.
- Downstream feature generators (e.g., DeepLC) and rescoring engines (Percolator, Mokapot) accept the output PSM file without modification notation errors or schema violations.

## Limitations

- Modification mapping requires manual curation of a configuration file; if a search engine uses an undocumented or ambiguous modification label not present in the mapping dictionary, the label will not be converted and may cause downstream failures.
- Fixed modifications are specified globally for all peptides; if a subset of peptides should not receive a particular fixed modification due to experimental design (e.g., some samples lack TMT labeling), this skill cannot selectively apply modifications—the configuration must be adjusted or PSM file pre-filtered.
- Formula-based notation (e.g., 'Formula:HO3P') is preferred over mass shifts for modifications not in controlled vocabularies (Unimod, PSI-MOD), but this requires knowledge of chemical composition; if formula is incorrect or unavailable, mapping may fail or produce ambiguous ProForma labels.
- This skill requires access to all target and decoy PSMs without FDR-filtering; pre-filtered PSM files (e.g., only top-ranked or FDR-filtered identifications) will result in incomplete or biased modification annotation across the dataset.

## Evidence

- [intro] MS²Rescore implements modification_mapping as a configuration object that maps search-engine-specific modification labels to ProForma labels in five accepted formats: PSI-MOD accession, PSI-MOD name, Unimod accession, Unimod name, or chemical formula (e.g., 'Formula:HO3P'). For example, MaxQuant's 'ox' label maps to 'U:Oxidation', and 'gl' maps to 'U:Gln->pyro-Glu'.: "MS²Rescore implements modification_mapping as a configuration object that maps search-engine-specific modification labels to ProForma labels in five accepted formats: PSI-MOD accession, PSI-MOD name,"
- [intro] Fixed modifications are configured through a mapping that associates ProForma modification labels (e.g., U:Carbamidomethyl, U:TMT6plex) with lists of residue target positions, including special labels N-term and C-term for terminal modifications.: "Fixed modifications are configured through a mapping that associates ProForma modification labels (e.g., U:Carbamidomethyl, U:TMT6plex) with lists of residue target positions, including special"
- [intro] MS²Rescore uses the `HUPO-PSI standardized ProForma v2 notation` to represent modified peptides...requires a configuration :py:obj:`modification_mapping` which maps each specific search engine: "MS²Rescore uses the HUPO-PSI standardized ProForma v2 notation to represent modified peptides and requires a configuration modification_mapping which maps each specific search engine"
- [intro] most PSM file types coming from different proteomics search engines use a custom modification notation...Therefore, ``ox`` needs to be mapped to ``U:Oxidation``: "most PSM file types coming from different proteomics search engines use a custom modification notation...Therefore, ox needs to be mapped to U:Oxidation"
- [intro] Some search engines, such as MaxQuant, do not report fixed modifications: "Some search engines, such as MaxQuant, do not report fixed modifications"
- [intro] MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**: "MS²Rescore always needs access to all target and decoy PSMs, without any FDR-filtering"
