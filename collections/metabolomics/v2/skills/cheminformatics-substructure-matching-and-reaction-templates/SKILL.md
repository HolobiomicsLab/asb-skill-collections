---
name: cheminformatics-substructure-matching-and-reaction-templates
description: 'Use when you have a chemical substrate and need to predict its biotransformation products using rule-based metabolism prediction. This applies when: (1) you possess a library of biotransformation rules extracted from a curated database (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0250
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - BioTransformer
  techniques:
  - tandem-MS
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
  - build: coll_biotransformer_1_0_cq
    doi: 10.1186/s13321-019-0375-2
    title: BioTransformer 1.0
  dedup_kept_from: coll_biotransformer_1_0_cq
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

# cheminformatics-substructure-matching-and-reaction-templates

## Summary

Apply SMARTS-based substructure matching and biotransformation reaction templates to predict small molecule metabolites in environmental, mammalian, and microbial systems. This skill enables systematic enumeration of possible metabolic products by matching input substrates against curated biotransformation rules and expanding matched substructures into product templates.

## When to use

Use this skill when you have a chemical substrate and need to predict its biotransformation products using rule-based metabolism prediction. This applies when: (1) you possess a library of biotransformation rules extracted from a curated database (e.g., EAWAG-BBD), (2) you need to enumerate all applicable transformations at a given metabolic depth, (3) the transformation rules are encoded as SMARTS patterns with condition thresholds and reaction metadata, and (4) you require reproducible, auditable metabolite prediction rather than black-box neural approaches.

## When NOT to use

- Input substrate is already a processed metabolite pool or feature table; this skill predicts de novo metabolites, not mining existing datasets.
- Biotransformation rules are unavailable or not encoded in SMARTS format; the skill requires a structured rule library to function.
- The analysis goal is to identify metabolites in untargeted mass spectrometry data without prediction; use spectral matching or molecular networking instead.

## Inputs

- substrate molecule in SMILES string format
- substrate molecule in MOL file format
- substrate molecule in SDF (multi-molecule) file format
- biotransformation rule set with SMARTS patterns, reaction metadata, and condition thresholds
- number of sequential transformation steps (integer: 1–3 typical)

## Outputs

- predicted metabolite structures in SDF format
- predicted metabolite structures in CSV format with metadata (parent, step, mass, formula, biotransformation rule ID)
- biotransformation pathway graph linking parent substrate to intermediate and final metabolites
- per-metabolite annotations: molecular mass, logP, molecular formula, enzyme family (if applicable)

## How to apply

First, parse and normalize biotransformation rules from a curated source (e.g., EAWAG's Biodegradation and Biocatalysis Database) into a structured rule set containing SMARTS patterns, reaction metadata, enzyme family constraints, and condition thresholds. Load the input substrate (provided as SMILES, MOL, or SDF format) into a cheminformatics library compatible with SMARTS matching. Iteratively apply each rule to the substrate by performing substructure matching: scan the substrate against each rule's SMARTS pattern to identify reactive sites. For every successful match, execute the associated reaction template to generate intermediate and final product structures. Store all generated metabolites along with their parent transformations, biotransformation pathway depth (step number), and molecular properties (mass, logP, formula). Control metabolite explosion by limiting the number of sequential transformation steps (e.g., 1–3 steps) as a parameter. Validate the output by comparing predicted metabolite structures, masses, and biotransformation logic against reference pathways documented in the source database or literature.

## Related tools

- **BioTransformer** (Core execution engine implementing substructure matching via SMARTS patterns and reaction template expansion for mammalian, gut microbial, and environmental microbial metabolism prediction.) — https://github.com/Wishartlab-openscience/Biotransformer

## Examples

```
java -jar biotransformer-3.0.0.jar -k pred -b envimicro -ismi "CC(C)C1=CC=C(C)C=C1O" -osdf metabolites.sdf -s 2
```

## Evaluation signals

- Predicted metabolites match reference biotransformations documented in EAWAG-BBD or published literature for the same substrate.
- Output metabolite masses and molecular formulas are consistent with expected mass shifts from applied biotransformation reactions (e.g., +16 for hydroxylation, −2 for dehydrogenation).
- All predicted metabolites satisfy the chemical validity constraints: valence rules, bond order integrity, and formal charge conservation in reaction templates.
- Biotransformation pathway depth does not exceed the user-specified step limit; no orphaned or disconnected metabolites in the pathway graph.
- SMARTS pattern matching results are reproducible: re-running the same substrate and rule set against the same cheminformatics library version yields identical products.

## Limitations

- The skill predicts thermodynamically and kinetically plausible reactions but does not rank by biological likelihood or organism-specific enzyme availability; organisms may not express all enzymatic pathways represented in the rule set.
- Environmental microbial module reports both aerobic and anaerobic reactions by default; users must filter manually if only one metabolic regime is relevant.
- Commercial use of environmental microbial degradation predictions requires explicit license from EnviPath; the EAWAG-BBD data is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0.
- Substructure matching may produce false positives if SMARTS patterns are overly permissive; validation against reference data is essential.
- Metabolite explosion increases exponentially with step depth; limiting steps to 1–3 is recommended unless computational resources and rule specificity justify deeper exploration.

## Evidence

- [other] biotransformation rules (reaction types, enzyme families, substrate patterns, product templates) applicable to soil and aquatic microbial degradation pathways: "extract biotransformation rules (reaction types, enzyme families, substrate patterns, product templates) applicable to soil and aquatic microbial degradation pathways"
- [other] SMARTS patterns, condition thresholds, reaction metadata: "Parse and normalize the biotransformation rules into a structured rule set (SMARTS patterns, condition thresholds, reaction metadata) compatible with cheminformatics libraries"
- [other] substructure matching and reaction template expansion: "applies the extracted biotransformation rules to input substrate molecules using substructure matching and reaction template expansion"
- [other] executing each applicable biotransformation rule against the input substrate: "Generate predicted metabolite structures by executing each applicable biotransformation rule against the input substrate and storing intermediate and final products"
- [other] output structures, biotransformation pathways, and molecular properties (mass, logP, etc.) against reference biotransformations: "Validate the predicted metabolite set by comparing output structures, biotransformation pathways, and molecular properties (mass, logP, etc.) against reference biotransformations documented in EAWAG"
- [readme] BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota"
- [readme] all reactions (aerobic and anaerobic) are reported, and not only the aerobic biotransformations: "For the environmental microbial biodegradation, all reactions (aerobic and anaerobic) are reported, and not only the aerobic biotransformations"
