---
name: cross-tool-performance-comparison
description: Use when when you have raw tandem MS metabolomics data in vendor formats (.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3361
  tools:
  - msCluster
  - Falcon
  - MaRaCluster
  - msconvert (ProteoWizard)
  - ThermoRawFileParser
  - GNPS 2.0 Classical Networking Workflow
  - GNPS 2.0 PerScanSummarizer
  - Clustering_benchmark_MS_RT.py
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-tool-performance-comparison

## Summary

Execute multiple tandem mass spectra clustering tools (msCluster, Falcon, MaRaCluster) on identical metabolomics datasets and standardize their outputs to enable direct quantitative comparison of runtime, memory, and clustering quality metrics. This skill enables practitioners to benchmark tool performance and select the most appropriate clustering method for their specific metabolomics application.

## When to use

When you have raw tandem MS metabolomics data in vendor formats (.raw) or standard formats (mzML, MGF) and need to evaluate which clustering tool—msCluster, Falcon, or MaRaCluster—produces the best clustering quality (silhouette score, Davies–Bouldin index, purity) and performance (runtime, memory usage) for your dataset. This skill is essential when tool selection is uncertain or when standardized benchmarking is required for method validation.

## When NOT to use

- Input data are already validated, single-tool clustered results; if the goal is refinement of one tool's parameters rather than tool selection, use tool-specific tuning instead.
- Dataset contains only a single MS/MS spectrum or fewer than ~100 spectra; benchmark metrics require sufficient statistical power and meaningful clustering structure.
- Clustering results are in incompatible formats (non-canonical column names or missing retention time data); tool-specific post-processing must first standardize output before benchmarking.

## Inputs

- Raw tandem mass spectrometry data files (Thermo .raw, or vendor-specific formats)
- Converted mzML or MGF format files
- Post-processed cluster assignment files (one per tool) with columns: filename, scan, mass/precursor_mz, rt_time, cluster
- Total MS/MS spectrum count for the dataset (integer)

## Outputs

- Standardized cluster assignment table (canonical format: filename, scan, mass, rt_time, cluster)
- Evaluation metrics per tool (silhouette score, Davies–Bouldin index, purity)
- Unified comparative performance report (runtime, memory usage, quality metrics across all tools)
- Aggregated metrics table for cross-tool comparison

## How to apply

First, convert raw MS data files to mzML or MGF format using msconvert or ThermoRawFileParser. Post-process clustering results from each tool to a canonical format with columns: 'filename', 'scan', 'mass' (or 'precursor_mz'), 'rt_time', and 'cluster'. For msCluster, use the GNPS 2.0 Classical Networking Workflow to generate clusterinfo.tsv; for Falcon, run the summarize_results utility script; for MaRaCluster, merge clustering output with retention time data from GNPS 2.0 PerScanSummarizer using the maracluster_processing script. Execute the Clustering_benchmark_MS_RT.py script specifying the cluster info file, total MS/MS count, tool name, and MS-RT tolerance (default 0.1). The script computes evaluation metrics (silhouette score, Davies–Bouldin index, purity) and generates a unified comparative report with runtime and memory usage for all tools. Judge success by verifying that all tools produce output in the canonical schema, metrics are computed without errors, and the comparative report shows interpretable performance differences.

## Related tools

- **msCluster** (Tandem MS clustering tool; outputs cluster assignments processed via GNPS 2.0 Classical Networking Workflow) — https://gnps2.org/workflowinput?workflowname=classical_networking_workflow
- **Falcon** (Tandem MS clustering tool; results formatted using summarize_results utility script in this project) — https://github.com/bittremieux/falcon
- **MaRaCluster** (Tandem MS clustering tool; results merged with retention time via GNPS 2.0 PerScanSummarizer and maracluster_processing script) — https://github.com/statisticalbiotechnology/maracluster
- **msconvert (ProteoWizard)** (Converts vendor-specific MS data formats (.raw) to standard mzML or MGF formats required as input) — http://proteowizard.sourceforge.net/download.html
- **ThermoRawFileParser** (Alternative cross-platform tool for converting Thermo .raw files to mzML or MGF formats without vendor software) — https://github.com/compomics/ThermoRawFileParser
- **GNPS 2.0 Classical Networking Workflow** (Preprocesses msCluster data and generates standardized clusterinfo.tsv output) — https://gnps2.org/workflowinput?workflowname=classical_networking_workflow
- **GNPS 2.0 PerScanSummarizer** (Extracts retention time information required for MaRaCluster result processing) — https://gnps2.org/workflowinput?workflowname=PerScanSummarizer
- **Clustering_benchmark_MS_RT.py** (Core benchmarking script that standardizes outputs, computes evaluation metrics, and generates comparative reports) — https://github.com/XianghuWang-287/Metabolomics_Clustering_Benchmark

## Examples

```
python3 src/Clustering_benchmark_MS_RT.py -c ./data/mscluster/mscluster_cluster_info.tsv -t 109333 -methods mscluster -tol 0.1
```

## Evaluation signals

- All post-processed cluster files contain the required canonical columns (filename, scan, mass, rt_time, cluster) with no missing values in the cluster column.
- Evaluation metrics (silhouette score, Davies–Bouldin index, purity) are computed successfully for each tool without NaN or error values; values fall within expected ranges (silhouette: -1 to 1; Davies–Bouldin: typically 0–3 for reasonable clusterings).
- Runtime and memory usage are logged and reported for each tool; reported values are non-negative and reasonable for the dataset size (e.g., memory usage < total available system RAM).
- Comparative report shows interpretable performance differences: at least one tool has higher silhouette score or lower Davies–Bouldin index than others, indicating the benchmarking discriminated tool quality.
- Total spectrum count in the output report matches the input `-t` parameter; cluster assignments reference only valid scan indices and filenames present in the input dataset.

## Limitations

- Benchmarking accuracy depends critically on correct post-processing of tool-specific outputs; errors in column mapping or missing retention time data will corrupt evaluation metrics.
- Evaluation metrics (silhouette, Davies–Bouldin, purity) assume ground truth clustering or stable statistical properties; results may not be interpretable if the dataset has weak or ambiguous cluster structure.
- MS-RT tolerance parameter (default 0.1) must be calibrated to the specific dataset and instrument; using an inappropriate tolerance will bias metrics and produce misleading tool comparisons.
- Benchmarking assumes all tools are given identical input data and comparable parameter settings; unfair parameter tuning favoring one tool will invalidate cross-tool comparison.
- Runtime and memory metrics are system-dependent and may vary significantly across computational environments; relative ranking of tools is more stable than absolute performance values.

## Evidence

- [other] tools to benchmark clustering tools for metabolomics datasets, implementing a harness that standardizes the evaluation process across tandem mass spectra clustering applications: "tools designed to benchmark clustering tools for metabolomics datasets, implementing a harness that standardizes the evaluation process across tandem mass spectra clustering applications"
- [other] For each clustering tool in the suite, parse tool-specific parameter templates and input/output schemas. Execute each clustering tool against the same tandem-MS dataset(s) with configured parameters, capturing runtime logs and intermediate cluster assignments. Standardize cluster output formats to a canonical representation (e.g., cluster ID per spectrum). Compute evaluation metrics (silhouette score, Davies–Bouldin index, purity, or other comparative measures) for each tool's results. Aggregate metrics and tool performance summaries into a unified evaluation table.: "For each clustering tool in the suite, parse tool-specific parameter templates and input/output schemas. Execute each clustering tool against the same tandem-MS dataset(s) with configured parameters,"
- [readme] For msCluster, you can use any processing protocol as long as the output file has the following column names: 'filename', 'scan', 'mass', 'rt_time', 'cluster': "the output file has the following column names: 'filename': `#Filename`; 'scan': `#Scan`; 'mass': `#ParentMass`; 'rt_time': `#RetTime`; 'cluster': `#ClusterIdx`"
- [readme] To process the results from Falcon, use the provided script in this project to summarize and format the Falcon results. Script Location: src/utility/summarize_results. Command to Run the Script: python3 src/utility/summarize_results ./falcon.csv output_summary: "use the provided script in this project to summarize and format the Falcon results. Script Location: src/utility/summarize_results. Command to Run the Script: python3 src/utility/summarize_results"
- [readme] Processing MaRaCluster results requires merging retention time information with the clustering results. Use the GNPS 2.0 PerScanSummarizer Workflow to extract retention time information. Use the provided script in this project to merge the retention time information with the MaRaCluster results.: "Processing MaRaCluster results requires merging retention time information with the clustering results. Use the GNPS 2.0 PerScanSummarizer Workflow to extract retention time information. Use the"
- [readme] python3 src/Clustering_benchmark_MS_RT.py -c <cluster_info_file> -t <number_of_msms> -methods <clustering_method> [-tol <tolerance>]: "python3 src/Clustering_benchmark_MS_RT.py -c <cluster_info_file> -t <number_of_msms> -methods <clustering_method> [-tol <tolerance>]"
- [readme] Before running the benchmarking script, ensure that the clustering results from msCluster, Falcon, and MaRaCluster have been post-processed and are in the required format: "ensure that the clustering results from msCluster, Falcon, and MaRaCluster have been post-processed and are in the required format"
