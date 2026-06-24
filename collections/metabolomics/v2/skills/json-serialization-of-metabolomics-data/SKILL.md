---
name: json-serialization-of-metabolomics-data
description: Use when after pre-annotation grouping (e.g., via khipu) has assigned
  features to empirical compounds, or when exporting feature tables and metadata from
  asari for downstream analysis in MetaboAnalyst or custom R/Python workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - khipu
  - Python
  - asari
  - metDataModel
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- pre-annotation to group featues to empirical compounds (khipu)
- Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm_cq
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# JSON serialization of metabolomics data

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Serialize grouped empirical compounds (EmpCpd) and feature tables into JSON format for portable, standardized representation of metabolomics annotations and results. This enables interoperability between tools in the metabolomics processing pipeline and downstream statistical analysis.

## When to use

Apply this skill after pre-annotation grouping (e.g., via khipu) has assigned features to empirical compounds, or when exporting feature tables and metadata from asari for downstream analysis in MetaboAnalyst or custom R/Python workflows. Use it whenever metabolomics intermediate results (feature tables, annotations, EmpCpd structures, sample metadata) must be exchanged between tools or archived in a tool-agnostic format.

## When NOT to use

- Feature grouping has not yet been completed (use khipu first)
- Data is already in a format suitable for immediate downstream analysis and no interoperability with other tools is required
- Raw LC-MS data is still in .raw or .mzML format and has not been converted to a feature table

## Inputs

- EmpCpd structure (grouped empirical compounds with adduct and isotope annotations)
- Feature table (m/z, retention time, intensity matrix)
- Sample metadata (sample names, type, batch information)
- MS1/MS2 annotations (if available)

## Outputs

- empCpd.json (serialized empirical compounds with pre-annotations)
- feature_table.json (optional; feature matrix in JSON format)
- sample_annotation_table.json (sample metadata and QC flags)
- .txt or .tsv exports (human-readable feature tables)

## How to apply

After khipu or asari processing completes, serialize the EmpCpd structure—containing grouped features, inferred adducts, isotope assignments, and pre-annotations—to JSON using Python's json module or the pipeline's built-in serialization routines. Include metadata fields such as empirical formula, charge state, retention time, and m/z for each group. Save the JSON file to the experiment's annotations subdirectory (e.g., annotations/empCpd.json). For feature tables, export to both .tsv (for human review and R compatibility) and JSON (for programmatic access). Ensure all m/z, retention time, and intensity values are preserved with appropriate precision (e.g., floating-point m/z to support ppm-level tolerance comparisons). Validate the JSON schema before archival to confirm all required fields are present and correctly typed.

## Related tools

- **khipu** (Groups features into empirical compounds (isotopes, adducts) prior to JSON serialization) — https://github.com/shuzhao-li-lab/khipu
- **asari** (Generates feature tables and supports export to standardized formats including JSON) — https://github.com/shuzhao-li/asari
- **metDataModel** (Defines common data models and schema for metabolomics structures serialized to JSON) — https://github.com/shuzhao-li-lab/metDataModel
- **Python** (json module and custom serialization routines for writing JSON files)

## Examples

```
import json
from khipu import Khipu
khipu_obj = Khipu(feature_table, mode='pos')
empcpds = khipu_obj.construct_empirical_compounds()
with open('experiment_dir/annotations/empCpd.json', 'w') as f:
    json.dump([ec.to_dict() for ec in empcpds], f, indent=2)
```

## Evaluation signals

- JSON file is syntactically valid (parses without errors using json.load or equivalent)
- All empirical compounds in empCpd.json contain required fields: neutral_mass, charge, adduct_annotation, isotope_state, and list of grouped features
- Feature m/z and retention time values are preserved with sufficient precision (floating-point) to support downstream tolerance matching (e.g., 5 ppm m/z tolerance, 2 sec retention time tolerance)
- JSON file can be read and reconstructed back into Python objects that match the original EmpCpd or feature table structure
- Sample metadata in JSON includes all fields from the input metadata CSV (sample type, batch, file path)

## Limitations

- JSON serialization does not compress data; file sizes can be large for high-dimensional feature tables with thousands of features. Consider gzip compression for long-term storage.
- No built-in versioning or schema versioning in the JSON output; future changes to the EmpCpd or feature table structure may break downstream tools expecting an older schema.
- Manual validation of JSON structure is required; the pipeline does not enforce schema compliance during serialization, so invalid or incomplete JSON may be written without error.
- JSON representation may lose numerical precision for very small m/z or intensity values due to floating-point rounding; critical for high-resolution Orbitrap data.

## Evidence

- [other] Serialize the grouped EmpCpd structure to JSON format and save to the experiment's annotations subdirectory.: "Serialize the grouped EmpCpd structure to JSON format and save to the experiment's annotations subdirectory"
- [readme] output data in standardized formats (.txt, JSON), ready for downstream analysis: "output data in standardized formats (.txt, JSON), ready for downstream analysis"
- [readme] This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM and empirical compounds as a JSON file representing putative metabolites: "empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards"
- [other] Khipu constructs empirical compounds by grouping features as isotopes and adducts with default parameters: charges up to z=3, m+13C3 isotopologues, common adducts by chromatography mode, 5 ppm mz tolerance, and 2 sec rt tolerance: "Khipu constructs empirical compounds by grouping features as isotopes and adducts with default parameters: charges up to z=3, m+13C3 isotopologues, common adducts by chromatography mode, 5 ppm mz"
