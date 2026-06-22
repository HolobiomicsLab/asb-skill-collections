---
name: multi-generation-transformation-hierarchies
description: Use when the analytical goal requires detection of downstream transformation products that are not direct metabolites of the parent but rather products of further metabolism or degradation (e.g., secondary metabolites, conjugates of phase I products).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_2275
  tools:
  - patRoon
  - BioTransformer
  - CTS
  - PubChem
  - CTS (Chemical Transformation Simulator)
  - PubChem/PubChemLite library
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
---

# Multi-generation transformation hierarchies

## Summary

Extend transformation product (TP) predictions beyond single-step metabolic transformations by recursively applying TP generation algorithms to predict secondary and tertiary metabolites (TPs of TPs). This skill is essential for comprehensive environmental screening when parent chemicals undergo sequential biotransformation or chemical degradation pathways.

## When to use

Apply this skill when the analytical goal requires detection of downstream transformation products that are not direct metabolites of the parent but rather products of further metabolism or degradation (e.g., secondary metabolites, conjugates of phase I products). Triggers include: (1) suspected presence of multi-step degradation chains in environmental or biological samples, (2) need to populate suspect lists for chemicals expected to accumulate only after sequential transformations, or (3) designing screening workflows where parent compounds are known environmental contaminants with known multi-step metabolic pathways.

## When NOT to use

- Input is a single chemical with no known biotransformation pathway or degradation mechanism — single-generation TP prediction is sufficient and more cost-effective.
- Analysis aims only to confirm parent compound presence; multi-generation predictions add false-positive burden without improving specificity for parent-only screening.
- Computational budget is severely constrained; multi-generation predictions, especially with structure-based algorithms (BioTransformer, CTS), scale combinatorially and may exceed practical runtime limits for large parent sets.

## Inputs

- parent compounds (data.frame with SMILES or formulas)
- matched feature groups from suspect screening
- annotation candidates (compounds or formula objects)
- algorithm selection (biotransformer, cts, library, library_formula, logic, ann_comp, ann_form)
- generations parameter (integer ≥ 1)

## Outputs

- hierarchical TP object containing parent → TP1 → TP2 → TPN chains
- multi-level suspect list for downstream MS screening
- ranked TP candidates with TP Score incorporating structural similarity and suspect matching

## How to apply

Use the `generations` parameter in the `generateTPs()` function to recursively generate TP hierarchies: set `generations = 1` for direct TPs (default), `generations = 2` for TPs of TPs, or higher integers for deeper hierarchies. For each generation, the function accepts the output TP set as parent input and dispatches to the same algorithm backend (BioTransformer, CTS, library, or logic rules). Because computational cost and prediction uncertainty both increase with generation depth, combine multi-generation prediction with filtering steps (`removeDuplicates = TRUE`, `minSimilarity` thresholds, `topMost` ranking by TP Score) to retain only chemically plausible candidates. Structural similarity and formula-based metrics become increasingly important for ranking candidates as isomer degeneracy grows with each generation.

## Related tools

- **BioTransformer** (Predicts biotransformation pathways via metabolic logic; supports recursive generation of multi-step metabolite hierarchies)
- **CTS (Chemical Transformation Simulator)** (In-silico prediction of chemical degradation transformations; can be dispatched iteratively for multi-generation predictions)
- **PubChem/PubChemLite library** (Provides library-based TP candidates; supports structure-to-structure multi-generation lookups)
- **patRoon** (Implements generateTPs() function with generations parameter and algorithm dispatch logic) — https://github.com/rickhelmus/patRoon

## Examples

```
TPsGen2 <- generateTPs(algorithm = "biotransformer", parents = TPs, generations = 2, type = "env")
```

## Evaluation signals

- Verify output TP objects contain explicit parent-child linkages traceable through multiple generations (inspect TP names, SMILES chains, and metadata fields).
- Check that the number of candidates increases from generation N to N+1, but that duplicate and near-duplicate isomers are correctly deduplicated (compare cardinality before/after `removeDuplicates = TRUE`).
- Confirm that TP Scores remain meaningful and interpretable across generations: structural similarity should decay monotonically with increasing generation depth, and suspect matches (if available) should occur primarily at lower generations.
- Validate that filter parameters (minSimilarity, minTPScore, topMost) are consistently applied across all generations and that candidate lists remain chemically plausible (spot-check structural transformations manually for presence of known biotransformation rules).
- Ensure that generation depth does not exceed documented or expected metabolic pathway lengths for the parent chemical class; excessively deep hierarchies are a warning sign of prediction drift or algorithmic artifacts.

## Limitations

- Prediction uncertainty increases with each generation; later-generation TPs may have low biological or chemical plausibility and should be treated as lower-confidence candidates.
- Computational cost scales combinatorially with generation depth, especially for structure-based algorithms (BioTransformer, CTS); practical limits are typically 2–3 generations for large parent sets.
- Multi-generation library lookups may miss novel or rare TPs if the underlying library is incomplete; formula-based and logic-based algorithms are more stable across generations but are less specific for structural isomers.
- No single TP Score metric captures both structural and mechanistic realism across multiple generations; ranking prioritization may require domain-specific tuning or expert validation.

## Evidence

- [other] Apply the generations parameter to extend predictions to multi-step transformations (TPs of TPs) where applicable.: "Apply the generations parameter to extend predictions to multi-step transformations (TPs of TPs) where applicable."
- [other] Screening for TPs, i.e. chemicals that are formed from a parent chemical by e.g. chemical or biological processes, has broad applications.: "Screening for TPs, i.e. chemicals that are formed from a _parent_ chemical by e.g. chemical or biological processes, has broad applications."
- [other] The generateTPs function is used to obtain TPs for a particular set of parents, with data obtained from either a library or predicted in-silico.: "The `generateTPs` function is used to obtain TPs for a particular set of parents, with data obtained from either a library or predicted _in-silico_."
- [other] For ann_comp and ann_form, rank candidates by TP Score incorporating structural similarity and suspect matching.: "For ann_comp and ann_form, rank candidates by TP Score incorporating structural similarity and suspect matching."
