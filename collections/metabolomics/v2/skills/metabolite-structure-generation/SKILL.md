---
name: metabolite-structure-generation
description: Use when you have a small-molecule structure (SMILES, MOL, or SDF format)
  and need to predict its metabolic fate in a specific biological context (mammalian
  phase I/II metabolism, human gut microbiota, or soil/aquatic microbial degradation).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - BioTransformer
  - EAWAG Biodegradation and Biocatalysis Database
  - PubChem
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab). Env. module data CC-BY-NC-SA (enviPath/EAWAG).
    url: https://bitbucket.org/wishartlab/biotransformer3.0jar.git
derived_from:
- doi: 10.1093/nar/gkac408
  title: BioTransformer 3.0
evidence_spans:
- This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that
  predicts small molecule metabolism
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biotransformer_3_0_cq
    doi: 10.1093/nar/gkac408
    title: BioTransformer 3.0
  dedup_kept_from: coll_biotransformer_3_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/nar/gkac408
  all_source_dois:
  - 10.1093/nar/gkac408
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-structure-generation

## Summary

Predict small-molecule metabolite structures by applying biotransformation rules from curated databases (EAWAG, CYP450, Phase II) to an input compound. This skill generates predicted metabolite structures and their associated transformation pathways, enabling downstream metabolite identification and pathway analysis.

## When to use

Use this skill when you have a small-molecule structure (SMILES, MOL, or SDF format) and need to predict its metabolic fate in a specific biological context (mammalian phase I/II metabolism, human gut microbiota, or soil/aquatic microbial degradation). Particularly valuable when you seek to identify putative metabolites before experimental confirmation or to explore biotransformation pathways under defined biotransformer types (EC-based, CYP450, Phase II, human gut microbial, or environmental microbial).

## When NOT to use

- Input is already an experimentally confirmed metabolite — use this skill for prediction, not validation.
- You require species-specific or strain-level metabolic predictions beyond the supported biotransformer types (mammalian, gut microbial, soil/aquatic microbial).
- The input molecule is a macromolecule (protein, nucleic acid, polysaccharide) or a complex natural product outside the scope of small-molecule biotransformation rule databases.

## Inputs

- Small-molecule structure in SMILES format
- Small-molecule structure in MOL format
- Batch of small-molecule structures in SDF format

## Outputs

- Predicted metabolite structures (SDF format, default)
- Predicted metabolite structures with PubChem CID and synonyms (SDF or CSV)
- Metabolism pathway(s) with intermediate and final metabolites
- CSV table of metabolites with associated biotransformation rules

## How to apply

Load the input molecule in SMILES, MOL, or SDF format into BioTransformer and select the appropriate biotransformer type (ecbased, cyp450, phaseII, hgut, superbio/allHuman, or envimicro) based on the biological context of interest. Specify the number of transformation steps (default 1; configurable up to multi-step predictions). For CYP450 predictions, optionally select the CYP450 mode (1=CypReact + BioTransformer rules; 2=CyProduct only; 3=Combined). BioTransformer applies biotransformation rules derived from its curated rule bases to generate predicted metabolite structures. Output metabolites as SDF (default), CSV, or with PubChem annotation. The rationale is that biotransformation rules encode recurring reaction patterns observed in biochemical databases, enabling systematic prediction of plausible products without expensive experimental screening.

## Related tools

- **BioTransformer** (Executes biotransformation rule-based prediction of small-molecule metabolite structures across mammalian, gut microbial, and environmental microbial contexts) — https://github.com/Wishartlab-openscience/Biotransformer
- **EAWAG Biodegradation and Biocatalysis Database** (Source of biotransformation rules for environmental microbial degradation module)
- **PubChem** (Optional annotation database for matching predicted metabolites to known compounds and retrieving chemical identifiers and synonyms)

## Examples

```
java -jar biotransformer-3.0.0.jar -k pred -b envimicro -ismi "CC(C)C1=CC=C(C)C=C1O" -osdf output.sdf -s 2 -a
```

## Evaluation signals

- Output SDF/CSV file contains valid chemical structures (no parse errors; all SMILES/InChI convertible to molecular graphs).
- Number of predicted metabolites grows monotonically with the number of transformation steps (or remains constant if no further transformations are possible).
- Each predicted metabolite has an associated biotransformation rule or reaction type (e.g., oxidation, conjugation, deconjugation) documented in the output.
- For annotated outputs, PubChem annotation retrieval succeeds for predicted structures matching known compounds; confidence or mass tolerance thresholds are documented.
- Predicted metabolites match the expected biotransformer type (e.g., CYP450 predictions should include oxidation products; phaseII should include conjugates; envimicro may include anaerobic cleavage products).

## Limitations

- Environmental microbial degradation module output (from EAWAG database) is licensed CC-BY-NC-SA 4.0; commercial use requires explicit license from EnviPath.
- BioTransformer predicts plausible metabolites based on biotransformation rule databases but does not guarantee metabolite formation in vivo; predictions require experimental validation.
- Biotransformation rules are derived from curated databases and may not capture novel or rare metabolic pathways absent from training data.
- Multi-step predictions can generate combinatorial explosion of metabolites; practical limits depend on molecule complexity and step count.
- The 'superbio' option runs transformations in a pre-defined order (e.g., deconjugation first, then oxidation/reduction); 'allHuman' predicts all possible reactions at each step, yielding different output sets.

## Evidence

- [other] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database to perform soil/aquatic microbial degradation predictions on small molecules.: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database to perform soil/aquatic microbial degradation predictions on small"
- [readme] BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota.: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota"
- [other] Execute BioTransformer's soil/aquatic microbiota degradation prediction module, which applies biotransformation rules derived from the EAWAG Biodegradation and Biocatalysis Database to generate predicted metabolite structures and transformations.: "Execute BioTransformer's soil/aquatic microbiota degradation prediction module, which applies biotransformation rules derived from the EAWAG Biodegradation and Biocatalysis Database to generate"
- [readme] For the CYP450 prediction mode, the user can select 1) CypReact + BioTransformer rules; 2) CyProduct only; 3) Combined: CypReact + BioTransformer rules + CyProducts.: "CYP450 prediction Mode here: 1) CypReact + BioTransformer rules; 2) CyProduct only; 3) Combined: CypReact + BioTransformer rules + CyProducts"
- [readme] The environmental microbial biodegradation module reports all reactions (aerobic and anaerobic), not only the aerobic biotransformations (as per default in the EAWAG BBD/PPS system).: "For the environmental microbial biodegradation, all reactions (aerobic and anaerobic) are reported, and not only the aerobic biotransformations (as per default in the EAWAG BBD/PPS system)"
- [readme] BioTransformer's environmental microbial degradation module data is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International; commercial use requires explicit license from EnviPath.: "To use the environmental microbial degradation module for commercial purposes, users must request an appropriate commercial license from EnviPath"
