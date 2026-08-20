---
name: soil-aquatic-microbiota-pathway-simulation
description: Use when when you have a small molecule (SMILES, MOL, or SDF format)
  and need to predict its degradation products in soil or aquatic microbial ecosystems;
  when environmental risk assessment, persistence prediction, or metabolite identification
  in these compartments is required;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_2269
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_3407
  tools:
  - BioTransformer
  - EAWAG's Biodegradation and Biocatalysis Database
  - EnviPath
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

# soil-aquatic-microbiota-pathway-simulation

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Simulate biotransformation pathways of small molecules in soil and aquatic microbial communities by applying EAWAG-derived biotransformation rules to predict environmental degradation metabolites. Use this skill when you need to predict soil/aquatic microbial metabolites of xenobiotics, pesticides, or environmental contaminants for risk assessment or biodegradation pathway elucidation.

## When to use

When you have a small molecule (SMILES, MOL, or SDF format) and need to predict its degradation products in soil or aquatic microbial ecosystems; when environmental risk assessment, persistence prediction, or metabolite identification in these compartments is required; when you need to explore multi-step aerobic and anaerobic biotransformation pathways at user-defined depth (number of steps).

## When NOT to use

- Input is a mammalian or human gut microbial substrate—use the allHuman, superbio, cyp450, phaseII, or hgut biotransformer options instead.
- You require only mammalian Phase I or Phase II conjugation predictions without environmental degradation context.
- Input molecules are proteins, polymers, or other macromolecules; BioTransformer operates only on small molecule chemical structures.

## Inputs

- SMILES string (single molecule)
- MOL file (single molecule structure)
- SDF file (multiple molecule structures)

## Outputs

- SDF file (default) containing predicted metabolites with reaction metadata
- CSV file (optional) with metabolite structures, masses, and transformation steps
- Biotransformation pathway trees showing parent → metabolite relationships

## How to apply

Execute BioTransformer with the environmental microbial degradation module (-b envimicro) on your input molecule(s) in SMILES, MOL, or SDF format, specifying the number of transformation steps (-s parameter, default 1) to simulate pathway depth. The tool applies structured biotransformation rules (SMARTS patterns and reaction templates) extracted from EAWAG's Biodegradation and Biocatalysis Database to perform substructure matching and reaction template expansion, generating predicted intermediate and final metabolite structures. By default, all reactions (aerobic and anaerobic) are reported—not only aerobic as in the native EAWAG system. Validate the predicted metabolite set by comparing output structures, biotransformation pathways, and molecular properties (mass, logP) against reference biotransformations in EAWAG or literature. Output can be saved as SDF (default) or CSV format with optional PubChem annotation (-a flag).

## Related tools

- **BioTransformer** (Core software tool that implements the environmental microbial degradation module, applies EAWAG biotransformation rules via substructure matching and reaction template expansion, and generates predicted metabolite structures and pathways) — https://github.com/Wishartlab-openscience/Biotransformer
- **EAWAG's Biodegradation and Biocatalysis Database** (Source database providing the biotransformation rules, reaction types, enzyme families, substrate patterns, and product templates used by BioTransformer's environmental microbial degradation module)
- **EnviPath** (Data provider and licensing authority for EAWAG BBD; hosts the database and manages commercial licensing for non-academic use of the environmental microbial module) — https://envipath.org/

## Examples

```
java -jar biotransformer-3.0.0.jar -k pred -b envimicro -ismi "CCNC1=NC(=NC(=N1)Cl)NC(C)C" -osdf atrazine-envimicro-metabolites.sdf -s 2 -a
```

## Evaluation signals

- Predicted metabolite structures are chemically plausible: molecular weight change is consistent with known biotransformation rules (e.g., oxidation +16 Da, conjugation with typical groups); no impossible bond configurations or valence violations present in SDF or CSV output.
- Pathway depth matches the specified number of steps (-s parameter): e.g., -s 2 should show parent → step 1 metabolites → step 2 metabolites in the output tree.
- All predicted metabolites can be cross-referenced against EAWAG BBD or published literature: reported biotransformation pathways and metabolite masses match known environmental degradation data for the input substrate.
- Molecular properties (logP, mass) of predicted metabolites are consistent with the parent compound: progressive changes in hydrophobicity or mass align with stated biotransformation rules.
- Output includes both aerobic and anaerobic reactions (not filtered to aerobic-only as in native EAWAG system) when envimicro module is used, confirming full pathway exploration.

## Limitations

- Environmental microbial degradation predictions are restricted by the scope and completeness of EAWAG's Biodegradation and Biocatalysis Database; novel or poorly characterized degradation pathways may not be captured.
- The envimicro module uses data licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International; commercial use requires explicit permission and a separate license from EnviPath.
- BioTransformer applies rules deterministically based on substructure matching; it does not account for organism-specific metabolic capacity, environmental conditions (pH, temperature, oxygen gradient), or bioavailability that influence real-world degradation rates or pathway preference.
- Multi-step predictions can produce combinatorially large metabolite sets; execution time and output size grow with step depth (-s parameter); users should validate results are not spurious artifacts of over-prediction at high step counts.

## Evidence

- [readme] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database, which is licensed by EnviPath"
- [other] Biotransformation rules from EAWAG are extracted and applied via substructure matching and reaction template expansion: "Retrieve the EAWAG Biodegradation and Biocatalysis Database records and extract biotransformation rules (reaction types, enzyme families, substrate patterns, product templates)"
- [other] Rule application engine performs substructure matching and generates predicted metabolite structures: "Implement the rule application engine in BioTransformer that applies the extracted biotransformation rules to input substrate molecules using substructure matching and reaction template expansion"
- [other] Validation involves comparing output structures and properties against EAWAG or literature references: "Validate the predicted metabolite set by comparing output structures, biotransformation pathways, and molecular properties (mass, logP, etc.) against reference biotransformations documented in EAWAG"
- [readme] Both aerobic and anaerobic reactions are reported by envimicro module, not just aerobic: "For the environmental microbial biodegradation, all reactions (aerobic and anaerobic) are reported, and not only the aerobic biotransformations"
- [readme] Output formats and annotation options available: "Save the results into the specified CSV file or SDF file; Search PuChem for each product, and annotate with CID and synonyms"
- [readme] Number of steps parameter controls pathway depth simulation: "The number of steps for the prediction. This option can be set by the user for the EC-based, CYP450, Phase II, and Environmental microbial biotransformers. The default value is 1."
