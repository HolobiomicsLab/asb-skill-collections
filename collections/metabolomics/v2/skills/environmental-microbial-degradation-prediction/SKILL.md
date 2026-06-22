---
name: environmental-microbial-degradation-prediction
description: Use when you have a small-molecule structure (in SMILES, MOL, or SDF format) and need to predict how soil or aquatic microbiota will degrade or biotransform it, particularly for environmental risk assessment, metabolite identification in biodegradation studies, or tracing microbial transformation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3938
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_2814
  - http://edamontology.org/topic_0154
  tools:
  - BioTransformer
  - EAWAG Biodegradation and Biocatalysis Database
  - EnviPath
derived_from:
- doi: 10.1093/nar/gkac408
  title: BioTransformer 3.0
evidence_spans:
- This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that predicts small molecule metabolism
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

# environmental-microbial-degradation-prediction

## Summary

Predict soil and aquatic microbial metabolite structures and biotransformation pathways for small molecules using BioTransformer's environmental microbial degradation module, which applies EAWAG Biodegradation and Biocatalysis Database rules to generate predicted degradation products and their associated transformations.

## When to use

Use this skill when you have a small-molecule structure (in SMILES, MOL, or SDF format) and need to predict how soil or aquatic microbiota will degrade or biotransform it, particularly for environmental risk assessment, metabolite identification in biodegradation studies, or tracing microbial transformation pathways in anaerobic and aerobic conditions.

## When NOT to use

- Input molecule is a complex biopolymer or protein — BioTransformer is designed for small molecules only
- Prediction is needed for human or mammalian metabolism specifically — use the CYP450, Phase II, or human super-transformer options instead
- Commercial use of environmental microbial predictions without an appropriate EnviPath commercial license from EnviPath; the environmental module data is licensed under CC-BY-NC-SA 4.0

## Inputs

- Small-molecule structure in SMILES format (string)
- Small-molecule structure in MOL file format
- Small-molecule structures in SDF (structure data file) format

## Outputs

- Predicted metabolite structures in SDF format (default)
- Predicted metabolite structures and metadata in CSV format
- Biotransformation rules and reaction types associated with each metabolite
- Metabolism pathway diagrams (optional with annotation flag)

## How to apply

Load the input small-molecule structure into BioTransformer using the `-b envimicro` biotransformer option, specify the number of transformation steps with `-s` (default 1), and select the input format flag (`-ismi` for SMILES, `-imol` for MOL, or `-isdf` for SDF). Execute the prediction task with `-k pred`, which applies biotransformation rules from the EAWAG database to generate predicted metabolite structures. Output results to SDF (default) or CSV format using `-osdf` or `-ocsv` flags. The module reports both aerobic and anaerobic reactions by default, unlike the EAWAG BBD/PPS system which reports only aerobic transformations.

## Related tools

- **BioTransformer** (Executes environmental microbial degradation prediction using EAWAG biotransformation rules to generate predicted metabolite structures and pathways) — https://github.com/Wishartlab-openscience/Biotransformer
- **EAWAG Biodegradation and Biocatalysis Database** (Source dataset providing biotransformation rules and microbial degradation knowledge for soil and aquatic microbiota)
- **EnviPath** (Licensing and distribution source for EAWAG database data; contains additional visualization and curation tools) — https://envipath.org/

## Examples

```
java -jar biotransformer-3.0.0.jar -k pred -b envimicro -ismi "CC(C)C1=CC=C(C)C=C1O" -osdf thymol_degradation.sdf -s 2
```

## Evaluation signals

- Output metabolite structures are valid chemical compounds (parseable by cheminformatics libraries; SMILES/InChI can be generated without error)
- All predicted metabolites are chemically feasible transformations of the input molecule (mass balance preserved; functional group changes correspond to known biotransformation reactions)
- Biotransformation rules are explicitly traced to EAWAG database entries and reaction type classifications (oxidation, reduction, hydrolysis, conjugation, deconjugation, etc.)
- Number of metabolites and depth of pathway matches the `-s` parameter; pathway does not exceed specified step count
- For multi-step predictions, downstream metabolites are derived from upstream products, forming a coherent acyclic transformation graph

## Limitations

- Environmental module predictions include both aerobic and anaerobic reactions by default; users cannot filter to aerobic-only transformations (unlike the EAWAG BBD/PPS system default behavior)
- Predictions are rule-based and do not account for environmental factors such as pH, temperature, oxygen availability, microbial community composition, or bioavailability
- EAWAG database coverage is biased toward chemicals of environmental concern and industrially relevant compounds; predictions for novel or rare structures may be limited or absent
- Commercial use requires a separate license from EnviPath; non-commercial academic and research use requires proper citation of the EnviPath paper and acknowledgment of the CC-BY-NC-SA 4.0 license

## Evidence

- [intro] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database"
- [other] Applies biotransformation rules to generate predicted metabolite structures and transformations: "Execute BioTransformer's soil/aquatic microbiota degradation prediction module, which applies biotransformation rules derived from the EAWAG Biodegradation and Biocatalysis Database to generate"
- [readme] Environmental microbial biotransformer option and step configuration: "Environmental microbial (envimicro)*. ... -s,--nsteps <Number of steps> The number of steps for the prediction. This option can be set by the user for the EC-based, CYP450, Phase II, and"
- [readme] All reactions (aerobic and anaerobic) are reported by default: "For the environmental microbial biodegradation, all reactions (aerobic and anaerobic) are reported, and not only the aerobic biotransformations (as per default in the EAWAG BBD/PPS system)"
- [readme] Commercial license requirement for environmental microbial module: "To use the environmental microbial module for commercial purposes, users must request an appropriate commercial license from EnviPath"
