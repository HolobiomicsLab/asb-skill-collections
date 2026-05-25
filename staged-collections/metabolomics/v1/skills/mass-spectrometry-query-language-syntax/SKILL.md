---
name: mass-spectrometry-query-language-syntax
description: Use when working in the metabolomics domain with LC-MS or GC-MS techniques to apply complex MS/MS filtering criteria such as precursor m/z, product ions, retention time, polarity, and ion mobility across mass spectrometry datasets.
when_to_use_negative:
- Do not use MassQL if you lack a well-defined fragmentation signature or product ion target. MassQL excels at hypothesis-driven filtering, not unbiased feature discovery.
- Do not use MassQL if your analysis requires leveraging consecutive MS spectra (e.g., isotope envelope fitting across multiple scans); the language has limited capability to process multi-scan chromatographic features.
- Do not use MassQL if your data is already annotated and you simply need to organize or cluster known compounds; it is designed for discovery and pattern matching, not for post-hoc metadata curation.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_3370
- http://edamontology.org/topic_0121
tools:
- name: lark
  role: Parses MassQL query strings into internal parse trees and data structures for execution
  repo: https://github.com/lark-parser/lark
- name: pyteomics
  role: Reads open-format MS data files (mzML, mzXML, MGF) and loads spectra into memory
- name: pandas
  role: Performs efficient data frame filtering and manipulation to apply query predicates
- name: Apache feather
  role: Caches parsed spectra for repeated querying and improved performance
- name: MZmine
  role: Open-source MS analysis software with native MassQL support for interactive querying
  repo: https://github.com/mzmine/mzmine
- name: MS-DIAL
  role: Open-source MS/MS data processing tool with integrated MassQL query capability
- name: MS-Cluster
  role: Collapses redundant MS/MS spectra from MassQL results into consensus spectra
- name: GNPS
  role: Public MS repository and molecular networking infrastructure supporting MassQL queries across millions of spectra
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1038/s41592-025-02660-z
    title: A universal language for finding mass spectrometry data patterns
schema_version: 0.2.0
derived_from:
- doi: 10.1038/s41592-025-02660-z
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/mass-spectrometry-query-language-syntax@sha256:83aff9096a427540d8ae2eed34b86b7a9b12504f276e76c5496bf341e3fd9066
---

# mass-spectrometry-query-language-syntax

## Summary

MassQL is a domain-specific query language for flexible, vendor-agnostic pattern matching across mass spectrometry datasets. It enables researchers to express complex MS/MS filtering criteria (precursor m/z, product ions, retention time, polarity, ion mobility) as human-readable query strings that are parsed into executable filters and applied across millions of spectra.

## When to use

Use MassQL syntax when you need to search large MS repositories (GNPS/MassIVE, Metabolomics Workbench, MetaboLights) for spectra matching specific fragmentation patterns—e.g., seeking all spectra with a phosphate product ion at m/z 98.9847 ± 50 ppm with ≥50% base peak intensity, or iron-characteristic isotope patterns across vendor-independent Q Exactive data. It is particularly suited when you have a well-defined chemical signature (a known product ion, precursor range, or retention time window) and need to scale that pattern across public or institutional datasets without manual interpretation.

## When NOT to use

- Do not use MassQL if you lack a well-defined fragmentation signature or product ion target. MassQL excels at hypothesis-driven filtering, not unbiased feature discovery.
- Do not use MassQL if your analysis requires leveraging consecutive MS spectra (e.g., isotope envelope fitting across multiple scans); the language has limited capability to process multi-scan chromatographic features.
- Do not use MassQL if your data is already annotated and you simply need to organize or cluster known compounds; it is designed for discovery and pattern matching, not for post-hoc metadata curation.

## Inputs

- MassQL query string (e.g., 'MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50')
- MS data files in mzML, mzXML, or MGF format from GNPS/MassIVE or local repositories
- Optional: pandas DataFrames or Apache feather-cached spectra

## Outputs

- Filtered MS/MS spectra in tabular format (CSV/TSV)
- Scan identifiers, precursor m/z, product ion m/z, intensity values, and metadata
- Consensus spectra (via MS-Cluster or Falcon-MS) for downstream molecular networking

## How to apply

Construct a MassQL query string using key–value pairs separated by colons (e.g., MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50). Define your target product ion m/z value, tolerance (in ppm), intensity thresholds (as percent of base peak), and optional filters (precursor m/z range via MS2PREC, retention time bounds via RTMIN/RTMAX, polarity, charge state, ion mobility). Parse the query using the lark parser library into an internal data structure. Load MS data from mzML, mzXML, or MGF formats using pyteomics and convert to pandas DataFrames (optionally caching as Apache feather files). Apply the query engine via pandas filtering to retain only MS/MS scans matching all criteria. Export matched spectra in tabular format (CSV/TSV) with scan identifiers, precursor m/z, product ion m/z, intensity values, and metadata. The choice of tolerance and intensity thresholds is critical: too loose and you retrieve thousands of false positives; too strict and you miss genuine low-intensity signals (as demonstrated by one siderophore whose 54Fe peak fell outside the 25% intensity tolerance).

## Related tools

- **lark** (Parses MassQL query strings into internal parse trees and data structures for execution) — https://github.com/lark-parser/lark
- **pyteomics** (Reads open-format MS data files (mzML, mzXML, MGF) and loads spectra into memory)
- **pandas** (Performs efficient data frame filtering and manipulation to apply query predicates)
- **Apache feather** (Caches parsed spectra for repeated querying and improved performance)
- **MZmine** (Open-source MS analysis software with native MassQL support for interactive querying) — https://github.com/mzmine/mzmine
- **MS-DIAL** (Open-source MS/MS data processing tool with integrated MassQL query capability)
- **MS-Cluster** (Collapses redundant MS/MS spectra from MassQL results into consensus spectra)
- **GNPS** (Public MS repository and molecular networking infrastructure supporting MassQL queries across millions of spectra)

## Examples

```
from massql import MassQueryLanguage; query = 'MS2PROD=98.9847:TOLERANCEPPM=50:INTENSITYPERCENT=50'; results = mql_engine.query(mzml_file, query); results.to_csv('phosphate_hits.csv')
```

## Evaluation signals

- Retrieved MS/MS spectra have product ion m/z within the specified tolerance (e.g., 98.9847 ± 50 ppm = 98.9717–98.9977 m/z) and intensity ≥ specified percent of base peak.
- Scan identifiers, precursor m/z, and metadata are correctly exported in output CSV/TSV without truncation or format errors.
- Query execution completes without parser errors; lark library successfully transforms the query string into a parse tree matching the MassQL grammar.
- Redundant spectra are consolidated via MS-Cluster (e.g., 589 raw spectra cluster into ~60 unique molecular features, as observed in the phosphate OPE example).
- Downstream molecular network or spectral library search validates that retrieved spectra correspond to intended chemical class (e.g., 51,310 of 338,439 OPE query results matched known OPEs in m/z space, and remaining 85% represent novel candidates).

## Limitations

- MassQL has limited capability to leverage multiple consecutive MS spectra from a single chromatographic feature; it is optimized for single-spectrum filtering and cannot easily model isotope envelopes or temporal peak shape across adjacent scans.
- Query results are sensitive to intensity tolerance: one siderophore was missed because its 54Fe peak intensity fell outside the expected 25% tolerance, highlighting the risk of false negatives with overly strict thresholds.
- MassQL does not natively integrate with spectral library annotation; 85–95% of discovered spectra remain unannotated after MassQL retrieval and require separate library matching and manual curation to yield putative identifications.
- Query performance scales linearly with dataset size (230 million MS/MS spectra searched takes proportionally longer); no built-in indexing or early termination is mentioned for very large repositories.

## Evidence

- [full_text] MassQL is agnostic to the instrument vendor, mass detector (for example, Orbitrap and quadrupole time-of-flight), ionization source (for example, electrospray ionization and matrix assisted laser: "MassQL is agnostic to the instrument vendor, mass detector (for example, Orbitrap and quadrupole time-of-flight), ionization source (for example, electrospray ionization and matrix assisted laser"
- [full_text] The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats: "The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats"
- [full_text] The parsing is done by using the lark Python library and specific Python code to transform a MassQL query to a parse tree: "The parsing is done by using the lark Python library and specific Python code to transform a MassQL query to a parse tree"
- [full_text] The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations: "The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations"
- [full_text] MassQL query found 338,439 [MS/MS spectra] for organophosphate ester phosphate product ion query: "To identify OPEs in public data, we scaled the MassQL query to all Q Exactive data in the GNPS/MassIVE data repository (which included >230 million MS/MS spectra). The MassQL query found 338,439"
- [full_text] MassQL has limited capabilities to leverage more than a handful of MS spectra, for example, consecutive MS spectra arising: "MassQL has limited capabilities to leverage more than a handful of MS spectra, for example, consecutive MS spectra arising"
- [full_text] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%: "The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%"
- [readme] Lark can parse all context-free languages… and do so efficiently. It also constructs an annotated parse-tree for you, using only the grammar and an input: "Lark can parse all context-free languages… It also constructs an annotated parse-tree for you, using only the grammar and an input"
