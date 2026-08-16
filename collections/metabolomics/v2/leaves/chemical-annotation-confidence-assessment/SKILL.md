---
name: chemical-annotation-confidence-assessment
description: Use when when you have received chemical annotations from GNPS spectral
  library matching workflow and need to assess their reliability before downstream
  analysis (e.g., chemical explorer visualization, sample filtering, or comparative
  metabolomics).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MassIVE
  - GNPS
  - ReDU
  - Emperor
  techniques:
  - CE-MS
  - MS-imaging
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-annotation-confidence-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate the confidence level of chemical annotations produced by GNPS spectral library matching against MS2 product-ion spectra using the 2007 metabolomics standards initiative (MSI) classification scheme. This skill distinguishes between level 2 (putative annotation based on spectral library similarity) and level 3 (putatively characterized compound class) annotations to contextualize the reliability of chemical identifications in reanalyzed public mass spectrometry data.

## When to use

When you have received chemical annotations from GNPS spectral library matching workflow and need to assess their reliability before downstream analysis (e.g., chemical explorer visualization, sample filtering, or comparative metabolomics). This is particularly important in ReDU reanalysis workflows where public data from heterogeneous sources are pooled and annotated in batch, and you need to document the evidence level supporting each identification.

## When NOT to use

- Input contains only compound masses without MS2 spectral data — MSI level classification requires spectral library matching evidence, not mass matching alone.
- Annotations have already been manually curated or validated by authentic standards — use your existing confidence metadata instead of re-classifying.
- You require level 1 confidence (exact match to a reference standard analyzed in-house) — GNPS library matching produces only level 2 or 3 per the MSI scheme.

## Inputs

- GNPS spectral library matching results table (TSV format containing matched chemical annotations, m/z values, and cosine similarity scores)
- MS2 product-ion spectra in open format (.mzML or .mzXML) used as input to GNPS workflow
- GNPS reference spectral library identifiers or library match metadata

## Outputs

- Annotated detection matrix with confidence level assignments (rows = files, columns = chemical identities, metadata column = MSI confidence level per annotation)
- Audit report listing chemicals with multiple GNPS annotations and their cosine similarity scores
- Tab-separated table with columns: chemical identity, m/z, cosine similarity, MSI confidence level (2 or 3), file detection pattern

## How to apply

After GNPS spectral library search completes and produces a detection matrix with matched chemical annotations and cosine similarity scores, classify each annotation according to the 2007 MSI metabolomics standard: assign level 2 confidence when the annotation is based on spectral library similarity (a reference fragmentation pattern matched the observed MS2 spectrum with a high cosine score), and assign level 3 when only the compound class can be putatively characterized. Document that the same chemical compound may receive multiple distinct GNPS annotations due to subtle variations in m/z values or fragment abundances between the same compound's MS2 spectra across different files or acquisition conditions; this multiplicity is expected and does not invalidate the annotations but should be collapsed or flagged during downstream interpretation. Use the cosine similarity score from the spectral match output as supporting evidence: higher scores (typically >0.7) indicate stronger confidence in the level 2 assignment. Retain the full annotation record (chemical name, m/z, cosine score, level) in the tabulated output for audit and reproducibility.

## Related tools

- **GNPS** (Performs spectral library matching against reference fragmentation patterns and outputs cosine similarity scores and chemical annotations required for confidence assessment) — https://github.com/CCMS-UCSD/GNPSDocumentation
- **MassIVE** (Public mass spectrometry data repository from which MS2 spectra are retrieved and submitted to GNPS for library matching and annotation) — https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp
- **ReDU** (Bridges GNPS and MassIVE; manages batch reanalysis of public MS2 data and aggregates annotations across files for population-scale confidence assessment) — https://github.com/mwang87/ReDU-MS2-GNPS
- **Emperor** (Provides interactive visualization of chemical annotations and their confidence levels across samples via PCA score plots and sample filtering) — https://github.com/biocore/emperor

## Evaluation signals

- All annotations in the output table are assigned either MSI level 2 or level 3; no unannotated or unclassified entries remain.
- Cosine similarity scores for level 2 annotations are ≥ 0.7 (or the site-specific threshold documented in GNPS output); scores below this threshold are downgraded to level 3 or flagged with reduced confidence.
- Duplicate chemical identifications within a single file are identified and reconciled (e.g., multiple MS2 spectra of the same chemical with slight m/z shifts produce separate rows but are annotated with the same chemical name and consistent confidence level).
- For a spot-check of 10–20 randomly selected annotations, verify that the cosine similarity score, m/z delta, and fragment ion alignment visible in GNPS match report align with the assigned MSI level.
- Detection matrix row sums and column sums (file counts and chemical counts) remain consistent before and after confidence assignment; no data loss during transformation.

## Limitations

- GNPS spectral library matching produces only level 2 or level 3 annotations per MSI 2007 standards; level 1 confidence (authentic standard match) cannot be assigned from library searches alone.
- The same chemical compound may appear under multiple GNPS annotations due to slight MS2 spectral variations across files or instruments; multiplicity must be documented but does not imply annotation error—it reflects legitimate analytical variation and requires manual chemical consolidation for some downstream uses.
- Cosine similarity score thresholds are heuristic and site-specific; the 0.7 threshold used here is illustrative and may require adjustment based on instrument type, ionization mode, or dataset characteristics.
- Confidence assessment depends entirely on the completeness and accuracy of the GNPS reference spectral library; novel or rarely-observed compounds absent from the library will not be detected or annotated regardless of their presence in the sample.

## Evidence

- [abstract] GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on: "GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on"
- [abstract] The same chemical can have multiple GNPS annotations due to slight variation in MS2 spectra: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical"
- [other] GNPS library search compares MS2 product-ion spectra against reference fragmentation patterns: "GNPS library search compares MS2 product-ion spectra against reference fragmentation patterns in its public spectral library, producing tabulated chemical annotations with file detection information"
- [methods] Chemical annotation is performed in GNPS by comparing MS2 spectra: "Chemical annotation is performed in [GNPS](https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp) by comparing MS2 spectra"
- [readme] ReDU is a community-minded approach to find and reuse public data containing tandem MS data at the repository scale: "ReDU is a community-minded approach to find and reuse public data containing tandem MS data at the repository scale. ReDU is a launchpad for co- or re-analysis of public data via the Global Natural"
