---
name: seed-product-relationship-tracking
description: Use when when applying biotransformation rules to seed metabolites to
  generate candidates, you need to record which rule produced each candidate and link
  it back to its parent seed structure. This is essential for downstream validation
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - PROXIMAL2
  - GNN-SOM
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.4c01565
  title: bam
evidence_spans:
- No usage/docs found.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bam_cq
    doi: 10.1021/acs.analchem.4c01565
    title: bam
  dedup_kept_from: coll_bam_cq
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

# seed-product-relationship-tracking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Track and maintain parent–product relationships and applied biotransformation rule metadata when generating candidate metabolites from seed structures. This enables traceability of how each candidate was derived and supports validation and ranking of biotransformation predictions.

## When to use

When applying biotransformation rules to seed metabolites to generate candidates, you need to record which rule produced each candidate and link it back to its parent seed structure. This is essential for downstream validation (e.g., suspect library construction), for ranking candidates by biotransformation type or chemical plausibility, and for interpreting why a particular molecular candidate was proposed.

## When NOT to use

- When seed metabolites are already known compounds in a reference database and no new structural candidates need to be generated.
- When the biotransformation rules are abstract or not grounded in reaction databases (e.g., arbitrary chemical transformations without rule provenance).
- When computational resources are severely constrained and metadata storage overhead is prohibitive (though this is rarely a blocker for metabolomics-scale data).

## Inputs

- Seed metabolite structures (SMILES or MOL format, parsed into RDKit molecular graph objects)
- Biotransformation rules (each specifying reactant SMARTS, product SMARTS, transformation type, and optional reaction metadata)
- Rule application results (matched rule, generated product molecule, canonicalized SMILES, validity flags)

## Outputs

- Parent–product relationship records (seed identifier, rule identifier, product SMILES, rule metadata)
- Candidate molecule set with deduplicated products and associated rule provenance
- Transformation history log linking each candidate to its biotransformation rule(s) and source seed(s)

## How to apply

After executing each biotransformation rule transformation (via SMARTS substructure matching), canonicalize the product SMILES and validate chemical properties (valence, aromaticity). Before aggregating products into a candidate set and removing duplicates, explicitly store a link record for each product that includes: (1) parent seed metabolite identifier/SMILES, (2) applied rule identifier and type, (3) product canonical SMILES, and (4) optional transformation metadata (e.g., reaction EC number if sourced from KEGG or RetroRules). When deduplicating by canonical SMILES, retain the rule metadata for the first occurrence and optionally flag if multiple distinct rules produce the same product. This metadata is critical for later stages such as ranking candidates by biotransformation plausibility or validating against known suspects.

## Related tools

- **RDKit** (Parses seed metabolite structures into molecular graphs, executes SMARTS-based rule matching, canonicalizes SMILES, and validates chemical properties (valence, aromaticity) of generated products.)
- **PROXIMAL2** (Predecessor tool used within BAM pipeline for generating biotransformation operators and pathway analysis.) — https://github.com/HassounLab/PROXIMAL2
- **GNN-SOM** (Predecessor tool used within BAM pipeline for site-of-metabolism prediction and ranking of enzymatic products.) — https://github.com/HassounLab/GNN-SOM

## Evaluation signals

- Every product in the candidate set has a traceable parent–product link to at least one seed metabolite and applied biotransformation rule.
- All products pass chemical validity checks (e.g., correct valence, valid aromaticity) before being stored in the candidate set.
- Canonical SMILES for each product is consistent across multiple deduplication runs (deterministic canonicalization).
- When the same product is generated by multiple distinct rules, all applicable rule identifiers are captured in the metadata.
- For validation cases (suspects with known structures), the correct suspect structure appears in the candidate set with documented rule provenance matching expected biotransformation pathways.

## Limitations

- Metadata storage scales linearly with the number of rules and seed metabolites; for large databases (e.g., KEGG with >10k metabolites and RetroRules with >100k reactions), storage and lookup efficiency must be managed.
- SMARTS-based rule matching can produce false-positive product candidates if rules are overly broad or not curated; metadata alone does not validate chemical feasibility or biological plausibility.
- If biotransformation rules do not encode biological context (e.g., organism, pathway, enzymatic specificity), tracking rule provenance may not distinguish biologically likely from unlikely products.
- Duplicate products generated by semantically equivalent but structurally distinct rules may be collapsed during deduplication, losing information about alternative transformation routes unless rule metadata is preserved before merging.

## Evidence

- [other] For each matched rule, execute the transformation to generate product molecule(s), canonicalize SMILES, and check for validity (e.g., valence, aromaticity). Aggregate all products into a candidate molecule set, remove duplicates (by canonical SMILES), and store with parent–product links and applied rule metadata.: "For each matched rule, execute the transformation to generate product molecule(s), canonicalize SMILES, and check for validity (e.g., valence, aromaticity). Aggregate all products into a candidate"
- [readme] The desired reaction dataset of interest needs to be specified. We have used KEGG and RetroRules as examples.: "The desired reaction dataset of interest needs to be specified. We have used KEGG and RetroRules as examples."
- [other] BAM implements a biotransformation-based annotation method that applies biotransformation rules to generate molecular candidates from metabolomics data.: "BAM implements a biotransformation-based annotation method that applies biotransformation rules to generate molecular candidates from metabolomics data."
