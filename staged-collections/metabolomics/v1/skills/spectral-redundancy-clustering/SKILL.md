---
name: spectral-redundancy-clustering
description: Collapse redundant MS/MS spectra from large-scale repository queries into consensus spectra using MS-Cluster or Falcon-MS, reducing dataset size by 70–80% while preserving representative fragmentation patterns for downstream molecular networking and library annotation.
when_to_use_negative:
- Input spectrum set is already small (< 100 unique spectra) or has been manually curated; clustering overhead is unnecessary.
- Spectral redundancy is intentional (e.g., studying instrument or ionization variability); collapsing removes that signal.
- You require preservation of individual scan metadata (retention time, instrument configuration, sample provenance) for post-hoc filtering; consensus spectra lose this granularity.
edam_operation: http://edamontology.org/operation_3933
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_0654
- http://edamontology.org/topic_3520
tools:
- name: MS-Cluster
  role: 'Primary clustering engine: merges redundant MS/MS spectra and outputs consensus peaks'
- name: Falcon-MS
  role: Alternative clustering tool for consensus spectrum generation from large result sets
- name: GNPS
  role: Hosts public MS/MS repository (MassIVE) from which spectra are retrieved; also performs molecular networking and spectral library matching on consensus spectra
  repo: https://gnps.ucsd.edu
- name: MassQL
  role: Upstream query engine used to retrieve the raw spectrum set before clustering
  repo: https://github.com/mwang87/MassQueryLanguage
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
    - outputs/audit_s41592_full/skills/spectral-redundancy-clustering/SKILL.md
    - outputs/audit_s41592_full/skills/spectral-redundancy-clustering/skill.md
    merged_at: '2026-05-25T07:15:30.948501+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/spectral-redundancy-clustering@sha256:431f4f9692b5895ab5760ee9a270aec07691ab7dd39380b62bcd52a3809f44bb
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1038/s41592-025-02660-z
---

# spectral-redundancy-clustering

## Summary

Collapse redundant MS/MS spectra from large-scale repository queries into consensus spectra using MS-Cluster or Falcon-MS, reducing dataset size by 70–80% while preserving representative fragmentation patterns for downstream molecular networking and library annotation.

## When to use

After a repository-scale MassQL query retrieves thousands of MS/MS spectra matching a chemical pattern (e.g., iron-characteristic isotope patterns, organophosphate ester product ions), and you observe high redundancy across replicate analyses or different instruments. Use when consensus spectra are needed for molecular networking, spectral library matching, or discovery of novel compounds in the unannotated tail of the result set.

## When NOT to use

- Input spectrum set is already small (< 100 unique spectra) or has been manually curated; clustering overhead is unnecessary.
- Spectral redundancy is intentional (e.g., studying instrument or ionization variability); collapsing removes that signal.
- You require preservation of individual scan metadata (retention time, instrument configuration, sample provenance) for post-hoc filtering; consensus spectra lose this granularity.

## Inputs

- MGF-formatted MS/MS spectra (retrieved from repository-scale MassQL query)
- 26,944+ MS/MS spectra from GNPS/MassIVE high-resolution Q Exactive data

## Outputs

- Consensus MS/MS spectra in MGF format (7,504 spectra from 26,944 input)
- Molecular network (GNPS-format annotation)
- Spectral library annotation table (5% matched to known compounds in example)

## How to apply

Load the MGF-formatted MS/MS spectra retrieved from GNPS/MassIVE or another public repository. Apply MS-Cluster or Falcon-MS with default settings to identify and merge redundant MS/MS observations based on spectral similarity, peak matching, and intensity thresholds. Output consensus spectra (representative peak lists per cluster) in MGF format. Expect a 70–80% reduction in total spectra count; for example, 26,944 iron-characteristic spectra clustered to 7,504 consensus spectra. Create a molecular network from the consensus spectra in GNPS and perform spectral library search to annotate the consensus set, leaving the unannotated fraction available for targeted discovery.

## Related tools

- **MS-Cluster** (Primary clustering engine: merges redundant MS/MS spectra and outputs consensus peaks)
- **Falcon-MS** (Alternative clustering tool for consensus spectrum generation from large result sets)
- **GNPS** (Hosts public MS/MS repository (MassIVE) from which spectra are retrieved; also performs molecular networking and spectral library matching on consensus spectra) — https://gnps.ucsd.edu
- **MassQL** (Upstream query engine used to retrieve the raw spectrum set before clustering) — https://github.com/mwang87/MassQueryLanguage

## Evaluation signals

- Reduction ratio: consensus spectra count is 70–80% lower than input (e.g., 7,504 from 26,944). Verify no inadvertent over-clustering by spot-checking a few consensus clusters for spectral coherence.
- Output file format: MGF conforms to standard MS/MS peak-list syntax (m/z, intensity pairs); parse and validate all consensus spectra are non-empty and have ≥1 peak.
- Molecular network density and size: consensus spectra generate a connected network in GNPS with expected graph metrics (nodes = consensus spectra, edges = cosine similarity); compare to pre-clustering network structure if available.
- Spectral library annotation rate: 5–15% of consensus spectra should match known compounds in GNPS libraries (mass tolerance ≤20 ppm, cosine similarity ≥0.7). Unannotated tail should be >85%, indicating discovery potential.
- Cluster size distribution: inspect that no single consensus cluster contains >10–20% of original spectra, which would indicate over-aggressive merging or mis-parameterization.

## Limitations

- MS-Cluster requires tuning of spectral similarity threshold and intensity tolerance; one siderophore with low-intensity 54Fe peak (outside 25% tolerance) was missed in the iron-binding example.
- Consensus spectra lose individual scan metadata (retention time, instrument config, sample ID), preventing post-hoc stratification or quality control by data source.
- MassQL has limited capability to leverage consecutive MS spectra from the same chromatographic feature, so redundancy metrics are based on standalone MS/MS matching rather than LC-MS context.
- Clustering is computationally intensive for very large result sets (>100k spectra); runtime is not quantified in the article.

## Evidence

- [full_text] We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations: "We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations"
- [full_text] MS-Cluster clustering of the 26,944 iron-characteristic MS/MS spectra yielded 7,504 consensus spectra, reducing the dataset by 72%: "MS-Cluster clustering of the 26,944 iron-characteristic MS/MS spectra yielded 7,504 consensus spectra, reducing the dataset by 72%"
- [full_text] Apply MS-Cluster algorithm with default settings to identify and merge redundant MS/MS observations. Output 7,504 consensus MS/MS spectra (representative peaks per cluster) in MGF format.: "Apply MS-Cluster algorithm with default settings to identify and merge redundant MS/MS observations. Output 7,504 consensus MS/MS spectra (representative peaks per cluster) in MGF format."
- [full_text] Using these consensus spectra, we created a molecular network in GNPS. We could putatively identify 441 (5%) of the consensus spectra: "Using these consensus spectra, we created a molecular network in GNPS. We could putatively identify 441 (5%) of the consensus spectra"
- [full_text] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%: "The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%"
