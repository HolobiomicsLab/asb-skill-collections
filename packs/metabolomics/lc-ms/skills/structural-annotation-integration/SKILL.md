---
name: structural-annotation-integration
description: Use when you have structural candidates from in silico tools (SIRIUS/CANOPUS) and library spectral matches from GNPS, but need to resolve conflicting or incomplete chemical classifications into a unified consensus.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
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
derived_from:
- doi: 10.3390/metabo12121275
  title: ConCISE
evidence_spans:
- ConCISE utlizes the structural annotations provided by in silico tools such as [SIRIUS]
- use NPClassifier instead of ClassyFire by checking the box in the GUI
- Currently GNPS has stopped supplying classyfire ontology information for spectral library matches
- Currently GNPS has stopped supplying classyfire ontology information for spectral library matches.
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

# structural-annotation-integration

## Summary

Integrate and reconcile multiple sources of chemical structural annotations (in silico predictions and spectral library matches) using ConCISE's consensus classification algorithm to assign a single canonical chemical ontology class to each spectral feature. This skill is essential when GNPS library matches provide incomplete or missing ClassyFire ontology data, requiring fallback to alternative annotation sources.

## When to use

You have structural candidates from in silico tools (SIRIUS/CANOPUS) and library spectral matches from GNPS, but need to resolve conflicting or incomplete chemical classifications into a unified consensus. Specifically, apply this skill when GNPS has stopped supplying ClassyFire ontology information for spectral library matches, forcing you to either substitute NPClassifier or manually retrieve ClassyFire data and merge it back into the GNPS result file.

## When NOT to use

- You have only library spectral matches without in silico structural predictions; ConCISE requires both sources to perform consensus reconciliation.
- Your structural annotations are already curated into a single agreed-upon chemical classification; consensus integration adds no value.
- ClassyFire or NPClassifier ontology data is completely unavailable and you cannot retrieve it from Fiehn Labs or other sources; ConCISE cannot operate without ontology mappings.

## Inputs

- SIRIUS canopus_summary.tsv file (in silico structural annotations with chemical class predictions)
- GNPS spectral library match DBResult file or libraryID file (library matches with ontology annotations)
- Node_info.tsv file (molecular networking information from GNPS)
- ClassyFire or NPClassifier ontology classifications (either from GNPS or manually retrieved via Fiehn Labs batch)

## Outputs

- Consensus classification table (TSV or equivalent) mapping spectral feature IDs to single canonical chemical classifications (superclass, class, subclass)
- Confidence/voting metrics per feature indicating how many annotation sources agreed on the consensus class

## How to apply

Load in silico structural annotations (e.g., SIRIUS canopus_summary output) and library match ontology data (ClassyFire or NPClassifier classifications from GNPS DBResult files) into ConCISE. Parse and normalize structural candidate identifiers and their associated chemical classifications from both sources. Apply ConCISE's consensus classification algorithm with user-defined percent thresholds (default: superclass 50%, class 70%, subclass 70%) to reconcile multiple classification sources and select the dominant chemical class per spectral feature. If ClassyFire ontology data from GNPS is unavailable, toggle the NPC argument to True or check the GUI NPClassifier box to substitute NPClassifier-derived taxonomies. Output a consensus classification table mapping each spectral feature to its single canonical chemical classification.

## Related tools

- **SIRIUS** (Provides in silico structural annotation candidates and CANOPUS chemical class predictions as input to ConCISE consensus integration) — https://bio.informatik.uni-jena.de/software/
- **ClassyFire** (Supplies chemical ontology classifications (superclass, class, subclass) for both library matches and in silico candidates; can be manually queried via Fiehn Labs batch when GNPS data is unavailable) — https://cfb.fiehnlab.ucdavis.edu/
- **NPClassifier** (Provides alternative ontology taxonomies when ClassyFire data from GNPS is unavailable; toggled via NPC argument or GUI checkbox)
- **GNPS** (Supplies spectral library matches and their ClassyFire ontology annotations (when available); provides molecular networking Node_info files) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ConCISE** (Core tool performing consensus classification algorithm; integrates in silico and library match annotations into single canonical chemical class per feature) — https://github.com/Zquinlan/conCISE

## Examples

```
python3 src/conciseCLI.py 16616afa8edd490ea7e50cc316a20222 exampleFiles/canopus_summary.tsv exampleFiles/Node_info.tsv 50 70 70 False
```

## Evaluation signals

- Output consensus classification table contains exactly one superclass, class, and subclass assignment per spectral feature with no missing or conflicting values.
- Voting/confidence metrics indicate the percentage of annotation sources that agreed on each consensus class; high agreement (e.g., >70% for class-level consensus) suggests robust consensus.
- When ClassyFire is substituted with NPClassifier (NPC=True), verify that ClassyFire is no longer invoked and that NPClassifier ontology term labels appear in the output.
- Cross-validate consensus assignments against archived runs using alternative ontology sources (ClassyFire vs. NPClassifier); coverage and confidence metrics should be documented for comparison.
- Sample spot-check: manually retrieve ClassyFire or NPClassifier data for 5–10 high-confidence spectral features and confirm that consensus class assignments match the most frequent ontology prediction across all input sources.

## Limitations

- GNPS has ceased supplying ClassyFire ontology information for spectral library matches; users must either substitute NPClassifier or manually retrieve and merge ClassyFire data from Fiehn Labs batch, adding manual curation overhead.
- Consensus classification depends on the quality and coverage of input in silico predictions and library matches; sparse or noisy annotations may yield low-confidence consensus (below user-defined thresholds) or result in features with no consensus assignment.
- The user-defined percent consensus thresholds (superclass 50%, class 70%, subclass 70%) are defaults and may require tuning for specific metabolite classes or experimental contexts; no guidance is provided for threshold optimization.
- ConCISE currently lacks a Mac GUI; Mac users must use the command-line interface or MyBinder virtual machine, reducing accessibility.

## Evidence

- [intro] ConCISE combines in silico structural annotations with library match ontology data: "ConCISE utlizes the structural annotations provided by in silico tools such as [SIRIUS]"
- [other] Consensus algorithm reconciles multiple classification sources: "Apply ConCISE's consensus classification algorithm to reconcile multiple classification sources and select the dominant or highest-confidence chemical class per spectral feature."
- [readme] NPClassifier offers validated workaround when ClassyFire is unavailable: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches. There are two workarounds: 1) use NPClassifier instead of ClassyFire by checking the box in the GUI"
- [readme] Manual ClassyFire retrieval via Fiehn Labs as alternative workflow: "You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' [classyfire Batch] identifier. Once these results are merged back into the original GNPS DBResult file with the correct"
- [readme] Default consensus thresholds for chemical classification levels: "Superclass percent consensus (optional; default = 50), Class percent consensus (optional; default = 70), Subclass percent consensus (optional; default = 70)"
