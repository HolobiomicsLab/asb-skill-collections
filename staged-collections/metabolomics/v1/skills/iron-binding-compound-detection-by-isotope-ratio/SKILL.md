---
name: iron-binding-compound-detection-by-isotope-ratio
description: Use when analyzing metabolomics data through untargeted LC-MS or GC-MS to detect iron-binding compounds by querying for characteristic iron isotope patterns, specifically the 54Fe/56Fe ratio at 6.3% relative intensity, 13C peaks, and iron-specific neutral loss signatures.
when_to_use_negative:
- Input spectra are already identified by reference spectral libraries or high-confidence in-silico predictions; use library search first
- MS data lacks isotope resolution or m/z accuracy below ~10 ppm (e.g., low-resolution or time-of-flight instruments without sufficient calibration)
- Sample has not been exposed to iron stress, supplementation, or chelator addition; isotope patterns will be absent or too weak to detect against noise
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_3520
- http://edamontology.org/topic_0091
tools:
- name: MassQL
  role: Query language and execution engine for defining and filtering MS spectra by chemical pattern (isotope ratios, neutral losses, product ions)
  repo: https://github.com/mwang87/MassQueryLanguage
- name: lark
  role: Parser library used to transform MassQL query strings into parse trees for execution
  repo: https://github.com/lark-parser/lark
- name: pyteomics
  role: Python library to read open-format MS data files (mzML, mzXML, MGF) into memory
- name: pandas
  role: Data frame library for filtering and manipulating MS spectra records during query execution
- name: MS-Cluster or Falcon-MS
  role: Spectral clustering tool to collapse redundant MS/MS observations into consensus spectra
- name: GNPS
  role: Global Natural Products Social Molecular Networking platform for creating consensus networks and spectral library annotation of iron-binding compound hits
- name: MZmine
  role: Open-source MS data analysis software with native MassQL integration for query execution and visualization
  repo: https://github.com/mzmine/mzmine
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1038/s41592-025-02660-z
    title: A universal language for finding mass spectrometry data patterns
schema_version: 0.2.0
derived_from:
- doi: 10.1038/s41592-025-02660-z
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/iron-binding-compound-detection-by-isotope-ratio@sha256:e7a4f6c833bd1e101b0e2bdcaadc1e7b1a29bcc24dc0b8ebd6183b7ea2a46e8f
---

# iron-binding-compound-detection-by-isotope-ratio

## Summary

Detect iron-binding compounds (siderophores) in untargeted mass spectrometry datasets by querying for characteristic iron isotope patterns (54Fe/56Fe ratio at 6.3% relative intensity), 13C peaks, and iron-specific neutral loss signatures. This skill enables discovery of novel iron-chelators across large public MS repositories without prior spectral library matches.

## When to use

You have high-resolution MS1 or MS2 spectra from iron-supplemented or iron-limited microbial or plant samples and want to discover iron-binding metabolites beyond what spectral library matching or ion-identity molecular networking can find. Use this skill when you need to identify isotope-defined chemical signatures (54Fe, 56Fe, 57Fe, 58Fe patterns) with known natural abundances and intensity tolerances across thousands to millions of spectra.

## When NOT to use

- Input spectra are already identified by reference spectral libraries or high-confidence in-silico predictions; use library search first
- MS data lacks isotope resolution or m/z accuracy below ~10 ppm (e.g., low-resolution or time-of-flight instruments without sufficient calibration)
- Sample has not been exposed to iron stress, supplementation, or chelator addition; isotope patterns will be absent or too weak to detect against noise

## Inputs

- High-resolution MS1 or MS/MS spectra in mzML, mzXML, or MGF format
- Iron-supplemented or iron-limited sample datasets (e.g., post-LC iron-addition datasets)
- MassQL query string defining isotope pattern criteria (54Fe/56Fe ratio, 13C peak, apo adduct m/z offset)

## Outputs

- JSON or CSV table of matched MS scans with scan number, precursor m/z, isotope peak intensities, retention time
- Consensus MS/MS spectra (collapsed redundant observations)
- Molecular network in GNPS format linking related iron-binding compounds

## How to apply

Parse a MassQL query string specifying the iron isotope pattern criteria (54Fe at 6.3% relative intensity to 56Fe baseline, 13C peak presence, proton-bound apo adduct at m/z x−52.91 with 25% intensity tolerance, 10 ppm m/z accuracy) using the lark parser into an internal parse tree. Load MS data files in mzML, mzXML, or MGF format using pyteomics into pandas DataFrames, preserving scan number, precursor m/z, retention time, and peak intensity arrays. Execute the parsed query engine by filtering MS1 spectra simultaneously against all four isotope pattern criteria using pandas boolean indexing. Export matched scans as JSON or CSV, recording scan identifiers, isotope peak intensities, m/z values, and retention times. Cluster redundant observations across multiple scans of the same feature using MS-Cluster or Falcon-MS, then construct a molecular network in GNPS to organize and annotate the consensus spectra, recognizing that >95% will remain unannotated and represent discovery opportunities.

## Related tools

- **MassQL** (Query language and execution engine for defining and filtering MS spectra by chemical pattern (isotope ratios, neutral losses, product ions)) — https://github.com/mwang87/MassQueryLanguage
- **lark** (Parser library used to transform MassQL query strings into parse trees for execution) — https://github.com/lark-parser/lark
- **pyteomics** (Python library to read open-format MS data files (mzML, mzXML, MGF) into memory)
- **pandas** (Data frame library for filtering and manipulating MS spectra records during query execution)
- **MS-Cluster or Falcon-MS** (Spectral clustering tool to collapse redundant MS/MS observations into consensus spectra)
- **GNPS** (Global Natural Products Social Molecular Networking platform for creating consensus networks and spectral library annotation of iron-binding compound hits)
- **MZmine** (Open-source MS data analysis software with native MassQL integration for query execution and visualization) — https://github.com/mzmine/mzmine

## Examples

```
from lark import Lark; import pyteomics.mzml; import pandas as pd; query_str = 'QUERY: [MS1MZ=54Fe (intensity: 6.3%)] AND [MS1MZ=13C] AND [MS2PREC apo adduct at m/z x-52.91 (intensity: 25% tol, 10 ppm accuracy)]'; parser = Lark(query_grammar); tree = parser.parse(query_str); spectra_df = pd.DataFrame([s for s in pyteomics.mzml.read('eutypa_lata_iron.mzML')]); matched = spectra_df[spectra_df['has_54Fe'] & spectra_df['has_13C'] & spectra_df['has_apo_adduct']]; matched.to_csv('iron_hits.csv')
```

## Evaluation signals

- Query execution yields ≥7 known reference siderophores (from IIMN or spectral library) in the E. lata validation dataset, confirming isotope pattern specificity
- Total number of matched scans and consensus spectra generated match expected ranges (11 iron-binding compounds in small datasets; >7,500 consensus spectra in repository-scale searches with 230M+ MS/MS spectra)
- Matched scans exhibit 54Fe/56Fe intensity ratios within 6.3% ± 25% tolerance (the stated acceptance window)
- Matched scans possess apo adduct peaks at m/z x−52.91 ± 10 ppm, confirming iron-neutral-loss signature
- Molecular network annotation shows ≥5% of consensus spectra match GNPS spectral libraries (expected for siderophores); remaining >95% are candidates for de novo discovery
- Isotope pattern from one siderophore with 54Fe peak intensity outside 25% tolerance falls below the match threshold, confirming intensity cutoff is enforced

## Limitations

- MassQL has limited capability to leverage multiple consecutive MS spectra from the same chromatographic feature; single-spectrum or few-spectrum queries are more reliable
- Siderophores with low-intensity 54Fe peaks (>25% deviation from expected 6.3% relative intensity) will be missed by the isotope pattern filter, even if genuine iron-binders
- Requires high-resolution (Orbitrap or quadrupole-TOF) instruments with ≤10 ppm m/z accuracy; low-resolution instruments cannot resolve iron isotopes adequately
- Query assumes proton-bound [M+H]+ or [M−Fe+H]+ adducts; other adduct types (e.g., [M+Na]+, [M+NH4]+) require separate query formulation

## Evidence

- [results] The MassQL siderophore query identified seven out of eight putative siderophores in the Eutypa lata post-LC iron-addition dataset that were previously identified using ion-identity molecular networking, plus an additional four molecules not found by IIMN, for a total discovery of 11 iron-binding compounds.: "The MassQL siderophore query identified seven out of eight putative siderophores in the Eutypa lata post-LC iron-addition dataset that were previously identified using ion-identity molecular"
- [methods] Parse the MassQL siderophore query string into an internal data structure using the lark parser, defining conditions for MS1MZ iron isotope pattern (54Fe at 6.3% intensity relative to 56Fe), 13C peak, and proton-bound apo adduct at m/z x−52.91 with 25% intensity tolerance and 10 ppm m/z accuracy.: "Parse the MassQL siderophore query string into an internal data structure using the lark parser, defining conditions for MS1MZ iron isotope pattern (54Fe at 6.3% intensity relative to 56Fe), 13C"
- [full_text] The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats: "The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats"
- [full_text] The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations: "The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations"
- [full_text] We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations: "We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations"
- [results] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%: "The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%"
- [full_text] MassQL has limited capabilities to leverage more than a handful of MS spectra, for example, consecutive MS spectra arising from a chromatographic feature: "MassQL has limited capabilities to leverage more than a handful of MS spectra, for example, consecutive MS spectra arising from a chromatographic feature"
- [full_text] Using these consensus spectra, we created a molecular network in GNPS: "Using these consensus spectra, we created a molecular network in GNPS"
