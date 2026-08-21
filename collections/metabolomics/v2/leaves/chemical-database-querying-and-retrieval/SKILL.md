---
name: chemical-database-querying-and-retrieval
description: Use when you have BioTransformer-predicted metabolite structures (in
  SMILES or InChI format) and need to identify which known compounds in public databases
  match those structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2258
  - http://edamontology.org/topic_0154
  tools:
  - BioTransformer
  - PubChem
  - ChEMBL
  - HMDB
  techniques:
  - NMR
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab). Env. module data CC-BY-NC-SA (enviPath/EAWAG).
    url: https://bitbucket.org/wishartlab/biotransformer3.0jar.git
  license_tier: noncommercial
  provenance_tier: literature
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

# chemical-database-querying-and-retrieval

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Query chemical structure databases (PubChem, ChEMBL, HMDB) with predicted metabolite structures to retrieve known compound identities and retrieve matching candidates ranked by structural similarity and biological plausibility. This skill transforms predicted SMILES or InChI structures into validated chemical identifiers and metadata for metabolite annotation.

## When to use

You have BioTransformer-predicted metabolite structures (in SMILES or InChI format) and need to identify which known compounds in public databases match those structures. Apply this skill when you want to assign chemical names, CAS numbers, and confidence scores to predictions within a specific biological context (mammalian, gut microbial, or environmental metabolism).

## When NOT to use

- The input metabolites are already experimentally validated and linked to reference standards—use direct reference matching instead.
- You need de novo structure determination from mass spectrometry or NMR—this skill assumes structures are already predicted.
- Commercial or proprietary compound databases are required; this skill is designed for open-access databases (PubChem, ChEMBL, HMDB).

## Inputs

- predicted metabolite structures (SMILES format)
- predicted metabolite structures (InChI format)
- organism or environmental context (mammalian, gut microbial, soil/aquatic)

## Outputs

- ranked candidate metabolite identifications (tabular)
- chemical name per candidate
- database identifiers (CAS, InChI, SMILES)
- confidence score per candidate
- structural similarity metrics

## How to apply

For each predicted metabolite from BioTransformer, query PubChem, ChEMBL, or HMDB using the structure in SMILES or InChI format as a lookup key. Retrieve all candidate compounds that match or are structurally similar to the query. Score and rank candidates by structural similarity to the prediction, breadth of database coverage (cross-referenced across PubChem/ChEMBL/HMDB), and biological plausibility in the target organism or environment. Compile results into a tabular output containing chemical name, identifier (CAS, InChI, SMILES), and a normalized confidence score reflecting the strength of the match and contextual applicability.

## Related tools

- **BioTransformer** (generates predicted metabolite structures (SMILES/InChI) that serve as input queries for database retrieval) — https://github.com/Wishartlab-openscience/Biotransformer
- **PubChem** (public chemical database queried to retrieve known compounds matching predicted metabolite structures)
- **ChEMBL** (chemical database queried for structural matches and candidate compound metadata)
- **HMDB** (human metabolome database queried for contextually relevant metabolite identifications in mammalian systems)

## Examples

```
java -jar biotransformer-3.0.0.jar -k cid -b allHuman -ismi "O[C@@H]1CC2=C(O)C=C(O)C=C2O[C@@H]1C1=CC=C(O)C(O)=C1" -osdf output.sdf -s 2 -m "292.0946;304.0946" -t 0.01 -a
```

## Evaluation signals

- Retrieved candidate list is non-empty and contains at least one structural match with confidence score ≥ 0.7 for predicted metabolites known to be in reference databases
- Ranked candidates maintain strict ordering by confidence score; candidates with higher structural similarity and broader database cross-reference coverage rank higher
- Output table contains all required fields (chemical name, CAS/InChI/SMILES identifiers, confidence score) with no missing values for top-ranked candidates
- Candidates are biologically plausible in the specified context (e.g., human metabolites do not include soil-specific xenobiotic degradation products)
- Structural similarity between query (predicted SMILES) and top candidate can be recomputed (e.g., Tanimoto coefficient) and matches reported score within ±0.05

## Limitations

- Identification quality depends on database coverage; rare or novel metabolites may have no matches even if structurally valid predictions.
- Structural similarity scoring may fail for highly regio-isomeric or stereoisomeric metabolites that are chemically similar but biologically distinct.
- Cross-database inconsistencies in chemical identifiers (CAS, SMILES canonicalization) may lead to false negatives or duplicates in candidate ranking.
- Biological plausibility filtering requires domain knowledge (e.g., organism-specific enzyme availability); algorithmic filtering alone may over- or under-rank candidates.

## Evidence

- [other] For each predicted metabolite, query chemical databases (PubChem, ChEMBL, or HMDB) to retrieve known compounds matching the predicted structure.: "For each predicted metabolite, query chemical databases (PubChem, ChEMBL, or HMDB) to retrieve known compounds matching the predicted structure."
- [other] Score and rank candidate identifications by structural similarity, database coverage, and biological plausibility within the relevant organism/environment context (mammalian, gut microbial, or soil/aquatic).: "Score and rank candidate identifications by structural similarity, database coverage, and biological plausibility within the relevant organism/environment context (mammalian, gut microbial, or"
- [other] Load the query compound identifier and BioTransformer's predicted metabolite structures (SMILES or InChI format).: "Load the query compound identifier and BioTransformer's predicted metabolite structures (SMILES or InChI format)."
- [readme] BioTransformer also assists scientists in metabolite identification, based on the metabolism prediction.: "BioTransformer also assists scientists in metabolite identification, based on the metabolism prediction."
- [other] Compile the ranked candidate list with chemical name, identifier (CAS, InChI, SMILES), and confidence score into a tabular output.: "Compile the ranked candidate list with chemical name, identifier (CAS, InChI, SMILES), and confidence score into a tabular output."
