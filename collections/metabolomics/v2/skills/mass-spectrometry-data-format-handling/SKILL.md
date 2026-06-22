---
name: mass-spectrometry-data-format-handling
description: Use when you have raw MRM sample files from an LC-MS/MS instrument and need to programmatically identify and tabulate all precursor m/z and product m/z pairs for each MRM transition.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - get_PrecMZ_ProdMZ
  - MRMQuant
  - KNIME
  - OpenMS
  - pyOpenMS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.4c02462
  title: MRMQuant
- doi: 10.1038/nmeth.3959
  title: ''
evidence_spans:
- Users can install get_PrecMZ_ProdMZ in the "program/associated programs" folder to acquire precursor and product m/z values in an MRM sample file.
- Be sure to use the latest version (currently MRMQuant v2.7).
- how you installed OpenMS (e.g., from within KNIME, binary installers, self compiled)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mrmquant_cq
    doi: 10.1021/acs.analchem.4c02462
    title: MRMQuant
  - build: coll_openms_2_cq
    doi: 10.1038/nmeth.3959
    title: OpenMS
  dedup_kept_from: coll_mrmquant_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c02462
  all_source_dois:
  - 10.1021/acs.analchem.4c02462
  - 10.1038/nmeth.3959
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-format-handling

## Summary

Extract precursor and product m/z values from LC-MS/MS MRM (multiple reaction monitoring) raw data files using specialized utility software. This skill transforms raw instrument output into structured m/z pair tables, which serve as the foundation for subsequent MRM transition quantification workflows.

## When to use

You have raw MRM sample files from an LC-MS/MS instrument and need to programmatically identify and tabulate all precursor m/z and product m/z pairs for each MRM transition. This is the initial data parsing step when you do not have pre-extracted transition lists and must recover them from the instrument's raw data format.

## When NOT to use

- Input already contains a pre-extracted or vendor-supplied transition list in tabular form.
- Data was acquired using a non-MRM acquisition mode (e.g., full-scan, data-dependent acquisition).
- Raw data file format is not natively supported by the get_PrecMZ_ProdMZ utility.

## Inputs

- raw MRM sample file (LC-MS/MS instrument format)

## Outputs

- structured table of precursor m/z and product m/z pairs (CSV or TSV format)

## How to apply

Install the get_PrecMZ_ProdMZ utility into the MRMQuant v2.7 associated programs folder. Load the raw MRM sample file (native LC-MS/MS instrument format) into the utility, which will parse the file to identify all MRM transitions and their associated precursor and product m/z values. The program extracts and tabulates these m/z pairs and outputs them in a structured table format (CSV or TSV). Verify that every expected transition is present in the output table and that m/z values match the instrument's acquisition method.

## Related tools

- **MRMQuant** (parent software package; provides the framework and associated programs folder in which get_PrecMZ_ProdMZ is installed) — https://github.com/kslynn128171/MRMQuant
- **get_PrecMZ_ProdMZ** (utility for extracting precursor and product m/z values from MRM sample files) — https://github.com/kslynn128171/MRMQuant

## Evaluation signals

- Output table contains one row per MRM transition with distinct precursor m/z and product m/z columns.
- All MRM transitions configured in the instrument's acquisition method are represented in the output.
- m/z values are numeric, positive, and fall within the expected mass range for the analytes and instrument.
- Output file conforms to declared format (CSV or TSV) with proper delimiters and no truncated or malformed entries.
- Row count and transition list match the instrument method file or vendor software's transition report.

## Limitations

- Utility depends on MRMQuant v2.7; compatibility with older or newer versions is not documented.
- No changelog or version history provided; breaking changes in file format support are not communicated.
- Success depends on the raw data file format being recognized by the underlying parser; unsupported or corrupted files may fail silently or produce incomplete output.

## Evidence

- [other] The get_PrecMZ_ProdMZ program is an associated utility that reads an MRM sample file and acquires precursor and product m/z values for each transition.: "The get_PrecMZ_ProdMZ program is an associated utility that reads an MRM sample file and acquires precursor and product m/z values for each transition."
- [readme] Users can install get_PrecMZ_ProdMZ in the "program/associated programs" folder to acquire precursor and product m/z values in an MRM sample file.: "Users can install get_PrecMZ_ProdMZ in the "program/associated programs" folder to acquire precursor and product m/z values in an MRM sample file."
- [other] Parse the file to identify all MRM transitions and their associated precursor m/z and product m/z values. Extract and tabulate precursor and product m/z pairs for each transition. Output the extracted m/z values in a structured table format (CSV or TSV).: "Parse the file to identify all MRM transitions and their associated precursor m/z and product m/z values. Extract and tabulate precursor and product m/z pairs for each transition. Output the"
- [readme] Be sure to use the latest version (currently MRMQuant v2.7).: "Be sure to use the latest version (currently MRMQuant v2.7)."
