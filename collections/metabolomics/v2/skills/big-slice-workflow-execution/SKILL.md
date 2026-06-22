---
name: big-slice-workflow-execution
description: Use when you have a collection of antiSMASH-processed GenBank files (or custom BGC GenBank files prepared via the provided converter script) organized in a structured input folder, and you want to cluster them into Gene Cluster Families (GCFs) to chart biosynthetic diversity or identify.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0630
  tools:
  - BiG-SLiCE
  - pyHMMER
  - antiSMASH v7.0.0
  - Flask
derived_from:
- doi: 10.1093/gigascience/giaa154
  title: BiG-SLiCE
evidence_spans:
- '**BiG-SLiCE** using pip'
- Ability to __export pre-calculated BGCs and GCFs table into TSVs__ (use __--export-csv__ parameter)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_big_slice_cq
    doi: 10.1093/gigascience/giaa154
    title: BiG-SLiCE
  dedup_kept_from: coll_big_slice_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa154
  all_source_dois:
  - 10.1093/gigascience/giaa154
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# big-slice-workflow-execution

## Summary

Execute a complete BiG-SLiCE v2.0 clustering analysis pipeline on a folder of antiSMASH-annotated BGC GenBank files to generate Gene Cluster Family (GCF) models, BGC-to-GCF assignments, and interactive visualization outputs. This skill applies when you have assembled microbial genomes with predicted biosynthetic gene clusters and need to perform comparative clustering analysis at scale using cosine-like (l2-normalized) distances and PFAM 35.0 HMM models.

## When to use

You have a collection of antiSMASH-processed GenBank files (or custom BGC GenBank files prepared via the provided converter script) organized in a structured input folder, and you want to cluster them into Gene Cluster Families (GCFs) to chart biosynthetic diversity or identify functionally related BGCs. This is the entry point for any large-scale BiG-SLiCE comparative analysis.

## When NOT to use

- Your GenBank files are not annotated with BGC boundaries or domain predictions (input must be antiSMASH v7.0.0 or equivalent; raw genome GenBank alone is insufficient)
- You only need to query a single BGC against pre-existing GCF models (use --query mode instead of full workflow execution)
- Your input data is already in tabular TSV format rather than GenBank; use --export-csv on a completed run to convert outputs

## Inputs

- antiSMASH GenBank files or custom BGC GenBank files (prepared via converter script)
- Input folder organized per BiG-SLiCE wiki specification
- Downloaded HMM database (PFAM 35.0, antiSMASH v7.0.0 definitions)

## Outputs

- SQLite3 database containing preprocessed BGC and GCF data
- Pre-calculated BGC and GCF cluster tables (TSV format if --export-csv is used)
- Flask web-app scripts and requirements.txt for interactive visualization
- Clustered BGCs assigned to Gene Cluster Families (GCFs)

## How to apply

First, ensure BiG-SLiCE v2.0 is installed via pip (e.g., `pip install bigslice` for stable release or from source for bleeding edge). Download the latest HMM database (~271 MB gzipped) using `download_bigslice_hmmdb`, which updates to PFAM 35.0 and antiSMASH v7.0.0 definitions. Organize your BGC GenBank files following the wiki Input folder structure (or use the provided example template). Invoke BiG-SLiCE with `bigslice -i <input_folder> <output_folder>`, which will perform full clustering using cosine-like distances via l2-normalization. The analysis outputs an SQLite3 database, pre-calculated BGC and GCF tables, and a Flask-based interactive web visualization. Verify successful execution by checking version output (`bigslice --version`) to confirm HMM database version and checksums match your expectations.

## Related tools

- **BiG-SLiCE** (Primary clustering engine that performs cosine-like distance calculations via l2-normalization, assigns BGCs to GCFs, and generates database and visualization outputs) — https://github.com/medema-group/bigslice
- **pyHMMER** (Cython-based HMMER3 bindings providing sequence homology searches against PFAM 35.0 models; replaces standalone HMMER for speed gains and pip-based installation) — https://github.com/althonos/pyhmmer
- **antiSMASH v7.0.0** (Upstream tool that annotates genomes with BGC predictions and domain predictions; BiG-SLiCE ingests its GenBank output)
- **Flask** (Python web framework powering the interactive visualization interface; run via start_server.sh after installing requirements.txt)

## Examples

```
bigslice -i <input_folder> <output_folder>
```

## Evaluation signals

- Verify `bigslice --version` output shows expected HMM database version and matching MD5 checksums for Biosynthetic-pfam and Sub-pfam models
- Confirm output folder contains an SQLite3 database file and a start_server.sh script with associated requirements.txt for web visualization
- Run SQL queries on the output database to retrieve BGC and GCF records; verify row counts are non-zero and match input GenBank count
- Launch the Flask web app via `bash <output_folder>/start_server.sh` and verify the browser interface loads without 500 errors and displays GCF clusters and BGC assignments
- If --export-csv was used, verify TSV files are generated and contain expected columns (e.g., BGC IDs, GCF assignments, distance scores) with no parsing errors

## Limitations

- Input GenBank files must conform to antiSMASH v7.0.0 schema; BGCs prepared with older antiSMASH versions or non-standard tools may produce incomplete or incorrect annotations
- Clustering distance metric is now l2-normalized cosine-like distance; results are not directly comparable to BiG-SLiCE v1.x, which used different distance calculations
- The README notes that no pre-processed GCF reference database is currently available for BiG-SLiCE v2.0 (unlike v1.x), limiting direct comparison to existing published datasets
- HMM database download is ~271 MB gzipped and must be fetched separately; installation will fail if download_bigslice_hmmdb is not executed

## Evidence

- [readme] Install BiG-SLiCE using pip from stable or source; fetch latest HMM models; verify with bigslice --version: "Install **BiG-SLiCE** using pip: ... from PyPI (stable) ... from source (bleeding edge) ... Fetch the latest HMM models (± 271MB gzipped): ... Check your installation: bigslice --version"
- [readme] Clustering uses cosine-like distances via l2-normalization and updated PFAM 35.0: "Clustering now uses __cosine-like__ (via l2-normalization) distances ... pHMM databases have been updated to __PFAM 35.0__"
- [readme] pyHMMER replaces HMMER for speed and pip installation: "Switching from HMMER to [pyHMMER](https://github.com/althonos/pyhmmer) (__speed-ups__, can now be fully installed via __pip__)"
- [readme] TSV export capability using --export-csv parameter: "Ability to __export pre-calculated BGCs and GCFs table into TSVs__ (use __--export-csv__ parameter)"
- [readme] Flask-based interactive visualization from output folder: "To run this visualization engine, follow these steps: 1. Fulfill the web-app's package requirements: ... pip install -r <output_folder>/requirements.txt ... 2. Run the"
- [readme] Programmatic access via SQL queries on output database: "To access **BiG-SLiCE**'s preprocessed data, (advanced) users need to be able to [run SQL(ite) queries]"
- [readme] No pre-processed v2.0 reference database currently available: "there is currently no pre-processed result for BiG-SLiCE v2, we will work to make it available soon"
