---
name: metabolite-identification-from-transformation-rules
description: Use when when you have a small-molecule structure (SMILES, MOL, or SDF format) and need to identify probable metabolites or degradation products in a specific biological compartment (e.g., soil/aquatic microbiota, mammalian liver, or gut microbiota).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-identification-from-transformation-rules

## Summary

Predict the chemical structures of small-molecule metabolites by applying biotransformation rules from curated metabolic databases to an input compound structure. This skill enables identification of likely degradation products and metabolic intermediates in specific biological contexts (mammalian, gut microbial, or environmental).

## When to use

When you have a small-molecule structure (SMILES, MOL, or SDF format) and need to identify probable metabolites or degradation products in a specific biological compartment (e.g., soil/aquatic microbiota, mammalian liver, or gut microbiota). Use this skill when experimental metabolite detection (e.g., mass spectrometry) has identified unknown peaks and you need to predict which biotransformations could have produced them, or when designing environmental fate assessments or xenobiotic metabolism studies.

## When NOT to use

- Input is a macromolecule (protein, nucleic acid, polysaccharide) — BioTransformer is designed for small molecules only.
- Biological context is not specified or irrelevant — tool modules are context-specific (mammalian vs. microbial vs. environmental); mismatched context will produce spurious predictions.
- Experimental metabolite identity is already confirmed by high-resolution mass spectrometry and NMR — use this skill for hypothesis generation, not validation of known structures.

## Inputs

- small-molecule structure (SMILES string)
- small-molecule structure (MOL file)
- small-molecule structure (SDF file)

## Outputs

- predicted metabolite structures (chemical coordinates and SMILES)
- applied biotransformation rules per metabolite
- degradation pathway annotations
- structured output file listing all predicted metabolites with annotations

## How to apply

Load the input small-molecule structure into BioTransformer in SMILES, MOL, or SDF format, then select and execute the appropriate degradation module (environmental microbial, mammalian, or gut microbiota) depending on your biological context of interest. BioTransformer queries curated metabolic transformation data (EAWAG-BBD or equivalent) to identify applicable enzymatic or abiotic transformation rules. The tool returns predicted metabolite structures along with the specific transformation rules applied and the degradation pathway annotations. Assess the plausibility of predictions by cross-referencing the predicted structures and pathways against your experimental observations (e.g., mass-to-charge ratios, retention times, or literature precedent for similar compounds).

## Related tools

- **BioTransformer** (Executes biotransformation prediction queries against EAWAG-BBD and EnviPath databases to generate metabolite structures and associated transformation rules for the input compound.) — bitbucket.org/wishartlab/biotransformer

## Evaluation signals

- Predicted metabolite structures are chemically valid (no valence violations, ring closures, or impossible chirality).
- Applied transformation rules are grounded in EAWAG-BBD or EnviPath (i.e., not ad-hoc or hallucinated).
- Predicted metabolites match the mass-to-charge ratios or chromatographic retention times of observed unknowns in your experimental data.
- Degradation pathways form a connected acyclic or weakly cyclic graph from parent to terminal metabolites, consistent with biochemical logic.
- Repeated predictions for chemically similar parent structures yield related (not random) metabolite sets.

## Limitations

- Predictions are based on curated transformations in EAWAG-BBD and EnviPath; rare or novel biotransformations not in these databases will not be predicted.
- BioTransformer does not account for organism-specific metabolic capacity, enzyme kinetics, or competition between pathways — all applicable rules are applied, potentially inflating the number of predicted metabolites.
- Environmental module predictions assume generic soil/aquatic microbiota consortia; site-specific microbial communities or environmental conditions (pH, redox, temperature) may follow different transformation hierarchies.
- No changelog provided; version stability and update frequency of underlying metabolic databases are not documented.

## Evidence

- [intro] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database"
- [other] Input format specification and execution workflow: "Load the input small-molecule structure (SMILES, MOL, or SDF format) into BioTransformer. 2. Execute BioTransformer's environmental microbial degradation module, which queries EAWAG-BBD and EnviPath"
- [other] Output includes metabolite structures and transformation annotations: "Retrieve predicted metabolites, including chemical structures, transformation rules applied, and degradation pathway information."
- [intro] BioTransformer's scope across biological contexts: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota"
- [intro] Role of predictions in metabolite identification: "BioTransformer also assists scientists in metabolite identification, based on the metabolism prediction"
