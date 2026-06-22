---
name: retention-time-direction-matching
description: Use when after componentization of parent and TP features with generateComponents(algorithm='tp'), when structural formula or compound annotations are available and you wish to prioritize TP candidates whose retention time behavior aligns with expected electronegativity, polarity, or hydrophobicity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - patRoon
  - BioTransformer
  - CTS
  - PubChem
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-direction-matching

## Summary

Filters parent–transformation product (TP) pairs by validating that the observed retention time shift between parent and candidate TP matches the expected chromatographic direction predicted from structural changes. This post-componentization filter improves TP assignment confidence by eliminating candidates whose retention behavior contradicts predicted metabolic transformations.

## When to use

After componentization of parent and TP features with generateComponents(algorithm='tp'), when structural formula or compound annotations are available and you wish to prioritize TP candidates whose retention time behavior aligns with expected electronegativity, polarity, or hydrophobicity changes caused by the transformation. Use this filter when the reference database or annotation pipeline includes formula or structural information to predict whether a transformation should increase or decrease retention time.

## When NOT to use

- Retention time data is unavailable or poorly calibrated across analyses
- Formulas or compound annotations are missing or unreliable, preventing prediction of expected RT direction
- The chromatographic system shows inconsistent or nonlinear retention behavior (e.g., severely peak-tailed features or poor reproducibility)

## Inputs

- componentsTPs object (output from generateComponents with algorithm='tp')
- formulas object (calculated formula candidates for features)
- optionally: compounds object or annotation data with structural information

## Outputs

- filtered componentsTPs object with candidates ranked or removed based on retention time direction match

## How to apply

Apply the retDirMatch filter during post-componentization refinement by passing the componentsTPs object, the formulas object (or annotation data), and setting retDirMatch=TRUE to generateComponents or the filter() method. The filter compares the observed retention time direction (parent RT vs. candidate TP RT) against the predicted direction inferred from structural changes in the annotations. Transformations that add electron-withdrawing groups or decrease molecular polarity typically shift retention time later (or vice versa for opposite changes). Candidates whose retention time shift contradicts the predicted direction are deprioritized or removed, reducing false positive TP assignments. The effectiveness of this filter depends on annotation accuracy and the chromatographic system's consistent relationship between molecular properties and retention.

## Related tools

- **patRoon** (Provides generateComponents and filter functions to apply retDirMatch post-componentization; implements RT direction prediction logic based on formula transformations) — https://github.com/rickhelmus/patRoon

## Examples

```
componTP <- filter(componTP, retDirMatch = TRUE, formulas = formulas)
```

## Evaluation signals

- componentsTPs object contains candidates with retDirMatch scores or ranks reflecting agreement between observed and predicted RT direction
- Number of retained candidates is reduced compared to unfiltered componentsTPs, indicating plausible filtering without over-pruning
- Manual inspection of a subset of retained parent–TP pairs confirms that RT shifts correlate with expected structural changes (e.g., hydroxylation increasing polarity and decreasing RT, methylation decreasing polarity and increasing RT)
- No candidates are retained with contradictory RT directions (e.g., candidate RT < parent RT when formula predicts increased polarity and earlier elution)
- Comparison of filter results with and without formulas shows that annotation quality directly impacts filter utility

## Limitations

- Requires accurate formula or compound annotations; poor annotations lead to incorrect RT direction predictions and unreliable filtering
- Assumes linear or monotonic relationship between molecular property changes and chromatographic retention, which may fail for complex matrices or poor column conditioning
- Cannot distinguish between structural isomers that have identical formulas but different RT behavior
- Relative RT shift magnitude (e.g., 5 seconds vs. 60 seconds) is not directly comparable across different analyses or chromatographic methods without calibration
- May inadvertently filter out genuine TPs if the chromatographic system is unstable or if the parent and TP co-elute or overlap in RT space

## Evidence

- [other] Apply post-componentization filters such as retDirMatch (expected retention direction), minSpecSim or minSpecSimBoth (spectrum similarity threshold), and minFragMatches or minNLMatches (shared fragment/neutral loss counts) to prioritize candidates.: "Apply post-componentization filters such as retDirMatch (expected retention direction), minSpecSim or minSpecSimBoth (spectrum similarity threshold), and minFragMatches or minNLMatches"
- [other] Filter | retDirMatch | Expected retention direction match based on structural transformations and formula changes.: "Filter | retDirMatch | Expected retention direction match based on structural transformations and formula changes"
- [other] componTP <- filter(componTP, retDirMatch = TRUE, formulas = formulas): "componTP <- filter(componTP, retDirMatch = TRUE, formulas = formulas)"
