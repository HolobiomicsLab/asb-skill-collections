---
name: clustering-metrics-computation
description: Use when when you have executed multiple clustering tools on the same tandem-MS dataset and need to quantitatively compare their performance using normalized, comparable metrics rather than raw cluster assignments alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Clustering_benchmark_MS_RT.py
  - msCluster
  - Falcon
  - MaRaCluster
  - GNPS 2.0 Classical Networking Workflow
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# clustering-metrics-computation

## Summary

Standardized computation of quantitative evaluation metrics (silhouette score, Davies–Bouldin index, purity) across clustering tool outputs to enable comparative benchmarking of tandem mass spectra clustering performance in metabolomics datasets.

## When to use

When you have executed multiple clustering tools on the same tandem-MS dataset and need to quantitatively compare their performance using normalized, comparable metrics rather than raw cluster assignments alone.

## When NOT to use

- Input clustering results have not been standardized to a common column schema (filename, scan, mass, rt_time, cluster) — must post-process first using tool-specific standardization scripts
- Clustering task is on data types other than tandem mass spectra (e.g., genomic or image clustering, where metric assumptions differ)
- Only a single clustering tool has been applied — these metrics are designed for comparative evaluation, not standalone validation

## Inputs

- Standardized cluster assignment files (TSV/CSV with columns: filename, scan, precursor_mz, retention_time, cluster_id)
- Reference or gold-standard cluster assignments (for purity calculation)
- Clustering tool output in vendor or tool-specific formats (msCluster, Falcon, MaRaCluster output)

## Outputs

- Unified evaluation metrics table (CSV/TSV with silhouette scores, Davies–Bouldin indices, purity values per tool)
- Comparative benchmarking report (runtime, memory usage, and quality metrics across all clustering tools)
- Per-cluster quality annotations (optional, for diagnostic inspection)

## How to apply

After standardizing cluster output formats to a canonical representation (cluster ID per spectrum with associated MS features like precursor m/z, retention time, and filename), compute evaluation metrics on each tool's results independently. Apply silhouette score to assess cluster cohesion and separation, Davies–Bouldin index to measure average similarity between each cluster and its most similar neighbor, and purity to evaluate clustering accuracy against reference assignments. Aggregate the computed metrics into a unified evaluation table alongside runtime and memory usage measurements. Use tolerance parameters (e.g., 0.1 Da for MS-RT window) consistently across all tools to ensure comparability.

## Related tools

- **Clustering_benchmark_MS_RT.py** (Primary benchmarking script that executes metric computation and aggregation across multiple clustering tools) — https://github.com/XianghuWang-287/Metabolomics_Clustering_Benchmark
- **msCluster** (Tandem-MS clustering tool whose output is standardized and evaluated)
- **Falcon** (Tandem-MS clustering tool whose output is standardized and evaluated) — https://github.com/bittremieux/falcon
- **MaRaCluster** (Tandem-MS clustering tool whose output is standardized and evaluated) — https://github.com/statisticalbiotechnology/maracluster
- **GNPS 2.0 Classical Networking Workflow** (Pre-processing workflow that standardizes msCluster output to required column format) — https://gnps2.org/workflowinput?workflowname=classical_networking_workflow

## Examples

```
python3 src/Clustering_benchmark_MS_RT.py -c ./data/falcon/falcon_cluster_info.tsv -t 109333 -methods falcon -tol 0.1
```

## Evaluation signals

- All input cluster files conform to the canonical schema: columns present are 'filename', 'scan', 'mass', 'rt_time', 'cluster' with correct data types (string, integer, float, float, integer/string respectively)
- Computed metric values fall within expected ranges: silhouette score ∈ [−1, +1], Davies–Bouldin index ≥ 0, purity ∈ [0, 1]
- Metrics are computed consistently across all tools using identical tolerance settings (e.g., MS-RT window tolerance = 0.1 Da)
- Output evaluation table contains exactly one row per clustering tool with all metrics populated (no missing values for successfully executed tools)
- Runtime and memory usage measurements are captured and reported alongside quality metrics for each tool

## Limitations

- Metric computation requires a gold-standard or reference clustering assignment; purity cannot be calculated if no reference is available
- Davies–Bouldin and silhouette metrics are sensitive to dataset dimensionality and cluster size distribution; interpretation must account for dataset characteristics
- Retention time information must be available in input files for MS-RT window-based metrics; tools that do not generate RT data cannot be fairly compared on RT-dependent metrics
- No changelog or discussion of metric selection rationale is provided in the repository; users must apply domain expertise to choose appropriate metrics for their metabolomics application

## Evidence

- [other] Standardize cluster output formats to a canonical representation (e.g., cluster ID per spectrum).: "Standardize cluster output formats to a canonical representation (e.g., cluster ID per spectrum)."
- [other] Compute evaluation metrics (silhouette score, Davies–Bouldin index, purity, or other comparative measures) for each tool's results.: "Compute evaluation metrics (silhouette score, Davies–Bouldin index, purity, or other comparative measures) for each tool's results."
- [other] Aggregate metrics and tool performance summaries into a unified evaluation table.: "Aggregate metrics and tool performance summaries into a unified evaluation table."
- [readme] The final output file should have at least the following columns: 'filename': filename 'scan': scan 'mass': precursor_mz 'rt_time': retention_time 'cluster': cluster: "'filename': filename
       - `'scan'`: `scan`
       - `'mass'`: `precursor_mz`
       - `'rt_time'`: `retention_time`
       - `'cluster'`: `cluster`"
- [readme] The benchmarking script accepts several command-line arguments to customize its behavior. ... Parameters ... tolerance for the MS-RT Window: Tolerance value for the mass-to-retention time window used in benchmarking.: "**Tolerance for the MS-RT Window:** Tolerance value for the mass-to-retention time window used in benchmarking."
