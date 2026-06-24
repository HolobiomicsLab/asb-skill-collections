---
name: data-structure-validation
description: Use when after converting or filtering objects (e.g., transformation
  products to suspect lists, feature groups through componentization) and before passing
  them to downstream functions like screenSuspects or generateComponents.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - patRoon
  - patRoonData
  techniques:
  - mass-spectrometry
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
  - build: coll_injectiondesign_cq
    doi: 10.1101/2023.02.26.530140v1.article-info
    title: InjectionDesign
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

# Data Structure Validation

## Summary

Verify that intermediate and output data objects conform to expected schemas and formats required by downstream processing steps in mass spectrometry non-target analysis workflows. This ensures compatibility across tool chains and prevents silent failures in suspect screening and transformation product pipelines.

## When to use

After converting or filtering objects (e.g., transformation products to suspect lists, feature groups through componentization) and before passing them to downstream functions like screenSuspects or generateComponents. Validation is critical when chaining multiple algorithms or combining results from different sources, as schema mismatches propagate silently through workflows.

## When NOT to use

- Input is a raw MS data file (mzML, NetCDF) — use format converters (ProteoWizard, OpenMS) instead; this skill applies only to R objects and data.frames.
- Object is being created for the first time within a well-tested function — implicit validation in the function (e.g., screenSuspects) is sufficient unless manual construction or third-party input is involved.
- You are debugging a function's internal consistency rather than validating inter-function compatibility — use R's str(), class(), and traceback() utilities.

## Inputs

- Transformation product object (output of generateTPs)
- Suspect list data.frame (output of convertToSuspects)
- Feature group object (output of groupFeatures)
- Component object (output of generateComponents)
- Filtered object output (output of filter() with any parameter)

## Outputs

- Validated data object (same type as input, confirmed schema-compliant)
- Validation report or error message indicating schema mismatches

## How to apply

Inspect the output object's structure against the documented schema expected by the next processing function. For suspect lists created by convertToSuspects, verify presence of required columns (name, SMILES or formula, optional adduct/mass fields) and data types. For transformation product objects, ensure parent and TP identifiers, names, and chemical identifiers (SMILES, InChIKey, formula) are correctly populated. Check that optional fields (e.g., includeParents flag output) are present when enabled. Compare the validated structure against known-good reference formats from example datasets (e.g., patRoonData::suspectsPos). This validation may occur implicitly when the downstream function (e.g., screenSuspects) is called, but explicit pre-validation catches issues earlier and aids debugging.

## Related tools

- **patRoon** (Provides convertToSuspects, generateTPs, screenSuspects, generateComponents and implicit validation through function signatures and S4 class definitions) — https://github.com/rickhelmus/patRoon
- **patRoonData** (Supplies reference datasets (suspectsPos, ISTDListPos) for comparison against validated structures)

## Examples

```
suspects <- convertToSuspects(TPs, includeParents = TRUE); str(suspects); all(c('name', 'SMILES') %in% colnames(suspects))
```

## Evaluation signals

- Validated suspect list data.frame contains exactly the required columns (name, SMILES or formula, optional adduct/mass) with no unexpected NA patterns in mandatory fields.
- Transformation product object validates that parents() function returns non-empty records when includeParents=TRUE, and empty or absent when FALSE.
- Downstream function (screenSuspects, generateComponents) accepts the validated object without throwing schema or type errors.
- Row counts and chemical identifier formats (SMILES string syntax, InChIKey character length, formula notation) match expected patterns from reference datasets.
- Optional fields (e.g., adduct column in suspect list, annotation score columns in TP object) are present and non-corrupted when enabled by user parameters.

## Limitations

- Validation is implicit in many patRoon functions; explicit schema documentation is sparse in the README and article, requiring inspection of function signatures and example code.
- Complex nested objects (e.g., TP objects with parent and annotation metadata) may have multiple valid schemas depending on which algorithms were used to generate them (BioTransformer vs. CTS vs. library); validation logic must account for algorithm-specific variations.
- No built-in validation reporting function is documented; users must manually inspect object structure using R introspection tools (str(), head(), class()) or rely on errors thrown downstream.

## Evidence

- [other] convertToSuspects converts a TP object into a suspect list format that can be used as input for screenSuspects, with an optional includeParents parameter to include parent compounds in addition to transformation products.: "convertToSuspects converts a TP object into a suspect list format that can be used as input for screenSuspects, with an optional includeParents parameter to include parent compounds"
- [other] Format extracted data into a suspect list data.frame with required columns (name, SMILES or formula, and optional adduct/mass columns).: "Format extracted data into a suspect list data.frame with required columns (name, SMILES or formula, and optional adduct/mass columns)"
- [other] Validate suspect list structure matches the format required by screenSuspects (same as standard suspect screening format).: "Validate suspect list structure matches the format required by screenSuspects (same as standard suspect screening format)"
- [readme] S4 classes and generics are used to implement a consistent interface to all supported algorithms.: "S4 classes and generics are used to implement a consistent interface to all supported algorithms"
- [readme] patRoon combines established software tools with novel functionality in order to provide comprehensive NTA workflows. The different algorithms are provided through a consistent interface, which removes the need to know all the details of each individual software tool and performing tedious data conversions during the workflow.: "The different algorithms are provided through a consistent interface, which removes the need to know all the details of each individual software tool and performing tedious data conversions"
