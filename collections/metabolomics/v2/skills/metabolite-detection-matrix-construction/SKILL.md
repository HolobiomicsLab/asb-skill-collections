---
name: metabolite-detection-matrix-construction
description: Use when after GNPS spectral library matching has been completed on a batch of MS2 spectra from public MassIVE datasets and you need to aggregate chemical annotations into a tabular format suitable for downstream comparative metabolomics, co-analysis, or chemical explorer visualizations across.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3790
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - MassIVE
  - GNPS
  - ReDU
  - Emperor
  techniques:
  - CE-MS
derived_from:
- doi: 10.1038/s41592-020-0916-7
  title: ReDU
- doi: 10.1186/2047-217x-2-16
  title: ''
evidence_spans:
- ReDU only interacts with MassIVE
- data uploaded to MassIVE as a public dataset
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_redu_cq
    doi: 10.1038/s41592-020-0916-7
    title: ReDU
  dedup_kept_from: coll_redu_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-020-0916-7
  all_source_dois:
  - 10.1038/s41592-020-0916-7
  - 10.1186/2047-217x-2-16
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-detection-matrix-construction

## Summary

Construct a binary detection matrix from GNPS spectral library search results, where rows represent MS files, columns represent chemically annotated compounds, and cells encode presence (1) or absence (0) of each metabolite. This enables pooled statistical and exploratory analysis of public tandem MS datasets at repository scale.

## When to use

After GNPS spectral library matching has been completed on a batch of MS2 spectra from public MassIVE datasets and you need to aggregate chemical annotations into a tabular format suitable for downstream comparative metabolomics, co-analysis, or chemical explorer visualizations across multiple files.

## When NOT to use

- Input spectra have not yet been searched against GNPS spectral library (run GNPS workflow first)
- You require quantitative abundance or peak intensity information rather than presence/absence calls (this skill produces only binary calls)
- Spectral library matching results are already formatted as a detection matrix or feature table

## Inputs

- GNPS spectral library search results table (TSV or CSV with columns: MS file identifier, matched compound name, m/z, cosine similarity score, spectral library reference ID)
- List of MS input files analyzed (MassIVE file identifiers or local file names)

## Outputs

- Binary detection matrix (TSV): rows = MS files, columns = chemical identities, values = 0 or 1
- Tab-separated values file suitable for ReDU chemical explorer and attribute filtering

## How to apply

Retrieve the GNPS spectral library matching results table, which contains matched chemical annotations, m/z values, and cosine similarity scores for each MS2 spectrum. For each unique chemical identity (matched compound name or spectral library entry) and each input MS file, determine presence by checking whether at least one MS2 spectrum in that file yielded a significant match (typically cosine similarity > 0.7 or as per GNPS default thresholds). Construct a two-dimensional table with files as rows and chemical identities as columns, populating cells with 1 (detected in that file) or 0 (not detected). Account for the fact that the same chemical may produce multiple GNPS annotations due to slight MS2 spectral variation, so either merge annotations by parent compound class or explicitly retain the multiple entries. Export as a tab-separated values file for compatibility with downstream analysis tools and ReDU filtering workflows.

## Related tools

- **GNPS** (Performs spectral library matching against reference MS/MS fragmentation patterns to generate chemical annotations with cosine similarity scores) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **MassIVE** (Public repository and data source for raw MS2 spectra in open formats (.mzML, .mzXML); ReDU retrieves MS files from MassIVE) — https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp
- **ReDU** (Web interface that integrates GNPS results and enables filtering, visualization, and comparative analysis of detection matrices across public datasets) — https://github.com/mwang87/ReDU-MS2-GNPS
- **Emperor** (Visualization and interactive analysis tool for high-dimensional metabolomics data, accepts detection matrices for PCA score plots and exploratory analysis) — https://github.com/biocore/emperor

## Evaluation signals

- Detection matrix dimensions match expected number of input files (rows) and unique GNPS-matched compounds (columns)
- All cells contain only binary values (0 or 1); no missing values, negative numbers, or fractional values are present
- Sum of 1s for each chemical (column) is > 0 and ≤ total number of files (i.e., each detected compound appears in at least one but not necessarily all files)
- File names in rows correspond exactly to input MassIVE identifiers or accession numbers provided to GNPS workflow
- Chemical compound names in columns match GNPS library reference IDs; if duplicate annotations for the same compound exist due to spectral variation, verify they are either merged or distinctly labeled
- Tab-separated file format is valid (no embedded tabs in chemical names; proper line breaks; UTF-8 encoding)

## Limitations

- Detection matrix records only presence/absence and loses quantitative spectral abundance or cosine similarity score information; downstream statistical power depends on sufficient biological or technical replication
- The same chemical can have multiple distinct GNPS annotations due to slight MS/MS spectral variation, requiring manual curation or consolidation by parent compound class before integration into a unified detection matrix
- GNPS spectral library matching produces only level 2 or level 3 metabolomics identifications (putative annotation based on library similarity or compound class), not definitive structure confirmation; users must interpret biochemical meaning accordingly
- Missing MS/MS spectra or spectra that fail to match the GNPS library are recorded as 0 (not detected), which conflates true absence from a biological absence of library match; reanalysis with alternative spectral libraries or fragment ion databases may reveal additional detections

## Evidence

- [other] GNPS library search compares MS2 product-ion spectra against reference fragmentation patterns in its public spectral library, producing tabulated chemical annotations with file detection information—a matrix where cells indicate whether each chemical was detected (1) or not detected (0) in each file.: "producing tabulated chemical annotations with file detection information—a matrix where cells indicate whether each chemical was detected (1) or not detected (0) in each file"
- [other] Parse the GNPS output to construct a binary detection matrix (rows = files, columns = chemical identities, values = 1 for detected, 0 for not detected) and export as a tab-separated table.: "Parse the GNPS output to construct a binary detection matrix (rows = files, columns = chemical identities, values = 1 for detected, 0 for not detected) and export as a tab-separated table"
- [other] The same chemical can have multiple GNPS annotations due to slight variation in MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra cause the pattern to match different reference MS2 spectra for the same chemical"
- [other] GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on: "GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class"
- [other] Chemical annotation is performed in [GNPS](https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp) by comparing MS2 spectra: "Chemical annotation is performed in GNPS by comparing MS2 spectra"
- [readme] Download from Google Sheets as a tab separated text file using **"File-Download as" and selecting "Tab-seperated values...": "Download from Google Sheets as a tab separated text file using **"File-Download as" and selecting "Tab-seperated values...""
