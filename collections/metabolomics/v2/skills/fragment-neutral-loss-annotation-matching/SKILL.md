---
name: fragment-neutral-loss-annotation-matching
description: Use when after generateComponents with algorithm='tp' has tentatively
  paired parent features with TP candidates based on retention time and spectrum similarity,
  and when formula annotations are available for both parents and candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - patRoon
  - SIRIUS
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s13321-020-00477-w
  title: patRoon
evidence_spans:
- The `generateTPs` function is used to obtain TPs for a particular set of parents.
- componTP <- generateComponents(algorithm = "tp",
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

# Fragment-Neutral Loss Annotation Matching

## Summary

Match shared fragments and neutral losses between parent and transformation product (TP) candidates using formula annotations to prioritize and validate parent-TP associations. This skill ranks TP candidates by counting concordant fragment and neutral loss patterns, filtering candidates below a specified match threshold.

## When to use

After generateComponents with algorithm='tp' has tentatively paired parent features with TP candidates based on retention time and spectrum similarity, and when formula annotations are available for both parents and candidates. Use this skill to filter and rank candidates by structural plausibility—i.e., TPs should share metabolic fragmentation patterns with their parents.

## When NOT to use

- When formula annotations are unavailable or unreliable; fragment-loss matching requires accurate molecular masses.
- When MS/MS spectra lack sufficient fragmentation or quality; matching requires informative peak lists.
- When comparing TPs from non-biotransformation pathways (e.g., purely chemical synthesis) where fragmentation patterns may not reflect parent-TP metabolic relationships.

## Inputs

- componentsTPs object (parent-TP candidate pairings with tentative spectrum similarity scores)
- formulas object (molecular formula annotations for parents and TP candidates)
- MSPeakLists (optional; feature MS/MS spectra for fragment and neutral loss extraction)

## Outputs

- filtered componentsTPs object (ranked candidates meeting minFragMatches or minNLMatches threshold)
- ranked parent-TP associations prioritized by number of shared fragments and neutral losses

## How to apply

Pass the componentsTPs object, formula annotations (formulas object), and optional MSPeakLists to generateComponents or apply post-hoc filtering with minFragMatches or minNLMatches parameters. The function calculates neutral loss and fragment matches by comparing the mass differences between parent and candidate spectra against expected formula-based mass losses. Retain only candidates meeting the minFragMatches (minimum number of shared fragments) or minNLMatches (minimum number of shared neutral losses) threshold. This filtering prioritizes chemically plausible TPs while reducing false positives from spectral noise or unrelated features.

## Related tools

- **patRoon** (Implements generateComponents with algorithm='tp' and minFragMatches/minNLMatches filters for fragment-neutral loss matching during TP componentization) — https://github.com/rickhelmus/patRoon
- **SIRIUS** (Provides formula annotations needed as input for calculating fragment and neutral loss matches)

## Examples

```
componTP <- generateComponents(algorithm = "tp", fGroups = fGroups, fGroupsTPs = fGroupsTPs, TPs = TPs, formulas = formulas, MSPeakLists = msplist); componTPfilt <- filter(componTP, minFragMatches = 3, minNLMatches = 2)
```

## Evaluation signals

- Verify that filtered componentsTPs contains only parent-TP pairs meeting the specified minFragMatches or minNLMatches threshold (inspect component structure and candidate count).
- Confirm that candidate ranking within each component reflects increasing fragmentation concordance: higher-ranked candidates should exhibit more shared fragments/neutral losses than lower-ranked candidates.
- Cross-check a sample of retained candidates against MS/MS spectra: visually confirm that shared neutral loss masses are present in both parent and TP spectra and align with expected formula-based losses.
- Validate that the number of candidates retained is reduced relative to pre-filtered componentsTPs, indicating effective prioritization; absence of filtering suggests incorrect parameter configuration.
- Inspect edge cases: verify that candidates with zero or below-threshold fragment matches are excluded, and that parent-TP pairs with chemically implausible mass differences are deprioritized.

## Limitations

- Fragment and neutral loss matching accuracy depends on formula annotation quality; errors or missing annotations will propagate to candidate rankings.
- Threshold parameters (minFragMatches, minNLMatches) must be tuned per dataset and MS/MS acquisition method; overly stringent thresholds may exclude valid TPs, while lenient thresholds retain noise.
- Fragmentation patterns vary significantly with ionization mode, collision energy, and instrument type; a parent-TP pair plausible at high collision energy may show poor match at low energy.
- TPs arising from non-metabolic transformations (e.g., photodegradation, hydrolysis) may not follow typical biotransformation fragmentation rules and could be incorrectly deprioritized.

## Evidence

- [other] Call generateComponents with algorithm='tp', passing fGroups, fGroupsTPs, TPs object, and optional annotation data (MSPeakLists, formulas, compounds) to calculate spectrum similarity and fragment/neutral loss matches between parents and TP candidates.: "Call generateComponents with algorithm='tp', passing fGroups, fGroupsTPs, TPs object, and optional annotation data (MSPeakLists, formulas, compounds) to calculate spectrum similarity and"
- [other] Apply post-componentization filters such as retDirMatch (expected retention direction), minSpecSim or minSpecSimBoth (spectrum similarity threshold), and minFragMatches or minNLMatches (shared fragment/neutral loss counts) to prioritize candidates.: "Apply post-componentization filters such as retDirMatch (expected retention direction), minSpecSim or minSpecSimBoth (spectrum similarity threshold), and minFragMatches or minNLMatches (shared"
- [other] Filter | minFragMatches, minNLMatches | Minimum number of formula fragment/neutral loss matches: "Filter | minFragMatches, minNLMatches | Minimum number of formula fragment/neutral loss matches"
- [other] Automatic screening of TPs using library/in-silico data, MS similarities and classifications.: "Automatic screening of TPs using library/in-silico data, MS similarities and classifications."
