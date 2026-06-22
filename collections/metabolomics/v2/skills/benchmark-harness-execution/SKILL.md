---
name: benchmark-harness-execution
description: Use when you have post-processed clustering results from multiple tools (msCluster, Falcon, MaRaCluster) on the same tandem MS dataset and need to generate a comparative performance report with quality metrics and runtime statistics to determine which tool suits your metabolomics workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - msCluster
  - Falcon
  - MaRaCluster
  - GNPS 2.0 Classical Networking Workflow
  - GNPS 2.0 PerScanSummarizer
  techniques:
  - tandem-MS
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

# benchmark-harness-execution

## Summary

Execute a standardized benchmarking harness to evaluate and compare clustering tool performance on tandem mass spectrometry metabolomics datasets using normalized metrics (silhouette score, Davies–Bouldin index, purity) and resource usage (runtime, memory).

## When to use

You have post-processed clustering results from multiple tools (msCluster, Falcon, MaRaCluster) on the same tandem MS dataset and need to generate a comparative performance report with quality metrics and runtime statistics to determine which tool best suits your metabolomics workflow.

## When NOT to use

- Clustering results from a single tool only (no comparative benchmark needed).
- Input files have not been post-processed to canonical column format (filename, scan, mass, rt_time, cluster).
- Dataset is too small or contains fewer than ~1000 spectra (benchmark metrics may be unstable).

## Inputs

- post-processed clustering results TSV file (columns: filename, scan, mass, rt_time, cluster)
- integer count of total MS/MS spectra in dataset
- clustering method name (string: 'falcon', 'mscluster', or 'maracluster')
- optional tolerance value for MS-RT window (float, default 0.1)

## Outputs

- comparative performance report file (TSV or summary table)
- aggregated evaluation metrics table (silhouette score, Davies–Bouldin index, purity per tool)
- tool runtime and memory usage summary
- standardized cluster quality statistics

## How to apply

First, ensure all clustering tool outputs are post-processed to a canonical format with required columns: filename, scan, precursor_mz (mass), retention_time (rt_time), and cluster ID. Then invoke the benchmarking script with the standardized cluster info file, dataset spectrum count, clustering method name, and optional MS-RT tolerance window (default 0.1). The harness will compute evaluation metrics (silhouette score, Davies–Bouldin index, purity) for each tool's cluster assignments, measure runtime and memory consumption, and aggregate results into a unified comparative report. Results are validated by confirming all input spectra are accounted for in cluster assignments and that metric ranges are within expected bounds (e.g., silhouette score ∈ [−1, 1], Davies–Bouldin index ≥ 0).

## Related tools

- **msCluster** (tandem MS clustering tool whose output is benchmarked)
- **Falcon** (tandem MS clustering tool whose output is benchmarked) — https://github.com/bittremieux/falcon
- **MaRaCluster** (tandem MS clustering tool whose output is benchmarked) — https://github.com/statisticalbiotechnology/maracluster
- **GNPS 2.0 Classical Networking Workflow** (preprocessing tool to generate standardized msCluster output format) — https://gnps2.org/workflowinput?workflowname=classical_networking_workflow
- **GNPS 2.0 PerScanSummarizer** (preprocessing tool to extract retention time information for MaRaCluster results merging) — https://gnps2.org/workflowinput?workflowname=PerScanSummarizer

## Examples

```
python3 src/Clustering_benchmark_MS_RT.py -c ./data/falcon/falcon_cluster_info.tsv -t 109333 -methods falcon -tol 0.1
```

## Evaluation signals

- All input spectra (count = -t parameter) are accounted for in exactly one cluster assignment across the output.
- Computed metrics are within valid ranges: silhouette score ∈ [−1, 1], Davies–Bouldin index ≥ 0, purity ∈ [0, 1].
- Output report includes runtime and memory usage for each benchmarked tool with non-null numeric values.
- Cluster ID column contains only non-negative integers with no gaps or missing values.
- Comparative metrics table rows match the number of clustering methods tested and are reproducible across re-runs with identical inputs.

## Limitations

- Benchmarking harness requires strict adherence to canonical column schema; deviations in naming or order will cause script failure.
- Evaluation metrics (silhouette, Davies–Bouldin) assume metric-space clustering and may not reflect domain-specific quality for metabolomics (e.g., spectral similarity preservation).
- No changelog or discussion section provided in repository to document metric selection rationale or version compatibility constraints.
- Runtime and memory measurements are system-dependent and may vary across hardware configurations; relative ranking is more reliable than absolute values.
- Harness does not validate whether cluster assignments reflect true spectral similarity or known metabolite groupings (ground truth).

## Evidence

- [other] Standardize cluster output formats to a canonical representation (e.g., cluster ID per spectrum).: "4. Standardize cluster output formats to a canonical representation (e.g., cluster ID per spectrum)."
- [other] Compute evaluation metrics (silhouette score, Davies–Bouldin index, purity, or other comparative measures) for each tool's results.: "5. Compute evaluation metrics (silhouette score, Davies–Bouldin index, purity, or other comparative measures) for each tool's results."
- [other] Aggregate metrics and tool performance summaries into a unified evaluation table.: "6. Aggregate metrics and tool performance summaries into a unified evaluation table."
- [other] Generate a comparative report file documenting runtime, memory usage, and quality metrics across all tools.: "7. Generate a comparative report file documenting runtime, memory usage, and quality metrics across all tools."
- [readme] For msCluster, you can use any processing protocol as long as the output file has the following column names: 'filename': '#Filename', 'scan': '#Scan', 'mass': '#ParentMass', 'rt_time': '#RetTime', 'cluster': '#ClusterIdx'.: "For **msCluster**, you can use any processing protocol as long as the output file has the following column names: 'filename': '#Filename', 'scan': '#Scan', 'mass': '#ParentMass', 'rt_time':"
- [readme] Once you have post-processed the clustering results from msCluster, Falcon, and MaRaCluster, you can benchmark their performance using the provided benchmarking script.: "Once you have post-processed the clustering results from **msCluster**, **Falcon**, and **MaRaCluster**, you can benchmark their performance using the provided benchmarking script."
- [readme] The benchmarking script accepts several command-line arguments to customize its behavior. Below is a detailed explanation of each parameter: -c (str, required) Input Clustering Results Filename; -t (int, required) Number of MS/MS in the Datasets; -methods (str, required) Clustering Methods; -tol (float, optional, default 0.1) Tolerance for the MS-RT Window.: "The benchmarking script accepts several command-line arguments to customize its behavior. Below is a detailed explanation of each parameter: `-c`, `-t`, `-methods`, `-tol`."
