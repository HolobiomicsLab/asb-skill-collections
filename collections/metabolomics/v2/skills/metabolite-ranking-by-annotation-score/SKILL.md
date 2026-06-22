---
name: metabolite-ranking-by-annotation-score
description: Use when when you have generated a set of candidate metabolites for a given experimental MS/MS spectrum and need to determine which candidate is most likely to be the true metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MAGMa
  techniques:
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5702/massspectrometry.S0033
  all_source_dois:
  - 10.5702/massspectrometry.S0033
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-ranking-by-annotation-score

## Summary

Rank candidate metabolites by comparing experimental MS/MS peaks against theoretical fragment ions using cosine similarity or peak-matching algorithms. This skill identifies the most probable metabolite annotations from a scored candidate list, enabling prioritization of biochemically relevant hits in untargeted metabolomics workflows.

## When to use

When you have generated a set of candidate metabolites for a given experimental MS/MS spectrum and need to determine which candidate is most likely to be the true metabolite. Apply this skill after in silico fragmentation has produced theoretical fragment ion patterns for each candidate, and experimental peaks have been acquired from a high-resolution mass spectrometer in mzML, mzXML, or equivalent format.

## When NOT to use

- Input candidate set contains only a single metabolite (ranking is not meaningful).
- Experimental MS/MS spectrum is of insufficient quality (e.g., <5 reliable peaks or very low signal-to-noise ratio).
- Theoretical fragment ion library is unavailable or not pre-computed for the candidate set.

## Inputs

- experimental MS/MS spectrum (m/z and intensity pairs)
- set of candidate metabolite structures with molecular formulas
- theoretical fragment ion predictions for each candidate

## Outputs

- ranked list of metabolite candidates with annotation scores
- match statistics per candidate (cosine similarity, matched peak count, mass error)

## How to apply

For each candidate metabolite, calculate theoretical fragment ions using established fragmentation rules. Compare the experimental MS/MS peak list against the theoretical fragments for each candidate by computing cosine similarity or peak-matching scores, which quantify the overlap and intensity agreement between observed and predicted peaks. Score each candidate according to the quality of this match. Rank all candidates by descending annotation score, with the highest-scoring candidate representing the most probable metabolite identity. Output the ranked list with match statistics (e.g., cosine similarity values, number of matched peaks, mass error in ppm) to allow downstream filtering and confidence assessment.

## Related tools

- **MAGMa** (performs in silico metabolite annotation including candidate generation, theoretical fragmentation, and ranking by peak-matching score) — https://github.com/NLeSC/MAGMa

## Evaluation signals

- Ranked list contains all candidate metabolites with no duplicates and scores in descending order.
- Annotation scores (cosine similarity or peak-matching metric) fall within expected range [0, 1] or are monotonically bounded.
- Top-ranked metabolite shows mass error within instrument tolerance (typically <5 ppm for high-resolution MS) and matched peak count ≥3.
- Comparison of ranked scores against known standard compounds (if available) shows the true metabolite ranked in top-N (e.g., top-3) candidates.
- Output schema includes all expected fields: metabolite identifier/name, annotation score, matched peak count, mass error, and rank position.

## Limitations

- Ranking accuracy depends critically on the quality and completeness of the theoretical fragmentation model; incorrect fragmentation rules will produce misleading scores.
- Cosine similarity and peak-matching algorithms are sensitive to mass calibration errors and instrument-specific peak intensity variation, which can misrank candidates with similar fragment patterns.
- PubChem database lookup may miss novel, biosynthetic, or rare metabolites not in the reference database, limiting the candidate set.
- High spectral noise or low precursor mass resolution can reduce discrimination between candidates with overlapping fragment ion patterns.

## Evidence

- [other] Score each candidate by comparing experimental MS/MS peaks against theoretical fragments using cosine similarity or peak-matching algorithm.: "Score each candidate by comparing experimental MS/MS peaks against theoretical fragments using cosine similarity or peak-matching algorithm."
- [other] Rank metabolite candidates by annotation score and output ranked list with match statistics.: "Rank metabolite candidates by annotation score and output ranked list with match statistics."
- [other] Calculate theoretical fragment ions for each candidate metabolite via fragmentation rules.: "Calculate theoretical fragment ions for each candidate metabolite via fragmentation rules."
- [readme] The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow.: "The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow."
