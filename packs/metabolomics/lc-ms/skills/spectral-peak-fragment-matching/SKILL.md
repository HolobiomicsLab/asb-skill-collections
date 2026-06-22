---
name: spectral-peak-fragment-matching
description: Use when you have MS/MS spectral data (mzML, mzXML format) and a parent mass or molecular formula, and you need to identify the metabolite(s) responsible for the observed fragmentation pattern by scoring candidates against their theoretical fragmentation profiles.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - MAGMa
  - PubChem
  techniques:
  - LC-MS
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

# spectral-peak-fragment-matching

## Summary

A chemo-informatics method for annotating metabolites by comparing experimental MS/MS spectral peaks against in silico-generated fragment ion signatures. The skill ranks candidate metabolites by cosine similarity or peak-matching score to enable metabolite identification from mass spectrometry data.

## When to use

Apply this skill when you have MS/MS spectral data (mzML, mzXML format) and a parent mass or molecular formula, and you need to identify the metabolite(s) responsible for the observed fragmentation pattern by scoring candidates against their theoretical fragmentation profiles.

## When NOT to use

- The input is already a curated list of identified metabolites (annotation is complete).
- MS/MS data is absent or severely fragmented; peak-matching requires sufficient spectral richness.
- Candidate metabolite structures or formulas are not available (the skill requires a pre-computed candidate pool, typically from mass lookup).

## Inputs

- MS/MS spectral data (mzML, mzXML, or equivalent format with m/z and intensity pairs)
- Experimental peak list (m/z, intensity values)
- Parent mass or molecular formula
- Candidate metabolite structures (or list of molecular formulas to lookup)
- Mass tolerance parameter (in ppm or Daltons)

## Outputs

- Ranked list of candidate metabolites with annotation scores
- Match statistics (e.g., number of matched peaks, cosine similarity value)
- Theoretical fragment ion assignments for top candidates

## How to apply

For each candidate metabolite (typically pre-filtered by mass from a database like PubChem), compute the theoretical m/z values of fragment ions using known fragmentation rules or chemical structure-based prediction. Then compare the experimental MS/MS peak list against the theoretical fragments using cosine similarity or peak-matching algorithms, which measure overlap in m/z position and intensity. Score each candidate by the degree of match, applying any mass tolerance threshold (e.g., 5 ppm or Daltons). Rank candidates by annotation score in descending order. The rationale is that true metabolites will exhibit high spectral similarity due to their real chemical fragmentation pathways, whereas false positives will scatter across lower scores.

## Related tools

- **MAGMa** (Implements in silico metabolite annotation by generating candidate structures, calculating theoretical fragments, and scoring them against experimental MS/MS spectra) — https://github.com/NLeSC/MAGMa
- **PubChem** (Source database for candidate metabolite structures and formulas to be matched against experimental peaks)

## Evaluation signals

- Top-ranked candidate(s) are known or validated metabolites (ground truth check).
- Cosine similarity or peak-matching score for the correct metabolite is significantly higher than decoy scores (e.g., >0.7 vs. <0.3).
- Number of matched experimental peaks to theoretical fragments is consistent with the expected fragmentation complexity of the true metabolite.
- Mass tolerance violations (outlier m/z mismatches) are absent or minimal in the top match.
- Annotation score distribution is bimodal or multimodal, indicating clear separation between true and false candidates.

## Limitations

- Performance depends on the quality and completeness of the candidate metabolite database (PubChem); rare or novel metabolites may not be present.
- Fragmentation rules and in silico prediction algorithms may not capture all chemical rearrangements or losses, especially for unusual functional groups.
- High spectral similarity can occur by chance between structurally unrelated metabolites; peak-matching scores alone cannot definitively confirm identity without complementary data (e.g., retention time, orthogonal spectroscopy).
- Mass tolerance choice (ppm vs. Daltons) affects sensitivity and specificity; too lenient a threshold inflates false positives, too strict a threshold causes misses.

## Evidence

- [other] Generate in silico metabolite structures and match them against MS/MS data: "The job subproject implements metabolite annotation by generating in silico metabolites and matching them against MS/MS data, as part of MAGMa (Ms Annotation based on in silico Generated Metabolites)."
- [other] Calculate theoretical fragment ions and score by comparing peaks: "Calculate theoretical fragment ions for each candidate metabolite via fragmentation rules. 5. Score each candidate by comparing experimental MS/MS peaks against theoretical fragments using cosine"
- [other] Rank metabolite candidates by annotation score: "Rank metabolite candidates by annotation score and output ranked list with match statistics."
- [other] File format support for MS/MS input data: "Load MS/MS spectral data from input file (mzML, mzXML, or equivalent format)."
- [readme] Project mission: chemo-informatics methods for metabolite identification: "The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow."
