---
name: smiles-formula-representation-chemistry
description: 'Use when when obtaining transformation products through mixed algorithmic
  backends (library, CTS, BioTransformer, metabolic logic rules) that require different
  chemical representations: structure-based algorithms need SMILES strings with optional
  log P values, while formula-based algorithms need.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3370
  tools:
  - patRoon
  - BioTransformer
  - CTS
  - PubChem
  - MetFrag
  license_tier: open
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

# SMILES-formula representation chemistry

## Summary

Convert between SMILES strings and molecular formulas to represent chemical structures in transformation product prediction and suspect screening workflows. This dual-representation approach enables both structure-based algorithms (requiring SMILES) and formula-based algorithms (requiring elemental composition) to operate on the same parent and TP datasets.

## When to use

When obtaining transformation products through mixed algorithmic backends (library, CTS, BioTransformer, metabolic logic rules) that require different chemical representations: structure-based algorithms need SMILES strings with optional log P values, while formula-based algorithms need elemental transformations or annotation candidates. Apply this skill when your parent input is a suspect list, matched feature groups, or compounds object that must be routed to heterogeneous prediction backends within a single generateTPs workflow.

## When NOT to use

- Input data already contains only pre-computed TP libraries without requiring algorithm dispatch or conversion between SMILES and formula representations.
- Analysis workflow does not include transformation product screening or only uses single algorithm backend (e.g., only PubChem library, no mixed algorithmic sources).
- Parent compounds lack both structural information (SMILES) and elemental composition data needed to route to appropriate algorithm backends.

## Inputs

- suspect list (data.frame with SMILES or formula columns)
- matched feature groups from suspect screening (with chemical identifiers)
- compounds object from annotation (with structural or formula information)
- parents parameter input to generateTPs function

## Outputs

- TP object containing parent names, SMILES strings (for structure-based results), molecular formulas (for formula-based results), and corresponding TP data
- ranked TP candidates with TP Score values (for annotation-based methods)
- multi-generation TP data (TPs of TPs) when generations parameter > 1

## How to apply

Accept parent input from suspect lists, matched feature groups from suspect screening, or annotation candidate compounds objects. For structure-based prediction algorithms (BioTransformer, CTS, PubChem library, ann_comp), ensure parents are represented as SMILES strings with optional log P values; retrieve or predict TPs with structural information. For formula-based algorithms (formula library, ann_form, logic rules), represent parents as molecular formulas and calculate TPs from elemental transformations or ranking annotation candidates by TP Score (incorporating structural similarity and suspect matching). Apply the generations parameter to extend predictions to multi-step transformations (TPs of TPs) where applicable. Return a TP object containing parent names with both SMILES and formula data as appropriate for the downstream suspect screening and componentization steps.

## Related tools

- **patRoon** (R package providing generateTPs function that dispatches parent chemical representations to heterogeneous TP prediction backends and manages dual SMILES/formula representations) — https://github.com/rickhelmus/patRoon
- **BioTransformer** (Structure-based TP prediction algorithm requiring SMILES input; invoked via generateTPs(algorithm = 'biotransformer', ...))
- **CTS** (Structure-based TP prediction algorithm requiring SMILES input; invoked via generateTPs(algorithm = 'cts', ...))
- **PubChem** (Library-based TP data source for structure-based queries; accessed via generateTPs(algorithm = 'library', ...) with optional custom library support)
- **MetFrag** (Compound annotation tool that consumes TP datasets with structural information (SMILES); convertToMFDB generates MetFrag databases for all TPs with structural information)

## Examples

```
TPsBT <- generateTPs(algorithm = "biotransformer", parents = patRoonData::suspectsPos, type = "env")
```

## Evaluation signals

- All parents successfully routed to appropriate algorithm backend: structure-based parents have SMILES strings, formula-based parents have elemental composition data with no routing errors.
- Output TP object contains consistent parent-TP linkages with proper representation format: SMILES-derived TPs include structural data; formula-derived TPs include elemental transformation records.
- Multi-generation TPs (when generations > 1) show nested parent-TP relationships without duplicate or orphaned records.
- TP Score rankings (for ann_comp and ann_form methods) incorporate both structural similarity and suspect matching criteria as specified in patRoon documentation.
- Downstream suspect screening (screenSuspects function) successfully matches TP candidates from both SMILES-based and formula-based sources to experimental features without format conversion failures.

## Limitations

- Some parent compounds may lack complete structural or formula information, forcing fallback to suboptimal algorithm backends or exclusion from prediction.
- Multi-generation TP prediction (generations > 1) exponentially increases computational burden; no automatic stopping criterion is provided for poorly predictive intermediate TPs.
- Formula-based algorithms (logic rules, formula library) cannot predict positional or stereochemical isomers that differ only in connectivity; TP Score filtering may remove isomeric candidates important for suspect screening.
- Conversion between SMILES and formula representations is lossy in one direction; SMILES to formula loses stereochemistry and connectivity details; formula to SMILES is ambiguous (multiple isomers per formula).

## Evidence

- [other] Accept parent input from one of three sources: a suspect list (data.frame), matched feature groups from suspect screening, or a compounds object from annotation. Validate algorithm selection and route to the appropriate backend (BioTransformer, CTS, PubChem library, formula library, metabolic logic rules, or annotation candidates).: "Accept parent input from one of three sources: a suspect list (data.frame), matched feature groups from suspect screening, or a compounds object from annotation. Validate algorithm selection and"
- [other] For structure-based algorithms (biotransformer, cts, library, ann_comp), retrieve or predict TPs with SMILES and optional log P values; for formula-based algorithms (library_formula, ann_form, logic), calculate TPs from elemental transformations or annotation candidates.: "For structure-based algorithms (biotransformer, cts, library, ann_comp), retrieve or predict TPs with SMILES and optional log P values; for formula-based algorithms (library_formula, ann_form,"
- [other] For ann_comp and ann_form, rank candidates by TP Score incorporating structural similarity and suspect matching.: "For ann_comp and ann_form, rank candidates by TP Score incorporating structural similarity and suspect matching."
- [other] Return a TP object containing parent names, SMILES/formulas, and corresponding TP data, formatted for downstream suspect screening and componentization.: "Return a TP object containing parent names, SMILES/formulas, and corresponding TP data, formatted for downstream suspect screening and componentization."
- [other] Data is obtained of potential TPs for the parents of interest. The TPs may originate from a library or predicted _in-silico_.: "Data is obtained of potential TPs for the parents of interest. The TPs may originate from a library or predicted _in-silico_."
