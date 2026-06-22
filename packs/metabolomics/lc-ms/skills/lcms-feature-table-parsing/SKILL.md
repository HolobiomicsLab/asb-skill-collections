---
name: lcms-feature-table-parsing
description: Use when you have raw nontargeted LCMS feature tables from one or more analytical methods in tabular format (with m/z, RT, and intensity columns) that need to be aligned or clustered, or when integrating multiple feature tables into a shared BMXP processing pipeline that requires standardized.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - bmxp
  - Python
  - Eclipse
  - Chroma
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1093/bioinformatics/btaf290/8128335
  title: Eclipse
evidence_spans:
- pip install bmxp
- They are written in Python and C
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_3d_molecular_cartography_optimus_ili_cq
    doi: 10.1038/nprot.2017.122
    title: 3D molecular cartography (Optimus / 'ili)
  - build: coll_eclipse_cq
    doi: 10.1093/bioinformatics/btaf290/8128335
    title: Eclipse
  dedup_kept_from: coll_eclipse_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf290/8128335
  all_source_dois:
  - 10.1093/bioinformatics/btaf290/8128335
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lcms-feature-table-parsing

## Summary

Parse and normalize nontargeted LCMS feature tables containing m/z, retention time, and intensity values into a standardized schema for downstream alignment and clustering. This skill is essential as the first step in multi-dataset feature correspondence workflows, ensuring consistent metadata representation across analytical methods.

## When to use

You have raw nontargeted LCMS feature tables from one or more analytical methods in tabular format (with m/z, RT, and intensity columns) that need to be aligned or clustered, or when integrating multiple feature tables into a shared BMXP processing pipeline that requires standardized column headers and data types.

## When NOT to use

- Input is already a parsed feature table conforming to bmxp.FMDATA schema with validated data types and no missing critical columns.
- Input is targeted LCMS data without retention time or m/z values (use __extraction_method field to flag mixed targeted/nontargeted datasets instead).
- Input is chromatographic raw data (.raw or .mzML files) — use Chroma module first to extract features before parsing.

## Inputs

- Nontargeted LCMS feature table (tabular format: CSV, TSV, or pandas DataFrame)
- Feature metadata columns: m/z, retention time, intensity, feature ID, analytical method
- Optional: injection metadata (injection_id mapping to samples)

## Outputs

- Parsed Feature Metadata table (bmxp.FMDATA): indexed by Compound_ID, with columns RT, MZ, Intensity, Method, Annotation_ID (if available)
- Feature Abundances pivot table (Compound_ID × injection_id): intensity values aligned to injections
- Injection Metadata table (bmxp.IMDATA): indexed by injection_id, with broad_id and injection_type

## How to apply

Load feature tables in tabular format (CSV, TSV, or similar) containing m/z, retention time, and intensity values. Map source column names to the BMXP shared schema: `Compound_ID` (feature identifier), `RT` (unitless retention time), `MZ` (mass-to-charge ratio), and `Intensity` (average feature intensity). Normalize metadata by validating data types (numeric for m/z, RT, intensity; string for IDs and method names), checking for missing values, and optionally scaling RT values if they differ across datasets. Store the parsed result as Feature Metadata (bmxp.FMDATA) and Feature Abundances (pivot table: Compound_ID × injection_id). Before parsing, configure the shared schema globally in bmxp if your column labels differ from defaults, ensuring all downstream modules (Eclipse, Blueshift, Gravity) use consistent terminology.

## Related tools

- **bmxp** (Provides shared schema (bmxp.FMDATA, bmxp.IMDATA) and column definitions used during parsing; parsed tables feed into Eclipse, Blueshift, Gravity, and Formation modules.) — https://github.com/broadinstitute/bmxp
- **Eclipse** (Accepts parsed Feature Metadata + Feature Abundances to align two or more same-method nontargeted LCMS datasets; requires well-formatted m/z and RT columns.) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/eclipse/readme.md
- **Chroma** (Reads .raw and .mzML files to extract features; output should be parsed using this skill before downstream workflows.) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/chroma/readme.md

## Examples

```
```python
import bmxp
from bmxp.eclipse import MSAligner
import pandas as pd

# Configure schema if needed
bmxp.FMDATA['Compound_ID'] = 'Feature_ID'
bmxp.IMDATA['injection_id'] = 'Filename'

# Load and parse feature table
features_df = pd.read_csv('raw_features.csv')
# Ensure columns: Compound_ID, RT, MZ, Intensity, Method
fm_data = features_df[['Compound_ID', 'RT', 'MZ', 'Intensity', 'Method']]
feature_abundances = features_df.set_index('Compound_ID').drop(['RT', 'MZ', 'Intensity', 'Method'], axis=1)
```
```

## Evaluation signals

- All rows in Feature Metadata have non-null Compound_ID, RT, MZ, and Intensity values; data types are numeric for RT/MZ/Intensity and string for IDs.
- Feature Abundances pivot table has Compound_ID as row index and injection_id as column headers, with no NaN abundance values (or NaN handled consistently).
- Column header names match the configured schema (e.g., 'Compound_ID', 'RT', 'MZ', 'Intensity', 'Method'); schema can be verified by inspecting bmxp.FMDATA and bmxp.IMDATA dictionaries.
- m/z values are positive and within expected mass range for nontargeted LCMS (typically 50–2000 m/z); RT values are non-negative and consistent in scale across all datasets.
- Injection Metadata has one row per unique injection_id with broad_id and injection_type populated; broad_id matches sample biospecimen labels if Sample Metadata is available.

## Limitations

- Assumes input feature tables are from the same analytical method; mixing methods requires separate parsing and explicit Method field annotation.
- Does not handle automated retention time alignment or scaling across different instrument configurations; users must manually verify RT comparability before Eclipse alignment.
- Schema configuration is global in bmxp; changing column labels affects all modules in a session, requiring care when working with mixed naming conventions.
- Missing intensity values, m/z outliers, or malformed injection_id entries are not automatically flagged; preprocessing validation is the user's responsibility.
- Supports nontargeted LCMS features only; targeted methods or ion mobility data require __extraction_method annotation but are not validated during parsing.

## Evidence

- [other] Load two or more nontargeted LCMS feature tables (from same analytical method) in a tabular format containing m/z, retention time, and intensity values.: "Load two or more nontargeted LCMS feature tables (from same analytical method) in a tabular format containing m/z, retention time, and intensity values."
- [other] Parse and normalize feature metadata (m/z, RT, intensity distributions) across datasets.: "Parse and normalize feature metadata (m/z, RT, intensity distributions) across datasets."
- [readme] All BMXP modules use a shared schema and file formats with our prefered columns headers. These files are (along with their labels): Feature Metadata `bmxp.FMDATA`: "All BMXP modules use a shared schema and file formats with our prefered columns headers. These files are (along with their labels): Feature Metadata `bmxp.FMDATA`"
- [readme] Feature Metadata describes the LCMS feature. This is a mixture of fundamental nontargeted feature information, annotation info, and anything else.: "Feature Metadata describes the LCMS feature. This is a mixture of fundamental nontargeted feature information, annotation info, and anything else."
- [readme] Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances.: "Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances."
- [readme] To update the schema, modify the dictionary objects in the module directly prior to running code.: "To update the schema, modify the dictionary objects in the module directly prior to running code."
