---
name: classification-workflow-parameter-toggling
description: Use when gNPS has stopped supplying ClassyFire ontology information for your spectral library matches, or when ClassyFire data is missing for in silico structural annotations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - NPClassifier
  - SIRIUS
  - GNPS
  - ClassyFire
  - ConCISE
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

# classification-workflow-parameter-toggling

## Summary

Toggle between ClassyFire and NPClassifier ontology sources within the ConCISE consensus classification workflow to handle scenarios where GNPS ClassyFire ontology data is unavailable. This skill enables validation of consensus classifications using an alternative taxonomic framework without re-running the full structural annotation pipeline.

## When to use

Apply this skill when GNPS has stopped supplying ClassyFire ontology information for your spectral library matches, or when ClassyFire data is missing for in silico structural annotations. Use this before running the ConCISE consensus classification step if you need to generate valid ontology assignments despite ClassyFire unavailability.

## When NOT to use

- When ClassyFire ontology data is already available and accessible from GNPS; toggling to NPClassifier would introduce unnecessary methodological change.
- When input structural annotations are already at the consensus level or do not contain raw ClassyFire/NPClassifier taxonomy assignments to be reconciled.
- When the analysis requires strict adherence to ClassyFire ontological definitions for regulatory or publication-specific reasons.

## Inputs

- GNPS task ID or spectral library match file (with InChIKey and compound metadata)
- SIRIUS canopus_summary.tsv file (in silico structural annotations)
- Node_info.tsv or equivalent networking information file
- NPC parameter value (True or False toggle)

## Outputs

- Consensus classification file (CSV or TSV) with superclass, class, and subclass fields derived from NPClassifier ontologies
- Confidence or coverage metrics for each consensus level

## How to apply

Load ConCISE (via GUI or CLI) with structural annotations from SIRIUS or equivalent in silico tools already prepared. Toggle the NPC (NPClassifier) argument from False to True (CLI) or check the NPClassifier checkbox (GUI). Run the classification step, which will substitute NPClassifier-derived taxonomies for ClassyFire ontologies in both library match and in silico annotation consensus rounds. Generate consensus classification output using the specified consensus thresholds (default: 50% superclass, 70% class, 70% subclass). Verify in the output that ClassyFire invocations no longer appear and that NPClassifier taxonomic fields (superclass, class, subclass) are populated. Compare consensus confidence or coverage metrics between NPClassifier output and any archived ClassyFire runs to validate consistency.

## Related tools

- **NPClassifier** (Alternative ontology framework substituted for ClassyFire to assign taxonomic consensus classifications when ClassyFire data unavailable)
- **ClassyFire** (Primary ontology framework for compound classification; toggled off when unavailable via GNPS)
- **SIRIUS** (Provides structural annotations and in silico predictions (canopus_summary.tsv input) to ConCISE) — https://bio.informatik.uni-jena.de/software/
- **GNPS** (Source of library spectral matches and ClassyFire ontology assignments; when GNPS stops supplying ClassyFire data, this skill becomes necessary) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ConCISE** (Workflow engine that executes the classification consensus algorithm with configurable ontology source via NPC toggle) — https://github.com/Zquinlan/conCISE

## Examples

```
python3 src/conciseCLI.py 16616afa8edd490ea7e50cc316a20222 exampleFiles/canopus_summary.tsv exampleFiles/Node_info.tsv 50 70 70 True
```

## Evaluation signals

- Verify that output consensus classification fields (superclass, class, subclass) are populated with NPClassifier taxonomy terms, not ClassyFire terms.
- Confirm that no ClassyFire API calls or GNPS ClassyFire fetch operations appear in application logs or console output.
- Validate that consensus confidence scores are computed and reported for each ontology level (superclass, class, subclass) using the threshold parameters.
- Check that all input structural annotations are successfully mapped to NPClassifier ontology IDs without errors or missing values.
- Compare row counts and confidence distributions between NPClassifier and any archived ClassyFire output to ensure no data loss or systematic bias.

## Limitations

- NPClassifier taxonomy may differ from ClassyFire, potentially affecting downstream compound classification consistency or publication comparability.
- The skill requires structural annotations to already be available (from SIRIUS, CANOPUS, or library matches); it does not re-annotate structures.
- Manual workaround (copying InChIKeys to Fiehn Labs ClassyFire Batch tool and re-merging) may be necessary if NPClassifier output does not meet analysis requirements.
- Mac GUI is currently deprecated; command-line or MyBinder interfaces must be used on macOS systems.

## Evidence

- [readme] Currently GNPS has stopped supplying classyfire ontology information for spectral library matches: "Currently GNPS has stopped supplying classyfire ontology information for spectral library matches"
- [readme] use NPClassifier instead of ClassyFire by checking the box in the GUI or changing the NPC argument from False to True: "use NPClassifier instead of ClassyFire by checking the box in the GUI or changing the NPC argument from False to True"
- [readme] ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS: "ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies"
- [readme] Use NPClassifier in place of ClassyFire Ontologies (True or False; e.g., 'True' will utilize NPClassifier ontologies for both library matches and in silico matches): "Use NPClassifier in place of ClassyFire Ontologies (True or False; e.g., 'True' will utilize NPClassifier ontologies for both library matches and in silico matches)"
- [readme] ConCISE utlizes the structural annotations provided by in silico tools such as SIRIUS: "ConCISE utlizes the structural annotations provided by in silico tools such as SIRIUS"
