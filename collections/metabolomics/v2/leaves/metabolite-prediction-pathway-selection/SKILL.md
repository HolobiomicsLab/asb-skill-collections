---
name: metabolite-prediction-pathway-selection
description: Use when when you have a small-molecule structure (SMILES, MOL, or SDF
  format) and need to predict its metabolic fate across one or more biological systems.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3938
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0154
  tools:
  - BioTransformer
  - EAWAG's Biodegradation and Biocatalysis Database
  - PubChem
  techniques:
  - NMR
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab). Env. module data CC-BY-NC-SA (enviPath/EAWAG).
    url: https://bitbucket.org/wishartlab/biotransformer.git
  license_tier: noncommercial
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

# metabolite-prediction-pathway-selection

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Use BioTransformer 3.0.0 to predict small-molecule metabolism by selecting the appropriate biological system module (mammalian, gut microbiota, or soil/aquatic microbiota) and executing prediction workflows on prepared molecular structures. This skill enables systematic exploration of how a compound is metabolized across different biological contexts.

## When to use

When you have a small-molecule structure (SMILES, MOL, or SDF format) and need to predict its metabolic fate across one or more biological systems. Apply this skill when your research question focuses on which metabolites are produced, what reaction types transform the parent compound, or how metabolic pathways differ between mammals and environmental microbiota.

## When NOT to use

- Input is a protein or macromolecule; BioTransformer is designed only for small-molecule metabolism.
- Your goal is to identify an unknown metabolite from experimental mass spectrometry or NMR data alone; use the compound identification task (-k cid) with target masses instead.
- You require commercial use of environmental microbial degradation predictions without an EnviPath commercial license; the EAWAG database is restricted to non-commercial use.

## Inputs

- small-molecule structure in SMILES format (string)
- small-molecule structure in MOL format (file)
- small-molecule structures in SDF format (file)

## Outputs

- predicted metabolite structures (SDF format by default)
- predicted metabolite structures and metadata (CSV format)
- reaction types applied during each biotransformation step
- metabolic pathway information linking parent to metabolites

## How to apply

Prepare the input small molecule in SMILES, MOL, or SDF format. Select the appropriate BioTransformer module based on your biological context of interest: 'superbio' or 'allHuman' for mammalian metabolism, 'hgut' for human gut microbiota, or 'envimicro' for soil/aquatic microbiota. Execute BioTransformer with the specified module, optionally setting the number of transformation steps (default 1) and output format (SDF or CSV). Collect the prediction output, which reports predicted metabolite structures, reaction types (oxidation, reduction, conjugation, etc.), and the metabolic pathway information. For mammalian CYP450 predictions, consider specifying the CYP450 mode (1=CypReact + rules, 2=CyProduct only, 3=combined) to control prediction strategy.

## Related tools

- **BioTransformer** (primary executable for predicting small-molecule metabolism across mammalian, gut microbial, and environmental microbial pathways) — https://github.com/Wishartlab-openscience/Biotransformer
- **EAWAG's Biodegradation and Biocatalysis Database** (underlying data source for environmental microbial degradation module reactions)
- **PubChem** (optional annotation source for metabolite names, synonyms, and compound IDs when -a flag is used)

## Examples

```
java -jar biotransformer-3.0.0.jar -k pred -b allHuman -ismi "CC(C)C1=CC=C(C)C=C1O" -ocsv output.csv -s 2 -cm 3
```

## Evaluation signals

- Output SDF or CSV file is non-empty and contains predicted metabolite structures with valid molecular geometry.
- Predicted metabolites have molecular mass changes consistent with declared reaction types (e.g., oxidation increases mass by ~15.9949 Da for mono-oxygenation, conjugation increases mass by added moiety).
- Metabolic pathway depth matches the requested number of steps (-s parameter); pathways show parent → metabolite → secondary metabolite chains of expected length.
- Reaction type annotations (oxidation, reduction, conjugation, deconjugation) are assigned to each transformation step with chemical plausibility.
- When using compound identification mode (-k cid) with target masses, identified metabolites fall within the specified mass tolerance (default 0.01 Da).

## Limitations

- BioTransformer predicts metabolism only for small molecules; macromolecules, proteins, and polymers are out of scope.
- Environmental microbial predictions are restricted to non-commercial use without EnviPath commercial license; all aerobic and anaerobic reactions are reported rather than only aerobic transformations.
- Predictions are rule-based and data-driven; novel or rare metabolic transformations not present in training data or reaction rules may not be captured.
- No changelog is provided in the README, making it difficult to assess differences from earlier versions or known fixes.
- The 'allHuman' mode reports all possible metabolites from any applicable reaction at each step, which can generate large combinatorial solution spaces; step depth and mode choice impact computational burden.

## Evidence

- [readme] BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota.: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota"
- [other] Prepare input small molecules in a supported format (SMILES, MOL, or SDF) and execute with appropriate module selection.: "Prepare input small molecules in a supported format (SMILES, MOL, or SDF). Execute BioTransformer 3.0.0 with the appropriate metabolic module selection (mammalian, gut microbiota, or soil/aquatic"
- [other] Output contains predicted metabolite structures, reaction types, and metabolic pathway information.: "Collect the tool's standard prediction output containing predicted metabolite structures, reaction types, and metabolic pathway information."
- [readme] Environmental module uses EAWAG's database which is licensed under Creative Commons Attribution-NonCommercial-ShareAlike.: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database, which is licensed by EnviPath under the Creative Commons"
- [readme] CYP450 mode parameter controls prediction strategy between three modes.: "CYP450 prediction Mode here: 1) CypReact + BioTransformer rules; 2) CyProduct only; 3) Combined: CypReact + BioTransformer rules + CyProducts. Default mode is 1."
- [readme] Default transformation step count and customization option.: "The number of steps for the prediction. This option can be set by the user for the EC-based, CYP450, Phase II, and Environmental microbial biotransformers. The default value is 1."
