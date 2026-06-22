---
name: gap-filling-and-reaction-conflict-resolution
description: Use when when merging multiple draft metabolic models (in JSON, XML, or SBML format) from community members or assembly variants and you encounter conflicting reaction annotations, missing metabolic pathways, or incomplete gap-filling decisions that require arbitration across inputs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3837
  edam_topics:
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - COMMIT
derived_from:
- doi: 10.1371/journal.pcbi.1009906
  title: COMMIT
evidence_spans:
- community-dependent gap-filling using COMMIT for communites sampled from
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_commit_cq
    doi: 10.1371/journal.pcbi.1009906
    title: COMMIT
  dedup_kept_from: coll_commit_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009906
  all_source_dois:
  - 10.1371/journal.pcbi.1009906
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gap-filling-and-reaction-conflict-resolution

## Summary

Resolve metabolic pathway conflicts and fill gaps in consensus reconstructions by applying community-dependent logic to select the most-supported reactions across multiple draft genome-scale models. This skill ensures the final consensus reconstruction captures biologically plausible pathways that are collectively supported by the input community members.

## When to use

When merging multiple draft metabolic models (in JSON, XML, or SBML format) from community members or assembly variants and you encounter conflicting reaction annotations, missing metabolic pathways, or incomplete gap-filling decisions that require arbitration across inputs. Apply this skill after parsing and validating individual models but before exporting the final consensus reconstruction.

## When NOT to use

- Input is a single metabolic model (no conflicts to resolve; use model validation instead)
- Models are from unrelated organisms with fundamentally different metabolic capabilities (consensus may be uninformative)
- Input models are already manually curated and conflict-resolved; additional gap-filling may introduce redundancy

## Inputs

- Multiple draft genome-scale metabolic models in standard format (JSON, XML, SBML)
- Parsed and validated individual metabolic model structures
- Annotation metadata (gene associations, reaction IDs, metabolite lists)

## Outputs

- Consensus metabolic reconstruction with resolved conflicts
- Final genome-scale metabolic model in SBML or standard systems biology format
- Gap-filling report documenting which pathways were selected and on what basis

## How to apply

After identifying common reactions, metabolites, and gene associations across all input models, execute COMMIT's community-dependent gap-filling logic to resolve conflicts by selecting the most supported metabolic pathways. The algorithm weighs evidence from all input draft reconstructions: reactions or pathways present in a higher proportion of input models are prioritized, and when conflicts arise (e.g., competing reaction variants or gene-protein-reaction associations), the choice favoring community consensus is retained. Apply thresholds based on support frequency across input models (e.g., pathways supported by >50% of inputs) to decide which to retain. Finally, validate that the consensus reconstruction maintains structural integrity and that all gap-filled reactions preserve mass and charge balance.

## Related tools

- **COMMIT** (Executes consensus-merging algorithm, conflict resolution, and community-dependent gap-filling logic to generate the final consensus metabolic reconstruction from multiple input draft models) — https://zenodo.org/badge/latestdoi/363932874

## Evaluation signals

- All reactions in the consensus model satisfy mass and charge balance constraints (validate using constraint checking)
- Reactions and pathways in the output model are supported by ≥1 of the input models; no novel reactions introduced without explicit gap-filling justification
- Gene-protein-reaction associations are consistent across all retained reactions (no orphaned or conflicting annotations)
- Consensus model can be successfully exported to SBML or equivalent format without schema or encoding errors
- Gap-filling report shows that each conflict resolution decision was made deterministically based on community support frequency or predefined criteria

## Limitations

- Gap-filling success depends on the quality and completeness of input draft models; poor-quality inputs may propagate errors to consensus
- Community-dependent logic assumes that higher support frequency correlates with biological correctness, which may fail when a minority of inputs capture rare but valid pathways
- Conflict resolution does not account for environmental or phenotypic context of individual community members; may produce an ecologically implausible 'average' reconstruction

## Evidence

- [other] COMMIT implements community-dependent gap-filling to generate consensus metabolic reconstructions from multiple draft reconstructions: "COMMIT implements community-dependent gap-filling to generate consensus metabolic reconstructions from multiple draft reconstructions of Arabidopsis thaliana-associated communities."
- [other] Execute COMMIT's consensus-merging algorithm to identify common reactions, metabolites, and gene associations across all input models: "Execute COMMIT's consensus-merging algorithm to identify common reactions, metabolites, and gene associations across all input models."
- [other] Resolve conflicts and gaps by applying COMMIT's community-dependent gap-filling logic to select the most supported metabolic pathways: "Resolve conflicts and gaps by applying COMMIT's community-dependent gap-filling logic to select the most supported metabolic pathways."
- [intro] Generation of consensus metabolic reconstructions and community-dependent gap-filling using COMMIT for communities sampled from Arabidopsis thaliana: "Generation of consensus metabolic reconstructions and community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana"
