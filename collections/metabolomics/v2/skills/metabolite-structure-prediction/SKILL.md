---
name: metabolite-structure-prediction
description: Use when you have a parent compound (or set of compounds) in SMILES,
  MOL, or SDF format and need to predict plausible metabolite structures and pathways
  in a specific biological context (mammalian Phase I/II metabolism, human gut microbiota,
  or soil/aquatic microbial degradation).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3407
  tools:
  - BioTransformer
  - EAWAG Biodegradation and Biocatalysis Database
  techniques:
  - LC-MS
  - NMR
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab). Env. module data CC-BY-NC-SA (enviPath/EAWAG).
    url: https://bitbucket.org/wishartlab/biotransformer.git
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-structure-prediction

## Summary

Predict small molecule metabolite structures across mammalian, gut microbial, and environmental microbial systems using BioTransformer's biotransformation rules and reaction templates. This skill enables scientists to generate candidate metabolite identities and metabolic pathways from parent compounds, supporting both exploratory metabolism studies and targeted metabolite identification workflows.

## When to use

Apply this skill when you have a parent compound (or set of compounds) in SMILES, MOL, or SDF format and need to predict plausible metabolite structures and pathways in a specific biological context (mammalian Phase I/II metabolism, human gut microbiota, or soil/aquatic microbial degradation). Use it prior to experimental validation (LC-MS, NMR) to constrain the search space for observed metabolites, or to generate reference metabolite libraries for annotation of untargeted metabolomics data.

## When NOT to use

- Input compound is not a small molecule or lacks chemical structure (e.g., peptide, polymer, or protein)
- You need to predict metabolism in an unlisted biological system not covered by BioTransformer (e.g., plant-specific, fungal-specific, or extinct organism metabolism)
- Input data are already annotated metabolite structures and you seek only to validate their chemical correctness without generating new predictions

## Inputs

- Parent compound(s) in SMILES format
- Parent compound(s) in MOL format
- Parent compound(s) in SDF format
- Target metabolite mass(es) [for identification task]
- Mass tolerance threshold [for identification task]

## Outputs

- Predicted metabolite structures (SDF format)
- Predicted metabolite structures (CSV format)
- Biotransformation reaction types and pathways
- Metabolite names and PubChem CIDs [if annotated]
- Metabolite match scores and organism context

## How to apply

Prepare the input compound(s) in SMILES, MOL, or SDF format. Select the appropriate BioTransformer biotransformer type (-b flag): 'cyp450', 'phaseII', 'ecbased', or 'hgut' for mammalian metabolism; 'superbio' or 'allHuman' for multi-step human transformations; or 'envimicro' for environmental microbial degradation (which applies EAWAG biodegradation rules). Specify the number of transformation steps (-s flag; default is 1) to control metabolic depth. Execute the prediction task (-k pred) to generate metabolite structures, biotransformation reaction types, and pathway information. Optionally annotate output metabolites with PubChem identifiers (-a flag) and save results in SDF or CSV format (-osdf or -ocsv). For targeted metabolite identification, combine predictions with mass-to-charge matching using the compound identification task (-k cid) with specified masses (-m flag) and mass tolerance (-t flag; default 0.01 Da).

## Related tools

- **BioTransformer** (Core metabolism prediction engine; applies biotransformation rules and reaction templates to predict metabolite structures, reaction pathways, and metabolic intermediates across mammalian, gut microbial, and environmental microbial systems.) — https://github.com/Wishartlab-openscience/Biotransformer
- **EAWAG Biodegradation and Biocatalysis Database** (Source of biotransformation rules and enzyme-catalyzed reactions for environmental microbial degradation module; provides substrate patterns, reaction types, and product templates.)

## Examples

```
java -jar biotransformer-3.0.0.jar -k pred -b allHuman -ismi "CC(C)C1=CC=C(C)C=C1O" -ocsv output.csv -s 2 -cm 3
```

## Evaluation signals

- Output metabolite structures are chemically valid (proper valence, stereochemistry, bond orders) and consistent with parent compound elemental composition
- Predicted metabolite masses match expected values given the biotransformation reactions applied (e.g., +16 Da for oxidation, +162 Da for glucuronidation)
- Biotransformation pathways respect known enzyme specificities and reaction mechanisms (e.g., CYP450 oxidations on aromatic rings or aliphatic carbons; Phase II conjugations on hydroxyl, carboxyl, or amine groups)
- When compound identification task is used, predicted metabolite structures align with observed spectral/chromatographic features and fall within specified mass tolerance window
- Number of predicted metabolites increases monotonically with number of transformation steps (-s flag) and is non-empty for biologically reasonable substrates

## Limitations

- Environmental microbial degradation module is licensed under Creative Commons BY-NC-SA 4.0; commercial use requires explicit license from EnviPath
- BioTransformer predicts thermodynamically and kinetically plausible metabolites but does not rank by bioavailability, tissue distribution, or actual likelihood of formation in vivo
- Prediction accuracy is limited by completeness of underlying biotransformation rule databases (mammalian CYP450 reactions, Phase II conjugations, gut microbiota biotransformations, EAWAG BBD reactions); novel or rare transformations may not be captured
- For environmental microbial degradation, all aerobic and anaerobic reactions are reported by default; filtering by ecologically relevant conditions requires manual post-processing

## Evidence

- [readme] BioTransformer predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota."
- [other] BioTransformer assists metabolite identification by leveraging metabolism predictions as basis for candidate structure assignment: "BioTransformer assists scientists in metabolite identification, based on the metabolism prediction."
- [readme] Environmental degradation module uses EAWAG biotransformation rules and reaction templates: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database"
- [other] Predicted metabolites are ranked and matched to observed features using structural similarity or mass alignment: "Match predicted structures against observed spectral/chromatographic features or provided experimental compound lists using structural similarity or mass-to-charge alignment."
- [readme] Input formats and output control parameters specified in README: "Read the input as a single molecule in SMILES format... Save the results into the specified CSV file... Save the results into the specified SDF file"
