---
name: consensus-classification-reconciliation
description: Use when you have spectral features annotated by both in silico structural
  prediction tools (e.g., SIRIUS/CANOPUS) and spectral library matching (GNPS), and
  you need a single authoritative chemical classification per feature rather than
  a list of competing candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3346
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - SIRIUS
  - NPClassifier
  - GNPS
  - ClassyFire
  - ConCISE
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3390/metabo12121275
  title: ConCISE
evidence_spans:
- ConCISE utlizes the structural annotations provided by in silico tools such as [SIRIUS]
- use NPClassifier instead of ClassyFire by checking the box in the GUI
- Currently GNPS has stopped supplying classyfire ontology information for spectral
  library matches
- Currently GNPS has stopped supplying classyfire ontology information for spectral
  library matches.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_concise_cq
    doi: 10.3390/metabo12121275
    title: ConCISE
  dedup_kept_from: coll_concise_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12121275
  all_source_dois:
  - 10.3390/metabo12121275
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# consensus-classification-reconciliation

## Summary

Reconcile multiple chemical classification sources (in silico structural predictions and spectral library matches) into a single consensus chemical class per spectral feature using ConCISE's ontology-aware voting algorithm. This skill is essential when you have competing or complementary structural annotations from tools like SIRIUS and GNPS library matches that must be unified into a canonical chemical classification for downstream chemical interpretation.

## When to use

Apply this skill when you have spectral features annotated by both in silico structural prediction tools (e.g., SIRIUS/CANOPUS) and spectral library matching (GNPS), and you need a single authoritative chemical classification per feature rather than a list of competing candidates. This is particularly relevant when GNPS library matches include ClassyFire or NPClassifier ontology data that can be reconciled with in silico predictions.

## When NOT to use

- Input spectral library match data lacks any ontology annotations (ClassyFire/NPClassifier columns); consensus cannot be computed without at least one annotated source.
- Your goal is to retain all candidate annotations rather than select a single class; consensus reconciliation deliberately discards low-confidence or minority annotations.
- In silico tool outputs are unavailable; ConCISE requires both library and in silico sources to achieve meaningful consensus voting.

## Inputs

- In silico structural annotations with chemical classifications (SIRIUS/CANOPUS output)
- Spectral library match file with ontology data (GNPS DBResult with ClassyFire or NPClassifier columns)
- GNPS networking node information file (Node_info.tsv)
- Optional: manually retrieved ClassyFire batch results (InChiKey-indexed)

## Outputs

- Consensus classification table mapping spectral features to canonical chemical classes
- Feature × ontology rank matrix (superclass, class, subclass per feature)

## How to apply

Load the in silico structural annotations (typically SIRIUS output with CANOPUS chemical classifications) and the library spectral match file containing ontology classifications (ClassyFire superclass/class/subclass or NPClassifier). Parse and normalize the chemical candidate identifiers and their associated ontology labels from both sources. Apply ConCISE's consensus classification algorithm, which voting-weights each source and selects the dominant chemical class when agreement exceeds configurable thresholds (default: 50% for superclass, 70% for class/subclass). If GNPS ontology data is unavailable, manually retrieve ClassyFire annotations via the Fiehn Labs batch tool using InChiKeys from library matches, then merge the results back into the GNPS file using standardized column names (superclass, class, subclass) before consensus reconciliation. Output a consensus classification table mapping each spectral feature to its single canonical chemical class at the chosen taxonomic rank.

## Related tools

- **SIRIUS** (Generates in silico structural candidate annotations and CANOPUS chemical classification predictions for spectral features) — https://bio.informatik.uni-jena.de/software/
- **GNPS** (Supplies spectral library matches with associated ClassyFire/NPClassifier ontology data and molecular networking context) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ClassyFire** (Provides chemical taxonomy ontologies (superclass/class/subclass) for annotating structural candidates and library matches) — https://cfb.fiehnlab.ucdavis.edu/
- **NPClassifier** (Alternative chemical taxonomy ontology usable in place of ClassyFire via GUI or CLI flag (NPC=True))
- **ConCISE** (Core consensus reconciliation engine that votes across annotation sources and outputs unified chemical classifications) — https://github.com/Zquinlan/conCISE

## Examples

```
python3 src/conciseCLI.py 16616afa8edd490ea7e50cc316a20222 exampleFiles/canopus_summary.tsv exampleFiles/Node_info.tsv 50 70 70 False
```

## Evaluation signals

- Each spectral feature has exactly one chemical class assigned at each ontology rank (superclass, class, subclass); no null or multi-valued entries in the consensus output table.
- Consensus classes match or exceed the configured agreement thresholds (default 50% superclass, 70% class/subclass); inspect voting tallies to confirm consensus strength.
- Cross-validation: re-run with adjusted thresholds (e.g., 60% instead of 50%) and verify that high-confidence classes remain stable while borderline calls shift predictably.
- Spot-check a sample of features where in silico and library annotations were originally discordant; the consensus class should correspond to the source with higher ontology evidence or stronger structural prediction score.
- All output feature IDs are traceable back to input spectral features; no features are dropped or merged during consensus reconciliation unless explicitly filtered.

## Limitations

- GNPS has stopped supplying ClassyFire ontology information for spectral library matches; manual retrieval via Fiehn Labs batch tool (using InChiKeys) is required as a workaround when GNPS data is missing.
- Consensus quality depends critically on agreement between in silico and library sources; features with conflicting predictions or isolated annotations may yield low-confidence consensus classes below the voting thresholds.
- ClassyFire and NPClassifier are mutually exclusive within a single ConCISE run; if library matches use ClassyFire but in silico predictions use NPClassifier (or vice versa), the two ontologies cannot be directly voted without prior harmonization.
- Consensus thresholds (50%, 70%) are global parameters applied uniformly; no per-rank or per-feature adaptive thresholds are supported, so rare chemical classes may be systematically under-represented if they appear in only one source.
- Column naming in manually merged ClassyFire data must exactly match expected field names (superclass, class, subclass); typos or case mismatches will cause parsing errors or silent data loss.

## Evidence

- [intro] ConCISE combines in silico structural annotations with library match ontology data: "ConCISE utlizes the structural annotations provided by in silico tools such as [SIRIUS]"
- [intro] Consensus algorithm reconciles multiple classification sources: "ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations."
- [readme] GNPS library ontology data is no longer available; manual retrieval via Fiehn Labs is an alternative: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches. There are two workarounds: 1) use NPClassifier instead of ClassyFire by checking the box in the GUI"
- [readme] Output and threshold parameters for consensus reconciliation: "Superclass percent consensus (optional; default = 50), Class percent consensus (optional; default = 70), Subclass percent consensus (optional; default = 70)"
- [readme] Consensus reconciliation merges column-normalized ontology data: "Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass), you can use this file in place of the libraryID."
