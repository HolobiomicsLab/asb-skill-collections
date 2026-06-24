---
name: compound-structure-enumeration-across-generations
description: Use when you have a set of seed compounds (as SMILES strings) and want
  to predict downstream products by systematically applying generalized reaction rules
  (e.g., from MetaCyc) across multiple reaction generations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - MongoDB
  - RDKit
  - Python
  - MetaCyc
  - eQuilibrator
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

# compound-structure-enumeration-across-generations

## Summary

Iteratively apply SMARTS-encoded reaction rules to an input compound set across multiple generations to predict and enumerate novel chemical structures in a reaction network expansion. This workflow uses RDKit to compute chemical transformations and optional filtering to manage network growth and compound set size.

## When to use

Use this skill when you have a set of seed compounds (as SMILES strings) and want to predict downstream products by systematically applying generalized reaction rules (e.g., from MetaCyc) across multiple reaction generations. Appropriate when exploring the full synthetic space reachable from a starting set or when generating in silico metabolic networks for pathway discovery or metabolomics validation.

## When NOT to use

- The input compound set is already exhaustively enumerated or closed (no novel structures expected); expansion will produce redundancy without new insights.
- Reaction rules are not generalized or are highly specific to a narrow substrate class, limiting applicability to diverse starting compounds.
- Computational resources are severely constrained and the estimated output size (e.g., 5 million compounds from 10,000 seeds with 272 rules) exceeds available storage or processing capacity.

## Inputs

- SMILES compound file (TSV or CSV with SMILES strings)
- reaction rule file (TSV, SMARTS-encoded rules from MetaCyc or other source)
- coreactant list (TSV file)
- filter parameters (optional: Tanimoto thresholds, metabolomics peaks with mass/RT tolerance, target structures)
- expansion parameters (number of generations, kekulization flag, neutralization flag, explicit hydrogen flag)

## Outputs

- TSV file containing predicted compounds with their SMILES, InChI, and molecular properties
- TSV file containing reaction network edges (reactant, product, rule applied)
- MongoDB collection (optional: compounds and reactions indexed for querying)
- Summary statistics (compound count per generation, filter removal counts)

## How to apply

Load starting compounds from a TSV or CSV file containing SMILES strings, and load reaction rules encoded as SMARTS patterns from a rule file (e.g., metacyc_generalized_rules.tsv). Initialize a Pickaxe instance with the compound set, coreactants, and rules, then configure expansion parameters including number of generations and optional flags (kekulize, neutralise, explicit hydrogen). Apply rules iteratively to the compound set using RDKit to compute chemical transformations for each generation. Between generations, apply specified filters (e.g., Tanimoto similarity, metabolomics, or target matching) to reduce the compound set size and focus expansion. Write the final reaction network and compound data to TSV files or a MongoDB instance for downstream analysis and querying.

## Related tools

- **RDKit** (compute chemical transformations by applying SMARTS reaction rules to compound structures) — https://rdkit.org
- **Python** (orchestrate file I/O, Pickaxe instance initialization, iteration logic, and output writing)
- **MongoDB** (optional persistent storage and indexing of generated compounds and reaction edges)
- **MetaCyc** (source of approximately 70,000 biological reactions condensed into ~1,200 generalized rules)
- **eQuilibrator** (optional thermodynamic scoring and filtering of predicted reactions)

## Examples

```
pickaxe = Pickaxe(compounds=compound_set, rules=rules_df, coreactants=coreactants_df, generations=3, kekulize=True, neutralise=True); pickaxe.run(); pickaxe.write_tsv('./output_dir/')
```

## Evaluation signals

- Output compound count and diversity increases as expected across generations; validate that kekulization, neutralization, and explicit hydrogen flags produce consistent SMILES canonicalization.
- Rule application is traceable: each output compound record should link to the parent compound(s) and the SMARTS rule that produced it; spot-check 10–20 reactions by hand using RDKit's reaction SMARTS validator.
- Filter statistics (e.g., Tanimoto threshold removal counts, metabolomics peak matches) are logged per generation; verify that filters reduce the compound set monotonically if applied.
- MongoDB queries (if used) return consistent results when filtering by generation, molecular weight range, or rule type; TSV files are valid (no truncated rows, all required columns present).
- Expansion terminates cleanly at the specified generation limit and does not crash due to invalid SMILES, missing coreactants, or rule parse errors; CPU/memory usage does not spike unexpectedly late in the run.

## Limitations

- Output size grows combinatorially with input compound count and rule set size: 10,000 input compounds × 272 rules can yield ~5 million compounds, straining storage and downstream analysis pipelines.
- Rule coverage is incomplete: 272 MetaCyc rules provide only ~90% coverage of MetaCyc reactions; reaching 99% or 100% coverage requires 956 or 1,221 rules respectively, which may introduce noise or off-target reactivity.
- No built-in handling of reaction regioselectivity, stereochemistry, or reaction mechanism; SMARTS rules assume topology-level transformation only.
- Filter choices strongly influence network topology: aggressive filtering (e.g., low Tanimoto threshold) may prune valid products; lenient filtering risks combinatorial explosion.
- Custom filter implementation requires direct modification of the minedatabase/filters.py file and manual integration into pickaxe_run.py; no plugin or declarative configuration interface is documented.

## Evidence

- [intro] Pickaxe executes a core workflow: (1) load input SMILES compounds and select reaction rules from metacyc_generalized, (2) apply rules iteratively across generations, (3) apply filters before each generation to reduce compounds for the next iteration, and (4) write output to MongoDB or local TSV files.: "Pickaxe executes a core workflow: (1) load input SMILES compounds and select reaction rules from metacyc_generalized, (2) apply rules iteratively across generations, (3) apply filters before each"
- [intro] Pickaxe applies reaction rules iteratively to your starting set of compounds, going for as many generations as you specify: "Pickaxe creates a network expansion by applying these reaction rules iteratively to your starting set of compounds, going for as many generations as you specify"
- [intro] Apply reaction rules iteratively across generations using RDKit to compute chemical transformations: "Apply reaction rules iteratively to the compound set for the specified number of generations using RDKit to compute chemical transformations."
- [intro] Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded: "Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded"
- [intro] There are two ways to output data: 1. Writing to a mongo database that is specified by a `mongo uri`, either local or in mongo_uri.csv 2. Local .tsv files: "There are two ways to output data: 1. Writing to a mongo database that is specified by a `mongo uri`, either local or in mongo_uri.csv 2. Local .tsv files"
- [intro] For example, expanding 10,000 compounds from KEGG with 272 rules from metacyc yields 5 million compounds: "For example, expanding 10,000 compounds from KEGG with 272 rules from metacyc yields 5 million compounds"
- [readme] An example file, pickaxe_run_template.py, provides a framework for running pickaxe through a python file. The starting compounds, rules and cofactors, optional database information, and Pickaxe run options are specified.: "An example file, pickaxe_run_template.py, provides a framework for running pickaxe through a python file. The starting compounds, rules and cofactors, optional database information, and Pickaxe run"
