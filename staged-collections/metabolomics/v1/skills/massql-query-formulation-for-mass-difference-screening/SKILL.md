---
name: massql-query-formulation-for-mass-difference-screening
description: Formulate and execute MassQL queries to systematically filter MS/MS spectra for specific neutral loss patterns (e.g., pentosylation or hexosylation) to annotate post-translationally modified metabolites in untargeted LC-MS/MS datasets. This skill enables rapid, high-throughput discovery of glycosylated or sugar-conjugated metabolites without manual spectral inspection.
when_to_use_negative:
- Input is tandem MS data with very low mass accuracy (>20 ppm instrument resolution) — neutral loss screening relies on precise mass matching and may suffer false positives or negatives.
- Target modification has a neutral loss mass that overlaps with common fragments from unmodified background compounds — specificity will degrade and manual filtering will be required.
- MS/MS spectra lack sufficient fragmentation intensity or dissociation efficiency to produce detectable neutral losses — no signal will be found regardless of MassQL specificity.
edam_operation: http://edamontology.org/operation_3631
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3172
tools:
- name: GNPS
  role: web platform hosting MassQL query engine, molecular networking workflows, and MS/MS spectral reference library; used to execute neutral loss queries and retrieve annotated spectra
- name: MassQL
  role: query language integrated into GNPS for formulating and executing high-throughput neutral loss and fragment ion filtering on MS/MS spectra
- name: LC-MS/MS
  role: analytical instrument producing raw MS/MS spectra containing neutral loss patterns for subsequent filtering
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1073/pnas
    title: Proceedings of the National Academy of Sciences
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/massql-query-formulation-for-mass-difference-screening@sha256:e8feba18dd18ff6631f574b74b18d72f57f828d92afad7bf695d8d343036096c
---

# massql-query-formulation-for-mass-difference-screening

## Summary

Formulate and execute MassQL queries to systematically filter MS/MS spectra for specific neutral loss patterns (e.g., pentosylation or hexosylation) to annotate post-translationally modified metabolites in untargeted LC-MS/MS datasets. This skill enables rapid, high-throughput discovery of glycosylated or sugar-conjugated metabolites without manual spectral inspection.

## When to use

Apply this skill when you have feature-based molecular networking output from GNPS with MS/MS spectra and need to identify metabolites bearing characteristic neutral losses (e.g., 132.0423 Da for pentose, 162.0528 Da for hexose). Use it when manual spectral annotation of modified metabolites would be prohibitively slow, or when you want to systematize discovery of a specific chemical modification class across hundreds of spectral nodes.

## When NOT to use

- Input is tandem MS data with very low mass accuracy (>20 ppm instrument resolution) — neutral loss screening relies on precise mass matching and may suffer false positives or negatives.
- Target modification has a neutral loss mass that overlaps with common fragments from unmodified background compounds — specificity will degrade and manual filtering will be required.
- MS/MS spectra lack sufficient fragmentation intensity or dissociation efficiency to produce detectable neutral losses — no signal will be found regardless of MassQL specificity.

## Inputs

- Feature-based molecular networking (FBMN) job output from GNPS (spectral nodes and edges)
- MS/MS spectra in mzML, mzXML, or NetCDF format uploaded to GNPS
- Theoretical neutral loss mass for target modification (Da)

## Outputs

- Filtered set of spectral node IDs exhibiting the target neutral loss
- Annotated molecular network subgraph highlighting modified metabolite clusters
- List of putative glycosylated or sugar-conjugated metabolites with structure proposals

## How to apply

Identify the target neutral loss mass corresponding to the modification of interest (e.g., 132.0423 Da for xylose, 162.0528 Da for glucose). Construct a MassQL query filtering for MS/MS spectra containing that neutral loss within typical mass accuracy tolerance (5 ppm or better). Execute the query against the GNPS spectral library or your uploaded dataset via the GNPS web interface. Cross-reference returned spectral nodes with the molecular network to cluster and visualize modified metabolite families. Validate hits by comparing detected nodes against known reference compounds or by orthogonal methods (NMR, high-resolution MS/MS fragmentation patterns). The rationale is that neutral loss screening is orders of magnitude faster than manual curation while maintaining specificity when the target loss is biochemically distinct.

## Related tools

- **GNPS** (web platform hosting MassQL query engine, molecular networking workflows, and MS/MS spectral reference library; used to execute neutral loss queries and retrieve annotated spectra)
- **MassQL** (query language integrated into GNPS for formulating and executing high-throughput neutral loss and fragment ion filtering on MS/MS spectra)
- **LC-MS/MS** (analytical instrument producing raw MS/MS spectra containing neutral loss patterns for subsequent filtering)

## Examples

```
Query GNPS MassQL via web interface: Filter MS/MS spectra for neutral loss = 132.0423 ± 0.01 Da to retrieve pentosylated metabolite spectral nodes; cross-reference hits against feature-based molecular network (FBMN job output) to identify xylosylated clusters and candidate structures.
```

## Evaluation signals

- Returned spectral nodes exhibit consistent neutral loss masses within ±5 ppm (typical GNPS mass accuracy) of the theoretical target loss (e.g., 132.04 ± 0.01 Da for pentose).
- Annotated metabolites from query hits align with known reference standards or prior literature reports for the target modification class (e.g., seven xylosylated compounds 2a–2g match isolation and NMR characterization).
- Cross-validation: orthogonal structural characterization (NMR, MS/MS fragmentation pattern, or acidic hydrolysis) confirms sugar conjugation on ≥50% of randomly sampled hits.
- Molecular network subgraph clustering shows strong cosine similarity (>0.7) among returned nodes, indicating they represent chemically related modified metabolites rather than unrelated noise.
- Query sensitivity check: known positive controls (reference compounds with target modification) are successfully recovered by the MassQL query.

## Limitations

- Neutral loss specificity depends on biochemical rarity of the target loss mass — if the modification shares a neutral loss with common unmodified fragments, false positives will increase.
- Requires adequate MS/MS fragmentation intensity; compounds with weak or dominant parent ion loss may not exhibit sufficient neutral loss signal for detection.
- MassQL queries return spectral annotations, not structural assignments — subsequent manual curation, comparison to reference spectra, or orthogonal characterization (NMR, HPLC-UV, etc.) is necessary to confirm identity and regioisomer assignment.
- Performance scales with spectral library size; queries against small or incomplete reference libraries will miss metabolites absent from the library, leading to underestimation of modification prevalence.

## Evidence

- [results] MassQL successfully annotated hexosylation and pentosylation by detecting neutral losses of 162.05 Da and 132.04 Da in MS/MS fragmentation spectra: "MassQL successfully annotated hexosylation and pentosylation by detecting neutral losses of 162.05 Da and 132.04 Da in MS/MS fragmentation spectra, enabling rapid annotation of glycosylated flavonoid"
- [results] MassQL was helpful for the annotation of sugar conjugation, as it rapidly annotated hexosylation and pentosylation of the flavonoids: "MassQL was helpful for the annotation of sugar conjugation, as it rapidly annotated hexosylation and pentosylation of the flavonoids"
- [other] Apply MassQL queries within GNPS to filter for MS/MS spectra exhibiting neutral losses of 132.0423 Da (pentosylation) or 162.0528 Da (hexosylation): "Apply MassQL queries within GNPS to filter for MS/MS spectra exhibiting neutral losses of 132.0423 Da (pentosylation) or 162.0528 Da (hexosylation)"
- [results] MS/MS spectra containing neutral losses of 132.0423 or 162.0528 Da were searched via MassQL: "MS/MS spectra containing neutral losses of 132.0423 or 162.0528 Da were searched via MassQL"
- [other] Cross-reference MassQL-annotated spectral nodes with the molecular network to identify clusters corresponding to pentosylated and hexosylated metabolites: "Cross-reference MassQL-annotated spectral nodes with the molecular network to identify clusters corresponding to pentosylated and hexosylated metabolites"
