---
name: reaction-network-generation-and-expansion
description: Use when you have (1) a set of starting compounds as SMILES strings,
  (2) a collection of reaction rules in SMARTS format (e.g., from MetaCyc), and (3)
  a need to systematically predict all reachable products within a bounded number
  of generations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - MongoDB
  - RDKit
  - Python
  - eQuilibrator
  - MINE-Database (Pickaxe)
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans:
- The URI of the mongo database to connect to. Defaults to mongodb://localhost:27017
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pickaxe_cq
    doi: 10.1186/s12859-023-05149-8
    title: Pickaxe
  dedup_kept_from: coll_pickaxe_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-023-05149-8
  all_source_dois:
  - 10.1186/s12859-023-05149-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# reaction-network-generation-and-expansion

## Summary

Use Pickaxe to iteratively apply generalized reaction rules (encoded as SMARTS) to starting compounds across multiple generations, building a multi-generation reaction network. This skill is essential when you need to predict downstream metabolic or synthetic chemistry products from an initial compound set and rule library.

## When to use

Apply this skill when you have (1) a set of starting compounds as SMILES strings, (2) a collection of reaction rules in SMARTS format (e.g., from MetaCyc), and (3) a need to systematically predict all reachable products within a bounded number of generations. Use it when exploring metabolic pathway completeness, predicting synthetic feasibility, or generating hypothetical compound spaces for experimental validation.

## When NOT to use

- Starting compounds are already in a fully expanded reaction network; use this skill only when you need to generate the network de novo.
- Reaction rules are not available in SMARTS format or cannot be converted to RDKit-compatible pattern strings.
- Your goal is to predict only single-step reactions; use simpler rule-matching approaches rather than multi-generation expansion.

## Inputs

- SMILES strings (TSV or CSV file containing starting compounds)
- SMARTS-encoded reaction rules (TSV file)
- Coreactant list (TSV file)
- Optional: target compounds for filtering (SMILES strings)
- Optional: metabolomics peaks (mass and retention time)

## Outputs

- Reaction network (compounds and their transformation relationships)
- Compound set (all generated and starting compounds)
- TSV files (local output) or MongoDB collection (remote output)

## How to apply

Load your starting compounds from a TSV or CSV file containing SMILES strings, and load reaction rules (SMARTS-encoded) and coreactants from reference TSV files. Initialize a Pickaxe instance with these compound sets and rules, then configure the number of generations and optional flags (kekulize, neutralise, explicit hydrogen). Apply reaction rules iteratively using RDKit to compute chemical transformations. Before each generation, apply optional filters (e.g., Tanimoto similarity, mass tolerance, or custom compound selection) to reduce the compound set and control expansion. Write the resulting reaction network and compound list to TSV files or a MongoDB instance specified by a mongo URI.

## Related tools

- **RDKit** (Compute chemical transformations by applying SMARTS reaction rules to SMILES compounds; provides cheminformatic operations for structure manipulation and filtering.) — https://rdkit.org/docs/api-docs.html
- **Python** (Primary language for scripting and orchestrating Pickaxe workflow; used to load input files, configure parameters, and manage iterations.) — https://github.com/tyo-nu/MINE-Database
- **MongoDB** (Optional database backend for storing and retrieving generated reaction network and compound data.)
- **eQuilibrator** (Calculate thermodynamic values for generated compounds and reactions.)
- **MINE-Database (Pickaxe)** (Core framework for iterative reaction rule application, filtering, and network generation.) — https://github.com/tyo-nu/MINE-Database

## Examples

```
from minedatabase.pickaxe import Pickaxe; pickaxe = Pickaxe(compounds=cpd_list, rules=rule_list, coreactants=coreactants, generations=3, filters=['tanimoto']); pickaxe.execute(); pickaxe.write_to_tsv('./output')
```

## Evaluation signals

- Output TSV files or MongoDB collections are non-empty and contain expected schema: compound records (ID, SMILES, generation) and reaction records (reactants, products, rule applied).
- Number of compounds and reactions grows monotonically with generation number and rule count; verify against published coverage curves (e.g., 272 rules yield ~90% MetaCyc coverage).
- Spot-check: generated SMILES are chemically valid and pass RDKit sanitization; reactants and products are correctly paired via applied rules.
- Filtering applied before each generation reduces compound count; if no filters are applied, verify that the final compound set grows as expected.
- When integrating with metabolomics peaks or target compounds, verify that filtered compounds fall within mass tolerance or match target structure SMILES.

## Limitations

- Expansion can be computationally expensive: expanding 10,000 KEGG compounds with 272 rules generates 5 million compounds; use generation limits and filters to control size.
- Rule coverage is incomplete: 1221 rules are needed for 100% MetaCyc coverage; selecting fewer rules (e.g., 20 rules) covers only 50% of reactions and may miss important pathways.
- RDKit is not available on pip and must be installed via conda or other package managers, adding setup complexity.
- Chemical validity and thermodynamic feasibility are not automatically enforced; filters and optional thermodynamic scoring (via eQuilibrator) must be manually configured.
- Output can be very large; local TSV files or MongoDB storage must have sufficient disk/database capacity.

## Evidence

- [intro] Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds in order to predict reactions: "Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds in order to predict reactions"
- [intro] Pickaxe creates a network expansion by applying these reaction rules iteratively to your starting set of compounds, going for as many generations as you specify: "Pickaxe creates a network expansion by applying these reaction rules iteratively to your starting set of compounds, going for as many generations as you specify"
- [intro] Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded: "Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded"
- [intro] There are two ways to output data: 1. Writing to a mongo database that is specified by a `mongo uri`, either local or in mongo_uri.csv 2. Local .tsv files: "There are two ways to output data: 1. Writing to a mongo database that is specified by a `mongo uri`, either local or in mongo_uri.csv 2. Local .tsv files"
- [intro] Pickaxe executes a core workflow: (1) load input SMILES compounds and select reaction rules from metacyc_generalized, (2) apply rules iteratively across generations, (3) apply filters before each generation to reduce compounds for the next iteration, and (4) write output to MongoDB or local TSV files.: "Pickaxe executes a core workflow: (1) load input SMILES compounds and select reaction rules from metacyc_generalized, (2) apply rules iteratively across generations, (3) apply filters before each"
- [intro] For example, expanding 10,000 compounds from KEGG with 272 rules from metacyc yields 5 million compounds: "For example, expanding 10,000 compounds from KEGG with 272 rules from metacyc yields 5 million compounds"
- [other] Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools.: "Default filters are created using RDKit, a python library providing a collection of cheminformatic tools."
- [readme] An example file, [pickaxe_run_template.py](https://github.com/tyo-nu/MINE-Database/blob/master/pickaxe_run_template.py), provides a framework for running pickaxe through a python file. Feel free to download it and change it to your needs. The starting compounds, rules and cofactors, optional database information, and Pickaxe run options are specified.: "An example file provides a framework for running pickaxe through a python file. The starting compounds, rules and cofactors, optional database information, and Pickaxe run options are specified."
