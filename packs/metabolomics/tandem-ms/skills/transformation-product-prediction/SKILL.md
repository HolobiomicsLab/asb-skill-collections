---
name: transformation-product-prediction
description: Use when after parent chemical suspects have been identified in a non-target screening workflow, use this skill when you need to screen for downstream products formed by chemical or biological transformation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3375
  tools:
  - patRoon
  - BioTransformer
  - CTS
  - PubChem
  - PubChemLite
  - MetFrag
  techniques:
  - ion-mobility-MS
  - tandem-MS
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

# transformation-product-prediction

## Summary

Predict transformation products (TPs) for parent chemicals by dispatching to multiple algorithms (library-based, in-silico structure prediction, or metabolic logic rules) and optionally extending predictions to multi-generation TPs. This skill enables screening for chemical degradation and metabolic products in environmental mass spectrometry data.

## When to use

After parent chemical suspects have been identified in a non-target screening workflow, use this skill when you need to screen for downstream products formed by chemical or biological transformation. Applies to both environmental fate studies (degradation products) and metabolic studies (phase I/II metabolites). Trigger on having: (1) a parent compound list (as SMILES, formulas, or annotation candidates), (2) a choice of TP source (library, in-silico prediction, or metabolic rules), and (3) a requirement to link parent features to product features in MS data.

## When NOT to use

- Input parents lack chemical structure or formula information and annotation data is unavailable — structure or formula is required for all TP prediction algorithms.
- Study aims only to identify parent compounds without investigating their environmental or metabolic fate — TP screening is specifically for downstream product detection.
- Raw MS data has not yet been processed into features and feature groups — parent screening must first identify candidate parent features in the dataset.

## Inputs

- parent compound list (data.frame with chemical identifiers)
- SMILES strings (for structure-based algorithms)
- molecular formulas (for formula-based algorithms)
- feature groups from suspect screening
- annotation candidates from compound identification
- log P values (optional, for some algorithms)

## Outputs

- TP object (containing parent names, SMILES, formulas, and TP data)
- suspect list (convertible from TP object via convertToSuspects)
- ranked TP candidates with TP Score
- multi-generation transformation pathways (when generations > 1)

## How to apply

Accept parent input from a suspect list (data.frame), matched feature groups, or annotation candidates. Validate and route to the appropriate algorithm backend: structure-based algorithms (BioTransformer, CTS, PubChem library, annotation candidates) retrieve or predict TPs with SMILES and optional log P values; formula-based algorithms (library_formula, metabolic logic rules, annotation formulas) calculate TPs from elemental transformations. Use the generations parameter to extend predictions to TPs-of-TPs for multi-step pathways where applicable. For annotation-based candidates (ann_comp, ann_form), rank outputs by TP Score, which incorporates structural similarity and suspect matching. Return a TP object containing parent names, SMILES/formulas, and corresponding TP data, formatted for downstream suspect screening and componentization. Filter results using minSimilarity, minTPScore, removeDuplicates, or removeParentIsomers thresholds to prioritize high-confidence predictions.

## Related tools

- **BioTransformer** (Structure-based in-silico TP prediction engine for biotransformation and metabolic pathways)
- **CTS** (Chemical Transformation Simulator for structure-based TP prediction)
- **PubChemLite** (Library of experimentally observed transformation products indexed by parent structure)
- **MetFrag** (Generates MS/MS fragmentation database for TPs to enable spectral matching in TP screening)
- **patRoon** (Framework implementing generateTPs function and unified interface to all TP algorithms) — https://github.com/rickhelmus/patRoon

## Examples

```
TPsBT <- generateTPs(algorithm = "biotransformer", parents = patRoonData::suspectsPos, type = "env")
```

## Evaluation signals

- Verify TP object is not empty and contains expected parent-TP relationships (check row counts and parent-TP pairing consistency).
- Confirm TP structures or formulas are chemically feasible transformations of parents (e.g., mass differences match expected biotransformations, functional groups are plausible modifications).
- Check that algorithm routing succeeded by inspecting TP source metadata (verify 'biotransformer', 'cts', 'library', or 'logic' label is correctly assigned per parent).
- When using multi-generation predictions (generations > 1), validate TP-of-TP chains do not exceed chemical plausibility (e.g., reasonable mass shifts, molecular weight increases/decreases follow biotransformation logic).
- After filtering (e.g., minTPScore ≥ 0.5, removeDuplicates = TRUE), confirm expected candidate reduction without loss of known reference TPs (if available in validation data).

## Limitations

- Structure-based algorithms (BioTransformer, CTS) depend on SMILES accuracy and valid chemical structure input; incorrect or ambiguous structures will produce unreliable predictions.
- Library-based predictions (PubChemLite, custom libraries) are limited to experimentally observed or curated TPs; novel or pathway-specific transformations may not be captured.
- In-silico predictions assume standard environmental or metabolic conditions and may not account for pH, co-metabolite availability, or organism-specific enzyme kinetics.
- Multi-generation predictions (generations > 1) increase computational time and may accumulate prediction uncertainty over successive transformation steps.
- TP screening matching relies on MS similarity and retention time; isomeric TPs or isobaric co-eluting compounds may not be resolvable without additional orthogonal separation (e.g., ion mobility).

## Evidence

- [other] The generateTPs function is used to obtain TPs for a particular set of parents, with data obtained from either a library or predicted in-silico.: "The `generateTPs` function is used to obtain TPs for a particular set of parents, with data obtained from either a library or predicted _in-silico_."
- [other] For structure-based algorithms, retrieve or predict TPs with SMILES; for formula-based algorithms, calculate TPs from elemental transformations.: "For structure-based algorithms (biotransformer, cts, library, ann_comp), retrieve or predict TPs with SMILES and optional log P values; for formula-based algorithms (library_formula, ann_form,"
- [other] Apply the generations parameter to extend predictions to multi-step transformations (TPs of TPs) where applicable.: "Apply the generations parameter to extend predictions to multi-step transformations (TPs of TPs) where applicable."
- [other] For annotation-based candidates, rank outputs by TP Score incorporating structural similarity and suspect matching.: "For ann_comp and ann_form, rank candidates by TP Score incorporating structural similarity and suspect matching."
- [other] Return a TP object containing parent names, SMILES/formulas, and corresponding TP data, formatted for downstream suspect screening and componentization.: "Return a TP object containing parent names, SMILES/formulas, and corresponding TP data, formatted for downstream suspect screening and componentization."
- [readme] patRoon combines established software tools with novel functionality to provide comprehensive NTA workflows including transformation product screening.: "`patRoon` combines established software tools with novel functionality in order to provide comprehensive NTA workflows. The different algorithms are provided through a consistent interface, which"
- [other] Screening for TPs, i.e. chemicals that are formed from a parent chemical by chemical or biological processes, has broad applications.: "Screening for TPs, i.e. chemicals that are formed from a _parent_ chemical by e.g. chemical or biological processes, has broad applications."
