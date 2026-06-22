---
name: biological-reactant-pair-mapping-kegg
description: Use when constructing or enriching a chemical formula database that must capture not just structural similarity (DBEdges) but also biological co-occurrence patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0601
  - http://edamontology.org/topic_3172
  tools:
  - SMART
  - KEGG
  techniques:
  - LC-MS
  - MS-imaging
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.4c06210
  title: SMART
evidence_spans:
- we present SMART, an open-source platform designed for precise formula assignment in mass spectrometry imaging
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_cq
    doi: 10.1021/acs.analchem.4c06210
    title: SMART
  dedup_kept_from: coll_smart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06210
  all_source_dois:
  - 10.1021/acs.analchem.4c06210
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biological-reactant-pair-mapping-kegg

## Summary

Extract and link chemical formulae that participate together in metabolic reactions by retrieving reactant pairs from KEGG and constructing BioEdges—graph edges that encode biological relationships between compounds. This skill bridges chemical structure databases with metabolic context, enabling formula assignment methods to score candidates based on whether they co-occur in known biochemical transformations.

## When to use

Apply this skill when constructing or enriching a chemical formula database that must capture not just structural similarity (DBEdges) but also biological co-occurrence patterns. Specifically: you have a collection of chemical formulae from multiple repositories (HMDB, ChEMBL, PubChem) and want to annotate which pairs participate together as substrate–product or cofactor relationships in metabolic pathways. This is essential if your downstream task is mass spectrometry imaging formula assignment, where a candidate formula gains credibility if its neighbors in the formula network are biochemically related.

## When NOT to use

- Your input is LC-MS/MS data without spatial context—SMART and BioEdge scoring are optimized for spatially-resolved metabolomics, where tissue-specific metabolic patterns are critical; conventional LC-MS may benefit less from metabolic co-occurrence signals.
- You are working with non-model organisms or specialized databases not covered by KEGG—BioEdges will be sparse or absent, reducing their utility for scoring.
- Your formula candidates already have orthogonal biological validation (e.g., isotope labeling, direct biochemical assay)—BioEdge enrichment adds marginal value and increases computational overhead.

## Inputs

- KEGG biological reactant pair list (compound ID pairs from enzymatic reactions)
- Unified formula database with existing chemical identifiers (InChI, SMILES, or KEGG compound IDs)
- Cross-reference mapping table (KEGG ID ↔ HMDB/ChEMBL/PubChem ID)

## Outputs

- BioEdge list: tuples of (formula_1_ID, formula_2_ID, reaction_ID, edge_metadata)
- Enhanced graph structure: merged DBEdges and BioEdges with unified node identifiers
- Indexed formula network: serialized database file enabling efficient lookup of formula neighbors by biological relationship

## How to apply

Retrieve KEGG biological reactant pairs—compounds that appear together as reactants, products, or cofactors in enzymatic reactions. For each pair, resolve the chemical identifiers (e.g., KEGG compound IDs, InChI, or SMILES) to their corresponding entries in your unified formula database using cross-reference mapping. Construct a directed or undirected edge (BioEdge) between the two formulae, optionally annotating it with reaction ID, enzyme commission number, or pathway category. Merge these BioEdges into your existing graph structure alongside DBEdges (structural relationships). During scoring of candidate formulae for a given m/z value, formulae that are connected via BioEdges to already-identified formula neighbors receive higher scores, on the rationale that co-occurrence in metabolic reactions is a strong signal of biological relevance in the tissue being imaged.

## Related tools

- **SMART** (Formula assignment platform that uses BioEdges from KEGG to score and rank candidate formulae for m/z values in spatially-resolved metabolomics data) — https://github.com/bioinfo-ibms-pumc/SMART
- **KEGG** (Source repository of biological reactant pairs (substrate–product relationships in enzymatic reactions) from which BioEdges are extracted)

## Examples

```
py SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0
```

## Evaluation signals

- All BioEdges connect formulae that exist in the unified formula database (no orphaned or unresolved nodes).
- BioEdge density and coverage: measure the proportion of formulae that have ≥1 biological neighbor; expect 40–70% coverage for human metabolomics given KEGG's focus on central metabolism.
- Scoring improvement: formulae ranked by BioEdge-augmented scores should show higher precision (% correctly assigned) on reference datasets compared to DBEdge-only scoring.
- Cross-reference validation: spot-check a sample of BioEdges against KEGG pathway maps to confirm reaction IDs and participant compounds are biochemically sound.
- Database integrity: verify the serialized output can be deserialized and queried without corruption; test m/z lookups return expected formula sets with correct edge annotations.

## Limitations

- KEGG coverage is biased toward model organisms and primary metabolism; specialized or xenobiotic pathways are underrepresented.
- Cross-reference resolution between KEGG and other databases (HMDB, ChEMBL, PubChem) is not deterministic; incorrect ID mappings will propagate false or spurious BioEdges.
- BioEdges are undirected or weakly directed in most implementations, discarding stoichiometry and enzyme specificity; a single edge cannot encode whether a compound is primary substrate vs. allosteric regulator.
- The utility of BioEdges depends on the metabolic relevance of the tissue and sample type being imaged; in non-model tissues or artificial samples, co-occurrence in KEGG may not predict actual co-abundance.

## Evidence

- [intro] Extract DBEdges and BioEdges methodology: "SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG biological reactant"
- [intro] BioEdge scoring rationale: "scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values"
- [readme] KEGG as BioEdge source in workflow: "Retrieve KEGG biological reactant pairs and construct BioEdges that link formulae involved in metabolic reactions"
