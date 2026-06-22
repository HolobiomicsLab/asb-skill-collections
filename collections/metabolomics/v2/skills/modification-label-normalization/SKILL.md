---
name: modification-label-normalization
description: Use when when PSM files from heterogeneous proteomics search engines (MaxQuant, MSGFPlus, Sage, X!Tandem, etc.) use inconsistent or proprietary modification notations that cannot be directly consumed by feature generators (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - psm_utils
  - MS²Rescore
  - MS²PIP
  - DeepLC
  - Percolator
  - Mokapot
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

# modification-label-normalization

## Summary

Convert search-engine-specific modification labels (e.g., MaxQuant 'ox', '+57.02146') into standardized HUPO-PSI ProForma v2 notation (e.g., 'U:Oxidation') using a configuration-driven mapping dictionary. This normalization is essential for downstream feature generation and rescoring in MS²Rescore, enabling cross-engine compatibility and standardized modification representation.

## When to use

When PSM files from heterogeneous proteomics search engines (MaxQuant, MSGFPlus, Sage, X!Tandem, etc.) use inconsistent or proprietary modification notations that cannot be directly consumed by feature generators (e.g., DeepLC, MS²PIP) or rescoring engines that require HUPO-PSI ProForma v2 compliance. Typically surfaced when loading raw PSM files into MS²Rescore before feature generation and rescoring.

## When NOT to use

- Input PSM file already contains HUPO-PSI ProForma v2 notation (e.g., from a prior MS²Rescore run or natively from psm_utils-compatible tools).
- PSM file has undergone strict FDR filtering before rescoring — MS²Rescore requires all target and decoy PSMs without FDR-filtering for accurate rescoring.
- Feature generators or rescoring engines being used do not require standardized modification notation (rare; most modern tools do require it).

## Inputs

- PSM file(s) from proteomics search engine (MaxQuant msms.txt, MSGFPlus .mzid, Sage .sage.tsv, X!Tandem .xml, Mascot .mzid, MS Amanda .csv, PeptideShaker .mzid, ProteomeDiscoverer .msf, PEAKS .mzid)
- Modification mapping configuration file (JSON or TOML format with search-engine-label → ProForma-label mappings)

## Outputs

- PSM records with normalized peptide sequences in HUPO-PSI ProForma v2 notation
- Annotated PSM object or intermediate file with modification mapping applied
- Validated PSM file ready for feature generation and rescoring

## How to apply

Load the PSM file and extract modification labels as they appear in search engine output (e.g., 'ox', '+57.02146', mass-shift notation). Read the modification_mapping configuration from a TOML or JSON file, where each search-engine-specific label is mapped to a ProForma-compatible label in one of five accepted formats: PSI-MOD accession, PSI-MOD name, Unimod accession, Unimod name, or chemical formula (e.g., 'Formula:HO3P'). For each PSM record, iterate through its peptide sequence and replace each search-engine modification label with its corresponding ProForma label using the mapping dictionary. Validate that all mapped labels conform to HUPO-PSI ProForma v2 notation and are recognized by psm_utils. Write or update the PSM record with remapped peptide sequences. Chemical formula notation is preferred over mass shifts when modifications are not in controlled vocabularies.

## Related tools

- **MS²Rescore** (Primary rescoring platform that orchestrates modification mapping and consumes normalized PSMs for feature generation and rescoring) — https://github.com/compomics/ms2rescore
- **psm_utils** (Parses PSM files from multiple search engines and validates ProForma-compliant modification labels)
- **MS²PIP** (Spectrum prediction model that requires normalized ProForma notation for modification-aware fragmentation prediction)
- **DeepLC** (Retention time prediction feature generator that requires modification formula representation for certain modifications)
- **Percolator** (Rescoring engine that consumes PSMs with normalized modifications for ML-driven rescoring) — https://github.com/percolator/percolator
- **Mokapot** (Alternative rescoring engine supported by MS²Rescore that consumes normalized PSMs)

## Evaluation signals

- All extracted modification labels from the input PSM file have a corresponding entry in the modification_mapping configuration; no unmapped labels remain in output.
- Output peptide sequences conform to HUPO-PSI ProForma v2 syntax (e.g., '[Phospho]', 'U:Oxidation', 'Formula:HO3P') and are recognized by psm_utils without parsing errors.
- Mapped modification labels are internally consistent across all PSM records — identical search-engine labels map to identical ProForma labels throughout the file.
- Feature generators (MS²PIP, DeepLC) can successfully consume the normalized PSM records without modification-related parsing failures.
- Round-trip validation: the original modification information (amino acid position, mass delta, or functional annotation) is preserved in the ProForma output; no information loss occurs during mapping.

## Limitations

- Mapping configuration must be manually constructed or curated per search engine; no universal, auto-generated mapping is provided by MS²Rescore.
- Custom or proprietary modifications not in PSI-MOD, Unimod, or ProForma dictionaries must be represented as chemical formulas (e.g., 'Formula:HO3P'); if formula is unknown or ambiguous, mapping may fail.
- Some search engines (e.g., MaxQuant) do not report fixed modifications in the PSM file; these must be configured separately and added after modification mapping.
- Mass-shift-only notation (e.g., '+57.02146') can be ambiguous if multiple modifications have similar or identical mass deltas; chemical formula or controlled vocabulary is preferred.
- ProForma v2 notation does not capture 3D structural information (secondary/tertiary structure) or complex cross-links; it is limited to linear primary structure representation.

## Evidence

- [other] MS²Rescore implements modification_mapping as a configuration object that maps search-engine-specific modification labels to ProForma labels in five accepted formats: PSI-MOD accession, PSI-MOD name, Unimod accession, Unimod name, or chemical formula (e.g., 'Formula:HO3P'). For example, MaxQuant's 'ox' label maps to 'U:Oxidation', and 'gl' maps to 'U:Gln->pyro-Glu'. Formula notation is preferred over mass shifts when modifications are not in controlled vocabularies.: "MS²Rescore implements modification_mapping as a configuration object that maps search-engine-specific modification labels to ProForma labels in five accepted formats: PSI-MOD accession, PSI-MOD name,"
- [intro] MS²Rescore uses the `HUPO-PSI standardized ProForma v2 notation` to represent modified peptides...requires a configuration :py:obj:`modification_mapping` which maps each specific search engine: "MS²Rescore uses the `HUPO-PSI standardized ProForma v2 notation` to represent modified peptides...requires a configuration :py:obj:`modification_mapping` which maps each specific search engine"
- [intro] most PSM file types coming from different proteomics search engines use a custom modification notation...Therefore, ``ox`` needs to be mapped to ``U:Oxidation``: "most PSM file types coming from different proteomics search engines use a custom modification notation...Therefore, ``ox`` needs to be mapped to ``U:Oxidation``"
- [readme] MS²Rescore can read peptide identifications in any format supported by [psm_utils][psm_utils] (see [Supported file formats][file-formats]) and has been tested with various search engines output files: [MS Amanda] `.csv`, [Sage] `.sage.tsv`, [PeptideShaker] `.mzid`, [ProteomeDiscoverer]`.msf`, [MSGFPlus] `.mzid`, [Mascot] `.mzid`, [MaxQuant] `msms.txt`, [X!Tandem] `.xml`, [PEAKS] `.mzid`: "MS²Rescore can read peptide identifications in any format supported by [psm_utils][psm_utils]...and has been tested with various search engines output files: [MS Amanda] `.csv`, [Sage] `.sage.tsv`,"
- [intro] some feature generators (such as DeepLC) require the modification formula: "some feature generators (such as DeepLC) require the modification formula"
- [intro] fixed modifications that are not reported in the PSM file must be configured separately: "fixed modifications that are not reported in the PSM file must be configured separately"
- [intro] MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
- [readme] Protein and peptide sequences...There is still no clear consensus about how to represent 'proteoforms' and 'peptidoforms'...A standard notation for proteoforms and peptidoforms is then required for the community: "A standard notation for proteoforms and peptidoforms is then required for the community, so that it can be embedded in many relevant PSI (and potentially other) file formats."
