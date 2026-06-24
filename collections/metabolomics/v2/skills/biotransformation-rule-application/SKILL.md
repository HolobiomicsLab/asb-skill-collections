---
name: biotransformation-rule-application
description: Use when when you have a small-molecule structure (SMILES, MOL, or SDF
  format) and need to predict its fate in soil or aquatic environments through microbial
  degradation pathways.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - BioTransformer
  - EAWAG Biodegradation and Biocatalysis Database
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

# biotransformation-rule-application

## Summary

Apply curated biotransformation rules from EAWAG's Biodegradation and Biocatalysis Database to predict metabolite structures and pathways for small molecules undergoing environmental microbial degradation. This skill enables scientists to map input chemical structures to predicted soil and aquatic microbial metabolites using enzyme reaction rules.

## When to use

When you have a small-molecule structure (SMILES, MOL, or SDF format) and need to predict its fate in soil or aquatic environments through microbial degradation pathways. Applicable when biotransformation rules from EAWAG/EnviPath are the appropriate knowledge source for your environmental compartment (aerobic and anaerobic soil/aquatic microbial degradation).

## When NOT to use

- Input is a mammalian metabolism prediction problem — use the 'superbio' or 'allHuman' options instead of 'envimicro'.
- Input is a human gut microbiota degradation prediction — use the 'hgut' biotransformer option instead.
- You require only Phase II conjugation or CYP450 metabolism — these are separate BioTransformer modules not specific to environmental microbial degradation.

## Inputs

- Small-molecule structure in SMILES format
- Small-molecule structure in MOL format
- SDF file containing one or more small-molecule structures

## Outputs

- Predicted metabolite structures (SDF format by default)
- Biotransformation rules applied to each prediction step
- Metabolism pathway showing parent → metabolite transformations
- Optional: CSV-formatted results with PubChem CID and synonyms
- Optional: Annotated metabolite names and database identifiers

## How to apply

Load the input small-molecule structure into BioTransformer in SMILES, MOL, or SDF format. Select the 'envimicro' biotransformer option, which invokes biotransformation rules derived from the EAWAG Biodegradation and Biocatalysis Database. Specify the number of transformation steps (default 1; configurable via -s parameter) to control metabolite prediction depth. Execute the prediction task (-k pred) to generate predicted metabolite structures and their associated biotransformation rules. Export results in SDF or CSV format with optional PubChem annotation (-a flag) for metabolite identification. For commercial applications, users must obtain a separate license from EnviPath, as the database is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.

## Related tools

- **BioTransformer** (Core tool executing biotransformation rule application via environmental microbial degradation module (envimicro option)) — https://github.com/Wishartlab-openscience/Biotransformer
- **EAWAG Biodegradation and Biocatalysis Database** (Source of biotransformation rules and reaction knowledge base used by BioTransformer's environmental microbial degradation module) — https://envipath.com/license/

## Examples

```
java -jar biotransformer-3.0.0.jar -k pred -b envimicro -ismi "CC(C)C1=CC=C(C)C=C1O" -osdf output.sdf -s 2 -a
```

## Evaluation signals

- Output metabolite structures are valid chemical structures (parseable SMILES/MOL formats with correct valence and chirality).
- Each predicted metabolite is chemically reachable from the parent structure via at least one biotransformation rule encoded in the EAWAG database.
- Metabolite molecular weight and formula changes are consistent with the reported transformation rules (e.g., hydroxylation adds 16 Da, deamination removes 16 Da).
- All aerobic and anaerobic reactions are reported in the output (per BioTransformer's environmental microbial mode, which differs from EAWAG BBD/PPS default).
- Results are reproducible across multiple runs with identical input structure and step count.

## Limitations

- Environmental microbial degradation module data is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International; commercial use requires explicit license from EnviPath.
- Predictions are limited to biotransformation rules in the EAWAG database; degradation pathways absent from EAWAG may not be predicted.
- Predictions assume standard soil/aquatic microbial communities; site-specific or specialized microbial consortia may exhibit different degradation patterns.
- No changelog provided in the README; version history and rule updates are not documented.
- Prediction accuracy depends on biotransformation rule completeness and may miss novel degradation pathways not yet characterized in EAWAG.

## Evidence

- [readme] Database source and licensing: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database, which is licensed by EnviPath under the Creative Commons"
- [readme] Prediction scope and capability: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota"
- [readme] Environmental microbial module behavior: "For the environmental microbial biodegradation, all reactions (aerobic and anaerobic) are reported, and not only the aerobic biotransformations (as per default in the EAWAG BBD/PPS system)"
- [readme] Input and output formats: "Read the input as a single molecule in SMILES format, Read the input as a single molecule in the specified MOL format, Read the input from the specified SDF format"
- [other] Workflow steps and rule application: "Execute BioTransformer's soil/aquatic microbiota degradation prediction module, which applies biotransformation rules derived from the EAWAG Biodegradation and Biocatalysis Database to generate"
