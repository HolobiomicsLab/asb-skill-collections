---
name: plant-metabolic-network-validation
description: Use when after community-dependent gap-filling has proposed reactions to fill metabolic gaps in individual consensus reconstructions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3678
  - http://edamontology.org/topic_0621
  tools:
  - COMMIT
derived_from:
- doi: 10.1371/journal.pcbi.1009906
  title: COMMIT
- doi: 10.5281/zenodo.363932874
  title: ''
evidence_spans:
- community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_commit
    doi: 10.1371/journal.pcbi.1009906
    title: COMMIT
  dedup_kept_from: coll_commit
schema_version: 0.2.0
---

# plant-metabolic-network-validation

## Summary

Validate gap-filled plant metabolic reconstructions by checking consistency with known plant metabolism and inter-member metabolic exchange requirements in microbial communities. This skill ensures that reactions proposed during community-dependent gap-filling are biologically plausible and compatible with the broader community metabolic context.

## When to use

After community-dependent gap-filling has proposed reactions to fill metabolic gaps in individual consensus reconstructions. Use this skill when you have gap-filled metabolic models for plant-associated microbial community members and need to verify that filled reactions are consistent with known Arabidopsis thaliana metabolism and do not violate inter-member metabolic dependencies or exchange constraints.

## When NOT to use

- Input metabolic models have not undergone gap-filling; validation is only meaningful after gap-filling has been applied.
- Community context and inter-member exchange requirements have not been characterized; validation requires knowledge of which metabolites are shared or exchanged between members.
- Working with non-plant microbial communities where reference Arabidopsis thaliana metabolism is not applicable as a validation standard.

## Inputs

- Gap-filled metabolic models for community members (COMMIT output with annotations of filled reactions)
- Consensus metabolic reconstructions for Arabidopsis thaliana reference
- Inter-member metabolic exchange requirements and dependency profiles

## Outputs

- Validated gap-filled metabolic models with confidence annotations
- Validation report indicating which filled reactions passed/failed consistency checks
- Flagged reactions requiring manual curation or removal

## How to apply

Load the gap-filled metabolic models output from the COMMIT community-dependent gap-filling module. For each filled reaction, cross-reference against curated plant (Arabidopsis thaliana) metabolic databases and biochemical literature to verify metabolic plausibility. Check that filled reactions maintain consistency with known plant metabolic pathways and do not introduce conflicting stoichiometric or energetic constraints. Verify that proposed reactions support rather than contradict identified inter-member metabolic exchange requirements (e.g., metabolite uptake/secretion profiles). Annotate each filled reaction with confidence scores and source justification, then flag reactions that fail validation for manual curation or removal.

## Related tools

- **COMMIT** (Generates community-dependent gap-filled metabolic reconstructions that serve as input to validation; outputs models with annotations indicating source and confidence of filled reactions) — 10.5281/zenodo.363932874

## Evaluation signals

- All filled reactions have been cross-referenced against Arabidopsis thaliana metabolic pathway databases and curated biochemical literature with documented sources.
- Validated filled reactions maintain stoichiometric and energetic consistency (no conflicting ATP or redox balance violations introduced).
- Inter-member metabolic exchange requirements are satisfied: filled reactions do not prevent expected metabolite exchange between community members.
- Confidence annotations or validation flags are consistently assigned and document the reasoning for acceptance or rejection of each filled reaction.
- Validation report shows high agreement rate (>80%) between automated checks and manual spot-checks of representative filled reactions.

## Limitations

- Validation relies on the completeness and accuracy of Arabidopsis thaliana reference metabolic knowledge; gaps or errors in reference databases will propagate into validation results.
- Inter-member exchange requirements may be incompletely characterized, limiting ability to validate cross-member metabolic consistency; validation may miss biologically implausible solutions that happen to match incomplete exchange data.
- Manual curation and biochemical literature review are labor-intensive; automated validation checks may miss context-dependent plausibility constraints that require expert judgment.
- No changelog or version tracking documented for the reference Arabidopsis thaliana metabolism used; reproducibility depends on explicitly versioning reference metabolic databases.

## Evidence

- [other] Validate filled gaps by checking consistency with known plant (Arabidopsis thaliana) metabolism and inter-member exchange requirements.: "Validate filled gaps by checking consistency with known plant (Arabidopsis thaliana) metabolism and inter-member exchange requirements."
- [other] Output gap-filled metabolic models for each community member with annotations indicating source and confidence of filled reactions.: "Output gap-filled metabolic models for each community member with annotations indicating source and confidence of filled reactions."
- [intro] community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana: "community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana"
