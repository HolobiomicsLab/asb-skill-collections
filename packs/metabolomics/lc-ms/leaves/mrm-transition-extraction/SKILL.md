---
name: mrm-transition-extraction
description: Use when you have raw LC-MS/MS data in MRM acquisition mode and need
  to systematically identify and catalog all precursor m/z and corresponding product
  m/z values for each transition monitored during data collection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - get_PrecMZ_ProdMZ
  - MRMQuant
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c02462
  title: MRMQuant
evidence_spans:
- Users can install get_PrecMZ_ProdMZ in the "program/associated programs" folder
  to acquire precursor and product m/z values in an MRM sample file.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mrm-transition-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract precursor and product m/z value pairs from raw MRM (Multiple Reaction Monitoring) LC-MS/MS sample files using the get_PrecMZ_ProdMZ utility. This skill is essential for downstream MRM quantification workflows that require cataloging all monitored transitions with their exact mass-to-charge ratios.

## When to use

Apply this skill when you have raw LC-MS/MS data in MRM acquisition mode and need to systematically identify and catalog all precursor m/z and corresponding product m/z values for each transition monitored during data collection. This is a prerequisite step before quantifying peak areas or validating transition specificity in targeted proteomics or metabolomics experiments.

## When NOT to use

- Input data is not from an MRM acquisition method (e.g., full-scan MS or data-dependent acquisition) — use full-spectrum extraction instead.
- m/z values and transition definitions are already available in a structured annotation file — skip directly to quantification.
- Using an older version of MRMQuant (< v2.7) where get_PrecMZ_ProdMZ may not be compatible or may not be bundled.

## Inputs

- Raw MRM sample file (LC-MS/MS instrument native format)
- MRMQuant v2.7 installation with associated programs folder

## Outputs

- Structured table of precursor m/z and product m/z pairs (CSV or TSV format)
- One row per MRM transition with m/z values tabulated

## How to apply

Install get_PrecMZ_ProdMZ from the MRMQuant github repository into the program/associated programs folder of MRMQuant v2.7. Load the raw MRM sample file (instrument-native format from the LC-MS/MS instrument) into the utility. The tool parses the file to identify all MRM transitions encoded in the acquisition method, systematically extracting the precursor m/z and product m/z values for each transition pair. The extracted m/z pairs are output in a structured tabular format (CSV or TSV) with one row per transition, enabling validation and downstream use in quantification pipelines.

## Related tools

- **MRMQuant** (Parent quantification framework that provides the associated programs folder and integration environment for get_PrecMZ_ProdMZ) — github.com/kslynn128171/MRMQuant
- **get_PrecMZ_ProdMZ** (Dedicated utility that reads MRM sample files and extracts precursor and product m/z values for all monitored transitions) — github.com/kslynn128171/MRMQuant

## Evaluation signals

- Output table contains one row per unique MRM transition with no duplicates or missing transitions visible in the raw file.
- Precursor m/z and product m/z columns contain numeric values within expected range for the analyte class (e.g., 100–1500 m/z for small molecules, 500–2000 for peptides).
- CSV or TSV output file is well-formed with consistent delimiter use and proper column headers.
- Number of extracted transitions matches the expected count from the instrument's acquisition method or published transition list for the assay.
- m/z values are consistent across multiple replicates of the same sample file (reproducibility check).

## Limitations

- The utility depends on correct parsing of instrument-specific raw file formats; compatibility is limited to formats supported by MRMQuant v2.7.
- No changelog is available to track version-specific improvements or bug fixes to the extraction algorithm.
- The tool extracts transitions as defined in the instrument method; it does not validate transition specificity or perform peak-level quality filtering.

## Evidence

- [intro] Install get_PrecMZ_ProdMZ step: "Users can install get_PrecMZ_ProdMZ in the "program/associated programs" folder to acquire precursor and product m/z values in an MRM sample file."
- [readme] Version requirement: "Be sure to use the latest version (currently MRMQuant v2.7)."
- [other] Extraction and output methodology: "Extract and tabulate precursor and product m/z pairs for each transition. Output the extracted m/z values in a structured table format (CSV or TSV)."
- [other] Input file type: "Load the MRM sample file (raw data format from LC-MS/MS instrument)."
