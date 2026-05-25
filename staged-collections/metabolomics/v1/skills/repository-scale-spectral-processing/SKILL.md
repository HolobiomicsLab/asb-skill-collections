---
name: repository-scale-spectral-processing
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to apply MS-Cluster or Falcon-MS for collapsing redundant MS/MS observations at repository scale into consensus spectra for downstream molecular networking and annotation.
when_to_use_negative:
- Input spectra are already deduplicated or come from a single sample with no redundancy expected.
- Consensus spectra are not required downstream; you plan direct library matching or molecular feature detection without aggregation.
- You need to preserve intensity or scan-level metadata that clustering would lose; consider filtering by retention time or other orthogonal criteria instead.
edam_operation: http://edamontology.org/operation_3933
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3520
tools:
- name: MS-Cluster
  role: Primary clustering algorithm to merge redundant MS/MS spectra into consensus spectra by identifying similar fragmentation patterns
- name: Falcon-MS
  role: Alternative consensus spectral generation tool for collapsing redundant observations; used interchangeably with MS-Cluster
- name: MassQL
  role: Upstream retrieval tool to query repository and generate the large spectral result sets that feed into clustering
  repo: https://github.com/mwang87/MassQueryLanguage
- name: GNPS
  role: Hosts downstream molecular networking and spectral library annotation on consensus spectra
- name: pyteomics
  role: Python library for reading and writing MS data files (mzML, mzXML, MGF) used by MassQL reference engine
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1038/s41592-025-02660-z
    title: A universal language for finding mass spectrometry data patterns
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_s41592_full/skills/repository-scale-spectral-processing/SKILL.md
    - outputs/audit_s41592_full/skills/repository-scale-spectral-processing/skill.md
    merged_at: '2026-05-25T07:33:56.414886+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/repository-scale-spectral-processing@sha256:a02ca468322fdcfde554cdbff3f444683f07f6ad07d51e6c22f46a2aa9e3a42a
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1038/s41592-025-02660-z
---

# Repository-scale spectral processing

## Summary

Apply MS-Cluster or Falcon-MS to collapse redundant MS/MS observations retrieved at repository scale (millions of spectra) into consensus spectra suitable for downstream molecular networking and annotation. This skill transforms large unfiltered spectral result sets into compact, representative datasets by identifying and merging duplicate acquisitions.

## When to use

You have retrieved a large number of MS/MS spectra (thousands to hundreds of thousands) from a repository query (e.g., via MassQL across GNPS/MassIVE) and observe high redundancy due to multiple acquisitions of the same compound in different samples or technical replicates. Apply this skill before molecular networking or spectral library annotation to reduce computational burden and improve statistical power of downstream analyses.

## When NOT to use

- Input spectra are already deduplicated or come from a single sample with no redundancy expected.
- Consensus spectra are not required downstream; you plan direct library matching or molecular feature detection without aggregation.
- You need to preserve intensity or scan-level metadata that clustering would lose; consider filtering by retention time or other orthogonal criteria instead.

## Inputs

- MS/MS spectra in MGF format (retrieved from repository query)
- Spectra count: typically 10,000–600,000+ observations
- Metadata: precursor m/z, charge state, scan retention time

## Outputs

- Consensus MS/MS spectra in MGF format
- Cluster assignment table (optional)
- Summary statistics: input spectra count, output consensus count, reduction ratio (%)

## How to apply

Load the retrieved MS/MS spectra in MGF format. Apply MS-Cluster with default settings (or Falcon-MS as an alternative) to identify and merge spectra with similar fragmentation patterns into clusters. Each cluster yields one consensus spectrum containing representative peaks. The consensus set will typically reduce the dataset by 60–75% depending on redundancy levels. Export consensus spectra in MGF format and validate that cluster count and dataset reduction ratio are consistent with the input size and expected redundancy. Downstream use cases (molecular networking, library search) should operate on consensus spectra rather than the full result set to improve annotation sensitivity and reduce false positive annotations from low-intensity or noisy spectra.

## Related tools

- **MS-Cluster** (Primary clustering algorithm to merge redundant MS/MS spectra into consensus spectra by identifying similar fragmentation patterns)
- **Falcon-MS** (Alternative consensus spectral generation tool for collapsing redundant observations; used interchangeably with MS-Cluster)
- **MassQL** (Upstream retrieval tool to query repository and generate the large spectral result sets that feed into clustering) — https://github.com/mwang87/MassQueryLanguage
- **GNPS** (Hosts downstream molecular networking and spectral library annotation on consensus spectra)
- **pyteomics** (Python library for reading and writing MS data files (mzML, mzXML, MGF) used by MassQL reference engine)

## Evaluation signals

- Consensus spectra count is substantially lower than input (expect 60–75% reduction for typical repository data).
- All consensus spectra have valid peak lists with at least one representative m/z and intensity pair.
- Cluster membership is deterministic: re-running on the same input yields identical consensus spectra.
- Downstream molecular network size and spectral library annotation rate (% putative IDs) are consistent with prior studies (e.g., 5–10% annotation for novel compound-rich networks).
- No consensus spectra are empty or contain only precursor m/z with no product ions.

## Limitations

- MS-Cluster depends on user-defined intensity tolerance thresholds; a single low-intensity characteristic peak falling outside tolerance (e.g., 54Fe peak at <25% relative intensity) can cause spectra to be missed entirely.
- Clustering is most effective on high-resolution, reproducible instruments (e.g., Orbitrap, QTOF); low-resolution data or inconsistent fragmentation may yield poor consensus quality.
- MassQL itself has limited ability to leverage multiple consecutive MS spectra from single chromatographic features, reducing the richness of spectral patterns available for clustering.
- Consensus spectra represent aggregate patterns and lose sample-level metadata (original scan number, retention time range, file provenance) unless explicitly preserved in output headers.
- Very large datasets (>1 million spectra) may incur significant runtime or memory overhead depending on clustering algorithm implementation.

## Evidence

- [full_text] MS-Cluster clustering of the 26,944 iron-characteristic MS/MS spectra yielded 7,504 consensus spectra, reducing the dataset by 72% for downstream molecular networking and annotation.
- [full_text] We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations
- [full_text] We extracted all MS/MS spectra and created consensus MS/MS spectra using Falcon-MS, resulting in 2,777 consensus spectra.
- [full_text] Using these consensus spectra, we created a molecular network in GNPS
- [full_text] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%