---
name: chemical-transformation-prediction-via-rule-application
description: 'Use when you have: (1) a set of starting compounds in SMILES format;
  (2) a library of reaction rules (SMARTS-encoded) from MetaCyc or custom sources;
  (3) a need to discover predicted reaction products and novel compounds across multiple
  reaction generations; and (4) constraints (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3324
  - http://edamontology.org/topic_0602
  tools:
  - MongoDB
  - RDKit
  - eQuilibrator
  - mordred
  license_tier: open
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

# chemical-transformation-prediction-via-rule-application

## Summary

Apply SMARTS-encoded reaction rules iteratively to a starting set of compounds to predict multi-generation reaction networks and discover novel compounds. This skill is essential when exploring the synthetic or metabolic space reachable from known starting materials under a defined set of reaction transformation patterns.

## When to use

Use this skill when you have: (1) a set of starting compounds in SMILES format; (2) a library of reaction rules (SMARTS-encoded) from MetaCyc or custom sources; (3) a need to discover predicted reaction products and novel compounds across multiple reaction generations; and (4) constraints (e.g., mass tolerance, Tanimoto similarity, target structure matching) that should gate expansion at each generation.

## When NOT to use

- When starting compounds are not available in SMILES format or when the reaction chemistry cannot be encoded as SMARTS patterns.
- When chemical transformations have strong stereochemical constraints that SMARTS-based pattern matching cannot capture.
- When the desired reaction space is better explored through literature review or experimental synthesis rather than rule-based prediction.

## Inputs

- Starting compounds (TSV or CSV file with SMILES strings)
- Reaction rules (TSV file with SMARTS-encoded rules, e.g., metacyc_generalized_rules.tsv)
- Coreactant list (TSV file)
- Filter configuration (optional: target compound file, Tanimoto thresholds, metabolomics peak list)

## Outputs

- Reaction network (TSV file or MongoDB collection with edges representing predicted reactions)
- Compound set (TSV file or MongoDB collection with compound structures, properties, and generation membership)
- Filter summary (stdout or logs reporting compounds retained/removed at each generation)

## How to apply

Initialize Pickaxe with starting SMILES compounds, load reaction rules (SMARTS-encoded) and coreactants from TSV files, and configure expansion parameters including number of generations and optional flags (kekulize, neutralise, explicit hydrogen). Apply rules iteratively using RDKit to compute chemical transformations on the compound set. Before each generation, apply filters (e.g., Tanimoto threshold, metabolomics matching, target filtering) to reduce the compound set and control network growth. Write the final reaction network and compound data to TSV files or a MongoDB instance. Rule coverage varies with selection size: 20 rules provide 50% MetaCyc coverage, 272 rules 90%, and 1221 rules 100% coverage.

## Related tools

- **RDKit** (Computes chemical transformations by applying SMARTS-encoded reaction rules to SMILES compounds) — https://rdkit.org/
- **MongoDB** (Stores and retrieves reaction network and compound data via mongo URI)
- **eQuilibrator** (Calculates thermodynamic values for predicted reactions)
- **mordred** (Computes molecular descriptors for filtering and downstream ML feature selection)

## Examples

```
from minedatabase.pickaxe import Pickaxe; pickaxe = Pickaxe(compounds='./compounds.csv', rules='./metacyc_generalized_rules.tsv', coreactants='./metacyc_coreactants.tsv', generations=2, filters=['Tanimoto'], output_type='tsv', output_dir='./results')
```

## Evaluation signals

- Compound count at each generation increases monotonically or plateaus when filters are applied, and output TSV/MongoDB records match schema (SMILES, inchi, generation, reaction_id).
- Filter application reduces compound set size predictably: Tanimoto threshold filter returns only compounds with max similarity ≥ threshold; metabolomics filter returns only compounds within mass ± tolerance.
- Output reaction network edges have SMARTS rule IDs, reactant SMILES, product SMILES, and coreactant information; no NaN or malformed SMILES.
- Network statistics (number of unique compounds, reactions, generations reached) match expected bounds for rule coverage (272 rules on 10,000 KEGG compounds yields ~5 million predicted compounds in literature).
- Comparison of predicted compounds to target structures (if provided) shows target filtering achieved expected recall and precision.

## Limitations

- SMARTS-based rules capture reaction transformation patterns but do not predict regioselectivity, stereoselectivity, or reaction yield—only connectivity changes.
- Network expansion grows combinatorially; 10,000 starting compounds with 272 rules can generate 5 million compounds, requiring aggressive filtering or coreactant constraints to remain computationally tractable.
- Rule coverage plateaus (272 MetaCyc rules cover 90% of MetaCyc reactions; 1221 rules cover 100%), meaning rare or non-standard reactions are not predicted.
- Coreactants and cofactors must be specified in advance; prediction cannot occur without their availability in the input list.
- No changelog found for version tracking; reproducibility depends on archiving exact rule and coreactant TSV files used.

## Evidence

- [intro] Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds in order to predict reactions: "Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds in order to predict reactions"
- [intro] Pickaxe creates a network expansion by applying these reaction rules iteratively to your starting set of compounds, going for as many generations as you specify: "Pickaxe creates a network expansion by applying these reaction rules iteratively to your starting set of compounds, going for as many generations as you specify"
- [intro] Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded: "Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded"
- [intro] Rules are generated using `SMARTS` which represent reactions in a string: "Rules are generated using `SMARTS` which represent reactions in a string"
- [intro] For example, expanding 10,000 compounds from KEGG with 272 rules from metacyc yields 5 million compounds: "For example, expanding 10,000 compounds from KEGG with 272 rules from metacyc yields 5 million compounds"
- [intro] There are two ways to output data: 1. Writing to a mongo database that is specified by a `mongo uri`, either local or in mongo_uri.csv 2. Local .tsv files: "There are two ways to output data: 1. Writing to a mongo database that is specified by a `mongo uri`, either local or in mongo_uri.csv 2. Local .tsv files"
- [intro] A set of biological reaction rules and cofactors are provided by default. These consist of approximately 70,000 MetaCyc reactions condensed into generic rules: "A set of biological reaction rules and cofactors are provided by default. These consist of approximately 70,000 MetaCyc reactions condensed into generic rules"
- [readme] An example file, pickaxe_run_template.py, provides a framework for running pickaxe through a python file. Feel free to download it and change it to your needs. The starting compounds, rules and cofactors, optional database information, and Pickaxe run options are specified.: "An example file, pickaxe_run_template.py, provides a framework for running pickaxe through a python file. Feel free to download it and change it to your needs. The starting compounds, rules and"
