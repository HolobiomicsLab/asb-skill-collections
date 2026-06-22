---
name: spectral-feature-chemical-assignment
description: Use when you have spectral feature data annotated by both in silico structural tools (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - SIRIUS
  - NPClassifier
  - GNPS
  - ClassyFire
  - ConCISE
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-feature-chemical-assignment

## Summary

Assign a single canonical chemical classification to each mass spectrometry spectral feature by reconciling multiple structural annotation sources (in silico tools and library matches) through a consensus algorithm. This skill is essential when you have competing or complementary chemical classifications from different annotation pipelines and need a unified, high-confidence class assignment per feature.

## When to use

You have spectral feature data annotated by both in silico structural tools (e.g., SIRIUS/CANOPUS) and library spectral matches with ClassyFire or NPClassifier ontology assignments, and you need to resolve conflicting or redundant classifications into a single consensus chemical class per feature. This is especially relevant when GNPS library match ontology data is unavailable or incomplete.

## When NOT to use

- Input spectral features lack both in silico annotations and library match data; consensus cannot be computed from a single source.
- Chemical classification ontologies have not been assigned to library matches or in silico predictions; preprocessing to add ontology data is required first.
- You require all candidate chemical classes ranked by confidence rather than a single consensus assignment; use raw annotation output directly instead.

## Inputs

- In silico structural annotations (e.g., SIRIUS output with CANOPUS summary table)
- Library spectral match file with ontology classifications (ClassyFire or NPClassifier)
- Feature-based molecular networking info file (Node_info.tsv or equivalent)
- GNPS task ID (optional, if data available) or manually curated ClassyFire batch results

## Outputs

- Consensus classification table mapping each spectral feature to superclass, class, and subclass
- Single canonical chemical classification per spectral feature

## How to apply

Load structural candidate annotations from in silico tools (e.g., SIRIUS output) and library match ontology classifications (ClassyFire or NPClassifier) from GNPS or manually retrieved sources. Parse and normalize structural candidate identifiers and their associated chemical classifications (superclass, class, subclass) from both sources. Apply ConCISE's consensus algorithm, which reconciles classifications by applying per-level percent agreement thresholds (default: superclass ≥50%, class ≥70%, subclass ≥70%) to select the dominant chemical class. Output a consensus classification table mapping each spectral feature to its single canonical chemical classification. If GNPS ontology data is unavailable, manually retrieve ClassyFire data by copying InChiKeys into the Fiehn Labs batch portal and merging results back into the library match file with correct column names (superclass, class, subclass).

## Related tools

- **SIRIUS** (Provides in silico structural candidate annotations and CANOPUS classifications for spectral features) — https://bio.informatik.uni-jena.de/software/
- **ClassyFire** (Supplies chemical ontology classifications (superclass, class, subclass) for both library matches and in silico candidates; can be queried via Fiehn Labs batch portal when GNPS data unavailable) — https://cfb.fiehnlab.ucdavis.edu/
- **NPClassifier** (Alternative chemical classification ontology source to ClassyFire; can be selected via GUI checkbox or CLI argument)
- **GNPS** (Provides spectral library matches with ClassyFire ontology annotations; currently no longer supplies ClassyFire data as of README date, requiring manual retrieval workaround) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ConCISE** (Core tool implementing the consensus classification algorithm; orchestrates integration of annotations and applies per-level thresholds) — https://github.com/Zquinlan/conCISE

## Examples

```
python3 src/conciseCLI.py 16616afa8edd490ea7e50cc316a20222 exampleFiles/canopus_summary.tsv exampleFiles/Node_info.tsv 50 70 70 False
```

## Evaluation signals

- Output consensus table contains exactly one superclass, class, and subclass entry per spectral feature with no missing values for features meeting confidence thresholds.
- Consensus class assignments are reproducible when run with identical threshold parameters (default or user-specified superclass %, class %, subclass %).
- For features with agreement below thresholds, verify that ConCISE either reports no consensus or flags uncertainty rather than selecting arbitrary candidates.
- Manual spot-check: verify that consensus class makes chemical sense given the in silico structure candidates and library match identities for a subset of features.
- Verify that ontology column names in merged library match files match expected format (superclass, class, subclass) when using manual ClassyFire retrieval workaround.

## Limitations

- GNPS has stopped supplying ClassyFire ontology information for spectral library matches as of the README publication date; manual retrieval via Fiehn Labs portal is required as a workaround, adding manual curation overhead.
- Consensus algorithm depends critically on agreement thresholds (default 50/70/70); low thresholds may inflate false consensus assignments, while high thresholds may leave many features unclassified.
- Performance degrades when in silico annotations and library matches disagree substantially or represent different chemical ontology conventions (e.g., mixing ClassyFire and NPClassifier without explicit harmonization).
- Requires correctly formatted ontology columns from both input sources; misaligned or missing column names will cause parsing failures or silent skipping of features.

## Evidence

- [readme] ConCISE utlizes the structural annotations provided by in silico tools such as SIRIUS: "ConCISE utlizes the structural annotations provided by in silico tools such as [SIRIUS]"
- [readme] ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations.: "ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations."
- [other] Apply ConCISE's consensus classification algorithm to reconcile multiple classification sources and select the dominant or highest-confidence chemical class per spectral feature.: "Apply ConCISE's consensus classification algorithm to reconcile multiple classification sources and select the dominant or highest-confidence chemical class per spectral feature."
- [readme] Currently GNPS has stopped supplying classyfire ontology information for spectral library matches: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches. There are two workarounds: 1) use NPClassifier instead of ClassyFire by checking the box in the GUI"
- [readme] You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier. Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass), you can use this file in place of the libraryID.: "You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' classyfire Batch identifier. Once these results are merged back into the original GNPS DBResult file with the correct"
- [readme] Superclass percent consensus (optional; default = 50), Class percent consensus (optional; default = 70), Subclass percent consensus (optional; default = 70): "Superclass percent consensus (optional; default = 50), Class percent consensus (optional; default = 70), Subclass percent consensus (optional; default = 70)"
