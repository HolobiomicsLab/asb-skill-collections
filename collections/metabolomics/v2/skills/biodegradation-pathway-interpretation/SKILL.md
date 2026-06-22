---
name: biodegradation-pathway-interpretation
description: Use when you have a small-molecule chemical structure (as SMILES, MOL, or SDF) and need to predict how soil or aquatic microbiota will degrade or biotransform it.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_2814
  tools:
  - BioTransformer
derived_from:
- doi: 10.1186/s13321-019-0375-2
  title: BioTransformer 1.0
evidence_spans:
- This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that predicts small molecule metabolism
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

# biodegradation-pathway-interpretation

## Summary

Reconstruct predicted environmental microbial degradation pathways for small molecules using BioTransformer's EAWAG-BBD-backed module to identify metabolites and transformation rules in soil and aquatic microbiota. This skill enables scientists to anticipate how xenobiotics and environmental contaminants will be metabolized by natural microbial communities.

## When to use

Apply this skill when you have a small-molecule chemical structure (as SMILES, MOL, or SDF) and need to predict how soil or aquatic microbiota will degrade or biotransform it. Use it to support metabolite identification, environmental fate assessment, or to understand which biotransformation rules apply to a given compound. Trigger: you are investigating environmental persistence, bioaccumulation risk, or microbial metabolic capacity for a novel or xenobiotic molecule.

## When NOT to use

- Input is a macromolecule (protein, RNA, polysaccharide) rather than a small molecule; BioTransformer targets xenobiotics and small-molecule metabolism.
- Goal is mammalian or gut microbiota metabolism; use BioTransformer's mammalian or gut-microbiota modules instead.
- Pathway prediction is not needed; if you only require chemical structure validation or property prediction without metabolic fate, use alternative cheminformatics tools.

## Inputs

- small-molecule structure in SMILES format
- small-molecule structure in MOL format
- small-molecule structure in SDF format

## Outputs

- predicted metabolite structures (MOL/SMILES)
- biotransformation rules applied per step
- degradation pathway graph/annotation
- structured output file with metabolites and transformations

## How to apply

Load the small-molecule structure into BioTransformer in SMILES, MOL, or SDF format. Execute the environmental microbial degradation module, which queries EAWAG-BBD (EAWAG's Biodegradation and Biocatalysis Database) and EnviPath metabolic transformation data to generate predictions. Retrieve the predicted metabolites, including their chemical structures and the specific transformation rules applied at each step. Format and export results as a structured output listing all predicted metabolites with their corresponding structures and transformation annotations. Validate the pathway by checking that transformation rules are sourced from EAWAG-BBD and that intermediate and terminal metabolites are chemically plausible.

## Related tools

- **BioTransformer** (primary tool for predicting environmental microbial degradation pathways by querying EAWAG-BBD and EnviPath transformation data) — bitbucket.org/wishartlab/biotransformer

## Evaluation signals

- All predicted metabolites have valid chemical structures (valid SMILES/MOL encoding).
- Each biotransformation step is annotated with a transformation rule sourced from EAWAG-BBD or EnviPath.
- Predicted metabolites are chemically plausible intermediates or products of known microbial enzymatic reactions (e.g., oxidation, hydrolysis, conjugation).
- Pathway completeness: terminal metabolites are identified and marked as dead-end or further degradable.
- Output file structure includes metabolite identifiers, structures, and transformation rule citations; no missing or malformed entries.

## Limitations

- BioTransformer predictions depend on the completeness and currency of EAWAG-BBD and EnviPath; compounds absent from these databases may yield incomplete or no predictions.
- Predictions are based on known microbial transformations and may not capture novel enzymatic pathways or rare catabolic functions of uncultured microbiota.
- Environmental factors (pH, temperature, oxygen availability, redox potential) are not explicitly modeled; predictions assume standard aerobic or anaerobic conditions represented in the training data.
- No changelog found in the available documentation; version 3.0.0 status and recent updates are not detailed.

## Evidence

- [other] environmental module input format support: "Load the input small-molecule structure (SMILES, MOL, or SDF format) into BioTransformer."
- [intro] EAWAG-BBD data source: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database"
- [other] environmental module output structure: "Retrieve predicted metabolites, including chemical structures, transformation rules applied, and degradation pathway information."
- [intro] metabolite identification use case: "BioTransformer also assists scientists in metabolite identification, based on the metabolism prediction"
- [intro] scope of BioTransformer metabolism prediction: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota"
