---
name: clustering-tool-orchestration
description: Use when you have raw tandem MS metabolomics data (in mzML or MGF format)
  and wish to compare the clustering performance of two or more MS clustering tools
  on the same dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - msCluster
  - Falcon
  - MaRaCluster
  - msconvert (ProteoWizard)
  - ThermoRawFileParser
  - GNPS 2.0 Classical Networking Workflow
  - GNPS 2.0 PerScanSummarizer Workflow
  - Clustering_benchmark_MS_RT.py
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.4c00881
  title: MS-RT
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_rt_cq
    doi: 10.1021/acs.jproteome.4c00881
    title: MS-RT
  dedup_kept_from: coll_ms_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00881
  all_source_dois:
  - 10.1021/acs.jproteome.4c00881
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# clustering-tool-orchestration

## Summary

Execute and standardize outputs from multiple tandem mass spectra clustering tools (msCluster, Falcon, MaRaCluster) against the same metabolomics dataset using a unified benchmarking harness. This skill ensures reproducible, comparable evaluation across tools by normalizing heterogeneous output formats and computing standardized performance metrics.

## When to use

You have raw tandem MS metabolomics data (in mzML or MGF format) and wish to compare the clustering performance of two or more MS clustering tools on the same dataset. This skill is essential when you need to benchmark clustering quality across tools using standardized metrics (silhouette score, Davies–Bouldin index, purity) rather than trusting individual tool outputs in isolation.

## When NOT to use

- Your tandem MS data is already in vendor binary format and you lack conversion tools (msconvert, ThermoRawFileParser) or permissions to use them—conversion is a prerequisite.
- You are evaluating a single clustering tool in isolation without need for cross-tool comparison; this skill is optimized for multi-tool benchmarking and adds overhead.
- Your clustering results are already in a standardized, unified format with harmonized column names and metrics; the normalization and harness steps would be redundant.

## Inputs

- raw tandem MS data files (vendor formats: .raw, or pre-converted mzML/MGF files)
- clustering tool output files (msCluster .tsv, Falcon .csv, MaRaCluster .tsv)
- dataset registry and tool parameter templates
- total count of MS/MS spectra in the dataset

## Outputs

- standardized cluster assignment table (columns: filename, scan, mass, rt_time, cluster)
- evaluation metrics per tool (silhouette score, Davies–Bouldin index, purity)
- comparative performance report (runtime, memory usage, quality metrics aggregated across tools)
- unified evaluation table documenting all tools side-by-side

## How to apply

First, prepare your raw vendor mass spectrometry files by converting them to mzML or MGF format using msconvert or ThermoRawFileParser. Next, run each clustering tool (msCluster, Falcon, MaRaCluster) on the same input dataset, capturing raw cluster assignments and metadata (scan numbers, retention times, precursor masses). Then post-process each tool's results to a canonical format with standardized column names ('filename', 'scan', 'mass', 'rt_time', 'cluster'). Use the benchmarking harness script to parse all normalized results, compute evaluation metrics for each tool, aggregate performance statistics, and generate a comparative report. Set the MS-RT tolerance parameter (default 0.1) to match your analytical requirements. Success is indicated by a unified evaluation table showing runtime, memory usage, and quality metrics across all tools, enabling objective comparison.

## Related tools

- **msCluster** (Tandem MS clustering tool; one of the tools orchestrated and benchmarked by the harness)
- **Falcon** (Tandem MS clustering tool; output post-processed via summarize_results script) — https://github.com/bittremieux/falcon
- **MaRaCluster** (Tandem MS clustering tool; output merged with retention time metadata via maracluster_processing script) — https://github.com/statisticalbiotechnology/maracluster
- **msconvert (ProteoWizard)** (Converts vendor-specific mass spectrometry formats (.raw) to open formats (mzML, MGF) for input to clustering tools) — http://proteowizard.sourceforge.net/download.html
- **ThermoRawFileParser** (Cross-platform converter for Thermo RAW files to mzML or MGF without vendor software dependency) — https://github.com/compomics/ThermoRawFileParser
- **GNPS 2.0 Classical Networking Workflow** (Generates standardized cluster info table (clusterinfo.tsv) for msCluster post-processing) — https://gnps2.org/workflowinput?workflowname=classical_networking_workflow
- **GNPS 2.0 PerScanSummarizer Workflow** (Extracts retention time information (results.csv) for merging with MaRaCluster results) — https://gnps2.org/workflowinput?workflowname=PerScanSummarizer
- **Clustering_benchmark_MS_RT.py** (Main benchmarking harness script that orchestrates tool execution, normalizes outputs, computes metrics, and generates comparative report) — https://github.com/XianghuWang-287/Metabolomics_Clustering_Benchmark

## Examples

```
python3 src/Clustering_benchmark_MS_RT.py -c ./data/falcon/falcon_cluster_info.tsv -t 109333 -methods falcon -tol 0.1
```

## Evaluation signals

- All clustering tool outputs are successfully normalized to the canonical schema with required columns ('filename', 'scan', 'mass', 'rt_time', 'cluster') and no missing or malformed values in the cluster ID field.
- The unified evaluation table contains exactly one row per clustering tool with non-null values for runtime (seconds), memory usage (MB), silhouette score, Davies–Bouldin index, and purity metric.
- Cross-tool consistency check: cluster assignments for the same spectrum from different tools are examined; high disagreement or zero consensus clusters signal potential preprocessing or parameter misalignment issues.
- Comparative report generation completes without errors; the output file is readable and parseable, with metrics sorted or grouped by tool for visual inspection.
- Runtime and memory measurements are within expected ranges for the dataset size (e.g., runtime scales appropriately with the number of MS/MS spectra provided via the `-t` parameter).

## Limitations

- Tool-specific output formats vary significantly (msCluster via GNPS, Falcon via CSV, MaRaCluster via TSV); post-processing scripts must be correctly configured for each tool and kept in sync with upstream tool updates.
- Retention time metadata is required for MS-RT benchmarking but may be absent or inconsistent across datasets; MaRaCluster specifically requires a separate GNPS PerScanSummarizer workflow to extract this data, introducing external dependency and latency.
- Benchmarking metrics (silhouette score, Davies–Bouldin index, purity) are computed on spectral-level clusters and depend on correct ground-truth labeling or reference spectral similarity; no discussion section is provided in the source material to address metric limitations or interpretation.
- The harness assumes all tools are executable in the same computational environment; cross-platform differences (Windows vs. macOS/Linux) or missing tool installations will cause failures without clear diagnostics.

## Evidence

- [intro] The repository provides tools designed to benchmark clustering tools for metabolomics datasets, implementing a harness that standardizes the evaluation process across tandem mass spectra clustering applications.: "tools designed to benchmark clustering tools for metabolomics datasets, implementing a harness that standardizes the evaluation process"
- [methods] Standardize cluster output formats to a canonical representation (e.g., cluster ID per spectrum). Compute evaluation metrics (silhouette score, Davies–Bouldin index, purity, or other comparative measures) for each tool's results. Aggregate metrics and tool performance summaries into a unified evaluation table.: "Standardize cluster output formats to a canonical representation (e.g., cluster ID per spectrum). Compute evaluation metrics (silhouette score, Davies–Bouldin index, purity, or other comparative"
- [readme] All datasets used in this project are publicly available and can be downloaded from ProteomeXchange, a globally coordinated initiative to facilitate the exchange and dissemination of proteomics data.: "All datasets used in this project are publicly available and can be downloaded from ProteomeXchange"
- [readme] For msCluster, you can use any processing protocol as long as the output file has the following column names: 'filename': '#Filename', 'scan': '#Scan', 'mass': '#ParentMass', 'rt_time': '#RetTime', 'cluster': '#ClusterIdx': "output file has the following column names: 'filename': '#Filename', 'scan': '#Scan', 'mass': '#ParentMass', 'rt_time': '#RetTime', 'cluster': '#ClusterIdx'"
- [readme] To process the raw data files, they need to be converted into standard formats like mzML or MGF. We recommend using either msconvert or ThermoRawFileParser for this purpose.: "raw data files need to be converted into standard formats like mzML or MGF. We recommend using either msconvert or ThermoRawFileParser"
- [readme] python3 src/Clustering_benchmark_MS_RT.py -c <cluster_info_file> -t <number_of_msms> -methods <clustering_method> [-tol <tolerance>]: "python3 src/Clustering_benchmark_MS_RT.py -c <cluster_info_file> -t <number_of_msms> -methods <clustering_method> [-tol <tolerance>]"
