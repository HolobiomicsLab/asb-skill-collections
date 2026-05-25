---
name: ms1-precursor-ion-filtering
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to filter MS1 spectra by precursor m/z value and isotope pattern intensity to isolate ions matching a target analyte class.
when_to_use_negative:
- Target analyte class has no characteristic isotope pattern or m/z signature (use untargeted feature detection instead)
- Input data is already annotated or filtered to a feature table (redundant application)
- MS1 resolution or mass accuracy is insufficient for the defined ppm tolerance (e.g., low-resolution quadrupole data with >50 ppm error)
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0769
- http://edamontology.org/topic_3172
tools:
- name: MassQL
  role: Query language and reference engine for parsing MS1 isotope pattern queries and executing filters on spectral DataFrames
  repo: https://github.com/mwang87/MassQueryLanguage
- name: lark
  role: Python parsing library used to parse MassQL query strings into an internal data structure and parse tree
  repo: https://github.com/lark-parser/lark
- name: pyteomics
  role: Python library to read open MS data file formats (mzML, mzXML, MGF) into pandas DataFrames
- name: pandas
  role: Data manipulation library used to filter DataFrame rows by m/z, intensity, and isotope pattern criteria
- name: MZmine
  role: Open-source MS data analysis tool with native MassQL support for executing MS1 precursor filtering workflows
  repo: https://github.com/mzmine/mzmine
- name: GNPS/MassIVE
  role: Public MS data repository from which reference datasets and large-scale MS1 scans are retrieved
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1038/s41592-025-02660-z
    title: A universal language for finding mass spectrometry data patterns
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_s41592_full/skills/ms1-precursor-ion-filtering/SKILL.md
    - outputs/audit_s41592_full/skills/ms1-precursor-ion-filtering/skill.md
    merged_at: '2026-05-25T06:57:01.583615+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/ms1-precursor-ion-filtering@sha256:1bcaf2d85da573ee3d1aa6c363146dec3916472b6fc4c8a7785171b784f825fc
derived_from:
- doi: 10.1038/s41592-025-02660-z
---

# MS1 Precursor Ion Filtering

## Summary

Filter MS1 spectra by precursor m/z value and isotope pattern intensity to isolate ions matching a target analyte class (e.g., iron-binding compounds, organophosphate esters). This skill enables targeted discovery of structurally related metabolites across large public repositories by applying precise m/z and intensity constraints to raw MS data.

## When to use

You have high-resolution MS1 data (mzML, mzXML, or MGF format) from a public repository (e.g., GNPS/MassIVE) and you want to retrieve all precursor ions matching a known isotope pattern or characteristic m/z signature. Use this skill when you have defined the target isotope pattern (m/z values, relative intensities, ppm tolerance) from reference compounds and need to scale that query across millions of MS1 scans without manual annotation.

## When NOT to use

- Target analyte class has no characteristic isotope pattern or m/z signature (use untargeted feature detection instead)
- Input data is already annotated or filtered to a feature table (redundant application)
- MS1 resolution or mass accuracy is insufficient for the defined ppm tolerance (e.g., low-resolution quadrupole data with >50 ppm error)

## Inputs

- MS1 spectral data in mzML, mzXML, or MGF format
- MassQL query string with MS1MZ, isotope pattern, and intensity tolerance specifications
- Reference dataset with known target compounds and their isotope patterns (optional, for query refinement)

## Outputs

- Filtered MS1 scan records (scan number, precursor m/z, isotope pattern intensities, retention time)
- JSON or CSV export of matched precursor ions
- Candidate list of MS1 scans for downstream MS/MS analysis or molecular networking

## How to apply

First, design the MassQL query string on a small reference dataset with known compounds, specifying the MS1MZ filter (target m/z), isotope pattern criteria (e.g., 54Fe at 6.3% relative intensity to 56Fe, 13C peak, apo adduct at m/z x−52.91), intensity tolerance (e.g., 25%), and mass accuracy (e.g., 10 ppm). Parse the query string using the lark Python library into an internal parse tree. Load MS data files from the repository using pyteomics into pandas DataFrames. Execute the query engine by filtering DataFrames row-by-row for scans matching all isotope pattern criteria simultaneously. Export matched precursor m/z, scan number, retention time, and isotope intensities to JSON or CSV. Validate by comparing the number of hits to known compounds in the reference set and checking that missed compounds fall outside the defined intensity tolerance bounds.

## Related tools

- **MassQL** (Query language and reference engine for parsing MS1 isotope pattern queries and executing filters on spectral DataFrames) — https://github.com/mwang87/MassQueryLanguage
- **lark** (Python parsing library used to parse MassQL query strings into an internal data structure and parse tree) — https://github.com/lark-parser/lark
- **pyteomics** (Python library to read open MS data file formats (mzML, mzXML, MGF) into pandas DataFrames)
- **pandas** (Data manipulation library used to filter DataFrame rows by m/z, intensity, and isotope pattern criteria)
- **MZmine** (Open-source MS data analysis tool with native MassQL support for executing MS1 precursor filtering workflows) — https://github.com/mzmine/mzmine
- **GNPS/MassIVE** (Public MS data repository from which reference datasets and large-scale MS1 scans are retrieved)

## Examples

```
from massql import query; results = query.spectrum_search("MS1MZ=163.1 MS1ISOTOPE=54Fe@6.3% INTENSITY_TOLERANCE=25 MASS_ACCURACY=10ppm", mzml_file="E_lata_post_LC_iron_addition.mzML"); results.to_csv("filtered_ms1_precursors.csv")
```

## Evaluation signals

- Number of matched MS1 scans equals or exceeds the count found using orthogonal methods (e.g., ion-identity molecular networking) on the same reference dataset
- All matched precursor m/z values fall within the specified ppm tolerance of the target m/z
- All matched isotope pattern intensities (e.g., 54Fe/56Fe ratio) fall within the specified tolerance (e.g., 25%)
- Missed compounds can be explained by falling outside defined thresholds (e.g., 54Fe peak intensity <6.3% - 25% = 3.8%)
- Retention time and scan number ranges are within the expected LC or data acquisition window

## Limitations

- MassQL has limited capability to leverage multiple consecutive MS1 spectra from the same chromatographic feature, reducing power for isotope pattern validation across an entire peak
- Query results depend critically on the intensity tolerance setting; compounds with low-intensity isotope peaks (e.g., 54Fe <3.8% for 6.3% ± 25%) will be missed
- MS1 filtering alone does not annotate or identify compounds; downstream MS/MS spectral matching is required to link filtered precursors to known metabolites
- Performance scales with repository size; searching >230 million MS/MS spectra across 97,109 files requires substantial computational resources and may take hours

## Evidence

- [other] Parse the MassQL siderophore query string into an internal data structure using the lark parser, defining conditions for MS1MZ iron isotope pattern (54Fe at 6.3% intensity relative to 56Fe), 13C peak, and proton-bound apo adduct at m/z x−52.91 with 25% intensity tolerance and 10 ppm m/z accuracy.: "Parse the MassQL siderophore query string into an internal data structure using the lark parser, defining conditions for MS1MZ iron isotope pattern (54Fe at 6.3% intensity relative to 56Fe), 13C"
- [full_text] The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats: "The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats"
- [full_text] The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations: "The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations"
- [full_text] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%: "The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%"
- [full_text] MassQL is agnostic to the instrument vendor, mass detector (for example, Orbitrap and quadrupole time-of-flight), ionization source (for example, electrospray ionization and matrix assisted laser: "MassQL is agnostic to the instrument vendor, mass detector (for example, Orbitrap and quadrupole time-of-flight), ionization source"
