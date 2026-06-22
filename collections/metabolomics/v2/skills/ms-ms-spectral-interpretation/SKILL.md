---
name: ms-ms-spectral-interpretation
description: Use when you have acquired MS/MS spectral data (in mzML, mzXML, or equivalent format) for unknown compounds and need to identify the most probable metabolite structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3370
  tools:
  - MAGMa
  - PubChem
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma_cq
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma_cq
schema_version: 0.2.0
---

# ms-ms-spectral-interpretation

## Summary

Interpret tandem mass spectrometry (MS/MS) spectra by matching experimental fragment ion peaks against theoretical fragmentations of candidate metabolites, ranked by cosine similarity or peak-matching scoring. This skill is essential when you need to annotate unknown metabolites from high-resolution MS/MS data in metabolomics workflows.

## When to use

Apply this skill when you have acquired MS/MS spectral data (in mzML, mzXML, or equivalent format) for unknown compounds and need to identify the most probable metabolite structure. Specifically use it when you have a parent mass or molecular formula and want to rank candidate structures by how well their theoretical fragmentation pattern matches your experimental spectrum.

## When NOT to use

- Input is already a putatively identified metabolite with high-confidence assignment — re-annotation adds no value.
- MS/MS spectral quality is poor (low signal-to-noise, sparse fragmentation, or < 3 informative peaks) — annotation scores will be unreliable.
- Parent mass is unknown or ambiguous (e.g., from low-resolution or uncalibrated instrument) — candidate filtering will be too broad.

## Inputs

- MS/MS spectral data (mzML, mzXML, or equivalent format)
- Parent mass or molecular formula
- PubChem candidate structure database or enumerated metabolite structure set

## Outputs

- Ranked list of metabolite candidates with annotation scores
- Match statistics (cosine similarity, peak-matching metrics, mass accuracy)
- Theoretical fragment ion assignments for top-ranked candidates

## How to apply

Load the experimental MS/MS spectrum and initialize the annotation job with the parent mass or molecular formula. Generate candidate in silico metabolite structures (typically via PubChem database lookup or structure enumeration). For each candidate, calculate theoretical fragment ions using fragmentation rules. Score each candidate by comparing experimental MS/MS peaks against theoretical fragments using cosine similarity or a peak-matching algorithm that weights peak intensity and mass accuracy. Rank metabolite candidates by annotation score and examine the ranked list, accepting candidates with high match statistics (typically cosine similarity > 0.7 or similar threshold, depending on your mass accuracy and spectral resolution).

## Related tools

- **MAGMa** (Implements in silico metabolite generation and MS/MS spectral matching; performs candidate ranking via theoretical fragment ion comparison) — https://github.com/NLeSC/MAGMa
- **PubChem** (Provides molecular structure database for candidate metabolite lookup and in silico structure enumeration)

## Evaluation signals

- Top-ranked candidate(s) have cosine similarity or peak-matching score above your acceptance threshold (typically > 0.7 for high-resolution data).
- Experimental MS/MS peaks align with predicted fragment ions from the top candidate within your specified mass tolerance (e.g., 5 ppm).
- Ranked list shows clear separation between top-scoring candidate and lower-ranked alternatives (e.g., score gap > 0.1–0.2 in cosine similarity).
- Known control metabolites or internal standards yield correct top-ranked annotation (positive control validation).
- Peak-matching algorithm reports consistent fragment assignments with chemical feasibility (e.g., fragments respect known bond-breaking rules).

## Limitations

- Annotation accuracy depends critically on PubChem coverage — metabolites absent from the database cannot be identified.
- Fragmentation rules and in silico fragmentation models may not capture all instrument-specific fragmentation behavior, leading to false negatives for unusual fragmentation patterns.
- Cosine similarity and peak-matching metrics are sensitive to mass calibration accuracy and spectral noise; poor spectral quality or miscalibration inflates false-positive scores.
- Isomeric and isobaric compounds produce identical or near-identical parent masses and may yield ambiguous rankings without additional orthogonal data (e.g., retention time, isotope pattern).

## Evidence

- [other] Generate in silico metabolites and match them against MS/MS data, as part of MAGMa (Ms Annotation based on in silico Generated Metabolites): "The job subproject implements metabolite annotation by generating in silico metabolites and matching them against MS/MS data, as part of MAGMa (Ms Annotation based on in silico Generated Metabolites)."
- [other] Workflow steps for spectral interpretation: "Load MS/MS spectral data from input file (mzML, mzXML, or equivalent format). Initialize MAGMa job with molecular formula or parent mass and MS/MS spectrum. Generate in silico metabolite structures"
- [readme] Project goal and chemo-informatics methods: "The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow."
- [readme] MAGMa abbreviation and scope: "MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'."
