---
name: mass-spectrometry-isotope-pattern-recognition
description: Query MS1 and MS2 spectra to detect characteristic isotope patterns (e.g., iron-binding 54Fe/56Fe ratios, 13C peaks, characteristic adducts) using declarative pattern-matching language (MassQL) and filtering across open MS data repositories. This skill enables discovery of novel compounds sharing isotopic signatures without prior spectral library annotation.
when_to_use_negative:
- Input is already a feature table or aligned peak matrix; this skill operates on raw or processed spectra in standard open formats (mzML, mzXML, MGF), not tabular peak-intensity matrices.
- The isotope pattern of interest cannot be characterized quantitatively (e.g., relative intensity thresholds, mass offsets, or adduct m/z offsets are unknown or highly variable). The skill requires precise, measurable isotopic signature criteria.
- You need to correlate isotope patterns across consecutive eluting chromatographic features or exploit temporal covariance in retention time; MassQL has limited capability to leverage more than a handful of consecutive MS spectra from a single feature.
edam_operation: http://edamontology.org/operation_3644
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3370
tools:
- name: MassQL
  role: Query engine to define and execute declarative patterns on MS isotope signatures; parses query syntax into a searchable specification
  repo: https://github.com/mwang87/MassQueryLanguage
- name: lark
  role: Python parsing toolkit to convert MassQL query strings into parse trees and internal data structures
  repo: https://github.com/lark-parser/lark
- name: pyteomics
  role: Reads open MS data formats (mzML, mzXML, MGF) and loads spectra into memory for querying
- name: pandas
  role: DataFrames for in-memory filtering and manipulation of MS spectra during query execution
- name: MZmine
  role: Open-source MS data processing and visualization platform with native MassQL integration
  repo: https://github.com/mzmine/mzmine
- name: MS-Cluster
  role: Collapses redundant MS/MS spectra to generate consensus spectra from matched isotope-pattern hits
- name: Falcon-MS
  role: Alternative tool to collapse redundant MS/MS spectra and generate consensus spectra
- name: GNPS/MassIVE
  role: Public MS data repository (230 million+ MS/MS spectra, 97,109 files) for large-scale isotope pattern queries and spectral library search
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
    - outputs/audit_s41592_full/skills/mass-spectrometry-isotope-pattern-recognition/SKILL.md
    - outputs/audit_s41592_full/skills/mass-spectrometry-isotope-pattern-recognition/skill.md
    merged_at: '2026-05-25T07:15:30.952993+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/mass-spectrometry-isotope-pattern-recognition@sha256:384b6ea059a09edd1221b35d9e8d7adee2c5b956e6bc9ff4fbe80e22a0eb7137
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1038/s41592-025-02660-z
---

# mass-spectrometry-isotope-pattern-recognition

## Summary

Query MS1 and MS2 spectra to detect characteristic isotope patterns (e.g., iron-binding 54Fe/56Fe ratios, 13C peaks, characteristic adducts) using declarative pattern-matching language (MassQL) and filtering across open MS data repositories. This skill enables discovery of novel compounds sharing isotopic signatures without prior spectral library annotation.

## When to use

You have a high-resolution LC-MS or direct-injection MS dataset (mzML, mzXML, or MGF format) and want to discover compounds bearing a known isotopic signature—such as iron-binding siderophores (54Fe at 6.3% relative intensity to 56Fe with 13C peak and m/z x−52.91 apo adduct), organophosphate esters (characteristic phosphate product ion m/z), or other metal-chelating ligands. Use this skill when spectral library matching alone misses compounds, or when you need to scale a known isotope pattern across millions of spectra in public repositories (GNPS/MassIVE, Metabolomics Workbench, MetaboLights).

## When NOT to use

- Input is already a feature table or aligned peak matrix; this skill operates on raw or processed spectra in standard open formats (mzML, mzXML, MGF), not tabular peak-intensity matrices.
- The isotope pattern of interest cannot be characterized quantitatively (e.g., relative intensity thresholds, mass offsets, or adduct m/z offsets are unknown or highly variable). The skill requires precise, measurable isotopic signature criteria.
- You need to correlate isotope patterns across consecutive eluting chromatographic features or exploit temporal covariance in retention time; MassQL has limited capability to leverage more than a handful of consecutive MS spectra from a single feature.

## Inputs

- mzML or mzXML mass spectrometry data files from LC-MS or direct-injection instruments (Thermo Q Exactive, Orbitrap, quadrupole time-of-flight)
- MassQL query string defining isotope pattern criteria (MS1MZ, MS2PREC, MS2PROD, charge state, polarity, retention time, ion mobility)
- Reference MS/MS spectra library (e.g., GNPS spectral library) for query design and validation

## Outputs

- Matched MS1 or MS2 scan records in JSON or CSV format (scan number, precursor m/z, isotope pattern peak intensities, retention time, ion mobility)
- Consensus MS/MS spectra derived from redundant matches (using MS-Cluster or Falcon-MS)
- Molecular network created from consensus spectra in GNPS
- Annotations from spectral library search against public MS/MS libraries

## How to apply

First, design and validate your MassQL query against a reference dataset with known positive compounds (e.g., 4,533 reference spectra of bile acids or curated siderophores from GNPS libraries). Define conditions for all relevant isotope pattern criteria: target m/z value (MS1MZ), relative intensity thresholds (e.g., 25% tolerance for 54Fe peak), isotope mass offsets (13C peak at +1.003 Da), characteristic adducts (e.g., m/z x−52.91 for apo form), and optional retention-time or ion-mobility gates. Parse the query string using the lark parser library into an internal data structure. Read MS data files using pyteomics to load mzML/mzXML spectra into pandas DataFrames. Execute the query engine by filtering MS1 or MS2 records simultaneously against all isotope pattern criteria (10 ppm m/z accuracy). Cache results as Apache feather files for repeated querying. Export matched scan records (scan number, precursor m/z, isotope pattern intensities, retention time) in JSON or CSV format.

## Related tools

- **MassQL** (Query engine to define and execute declarative patterns on MS isotope signatures; parses query syntax into a searchable specification) — https://github.com/mwang87/MassQueryLanguage
- **lark** (Python parsing toolkit to convert MassQL query strings into parse trees and internal data structures) — https://github.com/lark-parser/lark
- **pyteomics** (Reads open MS data formats (mzML, mzXML, MGF) and loads spectra into memory for querying)
- **pandas** (DataFrames for in-memory filtering and manipulation of MS spectra during query execution)
- **MZmine** (Open-source MS data processing and visualization platform with native MassQL integration) — https://github.com/mzmine/mzmine
- **MS-Cluster** (Collapses redundant MS/MS spectra to generate consensus spectra from matched isotope-pattern hits)
- **Falcon-MS** (Alternative tool to collapse redundant MS/MS spectra and generate consensus spectra)
- **GNPS/MassIVE** (Public MS data repository (230 million+ MS/MS spectra, 97,109 files) for large-scale isotope pattern queries and spectral library search)

## Examples

```
from massql import msql_engine; query = 'MS1MZ=163.1 AND (MS1ISOTOPE=[54Fe,56Fe,13C] WITH INTENSITY_RATIO=[0.063,1.0,0.2] TOLERANCE=[0.25,0.25,0.25] PPM=10) AND MS1NEUTRAL_LOSS=52.91'; results = msql_engine.query(data_file='sample.mzML', query=query); results.to_csv('iron_binding_hits.csv')
```

## Evaluation signals

- Query retrieval rate: compare the count of matched spectra from the refined MassQL query to known positive compounds in the reference library (validation dataset). The E. lata example recovered 7 out of 8 previously identified siderophores plus 4 additional novel compounds, indicating >87.5% recall on known samples.
- Isotope pattern intensity fidelity: verify that all matched spectra exhibit isotope peak intensities (54Fe, 13C, apo adduct) within the query-specified tolerance windows (e.g., ±25% for iron isotope ratios, 10 ppm m/z accuracy). One missed siderophore fell outside 25% intensity tolerance, establishing a measurable failure boundary.
- Consensus spectrum count: after clustering redundant MS/MS matches with MS-Cluster or Falcon-MS, confirm that the consensus spectrum count is proportional to chemical diversity and instrument coverage (e.g., 7,504 consensus siderophore spectra from 26,944 raw matches; 2,777 consensus OPE spectra from 338,439 raw matches).
- Spectral library annotation rate: perform spectral library search against GNPS MS/MS libraries on consensus spectra; expect ~5% of consensus spectra to annotate to known compounds (441 / 7,504 siderophores; 153 / 2,777 OPEs in the article), leaving >95% as potential novel compounds requiring further investigation.
- Cross-method agreement: where available, compare isotope-pattern query results to an orthogonal discovery method (e.g., ion-identity molecular networking). The article found 4 additional siderophores via MassQL that were missed by IIMN, indicating complementarity rather than redundancy.

## Limitations

- Query sensitivity is bounded by isotope peak intensity tolerance: one siderophore with unusually low 54Fe peak intensity (falling outside the 25% tolerance window) was missed by MassQL but detected by ion-identity molecular networking, showing that strict intensity thresholds risk false negatives if biological or instrumental variation is high.
- MassQL has limited capability to leverage consecutive MS spectra from a single chromatographic feature or to exploit temporal covariance during elution. The skill operates on individual scan-by-scan filtering rather than feature-level integration, reducing sensitivity to compounds with weak or fluctuating isotope signatures across the peak.
- Spectral library annotation bottleneck: >95% of discovered consensus spectra remain unannotated by spectral library search, requiring downstream dereplication, manual curation, or complementary structure-elucidation workflows (NMR, MS/MS fragmentation modeling, or database querying) to assign chemistry to isotope-pattern hits.

## Evidence

- [other] the MassQL query identified seven out of eight putative siderophores in the Eutypa lata post-LC iron-addition dataset that were previously identified using ion-identity molecular networking, plus an additional four molecules not found by IIMN, for a total discovery of 11 iron-binding compounds: "The MassQL siderophore query identified seven out of eight putative siderophores in the Eutypa lata post-LC iron-addition dataset that were previously identified using ion-identity molecular"
- [other] Parse the MassQL siderophore query string into an internal data structure using the lark parser, defining conditions for MS1MZ iron isotope pattern (54Fe at 6.3% intensity relative to 56Fe), 13C peak, and proton-bound apo adduct at m/z x−52.91 with 25% intensity tolerance and 10 ppm m/z accuracy: "Parse the MassQL siderophore query string into an internal data structure using the lark parser, defining conditions for MS1MZ iron isotope pattern (54Fe at 6.3% intensity relative to 56Fe), 13C"
- [full_text] The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats: "The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats"
- [full_text] we first used the GNPS spectral libraries (which contained 4,533 reference spectra of bile acids) to design and refine MassQL queries: "we first used the GNPS spectral libraries (which contained 4,533 reference spectra of bile acids) to design and refine MassQL queries"
- [full_text] We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations: "We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations"
- [full_text] In searching over 230 million MS/MS spectra in 97,109 public data files, we retrieved 26,944 MS/MS spectra associated with the iron-characteristic isotope pattern: "In searching over 230 million MS/MS spectra in 97,109 public data files, we retrieved 26,944 MS/MS spectra associated with the iron-characteristic isotope pattern"
- [full_text] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%: "The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%"
- [full_text] MassQL has limited capabilities to leverage more than a handful of MS spectra, for example, consecutive MS spectra arising: "MassQL has limited capabilities to leverage more than a handful of MS spectra, for example, consecutive MS spectra arising"
- [full_text] because such a large fraction (>95%) of the analytes in the molecular network could not be annotated to known molecules (Fig. 2d), this molecular network is probably a rich resource for the discovery: "because such a large fraction (>95%) of the analytes in the molecular network could not be annotated to known molecules, this molecular network is probably a rich resource for discovery"
