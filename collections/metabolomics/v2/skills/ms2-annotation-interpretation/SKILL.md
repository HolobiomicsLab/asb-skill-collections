---
name: ms2-annotation-interpretation
description: Use when after GNPS spectral library search has returned matched chemical annotations (with m/z values and cosine similarity scores) for MS/MS spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MassIVE
  - GNPS
  - ReDU
  - Emperor
  - MetaboLights
  techniques:
  - CE-MS
  - MS-imaging
derived_from:
- doi: 10.1038/s41592-020-0916-7
  title: ReDU
- doi: 10.1186/2047-217x-2-16
  title: ''
evidence_spans:
- ReDU only interacts with MassIVE
- data uploaded to MassIVE as a public dataset
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_redu_cq
    doi: 10.1038/s41592-020-0916-7
    title: ReDU
  dedup_kept_from: coll_redu_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-020-0916-7
  all_source_dois:
  - 10.1038/s41592-020-0916-7
  - 10.1186/2047-217x-2-16
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS2 Annotation Interpretation

## Summary

Interpret and contextualize chemical annotations derived from tandem MS (MS/MS) spectral library matching, understanding their confidence level, potential multiplicity, and implications for metabolite identification in high-throughput datasets. This skill bridges raw spectral matches to scientifically valid chemical identities by applying metabolomics confidence standards.

## When to use

After GNPS spectral library search has returned matched chemical annotations (with m/z values and cosine similarity scores) for MS/MS spectra. Use this skill when deciding which annotations are reliable enough for downstream statistical analysis, when reconciling the same chemical appearing under multiple annotation names due to MS/MS spectral variation, or when preparing annotations for publication or public deposition.

## When NOT to use

- Input is raw, unconverted mass spectrometry data files (e.g., .raw, .d)—apply file format conversion first, then spectral library matching, before interpreting annotations.
- Spectral library search has not yet been performed or no matched annotations are available—first execute GNPS spectral library search workflow on the MS/MS spectra.
- You are working with a closed, proprietary spectral reference library or in-house standards without MSI confidence classification metadata—annotation interpretation depends on standardized confidence frameworks.

## Inputs

- GNPS spectral library search results table (containing matched chemical names, m/z values, cosine similarity scores, and file detection information)
- Binary or weighted detection matrix (rows = files, columns = chemical identities, values = detection status or MS2 abundance)

## Outputs

- Annotated detection matrix with confidence-level metadata (level 2 or level 3 MSI classification per chemical)
- Consolidated chemical annotation list (deduplicated variants of the same chemical with confidence justification)
- Annotation quality report documenting cosine similarity ranges, MS/MS spectral variation patterns, and any cross-database validations performed

## How to apply

First, classify each GNPS annotation by its confidence level according to the 2007 Metabolomics Standards Initiative: level 2 annotations are putative identifications based on spectral library similarity (sufficient for exploratory analysis), while level 3 annotations represent putatively characterized compound classes (weaker confidence). Recognize that the same chemical often yields multiple GNPS annotations due to slight variation in m/z values or peak abundances in the MS/MS spectra, even when comparing against the same reference standard—consolidate these variants if the cosine similarity scores and precursor m/z values are consistent and the chemical identity is the same. Apply additional filtering based on your experimental design: if only high-confidence identifications are needed (e.g., for mechanistic studies), retain only level 2 annotations with cosine similarity above study-specific thresholds. Document the annotation confidence level assigned to each chemical in your detection matrix or feature table so downstream consumers understand the identification certainty. Cross-reference ambiguous or novel annotations against complementary databases (e.g., MetaboLights) when available to increase confidence.

## Related tools

- **GNPS** (Performs spectral library matching and generates the initial matched chemical annotations against reference MS/MS spectra that are interpreted by this skill) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ReDU** (Provides interface to explore and filter GNPS-annotated public MS/MS data by sample information and chemical identity, enabling validation and interpretation of annotations at repository scale) — https://github.com/mwang87/ReDU-MS2-GNPS
- **Emperor** (Visualizes high-dimensional annotation and sample metadata via PCA score plots to support interpretation and exploration of annotation patterns across files) — https://github.com/biocore/emperor
- **MetaboLights** (Cross-reference database for validating or resolving ambiguous GNPS chemical annotations when MSI confidence levels are unclear)

## Evaluation signals

- Each chemical annotation in the final detection matrix is tagged with an explicit MSI confidence level (level 2 or level 3) and cosine similarity score ≥ study-defined threshold.
- Duplicate or variant annotations of the same chemical (same chemical name, slight m/z or peak variation) are consolidated; the deduplication logic and retained representative annotation are documented.
- Cosine similarity score distribution across all matched annotations falls within biologically expected ranges (typically > 0.6–0.7 for good spectral matches); outliers are flagged and reviewed.
- Cross-validation against a secondary database (e.g., MetaboLights or in-house standards) confirms identity of a random sample of level 2 or level 3 annotations, with agreement documented.
- Detection matrix rows (files) and columns (chemicals) are consistent; no file or chemical is duplicated or missing; all cells contain valid 0/1 or abundance values.

## Limitations

- The same chemical can yield multiple GNPS annotations due to MS/MS spectral variation (slight differences in m/z or peak abundance); manual or computational deduplication is required and adds subjectivity.
- GNPS annotations via spectral library matching are inherently limited to chemicals present in the reference library; novel or rare compounds will not be annotated, leading to false negatives.
- MSI level 2 and level 3 annotations carry lower confidence than level 1 (confirmed by chemical standard) or MS/MS structure elucidation; unsuitable for definitive structural assignment or regulatory claims without orthogonal validation.
- Cosine similarity thresholds and confidence cutoffs are not standardized across studies; interpretation reproducibility depends on explicit documentation of parameters and thresholds used.

## Evidence

- [abstract] GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on: "GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on"
- [abstract] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical"
- [other] GNPS library search compares MS2 product-ion spectra against reference fragmentation patterns in its public spectral library, producing tabulated chemical annotations with file detection information: "GNPS library search compares MS2 product-ion spectra against reference fragmentation patterns in its public spectral library, producing tabulated chemical annotations with file detection information"
- [other] retrieve the spectral library matching results table containing matched chemical annotations, m/z values, and cosine similarity scores: "retrieve the spectral library matching results table containing matched chemical annotations, m/z values, and cosine similarity scores"
- [abstract] Chemical annotation is performed in GNPS by comparing MS2 spectra against the GNPS reference spectral library: "Chemical annotation is performed in [GNPS](https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp) by comparing MS2 spectra"
