---
name: environmental-microbial-metabolism-prediction
description: Use when you have a small molecule structure (SMILES, MOL, or SDF format)
  and need to understand how soil or aquatic microbiota would metabolize it.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0621
  tools:
  - BioTransformer
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

# environmental-microbial-metabolism-prediction

## Summary

Predict soil and aquatic microbial degradation pathways for a small molecule by querying BioTransformer's environmental microbial degradation module against EAWAG's biodegradation database. Use this skill to generate predicted metabolites, identify transformation rules applied, and trace degradation pathways for environmental fate assessment.

## When to use

Apply this skill when you have a small molecule structure (SMILES, MOL, or SDF format) and need to understand how soil or aquatic microbiota would metabolize it. Typical triggers: environmental risk assessment, predicting pollutant or xenobiotic degradation, identifying metabolite structures for environmental monitoring, or validating degradation pathways in contaminated ecosystems.

## When NOT to use

- Input is a mammalian or gut microbiota metabolism prediction task — use BioTransformer's mammalian or gut microbiota modules instead.
- The small molecule lacks sufficient structural information or is provided in an unsupported format (e.g. plain text name, IUPAC string without stereochemistry).
- The target environment is not soil or aquatic microbiota (e.g., clinical infections, fermentation cultures, or specialized engineered systems not covered by EAWAG-BBD).

## Inputs

- Small-molecule structure (SMILES string)
- Small-molecule structure (MOL file)
- Small-molecule structure (SDF file)

## Outputs

- Predicted metabolite structures (chemical structures of degradation products)
- Transformation rules applied (biotransformation steps linking parent to metabolite)
- Degradation pathway information (ordered sequence of transformations)
- Structured output file (list of predicted metabolites with annotations)

## How to apply

Load the small-molecule structure into BioTransformer in SMILES, MOL, or SDF format. Execute the environmental microbial degradation module, which queries EAWAG-BBD and EnviPath metabolic transformation data to generate predictions. Retrieve the structured output listing all predicted metabolites with their chemical structures and transformation rule annotations. Validate the results by checking that each predicted metabolite includes a transformation rule and parent–child relationship traceable to known biodegradation pathways in the EAWAG database.

## Related tools

- **BioTransformer** (Core tool that executes environmental microbial degradation module to query EAWAG-BBD and EnviPath and predict soil/aquatic microbiota metabolism for the input small molecule.) — bitbucket.org/wishartlab/biotransformer

## Evaluation signals

- All predicted metabolites include a valid transformation rule linking them to their parent compound or intermediate.
- Degradation pathway can be traced step-by-step from the input molecule to all terminal metabolites.
- Each predicted metabolite structure is chemically plausible (e.g., follows mass-balance and known biotransformation patterns such as oxidation, conjugation, or cleavage).
- Output is a structured file (e.g., CSV, JSON, or tabular format) with columns for parent molecule ID, predicted metabolite structure, transformation rule, and pathway step number.
- Predictions align with known biodegradation records in EAWAG-BBD for chemically similar parent compounds when available as a validation reference.

## Limitations

- Predictions depend on coverage and accuracy of EAWAG-BBD and EnviPath; novel or poorly-characterized biotransformation pathways may be missed.
- Environmental degradation predictions are community-level and do not account for site-specific factors (pH, temperature, redox state, nutrient availability, or specific microbial consortia composition).
- No changelog or version history of the database or transformation rules is publicly available, making it difficult to track changes to predictions over time.
- Predictions are for environmental microbial metabolism only; results do not predict human pharmacokinetics, toxicity, or bioaccumulation.

## Evidence

- [intro] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database"
- [other] Load input; execute module; retrieve metabolites with structures and transformations: "1. Load the input small-molecule structure (SMILES, MOL, or SDF format) into BioTransformer. 2. Execute BioTransformer's environmental microbial degradation module, which queries EAWAG-BBD and"
- [intro] BioTransformer predicts small molecule metabolism in soil/aquatic microbiota: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota"
- [intro] BioTransformer assists in metabolite identification based on metabolism prediction: "BioTransformer also assists scientists in metabolite identification, based on the metabolism prediction"
