---
name: biotransformation-rule-encoding
description: Use when you have untargeted metabolomics data with unknown metabolite
  structures and need to generate plausible candidate products by systematically applying
  known enzymatic or chemical transformation rules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - RDKit
  - HassounLab/BAM
  - PROXIMAL2
  - GNN-SOM
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c01565
  title: bam
evidence_spans:
- standard library for parsing and manipulating SMILES and chemical structures
- HassounLab/BAM
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bam
    doi: 10.1021/acs.analchem.4c01565
    title: bam
  dedup_kept_from: coll_bam
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01565
  all_source_dois:
  - 10.1021/acs.analchem.4c01565
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biotransformation-rule-encoding

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill encodes reaction biotransformation rules from metabolic databases (KEGG, RetroRules) into operator representations that enable systematic generation of candidate molecular structures from input metabolites. It is essential for scaling molecular structure discovery in untargeted metabolomics when the space of plausible biotransformations must be exhaustively represented.

## When to use

Apply this skill when you have untargeted metabolomics data with unknown metabolite structures and need to generate plausible candidate products by systematically applying known enzymatic or chemical transformation rules. Use it when you have access to a reaction dataset (KEGG, RetroRules, or custom) and need to encode those reactions as reusable operators for large-scale suspect generation.

## When NOT to use

- Reaction data is already encoded or available in a precomputed operator cache that matches your query set exactly — use the pre-encoded operators instead.
- You have only a small number of queries and manually curated biotransformations are more appropriate than exhaustive database-driven rule encoding.
- The input reaction dataset lacks EC annotations or standardized chemical structure formats (SMILES) — encoding will fail or produce incomplete operators.

## Inputs

- reaction_list CSV file with columns: id, formula, EC
- metabolites_list CSV file with metabolite identifiers and SMILES structures
- OP_CACHE_DIRECTORY path for operator storage

## Outputs

- Encoded biotransformation operators (cached in OP_CACHE_DIRECTORY)
- Serialized metabolite pair mappings (path_finalReactions)
- Transformation metadata (reaction ID, EC number, product relationships)

## How to apply

Load a reaction dataset specified as a CSV file with columns 'id', 'formula', and 'EC'. Parse the metabolites list (CSV with SMILES structures) and reaction definitions. Configure the biotransformation rule application engine within the BAM codebase to extract reaction patterns and convert them into operator representations, storing generated operators in a designated cache directory (OP_CACHE_DIRECTORY). The engine then uses these operators to map metabolite pairs and generate transformation metadata. This encoding step is critical before applying rules to query anchor-suspect pairs; it decouples rule extraction from rule application, allowing reuse across multiple query sets.

## Related tools

- **PROXIMAL2** (Prerequisite tool for biotransformation rule extraction and metabolic pathway prediction; BAM integrates PROXIMAL2 operators to encode biotransformation rules) — https://github.com/HassounLab/PROXIMAL2
- **GNN-SOM** (Graph neural network tool used alongside BAM for site-of-metabolism prediction and enzymatic product ranking; supports biotransformation rule application) — https://github.com/HassounLab/GNN-SOM
- **RDKit** (Chemical informatics library for parsing, validating, and manipulating SMILES structures during biotransformation rule encoding)

## Examples

```
sh runBAM.sh  # After configuring reaction_list, metabolites_list, OP_CACHE_DIRECTORY, and path_finalReactions in runBAM.sh with your KEGG or RetroRules dataset
```

## Evaluation signals

- All reactions in the input reaction_list are successfully parsed and assigned unique operator identifiers; no missing or malformed EC numbers.
- Generated operators correctly map metabolite pairs: verify that each operator produces valid SMILES product structures when applied to test substrates using RDKit validation.
- Operator cache directory contains serialized operator files matching the count and IDs of input reactions; file sizes are non-zero and schema is consistent.
- Metadata output (path_finalReactions) contains expected columns: substrate SMILES, product SMILES, operator ID, EC number, and reaction formula; no null entries for non-optional fields.
- Cross-validation: apply operators to a known biotransformation (e.g., a reference metabolite with annotated products) and confirm generated product SMILES match expected structures.

## Limitations

- Biotransformation rule encoding is database-dependent: KEGG and RetroRules may have different coverage, specificity, and reaction annotations; encoding results will vary significantly between databases.
- Operators are generated only for reactions with complete metadata (id, formula, EC); reactions with missing annotations are silently excluded, potentially reducing rule coverage.
- SMILES representation limitations: invalid or ambiguous SMILES in the metabolites_list will cause parsing failures; no automatic structure standardization is applied during encoding.
- The skill assumes conda environments for PROXIMAL2 and GNN-SOM are already installed and named 'proximal2' and 'som' respectively; encoding will fail if these prerequisites are not met.
- Operator cache grows with reaction database size; large KEGG or RetroRules datasets may require substantial disk space and memory for rule encoding.

## Evidence

- [readme] The desired reaction dataset of interest needs to be specified. We have used KEGG and RetroRules as examples.: "The desired reaction dataset of interest needs to be specified. We have used KEGG and RetroRules as examples."
- [readme] reaction_list = csv file of the reactions of interest. It must have the following columns: "id", "formula", "EC".: "reaction_list = csv file of the reactions of interest. It must have the following columns: "id", "formula", "EC"."
- [other] Access the biotransformation rules encoded in the BAM codebase and configure the rule application engine.: "Access the biotransformation rules encoded in the BAM codebase and configure the rule application engine."
- [readme] BAM uses previous tools, PROXIMAL2 and GNN-SOM. To use BAM, these tools need to be downloaded and included under the "BAM-main" directory.: "BAM uses previous tools, PROXIMAL2 and GNN-SOM. To use BAM, these tools need to be downloaded and included under the "BAM-main" directory."
- [readme] To apply BAM using other reaction data, the four reaction variables (metabolites_list, reaction_list, OP_CACHE_DIRECTORY, path_finalReactions) need to be appropriately defined: "To apply BAM using other reaction data, the four reaction variables (metabolites_list, reaction_list, OP_CACHE_DIRECTORY, path_finalReactions) need to be appropriately defined"
