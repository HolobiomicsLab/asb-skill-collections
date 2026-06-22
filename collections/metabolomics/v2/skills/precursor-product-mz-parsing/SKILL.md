---
name: precursor-product-mz-parsing
description: Use when you have raw MRM sample files from a LC-MS/MS instrument and need to systematically recover all precursor m/z and product m/z pairs for each transition. Use this as an initial parsing step before quantitation, method optimization, or transition verification workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - get_PrecMZ_ProdMZ
  - MRMQuant
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.4c02462
  title: MRMQuant
evidence_spans:
- Users can install get_PrecMZ_ProdMZ in the "program/associated programs" folder to acquire precursor and product m/z values in an MRM sample file.
- Be sure to use the latest version (currently MRMQuant v2.7).
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mrmquant_cq
    doi: 10.1021/acs.analchem.4c02462
    title: MRMQuant
  dedup_kept_from: coll_mrmquant_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c02462
  all_source_dois:
  - 10.1021/acs.analchem.4c02462
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# precursor-product-mz-parsing

## Summary

Extract precursor and product m/z value pairs from MRM (multiple reaction monitoring) LC-MS/MS raw data files using the get_PrecMZ_ProdMZ utility. This skill enables automated identification and tabulation of all MRM transitions' mass-to-charge ratios, essential for method validation and quantitation workflow setup.

## When to use

Apply this skill when you have raw MRM sample files from a LC-MS/MS instrument and need to systematically recover all precursor m/z and product m/z pairs for each transition. Use this as an initial parsing step before quantitation, method optimization, or transition verification workflows.

## When NOT to use

- Input is already a parsed or pre-extracted m/z transition table.
- Working with non-MRM data (e.g., full-scan MS, data-independent acquisition, or other MS/MS acquisition modes).
- Using MRMQuant versions older than v2.7.

## Inputs

- Raw MRM sample file (LC-MS/MS instrument format)

## Outputs

- Structured table of precursor m/z and product m/z value pairs (CSV or TSV format)
- Tabulated list of all MRM transitions with associated m/z values

## How to apply

Install get_PrecMZ_ProdMZ into the MRMQuant v2.7 'program/associated programs' folder from the project repository. Load the raw MRM sample file (native LC-MS/MS instrument format) into the utility. The program parses the file to identify all MRM transitions and their associated precursor and product m/z values. Extract and tabulate the precursor–product m/z pairs for each transition, outputting results in a structured table format (CSV or TSV) for downstream analysis or method documentation.

## Related tools

- **MRMQuant** (Parent quantitation package that hosts and manages get_PrecMZ_ProdMZ as an associated utility for MRM data processing) — github.com/kslynn128171/MRMQuant
- **get_PrecMZ_ProdMZ** (Dedicated utility for parsing raw MRM files and extracting precursor–product m/z transition data) — github.com/kslynn128171/MRMQuant

## Evaluation signals

- Output table contains one row per unique MRM transition with no missing or null m/z values.
- All precursor m/z values match the expected monoisotopic mass or expected parent ion m/z for the target compound.
- All product m/z values fall within the expected fragmentation pattern for the given precursor ion (typically < precursor m/z).
- CSV or TSV output is well-formed, parseable, and contains consistent column headers (e.g., 'Transition', 'Precursor_mz', 'Product_mz').
- Number of transitions extracted matches the expected count from the LC-MS/MS acquisition method file.

## Limitations

- Requires MRMQuant v2.7 or later; compatibility with older versions not confirmed.
- Only processes raw MRM sample files; cannot work with already-converted or abstracted data formats.
- No changelog provided in the repository documentation, limiting version-to-version change tracking.
- Depends on successful file format recognition; instrument-specific raw formats may require vendor-specific drivers or converters.

## Evidence

- [readme] Users can install get_PrecMZ_ProdMZ in the "program/associated programs" folder to acquire precursor and product m/z values in an MRM sample file.: "Users can install get_PrecMZ_ProdMZ in the "program/associated programs" folder to acquire precursor and product m/z values in an MRM sample file."
- [other] The get_PrecMZ_ProdMZ program is an associated utility that reads an MRM sample file and acquires precursor and product m/z values for each transition.: "The get_PrecMZ_ProdMZ program is an associated utility that reads an MRM sample file and acquires precursor and product m/z values for each transition."
- [readme] Be sure to use the latest version (currently MRMQuant v2.7).: "Be sure to use the latest version (currently MRMQuant v2.7)."
- [other] Output the extracted m/z values in a structured table format (CSV or TSV).: "Output the extracted m/z values in a structured table format (CSV or TSV)."
