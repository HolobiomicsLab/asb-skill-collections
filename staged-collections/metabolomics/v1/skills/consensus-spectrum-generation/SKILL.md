---
name: consensus-spectrum-generation
description: Collapse redundant MS/MS spectra from repository-scale queries into representative consensus spectra to reduce data dimensionality and enable downstream molecular networking and annotation. This skill is essential when large-scale mass spectrometry queries retrieve thousands of spectra with substantial redundancy across different samples or analytical runs.
when_to_use_negative:
- Input is already a curated spectral library or manually validated dataset — consensus generation is unnecessary and may obscure individual validated differences.
- Redundancy is intentionally preserved for statistical power or publication of all variant spectra — clustering removes this granularity.
- Spectra are from a single instrument run or highly controlled analytical study where each spectrum is already unique — clustering gain is minimal.
edam_operation: http://edamontology.org/operation_3933
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3520
tools:
- name: MS-Cluster
  role: Clusters redundant MS/MS spectra and generates consensus spectra with representative peaks and intensities
- name: Falcon-MS
  role: Alternative tool for consensus MS/MS spectrum generation from clustering results
- name: MassQL
  role: Generates the large-scale query results (e.g., 26,944 spectra) that serve as input to consensus generation
  repo: https://github.com/mwang87/MassQueryLanguage
- name: GNPS
  role: Accepts consensus spectra for molecular network construction and spectral library annotation
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
    - outputs/audit_s41592_full/skills/consensus-spectrum-generation/SKILL.md
    - outputs/audit_s41592_full/skills/consensus-spectrum-generation/skill.md
    merged_at: '2026-05-25T07:15:30.970370+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/consensus-spectrum-generation@sha256:c67c2a705974c275113dbf7201478f11d93b1f3912a5f9461d509ac35570ee94
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1038/s41592-025-02660-z
---

# consensus-spectrum-generation

## Summary

Collapse redundant MS/MS spectra from repository-scale queries into representative consensus spectra to reduce data dimensionality and enable downstream molecular networking and annotation. This skill is essential when large-scale mass spectrometry queries retrieve thousands of spectra with substantial redundancy across different samples or analytical runs.

## When to use

Apply this skill after executing a repository-scale MassQL query that retrieves large numbers of MS/MS spectra (typically thousands to hundreds of thousands) matching a specific chemical pattern or isotope signature. Use it when your query results contain many redundant observations of the same compounds across different files in public repositories like GNPS/MassIVE, and you need to reduce the dataset for efficient molecular networking and spectral library annotation.

## When NOT to use

- Input is already a curated spectral library or manually validated dataset — consensus generation is unnecessary and may obscure individual validated differences.
- Redundancy is intentionally preserved for statistical power or publication of all variant spectra — clustering removes this granularity.
- Spectra are from a single instrument run or highly controlled analytical study where each spectrum is already unique — clustering gain is minimal.

## Inputs

- MS/MS spectra in MGF format from MassQL repository-scale query
- Retrieved spectra count (e.g., 26,944 iron-characteristic spectra; 338,439 organophosphate ester spectra)

## Outputs

- Consensus MS/MS spectra in MGF format
- Cluster membership assignments (spectra grouped per consensus)
- Representative peak lists per consensus spectrum

## How to apply

Load the retrieved MS/MS spectra in MGF format into MS-Cluster or Falcon-MS and apply the clustering algorithm with default settings to identify and merge redundant observations. The tool will group similar spectra based on matching fragment peaks and generate a single representative consensus spectrum per cluster, complete with representative m/z values and intensities. This typically reduces dataset size by 70–75% while preserving chemical diversity. After clustering, export the consensus spectra in MGF format for downstream molecular network construction in GNPS or spectral library matching. The reduction ratio and number of resulting clusters should be verified to ensure adequate compression without information loss.

## Related tools

- **MS-Cluster** (Clusters redundant MS/MS spectra and generates consensus spectra with representative peaks and intensities)
- **Falcon-MS** (Alternative tool for consensus MS/MS spectrum generation from clustering results)
- **MassQL** (Generates the large-scale query results (e.g., 26,944 spectra) that serve as input to consensus generation) — https://github.com/mwang87/MassQueryLanguage
- **GNPS** (Accepts consensus spectra for molecular network construction and spectral library annotation)

## Evaluation signals

- Consensus spectrum count is 70–75% smaller than input spectrum count, confirming substantial redundancy collapse.
- All output consensus spectra are valid MGF records with m/z, intensity, and metadata fields.
- Cluster size distribution shows clusters contain related spectra with similar precursor m/z and fragment patterns (verify by spot-checking cluster members).
- Downstream molecular network size and annotation rate remain meaningful; e.g., >5% of consensus spectra are annotated by GNPS spectral library search.
- No consensus spectrum has zero peaks or malformed intensity values after clustering.

## Limitations

- MS-Cluster intensity tolerance thresholds (e.g., 25% for isotope patterns) may cause rare or low-intensity spectra to be missed or misclassified, as observed when a single siderophore with low-intensity ⁵⁴Fe peak fell outside expected tolerance.
- Consensus generation assumes redundancy is undesirable; if individual spectra carry independent biological or analytical significance, clustering may hide valuable information.
- Tool does not currently preserve sample metadata or retention-time information across clustered spectra; output is a consensus m/z and intensity list only.

## Evidence

- [full_text] MS-Cluster clustering of the 26,944 iron-characteristic MS/MS spectra yielded 7,504 consensus spectra, reducing the dataset by 72%: "MS-Cluster clustering of the 26,944 iron-characteristic MS/MS spectra yielded 7,504 consensus spectra, reducing the dataset by 72% for downstream molecular networking and annotation."
- [full_text] We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations: "We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations"
- [full_text] Load 26,944 MS/MS spectra, apply MS-Cluster with default settings, output 7,504 consensus spectra in MGF format: "1. Load 26,944 MS/MS spectra retrieved from GNPS/MassIVE iron-binding MassQL query (in MGF format). 2. Apply MS-Cluster algorithm with default settings to identify and merge redundant MS/MS"
- [full_text] Using these consensus spectra, we created a molecular network in GNPS: "Using these consensus spectra, we created a molecular network in GNPS"
- [full_text] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%: "The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%"
