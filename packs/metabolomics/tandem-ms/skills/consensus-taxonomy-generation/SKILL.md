---
name: consensus-taxonomy-generation
description: Use when when you have structural annotations from multiple sources (in silico predictions via SIRIUS/CANOPUS and GNPS spectral library matches) for the same molecular features and need a single authoritative taxonomy assignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3172
  tools:
  - NPClassifier
  - SIRIUS
  - GNPS
  - CANOPUS
  - ClassyFire
  - ConCISE
  - Fiehn Labs ClassyFire Batch
  techniques:
  - tandem-MS
derived_from:
- doi: 10.3390/metabo12121275
  title: ConCISE
evidence_spans:
- use NPClassifier instead of ClassyFire by checking the box in the GUI
- ConCISE utlizes the structural annotations provided by in silico tools such as [SIRIUS]
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

# consensus-taxonomy-generation

## Summary

Generates consensus ClassyFire or NPClassifier taxonomic classifications from multiple in silico structural annotation tools by voting on ontology levels (superclass, class, subclass) at configurable consensus thresholds. This skill reconciles conflicting annotations from SIRIUS/CANOPUS and GNPS spectral library matches into a single high-confidence classification.

## When to use

When you have structural annotations from multiple sources (in silico predictions via SIRIUS/CANOPUS and GNPS spectral library matches) for the same molecular features and need a single authoritative taxonomy assignment. Apply this skill when ClassyFire ontology data is available from GNPS or when NPClassifier taxonomies are substituted due to GNPS supply interruption.

## When NOT to use

- Input spectral library match data or in silico predictions lack ontology annotations (empty ClassyFire or NPClassifier fields); consensus voting requires at least one populated taxonomy source per feature.
- Single annotation source is available; consensus taxonomy requires multiple independent predictions to be meaningful.
- User requires ClassyFire ontologies but GNPS supply has not been restored and manual ClassyFire Batch lookup is not feasible.

## Inputs

- GNPS task ID or spectral library match file (DBResult format with InChiKeys)
- Canopus_summary.tsv file from SIRIUS/CANOPUS in silico predictions
- Node_info.tsv or equivalent networking information file from GNPS feature-based molecular networking
- Superclass, class, and subclass percent consensus thresholds (optional; defaults: 50, 70, 70)

## Outputs

- Consensus classification output file containing superclass, class, and subclass assignments per molecular feature
- Confidence or coverage metrics per ontology level

## How to apply

Load structural annotations from in silico tools (SIRIUS) and GNPS library spectral matches into ConCISE. Toggle the NPC argument (False for ClassyFire, True for NPClassifier) or check the corresponding GUI box. Run the classification step to vote on consensus at each ontology level using the superclass, class, and subclass percent consensus thresholds (default: 50%, 70%, 70% respectively). The workflow aggregates all taxonomic votes for each feature and retains only classifications meeting the specified threshold at each level. Verify output contains consensus classifications with no invocation of the undesired ontology source, and optionally compare consensus confidence or coverage metrics between NPClassifier and archived ClassyFire runs.

## Related tools

- **SIRIUS** (Provides in silico structural annotations and confidence scores that are classified by ClassyFire or NPClassifier ontologies) — https://bio.informatik.uni-jena.de/software/
- **CANOPUS** (Generates in silico predictions combined with SIRIUS annotations; outputs Canopus_summary.tsv used as input to consensus workflow)
- **GNPS** (Supplies spectral library matches with ClassyFire ontology information (when available) and feature-based molecular networking data) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ClassyFire** (Ontology source for taxonomic classification; substituted by NPClassifier when GNPS supply is unavailable)
- **NPClassifier** (Alternative validated ontology source toggled in via NPC argument or GUI checkbox when ClassyFire data is unavailable)
- **ConCISE** (Core application that orchestrates consensus voting across ontology levels) — https://github.com/Zquinlan/conCISE
- **Fiehn Labs ClassyFire Batch** (Manual lookup tool for retrieving ClassyFire ontologies by InChiKey when GNPS supply is interrupted) — https://cfb.fiehnlab.ucdavis.edu/

## Examples

```
python3 src/conciseCLI.py 16616afa8edd490ea7e50cc316a20222 exampleFiles/canopus_summary.tsv exampleFiles/Node_info.tsv 50 70 70 False
```

## Evaluation signals

- Output file contains consensus classifications (superclass, class, subclass) for all input molecular features without null values above the consensus thresholds.
- Verify that ClassyFire is not invoked in logs when NPC=True, and NPClassifier is not invoked when NPC=False.
- Consensus confidence (proportion of annotations agreeing at each level) meets or exceeds the specified thresholds (superclass ≥50%, class ≥70%, subclass ≥70% by default).
- Coverage metrics show percentage of features receiving consensus assignments at each ontology level; compare coverage and consensus confidence between NPClassifier and ClassyFire runs (if both available).
- Column names in merged output match expected ClassyFire/NPClassifier ontology schema: superclass, class, subclass (verify via schema validation or comparison with example outputs).

## Limitations

- GNPS has stopped supplying ClassyFire ontology information for spectral library matches, necessitating NPClassifier substitution or manual ClassyFire Batch lookup workaround.
- Consensus voting is sensitive to threshold settings; lowering thresholds increases coverage but reduces specificity, while raising thresholds improves confidence but may leave features unclassified.
- No changelog available to track feature compatibility or edge cases in version history.
- Performance and consensus quality depend on the availability and quality of in silico predictions from SIRIUS/CANOPUS and library spectral matches; sparse annotations reduce voting power.

## Evidence

- [readme] ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations.: "ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations."
- [readme] Currently GNPS has stopped supplying classyfire ontology information for spectral library matches. There are two workarounds: 1) use NPClassifier instead of ClassyFire by checking the box in the GUI or changing the NPC argument from False to True.: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches. There are two workarounds: 1) use NPClassifier instead of ClassyFire by checking the box in the GUI"
- [intro] NPClassifier is offered as a validated workaround when ClassyFire ontology information is unavailable, accessible by toggling the NPC argument from False to True or checking the corresponding GUI box.: "NPClassifier is offered as a validated workaround when ClassyFire ontology information is unavailable, accessible by toggling the NPC argument from False to True or checking the corresponding GUI box."
- [readme] Superclass percent consensus (optional; default = 50), Class percent consensus (optional; default = 70), Subclass percent consensus (optional; default = 70): "Superclass percent consensus (optional; default = 50), Class percent consensus (optional; default = 70), Subclass percent consensus (optional; default = 70)"
- [readme] ConCISE utlizes the structural annotations provided by in silico tools such as SIRIUS and CANOPUS combined with networking tools from GNPS: "ConCISE utlizes the structural annotations provided by in silico tools such as SIRIUS and CANOPUS combined with networking tools from GNPS"
