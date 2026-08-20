---
name: transformation-product-parent-linkage
description: Use when after suspect screening has identified both parent features
  (from before-treatment or reference samples) and TP candidate features (from after-treatment
  or exposed samples) in the same analysis set, and you have MS/MS spectral data or
  formula annotations available.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - patRoon
  - screenSuspects
  - convertToSuspects
  - MetFrag
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

# Transformation Product–Parent Linkage

## Summary

Link detected transformation product (TP) features to their parent compounds by calculating spectrum similarity and fragment/neutral loss matches between parent and TP candidates. This componentization step ranks and filters parent–TP pairs based on retention time tolerance, spectral similarity thresholds, and shared fragmentation patterns to produce a validated parent–TP component object.

## When to use

After suspect screening has identified both parent features (from before-treatment or reference samples) and TP candidate features (from after-treatment or exposed samples) in the same analysis set, and you have MS/MS spectral data or formula annotations available. Use this skill when the analysis goal is to establish transformation pathways and validate that detected TP candidates are chemically related to their suspected parents through shared fragment ions, neutral losses, or spectral similarity.

## When NOT to use

- Parent and TP features have not been separately screened or identified; generateComponents requires distinct fGroups and fGroupsTPs inputs.
- No MS/MS spectral data or formula information is available; spectrum similarity and fragment matching calculations cannot proceed without these annotations.
- The analysis goal is to predict new TP structures rather than validate existing detected TPs against known or predicted candidates.

## Inputs

- fGroups (feature group object with parent features, optionally filtered by sample metadata)
- fGroupsTPs (feature group object with TP candidate features)
- TPs object (transformation products with structural or library information)
- MSPeakLists (optional; MS/MS peak lists for spectrum similarity calculation)
- formulas (optional; calculated formula candidates to enable fragment/neutral loss matching)
- compounds (optional; compound annotations)

## Outputs

- componentsTPs object (links parent features to ranked TP candidates with similarity scores and match counts)

## How to apply

Prepare two feature group objects: fGroups containing parent features (optionally filtered by sample metadata using ignoreParents flag) and fGroupsTPs containing TP candidate features. Call generateComponents with algorithm='tp', passing fGroups, fGroupsTPs, and the TPs object, optionally including annotation data (MSPeakLists, formulas, compounds) to enable spectrum similarity and fragment matching calculations. Set minRTDiff parameter (in seconds) to define retention time tolerance for valid parent–TP pairs. Apply post-componentization filters in priority order: retDirMatch to enforce expected retention time direction, minSpecSim or minSpecSimBoth to set spectrum similarity thresholds (e.g., cosine similarity ≥0.7), and minFragMatches or minNLMatches to enforce minimum shared fragment or neutral loss counts. Validate the resulting componentsTPs object by confirming parent–TP assignments exist, verifying candidate rankings reflect similarity metrics, and inspecting the component structure.

## Related tools

- **patRoon** (Implements generateComponents function with algorithm='tp' for parent–TP linkage and post-componentization filtering) — https://github.com/rickhelmus/patRoon
- **screenSuspects** (Prerequisite function to identify and filter parent and TP features from feature groups before componentization) — https://github.com/rickhelmus/patRoon
- **convertToSuspects** (Converts TP object to suspect list format for screening; enables mapping of feature groups to parent and TP identities) — https://github.com/rickhelmus/patRoon
- **MetFrag** (Optional upstream tool; generates fragment annotations to support minFragMatches filtering during componentization)

## Examples

```
componTP <- generateComponents(algorithm = "tp", fGroups = fGroups[ni = treatment == "before"], fGroupsTPs = fGroups[ni = treatment == "after"], TPs = TPs, MSPeakLists = msPeakLists, formulas = formulas); componTP <- filter(componTP, retDirMatch = TRUE, minSpecSim = 0.7, minFragMatches = 2)
```

## Evaluation signals

- componentsTPs object is non-empty and contains parent–TP assignments with numeric similarity scores and match counts ranked in descending order.
- All parent features in componentsTPs have at least one TP candidate; verify no parents are orphaned unless filtering explicitly removed all candidates.
- Retention time differences between parent–TP pairs fall within the specified minRTDiff tolerance (in seconds); retDirMatch filtering ensures direction matches expected biotransformation behavior.
- Spectrum similarity (cosine or other metric) for top-ranked candidates meets or exceeds minSpecSim or minSpecSimBoth thresholds; fragment or neutral loss match counts meet minFragMatches or minNLMatches thresholds.
- Visual inspection of componentsTPs structure shows candidate ranking reflects expected chemical relationships (e.g., mass differences consistent with common transformations like oxidation, hydration, or conjugation).

## Limitations

- Performance depends critically on quality and completeness of MS/MS spectral data and formula annotations; missing or low-confidence annotations reduce matching sensitivity.
- Retention time tolerance (minRTDiff) must be tuned to the specific chromatographic system and biotransformation context; overly tight tolerances may miss valid TPs with unexpected retention shifts.
- Spectrum similarity and fragment matching are probabilistic; coincidental spectral similarity between unrelated compounds may produce false-positive parent–TP links, especially at low minSpecSim thresholds.
- The skill assumes parent and TP features are separable by sample metadata (e.g., before/after treatment); co-occurrence of parents and TPs in the same samples may confound linkage.
- TP prediction algorithms (BioTransformer, CTS, PubChem libraries) may have incomplete or biased coverage of actual transformation pathways, leading to missed or incorrectly predicted TPs.

## Evidence

- [other] The generateComponents function with algorithm='tp' builds TP components by creating one component per parent, taking as inputs a feature group object (fGroups) from before transformation and a feature group object containing TPs (fGroupsTPs) from after transformation, producing a componentsTPs object linking parents to their detected transformation products.: "The generateComponents function with algorithm='tp' builds TP components by creating one component per parent, taking as inputs a feature group object (fGroups) from before transformation and a"
- [other] Call generateComponents with algorithm='tp', passing fGroups, fGroupsTPs, TPs object, and optional annotation data (MSPeakLists, formulas, compounds) to calculate spectrum similarity and fragment/neutral loss matches between parents and TP candidates.: "Call generateComponents with algorithm='tp', passing fGroups, fGroupsTPs, TPs object, and optional annotation data (MSPeakLists, formulas, compounds) to calculate spectrum similarity and"
- [other] Set minRTDiff parameter (in seconds) to establish retention time tolerance for parent-TP pairing. Apply post-componentization filters such as retDirMatch (expected retention direction), minSpecSim or minSpecSimBoth (spectrum similarity threshold), and minFragMatches or minNLMatches (shared fragment/neutral loss counts) to prioritize candidates.: "Set minRTDiff parameter (in seconds) to establish retention time tolerance for parent-TP pairing. Apply post-componentization filters such as retDirMatch, minSpecSim or minSpecSimBoth, and"
- [other] Validate componentization output: inspect the componentsTPs object structure, verify parent-TP assignments exist, and confirm candidate rankings reflect similarity metrics.: "Validate componentization output: inspect the componentsTPs object structure, verify parent-TP assignments exist, and confirm candidate rankings reflect similarity metrics"
- [other] In the step the parent features are linked with the TP features. Several post-processing functionality exists to improve and prioritize the data.: "In the step the parent features are linked with the TP features. Several post-processing functionality exists to improve and prioritize the data"
- [other] Screening for TPs, i.e. chemicals that are formed from a parent chemical by e.g. chemical or biological processes, has broad applications.: "Screening for TPs, i.e. chemicals that are formed from a parent chemical by e.g. chemical or biological processes, has broad applications"
