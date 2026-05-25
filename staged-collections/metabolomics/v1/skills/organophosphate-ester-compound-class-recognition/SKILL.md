---
name: organophosphate-ester-compound-class-recognition
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to recognize organophosphate ester (OPE) compounds in high-resolution LC-MS/MS data by querying for a diagnostic phosphate product ion (H₄PO₄⁺, m/z 98.9847) using MassQL.
when_to_use_negative:
- Input is already a curated feature table or consensus spectrum library; use this skill on raw or minimally processed MS/MS data, not post-feature-detection outputs.
- Your analytical goal is quantitative OPE measurement or pharmacokinetics; this skill performs untargeted class discovery and produces primarily qualitative/putative identifications.
- MS data is from low-resolution instruments (e.g., nominal-mass quadrupole) where 50 ppm tolerance and intensity ratios cannot be reliably resolved.
- You require detection of OPE metabolites or degradation products that have lost the phosphate fragment; this query is specific to intact OPEs with H₄PO₄⁺ as a major product ion.
edam_operation: http://edamontology.org/operation_3632
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3520
tools:
- name: MassQL
  role: Core query language and execution engine for MS/MS pattern matching; parses OPE phosphate fragment query and filters spectra by product ion m/z and intensity.
  repo: https://github.com/mwang87/MassQueryLanguage
- name: lark parser
  role: Parses MassQL query string into abstract syntax tree for downstream filtering logic.
  repo: https://github.com/lark-parser/lark
- name: pyteomics
  role: Reads raw MS data from mzML, mzXML, and MGF formats into Python data structures for query processing.
- name: pandas
  role: Provides DataFrame-based filtering and data manipulation for MS/MS spectra by product ion m/z and intensity constraints.
- name: Apache Feather
  role: Optional caching format for rapid re-querying of large MS datasets across multiple refinements.
- name: GNPS/MassIVE
  role: Public repository of >230 million MS/MS spectra for large-scale OPE class discovery; also hosts spectral libraries for putative annotation.
  repo: https://gnps.ucsd.edu
- name: MS-Cluster
  role: Collapses redundant MS/MS spectra from query results into consensus spectra for downstream molecular networking.
- name: Falcon-MS
  role: Alternative tool for consensus spectrum generation from redundant OPE query hits.
- name: MZmine
  role: Open-source MS analysis platform with native MassQL support for integrated query execution and visualization.
  repo: https://github.com/mzmine/mzmine
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
    - outputs/audit_s41592_full/skills/organophosphate-ester-compound-class-recognition/SKILL.md
    - outputs/audit_s41592_full/skills/organophosphate-ester-compound-class-recognition/skill.md
    merged_at: '2026-05-25T07:33:56.399532+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/organophosphate-ester-compound-class-recognition@sha256:3c3f43164b8833ee913efd09f50aa95a61f509112a8f3940c47febc506f0e9a4
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1038/s41592-025-02660-z
---

# organophosphate-ester-compound-class-recognition

## Summary

Recognize organophosphate ester (OPE) compounds in high-resolution LC-MS/MS data by querying for a diagnostic phosphate product ion (H₄PO₄⁺, m/z 98.9847) using MassQL, enabling discovery of known and novel OPE structures across large public repositories. This skill leverages a class-selective fragmentation pattern rather than precursor m/z to identify compounds with diverse molecular weights and structures that share a common metabolic or synthetic route.

## When to use

You have untargeted or semi-targeted LC-MS/MS data (mzML, mzXML, or MGF format) from environmental, biological, or food samples and suspect the presence of organophosphate esters—either as known contaminants or as part of a chemical class discovery effort. Use this skill when: (1) you want to query across instrument vendors and ionization sources without rebuilding methods; (2) you have access to public repositories (GNPS/MassIVE, Metabolomics Workbench, MetaboLights) and wish to search >230 million spectra; (3) you want to identify both annotated OPEs and novel OPE-like compounds that share the diagnostic phosphate fragment; (4) your analytical goal is to move from single-compound detection to comprehensive class-level compound discovery.

## When NOT to use

- Input is already a curated feature table or consensus spectrum library; use this skill on raw or minimally processed MS/MS data, not post-feature-detection outputs.
- Your analytical goal is quantitative OPE measurement or pharmacokinetics; this skill performs untargeted class discovery and produces primarily qualitative/putative identifications.
- MS data is from low-resolution instruments (e.g., nominal-mass quadrupole) where 50 ppm tolerance and intensity ratios cannot be reliably resolved.
- You require detection of OPE metabolites or degradation products that have lost the phosphate fragment; this query is specific to intact OPEs with H₄PO₄⁺ as a major product ion.

## Inputs

- LC-MS/MS data in mzML, mzXML, or MGF format (raw or processed)
- MassQL query string specifying MS2PROD, TOLERANCEPPM, INTENSITYPERCENT filters
- Reference OPE spectral library (optional, for validation)

## Outputs

- CSV/TSV table of matched MS/MS spectra (scan ID, precursor m/z, product m/z, intensity, metadata)
- Consensus MS/MS spectra from redundancy clustering (e.g., 2,777 consensus OPE spectra)
- Molecular network in GNPS format for community annotation
- Putative OPE identities from spectral library search (typically ~5% of consensus spectra)

## How to apply

Construct a MassQL query string targeting the phosphate product ion diagnostic of OPEs: 'MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50'. This specifies: m/z 98.9847 ± 50 ppm (H₄PO₄⁺ fragment) with intensity ≥50% of base peak. Parse the query using the lark parser to build an internal syntax tree. Load MS/MS data into pandas DataFrames using pyteomics, optionally caching as Apache feather files for rapid re-querying. Apply the query engine to filter all MS/MS scans, retaining only those satisfying the product ion and intensity constraints. Export matched spectra (scan ID, precursor m/z, product m/z, intensity) in tabular CSV/TSV format. To prioritize known OPEs: cross-validate precursor m/z against reference OPE standards with 20 ppm mass error tolerance; only ~15% of retrieved spectra typically match known OPEs, so remaining results represent high-value discovery candidates. Cluster redundant spectra using MS-Cluster or Falcon-MS, then construct a molecular network in GNPS for spectral library matching and community annotation.

## Related tools

- **MassQL** (Core query language and execution engine for MS/MS pattern matching; parses OPE phosphate fragment query and filters spectra by product ion m/z and intensity.) — https://github.com/mwang87/MassQueryLanguage
- **lark parser** (Parses MassQL query string into abstract syntax tree for downstream filtering logic.) — https://github.com/lark-parser/lark
- **pyteomics** (Reads raw MS data from mzML, mzXML, and MGF formats into Python data structures for query processing.)
- **pandas** (Provides DataFrame-based filtering and data manipulation for MS/MS spectra by product ion m/z and intensity constraints.)
- **Apache Feather** (Optional caching format for rapid re-querying of large MS datasets across multiple refinements.)
- **GNPS/MassIVE** (Public repository of >230 million MS/MS spectra for large-scale OPE class discovery; also hosts spectral libraries for putative annotation.) — https://gnps.ucsd.edu
- **MS-Cluster** (Collapses redundant MS/MS spectra from query results into consensus spectra for downstream molecular networking.)
- **Falcon-MS** (Alternative tool for consensus spectrum generation from redundant OPE query hits.)
- **MZmine** (Open-source MS analysis platform with native MassQL support for integrated query execution and visualization.) — https://github.com/mzmine/mzmine

## Examples

```
massql_query = 'MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50'; spectra_df = query_engine.execute(query_string=massql_query, data_file='marine_water_lcmsms.mzML', output_format='csv')
```

## Evaluation signals

- Query execution completes without parsing errors; lark parser successfully converts 'MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50' into valid filter logic.
- Retrieved spectrum count is in expected range: >1,000 spectra for focused LC-MS/MS runs on contaminated samples; >100,000 when querying public repositories like GNPS/MassIVE.
- Precursor m/z distribution of matched spectra spans expected OPE molecular weight range (~300–500 m/z for typical organophosphate esters); outliers indicate potential false positives.
- Cross-validation: when querying reference OPE standards (e.g., TPHP, TDBP), ≥80% of known OPEs are retrieved with precursor m/z within ±20 ppm of theoretical; <5% false-negatives indicate adequate query stringency.
- Consensus spectrum clustering reduces >100,000 matched spectra to 1,000–10,000 unique clusters, consistent with chemical diversity of OPE class; clustering coefficient and network modularity are interpretable.
- Spectral library search recovers known OPEs in top hits (cosine similarity >0.7) for ~5–10% of consensus spectra; remaining unannotated spectra represent novel OPE-like compounds with intact phosphate fragment.

## Limitations

- MassQL cannot leverage multiple consecutive MS spectra from a single chromatographic feature; isotope patterns and adduct trains must be manually integrated post-query.
- Spectra with low-intensity phosphate peaks (e.g., 54Fe isotopologues or minor fragments <25% base peak intensity) may fall outside the INTENSITYPERCENT=50 threshold and be missed; sensitivity depends on ionization efficiency and instrument tuning.
- The H₄PO₄⁺ (m/z 98.9847) fragment is diagnostic for OPEs with phosphate moieties but does NOT detect OPE metabolites, degradation products, or structural isomers that have lost the phosphate group during fragmentation.
- Queries across >230 million spectra in GNPS/MassIVE are computationally expensive and may require server-side caching or batch processing; repeated refinements of TOLERANCEPPM or INTENSITYPERCENT may require re-execution.
- False-positive rate increases in samples with high background phosphorus-containing compounds (e.g., nucleotides, phospholipids, fertilizer residues); post-hoc filtering by precursor m/z against known OPE standards (±20 ppm) is recommended to reduce ~85% noise.
- Consensus spectrum generation and molecular networking introduce additional parameter choices (clustering threshold, network edge cutoff) that can affect final annotation yield (~5% of spectra typically match spectral libraries); user expertise in GNPS workflows is required for rigorous compound assignment.

## Evidence

- [full_text] MassQL phosphate fragment query for OPE class recognition: "Execute MassQL phosphate product-ion MS2 query (MS2PROD=98.9847, TOLERANCEPPM=50, INTENSITYPERCENT=50) on a marine water test dataset to retrieve candidate OPE spectra"
- [full_text] Discovery scope and false-positive rate in public repositories: "The MassQL query found 338,439 MS/MS spectra matching organophosphate ester phosphate product ion query. Only 15% (51,310) of the MS/MS found by MassQL could be explained (precursor m/z match with 20"
- [full_text] Workflow: query parsing and MS data filtering: "Parse the MassQL query string using the lark parser to construct an internal query data structure. Load MS data into pandas data frames using pyteomics. Apply the query engine to filter all MS/MS"
- [full_text] Redundancy clustering and network annotation for OPE discovery: "We extracted all MS/MS spectra and created consensus MS/MS spectra using Falcon-MS, resulting in 2,777 consensus spectra. We used these consensus spectra to create a molecular network."
- [full_text] Annotation yield and novel compound discovery: "Combining the spectral library search and the molecular network, we putatively identified 153 of the 2,777 consensus OPE spectra (5.5%). The remaining 94.5% represent potential novel OPE-like"
- [full_text] Instrument and vendor agnostic design: "MassQL is agnostic to the instrument vendor, mass detector (for example, Orbitrap and quadrupole time-of-flight), ionization source (for example, electrospray ionization)"
- [full_text] Data caching and optimization for repeated queries: "spectra in data frame format can optionally be saved as Apache feather files to cache data for repeated querying"
- [full_text] Export format and metadata preservation: "Export matched MS/MS spectra in tabular format (CSV/TSV) with scan identifiers, precursor m/z, product ion m/z, intensity values, and metadata."
