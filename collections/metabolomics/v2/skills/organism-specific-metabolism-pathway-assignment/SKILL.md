---
name: organism-specific-metabolism-pathway-assignment
description: Use when you have observed metabolites (from LC-MS/MS, chromatography,
  or spectroscopy) whose identities are unknown, and you wish to constrain the candidate
  pool by leveraging organism-specific metabolism predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3656
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0602
  tools:
  - BioTransformer
  - PubChem
  - EAWAG Biodegradation and Biocatalysis Database
  techniques:
  - LC-MS
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

# organism-specific-metabolism-pathway-assignment

## Summary

This skill uses BioTransformer to predict small molecule metabolism pathways in a specified biological context (mammals, gut microbiota, or soil/aquatic microbiota) and assign candidate metabolite structures to experimentally observed compounds by matching predicted structures against observed spectral or mass features.

## When to use

Apply this skill when you have observed metabolites (from LC-MS/MS, chromatography, or spectroscopy) whose identities are unknown, and you wish to constrain the candidate pool by leveraging organism-specific metabolism predictions. Use it especially when the parent compound is known and metabolite production is suspected in a particular microbiota context (human gut, environmental).

## When NOT to use

- The parent compound is already a predicted metabolite or intermediate product without known precursor — focus on forward prediction, not retroactive organism assignment.
- Observed metabolites have no clear mass or structural similarity to any BioTransformer-predicted products at the specified mass tolerance — consider relaxing tolerance or expanding the organism context.
- The compound is a xenobiotic or drug with proprietary metabolism not covered by mammalian, gut, or environmental databases — environmental microbial module requires explicit EAWAG BBD/PPS data licensing for commercial use.

## Inputs

- parent compound in SMILES format
- parent compound in MOL file format
- parent compound in SDF file format
- observed compound masses (whitespace-separated list in Da)
- observed metabolite structures or spectral features
- target organism identifier (mammals, hgut, envimicro)

## Outputs

- CSV table with metabolite identities, predicted structures, match scores, and organism context
- SDF file with predicted metabolites annotated with PubChem CID and synonyms (optional)
- ranked list of candidate metabolite identities for observed compounds
- metabolism pathway diagram showing parent-to-metabolite transformations

## How to apply

First, initialize BioTransformer 3.0.0 for your target organism context (mammals, hgut, or envimicro). Input the parent compound as SMILES, MOL, or SDF format, and generate predicted metabolite structures using the appropriate biotransformer module (e.g., 'allHuman' for human super transformer, 'hgut' for human gut microbial). Rank predicted metabolites by reaction likelihood score. Then match predicted structures against observed compounds by comparing mass-to-charge ratios (m/z) or structural similarity, applying a mass tolerance (default 0.01 Da). Assign the best-matching predicted metabolite as a candidate identity to each observed compound, recording the match score and organism context. Output results as a structured table (CSV or SDF) with metabolite names, predicted structures, match scores, and organism provenance.

## Related tools

- **BioTransformer** (predicts small molecule metabolism pathways in organism-specific contexts and assists in metabolite identification by assigning candidate structures to observed compounds) — https://github.com/Wishartlab-openscience/Biotransformer
- **PubChem** (annotates predicted metabolites with chemical identifiers (CID) and synonyms for structural validation)
- **EAWAG Biodegradation and Biocatalysis Database** (provides environmental microbial degradation reaction data used by BioTransformer's envimicro module)

## Examples

```
java -jar biotransformer-3.0.0.jar -k cid -b allHuman -ismi "O[C@@H]1CC2=C(O)C=C(O)C=C2O[C@@H]1C1=CC=C(O)C(O)=C1" -osdf output.sdf -s 2 -m "292.0946;304.0946" -t 0.01 -a
```

## Evaluation signals

- Predicted metabolite structures match observed m/z values within the specified mass tolerance (default ≤ 0.01 Da)
- Match scores (structural similarity or likelihood ranking) are reported for each assigned metabolite identity; high-confidence assignments cluster near the top of the ranking
- Output table includes organism context (e.g., 'allHuman', 'hgut', 'envimicro') consistent with the input biotransformer type, confirming organism-specific prediction was applied
- Predicted metabolites are chemically plausible transformations of the parent (e.g., oxidation, conjugation, reduction) according to the selected biotransformer rules (EC-based, CYP450, Phase II, or environmental microbial)
- CSV or SDF output is machine-readable and conforms to the expected schema (columns: parent ID, metabolite name, structure, match score, organism, transformation rules applied)

## Limitations

- BioTransformer's environmental microbial degradation module uses EAWAG data licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0; commercial use requires explicit license from EnviPath.
- Prediction accuracy is constrained by the completeness and currency of the underlying reaction databases (EC reactions, CYP450 rules, Phase II conjugation rules, and EAWAG BBD/PPS). Novel or rare biotransformations not in these databases will not be predicted.
- Mass tolerance (default 0.01 Da) may be too strict for low-resolution or nominal-mass instruments; users must manually adjust -t parameter if needed. Conversely, loose tolerance risks spurious matches.
- Organism-specific predictions assume the parent compound is metabolized in that organism; if metabolite is produced via a pathway not encoded in BioTransformer (e.g., strain-specific enzyme, spontaneous degradation), assignment will fail.
- Output annotation with PubChem (-a flag) depends on PubChem availability; if a predicted metabolite lacks a PubChem entry, annotation will be incomplete.

## Evidence

- [readme] BioTransformer version 3.0.0 … predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota: "BioTransformer is a software tool that predicts small molecule metabolism in mammals, their gut microbiota, as well as the soil/aquatic microbiota"
- [readme] metabolite identification based on metabolism prediction: "BioTransformer also assists scientists in metabolite identification, based on the metabolism prediction"
- [other] BioTransformer assists metabolite identification by leveraging metabolism predictions for candidate structure assignment: "BioTransformer assists scientists in metabolite identification by leveraging its metabolism predictions as the basis for candidate structure assignment to observed compounds"
- [other] workflow describes loading version 3.0.0, initializing module, generating structures, ranking by probability, and matching against experimental features: "Load BioTransformer version 3.0.0 and initialize the metabolism prediction module for the target organism(s) (mammals, gut microbiota, or soil/aquatic microbiota). 2. Input the parent compound(s) and"
- [readme] database source for environmental microbial module: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database"
- [readme] licensing requirement for commercial use of environmental module: "To use the environmental microbial module for commercial purposes, users must request an appropriate commercial license from EnviPath"
- [readme] example of metabolite identification with masses and tolerance: "Identify all human metabolites (max depth = 2) of Epicatechin … with masses 292.0946 Da and 304.0946 Da, with a mass tolerance of 0.01 Da"
- [other] output format specification for metabolite identification task: "generate a structured output table with metabolite names, predicted structures, match scores, and organism context"
