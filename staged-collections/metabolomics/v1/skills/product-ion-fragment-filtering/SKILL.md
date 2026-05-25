---
name: product-ion-fragment-filtering
description: Filter MS/MS spectra by the presence and intensity of specific product ions (fragment m/z values) to identify compounds with characteristic fragmentation patterns. This skill uses MassQL queries to retrieve all MS/MS scans containing a target product ion within a specified m/z tolerance and minimum relative intensity threshold.
when_to_use_negative:
- Input dataset contains only MS1 (full-scan) data without MS/MS fragmentation spectra—product-ion filtering requires tandem MS data.
- Target product ion is highly abundant across unrelated compound classes (high false-positive rate due to in-source fragmentation or common neutral losses); use orthogonal filtering (e.g., precursor m/z, retention time, or ion mobility) to reduce noise.
- MS/MS spectra lack sufficient intensity dynamic range or resolution to reliably detect the target product ion at the specified tolerance and intensity threshold; verify reference spectra meet quality criteria first.
edam_operation: http://edamontology.org/operation_3647
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3172
tools:
- name: MassQL
  role: Query language parser and execution engine for filtering MS/MS spectra by product ion m/z, tolerance, and intensity
  repo: https://github.com/mwang87/MassQueryLanguage
- name: lark
  role: Python parsing toolkit used to parse MassQL query strings into internal data structures
  repo: https://github.com/lark-parser/lark
- name: pyteomics
  role: Python library for reading and parsing open MS data file formats (mzML, mzXML, MGF)
- name: pandas
  role: Python DataFrame library for efficient filtering and manipulation of MS/MS spectra data
- name: Apache feather
  role: Columnar file format for caching and fast retrieval of repeated MS data queries
- name: MS-Cluster
  role: Clustering tool to collapse redundant MS/MS observations into consensus spectra after product-ion filtering
- name: Falcon-MS
  role: Alternative tool to generate consensus MS/MS spectra from redundant observations
- name: MZmine
  role: Open-source MS data analysis software with native MassQL support for product-ion filtering workflows
  repo: https://github.com/mzmine/mzmine
- name: GNPS/MassIVE
  role: Public MS data repository and spectral library resource for reference compounds and large-scale filtering
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1038/s41592-025-02660-z
    title: A universal language for finding mass spectrometry data patterns
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_s41592_full/skills/product-ion-fragment-filtering/SKILL.md
    - outputs/audit_s41592_full/skills/product-ion-fragment-filtering/skill.md
    merged_at: '2026-05-25T07:15:30.950460+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/product-ion-fragment-filtering@sha256:04c039186a12c868b071fd44702506164c129f83df8793f105e93bc9d996be56
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1038/s41592-025-02660-z
---

# product-ion-fragment-filtering

## Summary

Filter MS/MS spectra by the presence and intensity of specific product ions (fragment m/z values) to identify compounds with characteristic fragmentation patterns. This skill uses MassQL queries to retrieve all MS/MS scans containing a target product ion within a specified m/z tolerance and minimum relative intensity threshold.

## When to use

Apply this skill when you have a known characteristic fragment ion (e.g., H₄PO₄⁺ at m/z 98.9847 for organophosphate esters, or iron-characteristic isotope patterns) and want to retrieve all MS/MS spectra in a dataset—whether local or public repository—that contain that product ion at sufficient intensity to enable molecular identification or discovery. Use this when manual inspection has identified 3–10 reference compounds with this fragment and you want to scale discovery across millions of spectra.

## When NOT to use

- Input dataset contains only MS1 (full-scan) data without MS/MS fragmentation spectra—product-ion filtering requires tandem MS data.
- Target product ion is highly abundant across unrelated compound classes (high false-positive rate due to in-source fragmentation or common neutral losses); use orthogonal filtering (e.g., precursor m/z, retention time, or ion mobility) to reduce noise.
- MS/MS spectra lack sufficient intensity dynamic range or resolution to reliably detect the target product ion at the specified tolerance and intensity threshold; verify reference spectra meet quality criteria first.

## Inputs

- LC-MS/MS dataset in mzML, mzXML, or MGF format
- Reference MS/MS spectra with known compounds containing target product ion
- MassQL query string specifying MS2PROD, TOLERANCEPPM, and INTENSITYPERCENT parameters

## Outputs

- Filtered MS/MS spectra in CSV/TSV format with scan identifiers, precursor m/z, product ion m/z, and intensity values
- Metadata table mapping matched spectra to molecular features and acquisition conditions
- Summary statistics: total number of spectra retrieved, distribution by precursor m/z, consensus spectra (after clustering with MS-Cluster or Falcon-MS)

## How to apply

First, design and refine a MassQL query on a reference dataset containing known compounds with the target fragment (e.g., GNPS spectral libraries). The query must specify MS2PROD=<m/z value>, TOLERANCEPPM=<ppm tolerance>, and INTENSITYPERCENT=<minimum % of base peak intensity>. Parse the query string using the lark library to construct an internal query data structure. Load MS data files (mzML, mzXML, or MGF format) using pyteomics and convert to pandas DataFrames, optionally caching as Apache feather files for repeated queries. Apply the query engine to filter all MS/MS scans, retaining only those with a product ion at the specified m/z ± tolerance and peak intensity ≥ the specified percentage of base peak. Export matched spectra in tabular format (CSV/TSV) with scan identifiers, precursor m/z, product ion m/z, intensity values, and metadata. Validate that the number of retrieved spectra and their distribution across precursor m/z ranges match expectations from prior manual analyses.

## Related tools

- **MassQL** (Query language parser and execution engine for filtering MS/MS spectra by product ion m/z, tolerance, and intensity) — https://github.com/mwang87/MassQueryLanguage
- **lark** (Python parsing toolkit used to parse MassQL query strings into internal data structures) — https://github.com/lark-parser/lark
- **pyteomics** (Python library for reading and parsing open MS data file formats (mzML, mzXML, MGF))
- **pandas** (Python DataFrame library for efficient filtering and manipulation of MS/MS spectra data)
- **Apache feather** (Columnar file format for caching and fast retrieval of repeated MS data queries)
- **MS-Cluster** (Clustering tool to collapse redundant MS/MS observations into consensus spectra after product-ion filtering)
- **Falcon-MS** (Alternative tool to generate consensus MS/MS spectra from redundant observations)
- **MZmine** (Open-source MS data analysis software with native MassQL support for product-ion filtering workflows) — https://github.com/mzmine/mzmine
- **GNPS/MassIVE** (Public MS data repository and spectral library resource for reference compounds and large-scale filtering)

## Examples

```
from massql.query import MassQLQuery; query = MassQLQuery('MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50'); results = query.execute_on_file('marine_water.mzML'); results.to_csv('filtered_spectra.csv')
```

## Evaluation signals

- Retrieved spectrum count is consistent with expectations from prior manual analyses (e.g., ~589 spectra in a marine water test dataset for a single phosphate fragment, or 338,439 spectra across a repository of >230 million MS/MS scans).
- Consensus spectra generated after clustering contain product ions at the expected m/z ± tolerance in ≥50% of retained spectra.
- Spectral library matching recovers a plausible fraction of known compounds (e.g., 5–15% putative identification rate for novel compound discovery workflows).
- Precursor m/z distribution of filtered spectra matches expected molecular weight range for the compound class (e.g., 150–800 m/z for organophosphate esters).
- No redundant spectra remain after de-duplication; each consensus spectrum appears once in export tables.

## Limitations

- MassQL has limited capability to leverage multiple consecutive MS spectra (e.g., chromatographic peak shape) to refine molecular feature assignment; single MS/MS scans are queried independently.
- Product ions with low relative intensity fall outside intensity tolerance thresholds and are missed; if the target fragment has variable ionization efficiency across related compounds, some true positives may be excluded (e.g., one siderophore with 54Fe peak intensity outside 25% tolerance was missed).
- In-source fragmentation or neutral losses common to many compound classes can produce false positives; orthogonal filtering by precursor m/z or retention time is recommended to reduce noise in discovery workflows.

## Evidence

- [other] Execute MassQL phosphate product-ion MS2 query (MS2PROD=98.9847, TOLERANCEPPM=50, INTENSITYPERCENT=50) on a marine water test dataset to retrieve candidate OPE spectra: "Execute MassQL phosphate product-ion MS2 query (MS2PROD=98.9847, TOLERANCEPPM=50, INTENSITYPERCENT=50)"
- [other] In a test marine water dataset where three OPEs were previously identified by manual analysis, the MassQL phosphate fragment query returned 589 MS/MS spectra belonging to ~60 unique molecular features.: "the MassQL phosphate fragment query returned 589 MS/MS spectra belonging to ~60 unique molecular features"
- [other] Apply the query engine to filter all MS/MS scans, retaining only those with a product ion at m/z 98.9847 ± 50 ppm and peak intensity ≥ 50% of base peak.: "Apply the query engine to filter all MS/MS scans, retaining only those with a product ion at m/z 98.9847 ± 50 ppm and peak intensity ≥ 50% of base peak"
- [full_text] The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats: "The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats"
- [full_text] The parsing is done by using the lark Python library and specific Python code to transform a MassQL query to a parse tree: "The parsing is done by using the lark Python library and specific Python code to transform a MassQL query to a parse tree"
- [full_text] spectra in data frame format can optionally be saved as Apache feather files to cache data for repeated querying: "spectra in data frame format can optionally be saved as Apache feather files to cache data for repeated querying"
- [full_text] The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations: "The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations"
- [full_text] we first used the GNPS spectral libraries (which contained 4,533 reference spectra of bile acids) to design and refine MassQL queries: "we first used the GNPS spectral libraries to design and refine MassQL queries"
- [other] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%: "The unique compound was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%"
- [full_text] MassQL has limited capabilities to leverage more than a handful of MS spectra, for example, consecutive MS spectra arising: "MassQL has limited capabilities to leverage more than a handful of MS spectra, for example, consecutive MS spectra arising"
