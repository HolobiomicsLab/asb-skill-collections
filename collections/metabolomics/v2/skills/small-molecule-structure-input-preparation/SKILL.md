---
name: small-molecule-structure-input-preparation
description: Use when you have a small-molecule chemical structure in an initial or
  non-standard format and need to predict its environmental microbial degradation,
  gut microbiota metabolism, or mammalian biotransformation using BioTransformer's
  prediction modules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_3407
  tools:
  - BioTransformer
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab). Env. module data CC-BY-NC-SA (enviPath/EAWAG).
    url: https://bitbucket.org/wishartlab/biotransformer.git
  license_tier: noncommercial
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-019-0375-2
  title: BioTransformer 1.0
evidence_spans:
- This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that
  predicts small molecule metabolism
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biotransformer_1_0_2_cq
    doi: 10.1186/s13321-019-0375-2
    title: BioTransformer 1.0
  dedup_kept_from: coll_biotransformer_1_0_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-019-0375-2
  all_source_dois:
  - 10.1186/s13321-019-0375-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# small-molecule-structure-input-preparation

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Prepare and validate small-molecule chemical structures for computational metabolism prediction by converting them into formats compatible with BioTransformer (SMILES, MOL, or SDF). This skill ensures structural data is in the correct format and ready for input to prediction modules.

## When to use

You have a small-molecule chemical structure in an initial or non-standard format and need to predict its environmental microbial degradation, gut microbiota metabolism, or mammalian biotransformation using BioTransformer's prediction modules. Use this skill before executing any BioTransformer metabolism prediction workflow.

## When NOT to use

- The input is already a metabolite prediction result or a list of predicted metabolites.
- The input is a protein or macromolecular structure (BioTransformer is designed for small molecules).
- The structural data is incomplete or lacks sufficient chemical information to uniquely define a compound.

## Inputs

- SMILES string
- MOL file
- SDF file
- Chemical structure object

## Outputs

- Validated small-molecule structure in SMILES format
- Validated small-molecule structure in MOL format
- Validated small-molecule structure in SDF format
- BioTransformer-compatible input object

## How to apply

Accept chemical structure input in any common format (e.g., SMILES string, MOL file, SDF file, or structural representation). Validate the structure for chemical validity and completeness (proper valence, connectivity, stereochemistry where relevant). Convert the structure to one of BioTransformer's accepted input formats: SMILES, MOL, or SDF. Load the formatted structure into BioTransformer as input to the appropriate degradation or metabolism module. Verify that the structure loads without error before proceeding to the prediction step.

## Related tools

- **BioTransformer** (Accepts prepared small-molecule structures and predicts metabolism via environmental microbial degradation, gut microbiota, and mammalian modules) — bitbucket.org/wishartlab/biotransformer

## Evaluation signals

- The structure is successfully loaded into BioTransformer without parsing or format errors.
- Chemical validity is confirmed: all atoms have correct valence and bonding.
- Stereochemistry (if present in the original input) is preserved in the output format.
- The prepared structure can be queried against EAWAG-BBD and EnviPath transformation databases without ambiguity.
- Output format (SMILES, MOL, or SDF) matches one of BioTransformer's documented accepted inputs.

## Limitations

- BioTransformer is specifically designed for small molecules; macromolecular or polymeric structures are out of scope.
- Structures with incomplete or ambiguous stereochemical specification may produce multiple predictions.
- The fidelity of metabolism prediction depends on the completeness and accuracy of the input structure; errors in structure preparation will propagate downstream.
- No changelog is provided in the BioTransformer documentation, so format compatibility across version updates cannot be confirmed.

## Evidence

- [other] Load the input small-molecule structure (SMILES, MOL, or SDF format) into BioTransformer.: "Load the input small-molecule structure (SMILES, MOL, or SDF format) into BioTransformer."
- [intro] BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota"
- [intro] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database"
