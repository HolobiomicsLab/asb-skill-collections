---
name: annotation-candidate-ranking-tp-score
description: Use when after generating TP candidates from annotation algorithms (ann_comp for structure-based, ann_form for formula-based), when you need to filter and rank candidates to focus on the most credible identifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - patRoon
  - BioTransformer
  - CTS
  - PubChem
  - MetFrag
derived_from:
- doi: 10.1186/s13321-020-00477-w
  title: patRoon
evidence_spans:
- The `generateTPs` function is used to obtain TPs for a particular set of parents.
- componTP <- generateComponents(algorithm = "tp",
- '`generateTPs(algorithm = "biotransformer", ...)` | Parents | TPs structural information'
- '`generateTPs(algorithm = "cts", ...)` | Parents | TPs with structural information'
- Library ([PubChem][PubChemLiteTR] or custom)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_patroon_cq
    doi: 10.1186/s13321-020-00477-w
    title: patRoon
  dedup_kept_from: coll_patroon_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00477-w
  all_source_dois:
  - 10.1186/s13321-020-00477-w
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# annotation-candidate-ranking-tp-score

## Summary

Rank transformation product (TP) annotation candidates by TP Score, a composite metric incorporating structural similarity and suspect matching. This skill prioritizes the most likely TP identifications from annotation-derived candidates (ann_comp and ann_form algorithms) to improve downstream screening and reporting confidence.

## When to use

After generating TP candidates from annotation algorithms (ann_comp for structure-based, ann_form for formula-based), when you need to filter and rank candidates to focus on the most credible identifications. Use this skill particularly when combining positive/negative ionization data or when suspect TP lists are large and manual curation is impractical.

## When NOT to use

- Input TP object was generated from library, BioTransformer, CTS, or logic algorithms — these do not compute TP Score and are not amenable to this ranking approach.
- TP candidates are already manually curated or known to be high-confidence (e.g., literature-confirmed transformations) — additional automated ranking may not add value.
- Early exploratory analysis where you want to retain all candidates for inspection before filtering — use lower or no minTPScore threshold instead.

## Inputs

- TP object generated from ann_comp algorithm (structure-based annotation candidates)
- TP object generated from ann_form algorithm (formula-based annotation candidates)
- minTPScore parameter (numeric, 0–1, default typically 0.5)
- topMost parameter (integer, maximum number of candidates to retain per parent)

## Outputs

- filtered TP object with ranked candidates (sorted by TP Score descending)
- candidate reduction report (number of candidates before/after filtering)

## How to apply

Apply the filter() function to the TP object with minTPScore and topMost parameters to rank and retain only the highest-confidence candidates. The TP Score integrates structural similarity (e.g., via Tanimoto or spectral cosine similarity between parent and TP) and suspect matching strength (e.g., mass accuracy, chromatographic alignment). Set minTPScore (typically 0.5) to enforce a confidence threshold and topMost (e.g., 25) to limit output size for downstream processing. The ranking is performed automatically during TP object construction for ann_comp and ann_form, but filtering applies these thresholds post-hoc. Lower scores indicate weaker structural or spectral evidence; candidates falling below the threshold are discarded to reduce false positive TP assignments.

## Related tools

- **patRoon** (Filter and rank TP candidates by TP Score using filter() method on TP objects; orchestrates the full TP screening workflow including candidate ranking.) — https://github.com/rickhelmus/patRoon
- **MetFrag** (Optionally used to refine structural similarity scoring for TP candidates via convertToMFDB and spectral library matching.)

## Examples

```
TPsAnnCompF <- filter(TPsAnnComp, minTPScore = 0.5, topMost = 25)
```

## Evaluation signals

- TP Score values are numeric, range 0–1, and sorted in descending order in the output TP object.
- Number of candidates per parent does not exceed the topMost threshold (e.g., ≤25 if topMost=25).
- All remaining candidates have TP Score ≥ minTPScore threshold (e.g., ≥0.5 if minTPScore=0.5).
- Top-ranked candidates (highest TP Score) align with known/suspected transformations when cross-referenced against literature or database (MetFrag, SIRIUS, external TP libraries).
- Filtering reduces total candidate count by ≥30–70%, indicating meaningful prioritization without complete elimination of candidates.

## Limitations

- TP Score computation is available only for ann_comp and ann_form algorithms; library and in-silico prediction algorithms (biotransformer, cts) do not support this ranking method.
- TP Score quality depends on the parent–TP structural similarity metric and suspect list composition; poor suspect data or weak spectral evidence can inflate low-confidence scores.
- Threshold parameters (minTPScore, topMost) are user-defined and data-dependent; no automated, universal default ensures optimal performance across all environmental samples and compound classes.
- Ranking does not account for biological plausibility or metabolic pathway context; high-scoring candidates may still be chemically unlikely under true environmental conditions.

## Evidence

- [other] For ann_comp and ann_form, rank candidates by TP Score incorporating structural similarity and suspect matching.: "For ann_comp and ann_form, rank candidates by TP Score incorporating structural similarity and suspect matching."
- [other] TPsAnnCompF <- filter(TPsAnnComp, minTPScore = 0.5, topMost = 25): "TPsAnnCompF <- filter(TPsAnnComp, minTPScore = 0.5, topMost = 25)"
- [other] Screening for TPs, i.e. chemicals that are formed from a parent chemical by e.g. chemical or biological processes, has broad applications.: "Screening for TPs, i.e. chemicals that are formed from a parent chemical by e.g. chemical or biological processes, has broad applications."
- [readme] patRoon combines established software tools with novel functionality in order to provide comprehensive NTA workflows.: "patRoon combines established software tools with novel functionality in order to provide comprehensive NTA workflows."
