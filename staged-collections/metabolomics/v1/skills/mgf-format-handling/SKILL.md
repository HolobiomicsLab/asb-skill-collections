---
name: mgf-format-handling
description: Use when handling metabolomics data by loading and parsing tandem MS spectra from MGF (Mascot Generic Format) files for downstream clustering, networking, or querying.
when_to_use_negative:
- When working with vendor-specific binary formats (Thermo .raw, Waters .raw) without prior conversion—use native converters (RawFileReader, CDCReader) first.
- When you only have precursor m/z and intensity (MS1 level data)—MGF is designed for MS/MS (MS2) spectra with fragment ion information.
- When your analysis requires chromatographic trace information or ion mobility data that is not adequately represented in flat MGF format—consider mzML or mzXML for richer metadata.
edam_operation: http://edamontology.org/operation_3357
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3148
- http://edamontology.org/topic_3520
tools:
- name: MassQL
  role: Query language and retrieval engine that outputs MS/MS spectra in MGF format from repository-scale searches
  repo: https://github.com/mwang87/MassQueryLanguage
- name: pyteomics
  role: Python library used by MassQL reference engine to read and parse MGF, mzML, and mzXML files into data structures
- name: MS-Cluster
  role: Clustering tool that takes retrieved MGF spectra as input and outputs consensus spectra in MGF format
- name: Falcon-MS
  role: Alternative clustering tool for collapsing redundant MS/MS observations from MGF inputs
- name: MZmine
  role: Open-source MS data processing software with native MassQL and MGF support for workflow integration
  repo: https://github.com/mzmine/mzmine
- name: GNPS
  role: Global repository and molecular networking platform that accepts MGF files and integrates MassQL query results
- name: MS-DIAL
  role: Open-source peak detection and MS/MS spectral processing software with native MassQL support
- name: UniDec
  role: Deconvolution software supporting open MS data formats including those derived from MGF queries
  repo: https://github.com/michaelmarty/UniDec
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
    - outputs/audit_s41592_full/skills/mgf-format-handling/SKILL.md
    - outputs/audit_s41592_full/skills/mgf-format-handling/skill.md
    merged_at: '2026-05-25T07:33:56.397099+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/mgf-format-handling@sha256:8e4e828983262e7fae14a968cac6b4b7483e75747e7bae88202977f951362756
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1038/s41592-025-02660-z
---

# mgf-format-handling

## Summary

Loading and parsing tandem MS spectra from MGF (Mascot Generic Format) files for downstream clustering, networking, or querying. MGF is a human-readable text format widely supported by mass spectrometry analysis tools and repositories, making it essential for exchange of MS/MS spectral data.

## When to use

When you have retrieved MS/MS spectra from a repository (e.g., GNPS/MassIVE) via MassQL query or other retrieval methods and need to load them into clustering tools (MS-Cluster, Falcon-MS), molecular networking platforms (GNPS), or Python-based analysis pipelines. MGF format is the standard output of MassQL queries and is natively supported by most open-source MS analysis software.

## When NOT to use

- When working with vendor-specific binary formats (Thermo .raw, Waters .raw) without prior conversion—use native converters (RawFileReader, CDCReader) first.
- When you only have precursor m/z and intensity (MS1 level data)—MGF is designed for MS/MS (MS2) spectra with fragment ion information.
- When your analysis requires chromatographic trace information or ion mobility data that is not adequately represented in flat MGF format—consider mzML or mzXML for richer metadata.

## Inputs

- MGF files (Mascot Generic Format) containing MS/MS spectra with precursor m/z, charge state, and product ion lists
- Query results from MassQL or manual downloads from MS repositories (GNPS/MassIVE, Metabolomics Workbench, MetaboLights)
- mzML or mzXML files (alternative open formats supported by the same toolchain)

## Outputs

- In-memory MS/MS spectral data frame or parsed spectrum objects ready for filtering and clustering
- Consensus MGF files (output from MS-Cluster or Falcon-MS clustering step)
- Filtered spectral datasets prepared for molecular networking in GNPS or spectral library searching

## How to apply

Load MGF files using a library that supports open MS data formats (pyteomics in Python, or native support in tools like MZmine, MS-DIAL, UniDec). The MassQL reference engine uses pyteomics to read MGF files and convert them into a data frame structure for filtering and downstream analysis. Ensure all required MS/MS metadata (precursor m/z, charge state, product ion m/z values, retention time) are present in the MGF headers. After retrieval, cluster redundant spectra using MS-Cluster or Falcon-MS (with default settings) to generate consensus spectra, which reduces redundancy (e.g., 72% reduction in the iron-binding case, from 26,944 to 7,504 consensus spectra) and improves downstream molecular network quality.

## Related tools

- **MassQL** (Query language and retrieval engine that outputs MS/MS spectra in MGF format from repository-scale searches) — https://github.com/mwang87/MassQueryLanguage
- **pyteomics** (Python library used by MassQL reference engine to read and parse MGF, mzML, and mzXML files into data structures)
- **MS-Cluster** (Clustering tool that takes retrieved MGF spectra as input and outputs consensus spectra in MGF format)
- **Falcon-MS** (Alternative clustering tool for collapsing redundant MS/MS observations from MGF inputs)
- **MZmine** (Open-source MS data processing software with native MassQL and MGF support for workflow integration) — https://github.com/mzmine/mzmine
- **GNPS** (Global repository and molecular networking platform that accepts MGF files and integrates MassQL query results)
- **MS-DIAL** (Open-source peak detection and MS/MS spectral processing software with native MassQL support)
- **UniDec** (Deconvolution software supporting open MS data formats including those derived from MGF queries) — https://github.com/michaelmarty/UniDec

## Examples

```
from pyteomics import mgf; spectra = list(mgf.read('query_results.mgf')); print(f'Loaded {len(spectra)} MS/MS spectra'); df = pd.DataFrame([{'precursor_mz': s['precursor_mz'][0][0], 'charge': s['precursor_mz'][0][1], 'products': s['m/z']} for s in spectra])
```

## Evaluation signals

- MGF file successfully parses without errors; all required MS/MS spectra fields (precursor m/z, charge, product ions) are present and correctly formatted.
- Loaded spectra count matches expected count from MassQL query output or repository manifest (e.g., 26,944 spectra retrieved for iron-binding case).
- Downstream clustering tool (MS-Cluster, Falcon-MS) accepts parsed MGF data without format errors and produces consensus spectra output.
- Consensus spectral count and redundancy reduction align with expected ranges (e.g., 72% reduction observed in case study, from 26,944 to 7,504 spectra).
- Spectral metadata (retention time, mobility, polarity) are preserved through MGF loading and available for filtering and molecular networking steps.

## Limitations

- MGF format has limited capability to preserve chromatographic context—consecutive MS spectra or ion mobility information from a single feature may be represented as separate entries, making it harder to reconstruct the original LC-MS trace.
- Mass accuracy and intensity tolerance parameters used during query retrieval (e.g., ±20 ppm, 25% intensity window for isotope patterns) are not stored in MGF headers; users must track these externally or re-specify them during downstream filtering.
- Low-intensity product ions or isotope peaks falling outside expected intensity thresholds may be omitted from MGF entries during initial query, potentially missing valid compounds (e.g., one siderophore with low-intensity ⁵⁴Fe peak was missed by MassQL due to 25% intensity tolerance).
- MGF format is primarily designed for MS/MS (MS2) data; high-resolution MS1 precursor spectra are not typically included, limiting use for certain deconvolution or intact mass-based analyses.

## Evidence

- [full_text] Load 26,944 MS/MS spectra retrieved from GNPS/MassIVE iron-binding MassQL query (in MGF format)
- [full_text] The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats
- [full_text] Output 7,504 consensus MS/MS spectra (representative peaks per cluster) in MGF format
- [full_text] We used MS-Cluster on the retrieved MS/MS spectra to collapse redundant observations
- [full_text] MassQL has limited capabilities to leverage more than a handful of MS spectra, for example, consecutive MS spectra arising
- [full_text] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%